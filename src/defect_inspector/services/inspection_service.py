"""Orquestador de lógica de negocio en Capa 2 con política HITL configurable."""

from __future__ import annotations

import time
import uuid

from defect_inspector.inference.config import (
    NEU_CLASSES,
    NEU_CLASSES_ES,
    ModelSpecConfig,
)
from defect_inspector.inference.explainability import compute_saliency_and_roi
from defect_inspector.inference.model_loader import (
    ModelLoadError,
    OnnxDefectClassifier,
)
from defect_inspector.inference.preprocessor import preprocess_image
from defect_inspector.inference.reader import (
    InvalidImageError,
    UnsupportedMediaError,
    read_industrial_image,
)
from defect_inspector.services.dtos import (
    BoundingBoxDTO,
    ClassScoreDTO,
    HealthDTO,
    InspectionResponseDTO,
    ModelInfoDTO,
)
from defect_inspector.services.exceptions import (
    DomainValidationError,
    InspectionProcessingError,
    ModelNotReadyError,
    UnsupportedImageFormatError,
)

MIN_THRESHOLD = 0.05
MAX_THRESHOLD = 0.99


class DefectInspectionService:
    """Servicio desacoplado de inspección superficial NEU-DET (Capa 2)."""

    def __init__(
        self,
        classifier: OnnxDefectClassifier,
        config: ModelSpecConfig | None = None,
    ) -> None:
        self._classifier = classifier
        self._config = config or classifier.config
        self._started_at = time.monotonic()

    def check_health(self) -> HealthDTO:
        """Retorna estado operativo del servicio y modelo precargado en RAM."""
        uptime = int(max(0.0, time.monotonic() - self._started_at))
        return HealthDTO(
            status="SERVING",
            model_loaded=True,
            model_id=self._config.model_id,
            model_revision=self._config.revision,
            runtime=self._classifier.runtime_name,
            uptime_seconds=uptime,
        )

    def get_model_info(self) -> ModelInfoDTO:
        """Expone ficha técnica reproducible del modelo MaaS activo."""
        return ModelInfoDTO(
            model_id=self._config.model_id,
            model_revision=self._config.revision,
            license=self._config.license_name,
            hub_url=self._config.hub_url,
            classes=NEU_CLASSES,
            input_size=self._config.input_size,
            default_threshold=self._config.default_threshold,
        )

    def inspect(
        self,
        image_bytes: bytes,
        filename: str = "sample.png",
        content_type: str = "",
        conf_threshold: float | None = None,
        apply_clahe: bool = False,
        request_id: str = "",
    ) -> InspectionResponseDTO:
        """Ejecuta inspección completa con umbral HITL y trazabilidad temporal."""
        t0 = time.perf_counter()
        threshold = (
            self._config.default_threshold
            if conf_threshold is None or conf_threshold <= 0.0
            else float(conf_threshold)
        )
        if not MIN_THRESHOLD <= threshold <= MAX_THRESHOLD:
            raise DomainValidationError(
                f"Umbral conf_threshold={threshold} fuera de rango [{MIN_THRESHOLD}, {MAX_THRESHOLD}]."
            )

        req_id = request_id.strip() or f"insp-{uuid.uuid4().hex[:10]}"
        try:
            gray = read_industrial_image(image_bytes, content_type=content_type)
            tensor, resized_224 = preprocess_image(
                gray,
                apply_clahe=apply_clahe,
                target_size=self._config.input_size,
            )
            pred = self._classifier.predict_tensor(tensor)
            saliency = compute_saliency_and_roi(resized_224)
        except UnsupportedMediaError as exc:
            raise UnsupportedImageFormatError(str(exc)) from exc
        except InvalidImageError as exc:
            raise DomainValidationError(str(exc)) from exc
        except ModelLoadError as exc:
            raise ModelNotReadyError(str(exc)) from exc
        except Exception as exc:
            raise InspectionProcessingError(
                f"Error procesando {filename}: {exc}"
            ) from exc

        requires_review = pred.confidence < threshold
        decision = "LOW_CONFIDENCE_REVIEW" if requires_review else "DEFECT_DETECTED"
        scores = tuple(
            sorted(
                (
                    ClassScoreDTO(
                        class_id=idx,
                        class_name=cls_name,
                        label_es=NEU_CLASSES_ES[cls_name],
                        probability=pred.probabilities[cls_name],
                    )
                    for idx, cls_name in enumerate(NEU_CLASSES)
                ),
                key=lambda item: item.probability,
                reverse=True,
            )
        )
        latency_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        return InspectionResponseDTO(
            request_id=req_id,
            predicted_class=pred.predicted_class,
            predicted_label_es=pred.predicted_label_es,
            confidence=pred.confidence,
            requires_human_review=requires_review,
            decision_status=decision,
            latency_ms=latency_ms,
            applied_clahe=apply_clahe,
            conf_threshold=round(threshold, 4),
            model_id=self._config.model_id,
            model_revision=self._config.revision,
            scores=scores,
            roi_bbox=BoundingBoxDTO(*saliency.roi_bbox),
            overlay_png_base64=saliency.overlay_png_base64,
        )
