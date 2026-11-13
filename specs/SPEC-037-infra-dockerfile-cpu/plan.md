# Plan Técnico — SPEC-037

## Diseño y Decisiones
Imagen multi-etapa / slim `python:3.13-slim` copiando binario oficial `uv`, sincronizando `.venv` con `--frozen` sin capas innecesarias.

## Archivos Afectados
- `Dockerfile`, `.dockerignore`, `tests/test_docker_contract.py`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
