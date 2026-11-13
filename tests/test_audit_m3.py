"""Pruebas AAA finales de auditoría cuantitativa de Anuncio 007."""

from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_audit_m3_passes_quantitative_floors() -> None:
    # Arrange
    audit_path = REPO_ROOT / "scripts" / "audit_m3.py"
    spec = importlib.util.spec_from_file_location("audit_m3", audit_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Act
    report = mod.audit_repository(run_subprocesses=False)

    # Assert
    assert report["specs_complete"] >= 40
    assert report["missing_files"] == []
