# Plan Técnico — SPEC-035

## Diseño y Decisiones
Fixtures de servidor gRPC efímero limpio con cierre en `teardown`.

## Archivos Afectados
- `tests/test_grpc_integration.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
