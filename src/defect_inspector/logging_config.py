"""Configuración de logging estructurado compartida por gRPC y Gateway."""

from __future__ import annotations

import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    """Inicializa formato estructurado uniforme con timestamp y nombre de módulo."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s | level=%(levelname)s | logger=%(name)s | msg=%(message)s",
        stream=sys.stdout,
        force=True,
    )
