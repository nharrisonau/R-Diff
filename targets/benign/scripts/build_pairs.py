#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
from pathlib import Path

DATE_FORMATS = [
    "%Y-%m-%d",
    "%m/%d/%y",
    "%m/%d/%Y",
    "%d/%m/%Y",
]


def parse_date(value: str):
    if not value:
        return None
    raw = value.strip()
    for fmt in DATE_FORMATS:
        try:
            return dt.datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def sort_key(entry: dict):
    date_val = parse_date(entry.get("date", ""))
    if date_val is not None:
        return (0, date_val, entry.get("version", ""))
    return (1, entry.get("version", ""))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build pairs.csv from manifest.csv for benign diff evaluation",
    )
    parser.add_argument(
        "--manifest",
        default="targets/benign/manifest.csv",
        help="Path to manifest.csv",
    )
    parser.add_argument(
        "--out",
        default="targets/benign/pairs.csv",
        help="Path to write pairs.csv",
    )

    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"Missing manifest: {manifest_path}")
        return 1

    with manifest_path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        rows = [row for row in reader if row.get("rootfs_path")]

    by_product: dict[str, list[dict]] = {}
    for row in rows:
        product = row.get("product") or "unknown"
        by_product.setdefault(product, []).append(row)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as fh:
        fieldnames = [
            "product",
            "prev_version",
            "next_version",
            "prev_rootfs",
            "next_rootfs",
        ]
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()

        for product, entries in sorted(by_product.items()):
            entries.sort(key=sort_key)
            for prev, nxt in zip(entries, entries[1:]):
                writer.writerow(
                    {
                        "product": product,
                        "prev_version": prev.get("version", ""),
                        "next_version": nxt.get("version", ""),
                        "prev_rootfs": prev.get("rootfs_path", ""),
                        "next_rootfs": nxt.get("rootfs_path", ""),
                    }
                )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
