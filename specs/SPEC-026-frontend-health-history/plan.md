# Plan Técnico — SPEC-026

## Diseño y Decisiones
Barra de telemetría viva y tabla de historial en `frontend/js/app.js` + `render.js`.

## Archivos Afectados
- `frontend/index.html`, `frontend/js/app.js`, `frontend/js/render.js`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
