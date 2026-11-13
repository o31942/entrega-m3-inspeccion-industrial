"""Pruebas de integración HTTP Gateway -> gRPC con FastAPI TestClient."""

from __future__ import annotations

import cv2
import numpy as np
from fastapi.testclient import TestClient

from defect_inspector.api.gateway import create_gateway_app
from defect_inspector.api.grpc_server import create_grpc_server
from defect_inspector.inference.model_loader import OnnxDefectClassifier
from defect_inspector.services.inspection_service import DefectInspectionService


class _FakeSession:
    def get_inputs(self) -> list[object]:
        return []

    def run(
        self, output_names: list[str] | None, input_feed: dict[str, np.ndarray]
    ) -> list[np.ndarray]:
        return [np.array([[0.1, 0.1, 0.1, 3.8, 0.1, 0.1]], dtype=np.float32)]


def test_gateway_routes_health_model_docs_and_inspect_via_grpc() -> None:
    # Arrange
    svc = DefectInspectionService(
        classifier=OnnxDefectClassifier(session=_FakeSession())
    )
    server, port = create_grpc_server(svc, host="127.0.0.1", port=0)
    server.start()
    gateway_app = create_gateway_app(grpc_target=f"127.0.0.1:{port}")
    ok, buf = cv2.imencode(".png", np.full((64, 64), 100, dtype=np.uint8))
    assert ok

    try:
        with TestClient(gateway_app) as client:
            # Act
            r_health = client.get("/health")
            r_model = client.get("/api/v1/model")
            r_docs = client.get("/docs")
            r_insp = client.post(
                "/api/v1/inspect",
                files={"file": ("plate.png", buf.tobytes(), "image/png")},
                data={"conf_threshold": "0.60", "apply_clahe": "true"},
            )

        # Assert
        assert r_health.status_code == 200
        assert r_health.json()["status"] == "SERVING"
        assert r_model.status_code == 200
        assert len(r_model.json()["classes"]) == 6
        assert r_docs.status_code == 200
        assert r_insp.status_code == 200
        body = r_insp.json()
        assert body["predicted_class"] == "pitted_surface"
        assert body["transport"] == "HTTP->gRPC"
    finally:
        server.stop(grace=0.5)
