# SPEC-006 — US-06: Preprocesamiento CLAHE y normalización tensor ImageNet 224x224

- **Etiqueta Kanban:** `inference`
- **Story Points (Fibonacci 1:1):** `3 SP`
- **Milestone:** `M3`

## Problema y Contexto
El modelo `neu_resnet18.onnx` espera tensor `float32` de forma `(1, 3, 224, 224)` normalizado con ImageNet mean/std y soporta ecualización CLAHE industrial previa.

## Requisitos Funcionales y No Funcionales
- Implementar `preprocess_image(img, apply_clahe, target_size=224)` con CLAHE configurable (`clipLimit=2.0`, `tileGridSize=(8,8)`).
- Validar contrato estricto con `validate_tensor_contract(tensor)` (`dtype=float32`, finitud, shape `(1, 3, 224, 224)`).
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** matriz `uint8` arbitraria (`200x200` o `512x512` RGB/Gray), **When** se preprocesa, **Then** retorna `np.ndarray` `float32` con shape `(1, 3, 224, 224)` sin NaN/Inf.
2. **Given** `apply_clahe=True` vs `False`, **When** se aplica sobre imagen de bajo contraste, **Then** CLAHE incrementa entropía/contraste local preservando contrato.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
