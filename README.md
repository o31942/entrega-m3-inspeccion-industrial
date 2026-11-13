# Entrega Módulo 3 — Inspección Industrial de Acero Laminado (NEU-DET · gRPC + MaaS + MLflow)

[![Python 3.13](https://img.shields.io/badge/python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3130/)
[![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/badge/ruff-linter%20%26%20formatter-261230)](https://docs.astral.sh/ruff/)
[![gRPC](https://img.shields.io/badge/backend-gRPC%20%2B%20Protobuf-244C5A)](protos/defect_inspection.proto)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Servicio desacoplado de detección y clasificación multiclase de defectos superficiales en acero laminado (**NEU-DET**, 6 clases) construido sobre el proyecto del **Módulo 2** para la sustentación del **Módulo 3 (25%)** — *Maestría en Inteligencia Artificial y Ciencia de Datos, Universidad Autónoma de Occidente (Grupo 9 · Omar David Sánchez Jiménez)*.

---

## Enlaces Clave y Documentación Viva

- **Repositorio GitHub:** https://github.com/o31942/entrega-m3-inspeccion-industrial
- **Tablero Kanban (GitHub Projects):** https://github.com/users/o31942/projects/4 *(Público · Backlog / In Progress WIP=1 / In Review WIP=2 / Done)*
- **Diagrama de Arquitectura (Archify HTML):** [`docs/arquitectura.html`](docs/arquitectura.html)
- **Model Card del Sistema:** [`docs/model-card.md`](docs/model-card.md)
- **Especificaciones SDD (`specs/`):** [`specs/README.md`](specs/README.md) · Ejemplos iniciales: [`SPEC-001`](specs/SPEC-001-repo-gitflow/spec.md), [`SPEC-002`](specs/SPEC-002-proto-contract/spec.md)
- **Contrato Protobuf gRPC:** [`protos/defect_inspection.proto`](protos/defect_inspection.proto)

---

## Modelo Preentrenado (MaaS)

- **Repositorio Hub:** `senanurcetin/neu-steel-defect-resnet18@ad13c70618a8a28a50309456dd40d9a45b2869d1`
- **Licencia:** `MIT`
- **Model Card Hub:** https://huggingface.co/senanurcetin/neu-steel-defect-resnet18
- **Nota de gobernanza:** Los pesos `.onnx` **no** se versionan en Git; se descargan desde Hugging Face Hub mediante `make download-model` (`scripts/descargar_modelo.py`).

---

## Arquitectura Desacoplada en 3 Capas

1. **Cliente Web Desacoplado (`frontend/`, puerto `5173`):** Cliente HTML5/CSS3/ES Modules separado sin Streamlit/Gradio, con estados `idle`, `loading`, `success` y `error`.
2. **Gateway HTTP→gRPC (`:8000`) + Servidor gRPC (`:50051`):**
   - **Capa 3 (API / Contrato):** `protos/defect_inspection.proto`, `api/grpc_server.py` (gRPC puro `:50051` + health check + carga única al iniciar) y `api/gateway.py` (adaptador HTTP/JSON `/docs`, `/health`, `/api/v1/inspect` hacia el stub gRPC).
   - **Capa 2 (Servicio):** `services/inspection_service.py` (reglas HITL, umbrales, DTOs; sin importar gRPC/FastAPI).
   - **Capa 1 (Inferencia):** `inference/` (`reader.py`, `preprocessor.py`, `model_loader.py` con ONNX Runtime CPU).
3. **Observabilidad MLflow (`http://127.0.0.1:5050`):** Mínimo 3 corridas comparables, métricas de calidad y latencia (media/p95, throughput), artefactos y Model Registry consistente con el modelo en servicio.

---

## Instalación y Arranque Local (`uv` + Python 3.13)

```powershell
# 1. Instalar dependencias deterministas
uv sync

# 2. Compilar contrato Protobuf y descargar pesos MaaS (fuera de Git)
make proto
make download-model

# 3. Verificar calidad y pruebas sintéticas (AAA)
uv run ruff check .
uv run pytest -q

# 4. Levantar Backend (gRPC :50051 + Gateway HTTP :8000), Frontend (:5173) y MLflow (:5050)
make backend
make frontend
make mlflow
```

---

## Estructura del Repositorio

```text
entrega-modulo-3/
├── .github/                  # Plantilla oficial de PR y CI GitHub Actions
├── docs/                     # Model Card y diagrama interactivo Archify (HTML)
├── frontend/                 # Cliente web desacoplado (HTML5 + CSS3 + JS ESM)
├── protos/                   # Contrato gRPC (defect_inspection.proto)
├── scripts/                  # Descarga reproducible de pesos MaaS y corrida MLflow
├── specs/                    # Especificaciones SDD (SPEC-001 .. SPEC-040+)
├── src/defect_inspector/     # Paquete Python en 3 capas (inference, services, api)
└── tests/                    # Suite pytest sintética AAA (>= 120 pruebas)
```
