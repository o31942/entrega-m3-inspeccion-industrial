# Plan Técnico — SPEC-013

## Diseño y Decisiones
Tabla explícita `ERROR_TO_GRPC_STATUS` + helper `handle_grpc_errors` en `src/defect_inspector/api/error_mapping.py`.

## Archivos Afectados
- `src/defect_inspector/api/error_mapping.py`, `tests/test_grpc_error_mapping.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
