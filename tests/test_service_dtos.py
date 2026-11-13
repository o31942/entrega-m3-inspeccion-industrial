"""Pruebas unitarias AAA para DTOs, excepciones y desacoplamiento de Capa 2."""

from __future__ import annotations

from pathlib import Path

from defect_inspector.services.dtos import (
    BoundingBoxDTO,
    ClassScoreDTO,
    HealthDTO,
    InspectionResponseDTO,
)
from defect_inspector.services.exceptions import (
    DefectInspectorError,
    DomainValidationError,
    ModelNotReadyError,
)


def test_services_layer_never_imports_grpc_or_fastapi() -> None:
    # Arrange
    svc_dir = (
        Path(__file__).resolve().parent.parent / "src" / "defect_inspector" / "services"
    )

    # Act & Assert
    for py_file in svc_dir.glob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        assert "import grpc" not in content
        assert "from grpc" not in content
        assert "import fastapi" not in content
        assert "from fastapi" not in content


def test_inspection_dto_to_dict_preserves_types() -> None:
    # Arrange
    dto = InspectionResponseDTO(
        request_id="r-1",
        predicted_class="inclusion",
        predicted_label_es="Inclusión (Inclusion)",
        confidence=0.88,
        requires_human_review=False,
        decision_status="DEFECT_DETECTED",
        latency_ms=14.2,
        applied_clahe=True,
        conf_threshold=0.70,
        model_id="senanurcetin/neu-steel-defect-resnet18",
        model_revision="ad13c70618a8a28a50309456dd40d9a45b2869d1",
        scores=(ClassScoreDTO(1, "inclusion", "Inclusión (Inclusion)", 0.88),),
        roi_bbox=BoundingBoxDTO(10, 10, 120, 120),
        overlay_png_base64="abc",
    )

    # Act
    data = dto.to_dict()

    # Assert
    assert data["predicted_class"] == "inclusion"
    assert isinstance(data["scores"], list)
    assert issubclass(DomainValidationError, DefectInspectorError)
    assert issubclass(ModelNotReadyError, DefectInspectorError)
    assert HealthDTO("SERVING", True, "m", "rev", "ONNX", 5).model_loaded is True
