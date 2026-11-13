# Plan Técnico — SPEC-015

## Diseño y Decisiones
App FastAPI ligera con esquemas Pydantic en `src/defect_inspector/api/schemas.py` y canal gRPC administrado por `lifespan`.

## Archivos Afectados
- `src/defect_inspector/api/schemas.py`, `src/defect_inspector/api/gateway.py`, `tests/test_gateway_api.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
