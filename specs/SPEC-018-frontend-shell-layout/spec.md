# SPEC-018 — US-18: Estructura HTML5 semántica y sistema de diseño industrial CSS

- **Etiqueta Kanban:** `frontend`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
Anuncio 007 exige un cliente frontend desacoplado moderno (cero Streamlit/Gradio/Dash) orientado a operadores de control de calidad en planta siderúrgica.

## Requisitos Funcionales y No Funcionales
- Construir `frontend/index.html` semántico y `frontend/styles.css` con estética industrial de alto contraste, tarjetas de métricas, zona de carga, controles y panel visual.
- **RNF:** Cumplir estrictamente estándares Python 3.13, `uv`, `ruff` sin advertencias y separación de 3 capas.

## Criterios de Aceptación (Given-When-Then)
1. **Given** la carga de `http://127.0.0.1:5173`, **When** se abre en navegador de escritorio o móvil, **Then** renderiza estructura limpia sin librerías Python ni bloqueos.

## Métricas de Éxito
- Pruebas unitarias/integración AAA aprobadas en `pytest`.
- Cero errores de estilo o tipado en `ruff check .`.
