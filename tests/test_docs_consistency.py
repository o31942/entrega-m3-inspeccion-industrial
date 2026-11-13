"""Pruebas AAA de consistencia entre README, Archify HTML y Model Card."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_archify_and_model_card_align_with_repository_ports_and_model() -> None:
    # Arrange
    arch = (REPO_ROOT / "docs" / "arquitectura.html").read_text(encoding="utf-8")
    mc = (REPO_ROOT / "docs" / "model-card.md").read_text(encoding="utf-8")

    # Act & Assert
    for port in ("5173", "8000", "50051", "5050"):
        assert port in arch
    assert "senanurcetin/neu-steel-defect-resnet18" in mc
    assert "ad13c70618a8a28a50309456dd40d9a45b2869d1" in mc
    assert "LOW_CONFIDENCE_REVIEW" in mc
