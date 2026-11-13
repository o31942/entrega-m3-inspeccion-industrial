# SPEC-022 — US-22: Generador sintético local en Canvas para pruebas rápidas sin dataset

- **Etiqueta Kanban:** `frontend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
Durante demostraciones en vivo sin carpeta de pruebas externa a la mano, el usuario necesita generar muestras sintéticas realistas de lámina de acero (rayadura, picadura, parches) en un clic.

## Requisitos Funcionales y No Funcionales
- Implementar `frontend/js/samples.js` usando HTML5 `<canvas>` para generar texturas metálicas reales como `Blob`/`File` listas para enviarse por red al backend.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** clic en uno de los presets de muestra (`Rayadura`, `Parches`, `Picaduras`), **When** se genera en Canvas, **Then** carga como archivo real y dispara inferencia en tiempo real contra gRPC.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
