# Plan Técnico — SPEC-023

## Diseño y Decisiones
Controles vinculados reactivamente al estado de formulario y panel explicativo de política HITL.

## Archivos Afectados
- `frontend/index.html`, `frontend/js/app.js`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
