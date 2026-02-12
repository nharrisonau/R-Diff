#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

MANIFEST_FIELDS = [
    "dataset",
    "product",
    "version",
    "date",
    "url",
    "rootfs_path",
    "notes",
]

DATE_FORMATS = [
    "%Y-%m-%d",
    "%m/%d/%y",
    "%m/%d/%Y",
    "%d/%m/%Y",
]


def ensure_manifest(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()


def append_manifest(path: Path, row: dict) -> None:
    ensure_manifest(path)
    with path.open("a", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS)
        writer.writerow({k: row.get(k, "") for k in MANIFEST_FIELDS})


def sanitize(value: str, fallback: str = "unknown") -> str:
    if not value:
        return fallback
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    cleaned = cleaned.strip("._-")
    return cleaned or fallback


def parse_date(value: str) -> str:
    if not value:
        return ""
    raw = value.strip()
    for fmt in DATE_FORMATS:
        try:
            return dt.datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return raw


def extract_version(row: dict, url: str, fallback: str) -> str:
    version = (row.get("version") or "").strip()
    if version and version.lower() != "unknown":
        return version
    matches = re.findall(r"\d+\.\d+\.\d+(?:\.\d+)?", url or "")
    if matches:
        return matches[-1]
    return fallback


def unique_version(base_version: str, used: set[str]) -> str:
    if base_version not in used:
        used.add(base_version)
        return base_version
    idx = 2
    while f"{base_version}__{idx}" in used:
        idx += 1
    version = f"{base_version}__{idx}"
    used.add(version)
    return version


def relpath_or_abs(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def add_firmware_dataset_entries(products_dir: Path, out_root: Path, repo_root: Path, manifest: Path) -> None:
    csv_files = sorted(products_dir.rglob("*.csv"))
    for csv_path in csv_files:
        with csv_path.open(newline="") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)

        product_fallback = sanitize(csv_path.stem)
        used_versions: set[str] = set()

        for row in rows:
            url = (row.get("url") or "").strip()
            if not url:
                continue
            vendor = sanitize(row.get("vendor") or "")
            product_base = sanitize(row.get("product") or product_fallback)
            if vendor and vendor not in {"unknown", "others"}:
                product = f"{vendor}-{product_base}"
            else:
                product = product_base

            date_str = parse_date(row.get("date") or "")
            fallback_version = sanitize(date_str or "unknown")
            version_raw = extract_version(row, url, fallback_version)
            version = sanitize(version_raw)
            version = unique_version(version, used_versions)

            rootfs = out_root / product / version / "rootfs"
            append_manifest(
                manifest,
                {
                    "dataset": "benign",
                    "product": product,
                    "version": version,
                    "date": date_str,
                    "url": url,
                    "rootfs_path": relpath_or_abs(rootfs, repo_root),
                    "notes": "planned (no download)",
                },
            )


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    benign_root = script_dir.parent
    repo_root = benign_root.parent.parent

    parser = argparse.ArgumentParser(
        description="Generate benign manifest/pairs from source scripts without downloading firmware",
    )
    parser.add_argument(
        "--products-dir",
        default=str(benign_root / "sources" / "firmware-dataset" / "dataset_II" / "products"),
        help="Directory containing benign firmware URL CSV files",
    )
    parser.add_argument(
        "--out-root",
        default=str(benign_root),
        help="Root directory for targets/benign",
    )
    parser.add_argument(
        "--manifest",
        default=str(benign_root / "manifest.csv"),
        help="Manifest CSV to write",
    )
    parser.add_argument(
        "--pairs",
        default=str(benign_root / "pairs.csv"),
        help="Pairs CSV to write",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite manifest/pairs before writing",
    )
    parser.add_argument(
        "--skip-pairs",
        action="store_true",
        help="Skip generating pairs.csv",
    )

    args = parser.parse_args()

    products_dir = Path(args.products_dir)
    if not products_dir.exists():
        print(f"Missing products dir: {products_dir}")
        return 1

    manifest = Path(args.manifest)
    pairs = Path(args.pairs)

    if args.overwrite:
        manifest.unlink(missing_ok=True)
        pairs.unlink(missing_ok=True)

    out_root = Path(args.out_root)

    add_firmware_dataset_entries(products_dir, out_root, repo_root, manifest)
    if not args.skip_pairs:
        build_pairs = script_dir / "build_pairs.py"
        subprocess.run([
            sys.executable,
            str(build_pairs),
            "--manifest",
            str(manifest),
            "--out",
            str(pairs),
        ], check=False)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
