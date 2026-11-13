# SPEC-002 — Contrato Protobuf gRPC (`protos/defect_inspection.proto`)

- **Historia vinculada:** `#2`
- **Etiqueta:** `backend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
La arquitectura del Módulo 3 exige una frontera de servicio tipada e independiente de la implementación interna del modelo. Para el backend en gRPC (`:50051`), el contrato explícito debe residir en un archivo `.proto` compilable con `grpc_tools.protoc`.

## Requisitos Funcionales y No Funcionales
- **RF-001:** Definir el paquete `inspection.v1` y el servicio `DefectInspectionService` con los RPCs `CheckHealth`, `GetModelInfo` y `InspectSurface`.
- **RF-002:** Modelar mensajes tipados para request de imagen (`image_bytes`, `filename`, `content_type`, `conf_threshold`, `apply_clahe`, `request_id`) y respuesta estructurada (`predicted_class`, `predicted_label_es`, `confidence`, `requires_human_review`, `decision_status`, `latency_ms`, `scores`, `roi_bbox`, `overlay_png_base64`).
- **RNF-001:** El esquema Protobuf debe compilar sin advertencias en Python 3.13 mediante `grpc_tools.protoc`.

## Criterios de Aceptación (Given-When-Then)
1. **Given** el contrato `protos/defect_inspection.proto`, **When** se compila con `grpc_tools.protoc`, **Then** se generan los stubs `_pb2.py` y `_pb2_grpc.py` sin errores.
2. **Given** un mensaje `InspectResponse`, **When** se serializa y deserializa con Protobuf, **Then** conserva tipos numéricos, lista de puntajes de las 6 clases NEU y metadatos de trazabilidad del modelo.

## Fuera de Alcance
- Implementación del servidor gRPC, cliente CLI y puente HTTP para el navegador (especificados en PRs posteriores).

## Métricas de Éxito
- Compilación `make proto` exitosa y código fuente generado importable.
