# Plan Técnico — SPEC-043

## Diseño y Decisiones
1. **Unificación detrás de Proxy Inverso HTTPS sin romper desacoplamiento local:**
   - En desarrollo local, `scripts/serve_frontend.py` sirve `frontend/` en `:5173` consumiendo `http://127.0.0.1:8000`.
   - En producción (contenedor Docker en Droplet detrás de Caddy HTTPS en `:443`), `SERVE_STATIC_FRONTEND=1` monta `StaticFiles` de `frontend/` al final de `create_gateway_app` (después de registrar `/health`, `/docs` y `/api/v1/*`), mientras `state.js` usa `window.location.origin` cuando el puerto activo no es `5173`/`4173`. Así un único contenedor saludable atiende UI y API sobre el mismo dominio HTTPS evitando bloqueos de Mixed Content y CORS.
2. **Pipeline GitLab CI/CD en 4 etapas (`lint`, `test`, `build`, `deploy`):**
   - `lint` y `test` usan `ghcr.io/astral-sh/uv:python3.13-bookworm-slim` con caché en `.cache/uv` y reportes JUnit + Cobertura XML.
   - `build_image` usa `docker:27.3.1` + `docker:27.3.1-dind`, autenticándose contra GitLab Container Registry (`$CI_REGISTRY`) y opcionalmente Docker Hub (`$REGISTRY_USER` / `$REGISTRY_PASS`), publicando tags `:$CI_COMMIT_SHORT_SHA` y `:latest`.
   - `deploy_droplet` conecta por SSH con `$SSH_KEY`, enlaza puertos de aplicación solo a `127.0.0.1` del host (`127.0.0.1:8000:8000`, `127.0.0.1:50051:50051`) y espera el estado Docker `healthy` antes de validar el endpoint HTTPS público.
3. **Soporte Dual de Artefacto Modelo (Generic Packages + Hugging Face SHA):**
   - `scripts/descargar_modelo.py` acepta `MODEL_PACKAGE_URL` para descargar `neu_resnet18.onnx` desde GitLab Generic Packages cuando está definido, manteniendo respaldo reproducible al commit `ad13c70618a8a28a50309456dd40d9a45b2869d1` en Hugging Face Hub.

## Archivos Afectados
- `CONSTITUTION.md`, `README.md`, `.gitignore`, `.dockerignore`, `.env.example`, `Dockerfile`, `.gitlab-ci.yml`
- `src/defect_inspector/api/gateway.py`, `frontend/js/state.js`, `frontend/js/app.js`
- `scripts/descargar_modelo.py`, `scripts/publish_generic_package.py`
- `deploy/Caddyfile`, `deploy/setup_droplet.sh`
- `tests/test_m4_cicd_deploy.py`

## Estrategia de Pruebas
- Pruebas unitarias e integración AAA 100% offline validando `CONSTITUTION.md`, etapas y variables de `.gitlab-ci.yml`, montaje estático + `CORS_ORIGINS` en `gateway.py`, descarga por URL simulada y ausencia de secretos en el árbol Git.
