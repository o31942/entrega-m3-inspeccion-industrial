# SPEC-043 — US-43: Pipeline GitLab CI/CD (4 etapas), Constitución Técnica y Despliegue Cloud HTTPS

- **Etiqueta Kanban:** `infra`
- **Story Points (Fibonacci 1:1):** `5 SP`
- **Milestone:** `M4`

## Problema y Contexto
Para el Módulo 4, el sistema desacoplado de inspección industrial (`gRPC :50051` + `Gateway HTTP :8000` + `Frontend HTML5/ESM`) debe cerrar el ciclo continuo de extremo a extremo desde un `git push` hasta una URL pública HTTPS detrás de proxy inverso y firewall en un VPS/Droplet, publicando imágenes con tags trazables en Container Registry / Docker Hub y gobernando secretos fuera del repositorio junto con `CONSTITUTION.md`.

## Requisitos Funcionales y No Funcionales
- **RF-001:** Definir `CONSTITUTION.md` en la raíz del repositorio y enlazarla desde `README.md`.
- **RF-002:** Versionar `.gitlab-ci.yml` con las 4 etapas `lint` → `test` → `build` (`build_image`) → `deploy` (`deploy_droplet`), caché de `.cache/uv`, artefactos JUnit/cobertura y verificación activa de `HEALTHCHECK` (`healthy`).
- **RF-003:** Soportar modo de despliegue cloud unificado en `gateway.py` (`SERVE_STATIC_FRONTEND=1` y `CORS_ORIGINS` configurable) y autodetección de origen HTTPS en el frontend sin alterar el modo local desacoplado (`:5173` → `:8000` → `:50051`).
- **RF-004:** Proveer scripts reproducibles de aprovisionamiento del Droplet (`deploy/setup_droplet.sh` y `deploy/Caddyfile` con UFW `22/80/443` y SSL automático) y soporte de GitLab Generic Packages en `scripts/descargar_modelo.py` y `scripts/publish_generic_package.py`.
- **RNF-001:** Cero credenciales, llaves SSH, tokens ni archivos `.onnx`/`.env` versionados en Git; mantener Python 3.13, `uv`, `ruff` sin advertencias y suite `pytest` 100% verde.

## Criterios de Aceptación (Given-When-Then)
1. **Given** `SERVE_STATIC_FRONTEND=1` en el contenedor de producción, **When** un navegador consulta `GET /`, `GET /health`, `GET /docs` y `POST /api/v1/inspect`, **Then** sirve el cliente HTML5/ESM y delega toda inferencia por gRPC hacia `:50051`.
2. **Given** `.gitlab-ci.yml` y `CONSTITUTION.md` en el repositorio, **When** se ejecutan las pruebas contractuales en `pytest` y `ruff check .`, **Then** validan las 4 etapas CI/CD, artefactos, caché y ausencia total de secretos expuestos.
3. **Given** un Droplet aprovisionado con `deploy/setup_droplet.sh`, **When** finaliza la etapa `deploy` tras un `git push` a `main`, **Then** el contenedor reporta estado `healthy` detrás de Caddy con HTTPS válido.
