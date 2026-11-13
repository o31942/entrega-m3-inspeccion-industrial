# SPEC-010 — US-10: Orquestador DefectInspectionService con regla HITL configurable

- **Etiqueta Kanban:** `backend`
- **Story Points (Fibonacci 1:1):** `3 SP`
- **Milestone:** `M3`

## Problema y Contexto
El caso de uso completo debe validar el umbral (`0.05 <= conf_threshold <= 0.99`), invocar ingesta/preprocesamiento/ONNX/XAI y aplicar la política HITL (`LOW_CONFIDENCE_REVIEW` vs `DEFECT_DETECTED`).

## Requisitos Funcionales y No Funcionales
- Implementar `DefectInspectionService` con métodos `check_health()`, `get_model_info()` e `inspect(...)`.
- Medir `latency_ms` precisa y marcar `requires_human_review = confidence < conf_threshold`.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** una predicción con `confidence=0.62` y `conf_threshold=0.70`, **When** `inspect` resuelve, **Then** `requires_human_review=True` y `decision_status='LOW_CONFIDENCE_REVIEW'`.
2. **Given** `conf_threshold=1.5` inválido, **When** se llama `inspect`, **Then** lanza `DomainValidationError`.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
