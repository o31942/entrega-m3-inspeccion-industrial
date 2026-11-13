# SPEC-027 — US-27: Accesibilidad ARIA, diseño responsive y estados vacíos/reintento

- **Etiqueta Kanban:** `frontend`
- **Story Points (Fibonacci 1:1):** `1 SP`
- **Milestone:** `M3`

## Problema y Contexto
Garantizar accesibilidad mínima (atributos `aria-live`, roles, labels, contraste, navegación teclado) y estados claros de carga, vacío y error con botón de reintento.

## Requisitos Funcionales y No Funcionales
- Auditar atributos ARIA, foco por teclado, spinners accesibles y mensaje accionable en `error`.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** desconexión simulada del gateway, **When** se intenta inspeccionar, **Then** `aria-live='assertive'` anuncia el error y ofrece reintento en un clic.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
