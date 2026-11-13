# SPEC-024 — US-24: Visor dual original vs overlay térmico XAI y caja ROI

- **Etiqueta Kanban:** `frontend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
El operador necesita comparar lado a lado la captura original de bobina y el overlay térmico XAI (`overlay_png_base64`) retornado por el servicio gRPC.

## Requisitos Funcionales y No Funcionales
- Renderizar panel dual Original vs Saliencia XAI + coordenadas ROI `(x1, y1, x2, y2)` en `frontend/js/render.js`.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** respuesta exitosa con `overlay_png_base64`, **When** se renderiza `success`, **Then** el mapa de calor aparece nítido junto a las coordenadas ROI.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
