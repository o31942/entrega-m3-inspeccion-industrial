# SPEC-003 — US-03: Generación de stubs gRPC Protobuf e import wrapper

- **Etiqueta Kanban:** `backend`
- **Story Points (Fibonacci 1:1):** `1 SP`
- **Milestone:** `M3`

## Problema y Contexto
El contrato `protos/defect_inspection.proto` necesita stubs Python tipados compilados con `grpc_tools.protoc` y un módulo wrapper para importación limpia dentro de `src/defect_inspector/`.

## Requisitos Funcionales y No Funcionales
- Compilar `defect_inspection_pb2.py` y `defect_inspection_pb2_grpc.py`.
- Corregir imports en `generated/` para resolver dentro del paquete `defect_inspector`.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** `protos/defect_inspection.proto`, **When** se ejecuta `make proto`, **Then** los stubs compilados se importan sin `ModuleNotFoundError`.
2. **Given** un `InspectRequest`, **When** se serializa/deserializa, **Then** conserva bytes, float y flags booleanos intactos.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
