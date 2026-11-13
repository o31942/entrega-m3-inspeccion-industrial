# Plan Técnico — SPEC-019

## Diseño y Decisiones
Patrón observable ligero en ES Modules sin dependencias externas.

## Archivos Afectados
- `frontend/js/state.js`, `tests/test_frontend_js_structure.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
