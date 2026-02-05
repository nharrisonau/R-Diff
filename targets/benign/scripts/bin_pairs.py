#!/usr/bin/env python3
import argparse
import csv
import re
from pathlib import Path

SCOPE_ORDER = [
    "major",
    "minor",
    "patch",
    "build",
    "other",
]

SEMVERISH_RE = re.compile(r"^\d+(?:\.\d+)+$")
DOTTED3PLUS_RE = re.compile(r"^\d+(?:\.\d+){2,}$")
ARCH_VERSION_RE = re.compile(r"^(\d+(?:\.\d+)+)-([A-Za-z0-9]+)$")

def tokenize_version(value: str):
    return [int(x) for x in re.findall(r"\d+", value or "")]


def version_scope(prev: str, nxt: str) -> str:
    a = tokenize_version(prev)
    b = tokenize_version(nxt)
    if not a or not b:
        return "unknown"

    idx = None
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            idx = i
            break
    if idx is None:
        if len(a) != len(b):
            idx = min(len(a), len(b))
        else:
            return "unknown"

    if idx == 0:
        return "major"
    if idx == 1:
        return "minor"
    if idx == 2:
        return "patch"
    return "build"


def split_arch_suffix(value: str) -> tuple[str, str | None]:
    if not value:
        return "", None
    match = ARCH_VERSION_RE.match(value.strip())
    if not match:
        return value.strip(), None
    return match.group(1), match.group(2)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bin benign pairs by update scope (major/minor/patch/build/other)",
    )
    parser.add_argument(
        "--pairs",
        default="targets/benign/pairs.csv",
        help="Path to pairs.csv",
    )
    parser.add_argument(
        "--out",
        default="targets/benign/pairs_binned.csv",
        help="Path to write binned CSV",
    )
    parser.add_argument(
        "--out-txt",
        default="targets/benign/pairs_binned.txt",
        help="Path to write binned text list",
    )
    parser.add_argument(
        "--bins-dir",
        default="targets/benign/bins",
        help="Directory to write per-scope text files",
    )
    parser.add_argument(
        "--no-blank-lines",
        action="store_true",
        help="Do not insert blank lines between products in text outputs",
    )

    args = parser.parse_args()

    pairs_path = Path(args.pairs)
    if not pairs_path.exists():
        print(f"Missing pairs.csv: {pairs_path}")
        return 1

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    bins_dir = Path(args.bins_dir)
    bins_dir.mkdir(parents=True, exist_ok=True)

    bin_lines = {name: [] for name in SCOPE_ORDER}

    with pairs_path.open(newline="") as fh_in, out_path.open("w", newline="") as fh_out:
        reader = csv.DictReader(fh_in)
        fieldnames = [
            "product",
            "prev_version",
            "next_version",
            "prev_rootfs",
            "next_rootfs",
            "version_scope",
            "scope",
            "scope_reason",
        ]
        writer = csv.DictWriter(fh_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            product = (row.get("product") or "").strip()
            prev_version = (row.get("prev_version") or "").strip()
            next_version = (row.get("next_version") or "").strip()
            if not product or not prev_version or not next_version:
                continue

            prev_base, prev_arch = split_arch_suffix(prev_version)
            next_base, next_arch = split_arch_suffix(next_version)
            cross_arch = prev_arch and next_arch and prev_arch != next_arch
            same_arch = prev_arch and next_arch and prev_arch == next_arch

            prev_for_scope = prev_base if same_arch else prev_version
            next_for_scope = next_base if same_arch else next_version

            prev_semver = bool(SEMVERISH_RE.match(prev_for_scope))
            next_semver = bool(SEMVERISH_RE.match(next_for_scope))
            prev_dotted3 = bool(DOTTED3PLUS_RE.match(prev_for_scope))
            next_dotted3 = bool(DOTTED3PLUS_RE.match(next_for_scope))
            if prev_semver and next_semver:
                v_scope = version_scope(prev_for_scope, next_for_scope)
            else:
                v_scope = "unknown"

            if cross_arch:
                scope = "other"
                scope_reason = "arch-diff"
            elif prev_dotted3 or next_dotted3:
                if v_scope != "unknown":
                    scope = v_scope
                    scope_reason = "dotted3+"
                else:
                    scope = "other"
                    scope_reason = "dotted3+-fallback"
            elif not (prev_semver and next_semver):
                scope = "other"
                scope_reason = "non-semver"
            else:
                if v_scope != "unknown":
                    scope = v_scope
                    scope_reason = "version-tokens"
                else:
                    scope = "other"
                    scope_reason = "version-unknown"

            if scope not in {"major", "minor", "patch", "build"}:
                scope = "other"

            writer.writerow(
                {
                    "product": product,
                    "prev_version": prev_version,
                    "next_version": next_version,
                    "prev_rootfs": row.get("prev_rootfs", ""),
                    "next_rootfs": row.get("next_rootfs", ""),
                    "version_scope": v_scope,
                    "scope": scope,
                    "scope_reason": scope_reason,
                }
            )

            line = f"{product}-{next_version}, {product}-{prev_version}"
            bin_lines.setdefault(scope, []).append(line)

    # write master text list grouped by scope
    out_txt = Path(args.out_txt)
    lines = []
    for scope in SCOPE_ORDER:
        entries = bin_lines.get(scope, [])
        if not entries:
            continue
        if lines:
            lines.append("")
        lines.append(f"[{scope}]")
        lines.extend(entries)
    out_txt.write_text("\n".join(lines).rstrip() + "\n")

    # write per-scope files
    for scope, entries in bin_lines.items():
        if not entries:
            continue
        scope_path = bins_dir / f"{scope}.txt"
        if args.no_blank_lines:
            scope_path.write_text("\n".join(entries).rstrip() + "\n")
        else:
            scope_path.write_text("\n\n".join(entries).rstrip() + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
