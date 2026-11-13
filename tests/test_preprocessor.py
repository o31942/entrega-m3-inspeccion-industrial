"""Pruebas unitarias AAA para preprocesamiento CLAHE y normalización NCHW."""

from __future__ import annotations

import numpy as np
import pytest

from defect_inspector.inference.preprocessor import (
    preprocess_image,
    validate_tensor_contract,
)


def test_preprocess_produces_valid_nchw_float32_tensor() -> None:
    # Arrange
    rng = np.random.default_rng(7)
    img = rng.integers(50, 190, size=(200, 200), dtype=np.uint8)

    # Act
    tensor, resized = preprocess_image(img, apply_clahe=False)

    # Assert
    assert tensor.dtype == np.float32
    assert tensor.shape == (1, 3, 224, 224)
    assert np.all(np.isfinite(tensor))
    assert resized.shape == (224, 224)


def test_clahe_changes_low_contrast_distribution() -> None:
    # Arrange
    low_contrast = np.full((128, 128), 100, dtype=np.uint8)
    low_contrast[40:80, 40:80] = 112

    # Act
    t_plain, g_plain = preprocess_image(low_contrast, apply_clahe=False)
    t_clahe, g_clahe = preprocess_image(low_contrast, apply_clahe=True)

    # Assert
    assert t_clahe.shape == t_plain.shape == (1, 3, 224, 224)
    assert float(np.std(g_clahe)) > float(np.std(g_plain))


def test_validate_tensor_contract_rejects_nan_and_wrong_shape() -> None:
    # Arrange
    bad_shape = np.zeros((1, 1, 224, 224), dtype=np.float32)
    with_nan = np.zeros((1, 3, 224, 224), dtype=np.float32)
    with_nan[0, 0, 0, 0] = np.nan

    # Act & Assert
    with pytest.raises(ValueError):
        validate_tensor_contract(bad_shape)
    with pytest.raises(ValueError):
        validate_tensor_contract(with_nan)
