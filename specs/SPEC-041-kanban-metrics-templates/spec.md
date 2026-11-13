# SPEC-041 — US-41: Plantillas de Issue SDD, script de verificación y reporte métricas Kanban

- **Etiqueta Kanban:** `kanban`
- **Story Points (Fibonacci 1:1):** `1 SP`
- **Milestone:** `M3`

## Problema y Contexto
El tablero Kanban requiere plantilla estructurada de Historias de Usuario, guía clara de las 4 métricas ágiles (WIP, Throughput, Work Item Age, Cycle Time) y reporte verificable.

## Requisitos Funcionales y No Funcionales
- Agregar `.github/ISSUE_TEMPLATE/user_story.md` con formato Como/Quiero/Para, AC Given-When-Then y Fibonacci 1:1.
- Crear `docs/kanban-metricas.md` explicando cálculo y lectura de las 4 métricas sobre Project #4.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** `.github/ISSUE_TEMPLATE/user_story.md` y `docs/kanban-metricas.md`, **When** el revisor consulta la trazabilidad Kanban, **Then** encuentra fórmulas e interpretación directa para la defensa.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
