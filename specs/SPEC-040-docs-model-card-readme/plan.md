# Plan Técnico — SPEC-040

## Diseño y Decisiones
Consolidación documental cruzada sin enlaces rotos.

## Archivos Afectados
- `docs/adr-001-grpc-gateway.md`, `docs/model-card.md`, `README.md`

## Alternativas Descartadas y Riesgos
- Acoplar lógica de dominio o modelo dentro del transporte RPC/HTTP o en un único proceso tipo Streamlit: descartado por violar el diseño en 3 capas.

## Estrategia de Pruebas
- Pruebas sintéticas bajo patrón Arrange-Act-Assert (AAA) ejecutables 100% offline.
