# SPEC-029 — US-29: Preparación de lote de evaluación reproducible NEU/sintético calibrado

- **Etiqueta Kanban:** `mlflow`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
La evaluación reproducible en MLflow requiere un lote fijo etiquetado de imágenes de acero (descargado de Hugging Face / generado reproduciblemente fuera de Git en `data/eval_cache/`) para comparar configuraciones sobre exactamente las mismas muestras.

## Requisitos Funcionales y No Funcionales
- Implementar generador/descargador de conjunto de validación reproducible de 60 imágenes (10 por clase) con semilla fija y manifiesto JSON en `src/defect_inspector/mlops/eval_data.py`.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** ejecución de `build_evaluation_batch()`, **When** carga muestras reales cacheadas o genera suite estructurada calibrada, **Then** produce pares `(imagen, y_true)` reproducibles entre corridas.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
