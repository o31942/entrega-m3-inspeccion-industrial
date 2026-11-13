# Plan Técnico — SPEC-031

## Diseño y Decisiones
Clase `NEUDefectPyFunc` limpia en `src/defect_inspector/mlops/packaging.py` encapsulando preprocesamiento + ONNX Runtime.

## Archivos Afectados
- `src/defect_inspector/mlops/packaging.py`, `tests/test_mlops_packaging.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
