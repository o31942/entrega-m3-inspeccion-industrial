# SPEC-017 — US-17: Lanzador unificado backend (:50051 + :8000) y logging estructurado

- **Etiqueta Kanban:** `backend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
Arrancar servidor gRPC (`:50051`) y gateway HTTP (`:8000`) con un solo comando `make backend` requiere un lanzador multiproceso coordinado y logging estructurado.

## Requisitos Funcionales y No Funcionales
- Implementar `src/defect_inspector/api/run_backend.py` levantando gRPC primero, esperando su readiness y lanzando Uvicorn Gateway en el mismo flujo supervisado.
- Emitir logs estructurados JSON/key-value con `request_id` y `latency_ms`.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** `uv run python -m defect_inspector.api.run_backend`, **When** ambos procesos arrancan, **Then** `:50051` y `:8000` responden salud y detienen limpio ante Ctrl+C.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
