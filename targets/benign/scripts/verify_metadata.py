#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ALLOWED_SCOPES = {"major", "minor", "patch", "build", "other"}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify benign metadata consistency between manifest, pairs, and pairs_binned.",
    )
    parser.add_argument("--manifest", default="targets/benign/manifest.csv")
    parser.add_argument("--pairs", default="targets/benign/pairs.csv")
    parser.add_argument("--pairs-binned", default="targets/benign/pairs_binned.csv")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    pairs_path = Path(args.pairs)
    pairs_binned_path = Path(args.pairs_binned)

    for path in [manifest_path, pairs_path, pairs_binned_path]:
        if not path.exists():
            print(f"missing required file: {path}")
            return 2

    manifest_rows = _read_csv(manifest_path)
    pairs_rows = _read_csv(pairs_path)
    binned_rows = _read_csv(pairs_binned_path)

    errors: list[str] = []

    manifest_versions = {
        ((row.get("product") or "").strip(), (row.get("version") or "").strip())
        for row in manifest_rows
    }

    pair_keys: list[tuple[str, str, str]] = []
    for row in pairs_rows:
        product = (row.get("product") or "").strip()
        prev_version = (row.get("prev_version") or "").strip()
        next_version = (row.get("next_version") or "").strip()
        if not product or not prev_version or not next_version:
            errors.append(f"pairs.csv row missing product/version fields: {row}")
            continue
        pair_keys.append((product, prev_version, next_version))
        if (product, prev_version) not in manifest_versions:
            errors.append(
                f"pairs.csv references missing prev manifest row: {product} {prev_version}"
            )
        if (product, next_version) not in manifest_versions:
            errors.append(
                f"pairs.csv references missing next manifest row: {product} {next_version}"
            )

    binned_keys: list[tuple[str, str, str]] = []
    for row in binned_rows:
        product = (row.get("product") or "").strip()
        prev_version = (row.get("prev_version") or "").strip()
        next_version = (row.get("next_version") or "").strip()
        scope = (row.get("scope") or "").strip()
        if not product or not prev_version or not next_version:
            errors.append(f"pairs_binned.csv row missing product/version fields: {row}")
            continue
        binned_keys.append((product, prev_version, next_version))
        if scope not in ALLOWED_SCOPES:
            errors.append(f"invalid scope '{scope}' in pairs_binned.csv for {product}")

    if len(pairs_rows) != len(binned_rows):
        errors.append(
            f"pairs and pairs_binned row count mismatch: {len(pairs_rows)} != {len(binned_rows)}"
        )

    if sorted(pair_keys) != sorted(binned_keys):
        errors.append("pairs.csv and pairs_binned.csv do not contain identical pair keys")

    if errors:
        print("benign metadata verification failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print(
        "verified benign metadata:",
        f"{len(manifest_rows)} manifest rows,",
        f"{len(pairs_rows)} pair rows,",
        f"{len(binned_rows)} binned rows",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
