"""Pruebas AAA para el cliente CLI gRPC contra servidor efímero."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from defect_inspector.api.grpc_client import call_health, call_inspect
from defect_inspector.api.grpc_server import create_grpc_server
from defect_inspector.inference.model_loader import OnnxDefectClassifier
from defect_inspector.services.inspection_service import DefectInspectionService


class _FakeSession:
    def get_inputs(self) -> list[object]:
        return []

    def run(
        self, output_names: list[str] | None, input_feed: dict[str, np.ndarray]
    ) -> list[np.ndarray]:
        return [np.array([[0.0, 0.1, 4.5, 0.0, 0.0, 0.0]], dtype=np.float32)]


def test_grpc_cli_client_roundtrip(tmp_path: Path) -> None:
    # Arrange
    svc = DefectInspectionService(
        classifier=OnnxDefectClassifier(session=_FakeSession())
    )
    server, port = create_grpc_server(svc, host="127.0.0.1", port=0)
    server.start()
    img_path = tmp_path / "steel.png"
    ok, buf = cv2.imencode(".png", np.full((64, 64), 130, dtype=np.uint8))
    assert ok
    img_path.write_bytes(buf.tobytes())
    target = f"127.0.0.1:{port}"

    try:
        # Act
        health_out = call_health(target=target)
        insp_out = call_inspect(
            img_path, target=target, conf_threshold=0.70, apply_clahe=True
        )

        # Assert
        assert health_out["status"] == "SERVING"
        assert insp_out["predicted_class"] == "patches"
        assert insp_out["requires_human_review"] is False
    finally:
        server.stop(grace=0.5)
