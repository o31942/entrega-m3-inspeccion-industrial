"""Pruebas unitarias AAA para `scripts/evaluar.py` (sin servidor externo)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import cv2
import numpy as np

from defect_inspector.inference.model_loader import OnnxDefectClassifier
from defect_inspector.mlops.eval_data import EvalSample
from defect_inspector.services.inspection_service import DefectInspectionService

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "evaluar.py"


class _FakeSession:
    def get_inputs(self) -> list[object]:
        return []

    def run(
        self, output_names: list[str] | None, input_feed: dict[str, np.ndarray]
    ) -> list[np.ndarray]:
        return [np.array([[3.5, 0.2, 0.1, 0.1, 0.0, 0.0]], dtype=np.float32)]


def test_evaluar_module_loads_and_computes_metrics_with_fake_session() -> None:
    # Arrange
    spec = importlib.util.spec_from_file_location("evaluar_mod", SCRIPT_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["evaluar_mod"] = mod
    spec.loader.exec_module(mod)

    svc = DefectInspectionService(
        classifier=OnnxDefectClassifier(session=_FakeSession())
    )
    ok, buf = cv2.imencode(".png", np.full((64, 64), 100, dtype=np.uint8))
    assert ok
    samples = [
        EvalSample("id-1", "a.png", "crazing", 0, buf.tobytes(), "synth"),
        EvalSample("id-2", "b.png", "inclusion", 1, buf.tobytes(), "synth"),
    ]
    plan = mod.EvalRunPlan("test-run", apply_clahe=True, conf_threshold=0.70)

    # Act
    metrics, y_true, y_pred, rows = mod.evaluate_plan_once(svc, samples, plan)

    # Assert
    assert len(mod.DEFAULT_PLANS) >= 3
    assert len(y_true) == 2 and len(y_pred) == 2
    assert metrics["accuracy"] == 0.5
    assert len(rows) >= 1
