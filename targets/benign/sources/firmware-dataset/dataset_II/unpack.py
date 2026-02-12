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
    parser.add_argument("path")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    ingest = repo_root / "targets" / "benign" / "scripts" / "ingest_firmware_dataset.py"
    print(
        "DEPRECATED: dataset_II/unpack.py is retired. "
        "Use targets/benign/scripts/ingest_firmware_dataset.py for supported ingestion.",
        file=sys.stderr,
    )

    # Keep compatibility by forwarding to ingest with no downloads and overwrite of manifest only.
    cmd = [
        sys.executable,
        str(ingest),
        "--products-dir",
        args.path,
    ]
    proc = subprocess.run(cmd, check=False)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
