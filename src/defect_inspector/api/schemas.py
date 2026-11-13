"""Esquemas tipados Pydantic para el Gateway HTTP→gRPC y documentación OpenAPI."""

from __future__ import annotations

from pydantic import BaseModel, Field


class HealthSchema(BaseModel):
    """Respuesta de estado del servidor gRPC subyacente."""

    status: str = Field(..., examples=["SERVING"])
    model_loaded: bool
    model_id: str
    model_revision: str
    runtime: str
    uptime_seconds: int
    grpc_target: str


class ModelInfoSchema(BaseModel):
    """Metadatos del modelo MaaS expuestos por gRPC."""

    model_id: str
    model_revision: str
    license: str
    hub_url: str
    classes: list[str]
    input_size: int
    default_threshold: float


class ClassScoreSchema(BaseModel):
    """Probabilidad calibrada por clase de defecto."""

    class_id: int
    class_name: str
    label_es: str
    probability: float


class BoundingBoxSchema(BaseModel):
    """Coordenadas ROI del mapa de saliencia."""

    x1: int
    y1: int
    x2: int
    y2: int


class InspectionResponseSchema(BaseModel):
    """Respuesta unificada entregada al cliente web desacoplado."""

    request_id: str
    predicted_class: str
    predicted_label_es: str
    confidence: float
    requires_human_review: bool
    decision_status: str
    latency_ms: float
    applied_clahe: bool
    conf_threshold: float
    model_id: str
    model_revision: str
    transport: str = "HTTP->gRPC"
    scores: list[ClassScoreSchema]
    roi_bbox: BoundingBoxSchema
    overlay_png_base64: str
