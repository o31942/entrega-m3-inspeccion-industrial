"""Configuración centralizada de MLflow Tracking URI y verificación de salud."""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx
import mlflow

DEFAULT_MLFLOW_URI = "http://127.0.0.1:5050"
DEFAULT_EXPERIMENT_NAME = "neu-steel-defect-inspection"
DEFAULT_REGISTRY_NAME = "neu-steel-defect-resnet18"


@dataclass(frozen=True, slots=True)
class MlflowSettings:
    """Parámetros canónicos del servidor MLflow para evitar split-brain SQLite/FS."""

    tracking_uri: str = DEFAULT_MLFLOW_URI
    experiment_name: str = DEFAULT_EXPERIMENT_NAME
    registered_model_name: str = DEFAULT_REGISTRY_NAME
    backend_store_uri: str = "sqlite:///mlflow.db"
    artifact_root: str = "./mlruns"
    workers: int = 1

    @classmethod
    def from_env(cls) -> MlflowSettings:
        """Lee variables de entorno preservando los valores oficiales de M3."""
        return cls(
            tracking_uri=os.getenv("MLFLOW_TRACKING_URI", DEFAULT_MLFLOW_URI),
            experiment_name=os.getenv(
                "MLFLOW_EXPERIMENT_NAME", DEFAULT_EXPERIMENT_NAME
            ),
            registered_model_name=os.getenv(
                "MLFLOW_REGISTERED_MODEL", DEFAULT_REGISTRY_NAME
            ),
        )


def check_mlflow_server(tracking_uri: str, timeout_s: float = 3.0) -> bool:
    """Verifica conectividad HTTP al servidor MLflow UI antes de registrar corridas."""
    url = tracking_uri.rstrip("/") + "/health"
    try:
        resp = httpx.get(url, timeout=timeout_s)
        return resp.status_code == 200
    except httpx.HTTPError:
        return False


def configure_mlflow(settings: MlflowSettings | None = None) -> MlflowSettings:
    """Aplica tracking URI y selecciona/crea el experimento compartido."""
    cfg = settings or MlflowSettings.from_env()
    mlflow.set_tracking_uri(cfg.tracking_uri)
    mlflow.set_experiment(cfg.experiment_name)
    return cfg
