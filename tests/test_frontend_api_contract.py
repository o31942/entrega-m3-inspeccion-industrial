"""Pruebas AAA para cliente HTTP fetch/AbortController del frontend."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_api_js_uses_abort_controller_and_gateway_endpoints() -> None:
    # Arrange
    api_js = (REPO_ROOT / "frontend" / "js" / "api.js").read_text(encoding="utf-8")

    # Act & Assert
    assert "AbortController" in api_js
    assert "/health" in api_js
    assert "/api/v1/model" in api_js
    assert "/api/v1/inspect" in api_js
