#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def _repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def _run(cmd: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
    )


def _gitlinks(repo_root: Path) -> dict[str, str]:
    proc = _run(["git", "-C", str(repo_root), "ls-files", "--stage"])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "git ls-files --stage failed")
    out: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        meta, path = line.split("\t", 1)
        mode, sha, _stage = meta.split()[:3]
        if mode == "160000":
            out[path] = sha
    return out


def _submodule_urls(repo_root: Path) -> dict[str, str]:
    mod_path = repo_root / ".gitmodules"
    if not mod_path.exists():
        return {}
    proc = _run(
        [
            "git",
            "-C",
            str(repo_root),
            "config",
            "-f",
            str(mod_path),
            "--get-regexp",
            r"^submodule\..*\.path$",
        ]
    )
    if proc.returncode != 0 and proc.stdout.strip() == "":
        return {}

    name_to_path: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        key, path = line.split(" ", 1)
        # key format: submodule.<name>.path
        name = key[len("submodule.") : -len(".path")]
        name_to_path[name] = path.strip()

    out: dict[str, str] = {}
    for name, path in name_to_path.items():
        url_proc = _run(
            [
                "git",
                "-C",
                str(repo_root),
                "config",
                "-f",
                str(mod_path),
                "--get",
                f"submodule.{name}.url",
            ]
        )
        if url_proc.returncode == 0:
            out[path] = url_proc.stdout.strip()
    return out


def _active_source_paths(repo_root: Path, config_path: Path) -> set[str]:
    entries = json.loads(config_path.read_text())
    paths: set[str] = set()
    for entry in entries:
        rel = entry["path"]
        paths.add(f"targets/{rel}/original")
        paths.add(f"targets/{rel}/previous")
    return paths


def _lock_entries_by_path(lock_path: Path) -> dict[str, dict[str, str]]:
    lock = json.loads(lock_path.read_text())
    if lock.get("format_version") != 1:
        raise ValueError(f"unsupported sources.lock.json format_version: {lock.get('format_version')!r}")
    out: dict[str, dict[str, str]] = {}
    for entry in lock.get("entries", []):
        path = entry.get("path", "")
        if not path:
            continue
        out[path] = entry
    return out


def main() -> int:
    repo_root = _repo_root_from_script()
    ap = argparse.ArgumentParser(description="Verify malicious source provenance lockfile.")
    ap.add_argument(
        "--repo-root",
        default=str(repo_root),
        help="Repo root (default: auto-detected)",
    )
    ap.add_argument(
        "--config",
        default="",
        help="Path to baselines_config.json (default: targets/malicious/baselines_config.json)",
    )
    ap.add_argument(
        "--lock",
        default="",
        help="Path to sources.lock.json (default: targets/malicious/sources.lock.json)",
    )
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    config_path = (
        Path(args.config).resolve()
        if args.config
        else (repo_root / "targets" / "malicious" / "baselines_config.json")
    )
    lock_path = (
        Path(args.lock).resolve()
        if args.lock
        else (repo_root / "targets" / "malicious" / "sources.lock.json")
    )

    if not config_path.exists():
        print(f"missing config: {config_path}", file=sys.stderr)
        return 2
    if not lock_path.exists():
        print(f"missing lockfile: {lock_path}", file=sys.stderr)
        return 2

    active_paths = _active_source_paths(repo_root, config_path)
    gitlinks = _gitlinks(repo_root)
    urls = _submodule_urls(repo_root)
    lock_by_path = _lock_entries_by_path(lock_path)

    errors: list[str] = []

    for path in sorted(active_paths):
        if path not in gitlinks:
            errors.append(f"{path}: not tracked as gitlink submodule")
            continue
        if path not in urls:
            errors.append(f"{path}: missing .gitmodules URL entry")
            continue
        if not urls[path].startswith("https://"):
            errors.append(f"{path}: non-https submodule URL: {urls[path]}")

        entry = lock_by_path.get(path)
        if entry is None:
            errors.append(f"{path}: missing lock entry")
            continue

        expected_commit = entry.get("commit", "")
        actual_commit = gitlinks[path]
        if not expected_commit:
            errors.append(f"{path}: lock entry missing commit")
        elif expected_commit != actual_commit:
            errors.append(
                f"{path}: commit mismatch lock={expected_commit} gitlink={actual_commit}"
            )

        expected_url = entry.get("url", "")
        actual_url = urls[path]
        if expected_url != actual_url:
            errors.append(f"{path}: URL mismatch lock={expected_url} gitmodules={actual_url}")

        repo_dir = repo_root / path
        if repo_dir.exists():
            head = _run(["git", "-C", str(repo_dir), "rev-parse", "HEAD"])
            if head.returncode != 0:
                errors.append(f"{path}: unable to resolve submodule HEAD")
            elif head.stdout.strip() != actual_commit:
                errors.append(
                    f"{path}: working tree HEAD differs from gitlink ({head.stdout.strip()} vs {actual_commit})"
                )

    extra_lock_paths = sorted(set(lock_by_path) - active_paths)
    for path in extra_lock_paths:
        errors.append(f"{path}: lock entry is not an active malicious source path")

    if errors:
        print("source provenance verification failed:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    print(f"verified {len(active_paths)} source paths against {lock_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
