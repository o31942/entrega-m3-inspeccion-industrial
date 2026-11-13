"""Pruebas iniciales de bootstrap, versión del paquete y trazabilidad SDD."""

from __future__ import annotations

from pathlib import Path

import defect_inspector


def test_package_version_is_defined() -> None:
    # Arrange & Act
    version = defect_inspector.__version__

    # Assert
    assert isinstance(version, str)
    assert version == "0.1.0"


def test_required_sdd_specs_and_proto_exist() -> None:
    # Arrange
    root = Path(__file__).resolve().parent.parent

    # Act & Assert
    assert (root / "protos" / "defect_inspection.proto").is_file()
    assert (root / "docs" / "model-card.md").is_file()
    assert (root / "docs" / "arquitectura.html").is_file()
    assert (root / "specs" / "SPEC-001-repo-gitflow" / "spec.md").is_file()
    assert (root / "specs" / "SPEC-002-proto-contract" / "spec.md").is_file()
