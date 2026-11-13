# SPEC-026 — US-26: Indicador vivo /health del backend gRPC e historial de inspecciones

- **Etiqueta Kanban:** `frontend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
El operador debe saber en todo momento si el backend gRPC + modelo ONNX está disponible y revisar un historial local reciente de inspecciones de la sesión.

## Requisitos Funcionales y No Funcionales
- Consultar `/health` y `/api/v1/model` al iniciar y con botón de refresco.
- Mantener bitácora de las últimas 8 inspecciones en memoria de sesión UI.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** backend gRPC operativo, **When** abre la página, **Then** el indicador superior muestra `Online · ONNX ResNet-18` y versión del modelo.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
