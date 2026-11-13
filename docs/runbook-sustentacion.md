# Guion Operativo de Sustentación M3 (12 Minutos en Vivo + 3 Min Preguntas)

> **Grupo 9 · Omar David Sánchez Jiménez · Sábado 14 de noviembre de 2026 · 11:30–11:45 a.m. · Salón 2103 (A2)**

## Arranque Previo (antes de las 11:00 a.m.)

```powershell
# Terminal 1: Backend gRPC (:50051) + HTTP Gateway (:8000)
uv run python -m defect_inspector.api.run_backend

# Terminal 2: Cliente Desacoplado HTML/ESM (:5173)
uv run python scripts/serve_frontend.py

# Terminal 3: Servidor MLflow UI (:5050, worker único SQLite)
uv run mlflow server --host 127.0.0.1 --port 5050 --workers 1 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns
```

## Ventanas Abiertas en Pantalla
1. Navegador pestaña 1: Frontend `http://127.0.0.1:5173` (con DevTools → **Network** abierto).
2. Navegador pestaña 2: Swagger `/docs` en `http://127.0.0.1:8000/docs`.
3. Navegador pestaña 3: MLflow UI `http://127.0.0.1:5050`.
4. Navegador pestaña 4: GitHub Repo & Kanban Project `#4` (`https://github.com/users/o31942/projects/4`).
5. IDE abierto en `specs/`, `docs/arquitectura.html`, `docs/model-card.md` y terminal lista.

## Cronograma 12:00 Minutos
- **0:00–3:00 (Demo E2E, 25%):** En `:5173`, mostrar `/health` online → cargar muestra / generar Canvas → activar CLAHE y umbral `0.85` → ver estado `loading` → `success` con mapa térmico XAI + `LOW_CONFIDENCE_REVIEW` → bajar umbral a `0.50` → enseñar `POST /api/v1/inspect` en DevTools Network.
- **3:00–5:00 (Kanban + SDD, 15%):** Mostrar Project `#4` (4 columnas, WIP limits, Fibonacci 1:1) → abrir 2 specs completas en `specs/` (`spec.md`, `plan.md`, `tasks.md`) y su PR con `Closes #N`, checks verdes y revisión.
- **5:00–7:30 (MLflow, 20%):** En `http://127.0.0.1:5050`, abrir experimento `neu-steel-defect-inspection`, seleccionar las 4 corridas → **Compare** (accuracy, F1, latencia p95, throughput, sin hiperparámetros de entreno), enseñar `confusion_matrix.png`, wrapper PyFunc y **Model Registry** (`neu-steel-defect-resnet18@production`).
- **7:30–9:30 (Backend gRPC 3 Capas, 15%):** En terminal, ejecutar cliente CLI gRPC directo contra `:50051` (`uv run python -m defect_inspector.api.grpc_client --health`); mostrar `protos/defect_inspection.proto`, `/docs` y separación 3 capas en `src/defect_inspector/`.
- **9:30–11:00 (QA & Docker, 15%):** Ejecutar `uv run ruff check .`, `uv run pytest -q` (`>= 120 passed`) y enseñar `Dockerfile` + contenedor CPU corriendo.
- **11:00–12:00 (Model Card & Archify, 10%):** Mostrar `docs/arquitectura.html` (4 vistas) y `docs/model-card.md` resaltando HITL y sesgos del benchmark NEU.
