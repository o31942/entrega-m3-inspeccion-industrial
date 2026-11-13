## Trazabilidad Kanban & SDD
- **Historia / Issue vinculada:** Closes #
- **Especificación SDD:** `specs/SPEC-NNN-nombre/` (`spec.md`, `plan.md`, `tasks.md`)
- **Capa / Etiqueta:** `[ ] backend` `[ ] frontend` `[ ] inference` `[ ] mlflow` `[ ] qa` `[ ] infra` `[ ] docs` `[ ] kanban`
- **Story Points (Fibonacci 1:1):** `_ SP`

## Qué cambia y por qué
- Descripción concisa del cambio implementado conforme a `plan.md`.

## Cómo se probó
- [ ] `uv run ruff check .` sin errores.
- [ ] `uv run ruff format --check .` sin cambios pendientes.
- [ ] `uv run pytest -q` ejecutado en verde (pruebas sintéticas AAA).

## Riesgos y checklist de calidad
- [ ] Arquitectura en 3 capas respetada (`inference/` sin gRPC/HTTP; `services/` sin gRPC/HTTP).
- [ ] Sin pesos binarios (`.onnx`, `.pt`, `.h5`, `.joblib`), secretos (`.env`), notebooks (`.ipynb`) ni datasets crudos.
- [ ] Sin Streamlit/Gradio/Dash; cliente desacoplado consumiendo API/gRPC.
