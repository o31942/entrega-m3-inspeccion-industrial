# Entrega Módulo 3 — Inspección Industrial de Acero Laminado (NEU-DET · gRPC + MaaS + MLflow)

[![CI QA](https://github.com/o31942/entrega-m3-inspeccion-industrial/actions/workflows/ci.yml/badge.svg)](https://github.com/o31942/entrega-m3-inspeccion-industrial/actions/workflows/ci.yml)
[![Python 3.13](https://img.shields.io/badge/python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3130/)
[![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/badge/ruff-linter%20%26%20formatter-261230)](https://docs.astral.sh/ruff/)
[![gRPC](https://img.shields.io/badge/backend-gRPC%20%2B%20Protobuf-244C5A)](protos/defect_inspection.proto)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Servicio desacoplado de detección y clasificación multiclase de defectos superficiales en acero laminado (**NEU-DET**, 6 clases) construido sobre el proyecto del **Módulo 2** para la sustentación del **Módulo 3 (25%)** — *Maestría en Inteligencia Artificial y Ciencia de Datos, Universidad Autónoma de Occidente (Grupo 9 · Omar David Sánchez Jiménez)*.

---

## Enlaces Clave y Documentación Viva

- **Repositorio GitHub:** https://github.com/o31942/entrega-m3-inspeccion-industrial
- **Tablero Kanban (GitHub Projects #4):** https://github.com/users/o31942/projects/4 *(Backlog / In Progress WIP=1 / In Review WIP=2 / Done · 42 Historias · 42 PRs fusionadas)*
- **Diagrama Interactivo Archify:** [`docs/arquitectura.html`](docs/arquitectura.html) *(Architecture · Data Flow · Sequence · Lifecycle)*
- **Model Card Oficial:** [`docs/model-card.md`](docs/model-card.md)
- **Decisión de Arquitectura (ADR-001):** [`docs/adr-001-grpc-gateway.md`](docs/adr-001-grpc-gateway.md)
- **Métricas Kanban & Guion Defensa:** [`docs/kanban-metricas.md`](docs/kanban-metricas.md) · [`docs/runbook-sustentacion.md`](docs/runbook-sustentacion.md)
- **Especificaciones SDD (`specs/`):** [`specs/README.md`](specs/README.md) (`42` specs completas con `spec.md`, `plan.md`, `tasks.md`)
- **Contrato Protobuf gRPC:** [`protos/defect_inspection.proto`](protos/defect_inspection.proto)

---

## Modelo Preentrenado (MaaS)

- **Repositorio Hub:** `senanurcetin/neu-steel-defect-resnet18@ad13c70618a8a28a50309456dd40d9a45b2869d1`
- **Licencia:** `MIT`
- **Model Card Hub:** https://huggingface.co/senanurcetin/neu-steel-defect-resnet18
- **Gobernanza:** Los pesos `.onnx` **no** se versionan en Git; se descargan de manera reproducible mediante `make download-model` (`scripts/descargar_modelo.py`).

---

## Arranque Local Completo (4 Servicios Desacoplados)

```powershell
# 1. Instalar dependencias deterministas Python 3.13
uv sync

# 2. Descargar pesos MaaS verificados fuera de Git
make download-model

# 3. Terminal A — Servidor gRPC (:50051) + API Gateway HTTP/Swagger (:8000)
make backend

# 4. Terminal B — Cliente Web Desacoplado HTML5/CSS3/ESM (:5173, cero Streamlit)
make frontend

# 5. Terminal C — Servidor MLflow (:5050) + Evaluación comparable + Model Registry
make mlflow
make eval
```

### Prueba Directa por Terminal (Cliente gRPC Puro)

```powershell
uv run python -m defect_inspector.api.grpc_client --health
```

### Contenedor Docker CPU

```powershell
make docker-build
make docker-run
```

---

## Calidad, Pruebas y Auditoría M3

```powershell
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
uv run python scripts/audit_m3.py
```
