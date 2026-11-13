# SPEC-008 — US-08: Postprocesamiento con mapa térmico de saliencia XAI y ROI

- **Etiqueta Kanban:** `inference`
- **Story Points (Fibonacci 1:1):** `3 SP`
- **Milestone:** `M3`

## Problema y Contexto
Los operarios necesitan inspección visual explicable (XAI) junto al veredicto: mapa de calor de saliencia espacial, región de interés (ROI bbox) y superposición PNG codificada en Base64.

## Requisitos Funcionales y No Funcionales
- Implementar `compute_saliency_and_roi(gray_img, heatmap_size=224)` usando energía de gradientes Sobel + suavizado Gaussiano normalizado `[0, 1]`.
- Generar `overlay_png_base64` con colormap `JET` y bounding box ROI sobre la región de máxima respuesta.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** una imagen sintética con defecto lineal marcado, **When** se calcula saliencia y ROI, **Then** la caja `(x1, y1, x2, y2)` encierra la zona de mayor gradiente dentro de `[0, 224]`.
2. **Given** la imagen overlay generada, **When** se decodifica Base64, **Then** produce un PNG RGB válido sin fuga de memoria.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
