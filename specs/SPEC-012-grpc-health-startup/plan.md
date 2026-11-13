# Plan Técnico — SPEC-012

## Diseño y Decisiones
Factory `build_runtime_service()` invocada una vez al inicializar `serve()` en `src/defect_inspector/api/grpc_server.py`.

## Archivos Afectados
- `src/defect_inspector/api/grpc_server.py`, `tests/test_grpc_server_startup.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
