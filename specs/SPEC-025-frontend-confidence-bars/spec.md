# SPEC-025 — US-25: Visualización de puntaje de confianza, decisión HITL y top-6 barras

- **Etiqueta Kanban:** `frontend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
El veredicto debe mostrar claramente la clase predicha, el puntaje de confianza, la alerta HITL (`CONFORMING` / `DEFECT_DETECTED` / `LOW_CONFIDENCE_REVIEW`), latencia `ms` y la distribución completa de las 6 clases.

## Requisitos Funcionales y No Funcionales
- Construir tarjetas de veredicto HITL y barras horizontales porcentuales animadas para las 6 clases NEU-DET.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** un JSON de respuesta con 6 puntajes, **When** se renderiza `success`, **Then** ordena barras descendentes, resalta la top-1 y muestra el badge de decisión HITL.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
