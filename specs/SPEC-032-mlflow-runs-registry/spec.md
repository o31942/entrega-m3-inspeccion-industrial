# SPEC-032 — US-32: Ejecución de 3+ corridas comparables y registro en MLflow Model Registry

- **Etiqueta Kanban:** `mlflow`
- **Story Points (Fibonacci 1:1):** `3 SP`
- **Milestone:** `M3`

## Problema y Contexto
Anuncio 007 exige UI MLflow viva con >= 3 corridas comparables en el mismo experimento (sin hiperparámetros de entrenamiento) y Model Registry consistente con el modelo MaaS del backend.

## Requisitos Funcionales y No Funcionales
- Implementar `scripts/evaluar.py` ejecutando al menos 3 runs comparables:
  1) Baseline (`clahe=False`, `conf_threshold=0.50`)
  2) Umbral estricto HITL (`clahe=False`, `conf_threshold=0.70`)
  3) Preprocesamiento CLAHE (`clahe=True`, `conf_threshold=0.70`)
- Registrar modelo en MLflow Model Registry (`neu-steel-defect-resnet18`, alias `production` / `staging`).
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** servidor MLflow corriendo en `http://127.0.0.1:5050`, **When** se ejecuta `uv run python scripts/evaluar.py`, **Then** quedan registradas 3+ corridas comparables, tags, artefactos y modelo registrado en Model Registry.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
