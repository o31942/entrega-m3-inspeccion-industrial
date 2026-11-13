# Plan Técnico — SPEC-032

## Diseño y Decisiones
Script CLI reproducible conectado a `MLFLOW_TRACKING_URI=http://127.0.0.1:5050` usando los módulos reales de `inference/` + `mlops/`.

## Archivos Afectados
- `scripts/evaluar.py`, `tests/test_evaluar_script.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
