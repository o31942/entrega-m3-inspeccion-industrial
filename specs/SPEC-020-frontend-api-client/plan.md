# Plan Técnico — SPEC-020

## Diseño y Decisiones
Cliente `fetch` tipado vía JSDoc en ES Modules con parseo seguro de respuestas JSON de error.

## Archivos Afectados
- `frontend/js/api.js`, `frontend/js/app.js`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
