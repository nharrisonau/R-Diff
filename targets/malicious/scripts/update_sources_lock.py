#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def _repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def _run(cmd: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
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
    if proc.returncode != 0 and not proc.stdout.strip():
        return {}

    name_to_path: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        key, path = line.split(" ", 1)
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


def _exact_tag(path: Path) -> str:
    proc = _run(["git", "-C", str(path), "describe", "--tags", "--exact-match"])
    if proc.returncode != 0:
        return ""
    return proc.stdout.strip()


def main() -> int:
    repo_root = _repo_root_from_script()

    ap = argparse.ArgumentParser(
        description="Regenerate targets/malicious/sources.lock.json from submodule state."
    )
    ap.add_argument("--repo-root", default=str(repo_root), help="Repo root (default: auto-detected)")
    ap.add_argument(
        "--config",
        default="",
        help="Path to baselines_config.json (default: targets/malicious/baselines_config.json)",
    )
    ap.add_argument(
        "--out",
        default="",
        help="Path to write sources.lock.json (default: targets/malicious/sources.lock.json)",
    )
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    config_path = (
        Path(args.config).resolve()
        if args.config
        else (repo_root / "targets" / "malicious" / "baselines_config.json")
    )
    out_path = (
        Path(args.out).resolve()
        if args.out
        else (repo_root / "targets" / "malicious" / "sources.lock.json")
    )

    if not config_path.exists():
        raise SystemExit(f"missing config: {config_path}")

    entries_cfg = json.loads(config_path.read_text())
    gitlinks = _gitlinks(repo_root)
    urls = _submodule_urls(repo_root)

    entries: list[dict[str, str]] = []
    for cfg in entries_cfg:
        group = cfg["group"]
        rel_base = f"targets/{cfg['path']}"
        sample = Path(rel_base).name

        for role in ("original", "previous"):
            path = f"{rel_base}/{role}"
            commit = gitlinks.get(path, "")
            if not commit:
                raise SystemExit(f"missing gitlink for active source path: {path}")
            url = urls.get(path, "")
            if not url:
                raise SystemExit(f"missing .gitmodules URL for active source path: {path}")

            tag = ""
            repo_dir = repo_root / path
            if repo_dir.exists():
                tag = _exact_tag(repo_dir)

            entries.append(
                {
                    "group": group,
                    "sample": sample,
                    "path": path,
                    "role": role,
                    "url": url,
                    "commit": commit,
                    "tag": tag,
                }
            )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({"format_version": 1, "entries": entries}, indent=2) + "\n")
    print(f"wrote {len(entries)} lock entries -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
