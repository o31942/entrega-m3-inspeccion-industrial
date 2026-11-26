"""Pruebas AAA contractuales y funcionales del Módulo 4 (GitLab CI/CD, Cloud HTTPS y Constitución)."""

from __future__ import annotations

import importlib.util
import io
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest
from fastapi.testclient import TestClient

from defect_inspector.api.gateway import create_gateway_app, resolve_cors_origins
from defect_inspector.api.grpc_server import create_grpc_server
from defect_inspector.inference.model_loader import OnnxDefectClassifier
from defect_inspector.services.inspection_service import DefectInspectionService

REPO_ROOT = Path(__file__).resolve().parent.parent


class _FakeSession:
    def get_inputs(self) -> list[object]:
        return []

    def run(
        self, output_names: list[str] | None, input_feed: dict[str, np.ndarray]
    ) -> list[np.ndarray]:
        return [np.array([[0.1, 0.1, 0.1, 0.1, 0.1, 4.2]], dtype=np.float32)]


def _load_script(script_name: str):
    path = REPO_ROOT / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(script_name[:-3], path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_constitution_exists_and_is_linked_from_readme() -> None:
    # Arrange
    constitution = REPO_ROOT / "CONSTITUTION.md"
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    # Act
    text = constitution.read_text(encoding="utf-8")

    # Assert
    assert constitution.is_file()
    assert "CONSTITUTION.md" in readme
    for keyword in ("3 Capas", "uv", "SSH_KEY", "HEALTHCHECK", "LOW_CONFIDENCE_REVIEW"):
        assert keyword in text


def test_gitlab_ci_defines_four_stages_cache_artifacts_and_masked_secrets() -> None:
    # Arrange
    ci_path = REPO_ROOT / ".gitlab-ci.yml"

    # Act
    ci = ci_path.read_text(encoding="utf-8")

    # Assert
    assert ci_path.is_file()
    for stage_or_job in (
        "- lint",
        "- test",
        "- build",
        "- deploy",
        "build_image:",
        "deploy_droplet:",
    ):
        assert stage_or_job in ci
    assert ".cache/uv" in ci
    assert "uv sync --frozen" in ci
    assert "uv run ruff check ." in ci
    assert "uv run pytest -q" in ci
    assert "$CI_COMMIT_SHORT_SHA" in ci
    assert ":latest" in ci
    assert "healthy" in ci
    assert "BEGIN OPENSSH PRIVATE KEY" not in ci
    assert "glpat-" not in ci


def test_droplet_provisioning_configures_ufw_and_caddy_https() -> None:
    # Arrange
    setup_sh = (REPO_ROOT / "deploy" / "setup_droplet.sh").read_text(encoding="utf-8")
    caddyfile = (REPO_ROOT / "deploy" / "Caddyfile").read_text(encoding="utf-8")

    # Act & Assert
    assert "ufw allow 22/tcp" in setup_sh
    assert "ufw allow 80/tcp" in setup_sh
    assert "ufw allow 443/tcp" in setup_sh
    assert "sslip.io" in setup_sh
    assert "reverse_proxy 127.0.0.1:8000" in caddyfile


def test_resolve_cors_origins_preserves_defaults_and_adds_https_domain() -> None:
    # Arrange & Act
    origins = resolve_cors_origins("https://164-90-10-20.sslip.io/, https://app.uao.co")

    # Assert
    assert "http://127.0.0.1:5173" in origins
    assert "https://164-90-10-20.sslip.io" in origins
    assert "https://app.uao.co" in origins


def test_gateway_static_frontend_mode_serves_ui_without_shadowing_api() -> None:
    # Arrange
    svc = DefectInspectionService(
        classifier=OnnxDefectClassifier(session=_FakeSession())
    )
    server, port = create_grpc_server(svc, host="127.0.0.1", port=0)
    server.start()
    app = create_gateway_app(
        grpc_target=f"127.0.0.1:{port}",
        serve_static_frontend=True,
        frontend_dir=REPO_ROOT / "frontend",
    )

    try:
        with TestClient(app) as client:
            # Act
            r_root = client.get("/")
            r_js = client.get("/js/state.js")
            r_health = client.get("/health")
            r_docs = client.get("/docs")

        # Assert
        assert r_root.status_code == 200
        assert "SteelSight" in r_root.text
        assert r_js.status_code == 200
        assert "resolveDefaultGatewayUrl" in r_js.text
        assert r_health.status_code == 200
        assert r_health.json()["status"] == "SERVING"
        assert r_docs.status_code == 200
    finally:
        server.stop(grace=0.5)


def test_generic_package_helpers_build_url_and_download_stream(tmp_path: Path) -> None:
    # Arrange
    pub_mod = _load_script("publish_generic_package.py")
    dl_mod = _load_script("descargar_modelo.py")
    url = pub_mod.build_generic_package_url("https://gitlab.com/", "998877")
    dest = tmp_path / "neu_resnet18.onnx"

    class _DummyResponse(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *args: object) -> None:
            self.close()

    # Act
    with patch.object(
        dl_mod.urllib.request,
        "urlopen",
        return_value=_DummyResponse(b"fake-onnx-binary"),
    ):
        saved = dl_mod.download_from_package_url(url, dest)

    # Assert
    assert (
        url
        == "https://gitlab.com/api/v4/projects/998877/packages/generic/neu-steel-defect-model/1.0.0/neu_resnet18.onnx"
    )
    assert saved.read_bytes() == b"fake-onnx-binary"

    with (
        patch.object(
            dl_mod.urllib.request, "urlopen", return_value=_DummyResponse(b"")
        ),
        pytest.raises(RuntimeError),
    ):
        dl_mod.download_from_package_url(url, tmp_path / "empty.onnx")
