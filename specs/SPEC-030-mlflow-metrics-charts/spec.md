# SPEC-030 — US-30: Cálculo de métricas multiclase, latencia p95, throughput y matriz de confusión

- **Etiqueta Kanban:** `mlflow`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
MLflow exige tanto métricas de calidad del modelo (Accuracy, Precision, Recall, F1, ROC-AUC OvR) como métricas operativas de servicio (latencia media, p95, throughput img/s) y matriz de confusión como artefacto PNG.

## Requisitos Funcionales y No Funcionales
- Implementar calculador de métricas multiclase + percentiles de latencia + renderizador Matplotlib de matriz de confusión sin GUI (`Agg`).
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** vectores `y_true`, `y_prob` y lista `latencies_ms`, **When** se calcula el reporte, **Then** retorna todas las métricas finitas y genera archivo PNG válido de matriz de confusión.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
