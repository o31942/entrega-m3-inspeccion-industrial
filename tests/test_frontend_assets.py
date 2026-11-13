"""Pruebas AAA estructurales y contractuales del frontend desacoplado."""

from __future__ import annotations

import re
from pathlib import Path

from defect_inspector import __name__ as pkg_name

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_frontend_exists_without_streamlit_gradio_or_dash() -> None:
    # Arrange
    frontend_dir = REPO_ROOT / "frontend"
    html = (frontend_dir / "index.html").read_text(encoding="utf-8")
    css = (frontend_dir / "styles.css").read_text(encoding="utf-8")

    # Act & Assert
    assert pkg_name == "defect_inspector"
    assert '<script type="module"' in html
    assert ":root" in css
    for py_file in (REPO_ROOT / "src").rglob("*.py"):
        src = py_file.read_text(encoding="utf-8").lower()
        assert "streamlit" not in src
        assert "gradio" not in src
        assert "import dash" not in src


def test_html_exposes_critical_accessibility_and_control_ids() -> None:
    # Arrange
    html = (REPO_ROOT / "frontend" / "index.html").read_text(encoding="utf-8")
    ids = set(re.findall(r'id="([^"]+)"', html))

    # Act & Assert
    expected = {
        "health-badge",
        "gateway-url",
        "dropzone",
        "file-input",
        "conf-threshold",
        "apply-clahe",
        "btn-inspect",
        "btn-retry",
        "error-banner",
        "success-state",
        "scores-bars",
        "history-tbody",
    }
    assert expected.issubset(ids)
    assert 'aria-live="polite"' in html
    assert 'aria-live="assertive"' in html
