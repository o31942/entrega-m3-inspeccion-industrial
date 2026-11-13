"""Carga única en memoria del modelo MaaS ONNX y postprocesamiento softmax."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import numpy as np
import onnxruntime as ort

from defect_inspector.inference.config import (
    NEU_CLASSES,
    NEU_CLASSES_ES,
    ModelSpecConfig,
)


class ModelLoadError(RuntimeError):
    """Error lanzado cuando el archivo ONNX MaaS no existe o no puede inicializarse."""


class OnnxSessionProtocol(Protocol):
    """Protocolo mínimo compatible con onnxruntime.InferenceSession para testabilidad."""

    def get_inputs(self) -> list[object]: ...

    def run(
        self, output_names: list[str] | None, input_feed: dict[str, np.ndarray]
    ) -> list[np.ndarray]: ...


@dataclass(frozen=True, slots=True)
class RawPrediction:
    """Salida numérica calibrada de inferencia multiclase."""

    predicted_class: str
    predicted_label_es: str
    confidence: float
    probabilities: dict[str, float]


def stable_softmax(logits: np.ndarray) -> np.ndarray:
    """Calcula softmax numéricamente estable sobre vector 1D de logits."""
    arr = np.asarray(logits, dtype=np.float64).reshape(-1)
    shifted = arr - np.max(arr)
    exp_vals = np.exp(shifted)
    total = float(np.sum(exp_vals))
    if total <= 0.0:
        raise ValueError("La suma de exponenciales en softmax no es positiva.")
    return (exp_vals / total).astype(np.float64)


class OnnxDefectClassifier:
    """Clasificador ONNX Runtime CPU cargado una única vez al arrancar el servicio."""

    def __init__(
        self,
        config: ModelSpecConfig | None = None,
        session: OnnxSessionProtocol | None = None,
        input_name: str = "image",
    ) -> None:
        self.config = config or ModelSpecConfig.from_env()
        self.runtime_name = "ONNXRuntime-CPU"
        if session is not None:
            self._session = session
            self._input_name = input_name
            return

        model_path: Path = self.config.onnx_path
        if not model_path.is_file():
            raise ModelLoadError(
                f"Modelo MaaS no encontrado en '{model_path}'. "
                "Ejecuta 'uv run python scripts/descargar_modelo.py' primero."
            )
        sess_opts = ort.SessionOptions()
        sess_opts.intra_op_num_threads = 2
        self._session = ort.InferenceSession(
            str(model_path),
            sess_options=sess_opts,
            providers=["CPUExecutionProvider"],
        )
        self._input_name = str(self._session.get_inputs()[0].name)

    def predict_tensor(self, tensor: np.ndarray) -> RawPrediction:
        """Ejecuta inferencia forward sobre tensor NCHW (1, 3, 224, 224)."""
        outputs = self._session.run(None, {self._input_name: tensor.astype(np.float32)})
        logits = np.asarray(outputs[0])[0]
        probs = stable_softmax(logits)
        best_idx = int(np.argmax(probs))
        best_class = NEU_CLASSES[best_idx]
        prob_map = {
            cls_name: float(round(float(probs[idx]), 6))
            for idx, cls_name in enumerate(NEU_CLASSES)
        }
        return RawPrediction(
            predicted_class=best_class,
            predicted_label_es=NEU_CLASSES_ES[best_class],
            confidence=float(round(float(probs[best_idx]), 6)),
            probabilities=prob_map,
        )
