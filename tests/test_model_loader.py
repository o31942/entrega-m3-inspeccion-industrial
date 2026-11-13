"""Pruebas unitarias AAA para carga ONNX y postprocesamiento softmax."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from defect_inspector.inference.config import NEU_CLASSES, ModelSpecConfig
from defect_inspector.inference.model_loader import (
    ModelLoadError,
    OnnxDefectClassifier,
    stable_softmax,
)


class _DummyInput:
    name = "image"


class _FakeOnnxSession:
    def __init__(self, logits: list[float]) -> None:
        self._logits = np.array([logits], dtype=np.float32)

    def get_inputs(self) -> list[object]:
        return [_DummyInput()]

    def run(
        self, output_names: list[str] | None, input_feed: dict[str, np.ndarray]
    ) -> list[np.ndarray]:
        assert "image" in input_feed
        return [self._logits]


def test_stable_softmax_sums_to_one_even_with_large_logits() -> None:
    # Arrange
    logits = np.array([1000.0, 1002.0, 999.0, 998.0, 997.0, 996.0], dtype=np.float32)

    # Act
    probs = stable_softmax(logits)

    # Assert
    assert np.isclose(np.sum(probs), 1.0, atol=1e-6)
    assert int(np.argmax(probs)) == 1


def test_onnx_classifier_raises_helpful_error_when_weights_missing(
    tmp_path: Path,
) -> None:
    # Arrange
    cfg = ModelSpecConfig(models_dir=tmp_path)

    # Act & Assert
    with pytest.raises(ModelLoadError):
        OnnxDefectClassifier(config=cfg)


def test_onnx_classifier_predicts_top_class_with_injected_session() -> None:
    # Arrange
    fake_session = _FakeOnnxSession([0.1, 0.2, 0.3, 0.4, 0.5, 4.2])
    clf = OnnxDefectClassifier(session=fake_session)
    tensor = np.zeros((1, 3, 224, 224), dtype=np.float32)

    # Act
    pred = clf.predict_tensor(tensor)

    # Assert
    assert pred.predicted_class == NEU_CLASSES[5]
    assert 0.85 < pred.confidence < 1.0
    assert abs(sum(pred.probabilities.values()) - 1.0) < 1e-4
