"""Pruebas de arranque efímero gRPC y verificación grpc.health.v1."""

from __future__ import annotations

import grpc
import numpy as np
from grpc_health.v1 import health_pb2, health_pb2_grpc

from defect_inspector.api.grpc_server import create_grpc_server
from defect_inspector.generated import (
    defect_inspection_pb2,
    defect_inspection_pb2_grpc,
)
from defect_inspector.inference.model_loader import OnnxDefectClassifier
from defect_inspector.services.inspection_service import DefectInspectionService


class _FakeSession:
    def get_inputs(self) -> list[object]:
        return []

    def run(
        self, output_names: list[str] | None, input_feed: dict[str, np.ndarray]
    ) -> list[np.ndarray]:
        return [np.array([[3.0, 0.2, 0.1, 0.0, 0.0, 0.0]], dtype=np.float32)]


def test_ephemeral_grpc_server_serves_health_and_standard_probe() -> None:
    # Arrange
    svc = DefectInspectionService(
        classifier=OnnxDefectClassifier(session=_FakeSession())
    )
    server, port = create_grpc_server(svc, host="127.0.0.1", port=0)
    server.start()
    try:
        # Act
        with grpc.insecure_channel(f"127.0.0.1:{port}") as channel:
            std_stub = health_pb2_grpc.HealthStub(channel)
            std_resp = std_stub.Check(health_pb2.HealthCheckRequest(service=""))
            app_stub = defect_inspection_pb2_grpc.DefectInspectionServiceStub(channel)
            app_resp = app_stub.CheckHealth(defect_inspection_pb2.HealthRequest())

        # Assert
        assert std_resp.status == health_pb2.HealthCheckResponse.SERVING
        assert app_resp.status == "SERVING"
        assert app_resp.model_loaded is True
    finally:
        server.stop(grace=0.5)
