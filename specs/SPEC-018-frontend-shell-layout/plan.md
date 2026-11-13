# Plan Técnico — SPEC-018

## Diseño y Decisiones
HTML5 semántico (`header`, `main`, `section`, `aside`) + CSS Grid/Variables CSS con paleta oscura industrial accesible.

## Archivos Afectados
- `frontend/index.html`, `frontend/styles.css`, `tests/test_frontend_assets.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
