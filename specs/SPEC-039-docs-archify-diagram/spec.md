# SPEC-039 — US-39: Diagrama interactivo Archify en docs/arquitectura.html (4 vistas)

- **Etiqueta Kanban:** `docs`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
La sustentación revisa un diagrama de arquitectura estilo Archify en `docs/arquitectura.html` enlazado desde el README reflejando fielmente los puertos y componentes finales.

## Requisitos Funcionales y No Funcionales
- Actualizar y verificar `docs/arquitectura.html` con las 4 vistas interactivas (Architecture, Data Flow, Sequence, Lifecycle) alineadas al 100% con los módulos reales del repositorio.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** apertura de `docs/arquitectura.html` en navegador, **When** se navegan las pestañas, **Then** los puertos (`5173`, `8000`, `50051`, `5050`), clases y archivos coinciden exactamente con el código.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
