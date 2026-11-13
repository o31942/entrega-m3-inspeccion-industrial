# SPEC-023 — US-23: Controles reactivos de umbral HITL y toggle CLAHE

- **Etiqueta Kanban:** `frontend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
El umbral de confianza HITL y la activación de CLAHE son parámetros operativos clave que deben ajustarse dinámicamente desde la UI y viajar en cada RPC.

## Requisitos Funcionales y No Funcionales
- Integrar slider `conf_threshold` (`0.10–0.95`) y checkbox `apply_clahe` sincronizados en UI y enviados en `FormData` → `InspectRequest`.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** ajuste del umbral a `0.85` y CLAHE activo, **When** se inspecciona una imagen, **Then** el payload `POST /api/v1/inspect` y respuesta JSON reflejan exactamente `conf_threshold=0.85` y `applied_clahe=true`.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
