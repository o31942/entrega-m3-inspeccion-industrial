"""Cliente CLI directo gRPC para inspección y pruebas en terminal."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import grpc

from defect_inspector.generated import (
    defect_inspection_pb2,
    defect_inspection_pb2_grpc,
)


def call_health(
    target: str = "127.0.0.1:50051", timeout: float = 5.0
) -> dict[str, Any]:
    """Consulta CheckHealth en el servidor gRPC."""
    with grpc.insecure_channel(target) as channel:
        stub = defect_inspection_pb2_grpc.DefectInspectionServiceStub(channel)
        resp = stub.CheckHealth(defect_inspection_pb2.HealthRequest(), timeout=timeout)
        return {
            "status": resp.status,
            "model_loaded": resp.model_loaded,
            "model_id": resp.model_id,
            "model_revision": resp.model_revision,
            "runtime": resp.runtime,
            "uptime_seconds": resp.uptime_seconds,
        }


def call_inspect(
    image_path: Path,
    target: str = "127.0.0.1:50051",
    conf_threshold: float = 0.70,
    apply_clahe: bool = True,
    timeout: float = 15.0,
) -> dict[str, Any]:
    """Envía bytes de imagen por gRPC y retorna veredicto sin el binario Base64."""
    payload = image_path.read_bytes()
    with grpc.insecure_channel(target) as channel:
        stub = defect_inspection_pb2_grpc.DefectInspectionServiceStub(channel)
        resp = stub.InspectSurface(
            defect_inspection_pb2.InspectRequest(
                image_bytes=payload,
                filename=image_path.name,
                content_type="image/png",
                conf_threshold=conf_threshold,
                apply_clahe=apply_clahe,
            ),
            timeout=timeout,
        )
        return {
            "request_id": resp.request_id,
            "predicted_class": resp.predicted_class,
            "predicted_label_es": resp.predicted_label_es,
            "confidence": round(resp.confidence, 4),
            "decision_status": resp.decision_status,
            "requires_human_review": resp.requires_human_review,
            "latency_ms": resp.latency_ms,
            "roi_bbox": [
                resp.roi_bbox.x1,
                resp.roi_bbox.y1,
                resp.roi_bbox.x2,
                resp.roi_bbox.y2,
            ],
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Cliente gRPC de inspección NEU-DET")
    parser.add_argument("--target", default="127.0.0.1:50051")
    parser.add_argument("--health", action="store_true")
    parser.add_argument("--image", type=Path, default=None)
    parser.add_argument("--threshold", type=float, default=0.70)
    parser.add_argument("--clahe", action="store_true")
    args = parser.parse_args()

    if args.health or args.image is None:
        out = call_health(target=args.target)
    else:
        out = call_inspect(
            args.image,
            target=args.target,
            conf_threshold=args.threshold,
            apply_clahe=args.clahe,
        )
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
