"""Traducción explícita de excepciones de dominio a códigos de estado gRPC."""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any

import grpc

from defect_inspector.services.exceptions import (
    DomainValidationError,
    InspectionProcessingError,
    ModelNotReadyError,
    UnsupportedImageFormatError,
)

ERROR_TO_GRPC_STATUS: dict[type[Exception], grpc.StatusCode] = {
    DomainValidationError: grpc.StatusCode.INVALID_ARGUMENT,
    UnsupportedImageFormatError: grpc.StatusCode.INVALID_ARGUMENT,
    ModelNotReadyError: grpc.StatusCode.FAILED_PRECONDITION,
    InspectionProcessingError: grpc.StatusCode.INTERNAL,
}


def map_exception_to_grpc_status(exc: Exception) -> grpc.StatusCode:
    """Resuelve el grpc.StatusCode correspondiente a una excepción de dominio."""
    for exc_type, code in ERROR_TO_GRPC_STATUS.items():
        if isinstance(exc, exc_type):
            return code
    return grpc.StatusCode.INTERNAL


def handle_grpc_errors(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Decorador para traducir excepciones de Capa 2 en context.abort(...) gRPC."""

    @functools.wraps(fn)
    def wrapper(self: Any, request: Any, context: grpc.ServicerContext) -> Any:
        try:
            return fn(self, request, context)
        except Exception as exc:
            status_code = map_exception_to_grpc_status(exc)
            if context is not None:
                context.abort(status_code, str(exc))
            raise

    return wrapper
