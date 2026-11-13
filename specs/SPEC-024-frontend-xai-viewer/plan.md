# Plan Técnico — SPEC-024

## Diseño y Decisiones
Componente renderizador modular en `frontend/js/render.js` desacoplado de red.

## Archivos Afectados
- `frontend/js/render.js`, `frontend/styles.css`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
