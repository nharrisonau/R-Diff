# Contributing

## Scope

This repository is maintained as a research artifact. Contributions should prioritize:

- reproducibility,
- deterministic metadata generation,
- consistency between malicious and benign tracks,
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
python3 -m unittest discover -s targets/malicious/scripts/tests -v
python3 -m unittest discover -s targets/benign/scripts/tests -v
python3 targets/malicious/scripts/verify_sources.py
python3 targets/malicious/scripts/verify_target_metadata.py
python3 targets/benign/scripts/verify_metadata.py
```

## Malicious Provenance Updates

If you change malicious submodule commits/URLs, regenerate and verify the lockfile:

```bash
python3 targets/malicious/scripts/update_sources_lock.py
python3 targets/malicious/scripts/verify_sources.py
```

## Benign Metadata Updates

Regenerate benign metadata from vendored source lists:

```bash
python3 targets/benign/scripts/generate_lists.py --overwrite
python3 targets/benign/scripts/bin_pairs.py
python3 targets/benign/scripts/verify_metadata.py
```

Benign extracted root filesystems are runtime artifacts and should not be committed.

## Pull Request Guidelines

- Keep commits focused (one logical change per commit).
- Update docs for any interface/path/schema change.
- Do not commit `outputs/` or `local_outputs/` runtime artifacts.
