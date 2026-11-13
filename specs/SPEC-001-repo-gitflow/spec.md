# SPEC-001 — Inicialización del Repositorio, uv (Python 3.13) y Gitflow

- **Historia vinculada:** `#1`
- **Etiqueta:** `infra`
- **Story Points (Fibonacci 1:1):** `2 SP`
- **Milestone:** `M3`

## Problema y Contexto
El proyecto del Módulo 3 requiere una estructura reproducible y auditada bajo `src/` layout con Python 3.13 y `uv`, licencia MIT, `.gitignore` estricto sin artefactos pesados ni secretos, y reglas claras de Gitflow (`main` / `develop` / `feature/*`) junto con plantilla oficial de Pull Requests.

## Requisitos Funcionales y No Funcionales
- **RF-001:** El repositorio debe fijar Python `3.13` en `.python-version` y declararlo en `pyproject.toml`.
- **RF-002:** Las dependencias deben resolverse con `uv` (`uv.lock`), prohibiendo `pip` y `requirements.txt`.
- **RNF-001:** `.gitignore` debe excluir pesos binarios (`.onnx`, `.pt`, `.h5`, `.joblib`), `.env`, `.venv/`, `data/raw/`, `mlruns/`, `mlflow.db` y `.ipynb`.
- **RNF-002:** Incluir `LICENSE` MIT y `.github/PULL_REQUEST_TEMPLATE.md` con trazabilidad `Closes #N` y ruta `specs/SPEC-NNN-*`.

## Criterios de Aceptación (Given-When-Then)
1. **Given** un entorno limpio con `uv` instalado, **When** se ejecuta `uv sync`, **Then** el entorno virtual Python 3.13 instala todas las dependencias sin errores ni uso de `pip`.
2. **Given** la inspección del árbol de archivos del repositorio, **When** se revisan `.gitignore`, `LICENSE` y `.github/PULL_REQUEST_TEMPLATE.md`, **Then** cumplen con las restricciones de seguridad y gobernanza de Anuncio 007.

## Fuera de Alcance
- Implementación del servidor gRPC, cliente web y scripts de evaluación MLflow (cubiertos en `SPEC-002` a `SPEC-040`).

## Métricas de Éxito
- `uv sync` completa con código `0`.
- `uv run ruff check .` retorna `0` errores.
