# Plan Técnico — SPEC-007

## Diseño y Decisiones
Inyección de dependencia opcional de `session` para unit tests sintéticos sin disco y carga singleton perezosa/startup en producción con `CPUExecutionProvider`.

## Archivos Afectados
- `src/defect_inspector/inference/model_loader.py`, `tests/test_model_loader.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
