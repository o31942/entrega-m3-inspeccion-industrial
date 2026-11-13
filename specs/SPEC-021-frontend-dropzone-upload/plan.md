# Plan Técnico — SPEC-021

## Diseño y Decisiones
Event listeners `dragover`, `drop`, `change` + `URL.createObjectURL` con liberación automática.

## Archivos Afectados
- `frontend/js/app.js`, `frontend/styles.css`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
