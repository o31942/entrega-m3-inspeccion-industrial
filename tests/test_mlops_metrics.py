"""Pruebas AAA para métricas multiclase y generación PNG de matriz de confusión."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from defect_inspector.inference.config import NEU_CLASSES
from defect_inspector.mlops.metrics import (
    compute_evaluation_metrics,
    save_confusion_matrix_png,
)


def test_compute_evaluation_metrics_returns_finite_quality_and_latency() -> None:
    # Arrange
    y_true = [0, 1, 2, 3, 4, 5]
    y_pred = [0, 1, 2, 3, 4, 5]
    probs = np.eye(6, dtype=np.float64) * 0.90 + 0.02
    probs = probs / probs.sum(axis=1, keepdims=True)
    latencies = [10.0, 12.0, 14.0, 11.0, 13.0, 20.0]
    reviews = [False, False, False, True, False, False]

    # Act
    metrics = compute_evaluation_metrics(y_true, y_pred, probs, latencies, reviews)

    # Assert
    assert metrics["accuracy"] == 1.0
    assert metrics["macro_f1"] == 1.0
    assert metrics["latency_p95_ms"] >= metrics["latency_mean_ms"]
    assert metrics["throughput_img_s"] > 0.0
    assert abs(metrics["hitl_review_rate"] + metrics["auto_decision_rate"] - 1.0) < 1e-4


def test_save_confusion_matrix_png_creates_valid_image(tmp_path: Path) -> None:
    # Arrange
    out = tmp_path / "cm.png"

    # Act
    saved = save_confusion_matrix_png(
        y_true_idx=[0, 1, 2, 3, 4, 5],
        y_pred_idx=[0, 1, 1, 3, 4, 5],
        class_names=NEU_CLASSES,
        out_path=out,
    )

    # Assert
    assert saved.is_file()
    assert saved.read_bytes().startswith(b"\x89PNG")
