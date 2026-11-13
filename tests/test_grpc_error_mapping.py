"""Pruebas unitarias AAA para mapeo de excepciones de dominio a gRPC StatusCodes."""

from __future__ import annotations

import grpc
import numpy as np
import pytest

from defect_inspector.api.error_mapping import map_exception_to_grpc_status
from defect_inspector.api.grpc_server import create_grpc_server
from defect_inspector.generated import (
    defect_inspection_pb2,
    defect_inspection_pb2_grpc,
)
from defect_inspector.inference.model_loader import OnnxDefectClassifier
from defect_inspector.services.exceptions import (
    DomainValidationError,
    InspectionProcessingError,
    ModelNotReadyError,
    UnsupportedImageFormatError,
)
from defect_inspector.services.inspection_service import DefectInspectionService


class _FakeSession:
    def get_inputs(self) -> list[object]:
        return []

    def run(
        self, output_names: list[str] | None, input_feed: dict[str, np.ndarray]
    ) -> list[np.ndarray]:
        return [np.array([[1.0, 0.0, 0.0, 0.0, 0.0, 0.0]], dtype=np.float32)]


def test_exception_mapping_table_matches_grpc_semantics() -> None:
    # Arrange & Act & Assert
    assert (
        map_exception_to_grpc_status(DomainValidationError("bad"))
        == grpc.StatusCode.INVALID_ARGUMENT
    )
    assert (
        map_exception_to_grpc_status(UnsupportedImageFormatError("mime"))
        == grpc.StatusCode.INVALID_ARGUMENT
    )
    assert (
        map_exception_to_grpc_status(ModelNotReadyError("unloaded"))
        == grpc.StatusCode.FAILED_PRECONDITION
    )
    assert (
        map_exception_to_grpc_status(InspectionProcessingError("boom"))
        == grpc.StatusCode.INTERNAL
    )


def test_grpc_endpoint_returns_invalid_argument_on_corrupt_image() -> None:
    # Arrange
    svc = DefectInspectionService(
        classifier=OnnxDefectClassifier(session=_FakeSession())
    )
    server, port = create_grpc_server(svc, host="127.0.0.1", port=0)
    server.start()
    try:
        # Act & Assert
        with grpc.insecure_channel(f"127.0.0.1:{port}") as ch:
            stub = defect_inspection_pb2_grpc.DefectInspectionServiceStub(ch)
            with pytest.raises(grpc.RpcError) as err:
                stub.InspectSurface(
                    defect_inspection_pb2.InspectRequest(
                        image_bytes=b"bad-bytes",
                        filename="bad.png",
                        content_type="image/png",
                    )
                )
            assert err.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    finally:
        server.stop(grace=0.5)
