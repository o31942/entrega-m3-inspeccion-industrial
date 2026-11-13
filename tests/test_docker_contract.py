"""Pruebas AAA contractuales de empaquetado Docker CPU reproducible."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_dockerfile_follows_non_root_uv_cpu_best_practices() -> None:
    # Arrange
    df = (REPO_ROOT / "Dockerfile").read_text(encoding="utf-8")
    di = (REPO_ROOT / ".dockerignore").read_text(encoding="utf-8")

    # Act & Assert
    assert "FROM python:3.13-slim" in df
    assert "uv sync --frozen --no-dev" in df
    assert "USER appuser" in df
    assert "EXPOSE 50051 8000" in df
    assert "HEALTHCHECK" in df
    assert "models/" in di
    assert "mlruns/" in di
