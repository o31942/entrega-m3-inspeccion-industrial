"""Batería parametrizada AAA para Capa 1 (ingesta, CLAHE, ONNX loader, XAI)."""

from __future__ import annotations

import base64
from collections.abc import Callable

import cv2
import numpy as np
import pytest

from defect_inspector.inference.config import NEU_CLASSES, NEU_CLASSES_ES
from defect_inspector.inference.explainability import compute_saliency_and_roi
from defect_inspector.inference.model_loader import (
    OnnxDefectClassifier,
    stable_softmax,
)
from defect_inspector.inference.preprocessor import (
    preprocess_image,
    validate_tensor_contract,
)
from defect_inspector.inference.reader import (
    MAX_IMAGE_BYTES,
    InvalidImageError,
    UnsupportedMediaError,
    read_industrial_image,
)


@pytest.mark.parametrize("cls_name", NEU_CLASSES)
def test_neu_classes_have_spanish_translations(cls_name: str) -> None:
    # Arrange & Act & Assert
    assert cls_name in NEU_CLASSES_ES
    assert len(NEU_CLASSES_ES[cls_name]) > 3


@pytest.mark.parametrize(
    ("size", "channels", "ext"),
    [
        ((64, 64), 1, ".png"),
        ((128, 128), 3, ".png"),
        ((200, 200), 3, ".jpg"),
        ((256, 192), 1, ".bmp"),
        ((300, 300), 4, ".png"),
        ((48, 96), 3, ".jpg"),
    ],
)
def test_reader_decodes_valid_image_matrix_formats(
    make_encoded_image: Callable[[tuple[int, int], int, str], bytes],
    size: tuple[int, int],
    channels: int,
    ext: str,
) -> None:
    # Arrange
    payload = make_encoded_image(size, channels, ext)

    # Act
    decoded = read_industrial_image(payload)

    # Assert
    assert isinstance(decoded, np.ndarray)
    assert decoded.dtype == np.uint8
    assert decoded.shape[:2] == size


@pytest.mark.parametrize(
    "bad_mime",
    [
        "text/plain",
        "application/pdf",
        "application/json",
        "video/mp4",
        "image/svg+xml",
        "application/zip",
    ],
)
def test_reader_rejects_disallowed_mime_types(bad_mime: str) -> None:
    # Arrange & Act & Assert
    with pytest.raises(UnsupportedMediaError):
        read_industrial_image(b"dummy-bytes", content_type=bad_mime)


@pytest.mark.parametrize(
    "bad_payload",
    [
        b"",
        b"not-an-image-buffer",
        b"\x89PNG\r\n\x1a\ntruncated",
    ],
)
def test_reader_rejects_empty_or_corrupt_bytes(bad_payload: bytes) -> None:
    # Arrange & Act & Assert
    with pytest.raises(InvalidImageError):
        read_industrial_image(bad_payload, content_type="image/png")


def test_reader_rejects_oversized_payload() -> None:
    # Arrange
    oversized = b"0" * (MAX_IMAGE_BYTES + 1)

    # Act & Assert
    with pytest.raises(InvalidImageError):
        read_industrial_image(oversized, content_type="image/png")


@pytest.mark.parametrize("apply_clahe", [False, True])
@pytest.mark.parametrize("target_size", [112, 224])
@pytest.mark.parametrize("channels", [2, 3])
def test_preprocess_image_enforces_tensor_contract(
    apply_clahe: bool, target_size: int, channels: int
) -> None:
    # Arrange
    shape = (180, 180) if channels == 2 else (180, 180, 3)
    img = np.full(shape, 105, dtype=np.uint8)

    # Act
    tensor, gray = preprocess_image(
        img, apply_clahe=apply_clahe, target_size=target_size
    )

    # Assert
    validate_tensor_contract(tensor, target_size=target_size)
    assert gray.shape == (target_size, target_size)
    assert gray.dtype == np.uint8


@pytest.mark.parametrize(
    "logits",
    [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [1000.0, 999.0, 998.0, 0.0, 0.0, -500.0],
        [-100.0, -101.0, -102.0, -103.0, -104.0, -105.0],
        [5.0, -5.0, 1.5, 2.5, 0.0, -1.0],
    ],
)
def test_stable_softmax_sums_to_one_without_overflow(logits: list[float]) -> None:
    # Arrange & Act
    probs = stable_softmax(np.array(logits, dtype=np.float64))

    # Assert
    assert np.all(np.isfinite(probs))
    assert np.all(probs >= 0.0)
    assert pytest.approx(float(np.sum(probs)), abs=1e-6) == 1.0


@pytest.mark.parametrize("winner_idx", range(6))
def test_onnx_classifier_picks_highest_logit_class(
    make_fake_classifier: Callable[[list[float] | None], OnnxDefectClassifier],
    winner_idx: int,
) -> None:
    # Arrange
    logits = [0.0] * 6
    logits[winner_idx] = 6.0
    clf = make_fake_classifier(logits)
    tensor = np.zeros((1, 3, 224, 224), dtype=np.float32)

    # Act
    pred = clf.predict_tensor(tensor)

    # Assert
    assert pred.predicted_class == NEU_CLASSES[winner_idx]
    assert pred.confidence > 0.90


@pytest.mark.parametrize(
    ("cx", "cy"),
    [
        (35, 35),
        (185, 35),
        (35, 185),
        (185, 185),
        (112, 112),
    ],
)
def test_saliency_roi_tracks_defect_across_quadrants(cx: int, cy: int) -> None:
    # Arrange
    gray = np.full((224, 224), 100, dtype=np.uint8)
    cv2.rectangle(gray, (cx - 10, cy - 10), (cx + 10, cy + 10), (255,), -1)

    # Act
    res = compute_saliency_and_roi(gray)
    x1, y1, x2, y2 = res.roi_bbox

    # Assert
    assert 0 <= x1 < x2 <= 224
    assert 0 <= y1 < y2 <= 224
    assert x1 <= cx <= x2
    assert y1 <= cy <= y2
    assert base64.b64decode(res.overlay_png_base64).startswith(b"\x89PNG")
