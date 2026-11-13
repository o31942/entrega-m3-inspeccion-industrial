# SPEC-038 — US-38: Pipeline de CI reproducible (ruff check + format + pytest) y verificación pre-push

- **Etiqueta Kanban:** `infra`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
Todo cambio integrado a `develop` o `main` requiere validación automática reproducible de estilo (`ruff`), formato y pruebas (`pytest`) vía CI.

## Requisitos Funcionales y No Funcionales
- Definir workflow de integración continua estándar (`.github/workflows/ci.yml` o configuración reproducible + `scripts/verify_ci.py` ejecutado localmente en pre-push).
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** el manifiesto CI y script local de verificación, **When** se ejecuta verificación completa, **Then** valida `uv sync --frozen`, `ruff check`, `ruff format --check` y `pytest -q`.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
