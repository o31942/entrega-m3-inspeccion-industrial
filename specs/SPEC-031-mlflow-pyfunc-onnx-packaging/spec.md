# SPEC-031 — US-31: Empaquetado mlflow.onnx / mlflow.pyfunc y artefactos de reporte

- **Etiqueta Kanban:** `mlflow`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
Cada corrida comparable en MLflow debe guardar artefactos empaquetados (`mlflow.pyfunc` / modelo ONNX con signature), JSON de predicciones de muestra y reporte Markdown de evaluación.

## Requisitos Funcionales y No Funcionales
- Implementar wrapper `NEUDefectPyFunc(mlflow.pyfunc.PythonModel)` + función `log_evaluation_artifacts(...)` con tags completos (licencia, `model_rev`, equipo, PR, commit SHA).
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** una evaluación completada, **When** se registran artefactos en MLflow, **Then** el run contiene modelo empaquetado (`mlflow.pyfunc`), `confusion_matrix.png`, `sample_predictions.json` y `evaluation_report.md`.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
