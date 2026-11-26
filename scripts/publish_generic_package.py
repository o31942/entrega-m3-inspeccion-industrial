"""Publica el binario ONNX MaaS en GitLab Generic Packages usando GITLAB_TOKEN."""

from __future__ import annotations

import argparse
import os
import urllib.request
from pathlib import Path

DEFAULT_PACKAGE_NAME = "neu-steel-defect-model"
DEFAULT_PACKAGE_VERSION = "1.0.0"
DEFAULT_FILENAME = "neu_resnet18.onnx"


def build_generic_package_url(
    gitlab_base_url: str,
    project_id: str,
    package_name: str = DEFAULT_PACKAGE_NAME,
    package_version: str = DEFAULT_PACKAGE_VERSION,
    filename: str = DEFAULT_FILENAME,
) -> str:
    """Construye el endpoint REST v4 de GitLab Generic Packages."""
    base = gitlab_base_url.strip().rstrip("/")
    return (
        f"{base}/api/v4/projects/{project_id}/packages/generic/"
        f"{package_name}/{package_version}/{filename}"
    )


def publish_model_to_gitlab(
    onnx_path: Path,
    project_id: str,
    token: str,
    gitlab_base_url: str = "https://gitlab.com",
    package_name: str = DEFAULT_PACKAGE_NAME,
    package_version: str = DEFAULT_PACKAGE_VERSION,
) -> str:
    """Sube neu_resnet18.onnx a GitLab Generic Packages mediante HTTP PUT."""
    if not onnx_path.is_file():
        raise FileNotFoundError(
            f"No existe {onnx_path}. Ejecuta primero 'uv run python scripts/descargar_modelo.py'."
        )
    if not token.strip():
        raise ValueError(
            "Se requiere GITLAB_TOKEN en el entorno para autenticar el PUT."
        )

    url = build_generic_package_url(
        gitlab_base_url=gitlab_base_url,
        project_id=project_id,
        package_name=package_name,
        package_version=package_version,
        filename=onnx_path.name,
    )
    payload = onnx_path.read_bytes()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "PRIVATE-TOKEN": token.strip(),
            "Content-Type": "application/octet-stream",
        },
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=300.0) as resp:
        if resp.status not in (200, 201):
            raise RuntimeError(
                f"Respuesta inesperada de GitLab Packages: {resp.status}"
            )
    return url


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publica neu_resnet18.onnx en GitLab Generic Packages"
    )
    parser.add_argument(
        "--project-id",
        required=True,
        help="ID numérico o URL-encoded del proyecto GitLab",
    )
    parser.add_argument(
        "--gitlab-url", default=os.getenv("GITLAB_URL", "https://gitlab.com")
    )
    parser.add_argument("--package-name", default=DEFAULT_PACKAGE_NAME)
    parser.add_argument("--package-version", default=DEFAULT_PACKAGE_VERSION)
    parser.add_argument(
        "--model-path",
        default=str(
            Path(__file__).resolve().parent.parent / "models" / DEFAULT_FILENAME
        ),
    )
    args = parser.parse_args()
    token = os.getenv("GITLAB_TOKEN", "")
    url = publish_model_to_gitlab(
        onnx_path=Path(args.model_path),
        project_id=args.project_id,
        token=token,
        gitlab_base_url=args.gitlab_url,
        package_name=args.package_name,
        package_version=args.package_version,
    )
    print(f"[Generic Package OK] Publicado en: {url}")


if __name__ == "__main__":
    main()
