# SPEC-021 — US-21: Carga drag-and-drop y previsualización de imagen superficial

- **Etiqueta Kanban:** `frontend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
El inspector debe poder arrastrar o seleccionar imágenes locales (PNG/JPG/BMP) viendo miniatura, dimensiones, nombre y peso antes de enviar al servidor gRPC.

## Requisitos Funcionales y No Funcionales
- Implementar zona drag-and-drop y input file accesible en `frontend/js/app.js` con validación cliente de tipo y tamaño.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** un archivo `.png` válido arrastrado a la zona de carga, **When** se suelta, **Then** se muestra vista previa y se habilita el botón de inspección.
2. **Given** archivo no gráfico, **When** se selecciona, **Then** muestra estado `error` amigable sin invocar backend.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
