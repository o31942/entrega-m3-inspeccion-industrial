# SPEC-036 — US-36: Consolidación de cobertura y casos borde hasta >= 120 pruebas pytest

- **Etiqueta Kanban:** `qa`
- **Story Points (Fibonacci 1:1):** `3 SP`
- **Milestone:** `M3`

## Problema y Contexto
Consolidar el piso obligatorio de mínimo `120` pruebas `pytest` verdes auditando fronteras numéricas, casos borde de imágenes, contratos UI y serialización Protobuf.

## Requisitos Funcionales y No Funcionales
- Completar batería parametrizada hasta superar cómodamente 120 casos de prueba reales y significativos sin redundancias triviales.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** `uv run pytest -q`, **When** finaliza la ejecución completa, **Then** reporta `>= 120 passed`, `0 failed`, `0 skipped` y cero warnings.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
