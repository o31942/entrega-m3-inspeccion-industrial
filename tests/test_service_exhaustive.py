"""Batería parametrizada AAA para DefectInspectionService y fronteras HITL."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pytest

from defect_inspector.inference.config import NEU_CLASSES, NEU_CLASSES_ES
from defect_inspector.inference.model_loader import ModelLoadError, OnnxDefectClassifier
from defect_inspector.services.exceptions import (
    DomainValidationError,
    InspectionProcessingError,
    ModelNotReadyError,
    UnsupportedImageFormatError,
)
from defect_inspector.services.inspection_service import DefectInspectionService


class _RaisingSession:
    def get_inputs(self) -> list[object]:
        return []

    def run(
        self, output_names: list[str] | None, input_feed: dict[str, np.ndarray]
    ) -> list[np.ndarray]:
        raise ModelLoadError("session failed")


class _RuntimeCrashSession:
    def get_inputs(self) -> list[object]:
        return []

    def run(
        self, output_names: list[str] | None, input_feed: dict[str, np.ndarray]
    ) -> list[np.ndarray]:
        raise RuntimeError("unexpected numpy error")


@pytest.mark.parametrize("winner_idx", range(6))
def test_service_predicts_all_six_neu_classes_and_sorts_scores(
    make_encoded_image: Callable[[tuple[int, int], int, str], bytes],
    make_fake_service: Callable[[list[float] | None], DefectInspectionService],
    winner_idx: int,
) -> None:
    # Arrange
    logits = [0.1] * 6
    logits[winner_idx] = 5.5
    svc = make_fake_service(logits)
    img_bytes = make_encoded_image((128, 128), 1, ".png")

    # Act
    res = svc.inspect(img_bytes, conf_threshold=0.70, apply_clahe=True)

    # Assert
    expected_cls = NEU_CLASSES[winner_idx]
    assert res.predicted_class == expected_cls
    assert res.predicted_label_es == NEU_CLASSES_ES[expected_cls]
    assert res.requires_human_review is False
    assert res.decision_status == "DEFECT_DETECTED"
    probs = [s.probability for s in res.scores]
    assert probs == sorted(probs, reverse=True)


@pytest.mark.parametrize(
    ("threshold", "top_logit", "expect_review"),
    [
        (0.50, 4.0, False),
        (0.70, 4.0, False),
        (0.95, 2.0, True),
        (0.40, 0.2, True),
        (0.05, 0.0, False),
        (0.99, 3.0, True),
    ],
)
def test_service_hitl_threshold_matrix(
    make_encoded_image: Callable[[tuple[int, int], int, str], bytes],
    make_fake_service: Callable[[list[float] | None], DefectInspectionService],
    threshold: float,
    top_logit: float,
    expect_review: bool,
) -> None:
    # Arrange
    svc = make_fake_service([top_logit, 0.0, 0.0, 0.0, 0.0, 0.0])
    img_bytes = make_encoded_image((64, 64), 1, ".png")

    # Act
    out = svc.inspect(img_bytes, conf_threshold=threshold)

    # Assert
    assert out.requires_human_review is expect_review
    assert out.decision_status == (
        "LOW_CONFIDENCE_REVIEW" if expect_review else "DEFECT_DETECTED"
    )


@pytest.mark.parametrize("bad_thresh", [0.01, 0.049, 0.991, 1.5, 2.0])
def test_service_rejects_out_of_bounds_threshold(
    make_encoded_image: Callable[[tuple[int, int], int, str], bytes],
    make_fake_service: Callable[[list[float] | None], DefectInspectionService],
    bad_thresh: float,
) -> None:
    # Arrange
    svc = make_fake_service(None)
    img_bytes = make_encoded_image((64, 64), 1, ".png")

    # Act & Assert
    with pytest.raises(DomainValidationError):
        svc.inspect(img_bytes, conf_threshold=bad_thresh)


def test_service_maps_inference_errors_to_domain_exceptions(
    make_encoded_image: Callable[[tuple[int, int], int, str], bytes],
    make_fake_service: Callable[[list[float] | None], DefectInspectionService],
) -> None:
    # Arrange
    svc_ok = make_fake_service(None)
    svc_load_err = DefectInspectionService(
        classifier=OnnxDefectClassifier(session=_RaisingSession())
    )
    svc_runtime_err = DefectInspectionService(
        classifier=OnnxDefectClassifier(session=_RuntimeCrashSession())
    )
    valid_bytes = make_encoded_image((64, 64), 1, ".png")

    # Act & Assert
    with pytest.raises(UnsupportedImageFormatError):
        svc_ok.inspect(b"x", content_type="application/xml")
    with pytest.raises(DomainValidationError):
        svc_ok.inspect(b"corrupt")
    with pytest.raises(ModelNotReadyError):
        svc_load_err.inspect(valid_bytes)
    with pytest.raises(InspectionProcessingError):
        svc_runtime_err.inspect(valid_bytes)
