#!/usr/bin/env python3
"""
Placeholder downloader for model weights.

Fill in the URLs for each weight file and rerun.
"""

from __future__ import annotations

from pathlib import Path
import os
import sys
import urllib.request

WEIGHTS = {
    "hypertension.pt": "",
    "cimt_reg.pth": "",
    "vessel.pth": "",
    "fusion_cvd_notskewed.pth": "",
}


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    weights_dir = Path(os.getenv("WEIGHTS_DIR", repo_root / "weights"))
    weights_dir.mkdir(parents=True, exist_ok=True)

    missing_urls = [name for name, url in WEIGHTS.items() if not url]
    if missing_urls:
        print("Download URLs not configured for:")
        for name in missing_urls:
            print(f"- {name}")
        print("\nEdit scripts/download_weights.py to add URLs, or place files manually.")
        return 1

    for name, url in WEIGHTS.items():
        dest = weights_dir / name
        if dest.exists():
            print(f"Skipping existing {dest}")
            continue
        print(f"Downloading {name}...")
        urllib.request.urlretrieve(url, dest)
        print(f"Saved to {dest}")

    print("All downloads complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
