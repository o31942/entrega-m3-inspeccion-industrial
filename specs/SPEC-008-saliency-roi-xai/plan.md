# Plan Técnico — SPEC-008

## Diseño y Decisiones
Módulo `inference/explainability.py` desacoplado de red y HTTP que retorna dataclasses `SaliencyResult(heatmap, roi_bbox, overlay_png_base64)`.

## Archivos Afectados
- `src/defect_inspector/inference/explainability.py`, `tests/test_explainability.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
