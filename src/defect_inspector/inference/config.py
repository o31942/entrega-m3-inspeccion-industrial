"""Configuración inmutable del modelo MaaS NEU-DET y constantes de preprocesamiento."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_MODEL_ID = "senanurcetin/neu-steel-defect-resnet18"
DEFAULT_MODEL_REVISION = "ad13c70618a8a28a50309456dd40d9a45b2869d1"
DEFAULT_MODEL_LICENSE = "MIT"
DEFAULT_HUB_URL = f"https://huggingface.co/{DEFAULT_MODEL_ID}"
DEFAULT_MODEL_FILENAME = "neu_resnet18.onnx"
DEFAULT_INPUT_SIZE = 224
DEFAULT_CONF_THRESHOLD = 0.70

IMAGENET_MEAN: tuple[float, float, float] = (0.485, 0.456, 0.406)
IMAGENET_STD: tuple[float, float, float] = (0.229, 0.224, 0.225)

NEU_CLASSES: tuple[str, ...] = (
    "crazing",
    "inclusion",
    "patches",
    "pitted_surface",
    "rolled-in_scale",
    "scratches",
)

NEU_CLASSES_ES: dict[str, str] = {
    "crazing": "Agrietamiento (Crazing)",
    "inclusion": "Inclusión (Inclusion)",
    "patches": "Parches de Oxidación (Patches)",
    "pitted_surface": "Picaduras Superficiales (Pitted Surface)",
    "rolled-in_scale": "Cascarilla Laminada (Rolled-in Scale)",
    "scratches": "Rayaduras (Scratches)",
}


@dataclass(frozen=True, slots=True)
class ModelSpecConfig:
    """Especificación verificable del modelo preentrenado MaaS cargado en CPU."""

    model_id: str = DEFAULT_MODEL_ID
    revision: str = DEFAULT_MODEL_REVISION
    license_name: str = DEFAULT_MODEL_LICENSE
    hub_url: str = DEFAULT_HUB_URL
    filename: str = DEFAULT_MODEL_FILENAME
    input_size: int = DEFAULT_INPUT_SIZE
    default_threshold: float = DEFAULT_CONF_THRESHOLD
    models_dir: Path = Path("models")

    @property
    def onnx_path(self) -> Path:
        """Ruta esperada del binario ONNX local descargado fuera de Git."""
        return self.models_dir / self.filename

    @classmethod
    def from_env(cls, root_dir: Path | None = None) -> ModelSpecConfig:
        """Construye configuración respetando variables de entorno del despliegue."""
        base = root_dir or Path.cwd()
        model_id = os.getenv("MAAS_MODEL_ID", DEFAULT_MODEL_ID)
        revision = os.getenv("MAAS_MODEL_REVISION", DEFAULT_MODEL_REVISION)
        threshold = float(
            os.getenv("DEFAULT_CONF_THRESHOLD", str(DEFAULT_CONF_THRESHOLD))
        )
        models_dir = Path(os.getenv("MAAS_MODELS_DIR", str(base / "models")))
        return cls(
            model_id=model_id,
            revision=revision,
            hub_url=f"https://huggingface.co/{model_id}",
            default_threshold=threshold,
            models_dir=models_dir,
        )
