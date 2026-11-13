# Plan Técnico — SPEC-004

## Diseño y Decisiones
Separar constantes y `dataclass(frozen=True)` `ModelSpecConfig` con mapeo bilingüe EN→ES de las 6 clases NEU y soporte de variables de entorno.

## Archivos Afectados
- `src/defect_inspector/inference/__init__.py`, `src/defect_inspector/inference/config.py`, `tests/test_inference_config.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
