# Plan Técnico — SPEC-002

## Decisiones de Diseño
- Versionar el contrato como `package inspection.v1;` en `protos/defect_inspection.proto`.
- Incluir metadatos explícitos de trazabilidad MaaS (`model_id`, `model_revision`, `license`, `hub_url`) tanto en `HealthResponse` como en `ModelInfoResponse` e `InspectResponse` para auditar consistencia frente a MLflow.
- Separar el directorio `src/defect_inspector/generated/` y excluirlo del linter Ruff manteniendo tipado limpio en la capa API.

## Riesgos y Mitigación
- Riesgo: imports relativos generados por `protoc` no resueltos dentro de `src/defect_inspector/generated/`. Mitigación: wrapper de importación o compilación con ruta controlada y pruebas unitarias sobre stubs generados.

## Estrategia de Pruebas
- Pruebas unitarias de serialización/deserialización Protobuf y validación de campos obligatorios.
