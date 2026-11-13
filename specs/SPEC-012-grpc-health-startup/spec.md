# SPEC-012 — US-12: Arranque servidor gRPC (:50051) con carga única y grpc.health.v1

- **Etiqueta Kanban:** `backend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
El servidor gRPC (`:50051`) debe cargar el modelo MaaS una única vez antes de servir tráfico y registrar el servicio estándar `grpc.health.v1.Health`.

## Requisitos Funcionales y No Funcionales
- Construir `create_grpc_server(service, host, port)` con `ThreadPoolExecutor` y `health.HealthServicer` (`SERVING`).
- Garantizar arranque reproducible en `:50051` y cierre limpio ante `SIGINT`/`SIGTERM`.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** el arranque del servidor gRPC en puerto libre, **When** un cliente consulta `grpc.health.v1.Health/Check` o `CheckHealth`, **Then** responde `SERVING` y `model_loaded=True` sin recargar el modelo por petición.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
