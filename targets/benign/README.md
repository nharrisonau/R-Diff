# Benign Firmware Samples

Benign samples are extracted root filesystems stored under:

```
targets/benign/<product>/<version>/rootfs
```

These samples are used to estimate false-positive rates by comparing adjacent
firmware versions without injected backdoors.

## Sources

The `targets/benign/sources` directory vendors the benign firmware URL lists
used to build this benchmark. These are the only active benign sources.

## Ingestion scripts

All scripts write to `targets/benign/manifest.csv` and can be re-run safely; use
`--overwrite` if you want to replace existing rootfs directories.

## Dependencies

- `binwalk` (required to extract firmware root filesystems)

- `targets/benign/scripts/ingest_firmware_dataset.py`
  - Downloads firmware from the benign URL lists and extracts rootfs with `binwalk`.
- `targets/benign/scripts/generate_lists.py`
  - Generates `manifest.csv` and `pairs.csv` from the benign URL lists only (no downloads).
- `targets/benign/scripts/build_pairs.py`
  - Generates `targets/benign/pairs.csv` for adjacent-version diffs.
- `targets/benign/scripts/pairs_to_txt.py`
  - Renders `pairs.csv` as a simple text list.
- `targets/benign/scripts/bin_pairs.py`
  - Generates bucketed pair outputs in `targets/benign/pairs_binned.*`.
- `targets/benign/scripts/build_bucket.py`
  - Builds per-bucket manifests and pair lists under `targets/benign/buckets/`.
- `targets/benign/scripts/check_urls.py`
  - Verifies URL reachability and optionally filters the manifest.

## Buckets (Update Scope)

Pairs are binned by update scope in `targets/benign/pairs_binned.csv` and
`targets/benign/pairs_binned.txt`. The current buckets are:

- `major`, `minor`, `patch`, `build`
  - Determined by the first numeric token that changes in dotted versions
    (e.g., `1.2.3.4` is treated as patch/build depending on the first differing
    position). Dotted3+ versions are included here.
- `other`
  - Everything else (digits-only build numbers, underscore suffixes, cross-arch
    variants, date-like versions, etc.).

Use `targets/benign/scripts/bin_pairs.py` to regenerate bucketed outputs after
updating the manifest or pairs list.

## Bucket Builds

To extract a specific bucket into its own directory with `pairs.csv`,
`pairs_binned.csv`, `pairs.txt`, and a bucket-specific `manifest.csv`:

```
python targets/benign/scripts/build_bucket.py --bucket major
```

This writes to `targets/benign/buckets/<bucket>/` by default.
