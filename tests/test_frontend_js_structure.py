"""Pruebas AAA para módulos ES de frontend, máquina de estados y consistencia DOM."""

from __future__ import annotations

import mimetypes
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_state_js_defines_four_mandatory_ui_states() -> None:
    # Arrange
    state_js = (REPO_ROOT / "frontend" / "js" / "state.js").read_text(encoding="utf-8")

    # Act & Assert
    for token in ('"idle"', '"loading"', '"success"', '"error"'):
        assert token in state_js
    assert "createStore" in state_js
    assert "subscribe" in state_js


def test_js_getelementbyid_references_exist_in_html() -> None:
    # Arrange
    html = (REPO_ROOT / "frontend" / "index.html").read_text(encoding="utf-8")
    html_ids = set(re.findall(r'id="([^"]+)"', html))
    js_dir = REPO_ROOT / "frontend" / "js"
    referenced: set[str] = set()
    for js_file in js_dir.glob("*.js"):
        txt = js_file.read_text(encoding="utf-8")
        referenced.update(re.findall(r'getElementById\("([^"]+)"\)', txt))

    # Act & Assert
    missing = referenced - html_ids
    assert not missing, f"IDs referenciados en JS inexistentes en HTML: {missing}"


def test_serve_frontend_sets_js_mime_type() -> None:
    # Arrange
    srv_path = REPO_ROOT / "scripts" / "serve_frontend.py"
    assert srv_path.is_file()
    import importlib.util

    spec = importlib.util.spec_from_file_location("serve_frontend", srv_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Act
    guessed, _ = mimetypes.guess_type("app.js")

    # Assert
    assert mod.ModuleSafeHandler.extensions_map[".js"].startswith("text/javascript")
    assert guessed is not None and "javascript" in guessed
