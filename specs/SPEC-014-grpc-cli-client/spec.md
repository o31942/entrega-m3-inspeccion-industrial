# SPEC-014 — US-14: Cliente CLI gRPC para verificación directa en terminal

- **Etiqueta Kanban:** `backend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
Durante la sustentación de gRPC se debe demostrar un cliente Python independiente invocando directamente al servidor `:50051` en terminal.

## Requisitos Funcionales y No Funcionales
- Crear CLI `python -m defect_inspector.api.grpc_client` con subcomandos `--health`, `--info` e `--image <ruta>`.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** el servidor gRPC activo, **When** se invoca `grpc_client --health` o `--image`, **Then** imprime JSON estructurado con predicción, confianza y latencia.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
