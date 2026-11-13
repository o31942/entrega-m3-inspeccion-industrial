"""Pruebas unitarias AAA para ingesta y validación de imágenes."""

from __future__ import annotations

import cv2
import numpy as np
import pytest

from defect_inspector.inference.reader import (
    MAX_IMAGE_BYTES,
    InvalidImageError,
    UnsupportedMediaError,
    read_industrial_image,
)


def test_read_png_bytes_returns_grayscale_uint8() -> None:
    # Arrange
    raw = np.full((64, 64, 3), 128, dtype=np.uint8)
    ok, encoded = cv2.imencode(".png", raw)
    assert ok

    # Act
    gray = read_industrial_image(encoded.tobytes(), content_type="image/png")

    # Assert
    assert gray.dtype == np.uint8
    assert gray.shape == (64, 64)


def test_read_rejects_unsupported_mime_type() -> None:
    # Arrange
    payload = b"dummy"

    # Act & Assert
    with pytest.raises(UnsupportedMediaError):
        read_industrial_image(payload, content_type="application/pdf")


def test_read_rejects_corrupt_bytes_and_empty_payload() -> None:
    # Arrange & Act & Assert
    with pytest.raises(InvalidImageError):
        read_industrial_image(b"")
    with pytest.raises(InvalidImageError):
        read_industrial_image(b"not-a-valid-image-stream")


def test_read_rejects_oversized_payload() -> None:
    # Arrange
    huge = b"a" * (MAX_IMAGE_BYTES + 1)

    # Act & Assert
    with pytest.raises(InvalidImageError):
        read_industrial_image(huge, content_type="image/png")


def test_read_rejects_tiny_array() -> None:
    # Arrange
    tiny = np.zeros((8, 8), dtype=np.uint8)

    # Act & Assert
    with pytest.raises(InvalidImageError):
        read_industrial_image(tiny)
