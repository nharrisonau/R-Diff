#!/usr/bin/env python3
"""
Deprecated entrypoint.

Use targets/benign/scripts/ingest_firmware_dataset.py instead.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Deprecated: use targets/benign/scripts/ingest_firmware_dataset.py",
    )
    parser.add_argument("firmware_data_path_or_dir")
    parser.add_argument("save_path")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    ingest = repo_root / "targets" / "benign" / "scripts" / "ingest_firmware_dataset.py"
    print(
        "DEPRECATED: dataset_II/download.py is retired. "
        "Forwarding to targets/benign/scripts/ingest_firmware_dataset.py.",
        file=sys.stderr,
    )

    cmd = [
        sys.executable,
        str(ingest),
        "--products-dir",
        args.firmware_data_path_or_dir,
        "--out-root",
        args.save_path,
    ]
    proc = subprocess.run(cmd, check=False)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
