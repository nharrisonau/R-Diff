# Contributing

## Scope

This repository is maintained as a research artifact. Contributions should prioritize:

- reproducibility,
- deterministic metadata generation,
- clear provenance for all vendored sources.

## Setup

1. Clone with submodules:

```bash
git clone --recurse-submodules <repo-url>
```

2. If already cloned:

```bash
git submodule update --init --recursive
```

## Required Checks

Run these before opening a PR:

```bash
python3 -m unittest discover -s targets/scripts/tests -v
python3 targets/scripts/verify_sources.py
python3 targets/scripts/verify_target_metadata.py
```

## Provenance Updates

If you change submodule commits/URLs, regenerate and verify the lockfile:

```bash
python3 targets/scripts/update_sources_lock.py
python3 targets/scripts/verify_sources.py
```

## Pull Request Guidelines

- Keep commits focused (one logical change per commit).
- Update docs for any interface/path/schema change.
- Do not commit `outputs/` or `local_outputs/` runtime artifacts.
