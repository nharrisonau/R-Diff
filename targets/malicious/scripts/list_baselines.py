#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

try:
    # When imported as a package module.
    from .versioning import extract_versions_from_tags, parse_version
except ImportError:  # pragma: no cover
    # When executed as a script (python3 list_baselines.py).
    from versioning import extract_versions_from_tags, parse_version


def list_baselines(
    *,
    repo: Path,
    tag_patterns: list[str],
    version_scheme: str,
    current_version: str,
    major_token_index: int,
    include_prerelease: bool,
    min_version: str | None = None,
    exclude_versions: set[str] | None = None,
) -> list[tuple[str, str]]:
    patterns = [re.compile(p) for p in tag_patterns]
    proc = subprocess.run(
        ["git", "-C", str(repo), "tag", "--list"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git tag failed in {repo}")
    tags = [line.strip() for line in proc.stdout.splitlines() if line.strip()]

    versions = extract_versions_from_tags(tags, patterns, version_scheme)
    cur = parse_version(current_version, version_scheme)
    cur_major = cur.major_token(major_token_index)
    if cur_major is None:
        raise ValueError(f"current_version has no major token @{major_token_index}: {current_version!r}")

    min_parsed = parse_version(min_version, version_scheme) if min_version else None
    excluded = exclude_versions or set()

    selected: list[tuple[str, str]] = []
    for ver, tag in versions.items():
        if ver in excluded:
            continue
        pv = parse_version(ver, version_scheme)
        if not include_prerelease and pv.is_prerelease:
            continue
        major = pv.major_token(major_token_index)
        if major != cur_major:
            continue
        if pv.key > cur.key:
            continue
        if pv.key == cur.key:
            continue
        if min_parsed is not None and pv.key < min_parsed.key:
            continue
        selected.append((ver, tag))

    selected.sort(key=lambda x: parse_version(x[0], version_scheme).key, reverse=True)
    return selected


def main() -> int:
    ap = argparse.ArgumentParser(description="List baseline versions from git tags.")
    ap.add_argument("--repo", required=True, help="Path to upstream git repo")
    ap.add_argument("--current-version", required=True)
    ap.add_argument("--scheme", required=True, help="Version scheme (semver/openssl/sudo/dropbear_year)")
    ap.add_argument(
        "--tag-pattern",
        action="append",
        default=[],
        help="Regex with named capture group 'version' (repeatable)",
    )
    ap.add_argument("--major-token-index", type=int, default=0)
    ap.add_argument("--include-prerelease", action="store_true")
    ap.add_argument("--min-version", default="")
    ap.add_argument(
        "--exclude-version",
        action="append",
        default=[],
        help="Version to exclude from baseline candidates (repeatable)",
    )
    ap.add_argument("--format", choices=["jsonl", "csv"], default="jsonl")

    args = ap.parse_args()
    repo = Path(args.repo)
    if not repo.exists():
        raise SystemExit(f"Missing repo: {repo}")
    if not args.tag_pattern:
        raise SystemExit("Need at least one --tag-pattern")

    baselines = list_baselines(
        repo=repo,
        tag_patterns=args.tag_pattern,
        version_scheme=args.scheme,
        current_version=args.current_version,
        major_token_index=args.major_token_index,
        include_prerelease=args.include_prerelease,
        min_version=(args.min_version or None),
        exclude_versions=set(args.exclude_version or []),
    )

    if args.format == "csv":
        print("baseline_version,baseline_tag")
        for ver, tag in baselines:
            print(f"{ver},{tag}")
    else:
        for ver, tag in baselines:
            print(json.dumps({"baseline_version": ver, "baseline_tag": tag}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
