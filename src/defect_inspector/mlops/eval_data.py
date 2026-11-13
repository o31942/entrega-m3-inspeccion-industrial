"""Constructor del lote fijo de evaluación reproducible NEU-DET (caché fuera de Git)."""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from defect_inspector.inference.config import NEU_CLASSES

DEFAULT_HF_DATASET_ID = "newguyme/neu_det_caption"
DEFAULT_HF_PARQUET = "data/train-00000-of-00001.parquet"


@dataclass(frozen=True, slots=True)
class EvalSample:
    """Muestra etiquetada inmutable para comparación reproducible en MLflow."""

    sample_id: str
    filename: str
    true_label: str
    class_index: int
    image_bytes: bytes
    source: str


def generate_synthetic_eval_batch(
    per_class: int = 10,
    seed: int = 42,
) -> tuple[list[EvalSample], str]:
    """Genera lote sintético estratificado y determinista para pruebas offline."""
    rng = np.random.default_rng(seed)
    samples: list[EvalSample] = []
    for cls_idx, cls_name in enumerate(NEU_CLASSES):
        for k in range(per_class):
            canvas = rng.integers(88, 148, size=(200, 200), dtype=np.uint8)
            if cls_name == "crazing":
                for row in range(20, 180, 22):
                    cv2.line(canvas, (15, row), (185, row + 12), (35,), 1)
            elif cls_name == "inclusion":
                cv2.rectangle(canvas, (88, 25), (104, 175), (25,), -1)
            elif cls_name == "patches":
                cv2.circle(canvas, (70, 75), 34, (40,), -1)
                cv2.circle(canvas, (130, 125), 28, (205,), -1)
            elif cls_name == "pitted_surface":
                for dot in range(18):
                    cx = int(20 + ((dot * 37 + k * 13) % 160))
                    cy = int(20 + ((dot * 53 + k * 17) % 160))
                    cv2.circle(canvas, (cx, cy), 4, (20,), -1)
            elif cls_name == "rolled-in_scale":
                cv2.ellipse(canvas, (100, 100), (42, 14), 18, 0, 360, (28,), -1)
            else:
                cv2.line(canvas, (18, 45 + k * 8), (182, 55 + k * 8), (242,), 3)

            ok, buf = cv2.imencode(".png", canvas)
            if not ok:
                raise RuntimeError("Fallo codificando muestra sintética PNG.")
            fname = f"synth_{cls_name}_{k:02d}.png"
            samples.append(
                EvalSample(
                    sample_id=f"{cls_name}-{k:02d}",
                    filename=fname,
                    true_label=cls_name,
                    class_index=cls_idx,
                    image_bytes=buf.tobytes(),
                    source="synthetic-deterministic-fallback",
                )
            )
    return samples, "synthetic-deterministic-fallback"


def _load_from_cache(cache_dir: Path) -> tuple[list[EvalSample], str] | None:
    manifest_path = cache_dir / "manifest.json"
    if not manifest_path.is_file():
        return None
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source = str(manifest.get("source", "local-cache"))
    out: list[EvalSample] = []
    for row in manifest.get("samples", []):
        img_path = cache_dir / str(row["rel_path"])
        if not img_path.is_file():
            return None
        out.append(
            EvalSample(
                sample_id=str(row["sample_id"]),
                filename=str(row["filename"]),
                true_label=str(row["true_label"]),
                class_index=int(row["class_index"]),
                image_bytes=img_path.read_bytes(),
                source=source,
            )
        )
    return (out, source) if out else None


def load_reproducible_eval_batch(
    cache_dir: Path = Path("data/raw/eval_cache"),
    per_class: int = 20,
    seed: int = 42,
    allow_download: bool = True,
) -> tuple[list[EvalSample], str]:
    """Carga lote estratificado fijo: caché local, HF `newguyme/neu_det_caption` o fallback."""
    cached = _load_from_cache(cache_dir)
    if cached is not None:
        return cached

    if allow_download:
        try:
            import pyarrow.parquet as pq
            from huggingface_hub import hf_hub_download

            pq_path = hf_hub_download(
                repo_id=DEFAULT_HF_DATASET_ID,
                filename=DEFAULT_HF_PARQUET,
                repo_type="dataset",
            )
            table = pq.read_table(
                pq_path, columns=["image", "label", "filename", "label_str"]
            )
            by_class: dict[str, list[dict[str, object]]] = {c: [] for c in NEU_CLASSES}
            rows = table.to_pylist()
            for row in rows:
                lbl = str(row["label_str"])
                if lbl in by_class:
                    by_class[lbl].append(row)

            cache_dir.mkdir(parents=True, exist_ok=True)
            rng = random.Random(seed)
            manifest_rows: list[dict[str, object]] = []
            samples: list[EvalSample] = []
            source = f"huggingface:{DEFAULT_HF_DATASET_ID}"

            for cls_idx, cls_name in enumerate(NEU_CLASSES):
                bucket = sorted(
                    by_class[cls_name], key=lambda item: str(item["filename"])
                )
                chosen = rng.sample(bucket, k=min(per_class, len(bucket)))
                for idx, item in enumerate(chosen):
                    img_dict = item["image"]
                    img_bytes = bytes(img_dict["bytes"])  # type: ignore[index]
                    fname = str(item["filename"])
                    rel_path = f"{cls_name}/{fname}"
                    dst = cache_dir / rel_path
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    dst.write_bytes(img_bytes)
                    sample_id = f"{cls_name}-{idx:03d}"
                    manifest_rows.append(
                        {
                            "sample_id": sample_id,
                            "filename": fname,
                            "true_label": cls_name,
                            "class_index": cls_idx,
                            "rel_path": rel_path,
                        }
                    )
                    samples.append(
                        EvalSample(
                            sample_id=sample_id,
                            filename=fname,
                            true_label=cls_name,
                            class_index=cls_idx,
                            image_bytes=img_bytes,
                            source=source,
                        )
                    )
            (cache_dir / "manifest.json").write_text(
                json.dumps(
                    {"source": source, "seed": seed, "samples": manifest_rows}, indent=2
                ),
                encoding="utf-8",
            )
            return samples, source
        except Exception:
            pass

    return generate_synthetic_eval_batch(per_class=per_class, seed=seed)
