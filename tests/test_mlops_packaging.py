"""Pruebas AAA para artefactos de reporte y contrato MLflow PyFunc."""

from __future__ import annotations

import json
from pathlib import Path

from defect_inspector.mlops.packaging import (
    NEUDefectPyFunc,
    write_sample_predictions_and_report,
)


def test_write_sample_predictions_and_report_generates_valid_files(
    tmp_path: Path,
) -> None:
    # Arrange & Act
    s_path, r_path = write_sample_predictions_and_report(
        out_dir=tmp_path,
        run_name="run-baseline",
        params={"apply_clahe": False, "conf_threshold": 0.70},
        metrics={"accuracy": 0.95, "latency_p95_ms": 18.4},
        sample_rows=[{"filename": "crazing_1.jpg", "predicted_class": "crazing"}],
    )

    # Assert
    assert callable(NEUDefectPyFunc.predict)
    assert s_path.is_file()
    assert r_path.is_file()
    assert (
        json.loads(s_path.read_text(encoding="utf-8"))[0]["predicted_class"]
        == "crazing"
    )
    assert "run-baseline" in r_path.read_text(encoding="utf-8")
