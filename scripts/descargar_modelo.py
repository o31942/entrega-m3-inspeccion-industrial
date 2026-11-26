"""Descarga reproducible del modelo MaaS desde Generic Packages o Hugging Face Hub."""

from __future__ import annotations

import argparse
import os
import shutil
import urllib.request
from pathlib import Path

from huggingface_hub import hf_hub_download

DEFAULT_MODEL_ID = "senanurcetin/neu-steel-defect-resnet18"
DEFAULT_MODEL_REV = "ad13c70618a8a28a50309456dd40d9a45b2869d1"
REQUIRED_FILES = ("neu_resnet18.onnx", "labels.json", "results.json")


def _build_auth_headers() -> dict[str, str]:
    """Construye cabeceras opcionales para GitLab Generic Packages sin exponer secretos."""
    pat = os.getenv("GITLAB_TOKEN", "").strip()
    if pat:
        return {"PRIVATE-TOKEN": pat}
    job_token = os.getenv("CI_JOB_TOKEN", "").strip()
    if job_token:
        return {"JOB-TOKEN": job_token}
    secret_file = Path("/run/secrets/ci_job_token")
    if secret_file.is_file():
        mounted = secret_file.read_text(encoding="utf-8").strip()
        if mounted:
            return {"JOB-TOKEN": mounted}
    return {}


def download_from_package_url(package_url: str, dest_file: Path) -> Path:
    """Descarga el binario ONNX desde una URL de GitLab Generic Packages."""
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(
        package_url, headers=_build_auth_headers(), method="GET"
    )
    with urllib.request.urlopen(req, timeout=120.0) as resp, dest_file.open("wb") as fh:
        shutil.copyfileobj(resp, fh)
    if dest_file.stat().st_size == 0:
        raise RuntimeError(f"El paquete descargado desde {package_url} está vacío.")
    return dest_file


def download_maas_model(
    model_id: str = DEFAULT_MODEL_ID,
    revision: str = DEFAULT_MODEL_REV,
    target_dir: Path | None = None,
    package_url: str | None = None,
) -> Path:
    """Descarga pesos ONNX y metadatos a models/ sin versionar binarios en Git."""
    out_dir = target_dir or Path(__file__).resolve().parent.parent / "models"
    out_dir.mkdir(parents=True, exist_ok=True)
    resolved_pkg_url = (
        package_url
        if package_url is not None
        else os.getenv("MODEL_PACKAGE_URL", "").strip()
    )

    if resolved_pkg_url:
        download_from_package_url(resolved_pkg_url, out_dir / "neu_resnet18.onnx")
        metadata_files: tuple[str, ...] = ("labels.json", "results.json")
    else:
        metadata_files = REQUIRED_FILES

    for filename in metadata_files:
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
    parser.add_argument(
        "--package-url",
        default=os.getenv("MODEL_PACKAGE_URL", "").strip(),
        help="URL opcional en GitLab Generic Packages para neu_resnet18.onnx",
    )
    args = parser.parse_args()
    onnx_path = download_maas_model(
        model_id=args.model_id,
        revision=args.revision,
        package_url=args.package_url,
    )
    print(f"Modelo MaaS listo en: {onnx_path} ({onnx_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
