# Trazabilidad Ágil y Métricas Kanban (GitHub Projects #4)

- **Tablero público:** https://github.com/users/o31942/projects/4
- **Columnas oficiales y WIP Limits:**
  1. `Backlog` (sin límite)
  2. `In Progress` (**WIP = 1** por persona/flujo secuencial)
  3. `In Review` (**WIP = 2**)
  4. `Done` (cerradas vía PR con `Closes #N`)
- **Escala de esfuerzo:** Fibonacci **1:1** (`1, 2, 3, 5 SP`, nunca redondeada ni comprimida).

## Las 4 Métricas Kanban del Tablero

| Métrica | Definición operativa en Project #4 | Lectura esperada en M3 |
| --- | --- | --- |
| **WIP (Work In Progress)** | Tarjetas simultáneas en `In Progress` + `In Review` | `<= 3` (`In Progress = 1`, `In Review <= 2`) durante todo el sprint, bajando a `0` al cerrar todas las PRs. |
| **Throughput** | Historias (Issues + PRs) movidas a `Done` por oleada/unidad de tiempo | `42` historias cerradas mediante `42` PRs fusionadas vinculadas 1:1. |
| **Work Item Age** | Tiempo transcurrido desde que una tarjeta entra a `In Progress` sin llegar a `Done` | Controlado por historia individual; nunca supera la ventana de su oleada. |
| **Cycle Time** | Tiempo total desde entrada a `In Progress` hasta estado `Done` tras merge de PR | Pequeños lotes (`1–3 SP`) producen cycle time homogéneo y predecible. |
