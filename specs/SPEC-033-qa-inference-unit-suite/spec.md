# SPEC-033 — US-33: Suite unitaria AAA sintética para ingesta, CLAHE y cargador ONNX

- **Etiqueta Kanban:** `qa`
- **Story Points (Fibonacci 1:1):** `3 SP`
- **Milestone:** `M3`

## Problema y Contexto
El M3 hereda la exigencia de mínimo 120 pruebas `pytest` con patrón AAA, datos sintéticos, cero acceso a red y cero dependencia de GPU o dataset crudo.

## Requisitos Funcionales y No Funcionales
- Ampliar `tests/conftest.py` y crear baterías parametrizadas exhaustivas de ingesta, preprocesamiento CLAHE y cargador ONNX con sesión falsa determinista.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** ejecución offline `uv run pytest -q`, **When** corren las pruebas de capa `inference/`, **Then** todas siguen patrón AAA y pasan 100%.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
