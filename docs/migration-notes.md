# Migration Notes

This document summarizes workflow changes introduced in publication-prep cleanup.

## Baseline State Location

Changed:

- from `targets/malicious/baselines.csv`
- to `local_outputs/malicious/baselines.csv`

Updated defaults:

- `targets/malicious/scripts/build_baselines.py --out`
- `targets/malicious/scripts/collect_outputs_v2.py --baselines`
- `make -C targets all` now passes explicit baseline output path.

## Malicious Source Tracking

Malicious `original/` and `previous/` source trees are now submodule-managed and pinned via:

- `.gitmodules`
- `targets/malicious/sources.lock.json`

Validate with:

```bash
python3 targets/malicious/scripts/update_sources_lock.py   # when submodule commits/URLs change
python3 targets/malicious/scripts/verify_sources.py
```

## Benign Script Deprecation

Deprecated legacy entrypoints:

- `targets/benign/sources/firmware-dataset/dataset_II/download.py`
- `targets/benign/sources/firmware-dataset/dataset_II/unpack.py`

Use supported scripts in `targets/benign/scripts/` instead.

## Bucket Vocabulary

Standardized bucket names:

- `major`, `minor`, `patch`, `build`, `other`

`non-semver` has been retired in favor of `other`.
