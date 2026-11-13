"""Pruebas AAA para lote reproducible de evaluación estratificada."""

from __future__ import annotations

from pathlib import Path

from defect_inspector.inference.config import NEU_CLASSES
from defect_inspector.mlops.eval_data import (
    generate_synthetic_eval_batch,
    load_reproducible_eval_batch,
)


def test_synthetic_eval_batch_is_balanced_and_deterministic() -> None:
    # Arrange & Act
    batch_a, src_a = generate_synthetic_eval_batch(per_class=4, seed=7)
    batch_b, src_b = generate_synthetic_eval_batch(per_class=4, seed=7)

    # Assert
    assert src_a == src_b == "synthetic-deterministic-fallback"
    assert len(batch_a) == 24
    assert [s.sample_id for s in batch_a] == [s.sample_id for s in batch_b]
    counts = {c: sum(1 for s in batch_a if s.true_label == c) for c in NEU_CLASSES}
    assert all(cnt == 4 for cnt in counts.values())


def test_load_eval_batch_uses_offline_fallback_without_network(tmp_path: Path) -> None:
    # Arrange & Act
    samples, source = load_reproducible_eval_batch(
        cache_dir=tmp_path / "missing", per_class=2, allow_download=False
    )

    # Assert
    assert len(samples) == 12
    assert source == "synthetic-deterministic-fallback"
