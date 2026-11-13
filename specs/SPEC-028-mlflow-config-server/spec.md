# SPEC-028 — US-28: Configuración centralizada de MLflow Tracking URI (:5050) y SQLite store

- **Etiqueta Kanban:** `mlflow`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
El servidor MLflow y los scripts cliente deben usar SIEMPRE el mismo backend store (`sqlite:///mlflow.db`, `--workers 1`, `./mlruns`, puerto `5050`) para evitar split-brain en sustentación (lección Clase 9).

## Requisitos Funcionales y No Funcionales
- Crear `src/defect_inspector/mlops/tracking.py` con configuración centralizada (`DEFAULT_MLFLOW_URI='http://127.0.0.1:5050'`, `EXPERIMENT_NAME='neu-steel-defect-inspection'`).
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** variables de entorno por defecto, **When** se inicializa tracking MLflow, **Then** apunta a `http://127.0.0.1:5050` y verifica conectividad antes de loguear.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
