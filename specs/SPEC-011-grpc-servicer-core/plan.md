# Plan Técnico — SPEC-011

## Diseño y Decisiones
Mapeadores puros DTO → mensaje Protobuf en `src/defect_inspector/api/grpc_servicer.py`.

## Archivos Afectados
- `src/defect_inspector/api/__init__.py`, `src/defect_inspector/api/grpc_servicer.py`, `tests/test_grpc_servicer.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
