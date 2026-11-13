"""Descarga reproducible del modelo MaaS desde Hugging Face Hub (fuera de Git)."""

from __future__ import annotations

import argparse
from pathlib import Path

from huggingface_hub import hf_hub_download

DEFAULT_MODEL_ID = "senanurcetin/neu-steel-defect-resnet18"
DEFAULT_MODEL_REV = "ad13c70618a8a28a50309456dd40d9a45b2869d1"
REQUIRED_FILES = ("neu_resnet18.onnx", "labels.json", "results.json")


def download_maas_model(
    model_id: str = DEFAULT_MODEL_ID,
    revision: str = DEFAULT_MODEL_REV,
    target_dir: Path | None = None,
) -> Path:
    """Descarga pesos ONNX y metadatos a models/ sin versionar binarios en Git."""
    out_dir = target_dir or Path(__file__).resolve().parent.parent / "models"
    out_dir.mkdir(parents=True, exist_ok=True)
    for filename in REQUIRED_FILES:
        hf_hub_download(
            repo_id=model_id,
            revision=revision,
            filename=filename,
            local_dir=str(out_dir),
        )
    return out_dir / "neu_resnet18.onnx"


def main() -> None:
    parser = argparse.ArgumentParser(description="Descarga modelo MaaS NEU-DET")
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID)
    parser.add_argument("--revision", default=DEFAULT_MODEL_REV)
    args = parser.parse_args()
    onnx_path = download_maas_model(model_id=args.model_id, revision=args.revision)
    print(f"Modelo MaaS listo en: {onnx_path} ({onnx_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
