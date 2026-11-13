# Plan Técnico — SPEC-041

## Diseño y Decisiones
Plantilla Markdown YAML frontmatter + documentación operativa Kanban.

## Archivos Afectados
- `.github/ISSUE_TEMPLATE/user_story.md`, `docs/kanban-metricas.md`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
