"""Pruebas unitarias AAA para generación de saliencia XAI y ROI."""

from __future__ import annotations

import base64

import cv2
import numpy as np

from defect_inspector.inference.explainability import compute_saliency_and_roi


def test_saliency_localizes_high_contrast_scratch_region() -> None:
    # Arrange
    img = np.full((224, 224), 100, dtype=np.uint8)
    img[70:150, 155:165] = 250

    # Act
    sal = compute_saliency_and_roi(img)

    # Assert
    x1, y1, x2, y2 = sal.roi_bbox
    assert sal.heatmap.shape == (224, 224)
    assert 0.0 <= float(sal.heatmap.min()) <= float(sal.heatmap.max()) <= 1.0
    assert 0 <= x1 < x2 <= 224
    assert 0 <= y1 < y2 <= 224
    assert x1 <= 160 <= x2


def test_saliency_encodes_valid_png_base64() -> None:
    # Arrange
    img = np.linspace(0, 255, 224 * 224, dtype=np.uint8).reshape(224, 224)

    # Act
    sal = compute_saliency_and_roi(img)
    decoded = cv2.imdecode(
        np.frombuffer(base64.b64decode(sal.overlay_png_base64), dtype=np.uint8),
        cv2.IMREAD_COLOR,
    )

    # Assert
    assert decoded is not None
    assert decoded.shape == (224, 224, 3)
