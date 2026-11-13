# Plan Técnico — SPEC-022

## Diseño y Decisiones
Generador Canvas 2D determinista de texturas siderúrgicas convertido vía `canvas.toBlob(..., 'image/png')`.

## Archivos Afectados
- `frontend/js/samples.js`, `frontend/index.html`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
