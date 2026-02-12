#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
from collections import deque
from pathlib import Path

try:
    # When imported as a package module.
    from .list_baselines import list_baselines
    from .versioning import sanitize_component
except ImportError:  # pragma: no cover
    # When executed as a script (python3 build_baselines.py).
    from list_baselines import list_baselines
    from versioning import sanitize_component


BASELINE_SRC_DIR = "baseline-src"
BASELINE_ARTIFACTS_DIR = "baseline-artifacts"
BASELINE_FIELDS = [
    "group",
    "target_dir",
    "current_version",
    "baseline_version",
    "baseline_tag",
    "build_dir",
    "artifact_relpath",
    "status",
    "error",
]
MAKE_DIR_LINE_RE = re.compile(r"^make(?:\[\d+\])?: (?:Entering|Leaving) directory .*$")


def _repo_root_from_script() -> Path:
    # targets/malicious/scripts/build_baselines.py -> parents[3] is repo root
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


def _read_target_from_makefile(target_dir: Path) -> str | None:
    mk = target_dir / "Makefile"
    if not mk.exists():
        return None
    for line in mk.read_text(errors="replace").splitlines():
        if line.strip().startswith("#"):
            continue
        m = re.match(r"^\s*TARGET\s*[:?]?=\s*(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return None


def _run_cmd_tail(cmd: list[str], *, cwd: Path | None = None, tail_lines: int = 50) -> tuple[int, str]:
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
    )
    assert proc.stdout is not None
    tail = deque(maxlen=tail_lines)
    for line in proc.stdout:
        tail.append(line.rstrip("\n"))
    rc = proc.wait()
    return rc, "\n".join(tail).strip()


def _short_error(msg: str, *, limit: int = 500) -> str:
    text = (msg or "").strip()
    if not text:
        return ""
    lines = [re.sub(r"\s+", " ", line.strip()) for line in text.splitlines() if line.strip()]
    meaningful = [line for line in lines if not _is_make_dir_line(line)]
    if meaningful:
        return meaningful[-1][:limit]
    return lines[-1][:limit]


def _is_git_repo(path: Path) -> bool:
    proc = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0


def baseline_build_dir(baseline_version: str) -> str:
    return f"{BASELINE_ARTIFACTS_DIR}/{sanitize_component(baseline_version)}"


def _staged_artifact_path(target_dir: Path, baseline_version: str, artifact_relpath: str) -> Path:
    return target_dir / baseline_build_dir(baseline_version) / artifact_relpath


def _copy_artifact(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def dedupe_baseline_candidates(
    baselines: list[tuple[str, str]], seen_versions: set[str] | None = None
) -> list[tuple[str, str]]:
    seen = set(seen_versions or set())
    out: list[tuple[str, str]] = []
    for version, tag in baselines:
        if version in seen:
            continue
        seen.add(version)
        out.append((version, tag))
    return out


def _load_failed_versions(path: Path) -> dict[tuple[str, str], set[str]]:
    failed_by_target: dict[tuple[str, str], set[str]] = {}
    if not path.exists():
        return failed_by_target

    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if (row.get("status") or "").strip().lower() != "failed":
                continue
            group = (row.get("group") or "").strip()
            target_dir = (row.get("target_dir") or "").strip()
            baseline_version = (row.get("baseline_version") or "").strip()
            if not group or not target_dir or not baseline_version:
                continue
            failed_by_target.setdefault((group, target_dir), set()).add(baseline_version)

    return failed_by_target


def _ensure_baseline_checkout(target_dir: Path, upstream_repo: Path) -> tuple[Path | None, str]:
    baseline_src = target_dir / BASELINE_SRC_DIR

    if baseline_src.exists() and not _is_git_repo(baseline_src):
        shutil.rmtree(baseline_src)

    if not baseline_src.exists():
        rc, tail = _run_cmd_tail(
            ["git", "clone", "--no-checkout", str(upstream_repo), str(baseline_src)],
            cwd=target_dir,
        )
        if rc != 0:
            return None, _short_error(tail or f"git clone failed (rc={rc})")

    rc, _ = _run_cmd_tail(["git", "-C", str(baseline_src), "remote", "get-url", "origin"])
    if rc == 0:
        rc, tail = _run_cmd_tail(
            ["git", "-C", str(baseline_src), "remote", "set-url", "origin", str(upstream_repo)]
        )
    else:
        rc, tail = _run_cmd_tail(
            ["git", "-C", str(baseline_src), "remote", "add", "origin", str(upstream_repo)]
        )
    if rc != 0:
        return None, _short_error(tail or f"git remote update failed (rc={rc})")

    rc, tail = _run_cmd_tail(
        ["git", "-C", str(baseline_src), "fetch", "--force", "--tags", "origin"],
        cwd=target_dir,
    )
    if rc != 0:
        return None, _short_error(tail or f"git fetch failed (rc={rc})")

    return baseline_src, ""


def _checkout_baseline_version(baseline_src: Path, baseline_tag: str) -> tuple[bool, str]:
    rc, tail = _run_cmd_tail(
        ["git", "-C", str(baseline_src), "checkout", "--force", baseline_tag],
        tail_lines=50,
    )
    if rc != 0:
        return False, _short_error(tail or f"git checkout failed (rc={rc})")

    rc, tail = _run_cmd_tail(
        ["git", "-C", str(baseline_src), "clean", "-fdx"],
        tail_lines=50,
    )
    if rc != 0:
        return False, _short_error(tail or f"git clean failed (rc={rc})")

    return True, ""


def main() -> int:
    repo_root = _repo_root_from_script()
    ap = argparse.ArgumentParser(description="Build multi-baseline artifacts for malicious targets.")
    ap.add_argument(
        "--config",
        default=str(repo_root / "targets" / "malicious" / "baselines_config.json"),
        help="Path to baselines_config.json",
    )
    ap.add_argument(
        "--out",
        default=str(repo_root / "local_outputs" / "malicious" / "baselines.csv"),
        help="Where to write baselines.csv",
    )
    ap.add_argument("--limit", type=int, default=0, help="Limit baselines per target (0 = no limit)")
    ap.add_argument(
        "--stop-after-failures",
        type=int,
        default=0,
        help="Stop after N baseline build failures per target (0 = no stop)",
    )
    args = ap.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Missing config: {config_path}")
        return 1
    entries = json.loads(config_path.read_text())
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    previously_failed_versions = _load_failed_versions(out_path)

    rows: list[dict[str, str]] = []

    for entry in entries:
        rel = entry["path"]
        group = entry["group"]
        current_version = entry.get("current_version", "")
        mode = entry.get("mode", "manual")
        target_dir = (repo_root / "targets" / rel).resolve()
        target_name = Path(rel).name
        target_failed_versions = previously_failed_versions.get((group, target_name), set())
        configured_excluded_versions = {
            str(v).strip() for v in entry.get("exclude_versions", []) if str(v).strip()
        }
        excluded_versions = set(target_failed_versions) | configured_excluded_versions

        try:
            artifact_relpath = _run_make_print(target_dir, "print-target")
        except Exception:
            artifact_relpath = _read_target_from_makefile(target_dir) or ""

        if not artifact_relpath:
            rows.append(
                {
                    "group": group,
                    "target_dir": target_name,
                    "current_version": current_version,
                    "baseline_version": "",
                    "baseline_tag": "",
                    "build_dir": "",
                    "artifact_relpath": "",
                    "status": "failed",
                    "error": "could not determine TARGET",
                }
            )
            continue

        built_versions: set[str] = set()

        if mode == "manual":
            seen_manual_versions: set[str] = set()
            for mb in entry.get("manual_baselines", []):
                baseline_version = (mb.get("baseline_version", "") or "").strip()
                if not baseline_version or baseline_version in seen_manual_versions:
                    continue
                seen_manual_versions.add(baseline_version)
                if baseline_version in excluded_versions:
                    rows.append(
                        {
                            "group": group,
                            "target_dir": target_name,
                            "current_version": current_version,
                            "baseline_version": baseline_version,
                            "baseline_tag": mb.get("baseline_tag", ""),
                            "build_dir": baseline_build_dir(baseline_version),
                            "artifact_relpath": artifact_relpath,
                            "status": "skipped",
                            "error": "skipped previously failed baseline build",
                        }
                    )
                    continue
                baseline_tag = mb.get("baseline_tag", "")
                source_build_dir = mb.get("build_dir", "prev-safe")
                source_artifact = target_dir / source_build_dir / artifact_relpath
                build_dir = baseline_build_dir(baseline_version)
                staged_artifact = _staged_artifact_path(target_dir, baseline_version, artifact_relpath)
                if source_artifact.exists():
                    try:
                        _copy_artifact(source_artifact, staged_artifact)
                        status = "built"
                        err = ""
                        built_versions.add(baseline_version)
                    except Exception as exc:
                        status = "failed"
                        err = _short_error(str(exc))
                else:
                    status = "failed"
                    err = f"missing artifact: {source_build_dir}/{artifact_relpath}"
                rows.append(
                    {
                        "group": group,
                        "target_dir": target_name,
                        "current_version": current_version,
                        "baseline_version": baseline_version,
                        "baseline_tag": baseline_tag,
                        "build_dir": build_dir,
                        "artifact_relpath": artifact_relpath,
                        "status": status,
                        "error": err,
                    }
                )
            continue

        if mode != "git_tags":
            rows.append(
                {
                    "group": group,
                    "target_dir": target_name,
                    "current_version": current_version,
                    "baseline_version": "",
                    "baseline_tag": "",
                    "build_dir": "",
                    "artifact_relpath": artifact_relpath,
                    "status": "skipped",
                    "error": f"unknown mode: {mode}",
                }
            )
            continue

        upstream_repo = entry.get("upstream_repo", "")
        tag_patterns = entry.get("tag_patterns", [])
        version_scheme = entry.get("version_scheme", "semver")
        major_token_index = int(entry.get("major_token_index", 0))
        include_prerelease = bool(entry.get("include_prerelease", False))
        min_version = entry.get("min_version", "") or None

        upstream_path = (target_dir / upstream_repo).resolve()
        if not upstream_path.exists():
            rows.append(
                {
                    "group": group,
                    "target_dir": target_name,
                    "current_version": current_version,
                    "baseline_version": "",
                    "baseline_tag": "",
                    "build_dir": "",
                    "artifact_relpath": artifact_relpath,
                    "status": "failed",
                    "error": f"missing upstream repo: {upstream_repo}",
                }
            )
            continue
        if not _is_git_repo(upstream_path):
            rows.append(
                {
                    "group": group,
                    "target_dir": target_name,
                    "current_version": current_version,
                    "baseline_version": "",
                    "baseline_tag": "",
                    "build_dir": "",
                    "artifact_relpath": artifact_relpath,
                    "status": "failed",
                    "error": f"upstream repo is not a git checkout: {upstream_repo}",
                }
            )
            continue

        try:
            baselines = list_baselines(
                repo=upstream_path,
                tag_patterns=tag_patterns,
                version_scheme=version_scheme,
                current_version=current_version,
                major_token_index=major_token_index,
                include_prerelease=include_prerelease,
                min_version=min_version,
                exclude_versions=excluded_versions,
            )
        except Exception as exc:
            rows.append(
                {
                    "group": group,
                    "target_dir": target_name,
                    "current_version": current_version,
                    "baseline_version": "",
                    "baseline_tag": "",
                    "build_dir": "",
                    "artifact_relpath": artifact_relpath,
                    "status": "failed",
                    "error": f"baseline listing failed: {exc}",
                }
            )
            continue

        if args.limit and args.limit > 0:
            baselines = baselines[: args.limit]

        immediate_version = (entry.get("immediate_baseline_version", "") or "").strip()
        immediate_tag = ""
        if not immediate_version and baselines:
            immediate_version = baselines[0][0]
            immediate_tag = baselines[0][1]
        elif immediate_version:
            for version, tag in baselines:
                if version == immediate_version:
                    immediate_tag = tag
                    break

        if immediate_version and immediate_version in excluded_versions:
            rows.append(
                {
                    "group": group,
                    "target_dir": target_name,
                    "current_version": current_version,
                    "baseline_version": immediate_version,
                    "baseline_tag": immediate_tag,
                    "build_dir": baseline_build_dir(immediate_version),
                    "artifact_relpath": artifact_relpath,
                    "status": "skipped",
                    "error": "skipped previously failed baseline build",
                }
            )
            immediate_version = ""
            immediate_tag = ""

        prev_safe_artifact = target_dir / "prev-safe" / artifact_relpath
        if immediate_version and prev_safe_artifact.exists():
            try:
                _copy_artifact(
                    prev_safe_artifact,
                    _staged_artifact_path(target_dir, immediate_version, artifact_relpath),
                )
                rows.append(
                    {
                        "group": group,
                        "target_dir": target_name,
                        "current_version": current_version,
                        "baseline_version": immediate_version,
                        "baseline_tag": immediate_tag,
                        "build_dir": baseline_build_dir(immediate_version),
                        "artifact_relpath": artifact_relpath,
                        "status": "built",
                        "error": "",
                    }
                )
                built_versions.add(immediate_version)
            except Exception as exc:
                rows.append(
                    {
                        "group": group,
                        "target_dir": target_name,
                        "current_version": current_version,
                        "baseline_version": immediate_version,
                        "baseline_tag": immediate_tag,
                        "build_dir": baseline_build_dir(immediate_version),
                        "artifact_relpath": artifact_relpath,
                        "status": "failed",
                        "error": _short_error(str(exc)),
                    }
                )

        baselines = dedupe_baseline_candidates(baselines, built_versions)

        failures = 0
        baseline_src: Path | None = None
        for baseline_version, baseline_tag in baselines:
            build_dir = baseline_build_dir(baseline_version)
            staged_artifact = _staged_artifact_path(target_dir, baseline_version, artifact_relpath)
            if staged_artifact.exists():
                rows.append(
                    {
                        "group": group,
                        "target_dir": target_name,
                        "current_version": current_version,
                        "baseline_version": baseline_version,
                        "baseline_tag": baseline_tag,
                        "build_dir": build_dir,
                        "artifact_relpath": artifact_relpath,
                        "status": "built",
                        "error": "",
                    }
                )
                built_versions.add(baseline_version)
                continue

            if baseline_src is None:
                baseline_src, err = _ensure_baseline_checkout(target_dir, upstream_path)
                if baseline_src is None:
                    failures += 1
                    rows.append(
                        {
                            "group": group,
                            "target_dir": target_name,
                            "current_version": current_version,
                            "baseline_version": baseline_version,
                            "baseline_tag": baseline_tag,
                            "build_dir": build_dir,
                            "artifact_relpath": artifact_relpath,
                            "status": "failed",
                            "error": f"baseline checkout init failed: {err}",
                        }
                    )
                    break

            ok, err = _checkout_baseline_version(baseline_src, baseline_tag)
            if not ok:
                failures += 1
                rows.append(
                    {
                        "group": group,
                        "target_dir": target_name,
                        "current_version": current_version,
                        "baseline_version": baseline_version,
                        "baseline_tag": baseline_tag,
                        "build_dir": build_dir,
                        "artifact_relpath": artifact_relpath,
                        "status": "failed",
                        "error": err,
                    }
                )
                if args.stop_after_failures and failures >= args.stop_after_failures:
                    break
                continue

            cmd = [
                "make",
                "-C",
                str(target_dir),
                "prev-safe",
                f"PREV_DIR={BASELINE_SRC_DIR}",
                f"PREVIOUS_REPO={BASELINE_SRC_DIR}",
                "COPY_PREVIOUS=0",
                "SUDO=",
            ]
            rc, tail = _run_cmd_tail(cmd, cwd=repo_root)
            src_artifact = baseline_src / artifact_relpath
            if rc != 0 or not src_artifact.exists():
                failures += 1
                rows.append(
                    {
                        "group": group,
                        "target_dir": target_name,
                        "current_version": current_version,
                        "baseline_version": baseline_version,
                        "baseline_tag": baseline_tag,
                        "build_dir": build_dir,
                        "artifact_relpath": artifact_relpath,
                        "status": "failed",
                        "error": _short_error(tail or f"make failed (rc={rc})"),
                    }
                )
                if args.stop_after_failures and failures >= args.stop_after_failures:
                    break
                continue

            try:
                _copy_artifact(src_artifact, staged_artifact)
            except Exception as exc:
                failures += 1
                rows.append(
                    {
                        "group": group,
                        "target_dir": target_name,
                        "current_version": current_version,
                        "baseline_version": baseline_version,
                        "baseline_tag": baseline_tag,
                        "build_dir": build_dir,
                        "artifact_relpath": artifact_relpath,
                        "status": "failed",
                        "error": _short_error(str(exc)),
                    }
                )
                if args.stop_after_failures and failures >= args.stop_after_failures:
                    break
                continue

            rows.append(
                {
                    "group": group,
                    "target_dir": target_name,
                    "current_version": current_version,
                    "baseline_version": baseline_version,
                    "baseline_tag": baseline_tag,
                    "build_dir": build_dir,
                    "artifact_relpath": artifact_relpath,
                    "status": "built",
                    "error": "",
                }
            )
            built_versions.add(baseline_version)

    with out_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=BASELINE_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in BASELINE_FIELDS})

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
