"""Script reproducible para ejecutar >= 4 corridas comparables en MLflow + Model Registry."""

from __future__ import annotations

import argparse
import base64
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import mlflow
import numpy as np
import pandas as pd
from mlflow.models import infer_signature
from mlflow.tracking import MlflowClient

from defect_inspector.inference.config import NEU_CLASSES, ModelSpecConfig
from defect_inspector.inference.model_loader import OnnxDefectClassifier
from defect_inspector.mlops.eval_data import (
    EvalSample,
    load_reproducible_eval_batch,
)
from defect_inspector.mlops.metrics import (
    compute_evaluation_metrics,
    save_confusion_matrix_png,
)
from defect_inspector.mlops.packaging import (
    NEUDefectPyFunc,
    write_sample_predictions_and_report,
)
from defect_inspector.mlops.tracking import (
    MlflowSettings,
    check_mlflow_server,
    configure_mlflow,
)
from defect_inspector.services.inspection_service import DefectInspectionService


@dataclass(frozen=True, slots=True)
class EvalRunPlan:
    """Configuración comparable de inferencia/postprocesamiento sin hiperparámetros de entreno."""

    run_name: str
    apply_clahe: bool
    conf_threshold: float
    register_model: bool = False
    alias: str = ""


DEFAULT_PLANS: tuple[EvalRunPlan, ...] = (
    EvalRunPlan("eval-01-baseline-raw-t050", apply_clahe=False, conf_threshold=0.50),
    EvalRunPlan("eval-02-hitl-strict-t070", apply_clahe=False, conf_threshold=0.70),
    EvalRunPlan(
        "eval-03-clahe-hitl-t070",
        apply_clahe=True,
        conf_threshold=0.70,
        register_model=True,
        alias="production",
    ),
    EvalRunPlan(
        "eval-04-clahe-conservative-t085", apply_clahe=True, conf_threshold=0.85
    ),
)


def _git_short_sha() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True
        )
        return out.strip()
    except Exception:
        return "unknown"


def evaluate_plan_once(
    service: DefectInspectionService,
    samples: list[EvalSample],
    plan: EvalRunPlan,
) -> tuple[dict[str, float], list[int], list[int], list[dict[str, object]]]:
    """Ejecuta un lote completo sobre el servicio real de Capa 2."""
    y_true_idx: list[int] = []
    y_pred_idx: list[int] = []
    probs_rows: list[list[float]] = []
    latencies: list[float] = []
    reviews: list[bool] = []
    sample_rows: list[dict[str, object]] = []
    class_index = {c: i for i, c in enumerate(NEU_CLASSES)}

    for idx, sample in enumerate(samples):
        dto = service.inspect(
            image_bytes=sample.image_bytes,
            filename=sample.filename,
            conf_threshold=plan.conf_threshold,
            apply_clahe=plan.apply_clahe,
            request_id=f"{plan.run_name}-{idx:03d}",
        )
        y_true_idx.append(sample.class_index)
        y_pred_idx.append(class_index[dto.predicted_class])
        score_map = {s.class_name: s.probability for s in dto.scores}
        probs_rows.append([float(score_map[c]) for c in NEU_CLASSES])
        latencies.append(dto.latency_ms)
        reviews.append(dto.requires_human_review)

        if idx % max(1, len(samples) // 24) == 0:
            sample_rows.append(
                {
                    "filename": sample.filename,
                    "true_class": sample.true_label,
                    "predicted_class": dto.predicted_class,
                    "confidence": dto.confidence,
                    "decision_status": dto.decision_status,
                    "latency_ms": dto.latency_ms,
                }
            )

    metrics = compute_evaluation_metrics(
        y_true_idx=y_true_idx,
        y_pred_idx=y_pred_idx,
        y_prob_matrix=np.asarray(probs_rows, dtype=np.float64),
        latencies_ms=latencies,
        requires_review_flags=reviews,
    )
    return metrics, y_true_idx, y_pred_idx, sample_rows


def run_evaluation_suite(
    plans: tuple[EvalRunPlan, ...] = DEFAULT_PLANS,
    per_class: int = 20,
    allow_download: bool = True,
    require_live_server: bool = True,
) -> list[dict[str, object]]:
    """Corre las comparativas configuradas y registra corridas + modelo en MLflow."""
    ml_cfg = MlflowSettings.from_env()
    if require_live_server and not check_mlflow_server(ml_cfg.tracking_uri):
        raise RuntimeError(
            f"Servidor MLflow no responde en {ml_cfg.tracking_uri}. "
            "Inicia primero: uv run mlflow server --backend-store-uri sqlite:///mlflow.db "
            "--default-artifact-root ./mlruns --host 127.0.0.1 --port 5050 --workers 1"
        )
    configure_mlflow(ml_cfg)

    repo_root = Path(__file__).resolve().parent.parent
    model_cfg = ModelSpecConfig.from_env(root_dir=repo_root)
    classifier = OnnxDefectClassifier(config=model_cfg)
    service = DefectInspectionService(classifier=classifier, config=model_cfg)
    samples, dataset_source = load_reproducible_eval_batch(
        cache_dir=repo_root / "data" / "raw" / "eval_cache",
        per_class=per_class,
        allow_download=allow_download,
    )
    sha = _git_short_sha()
    summary: list[dict[str, object]] = []

    sample_b64 = base64.b64encode(samples[0].image_bytes).decode("ascii")
    sig_input = pd.DataFrame([{"image_base64": sample_b64}])
    sig_output = pd.DataFrame([{"predicted_class": NEU_CLASSES[0], "confidence": 0.95}])
    signature = infer_signature(sig_input, sig_output)

    for plan in plans:
        metrics, y_true_idx, y_pred_idx, sample_rows = evaluate_plan_once(
            service, samples, plan
        )
        params: dict[str, object] = {
            "model_id": model_cfg.model_id,
            "model_revision": model_cfg.revision,
            "input_size": model_cfg.input_size,
            "apply_clahe": plan.apply_clahe,
            "clahe_clip_limit": 2.0 if plan.apply_clahe else 0.0,
            "conf_threshold": plan.conf_threshold,
            "eval_samples": len(samples),
            "dataset_source": dataset_source,
        }
        tags = {
            "project": "entrega-m3-inspeccion-industrial",
            "group": "Grupo 9",
            "author": "Omar David Sanchez Jimenez",
            "license": model_cfg.license_name,
            "model_revision": model_cfg.revision,
            "architecture": "gRPC + Thin HTTP Gateway + HTML/ESM",
            "dataset_source": dataset_source,
            "git_commit": sha,
        }

        with mlflow.start_run(run_name=plan.run_name) as run:
            mlflow.log_params(params)
            mlflow.log_metrics(metrics)
            mlflow.set_tags(tags)

            with tempfile.TemporaryDirectory() as tmp:
                tmp_dir = Path(tmp)
                cm_path = save_confusion_matrix_png(
                    y_true_idx=y_true_idx,
                    y_pred_idx=y_pred_idx,
                    class_names=NEU_CLASSES,
                    out_path=tmp_dir / "confusion_matrix.png",
                    title=f"Matriz de Confusión — {plan.run_name}",
                )
                s_path, r_path = write_sample_predictions_and_report(
                    out_dir=tmp_dir,
                    run_name=plan.run_name,
                    params=params,
                    metrics=metrics,
                    sample_rows=sample_rows,
                )
                mlflow.log_artifact(str(cm_path), artifact_path="plots")
                mlflow.log_artifact(str(s_path), artifact_path="reports")
                mlflow.log_artifact(str(r_path), artifact_path="reports")

                if plan.register_model:
                    model_info = mlflow.pyfunc.log_model(
                        name="neu_defect_inspector_model",
                        python_model=NEUDefectPyFunc(),
                        artifacts={"onnx_model": str(model_cfg.onnx_path)},
                        signature=signature,
                        pip_requirements=[
                            "onnxruntime",
                            "numpy",
                            "opencv-python-headless",
                            "pandas",
                        ],
                        registered_model_name=ml_cfg.registered_model_name,
                    )
                    if plan.alias and model_info.registered_model_version is not None:
                        client = MlflowClient(tracking_uri=ml_cfg.tracking_uri)
                        client.set_registered_model_alias(
                            name=ml_cfg.registered_model_name,
                            alias=plan.alias,
                            version=str(model_info.registered_model_version),
                        )

            summary.append(
                {
                    "run_id": run.info.run_id,
                    "run_name": plan.run_name,
                    "metrics": metrics,
                }
            )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluación reproducible MLflow M3")
    parser.add_argument("--per-class", type=int, default=20)
    parser.add_argument("--offline-only", action="store_true")
    args = parser.parse_args()
    results = run_evaluation_suite(
        per_class=args.per_class,
        allow_download=not args.offline_only,
        require_live_server=True,
    )
    for row in results:
        print(f"[MLflow OK] {row['run_name']} ({row['run_id']}) -> {row['metrics']}")


if __name__ == "__main__":
    main()
