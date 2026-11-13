"""Pruebas unitarias AAA para configuración centralizada de MLflow (:5050)."""

from __future__ import annotations

from pathlib import Path

from defect_inspector.mlops.tracking import (
    DEFAULT_EXPERIMENT_NAME,
    DEFAULT_MLFLOW_URI,
    MlflowSettings,
    check_mlflow_server,
)


def test_mlflow_settings_defaults_prevent_split_brain(tmp_path: Path) -> None:
    # Arrange & Act
    cfg = MlflowSettings.from_env()

    # Assert
    assert cfg.tracking_uri == DEFAULT_MLFLOW_URI
    assert cfg.experiment_name == DEFAULT_EXPERIMENT_NAME
    assert cfg.backend_store_uri == "sqlite:///mlflow.db"
    assert cfg.workers == 1
    assert tmp_path.exists()


def test_check_mlflow_server_returns_false_on_closed_port() -> None:
    # Arrange & Act
    ok = check_mlflow_server("http://127.0.0.1:59997", timeout_s=0.3)

    # Assert
    assert ok is False
