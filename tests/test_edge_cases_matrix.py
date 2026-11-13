"""Matriz de casos borde, fronteras de tamaño, Protobuf y métricas MLOps."""

from __future__ import annotations

import cv2
import numpy as np
import pytest

from defect_inspector.generated import defect_inspection_pb2
from defect_inspector.inference.config import NEU_CLASSES
from defect_inspector.inference.reader import InvalidImageError, read_industrial_image
from defect_inspector.mlops.eval_data import generate_synthetic_eval_batch
from defect_inspector.mlops.metrics import compute_evaluation_metrics


@pytest.mark.parametrize(
    ("height", "width", "should_pass"),
    [
        (16, 16, True),
        (17, 201, True),
        (201, 17, True),
        (15, 16, False),
        (16, 15, False),
        (8, 8, False),
    ],
)
def test_minimum_dimension_boundary_16px(
    height: int, width: int, should_pass: bool
) -> None:
    # Arrange
    img = np.full((height, width), 110, dtype=np.uint8)
    ok, buf = cv2.imencode(".png", img)
    assert ok

    # Act & Assert
    if should_pass:
        arr = read_industrial_image(buf.tobytes(), content_type="image/png")
        assert arr.shape[:2] == (height, width)
    else:
        with pytest.raises(InvalidImageError):
            read_industrial_image(buf.tobytes(), content_type="image/png")


@pytest.mark.parametrize("seed", [1, 42, 99])
def test_protobuf_roundtrip_and_eval_seeds(seed: int) -> None:
    # Arrange
    batch, _ = generate_synthetic_eval_batch(per_class=1, seed=seed)
    msg = defect_inspection_pb2.InspectRequest(
        image_bytes=batch[0].image_bytes,
        filename=batch[0].filename,
        content_type="image/png",
        conf_threshold=0.72,
        apply_clahe=True,
        request_id=f"seed-{seed}",
    )

    # Act
    decoded = defect_inspection_pb2.InspectRequest.FromString(msg.SerializeToString())

    # Assert
    assert len(batch) == len(NEU_CLASSES)
    assert decoded.filename == batch[0].filename
    assert pytest.approx(decoded.conf_threshold, abs=1e-5) == 0.72
    assert decoded.apply_clahe is True


def test_metrics_handles_single_class_roc_auc_fallback() -> None:
    # Arrange
    y_true = [0, 0, 0]
    y_pred = [0, 0, 1]
    probs = np.array(
        [
            [0.8, 0.2, 0.0, 0.0, 0.0, 0.0],
            [0.7, 0.3, 0.0, 0.0, 0.0, 0.0],
            [0.4, 0.6, 0.0, 0.0, 0.0, 0.0],
        ],
        dtype=np.float64,
    )

    # Act
    res = compute_evaluation_metrics(
        y_true_idx=y_true,
        y_pred_idx=y_pred,
        y_prob_matrix=probs,
        latencies_ms=[5.0, 6.0, 7.0],
        requires_review_flags=[False, False, True],
    )

    # Assert
    assert res["roc_auc_ovr"] == 0.0
    assert pytest.approx(res["accuracy"], abs=1e-3) == 0.6667
