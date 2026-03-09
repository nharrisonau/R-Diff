# R-Diff: Benchmark for Detection of Backdoors in Firmware Updates

## About

R-Diff is built on top of the upstream [ROSARUM](https://github.com/binsec/rosarum)
pipeline. The original project focuses on dynamic backdoor detection; this extends the pipelines
to study **differential (delta-scan) static analysis of software updates** and backdoors introduced as part of updates.

Every pipeline now ships with multiple build flavors:

- _safe_: a backdoor-free build of the current version;
- _backdoored_: the current version with the backdoor enabled;
- _prev-safe_: a build of the target's configured `previous/` source tree, used for static diffs;
- _baseline_: the collected configured baseline build used for static diffs.

Each target keeps two source trees: `original/` for the current release and `previous/` for the
configured `prev-safe` comparison build. The `prev-safe` variant is built from `previous/`, while
`safe` and `backdoored` are built from `original/` (with or without the backdoor patch).

Baseline builds reuse a single `baseline-src/` checkout per target and stage the selected
artifact under `baseline-artifacts/<version>/`, recorded in `local_outputs/baselines.csv`.
Collected outputs are flattened under `outputs/targets/{normal,stripped}/<group>/<target>/baseline/<binary>`.
Baseline selection is curated per target via `pipeline/baselines_config.json`:

- `version` pins the single baseline version used for that target.
- `mode` chooses whether that exact version is resolved from upstream git tags or copied from a
  local manual baseline build.
- `artifact_relpath` explicitly declares which built binary/object to stage and collect for that target.
- source provenance is pinned in `pipeline/sources.lock.json` and verified by
  `pipeline/scripts/verify_sources.py`.

To avoid repeated work, `pipeline/scripts/build_baselines.py` also reads prior failed rows
from `local_outputs/baselines.csv` and skips retrying the same exact version on subsequent runs.
This replaces the upstream `ground-truth` instrumentation so tools can reason directly about the code
delta that introduced the backdoor across release updates. Because many payloads remain
dangerous, **use a containerized environment** (e.g., Docker) when building or running binaries.

### Benchmark Layout

Targets are split into groups under [`targets/`](./targets/):

- [`targets/authentic/`](./targets/authentic/) contains authentic backdoor
  pipelines intended for direct analysis.
- [`targets/synthetic/`](./targets/synthetic/) contains synthetic backdoor
  pipelines intended for direct analysis.

For active-set trigger and payload summaries, see [`docs/backdoor-audit.md`](./docs/backdoor-audit.md).

Each target directory follows a consistent layout (`original/`, `previous/`, `patches/`, Makefile
with `safe`, `backdoored` and `prev-safe` rules, plus a per-target README describing the trigger for the backdoor).

### Benchmark Summary

The active target set is defined by `pipeline/baselines_config.json` and currently
contains 50 targets (5 authentic, 45 synthetic).
Each target stages exactly one configured baseline in addition to `prev-safe` for update comparison.

#### Authentic Backdoor Samples

| Target | Current | CVE | Backdoor behavior |
| --- | --- | --- | --- |
| `php-8.1.0-dev` | 8.1.0 | N/A | command execution via crafted HTTP header |
| `proftpd-1.3.3c` | 1.3.3c | CVE-2010-4221 | command execution via hidden FTP command |
| `unrealircd-3.2.8.1` | 3.2.8.1 | N/A | command execution via crafted IRC packet |
| `vsftpd-2.3.4` | 2.3.4 | CVE-2011-2523 | authentication bypass with shell listener |
| `xz-5.6.1` | 5.6.1 | CVE-2024-3094 | build-time policy/verification bypass |

#### Synthetic Backdoor Samples

| Target | Current | Backdoor behavior |
| --- | --- | --- |
| `dropbear-2024.86` | 2024.86 | authentication bypass |
| `dropbear-2025.89` | 2025.89 | authentication bypass (split-key variant) |
| `dropbear-2025.89-II` | 2025.89 | authentication bypass (multi-attempt variant) |
| `curl-8.18.0` | 8.18.0 | command execution |
| `dnsmasq-2.92` | 2.92 | policy/verification bypass |
| `expat-2.7.4` | 2.7.4 | policy/verification bypass |
| `json-c-0.18` | 0.18 | policy/verification bypass |
| `libarchive-3.8.5` | 3.8.5 | data disclosure |
| `libpng-1.6.43` | 1.6.43 | command execution |
| `libpng-1.6.54` | 1.6.54 | command execution (staged metadata) |
| `libpng-1.6.54-II` | 1.6.54 | integrity tampering |
| `libsndfile-1.2.2` | 1.2.2 | command execution |
| `libtiff-4.3.0` | 4.3.0 | command execution |
| `libtiff-4.7.1` | 4.7.1 | command execution (build-gated) |
| `libtiff-4.7.1-II` | 4.7.1 | integrity tampering |
| `libxml2-2.15.1` | 2.15.1 | command execution |
| `libxml2-2.15.1-II` | 2.15.1 | policy/verification bypass |
| `libxml2-2.9.12` | 2.9.12 | command execution |
| `libyaml-0.2.5` | 0.2.5 | integrity tampering |
| `lighttpd-1.4.82` | 1.4.82 | integrity tampering |
| `lua-5.4.7` | 5.4.7 | data disclosure |
| `nginx-1.29.5` | 1.29.5 | command execution |
| `openssh-10.2p1` | 10.2p1 | authentication bypass |
| `openssl-3.0.0` | 3.0.0 | command execution |
| `openssl-3.0.14` | 3.0.14 | policy/verification bypass |
| `openssl-3.3.4` | 3.3.4 | policy/verification bypass |
| `openssl-3.6.1` | 3.6.1 | data disclosure |
| `openssl-3.6.1-II` | 3.6.1 | policy/verification bypass |
| `openssl-3.6.1-III` | 3.6.1 | policy/verification bypass |
| `php-8.0.20` | 8.0.20 | command execution |
| `php-8.5.2` | 8.5.2 | policy/verification bypass |
| `php-8.5.2-II` | 8.5.2 | command execution |
| `php-8.5.2-III` | 8.5.2 | policy/verification bypass |
| `poppler-21.07.0` | 21.07.0 | command execution |
| `poppler-26.02.0` | 26.02.0 | command execution |
| `poppler-26.02.0-II` | 26.02.0 | command execution |
| `sqlite3-3.37.0-I` | 3.37.0 | command execution |
| `sqlite3-3.37.0-II` | 3.37.0 | policy/verification bypass |
| `sqlite3-3.37.0-III` | 3.37.0 | data disclosure |
| `sqlite3-3.37.0-IV` | 3.37.0 | integrity tampering |
| `sudo-1.9.15p5` | 1.9.15p5 | authentication bypass |
| `sudo-1.9.16` | 1.9.16 | authentication bypass |
| `sudo-1.9.16p2` | 1.9.16p2 | authentication bypass |
| `sudo-1.9.16p2-II` | 1.9.16p2 | authentication bypass |
| `zstd-1.5.7` | 1.5.7 | data disclosure |


### Ground-truth metadata

Each sample README now lists the backdoored function and includes a placeholder for its OXIDE
address. Fill in the OXIDE address once you confirm the ground truth for that function so the
location references stay stable across decompilers and analysis tools.

## Installation

### Docker workflow

We **highly** recommend using R-Diff in a
[Docker](https://docs.docker.com/get-started/) container, since some backdoors may carry payloads
that can affect your machine (e.g., by removing the `/home/` directory).

Before using the helper scripts, make sure that you have cloned **all of the submodules** used in
this repo. You can do this either by cloning the repo with `--recurse-submodules`, or by running
`git submodule update --init --recursive` post-cloning.

Build the Docker image with:

```bash
./build.sh
```

To build a single sample image variant, pass the target path:

```bash
./build.sh synthetic/libpng-1.6.43
```

Run the resulting container with:

```bash
./run.sh
```

`build.sh` uses the image name from `IMAGE`, and `run.sh` wraps `docker run -ti --rm $(cat IMAGE)`.
