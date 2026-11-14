# SPEC-042 — US-42: Auditoría final pre-sustentación (M3) y verificación cuantitativa

- **Etiqueta Kanban:** `kanban`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
Antes de la entrega del Módulo 3, se requiere una auditoría automatizada que valide los pisos cuantitativos de especificaciones SDD, pruebas `pytest`, linter `ruff` y archivos técnicos exigidos sin depender de notas privadas dentro del repositorio.

## Requisitos Funcionales y No Funcionales
- Implementar el script `scripts/audit_m3.py` para verificar de forma determinista: specs >= 40, colección `pytest` >= 120, `ruff` limpio y presencia de los entregables documentales requeridos.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** `uv run python scripts/audit_m3.py`, **When** se ejecuta sobre el repositorio completo, **Then** valida todos los pisos cuantitativos de Anuncio 007 en verde.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
