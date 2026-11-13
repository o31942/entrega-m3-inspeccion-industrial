# Plan Técnico — SPEC-025

## Diseño y Decisiones
Renderizado DOM seguro (`textContent` sin inyección HTML insegura) en `frontend/js/render.js`.

## Archivos Afectados
- `frontend/js/render.js`, `frontend/styles.css`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
