#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED_README_FIELDS = [
    "**Type**",
    "**Affected Versions**",
    "**Previous Version**",
    "**Insertion Style**",
    "**Insertion-Point Function**",
    "**Insertion-Point Offset**",
]

REQUIRED_README_SECTIONS = [
    "## Behavior",
    "## Triggering",
    "## Reference",
]

REQUIRED_MAKE_TARGETS = [
    "safe",
    "backdoored",
    "previous",
    "clean",
    "setup",
    "teardown",
    "print-target",
    "print-current-version",
]

REQUIRED_MAKE_VARS = [
    "TARGET",
    "CURRENT_VERSION",
    "ORIGINAL_REPO",
    "PREVIOUS_REPO",
    "PREVIOUS_DIR",
    "COPY_PREVIOUS",
]
EXPECTED_PREVIOUS_DIR = "previous-build"


def _repo_root_from_script() -> Path:
    # pipeline/scripts/verify_target_metadata.py -> parents[2] is repo root
    return Path(__file__).resolve().parents[2]


def _has_target(make_text: str, target: str) -> bool:
    return bool(re.search(rf"(?m)^{re.escape(target)}\s*:", make_text))


def _has_var(make_text: str, var: str) -> bool:
    return bool(re.search(rf"(?m)^\s*{re.escape(var)}\s*[:?]?=", make_text))


def _var_value(make_text: str, var: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(var)}\s*\??=\s*(.+?)\s*$", make_text)
    if match is None:
        return None
    return match.group(1).strip()


def _target_recipe(make_text: str, target: str) -> str:
    match = re.search(
        rf"(?ms)^{re.escape(target)}\s*:.*\n((?:\t.*(?:\n|$))*)", make_text
    )
    if match is None:
        return ""
    return match.group(1)


def _has_previous_target_contract(make_text: str) -> bool:
    return bool(
        re.search(
            r"(?m)^\s*PREVIOUS_TARGET\s*=\s*\$\(PREVIOUS_DIR\)/\$\(TARGET\)\s*$",
            make_text,
        )
    )


def main() -> int:
    repo_root = _repo_root_from_script()
    ap = argparse.ArgumentParser(description="Verify target contract metadata.")
    ap.add_argument(
        "--repo-root",
        default=str(repo_root),
        help="Repo root (default: auto-detected)",
    )
    ap.add_argument(
        "--config",
        default="",
        help="Path to previous_config.json (default: pipeline/previous_config.json)",
    )
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    config_path = (
        Path(args.config).resolve()
        if args.config
        else repo_root / "pipeline" / "previous_config.json"
    )
    if not config_path.exists():
        print(f"missing config: {config_path}")
        return 2

    entries = json.loads(config_path.read_text())
    errors: list[str] = []

    for entry in entries:
        rel = entry["path"]
        sample_root = repo_root / "targets" / rel
        sample_name = Path(rel).name

        for required in ["Makefile", "README.md", "patches", "original", "previous"]:
            if not (sample_root / required).exists():
                errors.append(f"{sample_name}: missing required path {required}")

        makefile = sample_root / "Makefile"
        if makefile.exists():
            make_text = makefile.read_text(errors="replace")
            for target in REQUIRED_MAKE_TARGETS:
                if not _has_target(make_text, target):
                    errors.append(f"{sample_name}: missing make target '{target}'")
            for var in REQUIRED_MAKE_VARS:
                if not _has_var(make_text, var):
                    errors.append(f"{sample_name}: missing make variable '{var}'")
            previous_dir = _var_value(make_text, "PREVIOUS_DIR")
            if previous_dir == "previous":
                errors.append(
                    f"{sample_name}: PREVIOUS_DIR must not default to 'previous'"
                )
            elif previous_dir and previous_dir != EXPECTED_PREVIOUS_DIR:
                errors.append(
                    f"{sample_name}: PREVIOUS_DIR must default to '{EXPECTED_PREVIOUS_DIR}'"
                )
            if not _has_previous_target_contract(make_text):
                errors.append(
                    f"{sample_name}: missing PREVIOUS_TARGET contract '$(PREVIOUS_DIR)/$(TARGET)'"
                )
            clean_recipe = _target_recipe(make_text, "clean")
            if clean_recipe:
                if "previous/" in clean_recipe:
                    errors.append(
                        f"{sample_name}: clean target must not remove literal 'previous/'"
                    )
                if "$(PREVIOUS_REPO)" in clean_recipe:
                    errors.append(
                        f"{sample_name}: clean target must not remove '$(PREVIOUS_REPO)'"
                    )
                if "$(PREVIOUS_DIR)" not in clean_recipe:
                    errors.append(
                        f"{sample_name}: clean target must remove '$(PREVIOUS_DIR)/'"
                    )

        readme = sample_root / "README.md"
        if readme.exists():
            readme_text = readme.read_text(errors="replace")
            h1_count = len(re.findall(r"(?m)^#\s+", readme_text))
            if h1_count != 1:
                errors.append(
                    f"{sample_name}: README must contain exactly one H1 heading"
                )
            for field in REQUIRED_README_FIELDS:
                if field not in readme_text:
                    errors.append(f"{sample_name}: missing README field '{field}'")
            if "**Backdoored function**" in readme_text:
                errors.append(
                    f"{sample_name}: non-canonical README field '**Backdoored function**'"
                )
            if "**Backdoored functions**" in readme_text:
                errors.append(
                    f"{sample_name}: non-canonical README field '**Backdoored functions**'"
                )
            for legacy in [
                "**Affected versions**",
                "**Previous version**",
                "**Insertion style**",
                "**Insertion-point function**",
                "**Insertion-point addr (OXIDE)**",
                "**Insertion-Point Addr (OXIDE)**",
            ]:
                if legacy in readme_text:
                    errors.append(
                        f"{sample_name}: non-canonical README field '{legacy}'"
                    )
            for section in REQUIRED_README_SECTIONS:
                if section not in readme_text:
                    errors.append(f"{sample_name}: missing README section '{section}'")

    if errors:
        print("target metadata verification failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print(f"verified {len(entries)} targets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
