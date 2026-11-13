# Plan Técnico — SPEC-034

## Diseño y Decisiones
Mock ligero de `SurfaceModelRunner` inyectado por constructor respetando estricto patrón AAA.

## Archivos Afectados
- `tests/test_service_exhaustive.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
