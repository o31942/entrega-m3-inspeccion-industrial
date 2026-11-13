"""Pruebas AAA para códigos HTTP 400/415/422/503 y cabeceras CORS en Gateway."""

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
        return [np.array([[1.0, 0.0, 0.0, 0.0, 0.0, 0.0]], dtype=np.float32)]


def test_gateway_returns_415_400_422_and_cors_headers() -> None:
    # Arrange
    svc = DefectInspectionService(
        classifier=OnnxDefectClassifier(session=_FakeSession())
    )
    server, port = create_grpc_server(svc, host="127.0.0.1", port=0)
    server.start()
    app = create_gateway_app(grpc_target=f"127.0.0.1:{port}")
    ok, valid_png = cv2.imencode(".png", np.full((64, 64), 90, dtype=np.uint8))
    assert ok

    try:
        with TestClient(app) as client:
            # Act
            r_mime = client.post(
                "/api/v1/inspect",
                files={"file": ("notes.txt", b"hello", "text/plain")},
            )
            r_empty = client.post(
                "/api/v1/inspect",
                files={"file": ("empty.png", b"", "image/png")},
            )
            r_corrupt = client.post(
                "/api/v1/inspect",
                files={"file": ("bad.png", b"not-an-image", "image/png")},
            )
            r_thresh = client.post(
                "/api/v1/inspect",
                files={"file": ("ok.png", valid_png.tobytes(), "image/png")},
                data={"conf_threshold": "1.99"},
            )
            r_cors = client.options(
                "/api/v1/inspect",
                headers={
                    "Origin": "http://127.0.0.1:5173",
                    "Access-Control-Request-Method": "POST",
                },
            )

        # Assert
        assert r_mime.status_code == 415
        assert r_empty.status_code == 400
        assert r_corrupt.status_code == 400
        assert r_thresh.status_code == 422
        assert (
            r_cors.headers.get("access-control-allow-origin") == "http://127.0.0.1:5173"
        )
    finally:
        server.stop(grace=0.5)


def test_gateway_returns_503_when_grpc_backend_is_unavailable() -> None:
    # Arrange
    app = create_gateway_app(grpc_target="127.0.0.1:59999")

    # Act
    with TestClient(app) as client:
        resp = client.get("/health")

    # Assert
    assert resp.status_code == 503
