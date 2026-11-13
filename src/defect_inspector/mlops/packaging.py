"""Empaquetado MLflow PyFunc (envolviendo ONNX Runtime) y generación de artefactos."""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

import mlflow.pyfunc
import pandas as pd

from defect_inspector.inference.config import ModelSpecConfig
from defect_inspector.inference.model_loader import OnnxDefectClassifier
from defect_inspector.inference.preprocessor import preprocess_image
from defect_inspector.inference.reader import read_industrial_image


class NEUDefectPyFunc(mlflow.pyfunc.PythonModel):
    """Wrapper PyFunc portable para servir `neu_resnet18.onnx` desde MLflow."""

    def load_context(self, context: mlflow.pyfunc.PythonModelContext) -> None:
        onnx_file = Path(context.artifacts["onnx_model"])
        cfg = ModelSpecConfig(models_dir=onnx_file.parent, filename=onnx_file.name)
        self._classifier = OnnxDefectClassifier(config=cfg)

    def predict(
        self,
        context: mlflow.pyfunc.PythonModelContext,
        model_input: pd.DataFrame,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, object]]:
        apply_clahe = bool((params or {}).get("apply_clahe", False))
        results: list[dict[str, object]] = []
        for _, row in model_input.iterrows():
            raw_bytes = base64.b64decode(str(row["image_base64"]))
            gray = read_industrial_image(raw_bytes)
            tensor, _ = preprocess_image(gray, apply_clahe=apply_clahe)
            pred = self._classifier.predict_tensor(tensor)
            results.append(
                {
                    "predicted_class": pred.predicted_class,
                    "confidence": pred.confidence,
                }
            )
        return pd.DataFrame(results)


def write_sample_predictions_and_report(
    out_dir: Path,
    run_name: str,
    params: dict[str, object],
    metrics: dict[str, float],
    sample_rows: list[dict[str, object]],
) -> tuple[Path, Path]:
    """Escribe artefactos `sample_predictions.json` y `evaluation_report.md`."""
    out_dir.mkdir(parents=True, exist_ok=True)
    samples_path = out_dir / "sample_predictions.json"
    report_path = out_dir / "evaluation_report.md"

    samples_path.write_text(
        json.dumps(sample_rows, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    lines = [
        f"# Reporte de Evaluación — {run_name}",
        "",
        "## Parámetros Operativos (Inferencia / Postprocesamiento)",
    ]
    for k, v in params.items():
        lines.append(f"- `{k}`: `{v}`")
    lines.extend(["", "## Métricas Medidas"])
    for k, v in metrics.items():
        lines.append(f"- **{k}**: `{v}`")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return samples_path, report_path
