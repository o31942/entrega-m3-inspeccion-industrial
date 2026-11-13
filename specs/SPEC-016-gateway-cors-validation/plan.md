# Plan Técnico — SPEC-016

## Diseño y Decisiones
Mapa determinista `GRPC_TO_HTTP_STATUS` y validación previa de upload multipart en `gateway.py`.

## Archivos Afectados
- `src/defect_inspector/api/gateway.py`, `tests/test_gateway_errors_cors.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
