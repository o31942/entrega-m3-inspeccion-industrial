"""Pruebas unitarias para stubs compilados de Protobuf gRPC."""

from __future__ import annotations

from defect_inspector.generated import (
    defect_inspection_pb2,
    defect_inspection_pb2_grpc,
)


def test_inspect_request_roundtrip_serialization() -> None:
    # Arrange
    req = defect_inspection_pb2.InspectRequest(
        image_bytes=b"pngbytes",
        filename="sample.png",
        content_type="image/png",
        conf_threshold=0.72,
        apply_clahe=True,
        request_id="req-001",
    )

    # Act
    raw = req.SerializeToString()
    restored = defect_inspection_pb2.InspectRequest()
    restored.ParseFromString(raw)

    # Assert
    assert restored.image_bytes == b"pngbytes"
    assert restored.filename == "sample.png"
    assert restored.apply_clahe is True
    assert abs(restored.conf_threshold - 0.72) < 1e-5
    assert restored.request_id == "req-001"


def test_inspect_response_contains_scores_and_bbox() -> None:
    # Arrange
    resp = defect_inspection_pb2.InspectResponse(
        request_id="req-002",
        predicted_class="scratches",
        predicted_label_es="Rayaduras (Scratches)",
        confidence=0.94,
        requires_human_review=False,
        decision_status="DEFECT_DETECTED",
        latency_ms=18.5,
        applied_clahe=True,
        conf_threshold=0.70,
        model_id="senanurcetin/neu-steel-defect-resnet18",
        model_revision="ad13c70618a8a28a50309456dd40d9a45b2869d1",
        scores=[
            defect_inspection_pb2.ClassScore(
                class_id=5,
                class_name="scratches",
                label_es="Rayaduras (Scratches)",
                probability=0.94,
            )
        ],
        roi_bbox=defect_inspection_pb2.BoundingBox(x1=10, y1=20, x2=180, y2=190),
        overlay_png_base64="AAAA",
    )

    # Act
    payload = resp.SerializeToString()
    decoded = defect_inspection_pb2.InspectResponse()
    decoded.ParseFromString(payload)

    # Assert
    assert decoded.predicted_class == "scratches"
    assert len(decoded.scores) == 1
    assert decoded.roi_bbox.x2 == 180
    assert hasattr(defect_inspection_pb2_grpc, "DefectInspectionServiceStub")
