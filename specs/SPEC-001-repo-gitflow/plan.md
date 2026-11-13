# Plan Técnico — SPEC-001

## Decisiones de Diseño y Contratos
- Se adopta estructura `src/defect_inspector/` declarada en `[tool.hatch.build.targets.wheel]` de `pyproject.toml`.
- Se agrega `[tool.uv] constraint-dependencies = ["anyio>=4.0,<4.11"]` para prevenir incompatibilidades HTTP 500 en MLflow UI sobre ASGI (lección Clase 9).
- Se configura Ruff para Python 3.13 (`E`, `F`, `I`, `B`, `UP`) y Pytest sobre `tests/`.
- Se crea `Makefile` con comandos unificados (`sync`, `proto`, `backend`, `frontend`, `mlflow`, `eval`, `test`, `lint`, `docker-build`).

## Alternativas Descartadas
- Usar `requirements.txt` + `pip`: descartado por incumplir la regla obligatoria de reproducibilidad con `uv` y Python 3.13.
- Mezclar UI Streamlit en `pyproject.toml`: descartado por prohibición explícita de Streamlit en Anuncio 007.

## Riesgos y Mitigación
- Riesgo: inclusión accidental de pesos `.onnx` descargados localmente en `git add`. Mitigación: exclusión explícita de extensiones binarias y carpeta `models/` en `.gitignore`.

## Estrategia de Pruebas
- Verificación de carga del paquete `defect_inspector.__version__` y ejecución de `uv run ruff check .` y `uv run pytest -q`.
