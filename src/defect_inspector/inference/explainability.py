"""Generación de mapa térmico de saliencia XAI, ROI y overlay PNG Base64."""

from __future__ import annotations

import base64
from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True, slots=True)
class SaliencyResult:
    """Resultado visual de explicabilidad espacial para apoyo del inspector."""

    heatmap: np.ndarray
    roi_bbox: tuple[int, int, int, int]
    overlay_png_base64: str


def compute_saliency_and_roi(
    gray_224: np.ndarray,
    roi_half_window: int = 44,
) -> SaliencyResult:
    """Calcula mapa de energía de gradientes Sobel, caja ROI y PNG Base64."""
    if gray_224.ndim != 2:
        raise ValueError(f"Se esperaba matriz 2D, recibido shape {gray_224.shape}.")
    h, w = gray_224.shape
    plane = gray_224.astype(np.float32) / 255.0
    gx = cv2.Sobel(plane, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(plane, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.sqrt(gx**2 + gy**2)
    heatmap = cv2.GaussianBlur(mag, (25, 25), 0)

    max_val = float(heatmap.max())
    if max_val > 1e-6:
        heatmap = heatmap / max_val
    heatmap = np.clip(heatmap, 0.0, 1.0).astype(np.float32)

    _, _, _, max_loc = cv2.minMaxLoc(heatmap)
    cx, cy = int(max_loc[0]), int(max_loc[1])
    x1 = max(0, cx - roi_half_window)
    y1 = max(0, cy - roi_half_window)
    x2 = min(w, cx + roi_half_window)
    y2 = min(h, cy + roi_half_window)

    base_bgr = cv2.cvtColor(gray_224.astype(np.uint8), cv2.COLOR_GRAY2BGR)
    heat_u8 = (heatmap * 255.0).astype(np.uint8)
    color_map = cv2.applyColorMap(heat_u8, cv2.COLORMAP_JET)
    blended = cv2.addWeighted(base_bgr, 0.62, color_map, 0.38, 0)
    cv2.rectangle(blended, (x1, y1), (x2, y2), (16, 185, 129), 2)

    ok, png_buf = cv2.imencode(".png", blended)
    if not ok:
        raise RuntimeError("No se pudo codificar el overlay XAI a PNG.")
    b64 = base64.b64encode(png_buf.tobytes()).decode("ascii")
    return SaliencyResult(
        heatmap=heatmap, roi_bbox=(x1, y1, x2, y2), overlay_png_base64=b64
    )
