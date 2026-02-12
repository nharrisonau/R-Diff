# Malicious Sample Update Coverage

This document describes update coverage for each active malicious sample in R-Diff.

Source of truth:

- `targets/malicious/baselines_config.json` (active target list and baseline constraints)
- `targets/malicious/scripts/list_baselines.py` (tag-based baseline resolution)
- `targets/malicious/scripts/build_baselines.py` (build/skip behavior)
- `targets/malicious/sources.lock.json` (source provenance pins; regenerate with
  `targets/malicious/scripts/update_sources_lock.py`)

Baseline selection policy:

- `mode: manual` uses explicit `manual_baselines`.
- `mode: git_tags` resolves historical versions from matching tags.
- `min_version` and `exclude_versions` in `baselines_config.json` constrain historical windows.
- Previously failed baseline versions recorded in `local_outputs/malicious/baselines.csv` are skipped on
  subsequent builds.

## Active Samples (Build Matrix)

| Group | Sample | Current | Mode | Immediate Baseline | Historical Baselines | Constraints |
| --- | --- | --- | --- | --- | --- | --- |
| synthetic | dropbear2024-86 | 2024.86 | git_tags | 2024.85 | 2 | none |
| synthetic | libpng-1.6.43 | 1.6.43 | git_tags | 1.6.42 | 10 | `min_version=1.6.32`, `exclude_versions=[1.6.38]` |
| synthetic | libsndfile-1.2.2 | 1.2.2 | git_tags | 1.2.1 | 4 | `min_version=1.0.31` |
| synthetic | libtiff-4.3.0 | 4.3.0 | git_tags | 4.2.0 | 2 | `min_version=4.1.0` |
| synthetic | libxml2-2.9.12 | 2.9.12 | git_tags | 2.9.11 | 13 | `min_version=2.8.0` |
| synthetic | lua-5.4.7 | 5.4.7 | manual | 5.4.6 | 1 | manual only |
| synthetic | openssl-3.0.0 | 3.0.0 | git_tags | 3.0.0-beta2 | 7 | `min_version=3.0.0-alpha13` |
| synthetic | php-8.0.20 | 8.0.20 | git_tags | 8.0.19 | 19 | none |
| synthetic | poppler-21.07.0 | 21.07.0 | git_tags | 21.06.1 | 7 | none |
| synthetic | sqlite3-3.37.0 | 3.37.0 | manual | 3.36.0 | 1 | manual only |
| synthetic | sudo-1.9.15p5 | 1.9.15p5 | git_tags | 1.9.15p4 | 39 | `min_version=1.9.1`, `exclude_versions=[1.9.4]` |
| synthetic | sudo-1.6.1 | 1.6.1 | git_tags | 1.6.0 | 13 | `min_version=1.3.0` |
| authentic | php-8.1.0-dev | 8.1.0 | git_tags | 8.0.30 | 30 | none |
| authentic | proftpd-1.3.3c | 1.3.3c | manual | 1.3.3b | 1 | manual only |
| authentic | vsftpd-2.3.4 | 2.3.4 | manual | 2.3.3 | 1 | manual only |

## Per-Sample Baseline Versions

### Authentic

- `php-8.1.0-dev` (current `8.1.0`):
  - `8.0.30, 8.0.29, 8.0.28, 8.0.27, 8.0.26, 8.0.25, 8.0.24, 8.0.23, 8.0.22, 8.0.21, 8.0.20, 8.0.19, 8.0.18, 8.0.17, 8.0.16, 8.0.15, 8.0.14, 8.0.13, 8.0.12, 8.0.11, 8.0.10, 8.0.9, 8.0.8, 8.0.7, 8.0.6, 8.0.5, 8.0.3, 8.0.2, 8.0.1, 8.0.0`
- `proftpd-1.3.3c` (current `1.3.3c`):
  - `1.3.3b`
- `vsftpd-2.3.4` (current `2.3.4`):
  - `2.3.3`

### Synthetic

- `dropbear2024-86` (current `2024.86`):
  - `2024.85, 2024.84`
- `libpng-1.6.43` (current `1.6.43`, constrained by `min_version=1.6.32`, excluding `1.6.38`):
  - `1.6.42, 1.6.41, 1.6.40, 1.6.39, 1.6.37, 1.6.36, 1.6.35, 1.6.34, 1.6.33, 1.6.32`
- `libsndfile-1.2.2` (current `1.2.2`, constrained by `min_version=1.0.31`):
  - `1.2.1, 1.2.0, 1.1.0, 1.0.31`
- `libtiff-4.3.0` (current `4.3.0`, constrained by `min_version=4.1.0`):
  - `4.2.0, 4.1.0`
- `libxml2-2.9.12` (current `2.9.12`, constrained by `min_version=2.8.0`):
  - `2.9.11, 2.9.10, 2.9.9, 2.9.8, 2.9.7, 2.9.6, 2.9.5, 2.9.4, 2.9.3, 2.9.2, 2.9.1, 2.9.0, 2.8.0`
- `lua-5.4.7` (current `5.4.7`, manual):
  - `5.4.6`
- `openssl-3.0.0` (current `3.0.0`, constrained by `min_version=3.0.0-alpha13`):
  - `3.0.0-beta2, 3.0.0-beta1, 3.0.0-alpha17, 3.0.0-alpha16, 3.0.0-alpha15, 3.0.0-alpha14, 3.0.0-alpha13`
- `php-8.0.20` (current `8.0.20`):
  - `8.0.19, 8.0.18, 8.0.17, 8.0.16, 8.0.15, 8.0.14, 8.0.13, 8.0.12, 8.0.11, 8.0.10, 8.0.9, 8.0.8, 8.0.7, 8.0.6, 8.0.5, 8.0.3, 8.0.2, 8.0.1, 8.0.0`
- `poppler-21.07.0` (current `21.07.0`):
  - `21.06.1, 21.06.0, 21.05.0, 21.04.0, 21.03.0, 21.02.0, 21.01.0`
- `sqlite3-3.37.0` (current `3.37.0`, manual):
  - `3.36.0`
- `sudo-1.9.15p5` (current `1.9.15p5`, constrained by `min_version=1.9.1`, excluding `1.9.4`):
  - `1.9.15p4, 1.9.15p3, 1.9.15p2, 1.9.15p1, 1.9.15, 1.9.14p3, 1.9.14p2, 1.9.14p1, 1.9.14, 1.9.13p3, 1.9.13p2, 1.9.13p1, 1.9.13, 1.9.12p2, 1.9.12p1, 1.9.12, 1.9.11p3, 1.9.11p2, 1.9.11p1, 1.9.11, 1.9.10, 1.9.9, 1.9.8p2, 1.9.8p1, 1.9.8, 1.9.7p2, 1.9.7p1, 1.9.7, 1.9.6p1, 1.9.6, 1.9.5p2, 1.9.5p1, 1.9.5, 1.9.4p2, 1.9.4p1, 1.9.3p1, 1.9.3, 1.9.2, 1.9.1`
- `sudo-1.6.1` (current `1.6.1`, constrained by `min_version=1.3.0`):
  - `1.6.0, 1.5.9, 1.5.8, 1.5.7, 1.5.6, 1.5.4, 1.5.3, 1.5.2, 1.5.1, 1.5.0, 1.4.0, 1.3.1, 1.3.0`

## Notes

- The active malicious set is defined only by `targets/malicious/baselines_config.json` (15 targets).
