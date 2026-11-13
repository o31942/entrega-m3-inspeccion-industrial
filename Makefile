.PHONY: help sync proto download-model test lint format backend grpc gateway frontend mlflow eval docker-build docker-run

help:
	@echo "Comandos disponibles - Entrega M3 (gRPC + MaaS ONNX + Frontend Desacoplado + MLflow)"
	@echo "  uv sync              Instala dependencias deterministas Python 3.13"
	@echo "  make proto           Compila protos/defect_inspection.proto"
	@echo "  make download-model  Descarga pesos MaaS desde Hugging Face Hub (sin Git)"
	@echo "  make backend         Inicia servidor gRPC (:50051) + gateway HTTP (:8000)"
	@echo "  make grpc            Inicia unicamente el servidor gRPC (:50051)"
	@echo "  make frontend        Sirve el cliente desacoplado HTML/CSS/ESM (:5173)"
	@echo "  make mlflow          Inicia servidor y UI MLflow en http://127.0.0.1:5050"
	@echo "  make eval            Registra runs comparables en MLflow (:5050)"
	@echo "  make test            Ejecuta suite pytest en verde"
	@echo "  make lint            Ejecuta ruff check y format --check"

sync:
	uv sync

proto:
	uv run python -m grpc_tools.protoc -Iprotos --python_out=src/defect_inspector/generated --grpc_python_out=src/defect_inspector/generated protos/defect_inspection.proto

download-model:
	uv run python scripts/descargar_modelo.py

test:
	uv run pytest -q

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .

grpc:
	uv run python -m defect_inspector.api.grpc_server

gateway:
	uv run uvicorn defect_inspector.api.gateway:app --host 127.0.0.1 --port 8000

backend:
	uv run python -m defect_inspector.api.run_backend

frontend:
	uv run python -m http.server 5173 --directory frontend

mlflow:
	uv run mlflow server --host 127.0.0.1 --port 5050 --workers 1 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns

eval:
	uv run python scripts/evaluar.py

docker-build:
	docker build -t defect-inspector-grpc:m3 .

docker-run:
	docker run --rm -p 50051:50051 -p 8000:8000 defect-inspector-grpc:m3
