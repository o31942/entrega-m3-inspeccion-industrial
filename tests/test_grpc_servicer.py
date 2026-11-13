"""Pruebas unitarias AAA del Servicer gRPC y separación de capas."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from defect_inspector.api.grpc_servicer import DefectInspectionServicer
from defect_inspector.generated import defect_inspection_pb2
from defect_inspector.inference.model_loader import OnnxDefectClassifier
from defect_inspector.services.inspection_service import DefectInspectionService


class _FakeSession:
    def get_inputs(self) -> list[object]:
        return []

    def run(
        self, output_names: list[str] | None, input_feed: dict[str, np.ndarray]
    ) -> list[np.ndarray]:
        return [np.array([[0.2, 4.1, 0.1, 0.0, 0.0, 0.0]], dtype=np.float32)]


def test_grpc_servicer_file_contains_no_opencv_or_onnx_logic() -> None:
    # Arrange
    path = (
        Path(__file__).resolve().parent.parent
        / "src"
        / "defect_inspector"
        / "api"
        / "grpc_servicer.py"
    )
    txt = path.read_text(encoding="utf-8")

    # Act & Assert
    assert "import cv2" not in txt
    assert "onnxruntime" not in txt


def test_grpc_servicer_handles_health_model_info_and_inspect() -> None:
    # Arrange
    svc = DefectInspectionService(
        classifier=OnnxDefectClassifier(session=_FakeSession())
    )
    servicer = DefectInspectionServicer(svc)
    ok, buf = cv2.imencode(".png", np.full((64, 64), 120, dtype=np.uint8))
    assert ok

    # Act
    h = servicer.CheckHealth(defect_inspection_pb2.HealthRequest(), None)  # type: ignore[arg-type]
    m = servicer.GetModelInfo(defect_inspection_pb2.ModelInfoRequest(), None)  # type: ignore[arg-type]
    r = servicer.InspectSurface(
        defect_inspection_pb2.InspectRequest(
            image_bytes=buf.tobytes(),
            filename="coil.png",
            content_type="image/png",
            conf_threshold=0.70,
            apply_clahe=False,
        ),
        None,  # type: ignore[arg-type]
    )

    # Assert
    assert h.status == "SERVING"
    assert h.model_loaded is True
    assert len(m.classes) == 6
    assert r.predicted_class == "inclusion"
    assert len(r.scores) == 6
