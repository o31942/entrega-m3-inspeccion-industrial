"""Fixtures compartidos sintéticos AAA para suite offline >= 120 pruebas."""

from __future__ import annotations

from collections.abc import Callable

import cv2
import numpy as np
import pytest

from defect_inspector.inference.model_loader import OnnxDefectClassifier
from defect_inspector.services.inspection_service import DefectInspectionService


class DeterministicFakeSession:
    """Sesión falsa ONNX determinista sin archivos en disco ni GPU."""

    def __init__(self, logits: list[float] | None = None) -> None:
        self._logits = np.array(
            [logits or [0.1, 0.2, 4.2, 0.1, 0.0, 0.1]],
            dtype=np.float32,
        )

    def get_inputs(self) -> list[object]:
        return []

    def run(
        self, output_names: list[str] | None, input_feed: dict[str, np.ndarray]
    ) -> list[np.ndarray]:
        return [self._logits]


@pytest.fixture
def make_encoded_image() -> Callable[[tuple[int, int], int, str], bytes]:
    """Construye imagen sintética en memoria codificada como PNG, JPG o BMP."""

    def _factory(
        size: tuple[int, int] = (128, 128),
        channels: int = 1,
        ext: str = ".png",
    ) -> bytes:
        h, w = size
        shape = (h, w) if channels == 1 else (h, w, channels)
        arr = np.full(shape, 120, dtype=np.uint8)
        arr[h // 4 : (3 * h) // 4, w // 2 - 2 : w // 2 + 2] = 240
        ok, buf = cv2.imencode(ext, arr)
        assert ok
        return buf.tobytes()

    return _factory


@pytest.fixture
def make_fake_classifier() -> Callable[[list[float] | None], OnnxDefectClassifier]:
    """Instancia OnnxDefectClassifier con sesión ONNX sintética."""

    def _factory(logits: list[float] | None = None) -> OnnxDefectClassifier:
        return OnnxDefectClassifier(session=DeterministicFakeSession(logits=logits))

    return _factory


@pytest.fixture
def make_fake_service(
    make_fake_classifier: Callable[[list[float] | None], OnnxDefectClassifier],
) -> Callable[[list[float] | None], DefectInspectionService]:
    """Instancia DefectInspectionService con sesión ONNX sintética configurable."""

    def _factory(logits: list[float] | None = None) -> DefectInspectionService:
        return DefectInspectionService(classifier=make_fake_classifier(logits))

    return _factory
