"""Implementación del Servicer gRPC (Capa 3 pura sin lógica de modelo)."""

from __future__ import annotations

import grpc

from defect_inspector.api.error_mapping import handle_grpc_errors
from defect_inspector.generated import (
    defect_inspection_pb2,
    defect_inspection_pb2_grpc,
)
from defect_inspector.services.inspection_service import DefectInspectionService


class DefectInspectionServicer(
    defect_inspection_pb2_grpc.DefectInspectionServiceServicer
):
    """Traduce peticiones Protobuf hacia DefectInspectionService y viceversa."""

    def __init__(self, service: DefectInspectionService) -> None:
        self._service = service

    def CheckHealth(
        self,
        request: defect_inspection_pb2.HealthRequest,
        context: grpc.ServicerContext,
    ) -> defect_inspection_pb2.HealthResponse:
        dto = self._service.check_health()
        return defect_inspection_pb2.HealthResponse(
            status=dto.status,
            model_loaded=dto.model_loaded,
            model_id=dto.model_id,
            model_revision=dto.model_revision,
            runtime=dto.runtime,
            uptime_seconds=dto.uptime_seconds,
        )

    def GetModelInfo(
        self,
        request: defect_inspection_pb2.ModelInfoRequest,
        context: grpc.ServicerContext,
    ) -> defect_inspection_pb2.ModelInfoResponse:
        info = self._service.get_model_info()
        return defect_inspection_pb2.ModelInfoResponse(
            model_id=info.model_id,
            model_revision=info.model_revision,
            license=info.license,
            hub_url=info.hub_url,
            classes=list(info.classes),
            input_size=info.input_size,
            default_threshold=info.default_threshold,
        )

    @handle_grpc_errors
    def InspectSurface(
        self,
        request: defect_inspection_pb2.InspectRequest,
        context: grpc.ServicerContext,
    ) -> defect_inspection_pb2.InspectResponse:
        dto = self._service.inspect(
            image_bytes=request.image_bytes,
            filename=request.filename or "upload.png",
            content_type=request.content_type,
            conf_threshold=request.conf_threshold
            if request.conf_threshold > 0
            else None,
            apply_clahe=bool(request.apply_clahe),
            request_id=request.request_id,
        )
        return defect_inspection_pb2.InspectResponse(
            request_id=dto.request_id,
            predicted_class=dto.predicted_class,
            predicted_label_es=dto.predicted_label_es,
            confidence=dto.confidence,
            requires_human_review=dto.requires_human_review,
            decision_status=dto.decision_status,
            latency_ms=dto.latency_ms,
            applied_clahe=dto.applied_clahe,
            conf_threshold=dto.conf_threshold,
            model_id=dto.model_id,
            model_revision=dto.model_revision,
            scores=[
                defect_inspection_pb2.ClassScore(
                    class_id=s.class_id,
                    class_name=s.class_name,
                    label_es=s.label_es,
                    probability=s.probability,
                )
                for s in dto.scores
            ],
            roi_bbox=defect_inspection_pb2.BoundingBox(
                x1=dto.roi_bbox.x1,
                y1=dto.roi_bbox.y1,
                x2=dto.roi_bbox.x2,
                y2=dto.roi_bbox.y2,
            ),
            overlay_png_base64=dto.overlay_png_base64,
        )
