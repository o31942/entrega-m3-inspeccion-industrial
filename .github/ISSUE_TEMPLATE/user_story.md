---
name: Historia de Usuario M3 (SDD + Kanban)
about: Plantilla oficial de historia en GitHub Projects (#4) vinculada a spec SDD
title: "US-XX: <Título conciso del incremento>"
labels: backend
---

## Historia de Usuario
**Como** <rol de usuario / ingeniero>
**Quiero** <capacidad medible>
**Para** <beneficio verificable en el proyecto M3>

## Especificación SDD Asociada
- Ruta SDD: `specs/SPEC-XXX-<slug>/` (`spec.md`, `plan.md`, `tasks.md`)
- Story Points (Fibonacci 1:1): `2 SP`

## Criterios de Aceptación (Given / When / Then)
1. **Given** <precondición>, **When** <acción>, **Then** <resultado esperado>.
2. **Given** <escenario de error>, **When** <entrada inválida>, **Then** <respuesta controlada>.

## Checklist Definition of Done
- [ ] `spec.md`, `plan.md` y `tasks.md` versionados ANTES del código.
- [ ] `uv run ruff check .` y `uv run pytest -q` verdes sin advertencias.
- [ ] PR abierta hacia `develop` con `Closes #N` y revisión aprobada.
