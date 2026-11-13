# Especificaciones SDD — Entrega Módulo 3

Cada funcionalidad o historia del tablero Kanban posee su carpeta versionada en `specs/SPEC-NNN-nombre/` creada **antes de implementar** (Spec-Driven Development) y vinculada 1:1 a una Pull Request (`Closes #N`).

Cada especificación contiene:
- `spec.md`: contexto, problema, requisitos funcionales/no funcionales, criterios de aceptación Given-When-Then y fuera de alcance.
- `plan.md`: diseño técnico en 3 capas, contratos Protobuf/DTO, decisiones, riesgos y estrategia de verificación.
- `tasks.md`: tareas atómicas verificables marcadas al cerrar la PR.
