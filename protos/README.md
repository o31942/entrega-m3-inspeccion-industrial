# Contratos Protobuf gRPC (`inspection.v1`)

Contrato único fuente de verdad para `DefectInspectionService` en `:50051`:
- `CheckHealth(HealthRequest) -> HealthResponse`
- `GetModelInfo(ModelInfoRequest) -> ModelInfoResponse`
- `InspectSurface(InspectRequest) -> InspectResponse`

Compilar stubs con `make proto`.
