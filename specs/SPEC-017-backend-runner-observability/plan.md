# Plan Técnico — SPEC-017

## Diseño y Decisiones
Orquestador Python en `run_backend.py` con módulo `defect_inspector.logging_config` y captura de señales.

## Archivos Afectados
- `src/defect_inspector/logging_config.py`, `src/defect_inspector/api/run_backend.py`, `tests/test_logging_runner.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
