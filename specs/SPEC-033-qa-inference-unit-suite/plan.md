# Plan Técnico — SPEC-033

## Diseño y Decisiones
Fixtures sintéticos por cada una de las 6 clases de defecto y parametrización con `@pytest.mark.parametrize`.

## Archivos Afectados
- `tests/conftest.py`, `tests/test_inference_exhaustive.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
