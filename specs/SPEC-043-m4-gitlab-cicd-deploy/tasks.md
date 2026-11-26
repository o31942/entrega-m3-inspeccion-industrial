# Tareas Verificables — SPEC-043

- [x] Redactar y versionar `SPEC-043` (`spec.md`, `plan.md`, `tasks.md`) previo a codificar.
- [x] Crear `CONSTITUTION.md` en la raíz y enlazarla en `README.md`.
- [x] Implementar `CORS_ORIGINS` dinámico, servicio estático opcional `SERVE_STATIC_FRONTEND` en `gateway.py` y autodetección de origen en `frontend/js/`.
- [x] Actualizar `.dockerignore`, `Dockerfile` y `scripts/descargar_modelo.py` + `scripts/publish_generic_package.py` para Generic Packages y empaquetado web completo.
- [x] Implementar `.gitlab-ci.yml` (`lint`, `test`, `build_image`, `deploy_droplet`) y scripts de infraestructura `deploy/Caddyfile` + `deploy/setup_droplet.sh`.
- [x] Añadir suite `tests/test_m4_cicd_deploy.py` y verificar `ruff check .`, `ruff format --check .`, `pytest -q` y `scripts/audit_m3.py` en verde.
