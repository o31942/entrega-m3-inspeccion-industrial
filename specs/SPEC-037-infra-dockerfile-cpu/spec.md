# SPEC-037 — US-37: Contenedor Docker CPU reproducible con uv, librerías C++ y healthcheck

- **Etiqueta Kanban:** `infra`
- **Story Points (Fibonacci 1:1):** `3 SP`
- **Milestone:** `M3`

## Problema y Contexto
El servicio backend debe ejecutarse de forma idéntica en cualquier máquina mediante un contenedor Docker CPU reproducible basado en Python 3.13 + `uv`.

## Requisitos Funcionales y No Funcionales
- Escribir `Dockerfile` CPU con usuario no privilegiado, librerías C++ mínimas (`libglib2.0-0`, `libgl1` o equivalentes Debian slim para OpenCV headless), `uv sync --frozen --no-dev` y descarga o montaje limpio del servicio gRPC+Gateway.
- Incluir `.dockerignore` y comando `HEALTHCHECK`.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** `docker build -t defect-inspector-grpc:m3 .`, **When** se construye y arranca el contenedor, **Then** compila sin errores y expone puertos `50051` y `8000` saludables.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
