# SPEC-011 — US-11: Implementación del Servicer gRPC DefectInspectionService

- **Etiqueta Kanban:** `backend`
- **Story Points (Fibonacci 1:1):** `3 SP`
- **Milestone:** `M3`

## Problema y Contexto
La Capa 3 debe exponer `DefectInspectionServiceServicer` implementando los RPCs del `.proto` traduciendo únicamente DTOs ↔ Protobuf.

## Requisitos Funcionales y No Funcionales
- Implementar `DefectInspectionServicer` delegando en `DefectInspectionService`.
- Convertir `InspectionResponseDTO` en `defect_inspection_pb2.InspectResponse`.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** una instancia `DefectInspectionServicer`, **When** recibe `InspectRequest`, **Then** retorna `InspectResponse` completo sin contener lógica de OpenCV u ONNX en el archivo.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
