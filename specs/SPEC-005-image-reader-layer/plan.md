# Plan Técnico — SPEC-005

## Diseño y Decisiones
Capa 1 pura usando `numpy` y `cv2.imdecode` con verificación de tamaño mínimo (`>= 16x16`), máximo de payload (`10 MB`) y whitelist MIME.

## Archivos Afectados
- `src/defect_inspector/inference/reader.py`, `tests/test_reader.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
