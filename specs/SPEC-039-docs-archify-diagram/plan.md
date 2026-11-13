# Plan Técnico — SPEC-039

## Diseño y Decisiones
HTML autocontenido SVG interactivo validado con prueba automatizada de existencia de etiquetas clave.

## Archivos Afectados
- `docs/arquitectura.html`, `tests/test_docs_consistency.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
