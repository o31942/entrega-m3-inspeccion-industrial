# SPEC-034 — US-34: Suite unitaria AAA para capa de servicio, umbrales HITL y errores

- **Etiqueta Kanban:** `qa`
- **Story Points (Fibonacci 1:1):** `3 SP`
- **Milestone:** `M3`

## Problema y Contexto
Verificar exhaustivamente toda la lógica de negocio HITL, fronteras de umbral, DTOs y excepciones en `services/` ante entradas válidas y adversas.

## Requisitos Funcionales y No Funcionales
- Implementar suite exhaustiva parametrizada para `DefectInspectionService` cubriendo todas las clases, decisiones (`DEFECT_DETECTED`, `LOW_CONFIDENCE_REVIEW`), tiempos y códigos de error.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** combinaciones parametrizadas de logits y umbrales, **When** se evalúa `DefectInspectionService`, **Then** verifica comportamiento exacto sin depender de ONNX real en disco.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
