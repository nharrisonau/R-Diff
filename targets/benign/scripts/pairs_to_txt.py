#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render pairs.csv as a simple text list: <product>-<next>, <product>-<prev>",
    )
    parser.add_argument(
        "--pairs",
        default="targets/benign/pairs.csv",
        help="Path to pairs.csv",
    )
    parser.add_argument(
        "--out",
        default="targets/benign/pairs.txt",
        help="Path to write the text list",
    )
    parser.add_argument(
        "--no-blank-lines",
        action="store_true",
        help="Do not insert blank lines between products",
    )

    args = parser.parse_args()
    pairs_path = Path(args.pairs)
    if not pairs_path.exists():
        print(f"Missing pairs.csv: {pairs_path}")
        return 1

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    last_product = None

    with pairs_path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            product = row.get("product", "").strip()
            prev_version = row.get("prev_version", "").strip()
            next_version = row.get("next_version", "").strip()
            if not product or not prev_version or not next_version:
                continue

            if not args.no_blank_lines and last_product is not None and product != last_product:
                lines.append("")

            lines.append(f"{product}-{next_version}, {product}-{prev_version}")
            last_product = product

    out_path.write_text("\n".join(lines).rstrip() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
