"""Gateway delgado HTTP/JSON → gRPC para consumo desde navegador (/docs, /health)."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

import grpc
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from defect_inspector.api.schemas import (
    BoundingBoxSchema,
    ClassScoreSchema,
    HealthSchema,
    InspectionResponseSchema,
    ModelInfoSchema,
)
from defect_inspector.generated import (
    defect_inspection_pb2,
    defect_inspection_pb2_grpc,
)
from defect_inspector.inference.reader import ALLOWED_CONTENT_TYPES, MAX_IMAGE_BYTES

GRPC_TO_HTTP_STATUS: dict[grpc.StatusCode, int] = {
    grpc.StatusCode.INVALID_ARGUMENT: 400,
    grpc.StatusCode.FAILED_PRECONDITION: 503,
    grpc.StatusCode.UNAVAILABLE: 503,
    grpc.StatusCode.DEADLINE_EXCEEDED: 504,
    grpc.StatusCode.INTERNAL: 500,
}


def grpc_error_to_http(exc: grpc.RpcError) -> HTTPException:
    """Convierte RpcError en HTTPException conservando código semántico."""
    code = exc.code()
    status_code = GRPC_TO_HTTP_STATUS.get(code, 502)
    detail = exc.details() or str(code)
    return HTTPException(status_code=status_code, detail=detail)


def create_gateway_app(grpc_target: str | None = None) -> FastAPI:
    """Construye aplicación FastAPI actuando únicamente como proxy cliente gRPC."""
    target = grpc_target or os.getenv("GRPC_TARGET", "127.0.0.1:50051")

    @asynccontextmanager
    async def lifespan(app_instance: FastAPI) -> AsyncIterator[None]:
        channel = grpc.insecure_channel(target)
        app_instance.state.grpc_target = target
        app_instance.state.grpc_channel = channel
        app_instance.state.grpc_stub = (
            defect_inspection_pb2_grpc.DefectInspectionServiceStub(channel)
        )
        try:
            yield
        finally:
            channel.close()

    app_instance = FastAPI(
        title="NEU Steel Defect Inspector — HTTP/gRPC Gateway",
        version="0.1.0",
        description=(
            "Puente HTTP/JSON hacia el servidor gRPC DefectInspectionService (:50051). "
            "Cero inferencia o lógica de modelo dentro de este proceso."
        ),
        lifespan=lifespan,
    )
    app_instance.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:5173",
            "http://localhost:5173",
            "http://127.0.0.1:4173",
            "http://localhost:4173",
        ],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app_instance.get("/health", response_model=HealthSchema, tags=["Observabilidad"])
    async def health_check(request: Request) -> HealthSchema:
        stub: defect_inspection_pb2_grpc.DefectInspectionServiceStub = (
            request.app.state.grpc_stub
        )
        try:
            resp = stub.CheckHealth(defect_inspection_pb2.HealthRequest(), timeout=5.0)
        except grpc.RpcError as exc:
            raise grpc_error_to_http(exc) from exc
        return HealthSchema(
            status=resp.status,
            model_loaded=resp.model_loaded,
            model_id=resp.model_id,
            model_revision=resp.model_revision,
            runtime=resp.runtime,
            uptime_seconds=resp.uptime_seconds,
            grpc_target=request.app.state.grpc_target,
        )

    @app_instance.get(
        "/api/v1/model", response_model=ModelInfoSchema, tags=["Modelo MaaS"]
    )
    async def model_info(request: Request) -> ModelInfoSchema:
        stub: defect_inspection_pb2_grpc.DefectInspectionServiceStub = (
            request.app.state.grpc_stub
        )
        try:
            resp = stub.GetModelInfo(
                defect_inspection_pb2.ModelInfoRequest(), timeout=5.0
            )
        except grpc.RpcError as exc:
            raise grpc_error_to_http(exc) from exc
        return ModelInfoSchema(
            model_id=resp.model_id,
            model_revision=resp.model_revision,
            license=resp.license,
            hub_url=resp.hub_url,
            classes=list(resp.classes),
            input_size=resp.input_size,
            default_threshold=round(float(resp.default_threshold), 4),
        )

    @app_instance.post(
        "/api/v1/inspect",
        response_model=InspectionResponseSchema,
        tags=["Inferencia"],
    )
    async def inspect_surface(
        request: Request,
        file: Annotated[UploadFile, File(...)],
        conf_threshold: Annotated[float, Form(ge=0.05, le=0.99)] = 0.70,
        apply_clahe: Annotated[bool, Form()] = False,
    ) -> InspectionResponseSchema:
        content_type = (file.content_type or "").strip().lower().split(";", 1)[0]
        if content_type and content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=415,
                detail=f"Formato MIME no soportado: {file.content_type}",
            )
        payload = await file.read()
        if not payload:
            raise HTTPException(status_code=400, detail="El archivo subido está vacío.")
        if len(payload) > MAX_IMAGE_BYTES:
            raise HTTPException(
                status_code=413,
                detail="El archivo excede el límite máximo de 10 MB.",
            )

        stub: defect_inspection_pb2_grpc.DefectInspectionServiceStub = (
            request.app.state.grpc_stub
        )
        try:
            resp = stub.InspectSurface(
                defect_inspection_pb2.InspectRequest(
                    image_bytes=payload,
                    filename=file.filename or "upload.png",
                    content_type=content_type,
                    conf_threshold=conf_threshold,
                    apply_clahe=apply_clahe,
                ),
                timeout=15.0,
            )
        except grpc.RpcError as exc:
            raise grpc_error_to_http(exc) from exc

        return InspectionResponseSchema(
            request_id=resp.request_id,
            predicted_class=resp.predicted_class,
            predicted_label_es=resp.predicted_label_es,
            confidence=round(float(resp.confidence), 6),
            requires_human_review=resp.requires_human_review,
            decision_status=resp.decision_status,
            latency_ms=round(float(resp.latency_ms), 2),
            applied_clahe=resp.applied_clahe,
            conf_threshold=round(float(resp.conf_threshold), 4),
            model_id=resp.model_id,
            model_revision=resp.model_revision,
            scores=[
                ClassScoreSchema(
                    class_id=s.class_id,
                    class_name=s.class_name,
                    label_es=s.label_es,
                    probability=round(float(s.probability), 6),
                )
                for s in resp.scores
            ],
            roi_bbox=BoundingBoxSchema(
                x1=resp.roi_bbox.x1,
                y1=resp.roi_bbox.y1,
                x2=resp.roi_bbox.x2,
                y2=resp.roi_bbox.y2,
            ),
            overlay_png_base64=resp.overlay_png_base64,
        )

    return app_instance


app = create_gateway_app()
