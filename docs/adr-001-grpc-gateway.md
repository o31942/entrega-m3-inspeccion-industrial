# ADR-001: Arquitectura gRPC (:50051) + Gateway HTTP (:8000) + Frontend HTML5/ESM (:5173)

- **Estado:** Aceptado (Módulo 3 · Cohorte 2026-2S · Grupo 9)
- **Fecha:** 2026-11-13
- **Decisores:** Omar David Sánchez Jiménez

## Contexto y Restricciones

1. Anuncio 007 prohíbe explícitamente Streamlit, Gradio o Dash y exige un cliente frontend desacoplado consumiendo el backend por red.
2. El sistema requiere separación estricta en 3 capas (`inference/`, `services/`, `api/`) sirviendo `senanurcetin/neu-steel-defect-resnet18` (`ONNXRuntime-CPU`) una sola vez al iniciar.
3. Un navegador web estándar no invoca gRPC HTTP/2 binario nativo sin proxy, mientras que las pruebas en terminal y clientes servicio-a-servicio sí consumen gRPC directamente (`protos/defect_inspection.proto`).

## Decisión

1. Implementar el **Backend Nuclear en gRPC puro (`:50051`)** sobre Protobuf (`DefectInspectionService`: `CheckHealth`, `GetModelInfo`, `InspectSurface`) más `grpc.health.v1.Health`, demostrable directamente en CLI con `defect_inspector.api.grpc_client`.
2. Exponer un **Gateway HTTP/JSON delgado (`:8000`)** con FastAPI cuya ÚNICA responsabilidad es traducir multipart/REST + Swagger (`/docs`, `/health`) hacia el stub gRPC `:50051` y aplicar CORS al cliente web. Cero código OpenCV ni ONNX vive en el Gateway.
3. Construir el **Frontend Desacoplado (`:5173`)** en HTML5/CSS3/JavaScript ES Modules puro (`frontend/`), con máquina de estados explícita (`idle`, `loading`, `success`, `error`), visible en Chrome DevTools (`Network`).

## Consecuencias

- **Positivas:** Desacoplamiento real demostrable; interoperabilidad dual (gRPC nativo + REST Swagger); prueba unitaria automatizada que impide fugas entre capas.
- **Compensaciones aceptadas:** Se ejecutan dos listeners de red coordinados por `defect_inspector.api.run_backend` tanto localmente como dentro del contenedor Docker CPU.
