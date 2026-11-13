# SPEC-035 — US-35: Pruebas de integración en vivo gRPC server y HTTP Gateway sin red externa

- **Etiqueta Kanban:** `qa`
- **Story Points (Fibonacci 1:1):** `3 SP`
- **Milestone:** `M3`

## Problema y Contexto
Las capas de transporte (`grpc_server.py`, `grpc_client.py`, `gateway.py`) deben probarse de extremo a extremo en memoria/puerto efímero local sin tocar Hugging Face ni red externa.

## Requisitos Funcionales y No Funcionales
- Crear pruebas de integración en vivo levantando `DefectInspectionServiceServicer` en puerto local efímero (`127.0.0.1:0`) y cliente FastAPI `TestClient` conectado a gRPC.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** servidor gRPC efímero y gateway de prueba, **When** se invoca `CheckHealth`, `GetModelInfo`, `InspectSurface` y `POST /api/v1/inspect`, **Then** validan status `200`, `400`, `415`, `422` y respuesta completa.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
