"""Pruebas AAA para máquina de estados ES Module."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_state_machine_defines_mandatory_states() -> None:
    # Arrange
    state_js = (REPO_ROOT / "frontend" / "js" / "state.js").read_text(encoding="utf-8")

    # Act & Assert
    for st in ('"idle"', '"loading"', '"success"', '"error"'):
        assert st in state_js
