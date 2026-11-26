# Constitución de Ingeniería — Inspección Industrial NEU-DET (M1–M4)

> **Proyecto:** `entrega-m3-inspeccion-industrial` · **Grupo 9:** Omar David Sánchez Jiménez · **UAO Maestría en IA y Ciencia de Datos (2026-2S)**

Este documento establece las **reglas arquitectónicas, operativas y de seguridad innegociables** que rigen todo cambio, Pull Request / Merge Request, pipeline CI/CD y despliegue en nube del sistema.

---

## 1. Arquitectura en 3 Capas y Desacoplamiento Real

1. **Separación estricta de responsabilidades en `src/defect_inspector/`:**
   - **Capa 1 (`inference/`):** lectura segura MIME, preprocesamiento CLAHE, inferencia única en memoria con **ONNX Runtime CPU** (`OnnxDefectClassifier`) y explicabilidad espacial Sobel (`compute_saliency_and_roi`). Prohibido importar `grpc`, `fastapi` o librerías de transporte.
   - **Capa 2 (`services/`):** DTOs inmutables, validaciones de dominio y política **Human-in-the-Loop (HITL)** (`LOW_CONFIDENCE_REVIEW` cuando `confidence < conf_threshold`). Prohibido acoplarse a gRPC o HTTP.
   - **Capa 3 (`api/`):** servidor **gRPC + Protobuf** (`:50051`, contrato `protos/defect_inspection.proto` + `grpc.health.v1`) y **API Gateway FastAPI** delgado (`:8000`) que traduce REST/multipart exclusivamente hacia el stub gRPC, sin ejecutar inferencia propia.
2. **Cliente Web Desacoplado (`frontend/`):** HTML5 + CSS3 + JavaScript ES Modules puro con máquina de 4 estados (`idle`, `loading`, `success`, `error`). Queda prohibido el uso de frameworks monolíticos acoplados al proceso Python de inferencia.

---

## 2. Metodología Spec-Driven Development (SDD) y Flujo Git / Kanban

1. **Spec-First:** Ninguna funcionalidad entra sin su especificación previa en `specs/SPEC-NNN-nombre/` (`spec.md`, `plan.md`, `tasks.md`).
2. **Flujo de ramas y trazabilidad:** Ramas `feature/spec-NNN-*` hacia `develop` y entregas verificadas hacia `main`, usando **Conventional Commits** (`feat`, `fix`, `docs`, `chore`, `ci`, `infra`), plantilla de PR y cierre trazable (`Closes #N`).
3. **Límites WIP en Kanban (GitHub Projects #4):** `In Progress` (`WIP = 1`), `In Review` (`WIP = 2`) y estimación Fibonacci `1:1`.

---

## 3. Entorno Determinista y Puertas de Calidad (QA)

1. **Gestor único `uv`:** Python `3.13` fijado en `.python-version`, `pyproject.toml` y `uv.lock`. Prohibido versionar `requirements.txt` o instalar paquetes globales con `pip`.
2. **Calidad obligatoria antes de cada merge o deploy:**
   - `uv run ruff check .` y `uv run ruff format --check .` con cero advertencias.
   - `uv run pytest -q` con al menos **120 pruebas** deterministas bajo patrón **AAA (Arrange-Act-Assert)** ejecutables 100% offline.
   - `uv run python scripts/verify_ci.py` y `uv run python scripts/audit_m3.py` en verde.

---

## 4. Seguridad, Secretos y Gobernanza de Artefactos Pesados

1. **Cero secretos en el repositorio:** Queda estrictamente prohibido versionar archivos `.env`, llaves privadas SSH (`SSH_KEY`, `*.pem`, `id_ed25519*`), contraseñas o tokens (`REGISTRY_PASS`, `GITLAB_TOKEN`). Toda credencial reside únicamente en variables protegidas/enmascaradas de CI/CD.
2. **Cero binarios pesados en Git:** Ningún peso de modelo (`.onnx`, `.h5`, `.pt`, `.joblib`, `.pkl`) ni notebook (`.ipynb`) puede versionarse en Git. El modelo MaaS (`senanurcetin/neu-steel-defect-resnet18@ad13c70618a8a28a50309456dd40d9a45b2869d1`, licencia `MIT`) se obtiene de forma reproducible desde **GitLab Generic Packages** o **Hugging Face Hub** mediante `scripts/descargar_modelo.py`.
3. **Contenedor seguro:** Ejecución bajo usuario sin privilegios (`USER appuser`), puertos de aplicación ligados a `127.0.0.1` en el VPS detrás de firewall **UFW** (`22/80/443`) y proxy inverso **Caddy** con **HTTPS/TLS válido**.

---

## 5. Pipeline CI/CD Continuo y Operación MLOps

1. **Pipeline automatizado de 4 etapas (`.gitlab-ci.yml`):**
   - `lint` → `test` (con caché `.cache/uv` y artefactos JUnit/cobertura) → `build` (`build_image` publicando tags `:$CI_COMMIT_SHORT_SHA` y `:latest` en Container Registry y Docker Hub) → `deploy` (`deploy_droplet` vía SSH verificando `HEALTHCHECK` Docker `healthy` y endpoint `/health` sobre HTTPS).
2. **Trazabilidad MLOps y Supervisión Humana:** Las configuraciones operativas (CLAHE y umbral HITL) se auditan empíricamente en **MLflow** (`scripts/evaluar.py`, Model Registry `@production`), preservando siempre la derivación a revisión humana ante baja incertidumbre.
