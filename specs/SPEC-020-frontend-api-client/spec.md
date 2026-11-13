# SPEC-020 — US-20: Cliente HTTP/JSON ESM con timeout, manejo de errores y AbortController

- **Etiqueta Kanban:** `frontend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
El frontend debe comunicarse con el backend por red visible en Chrome DevTools (`Network`), con timeouts controlados y manejo claro de errores HTTP `4xx`/`5xx` o caída de servicio.

## Requisitos Funcionales y No Funcionales
- Crear `frontend/js/api.js` encapsulando `fetch` con `AbortController` (timeout 15s), `checkHealth()`, `fetchModelInfo()` e `inspectImage()`.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** URL del gateway configurable (`http://127.0.0.1:8000`), **When** se ejecuta `inspectImage`, **Then** aparece petición `POST /api/v1/inspect` en DevTools Network retornando JSON o error descriptivo.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
