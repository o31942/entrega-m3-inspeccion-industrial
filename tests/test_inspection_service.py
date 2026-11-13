"""Pruebas unitarias AAA para DefectInspectionService y política HITL."""

from __future__ import annotations

import cv2
import numpy as np
import pytest

from defect_inspector.inference.model_loader import OnnxDefectClassifier
from defect_inspector.services.exceptions import (
    DomainValidationError,
    UnsupportedImageFormatError,
)
from defect_inspector.services.inspection_service import DefectInspectionService


class _StubSession:
    def __init__(self, logits: list[float]) -> None:
        self._logits = np.array([logits], dtype=np.float32)

    def get_inputs(self) -> list[object]:
        return []

    def run(
        self, output_names: list[str] | None, input_feed: dict[str, np.ndarray]
    ) -> list[np.ndarray]:
        return [self._logits]


def _sample_png_bytes() -> bytes:
    img = np.full((100, 100), 110, dtype=np.uint8)
    img[20:80, 48:53] = 245
    ok, buf = cv2.imencode(".png", img)
    assert ok
    return buf.tobytes()


def test_service_marks_low_confidence_for_hitl_review() -> None:
    # Arrange
    clf = OnnxDefectClassifier(session=_StubSession([0.4, 0.3, 0.3, 0.2, 0.1, 0.5]))
    svc = DefectInspectionService(classifier=clf)

    # Act
    out = svc.inspect(_sample_png_bytes(), conf_threshold=0.75, apply_clahe=True)

    # Assert
    assert out.requires_human_review is True
    assert out.decision_status == "LOW_CONFIDENCE_REVIEW"
    assert out.applied_clahe is True
    assert len(out.scores) == 6
    assert out.scores[0].probability >= out.scores[-1].probability


def test_service_marks_defect_detected_above_threshold() -> None:
    # Arrange
    clf = OnnxDefectClassifier(session=_StubSession([0.0, 0.0, 0.0, 0.0, 0.0, 5.0]))
    svc = DefectInspectionService(classifier=clf)

    # Act
    out = svc.inspect(_sample_png_bytes(), conf_threshold=0.70, request_id="hit-1")

    # Assert
    assert out.request_id == "hit-1"
    assert out.predicted_class == "scratches"
    assert out.requires_human_review is False
    assert out.decision_status == "DEFECT_DETECTED"


def test_service_validates_threshold_and_media_type() -> None:
    # Arrange
    clf = OnnxDefectClassifier(session=_StubSession([1.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
    svc = DefectInspectionService(classifier=clf)

    # Act & Assert
    with pytest.raises(DomainValidationError):
        svc.inspect(_sample_png_bytes(), conf_threshold=1.2)
    with pytest.raises(UnsupportedImageFormatError):
        svc.inspect(b"abc", content_type="text/plain")
