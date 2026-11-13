"""Lanzador unificado del backend: gRPC (:50051) + API Gateway HTTP (:8000)."""

from __future__ import annotations

import os
import threading
import time

import uvicorn

from defect_inspector.api.gateway import create_gateway_app
from defect_inspector.api.grpc_server import build_runtime_service, create_grpc_server
from defect_inspector.logging_config import configure_logging


def main() -> None:
    """Inicia servidor gRPC en hilo dedicado y Gateway Uvicorn HTTP en primer plano."""
    configure_logging(os.getenv("LOG_LEVEL", "INFO"))
    grpc_host = os.getenv("GRPC_HOST", "127.0.0.1")
    grpc_port = int(os.getenv("GRPC_PORT", "50051"))
    gw_host = os.getenv("GATEWAY_HOST", "127.0.0.1")
    gw_port = int(os.getenv("GATEWAY_PORT", "8000"))

    service = build_runtime_service()
    grpc_server, bound_port = create_grpc_server(
        service, host=grpc_host, port=grpc_port
    )
    grpc_server.start()

    connect_host = "127.0.0.1" if grpc_host == "0.0.0.0" else grpc_host
    target = f"{connect_host}:{bound_port}"
    gateway_app = create_gateway_app(grpc_target=target)

    stop_event = threading.Event()

    def _watch() -> None:
        while not stop_event.is_set():
            time.sleep(0.5)
        grpc_server.stop(grace=2.0)

    watcher = threading.Thread(target=_watch, daemon=True)
    watcher.start()
    try:
        uvicorn.run(gateway_app, host=gw_host, port=gw_port, log_level="info")
    finally:
        stop_event.set()
        grpc_server.stop(grace=2.0)


if __name__ == "__main__":
    main()
