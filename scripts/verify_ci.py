"""Verificador local y en CI de puertas QA (>= 120 tests, Ruff, 0 binarios en Git)."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN_SUFFIXES = (".onnx", ".pt", ".pth", ".h5", ".joblib", ".ipynb", ".pkl")


def check_tracked_binaries() -> list[str]:
    out = subprocess.check_output(["git", "ls-files"], cwd=str(REPO_ROOT), text=True)
    bad = []
    for line in out.splitlines():
        if line.endswith(FORBIDDEN_SUFFIXES) or line == ".env":
            bad.append(line)
    return bad


def main() -> None:
    parser = argparse.ArgumentParser(description="Verificador QA CI M3")
    parser.add_argument("--skip-subprocess", action="store_true")
    args = parser.parse_args()

    bad = check_tracked_binaries()
    if bad:
        print(f"ERROR: Archivos prohibidos versionados en Git: {bad}")
        sys.exit(1)

    if not args.skip_subprocess:
        subprocess.check_call(["uv", "run", "ruff", "check", "."], cwd=str(REPO_ROOT))
        subprocess.check_call(
            ["uv", "run", "ruff", "format", "--check", "."], cwd=str(REPO_ROOT)
        )
        res = subprocess.check_output(
            ["uv", "run", "pytest", "-q"], cwd=str(REPO_ROOT), text=True
        )
        m = re.search(r"(\d+)\s+passed", res)
        count = int(m.group(1)) if m else 0
        print(f"Pytest passed count: {count}")
        if count < 120:
            print(f"ERROR: Se requieren >= 120 pruebas pytest, actual={count}")
            sys.exit(1)
    print("[CI VERIFY OK] Cero binarios en Git y puertas QA verificadas.")


if __name__ == "__main__":
    main()
