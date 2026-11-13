# SPEC-016 — US-16: CORS desacoplado, validación MIME/tamaño y status 400/415/422

- **Etiqueta Kanban:** `backend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
El cliente web desacoplado corre en otro origen (`http://127.0.0.1:5173`) y requiere CORS habilitado, validación temprana de archivos vacíos/MIME y traducción fiel de `RpcError` a códigos HTTP `400`/`415`/`422`/`500`/`503`.

## Requisitos Funcionales y No Funcionales
- Configurar `CORSMiddleware` para `localhost:5173` / `127.0.0.1:5173`.
- Traducir `grpc.StatusCode` → `HTTPStatus` exacto (`INVALID_ARGUMENT -> 400`, `UNAVAILABLE -> 503`, `INTERNAL -> 500`, validación FastAPI -> `422`).
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** subida de archivo `.txt` o mayor a 10 MB, **When** alcanza `POST /api/v1/inspect`, **Then** responde HTTP `400` o `415` con detalle estructurado.
2. **Given** solicitud `OPTIONS` desde `:5173`, **When** responde el gateway, **Then** incluye cabeceras CORS permitidas.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
