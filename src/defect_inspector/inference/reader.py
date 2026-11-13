"""Ingesta segura y validación de imágenes superficiales en Capa 1."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

ALLOWED_CONTENT_TYPES: frozenset[str] = frozenset(
    {
        "",
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/bmp",
        "image/webp",
        "image/tiff",
        "application/octet-stream",
    }
)
MIN_IMAGE_EDGE = 16
MAX_IMAGE_BYTES = 10 * 1024 * 1024


class InvalidImageError(ValueError):
    """Error lanzado cuando la imagen está vacía, corrupta o es demasiado pequeña."""


class UnsupportedMediaError(ValueError):
    """Error lanzado cuando el tipo MIME declarado no corresponde a imagen soportada."""


def _validate_dimensions(img: np.ndarray) -> np.ndarray:
    if img.ndim not in (2, 3):
        raise InvalidImageError(f"Dimensiones de imagen no soportadas: {img.shape}")
    height, width = img.shape[:2]
    if height < MIN_IMAGE_EDGE or width < MIN_IMAGE_EDGE:
        raise InvalidImageError(
            f"Resolución insuficiente ({width}x{height}); mínimo {MIN_IMAGE_EDGE}x{MIN_IMAGE_EDGE}."
        )
    if img.ndim == 3 and img.shape[2] == 4:
        return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    if img.ndim == 3 and img.shape[2] == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if img.ndim == 3 and img.shape[2] == 1:
        return img[:, :, 0].copy()
    return img.copy()


def read_industrial_image(
    source: str | Path | bytes | np.ndarray,
    content_type: str = "",
) -> np.ndarray:
    """Lee una imagen superficial y retorna matriz 2D uint8 en escala de grises."""
    normalized_ct = content_type.strip().lower().split(";", 1)[0]
    if normalized_ct not in ALLOWED_CONTENT_TYPES:
        raise UnsupportedMediaError(
            f"Tipo de contenido no soportado: '{content_type}'. Use PNG, JPEG o BMP."
        )

    if isinstance(source, np.ndarray):
        if source.size == 0:
            raise InvalidImageError("La matriz de imagen está vacía.")
        return _validate_dimensions(np.clip(source, 0, 255).astype(np.uint8))

    if isinstance(source, bytes):
        if not source:
            raise InvalidImageError("El buffer de imagen está vacío.")
        if len(source) > MAX_IMAGE_BYTES:
            raise InvalidImageError(
                f"El archivo excede el máximo permitido ({MAX_IMAGE_BYTES // (1024 * 1024)} MB)."
            )
        arr = np.frombuffer(source, dtype=np.uint8)
        decoded = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
        if decoded is None:
            raise InvalidImageError(
                "No se pudo decodificar el buffer como imagen válida."
            )
        return _validate_dimensions(decoded)

    path = Path(source)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Archivo de imagen no encontrado: {path}")
    raw_bytes = path.read_bytes()
    return read_industrial_image(raw_bytes, content_type=content_type)
