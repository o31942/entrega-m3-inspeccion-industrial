# Plan Técnico — SPEC-003

## Diseño y Decisiones
Ejecutar `grpc_tools.protoc` apuntando a `src/defect_inspector/generated/` y ajustar el import relativo del stub gRPC mediante helper limpio.

## Archivos Afectados
- `src/defect_inspector/generated/defect_inspection_pb2.py`, `src/defect_inspector/generated/defect_inspection_pb2_grpc.py`, `tests/test_proto_stubs.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
