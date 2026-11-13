# SPEC-019 — US-19: Máquina de estados cliente desacoplado (idle/loading/success/error)

- **Etiqueta Kanban:** `frontend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
Un cliente desacoplado real debe modelar explícitamente sus estados UI (`idle`, `loading`, `success`, `error`) para retroalimentación inmediata y prevención de dobles envíos.

## Requisitos Funcionales y No Funcionales
- Crear `frontend/js/state.js` con máquina de estados pura, transiciones válidas y listeners reactivos.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** estado `idle`, **When** inicia inferencia, **Then** transiciona a `loading` bloqueando botón de envío; al responder pasa a `success` o `error` con botón de reintento.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
