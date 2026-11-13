# Plan Técnico — SPEC-009

## Diseño y Decisiones
Dataclasses con `slots=True` / `frozen=True` en `services/dtos.py` y jerarquía `DefectInspectorError` en `services/exceptions.py`.

## Archivos Afectados
- `src/defect_inspector/services/__init__.py`, `src/defect_inspector/services/dtos.py`, `src/defect_inspector/services/exceptions.py`, `tests/test_service_dtos.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
