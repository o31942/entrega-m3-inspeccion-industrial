# Plan Técnico — SPEC-038

## Diseño y Decisiones
Definición clara de pasos CI en `.github/workflows/ci.yml` y ejecutor local `scripts/verify_ci.py` para auditoría inmediata.

## Archivos Afectados
- `.github/workflows/ci.yml`, `scripts/verify_ci.py`, `tests/test_ci_workflow.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
