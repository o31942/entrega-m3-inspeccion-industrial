# Plan Técnico — SPEC-036

## Diseño y Decisiones
Matrices parametrizadas de casos borde (dimensiones impares, escala de grises/RGBA, umbrales límite, Protobuf roundtrip, CORS y MLOps).

## Archivos Afectados
- `tests/test_edge_cases_matrix.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
