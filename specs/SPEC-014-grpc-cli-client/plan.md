# Plan Técnico — SPEC-014

## Diseño y Decisiones
Stub cliente sobre `grpc.insecure_channel` en `src/defect_inspector/api/grpc_client.py` con formato legible y código de salida no-cero en error.

## Archivos Afectados
- `src/defect_inspector/api/grpc_client.py`, `tests/test_grpc_client.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
