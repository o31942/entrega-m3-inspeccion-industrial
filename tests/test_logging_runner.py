"""Pruebas AAA para configuración de logging estructurado y módulos backend."""

from __future__ import annotations

import logging

from defect_inspector.api import run_backend
from defect_inspector.logging_config import configure_logging


def test_configure_logging_sets_requested_level() -> None:
    # Arrange & Act
    configure_logging("DEBUG")

    # Assert
    assert logging.getLogger().getEffectiveLevel() == logging.DEBUG
    assert callable(run_backend.main)
