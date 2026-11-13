# SPEC-009 — US-09: Contratos DTO tipados y excepciones de dominio en capa de servicio

- **Etiqueta Kanban:** `backend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
La capa de servicio (`services/`) no debe acoplarse ni a Protobuf ni a Pydantic; necesita DTOs Python tipados y jerarquía de excepciones de dominio traducibles por la capa API.

## Requisitos Funcionales y No Funcionales
- Definir `ClassScoreDTO`, `BoundingBoxDTO`, `InspectionResponseDTO`, `HealthDTO`, `ModelInfoDTO`.
- Definir excepciones `DomainValidationError`, `ModelNotReadyError`, `InspectionProcessingError`.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** módulos dentro de `src/defect_inspector/services/`, **When** se auditan sus imports, **Then** no contienen ninguna referencia a `grpc` ni `fastapi`.
2. **Given** cualquier DTO instanciado, **When** se serializa a diccionario simple, **Then** conserva invariantes de tipo (`float`, `int`, `bool`, `str`).

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
