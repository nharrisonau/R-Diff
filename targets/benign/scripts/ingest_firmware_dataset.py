#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import os
import re
import shutil
import subprocess
import urllib.request
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

PREFERRED_ROOT_NAMES = [
    "squashfs-root",
    "rootfs",
    "ext-root",
    "root",
    "fs",
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


def download_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(url) as response, tmp.open("wb") as fh:
        shutil.copyfileobj(response, fh)
    tmp.replace(dest)


def run_binwalk(fw_path: Path, extract_dir: Path) -> None:
    extract_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "binwalk",
            "-Mre",
            "--directory",
            str(extract_dir),
            str(fw_path),
        ],
        check=False,
    )


def find_rootfs_dir(search_root: Path) -> Path | None:
    candidates = []
    for dirpath, dirnames, _ in os.walk(search_root):
        name = os.path.basename(dirpath)
        score = 0
        if name in PREFERRED_ROOT_NAMES:
            score += 3
        if os.path.isdir(os.path.join(dirpath, "etc")):
            score += 2
        if os.path.isdir(os.path.join(dirpath, "bin")):
            score += 1
        if score > 0:
            candidates.append((score, Path(dirpath)))
    if not candidates:
        return None
    candidates.sort(key=lambda item: (-item[0], str(item[1])))
    return candidates[0][1]


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


def ingest_csv(
    csv_path: Path,
    out_root: Path,
    cache_root: Path,
    manifest: Path,
    overwrite: bool,
    repo_root: Path,
) -> None:
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

        dest_rootfs = out_root / product / version / "rootfs"
        if dest_rootfs.exists() and not overwrite:
            continue

        filename = url.rsplit("/", 1)[-1] or f"{product}-{version}.bin"
        download_dir = cache_root / product / version / "downloads"
        extract_dir = cache_root / product / version / "extracted"
        fw_path = download_dir / filename

        try:
            download_file(url, fw_path)
        except Exception as exc:
            append_manifest(
                manifest,
                {
                    "dataset": "benign",
                    "product": product,
                    "version": version,
                    "date": date_str,
                    "url": url,
                    "rootfs_path": "",
                    "notes": f"download failed: {exc}",
                },
            )
            continue

        run_binwalk(fw_path, extract_dir)
        rootfs_dir = find_rootfs_dir(extract_dir)
        if rootfs_dir is None:
            append_manifest(
                manifest,
                {
                    "dataset": "benign",
                    "product": product,
                    "version": version,
                    "date": date_str,
                    "url": url,
                    "rootfs_path": "",
                    "notes": "rootfs not found",
                },
            )
            continue

        if dest_rootfs.exists():
            shutil.rmtree(dest_rootfs)
        dest_rootfs.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(rootfs_dir, dest_rootfs, symlinks=True)

        append_manifest(
            manifest,
            {
                "dataset": "benign",
                "product": product,
                "version": version,
                "date": date_str,
                "url": url,
                "rootfs_path": relpath_or_abs(dest_rootfs, repo_root),
                "notes": "",
            },
        )


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    benign_root = script_dir.parent
    repo_root = benign_root.parent.parent
    default_out_root = repo_root / "local_outputs" / "benign"

    if shutil.which("binwalk") is None:
        print("Missing dependency: binwalk")
        print("Install options:")
        print("  - Ubuntu/Debian: sudo apt-get install -y binwalk")
        print("  - macOS (Homebrew): brew install binwalk")
        print("  - Python/pipx: pipx install binwalk")
        print("Then re-run this script.")
        return 1

    parser = argparse.ArgumentParser(
        description=(
            "Ingest benign firmware URL CSVs into --out-root/<product>/<version>/rootfs "
            "(default out-root: local_outputs/benign)"
        ),
    )
    parser.add_argument(
        "--products-dir",
        default=str(benign_root / "sources" / "firmware-dataset" / "dataset_II" / "products"),
        help="Directory containing benign firmware URL CSV files",
    )
    parser.add_argument(
        "--manifest-in",
        default="",
        help=(
            "Manifest CSV to ingest instead of products dir "
            "(e.g., local_outputs/benign/buckets/<bucket>/manifest.csv)"
        ),
    )
    parser.add_argument(
        "--out-root",
        default=str(default_out_root),
        help="Root directory for extracted benign rootfs outputs",
    )
    parser.add_argument(
        "--cache-dir",
        default=str(default_out_root / ".cache" / "firmware-dataset"),
        help="Cache directory for downloads and extraction",
    )
    parser.add_argument(
        "--manifest",
        default=str(default_out_root / "manifest.csv"),
        help="Manifest CSV to append to",
    )
    parser.add_argument(
        "--overwrite-manifest",
        action="store_true",
        help="Overwrite the output manifest before writing",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing rootfs directories",
    )

    args = parser.parse_args()

    out_root = Path(args.out_root)
    cache_root = Path(args.cache_dir)
    manifest = Path(args.manifest)

    if args.overwrite_manifest:
        manifest.unlink(missing_ok=True)

    if args.manifest_in:
        manifest_in = Path(args.manifest_in)
        if not manifest_in.exists():
            print(f"Missing manifest input: {manifest_in}")
            return 1
        ingest_manifest(
            manifest_in,
            out_root,
            cache_root,
            manifest,
            args.overwrite,
            repo_root,
        )
        return 0

    products_dir = Path(args.products_dir)
    if not products_dir.exists():
        print(f"Missing products dir: {products_dir}")
        return 1

    csv_files = sorted(products_dir.rglob("*.csv"))
    if not csv_files:
        print(f"No CSV files found under {products_dir}")
        return 1

    for csv_path in csv_files:
        ingest_csv(
            csv_path,
            out_root,
            cache_root,
            manifest,
            args.overwrite,
            repo_root,
        )

    return 0


def ingest_manifest(
    manifest_in: Path,
    out_root: Path,
    cache_root: Path,
    manifest_out: Path,
    overwrite: bool,
    repo_root: Path,
) -> None:
    with manifest_in.open(newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    for row in rows:
        url = (row.get("url") or "").strip()
        if not url:
            continue

        product = sanitize(row.get("product") or "")
        version = sanitize(row.get("version") or "")
        if not product or not version:
            continue

        date_str = parse_date(row.get("date") or "")
        dataset = (row.get("dataset") or "benign").strip() or "benign"

        dest_rootfs = out_root / product / version / "rootfs"
        if dest_rootfs.exists() and not overwrite:
            continue

        filename = url.rsplit("/", 1)[-1] or f"{product}-{version}.bin"
        download_dir = cache_root / product / version / "downloads"
        extract_dir = cache_root / product / version / "extracted"
        fw_path = download_dir / filename

        try:
            download_file(url, fw_path)
        except Exception as exc:
            append_manifest(
                manifest_out,
                {
                    "dataset": dataset,
                    "product": product,
                    "version": version,
                    "date": date_str,
                    "url": url,
                    "rootfs_path": "",
                    "notes": f"download failed: {exc}",
                },
            )
            continue

        run_binwalk(fw_path, extract_dir)
        rootfs_dir = find_rootfs_dir(extract_dir)
        if rootfs_dir is None:
            append_manifest(
                manifest_out,
                {
                    "dataset": dataset,
                    "product": product,
                    "version": version,
                    "date": date_str,
                    "url": url,
                    "rootfs_path": "",
                    "notes": "rootfs not found",
                },
            )
            continue

        if dest_rootfs.exists():
            shutil.rmtree(dest_rootfs)
        dest_rootfs.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(rootfs_dir, dest_rootfs, symlinks=True)

        append_manifest(
            manifest_out,
            {
                "dataset": dataset,
                "product": product,
                "version": version,
                "date": date_str,
                "url": url,
                "rootfs_path": relpath_or_abs(dest_rootfs, repo_root),
                "notes": "",
            },
        )


if __name__ == "__main__":
    raise SystemExit(main())
