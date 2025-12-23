#!/usr/bin/env python3
"""
Validate required model weights are present.

Usage:
  python scripts/check_weights.py
"""

from __future__ import annotations

from pathlib import Path
import os
import sys

REQUIRED_FILES = [
    "hypertension.pt",
    "cimt_reg.pth",
    "vessel.pth",
    "fusion_cvd_notskewed.pth",
]


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    weights_dir = Path(os.getenv("WEIGHTS_DIR", repo_root / "weights"))

    missing = []
    for filename in REQUIRED_FILES:
        path = weights_dir / filename
        if not path.exists():
            missing.append(path)

    if not missing:
        print(f"OK: All required weights found in {weights_dir}")
        return 0

    print("Missing required weight files:")
    for path in missing:
        print(f"- {path}")

    print("\nHow to fix:")
    print("1) Place the files listed above into the weights directory.")
    print("2) If your weights live elsewhere, set WEIGHTS_DIR to that folder.")
    print("   Example (macOS/Linux): WEIGHTS_DIR=/path/to/weights python scripts/check_weights.py")
    print("   Example (PowerShell): $env:WEIGHTS_DIR='C:\\path\\to\\weights'; python scripts/check_weights.py")
    print("\nSee weights/README.md for expected filenames.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
