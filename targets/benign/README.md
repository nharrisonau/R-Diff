# Benign Firmware Samples

The benign track is metadata-first. Canonical tracked artifacts are:

```
targets/benign/manifest.csv
targets/benign/pairs.csv
targets/benign/pairs_binned.csv
```

Optional extracted root filesystems can be generated on demand and are not
tracked in git by default.

## Sources

The `targets/benign/sources` directory vendors the benign firmware URL lists
used to build this benchmark. These are the only active benign sources.

## Ingestion scripts

All supported workflows use scripts under `targets/benign/scripts`.
Legacy entrypoints under `targets/benign/sources/.../download.py` and
`targets/benign/sources/.../unpack.py` are deprecated wrappers.

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
  - Builds per-bucket manifests and pair lists under `local_outputs/benign/buckets/`.
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

```bash
python3 targets/benign/scripts/build_bucket.py --bucket major
```

This writes to `local_outputs/benign/buckets/<bucket>/` by default.

## Bucket Downloads

To download and unpack only the samples referenced by a specific bucket,
first build the bucket manifest, then ingest from that manifest:

```bash
python3 targets/benign/scripts/build_bucket.py --bucket major
python3 targets/benign/scripts/ingest_firmware_dataset.py \
  --manifest-in local_outputs/benign/buckets/major/manifest.csv \
  --manifest local_outputs/benign/buckets/major/manifest_downloaded.csv \
  --overwrite-manifest
```

This downloads firmware, extracts rootfs, and writes the output manifest to
`local_outputs/benign/buckets/<bucket>/manifest_downloaded.csv`.
