# Plan Técnico — SPEC-030

## Diseño y Decisiones
Uso de `scikit-learn` (`accuracy_score`, `precision_recall_fscore_support`, `roc_auc_score`, `confusion_matrix`) y `matplotlib` backend `Agg`.

## Archivos Afectados
- `src/defect_inspector/mlops/metrics.py`, `tests/test_mlops_metrics.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
