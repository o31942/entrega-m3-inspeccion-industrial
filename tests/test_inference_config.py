"""Pruebas unitarias para configuración del modelo MaaS NEU-DET."""

from __future__ import annotations

from pathlib import Path

from defect_inspector.inference.config import (
    DEFAULT_MODEL_ID,
    DEFAULT_MODEL_REVISION,
    IMAGENET_MEAN,
    IMAGENET_STD,
    NEU_CLASSES,
    NEU_CLASSES_ES,
    ModelSpecConfig,
)


def test_default_model_spec_matches_verified_hub_revision() -> None:
    # Arrange & Act
    cfg = ModelSpecConfig()

    # Assert
    assert cfg.model_id == DEFAULT_MODEL_ID
    assert cfg.revision == DEFAULT_MODEL_REVISION
    assert cfg.license_name == "MIT"
    assert cfg.input_size == 224
    assert cfg.onnx_path == Path("models") / "neu_resnet18.onnx"


def test_all_six_neu_classes_have_spanish_translations() -> None:
    # Arrange & Act & Assert
    assert len(NEU_CLASSES) == 6
    for cls_name in NEU_CLASSES:
        assert cls_name in NEU_CLASSES_ES
        assert len(NEU_CLASSES_ES[cls_name]) > 3
    assert len(IMAGENET_MEAN) == 3
    assert len(IMAGENET_STD) == 3


def test_config_from_env_overrides_threshold(monkeypatch) -> None:
    # Arrange
    monkeypatch.setenv("DEFAULT_CONF_THRESHOLD", "0.82")

    # Act
    cfg = ModelSpecConfig.from_env(Path("/tmp/custom"))

    # Assert
    assert abs(cfg.default_threshold - 0.82) < 1e-6
    assert cfg.models_dir == Path("/tmp/custom/models")
