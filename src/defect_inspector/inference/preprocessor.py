"""Preprocesamiento adaptativo CLAHE y normalización NCHW para ResNet-18 ONNX."""

from __future__ import annotations

import cv2
import numpy as np

from defect_inspector.inference.config import (
    DEFAULT_INPUT_SIZE,
    IMAGENET_MEAN,
    IMAGENET_STD,
)
from defect_inspector.inference.reader import InvalidImageError


def validate_tensor_contract(
    tensor: np.ndarray,
    target_size: int = DEFAULT_INPUT_SIZE,
) -> None:
    """Valida contrato numérico exacto (1, 3, H, W) float32 finito."""
    expected_shape = (1, 3, target_size, target_size)
    if not isinstance(tensor, np.ndarray):
        raise TypeError("El tensor debe ser una instancia de np.ndarray.")
    if tensor.dtype != np.float32:
        raise ValueError(f"Tipo inválido {tensor.dtype}; se requiere float32.")
    if tensor.shape != expected_shape:
        raise ValueError(f"Shape inválido {tensor.shape}; esperado {expected_shape}.")
    if not np.all(np.isfinite(tensor)):
        raise ValueError("El tensor contiene valores NaN o Inf.")


def enhance_with_clahe(
    gray_img: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: tuple[int, int] = (8, 8),
) -> np.ndarray:
    """Aplica ecualización adaptativa CLAHE preservando matriz uint8 2D."""
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(gray_img.astype(np.uint8))


def preprocess_image(
    raw_img: np.ndarray,
    apply_clahe: bool = False,
    target_size: int = DEFAULT_INPUT_SIZE,
    clip_limit: float = 2.0,
    tile_grid_size: tuple[int, int] = (8, 8),
) -> tuple[np.ndarray, np.ndarray]:
    """Preprocesa imagen hacia tensor NCHW ImageNet y retorna imagen procesada uint8."""
    if raw_img is None or raw_img.size == 0:
        raise InvalidImageError("La imagen a preprocesar está vacía.")

    if raw_img.ndim == 3:
        gray = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
    elif raw_img.ndim == 2:
        gray = raw_img.copy()
    else:
        raise InvalidImageError(f"Dimensiones no soportadas: {raw_img.shape}")

    gray_u8 = gray.astype(np.uint8)
    working = (
        enhance_with_clahe(
            gray_u8, clip_limit=clip_limit, tile_grid_size=tile_grid_size
        )
        if apply_clahe
        else gray_u8
    )

    resized_gray = cv2.resize(
        working, (target_size, target_size), interpolation=cv2.INTER_LINEAR
    )
    rgb = cv2.cvtColor(resized_gray, cv2.COLOR_GRAY2RGB).astype(np.float32) / 255.0

    mean = np.array(IMAGENET_MEAN, dtype=np.float32)
    std = np.array(IMAGENET_STD, dtype=np.float32)
    normalized = (rgb - mean) / std
    nchw = np.transpose(normalized, (2, 0, 1))[np.newaxis, ...].astype(np.float32)
    nchw = np.ascontiguousarray(nchw)

    validate_tensor_contract(nchw, target_size=target_size)
    return nchw, resized_gray
