# SPEC-015 — US-15: API Gateway HTTP→gRPC (:8000) con /health, /docs y /api/v1/inspect

- **Etiqueta Kanban:** `backend`
- **Story Points (Fibonacci 1:1):** `3 SP`
- **Milestone:** `M3`

## Problema y Contexto
Los navegadores web modernos no hablan HTTP/2 gRPC binario directamente sin proxy; un gateway delgado en `:8000` traduce HTTP/JSON + OpenAPI (`/docs`) a llamadas gRPC reales hacia `:50051`.

## Requisitos Funcionales y No Funcionales
- Exponer `GET /health`, `GET /api/v1/model`, `POST /api/v1/inspect` en `src/defect_inspector/api/gateway.py`.
- Delegar TODA operación al stub gRPC `DefectInspectionServiceStub` (cero inferencia en el gateway).
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** el gateway HTTP activo conectado al servidor gRPC, **When** se consulta `GET /docs`, `GET /health` o `POST /api/v1/inspect`, **Then** responde OpenAPI Swagger y reenvía la petición vía gRPC retornando JSON tipado.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
