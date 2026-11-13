"""Pruebas AAA para workflow CI y guardián anti-binarios."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_ci_workflow_runs_ruff_and_pytest() -> None:
    # Arrange
    ci = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    # Act & Assert
    assert "uv sync --frozen" in ci
    assert "uv run ruff check ." in ci
    assert "uv run ruff format --check ." in ci
    assert "uv run pytest -q" in ci
