"""Métricas multiclase, telemetría de latencia p95 y matriz de confusión PNG."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
    roc_auc_score,
)


def compute_evaluation_metrics(
    y_true_idx: list[int],
    y_pred_idx: list[int],
    y_prob_matrix: np.ndarray,
    latencies_ms: list[float],
    requires_review_flags: list[bool],
) -> dict[str, float]:
    """Calcula métricas de clasificación y latencia/throughput para MLflow."""
    if not y_true_idx:
        raise ValueError("La lista de evaluación no puede estar vacía.")
    acc = float(accuracy_score(y_true_idx, y_pred_idx))
    prec, rec, f1, _ = precision_recall_fscore_support(
        y_true_idx,
        y_pred_idx,
        average="macro",
        zero_division=0,
    )
    try:
        auc_ovr = float(
            roc_auc_score(
                y_true_idx,
                y_prob_matrix,
                multi_class="ovr",
                average="macro",
                labels=list(range(y_prob_matrix.shape[1])),
            )
        )
    except ValueError:
        auc_ovr = 0.0

    lat_arr = np.asarray(latencies_ms, dtype=np.float64)
    mean_lat = float(np.mean(lat_arr))
    p95_lat = float(np.percentile(lat_arr, 95))
    total_sec = float(np.sum(lat_arr) / 1000.0)
    throughput = float(len(y_true_idx) / total_sec) if total_sec > 0 else 0.0
    review_rate = float(np.mean(np.asarray(requires_review_flags, dtype=np.float64)))
    auto_rate = float(1.0 - review_rate)

    return {
        "accuracy": round(acc, 4),
        "macro_precision": round(float(prec), 4),
        "macro_recall": round(float(rec), 4),
        "macro_f1": round(float(f1), 4),
        "roc_auc_ovr": round(auc_ovr, 4),
        "latency_mean_ms": round(mean_lat, 3),
        "latency_p95_ms": round(p95_lat, 3),
        "throughput_img_s": round(throughput, 2),
        "hitl_review_rate": round(review_rate, 4),
        "auto_decision_rate": round(auto_rate, 4),
    }


def save_confusion_matrix_png(
    y_true_idx: list[int],
    y_pred_idx: list[int],
    class_names: tuple[str, ...] | list[str],
    out_path: Path,
    title: str = "NEU-DET Matriz de Confusión",
) -> Path:
    """Renderiza matriz de confusión en PNG con backend Agg sin GUI."""
    cm = confusion_matrix(y_true_idx, y_pred_idx, labels=list(range(len(class_names))))
    fig, ax = plt.subplots(figsize=(7.5, 6.2), dpi=150)
    im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    ticks = np.arange(len(class_names))
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(class_names, rotation=30, ha="right", fontsize=8)
    ax.set_yticklabels(class_names, fontsize=8)
    ax.set_ylabel("Clase Real")
    ax.set_xlabel("Clase Predicha")
    ax.set_title(title, fontsize=11, fontweight="bold")

    thresh = cm.max() / 2.0 if cm.max() > 0 else 0.5
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j,
                i,
                format(int(cm[i, j]), "d"),
                ha="center",
                va="center",
                color="white" if cm[i, j] > thresh else "#0f172a",
                fontsize=9,
                fontweight="bold",
            )

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(out_path))
    plt.close(fig)
    return out_path
