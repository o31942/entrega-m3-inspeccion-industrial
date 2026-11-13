# Plan Técnico — SPEC-006

## Diseño y Decisiones
Conversiones controladas gris→CLAHE→RGB→Resize Bilineal→Rescale `[0,1]`→Normalize `(x-mean)/std`→NCHW `(1,3,224,224)`.

## Archivos Afectados
- `src/defect_inspector/inference/preprocessor.py`, `tests/test_preprocessor.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
