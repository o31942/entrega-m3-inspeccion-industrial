# SPEC-005 — US-05: Módulo de ingesta y validación de buffers e imágenes

- **Etiqueta Kanban:** `inference`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
El servicio recibe imágenes desde buffer binario (gRPC bytes) o disco; debe rechazar formatos corruptos, tamaños extremos y MIME no soportados antes de preprocesar.

## Requisitos Funcionales y No Funcionales
- Implementar `read_industrial_image(source, content_type)` validando bytes no vacíos, cabecera imagen válida y decodificación vía OpenCV/Pillow.
- Definir excepciones explícitas `InvalidImageError` / `UnsupportedMediaError` en `inference/`.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** un buffer PNG/JPEG válido, **When** se llama `read_industrial_image`, **Then** retorna matriz `np.ndarray` `uint8` 2D/RGB válida.
2. **Given** bytes corruptos o MIME `application/pdf`, **When** se invoca ingesta, **Then** lanza error de validación sin importar `fastapi` o `grpc`.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
