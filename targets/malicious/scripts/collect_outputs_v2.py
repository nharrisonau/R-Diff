#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, cast

REPORT_FIELDS = [
    "group",
    "target_dir",
    "current_version",
    "collected_baseline_count",
    "collected_baseline_versions",
    "failed_baseline_count",
    "failed_baseline_versions",
    "failed_details",
]
MAKE_DIR_LINE_RE = re.compile(r"^make(?:\[\d+\])?: (?:Entering|Leaving) directory .*$")


def _repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def _is_make_dir_line(line: str) -> bool:
    return bool(MAKE_DIR_LINE_RE.match(line.strip()))


def _run_make_print(target_dir: Path, target: str) -> str:
    proc = subprocess.run(
        ["make", "--no-print-directory", "-s", "-C", str(target_dir), target],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or f"make {target} failed")
    lines = [line.strip() for line in (proc.stdout + "\n" + proc.stderr).splitlines()]
    candidates = [line for line in lines if line and not _is_make_dir_line(line)]
    if candidates:
        return candidates[-1]
    if proc.stdout.strip():
        return proc.stdout.strip().splitlines()[-1].strip()
    raise RuntimeError(f"make {target} produced no output")


def _is_elf(path: Path) -> bool:
    proc = subprocess.run(["file", "-b", str(path)], capture_output=True, text=True, check=False)
    return proc.returncode == 0 and proc.stdout.startswith("ELF ")


def _maybe_strip(path: Path, strip_tool: str, strip_flags: list[str]) -> None:
    if not _is_elf(path):
        return
    subprocess.run([strip_tool, *strip_flags, str(path)], check=False)


def _copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _append_unique(values: list[str], value: str) -> None:
    if value and value not in values:
        values.append(value)


def _new_report_row(group: str, target_dir: str, current_version: str) -> dict[str, Any]:
    return {
        "group": group,
        "target_dir": target_dir,
        "current_version": current_version,
        "collected_baseline_versions": [],
        "failed_baseline_versions": [],
        "failed_details": [],
    }


def _record_failed_baseline(report_row: dict[str, Any], baseline_version: str, error: str) -> None:
    version = baseline_version.strip() or "(unspecified)"
    detail = f"{version}: {error.strip()}" if error.strip() else version
    failed_versions = cast(list[str], report_row["failed_baseline_versions"])
    failed_details = cast(list[str], report_row["failed_details"])
    _append_unique(failed_versions, version)
    _append_unique(failed_details, detail)


def main() -> int:
    repo_root = _repo_root_from_script()

    ap = argparse.ArgumentParser(description="Collect outputs into outputs/v2/{normal,stripped}.")
    ap.add_argument("--repo-root", default=str(repo_root), help="Repo root (default: auto-detected)")
    ap.add_argument(
        "--out-base",
        default="",
        help="Output base directory (default: <repo-root>/outputs)",
    )
    ap.add_argument(
        "--config",
        default="",
        help="Path to baselines_config.json (default: targets/malicious/baselines_config.json)",
    )
    ap.add_argument(
        "--baselines",
        default="",
        help="Path to baselines.csv (default: local_outputs/malicious/baselines.csv)",
    )
    ap.add_argument(
        "--report",
        default="",
        help="Path to malicious baseline report CSV (default: <out-base>/v2/reports/malicious_baselines_report.csv)",
    )
    ap.add_argument("--strip-tool", default=os.environ.get("STRIP_TOOL", "strip"))
    ap.add_argument(
        "--strip-flag",
        action="append",
        default=[],
        help="Repeatable strip flags (default: --strip-unneeded)",
    )
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    out_base = Path(args.out_base).resolve() if args.out_base else (repo_root / "outputs")
    config_path = Path(args.config).resolve() if args.config else (repo_root / "targets" / "malicious" / "baselines_config.json")
    baselines_path = (
        Path(args.baselines).resolve()
        if args.baselines
        else (repo_root / "local_outputs" / "malicious" / "baselines.csv")
    )
    report_path = (
        Path(args.report).resolve()
        if args.report
        else (out_base / "v2" / "reports" / "malicious_baselines_report.csv")
    )

    strip_flags = args.strip_flag or ["--strip-unneeded"]

    if not config_path.exists():
        print(f"Missing config: {config_path}")
        return 1

    entries = json.loads(config_path.read_text())

    report_by_target: dict[tuple[str, str], dict[str, Any]] = {}
    for entry in entries:
        rel = entry["path"]
        group = entry["group"]
        target_name = Path(rel).name
        current_version = (entry.get("current_version") or "").strip()
        report_by_target[(group, target_name)] = _new_report_row(group, target_name, current_version)

    baseline_rows: list[dict[str, str]] = []
    if baselines_path.exists():
        with baselines_path.open(newline="") as fh:
            reader = csv.DictReader(fh)
            baseline_rows = [row for row in reader]

    by_target: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in baseline_rows:
        status = (row.get("status") or "").strip().lower()
        group = (row.get("group") or "").strip()
        target_dir = (row.get("target_dir") or "").strip()
        if not group or not target_dir:
            continue
        key = (group, target_dir)
        report_row = report_by_target.setdefault(
            key,
            _new_report_row(group, target_dir, (row.get("current_version") or "").strip()),
        )
        if status == "built":
            by_target.setdefault(key, []).append(row)
            continue
        if status == "failed":
            _record_failed_baseline(
                report_row,
                (row.get("baseline_version") or "").strip(),
                (row.get("error") or "").strip(),
            )

    out_normal = out_base / "v2" / "normal"
    out_stripped = out_base / "v2" / "stripped"
    out_normal.mkdir(parents=True, exist_ok=True)
    out_stripped.mkdir(parents=True, exist_ok=True)

    for entry in entries:
        rel = entry["path"]
        group = entry["group"]
        target_dir_path = (repo_root / "targets" / rel).resolve()
        target_name = Path(rel).name
        report_row = report_by_target[(group, target_name)]

        try:
            artifact_relpath = _run_make_print(target_dir_path, "print-target")
        except Exception as exc:
            _record_failed_baseline(report_row, "", f"could not resolve print-target: {exc}")
            continue
        binary_name = Path(artifact_relpath).name

        safe_src = target_dir_path / "safe" / artifact_relpath
        back_src = target_dir_path / "backdoored" / artifact_relpath

        if safe_src.exists():
            dst = out_normal / "malicious" / group / target_name / "safe" / binary_name
            _copy_file(safe_src, dst)
            dst2 = out_stripped / "malicious" / group / target_name / "safe" / binary_name
            _copy_file(safe_src, dst2)
            _maybe_strip(dst2, args.strip_tool, strip_flags)

        if back_src.exists():
            dst = out_normal / "malicious" / group / target_name / "backdoored" / binary_name
            _copy_file(back_src, dst)
            dst2 = out_stripped / "malicious" / group / target_name / "backdoored" / binary_name
            _copy_file(back_src, dst2)
            _maybe_strip(dst2, args.strip_tool, strip_flags)

        for row in by_target.get((group, target_name), []):
            baseline_version = (row.get("baseline_version") or "").strip()
            build_dir = (row.get("build_dir") or "").strip()
            if not baseline_version or not build_dir:
                _record_failed_baseline(
                    report_row,
                    baseline_version,
                    "invalid built baseline row (missing baseline_version/build_dir)",
                )
                continue
            src = target_dir_path / build_dir / artifact_relpath
            if not src.exists():
                _record_failed_baseline(
                    report_row,
                    baseline_version,
                    f"missing artifact during collection: {build_dir}/{artifact_relpath}",
                )
                continue

            dst = (
                out_normal
                / "malicious"
                / group
                / target_name
                / "baseline"
                / baseline_version
                / binary_name
            )
            _copy_file(src, dst)

            dst2 = (
                out_stripped
                / "malicious"
                / group
                / target_name
                / "baseline"
                / baseline_version
                / binary_name
            )
            _copy_file(src, dst2)
            _maybe_strip(dst2, args.strip_tool, strip_flags)
            collected_versions = cast(list[str], report_row["collected_baseline_versions"])
            _append_unique(collected_versions, baseline_version)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=REPORT_FIELDS)
        writer.writeheader()
        for key in sorted(report_by_target):
            row = report_by_target[key]
            collected_versions = cast(list[str], row["collected_baseline_versions"])
            failed_versions = cast(list[str], row["failed_baseline_versions"])
            failed_details = cast(list[str], row["failed_details"])
            writer.writerow(
                {
                    "group": row["group"],
                    "target_dir": row["target_dir"],
                    "current_version": row["current_version"],
                    "collected_baseline_count": len(collected_versions),
                    "collected_baseline_versions": ";".join(collected_versions),
                    "failed_baseline_count": len(failed_versions),
                    "failed_baseline_versions": ";".join(failed_versions),
                    "failed_details": " | ".join(failed_details),
                }
            )
    print(f"Wrote malicious baseline report: {report_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
