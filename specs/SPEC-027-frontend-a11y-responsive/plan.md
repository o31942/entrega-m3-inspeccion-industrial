# Plan Técnico — SPEC-027

## Diseño y Decisiones
Refinamiento semántico WCAG básico en `frontend/index.html` y `styles.css` + tests de estructura.

## Archivos Afectados
- `frontend/index.html`, `frontend/styles.css`, `tests/test_frontend_assets.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
