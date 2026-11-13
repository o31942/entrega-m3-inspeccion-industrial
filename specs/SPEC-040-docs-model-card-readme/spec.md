# SPEC-040 — US-40: Model Card formal verificada, ADR-001 gRPC y README completo con badges

- **Etiqueta Kanban:** `docs`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
El bloque 6 (10%) exige Model Card formal en `docs/model-card.md`, documentación de decisiones arquitectónicas (ADR-001) y README completo con badges, guía de ejecución y enlaces verificados.

## Requisitos Funcionales y No Funcionales
- Crear `docs/adr-001-grpc-gateway.md` justificando gRPC + Gateway HTTP + Frontend HTML/ESM.
- Actualizar `docs/model-card.md` y `README.md` con métricas medidas en MLflow, comandos reales y enlace a ADR/specs/Kanban.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** revisión de `README.md`, `docs/model-card.md` y `docs/adr-001-grpc-gateway.md`, **When** se auditan rutas y hashes, **Then** coinciden exactamente con `senanurcetin/neu-steel-defect-resnet18@ad13c70618a8a28a50309456dd40d9a45b2869d1` y archivos del repo.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
