# Benign Update Pairs

This document defines how benign update pairs are constructed for false-positive evaluation.

## Data Provenance

Benign metadata is sourced from vendored URL lists under:

- `targets/benign/sources/firmware-dataset/dataset_II/products/*.csv`

The canonical generated metadata files are:

- `targets/benign/manifest.csv`
- `targets/benign/pairs.csv`
- `targets/benign/pairs_binned.csv`

Extracted root filesystems are not tracked in git by default.

## Pair Construction

Pairs are built per product from `manifest.csv` using `targets/benign/scripts/build_pairs.py`.

Sorting order per product:

1. Parse `date` using known date formats.
2. If date parse succeeds: sort by date ascending, then `version`.
3. If date parse fails: sort by `version` string.

Adjacent entries in the sorted list form update pairs:

- `prev_version` -> `next_version`
- `prev_rootfs` -> `next_rootfs`

## Bucketing Rules

`targets/benign/scripts/bin_pairs.py` assigns each pair to one scope:

- `major`
- `minor`
- `patch`
- `build`
- `other`

The first differing numeric token in version strings determines scope when both versions are semver-like.
Non-semver patterns, cross-architecture transitions, or unresolved comparisons are assigned to `other`.

## Reproducibility

To regenerate benign metadata without downloading firmware:

```bash
python3 targets/benign/scripts/generate_lists.py --overwrite
python3 targets/benign/scripts/bin_pairs.py
```

To build bucket-specific outputs:

```bash
python3 targets/benign/scripts/build_bucket.py --bucket major
```

## Limitations

- Version strings are heterogeneous across vendors.
- Some versions are normalized with suffixes (for example `__2`) to avoid collisions.
- URL availability can change over time; use `targets/benign/scripts/check_urls.py` for audit.
