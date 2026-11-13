# SPEC-013 — US-13: Mapeo explícito de errores de dominio a gRPC StatusCodes

- **Etiqueta Kanban:** `backend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
Las excepciones de dominio (`DomainValidationError`, `UnsupportedMediaError`, `ModelNotReadyError`) deben mapearse determinísticamente a `grpc.StatusCode` (`INVALID_ARGUMENT`, `FAILED_PRECONDITION`, `INTERNAL`).

## Requisitos Funcionales y No Funcionales
- Implementar traductor de errores e interceptor gRPC reutilizable sin ocultar mensajes útiles al cliente.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** imagen corrupta que dispara `InvalidImageError`, **When** se procesa vía RPC, **Then** el contexto gRPC aborta con `StatusCode.INVALID_ARGUMENT`.
2. **Given** fallo no esperado de sesión, **When** se procesa vía RPC, **Then** aborta con `StatusCode.INTERNAL`.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
