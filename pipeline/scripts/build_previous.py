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
    from .list_previous import list_previous
    from .versioning import sanitize_component
except ImportError:  # pragma: no cover
    # When executed as a script (python3 build_previous.py).
    from list_previous import list_previous
    from versioning import sanitize_component


PREVIOUS_SRC_DIR = "previous-src"
PREVIOUS_ARTIFACTS_DIR = "previous-artifacts"
PREVIOUS_FIELDS = [
    "group",
    "target_dir",
    "current_version",
    "previous_version",
    "previous_tag",
    "build_dir",
    "artifact_relpath",
    "status",
    "error",
]
MAKE_DIR_LINE_RE = re.compile(r"^make(?:\[\d+\])?: (?:Entering|Leaving) directory .*$")


def _repo_root_from_script() -> Path:
    # pipeline/scripts/build_previous.py -> parents[2] is repo root
    return Path(__file__).resolve().parents[2]


def _is_make_dir_line(line: str) -> bool:
    return bool(MAKE_DIR_LINE_RE.match(line.strip()))


def _resolve_artifact_relpath(entry: dict[str, object]) -> str:
    artifact_relpath = str(entry.get("artifact_relpath", "") or "").strip()
    if artifact_relpath:
        return artifact_relpath
    raise RuntimeError("missing required artifact_relpath in previous config")


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


def previous_build_dir(previous_version: str) -> str:
    return f"{PREVIOUS_ARTIFACTS_DIR}/{sanitize_component(previous_version)}"


def _staged_artifact_path(target_dir: Path, previous_version: str, artifact_relpath: str) -> Path:
    return target_dir / previous_build_dir(previous_version) / artifact_relpath


def _copy_artifact(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _configured_previous_version(entry: dict[str, object]) -> tuple[str, str]:
    previous_version = str(entry.get("version", "") or "").strip()
    if not previous_version:
        return "", "missing required version"
    return previous_version, ""


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
            previous_version = (row.get("previous_version") or "").strip()
            if not group or not target_dir or not previous_version:
                continue
            failed_by_target.setdefault((group, target_dir), set()).add(previous_version)

    return failed_by_target


def _ensure_previous_checkout(target_dir: Path, upstream_repo: Path) -> tuple[Path | None, str]:
    previous_src = target_dir / PREVIOUS_SRC_DIR

    if previous_src.exists() and not _is_git_repo(previous_src):
        shutil.rmtree(previous_src)

    if not previous_src.exists():
        rc, tail = _run_cmd_tail(
            ["git", "clone", "--no-checkout", str(upstream_repo), str(previous_src)],
            cwd=target_dir,
        )
        if rc != 0:
            return None, _short_error(tail or f"git clone failed (rc={rc})")

    rc, _ = _run_cmd_tail(["git", "-C", str(previous_src), "remote", "get-url", "origin"])
    if rc == 0:
        rc, tail = _run_cmd_tail(
            ["git", "-C", str(previous_src), "remote", "set-url", "origin", str(upstream_repo)]
        )
    else:
        rc, tail = _run_cmd_tail(
            ["git", "-C", str(previous_src), "remote", "add", "origin", str(upstream_repo)]
        )
    if rc != 0:
        return None, _short_error(tail or f"git remote update failed (rc={rc})")

    rc, tail = _run_cmd_tail(
        ["git", "-C", str(previous_src), "fetch", "--force", "--tags", "origin"],
        cwd=target_dir,
    )
    if rc != 0:
        return None, _short_error(tail or f"git fetch failed (rc={rc})")

    return previous_src, ""


def _checkout_previous_version(previous_src: Path, previous_tag: str) -> tuple[bool, str]:
    rc, tail = _run_cmd_tail(
        ["git", "-C", str(previous_src), "checkout", "--force", previous_tag],
        tail_lines=50,
    )
    if rc != 0:
        return False, _short_error(tail or f"git checkout failed (rc={rc})")

    rc, tail = _run_cmd_tail(
        ["git", "-C", str(previous_src), "clean", "-fdx"],
        tail_lines=50,
    )
    if rc != 0:
        return False, _short_error(tail or f"git clean failed (rc={rc})")

    return True, ""


def _previous_row(
    *,
    group: str,
    target_name: str,
    current_version: str,
    artifact_relpath: str,
    status: str,
    error: str,
    previous_version: str = "",
    previous_tag: str = "",
    build_dir: str = "",
) -> dict[str, str]:
    return {
        "group": group,
        "target_dir": target_name,
        "current_version": current_version,
        "previous_version": previous_version,
        "previous_tag": previous_tag,
        "build_dir": build_dir,
        "artifact_relpath": artifact_relpath,
        "status": status,
        "error": error,
    }


def main() -> int:
    repo_root = _repo_root_from_script()
    ap = argparse.ArgumentParser(description="Build one previous artifact per target.")
    ap.add_argument(
        "--config",
        default=str(repo_root / "pipeline" / "previous_config.json"),
        help="Path to previous_config.json",
    )
    ap.add_argument(
        "--out",
        default=str(repo_root / "local_outputs" / "previous.csv"),
        help="Where to write previous.csv",
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

        try:
            artifact_relpath = _resolve_artifact_relpath(entry)
        except Exception as exc:
            rows.append(
                _previous_row(
                    group=group,
                    target_name=target_name,
                    current_version=current_version,
                    previous_version="",
                    previous_tag="",
                    build_dir="",
                    artifact_relpath="",
                    status="failed",
                    error=f"could not resolve artifact path: {exc}",
                )
            )
            continue

        previous_version, version_err = _configured_previous_version(entry)
        if not previous_version:
            rows.append(
                _previous_row(
                    group=group,
                    target_name=target_name,
                    current_version=current_version,
                    artifact_relpath=artifact_relpath,
                    status="failed",
                    error=version_err,
                )
            )
            continue

        if previous_version in target_failed_versions:
            rows.append(
                _previous_row(
                    group=group,
                    target_name=target_name,
                    current_version=current_version,
                    previous_version=previous_version,
                    build_dir=previous_build_dir(previous_version),
                    artifact_relpath=artifact_relpath,
                    status="failed",
                    error=(
                        f"previous version {previous_version} previously failed; "
                        "remove its row from previous.csv to retry"
                    ),
                )
            )
            continue

        if mode == "manual":
            previous_tag = str(entry.get("previous_tag", "") or "").strip()
            source_build_dir = str(entry.get("source_build_dir", "previous") or "previous").strip()
            build_dir = previous_build_dir(previous_version)
            source_artifact = target_dir / source_build_dir / artifact_relpath
            staged_artifact = _staged_artifact_path(target_dir, previous_version, artifact_relpath)

            if not source_artifact.exists():
                rows.append(
                    _previous_row(
                        group=group,
                        target_name=target_name,
                        current_version=current_version,
                        previous_version=previous_version,
                        previous_tag=previous_tag,
                        build_dir=build_dir,
                        artifact_relpath=artifact_relpath,
                        status="failed",
                        error=f"missing artifact: {source_build_dir}/{artifact_relpath}",
                    )
                )
                continue

            try:
                _copy_artifact(source_artifact, staged_artifact)
            except Exception as exc:
                rows.append(
                    _previous_row(
                        group=group,
                        target_name=target_name,
                        current_version=current_version,
                        previous_version=previous_version,
                        previous_tag=previous_tag,
                        build_dir=build_dir,
                        artifact_relpath=artifact_relpath,
                        status="failed",
                        error=_short_error(str(exc)),
                    )
                )
                continue

            rows.append(
                _previous_row(
                    group=group,
                    target_name=target_name,
                    current_version=current_version,
                    previous_version=previous_version,
                    previous_tag=previous_tag,
                    build_dir=build_dir,
                    artifact_relpath=artifact_relpath,
                    status="built",
                    error="",
                )
            )
            continue

        if mode != "git_tags":
            rows.append(
                _previous_row(
                    group=group,
                    target_name=target_name,
                    current_version=current_version,
                    artifact_relpath=artifact_relpath,
                    status="failed",
                    error=f"unknown mode: {mode}",
                )
            )
            continue

        upstream_repo = entry.get("upstream_repo", "")
        tag_patterns = entry.get("tag_patterns", [])
        version_scheme = entry.get("version_scheme", "semver")
        major_token_index = int(entry.get("major_token_index", 0))
        include_prerelease = bool(entry.get("include_prerelease", False))

        upstream_path = (target_dir / upstream_repo).resolve()
        if not upstream_path.exists():
            rows.append(
                _previous_row(
                    group=group,
                    target_name=target_name,
                    current_version=current_version,
                    artifact_relpath=artifact_relpath,
                    status="failed",
                    error=f"missing upstream repo: {upstream_repo}",
                )
            )
            continue
        if not _is_git_repo(upstream_path):
            rows.append(
                _previous_row(
                    group=group,
                    target_name=target_name,
                    current_version=current_version,
                    artifact_relpath=artifact_relpath,
                    status="failed",
                    error=f"upstream repo is not a git checkout: {upstream_repo}",
                )
            )
            continue

        try:
            previous_matches = list_previous(
                repo=upstream_path,
                tag_patterns=tag_patterns,
                version_scheme=version_scheme,
                current_version=current_version,
                version=previous_version,
                major_token_index=major_token_index,
                include_prerelease=include_prerelease,
            )
        except Exception as exc:
            rows.append(
                _previous_row(
                    group=group,
                    target_name=target_name,
                    current_version=current_version,
                    artifact_relpath=artifact_relpath,
                    status="failed",
                    error=f"previous listing failed: {exc}",
                )
            )
            continue

        if not previous_matches:
            rows.append(
                _previous_row(
                    group=group,
                    target_name=target_name,
                    current_version=current_version,
                    previous_version=previous_version,
                    previous_tag="",
                    build_dir=previous_build_dir(previous_version),
                    artifact_relpath=artifact_relpath,
                    status="failed",
                    error=f"configured version {previous_version!r} is not a resolvable previous version",
                )
            )
            continue
        previous_version, previous_tag = previous_matches[0]

        build_dir = previous_build_dir(previous_version)
        staged_artifact = _staged_artifact_path(target_dir, previous_version, artifact_relpath)
        if staged_artifact.exists():
            rows.append(
                _previous_row(
                    group=group,
                    target_name=target_name,
                    current_version=current_version,
                    previous_version=previous_version,
                    previous_tag=previous_tag,
                    build_dir=build_dir,
                    artifact_relpath=artifact_relpath,
                    status="built",
                    error="",
                )
            )
            continue

        previous_artifact = target_dir / "previous" / artifact_relpath
        if previous_artifact.exists():
            try:
                _copy_artifact(
                    previous_artifact,
                    staged_artifact,
                )
                rows.append(
                    _previous_row(
                        group=group,
                        target_name=target_name,
                        current_version=current_version,
                        previous_version=previous_version,
                        previous_tag=previous_tag,
                        build_dir=build_dir,
                        artifact_relpath=artifact_relpath,
                        status="built",
                        error="",
                    )
                )
            except Exception as exc:
                rows.append(
                    _previous_row(
                        group=group,
                        target_name=target_name,
                        current_version=current_version,
                        previous_version=previous_version,
                        previous_tag=previous_tag,
                        build_dir=build_dir,
                        artifact_relpath=artifact_relpath,
                        status="failed",
                        error=_short_error(str(exc)),
                    )
                )
            continue

        previous_src, err = _ensure_previous_checkout(target_dir, upstream_path)
        if previous_src is None:
            rows.append(
                _previous_row(
                    group=group,
                    target_name=target_name,
                    current_version=current_version,
                    previous_version=previous_version,
                    previous_tag=previous_tag,
                    build_dir=build_dir,
                    artifact_relpath=artifact_relpath,
                    status="failed",
                    error=f"previous checkout init failed: {err}",
                )
            )
            continue

        ok, err = _checkout_previous_version(previous_src, previous_tag)
        if not ok:
            rows.append(
                _previous_row(
                    group=group,
                    target_name=target_name,
                    current_version=current_version,
                    previous_version=previous_version,
                    previous_tag=previous_tag,
                    build_dir=build_dir,
                    artifact_relpath=artifact_relpath,
                    status="failed",
                    error=err,
                )
            )
            continue

        cmd = [
            "make",
            "-C",
            str(target_dir),
            "previous",
            f"PREVIOUS_DIR={PREVIOUS_SRC_DIR}",
            f"PREVIOUS_REPO={PREVIOUS_SRC_DIR}",
            "COPY_PREVIOUS=0",
            "SUDO=",
        ]
        rc, tail = _run_cmd_tail(cmd, cwd=repo_root)
        src_artifact = previous_src / artifact_relpath
        if rc != 0 or not src_artifact.exists():
            err_text = _short_error(tail or f"make failed (rc={rc})")
            if rc == 0 and not src_artifact.exists():
                err_text = f"missing artifact after previous build: {PREVIOUS_SRC_DIR}/{artifact_relpath}"
            rows.append(
                _previous_row(
                    group=group,
                    target_name=target_name,
                    current_version=current_version,
                    previous_version=previous_version,
                    previous_tag=previous_tag,
                    build_dir=build_dir,
                    artifact_relpath=artifact_relpath,
                    status="failed",
                    error=err_text,
                )
            )
            continue

        try:
            _copy_artifact(src_artifact, staged_artifact)
        except Exception as exc:
            rows.append(
                _previous_row(
                    group=group,
                    target_name=target_name,
                    current_version=current_version,
                    previous_version=previous_version,
                    previous_tag=previous_tag,
                    build_dir=build_dir,
                    artifact_relpath=artifact_relpath,
                    status="failed",
                    error=_short_error(str(exc)),
                )
            )
            continue

        rows.append(
            _previous_row(
                group=group,
                target_name=target_name,
                current_version=current_version,
                previous_version=previous_version,
                previous_tag=previous_tag,
                build_dir=build_dir,
                artifact_relpath=artifact_relpath,
                status="built",
                error="",
            )
        )

    with out_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=PREVIOUS_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in PREVIOUS_FIELDS})

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
