# SPEC-004 — US-04: Descarga verificada del modelo MaaS ONNX y revisión fija

- **Etiqueta Kanban:** `inference`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
Los pesos ONNX MaaS (`senanurcetin/neu-steel-defect-resnet18@ad13c70618a8a28a50309456dd40d9a45b2869d1`) no deben ir en Git, pero el sistema requiere configuración tipada y descarga reproducible verificada.

## Requisitos Funcionales y No Funcionales
- Centralizar configuración de modelo (`DEFAULT_MODEL_ID`, `DEFAULT_MODEL_REV`, clases y rutas) en `inference/config.py`.
- Verificar integridad de archivo `.onnx` y `labels.json` en descarga local.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** `inference/config.py`, **When** se consulta `ModelSpecConfig`, **Then** expone ID, revisión fija SHA, licencia MIT y 6 clases NEU.
2. **Given** ausencia de pesos locales, **When** falla validación de archivo, **Then** emite `FileNotFoundError` instructivo hacia `make download-model`.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
