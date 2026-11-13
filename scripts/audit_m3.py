"""Auditor automatizado de cumplimiento cuantitativo Anuncio 007 (Módulo 3)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def audit_repository(run_subprocesses: bool = True) -> dict[str, object]:
    """Recopila conteos reales del repositorio para verificar requisitos M3."""
    specs = sorted(
        p
        for p in (REPO_ROOT / "specs").glob("SPEC-*")
        if (p / "spec.md").is_file()
        and (p / "plan.md").is_file()
        and (p / "tasks.md").is_file()
    )
    tests_collected = 0
    ruff_ok = True
    if run_subprocesses:
        collect = subprocess.run(
            ["uv", "run", "--offline", "pytest", "--collect-only"],
            cwd=str(REPO_ROOT),
            text=True,
            capture_output=True,
        )
        m = re.search(r"(\d+)\s+tests?\s+collected", collect.stdout)
        if m:
            tests_collected = int(m.group(1))
        else:
            node_lines = [ln for ln in collect.stdout.splitlines() if "::" in ln]
            if node_lines:
                tests_collected = len(node_lines)
            else:
                tests_collected = sum(
                    int(n)
                    for n in re.findall(
                        r"^tests/.*?:\s*(\d+)\s*$", collect.stdout, re.MULTILINE
                    )
                )

        ruff_res = subprocess.run(
            ["uv", "run", "--offline", "ruff", "check", "."],
            cwd=str(REPO_ROOT),
            text=True,
            capture_output=True,
        )
        ruff_ok = ruff_res.returncode == 0

    required_files = [
        "LICENSE",
        "README.md",
        "Dockerfile",
        "protos/defect_inspection.proto",
        "docs/model-card.md",
        "docs/arquitectura.html",
        "docs/adr-001-grpc-gateway.md",
        "frontend/index.html",
        "frontend/js/app.js",
        "scripts/evaluar.py",
    ]
    missing = [f for f in required_files if not (REPO_ROOT / f).is_file()]
    return {
        "specs_complete": len(specs),
        "tests_collected": tests_collected,
        "ruff_ok": ruff_ok,
        "missing_files": missing,
    }


def main() -> None:
    report = audit_repository()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if (
        report["specs_complete"] < 40
        or report["tests_collected"] < 120
        or not report["ruff_ok"]
        or report["missing_files"]
    ):
        sys.exit(1)


if __name__ == "__main__":
    main()
