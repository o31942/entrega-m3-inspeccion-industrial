# Plan Técnico — SPEC-028

## Diseño y Decisiones
Módulo `mlops/tracking.py` desacoplado del backend runtime gRPC.

## Archivos Afectados
- `src/defect_inspector/mlops/__init__.py`, `src/defect_inspector/mlops/tracking.py`, `tests/test_mlflow_config.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
