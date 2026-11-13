"""Contratos de transferencia de datos (DTOs) puros en Python para Capa 2."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class ClassScoreDTO:
    """Puntaje de probabilidad calibrado para una clase de defecto NEU."""

    class_id: int
    class_name: str
    label_es: str
    probability: float


@dataclass(frozen=True, slots=True)
class BoundingBoxDTO:
    """Caja delimitadora ROI de mayor respuesta espacial (píxeles en 224x224)."""

    x1: int
    y1: int
    x2: int
    y2: int


@dataclass(frozen=True, slots=True)
class HealthDTO:
    """Estado de salud del servicio y carga del modelo MaaS."""

    status: str
    model_loaded: bool
    model_id: str
    model_revision: str
    runtime: str
    uptime_seconds: int


@dataclass(frozen=True, slots=True)
class ModelInfoDTO:
    """Metadatos verificables del modelo preentrenado registrado."""

    model_id: str
    model_revision: str
    license: str
    hub_url: str
    classes: tuple[str, ...]
    input_size: int
    default_threshold: float


@dataclass(frozen=True, slots=True)
class InspectionResponseDTO:
    """Resultado completo tipado de inspección superficial."""

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
    scores: tuple[ClassScoreDTO, ...]
    roi_bbox: BoundingBoxDTO
    overlay_png_base64: str

    def to_dict(self) -> dict[str, object]:
        """Serializa el DTO a diccionario estándar de Python."""
        payload = asdict(self)
        payload["scores"] = list(payload["scores"])
        return payload
