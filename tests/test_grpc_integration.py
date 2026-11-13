"""Pruebas de integración gRPC + FastAPI Gateway con servidor efímero."""

from __future__ import annotations

from collections.abc import Callable

import grpc
import pytest
from fastapi.testclient import TestClient

from defect_inspector.api.error_mapping import map_exception_to_grpc_status
from defect_inspector.api.gateway import create_gateway_app, grpc_error_to_http
from defect_inspector.api.grpc_server import create_grpc_server
from defect_inspector.inference.config import NEU_CLASSES
from defect_inspector.services.exceptions import (
    DomainValidationError,
    InspectionProcessingError,
    ModelNotReadyError,
)
from defect_inspector.services.inspection_service import DefectInspectionService


@pytest.mark.parametrize("winner_idx", range(6))
@pytest.mark.parametrize("apply_clahe", [False, True])
def test_gateway_end_to_end_across_classes_and_clahe(
    make_encoded_image: Callable[[tuple[int, int], int, str], bytes],
    make_fake_service: Callable[[list[float] | None], DefectInspectionService],
    winner_idx: int,
    apply_clahe: bool,
) -> None:
    # Arrange
    logits = [0.0] * 6
    logits[winner_idx] = 5.0
    svc = make_fake_service(logits)
    server, port = create_grpc_server(svc, host="127.0.0.1", port=0)
    server.start()
    app = create_gateway_app(grpc_target=f"127.0.0.1:{port}")
    payload = make_encoded_image((96, 96), 3, ".png")

    try:
        with TestClient(app) as client:
            # Act
            resp = client.post(
                "/api/v1/inspect",
                files={"file": ("coil.png", payload, "image/png")},
                data={
                    "conf_threshold": "0.65",
                    "apply_clahe": "true" if apply_clahe else "false",
                },
            )

        # Assert
        assert resp.status_code == 200
        body = resp.json()
        assert body["predicted_class"] == NEU_CLASSES[winner_idx]
        assert body["applied_clahe"] is apply_clahe
        assert len(body["scores"]) == 6
    finally:
        server.stop(grace=0.5)


class _DummyRpcError(grpc.RpcError):
    def __init__(self, status_code: grpc.StatusCode, msg: str) -> None:
        self._code = status_code
        self._msg = msg

    def code(self) -> grpc.StatusCode:
        return self._code

    def details(self) -> str:
        return self._msg


@pytest.mark.parametrize(
    ("grpc_code", "expected_http"),
    [
        (grpc.StatusCode.INVALID_ARGUMENT, 400),
        (grpc.StatusCode.FAILED_PRECONDITION, 503),
        (grpc.StatusCode.UNAVAILABLE, 503),
        (grpc.StatusCode.DEADLINE_EXCEEDED, 504),
        (grpc.StatusCode.INTERNAL, 500),
        (grpc.StatusCode.UNKNOWN, 502),
    ],
)
def test_grpc_error_to_http_mapping_matrix(
    grpc_code: grpc.StatusCode, expected_http: int
) -> None:
    # Arrange & Act
    http_exc = grpc_error_to_http(_DummyRpcError(grpc_code, "detail"))

    # Assert
    assert http_exc.status_code == expected_http


def test_domain_to_grpc_status_mapping_covers_unexpected_exceptions() -> None:
    # Arrange & Act & Assert
    assert (
        map_exception_to_grpc_status(DomainValidationError("x"))
        == grpc.StatusCode.INVALID_ARGUMENT
    )
    assert (
        map_exception_to_grpc_status(ModelNotReadyError("x"))
        == grpc.StatusCode.FAILED_PRECONDITION
    )
    assert (
        map_exception_to_grpc_status(InspectionProcessingError("x"))
        == grpc.StatusCode.INTERNAL
    )
    assert map_exception_to_grpc_status(ValueError("x")) == grpc.StatusCode.INTERNAL
