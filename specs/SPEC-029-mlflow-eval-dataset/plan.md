# Plan Técnico — SPEC-029

## Diseño y Decisiones
Soporte dual: descarga muestras reales NEU de HF Hub si hay red (`newguyme/neu_det_caption` / cache) con respaldo determinista auditado etiquetado con el origen del dataset en los tags MLflow.

## Archivos Afectados
- `src/defect_inspector/mlops/eval_data.py`, `tests/test_eval_data.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
