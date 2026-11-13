# Plan Técnico — SPEC-010

## Diseño y Decisiones
Orquestador puro en `services/inspection_service.py` recibiendo dependencias de inferencia por constructor para testabilidad determinista.

## Archivos Afectados
- `src/defect_inspector/services/inspection_service.py`, `tests/test_inspection_service.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
