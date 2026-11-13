"""Servidor gRPC con carga única del modelo MaaS y grpc.health.v1."""

from __future__ import annotations

import logging
import os
from concurrent import futures
from pathlib import Path

import grpc
from grpc_health.v1 import health, health_pb2, health_pb2_grpc

from defect_inspector.api.grpc_servicer import DefectInspectionServicer
from defect_inspector.generated import defect_inspection_pb2_grpc
from defect_inspector.inference.config import ModelSpecConfig
from defect_inspector.inference.model_loader import OnnxDefectClassifier
from defect_inspector.services.inspection_service import DefectInspectionService

logger = logging.getLogger("defect_inspector.grpc")


def build_runtime_service(root_dir: Path | None = None) -> DefectInspectionService:
    """Instancia el modelo ONNX UNA sola vez al arranque del servidor."""
    cfg = ModelSpecConfig.from_env(root_dir=root_dir)
    classifier = OnnxDefectClassifier(config=cfg)
    return DefectInspectionService(classifier=classifier, config=cfg)


def create_grpc_server(
    service: DefectInspectionService,
    host: str = "127.0.0.1",
    port: int = 50051,
    max_workers: int = 8,
) -> tuple[grpc.Server, int]:
    """Configura servidor gRPC con límites de payload y HealthServicer estándar."""
    options = [
        ("grpc.max_send_message_length", 20 * 1024 * 1024),
        ("grpc.max_receive_message_length", 20 * 1024 * 1024),
    ]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers),
        options=options,
    )
    defect_inspection_pb2_grpc.add_DefectInspectionServiceServicer_to_server(
        DefectInspectionServicer(service), server
    )
    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    health_servicer.set("", health_pb2.HealthCheckResponse.SERVING)
    health_servicer.set(
        "inspection.v1.DefectInspectionService",
        health_pb2.HealthCheckResponse.SERVING,
    )
    bound_port = server.add_insecure_port(f"{host}:{port}")
    if bound_port == 0:
        raise RuntimeError(f"No se pudo enlazar puerto gRPC en {host}:{port}")
    return server, bound_port


def serve() -> None:
    """Inicia el servidor gRPC bloqueante escuchando peticiones en 127.0.0.1:50051."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    host = os.getenv("GRPC_HOST", "127.0.0.1")
    port = int(os.getenv("GRPC_PORT", "50051"))
    svc = build_runtime_service()
    server, bound_port = create_grpc_server(svc, host=host, port=port)
    server.start()
    logger.info(
        "gRPC DefectInspectionService activo en %s:%d (modelo=%s@%s)",
        host,
        bound_port,
        svc.check_health().model_id,
        svc.check_health().model_revision[:8],
    )
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Apagando servidor gRPC de forma ordenada...")
        server.stop(grace=2.0)


if __name__ == "__main__":
    serve()
