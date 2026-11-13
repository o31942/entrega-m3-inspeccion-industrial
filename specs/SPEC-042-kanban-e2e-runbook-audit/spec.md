# SPEC-042 — US-42: Auditoría final pre-sustentación (3 minutos) y guion operativo de 15 min

- **Etiqueta Kanban:** `kanban`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
Antes de la sustentación del sábado 14/11 (11:30–11:45 a.m.), se debe ejecutar la prueba de 3 minutos y contar con un runbook paso a paso para los 12 minutos de demo en vivo.

## Requisitos Funcionales y No Funcionales
- Crear `docs/runbook-sustentacion.md` con el guion cronometrado (0:00–15:00) y script `scripts/audit_m3.py` verificando en vivo: specs >= 40, PRs, pytest >= 120, ruff limpio y endpoints.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** `uv run python scripts/audit_m3.py`, **When** se ejecuta sobre el repositorio completo, **Then** valida todos los pisos cuantitativos de Anuncio 007 en verde.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
