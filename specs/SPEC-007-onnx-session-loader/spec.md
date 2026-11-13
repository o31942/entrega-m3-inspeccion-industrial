# SPEC-007 — US-07: Cargador único ONNX Runtime CPU y softmax multiclase

- **Etiqueta Kanban:** `inference`
- **Story Points (Fibonacci 1:1):** `3 SP`
- **Milestone:** `M3`

## Problema y Contexto
Cargar `onnxruntime.InferenceSession` por petición añadiría cientos de milisegundos; debe cargarse UNA SOLA VEZ al arrancar y exponer softmax multiclase estable.

## Requisitos Funcionales y No Funcionales
- Implementar `OnnxDefectClassifier` con `InferenceSession(..., providers=['CPUExecutionProvider'])` inyectable o cargado una sola vez.
- Implementar `stable_softmax(logits)` y obtención de top-k predicciones ordenadas.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** una sesión ONNX precargada o inyectada en tests, **When** se llama `predict_logits(tensor)`, **Then** retorna probabilidades que suman `1.0 ± 1e-5`.
2. **Given** un archivo `.onnx` inexistente, **When** se instancia `OnnxDefectClassifier`, **Then** falla rápido con error explícito.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
