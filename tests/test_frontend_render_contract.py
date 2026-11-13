"""Pruebas AAA para contrato del renderizador XAI, barras Top-6 y badges HITL."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_render_js_avoids_innerhtml_and_supports_hitl_scores() -> None:
    # Arrange
    txt = (REPO_ROOT / "frontend" / "js" / "render.js").read_text(encoding="utf-8")

    # Act & Assert
    assert "innerHTML" not in txt
    assert "LOW_CONFIDENCE_REVIEW" in txt
    assert "DEFECT_DETECTED" in txt
    assert "overlay_png_base64" in txt
