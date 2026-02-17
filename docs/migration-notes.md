# Migration Notes

This document summarizes workflow changes introduced in publication-prep cleanup.

## Baseline State Location

Changed:

- from `baselines.csv` under `targets/` (older snapshots)
- to `local_outputs/baselines.csv`

Updated defaults:

- `targets/scripts/build_baselines.py --out`
- `targets/scripts/collect_outputs_v2.py --baselines`
- `make -C targets all` now passes explicit baseline output path.

## Source Tracking

`original/` and `previous/` source trees are submodule-managed and pinned via:

- `.gitmodules`
- `targets/sources.lock.json`

Validate with:

```bash
python3 targets/scripts/update_sources_lock.py   # when submodule commits/URLs change
python3 targets/scripts/verify_sources.py
```
