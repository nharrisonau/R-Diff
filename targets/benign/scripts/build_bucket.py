#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build bucket-specific manifests and pair lists from pairs_binned.csv",
    )
    parser.add_argument(
        "--bucket",
        required=True,
        help="Bucket name (scope) to extract, e.g. major, minor, patch, build, non-semver",
    )
    parser.add_argument(
        "--pairs-binned",
        default="targets/benign/pairs_binned.csv",
        help="Path to pairs_binned.csv",
    )
    parser.add_argument(
        "--manifest",
        default="targets/benign/manifest.csv",
        help="Path to manifest.csv",
    )
    parser.add_argument(
        "--out-dir",
        default="",
        help="Output directory (default: targets/benign/buckets/<bucket>)",
    )
    parser.add_argument(
        "--no-blank-lines",
        action="store_true",
        help="Do not insert blank lines between products in pairs.txt",
    )

    args = parser.parse_args()
    bucket = args.bucket

    pairs_binned_path = Path(args.pairs_binned)
    if not pairs_binned_path.exists():
        print(f"Missing pairs_binned.csv: {pairs_binned_path}")
        return 1

    if args.out_dir:
        out_dir = Path(args.out_dir)
    else:
        repo_root = Path(__file__).resolve().parents[3]
        out_dir = repo_root / "local_outputs" / "benign" / "buckets" / bucket
    out_dir.mkdir(parents=True, exist_ok=True)

    pairs_csv_path = out_dir / "pairs.csv"
    pairs_binned_out = out_dir / "pairs_binned.csv"
    pairs_txt_path = out_dir / "pairs.txt"

    # Read and filter pairs
    filtered_pairs = []
    with pairs_binned_path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        binned_fields = reader.fieldnames or []
        for row in reader:
            if row.get("scope") != bucket:
                continue
            filtered_pairs.append(row)

    if not filtered_pairs:
        print(f"No pairs found for bucket '{bucket}'")
        return 1

    # Write pairs_binned.csv
    with pairs_binned_out.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=binned_fields)
        writer.writeheader()
        writer.writerows(filtered_pairs)

    # Write pairs.csv
    pair_fields = ["product", "prev_version", "next_version", "prev_rootfs", "next_rootfs"]
    with pairs_csv_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=pair_fields)
        writer.writeheader()
        for row in filtered_pairs:
            writer.writerow({k: row.get(k, "") for k in pair_fields})

    # Write pairs.txt
    lines = []
    last_product = None
    for row in filtered_pairs:
        product = (row.get("product") or "").strip()
        prev_version = (row.get("prev_version") or "").strip()
        next_version = (row.get("next_version") or "").strip()
        if not product or not prev_version or not next_version:
            continue
        if not args.no_blank_lines and last_product is not None and product != last_product:
            lines.append("")
        lines.append(f"{product}-{next_version}, {product}-{prev_version}")
        last_product = product
    pairs_txt_path.write_text("\n".join(lines).rstrip() + "\n")

    # Filter manifest to rows referenced by this bucket
    manifest_path = Path(args.manifest)
    if manifest_path.exists():
        with manifest_path.open(newline="") as fh:
            reader = csv.DictReader(fh)
            manifest_rows = list(reader)
            manifest_fields = reader.fieldnames or []

        needed = set()
        for row in filtered_pairs:
            product = (row.get("product") or "").strip()
            prev_version = (row.get("prev_version") or "").strip()
            next_version = (row.get("next_version") or "").strip()
            if product and prev_version:
                needed.add((product, prev_version))
            if product and next_version:
                needed.add((product, next_version))

        out_manifest = out_dir / "manifest.csv"
        with out_manifest.open("w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=manifest_fields)
            writer.writeheader()
            for row in manifest_rows:
                product = (row.get("product") or "").strip()
                version = (row.get("version") or "").strip()
                if (product, version) in needed:
                    writer.writerow(row)

    print(f"Wrote bucket '{bucket}' to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
