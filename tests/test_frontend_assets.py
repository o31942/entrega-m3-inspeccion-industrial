"""Pruebas AAA iniciales para maquetación HTML5 y estilos CSS desacoplados."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_frontend_html_and_css_present_without_streamlit() -> None:
    # Arrange
    html = (REPO_ROOT / "frontend" / "index.html").read_text(encoding="utf-8")
    css = (REPO_ROOT / "frontend" / "styles.css").read_text(encoding="utf-8")

    # Act & Assert
    assert "<main" in html
    assert "<header" in html
    assert ":root" in css
    assert "streamlit" not in html.lower()
