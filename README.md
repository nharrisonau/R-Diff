# R-Diff: Benchmark for Detection of Backdoors in Firmware Updates

## About

R-Diff is built on top of the upstream [ROSARUM](https://github.com/binsec/rosarum)
pipeline. The original project focuses on dynamic backdoor detection; this extends the pipelines
to study **static analysis of software updates** and backdoors introduced as part of updates.

Every pipeline now ships with multiple build flavors:

- _safe_: a backdoor-free build of the current version;
- _backdoored_: the current version with the backdoor enabled;
- _prev-safe_: a build of the previous release of the software, used as a baseline for static diffs;
- _baseline/<version>_: additional historical baseline builds (patch and minor updates) used to
  evaluate analysis difficulty as the distance between versions increases.

Each target keeps two source trees: `original/` for the current release and `previous/` for the
immediate baseline. The `prev-safe` variant is built from `previous/`, while `safe` and `backdoored`
are built from `original/` (with or without the backdoor patch).

For multi-baseline evaluation, historical baselines are built by reusing a single `baseline-src/`
checkout per target and switching tags between builds. Built binaries are staged in
`baseline-artifacts/<version>/` and recorded in `local_outputs/baselines.csv`.
Baseline selection is curated per target via `pipeline/baselines_config.json`:

- `min_version` sets the oldest version to consider for that target.
- `exclude_versions` removes known outlier tags that are incompatible with the fixed build recipe.
- `artifact_relpath` explicitly declares which built binary/object to stage and collect for that target.
- source provenance is pinned in `pipeline/sources.lock.json` and verified by
  `pipeline/scripts/verify_sources.py`.

To avoid repeated work, `pipeline/scripts/build_baselines.py` also reads prior failed rows
from `local_outputs/baselines.csv` and skips those versions on subsequent runs.
This replaces the upstream `ground-truth` instrumentation so tools can reason directly about the code
delta that introduced the backdoor across multiple historical baselines. Because many payloads remain
dangerous, **use a containerized environment** (e.g., Docker) when building or running binaries.

### Benchmark layout

Targets are split into groups under [`targets/`](./targets/):

- [`targets/authentic/`](./targets/authentic/) contains authentic backdoor
  pipelines intended for direct analysis.
- [`targets/synthetic/`](./targets/synthetic/) contains synthetic backdoor
  pipelines intended for direct analysis.

For per-sample update coverage (current version, immediate baseline, and historical baseline windows),
see [`docs/updates.md`](./docs/updates.md).

Each target directory follows a consistent layout (`original/`, `previous/`, `patches/`, Makefile
with `safe`, `backdoored` and `prev-safe` rules, plus a per-target README describing how to trigger
its backdoor).

### Track workflow map

#### Backdoor track

- **Sources**: git submodules under `targets/{authentic,synthetic}/*/{original,previous}`, pinned in
  `pipeline/sources.lock.json`.
- **Build**: `make -C pipeline current` (or `make -C pipeline baselines` for historical baselines).
- **Outputs**: `outputs/targets/{normal,stripped}/...` plus `outputs/targets/reports/baselines_report.csv`.
- **Evaluation unit**: compare `backdoored` against `prev-safe` and additional historical baselines.

### Benchmark summary

The active target set is defined by `pipeline/baselines_config.json` and currently
contains 44 targets (3 authentic, 41 synthetic).
`Baselines (#)` below counts baseline versions available per target (including `prev-safe`).

#### Authentic backdoor samples

| Target | Current | Baselines (#) | Backdoor behavior |
| --- | --- | --- | --- |
| `php-8.1.0-dev` | 8.1.0 | 30 | hidden command, hardcoded credentials |
| `proftpd-1.3.3c` | 1.3.3c | 1 | hidden command |
| `vsftpd-2.3.4` | 2.3.4 | 1 | hardcoded credentials |

#### Synthetic backdoor samples

| Target | Current | Baselines (#) | Backdoor behavior |
| --- | --- | --- | --- |
| `dropbear-2024.86` | 2024.86 | 2 | hard-coded authentication key |
| `dropbear-2025.89` | 2025.89 | 2 | hard-coded authentication key (split/decoded) |
| `dropbear-2025.89-II` | 2025.89 | 2 | multi-attempt auth sequence + split key-fragment backdoor |
| `curl-8.18.0` | 8.18.0 | 1 | redirect/auth transition trigger with hidden header-leak marker |
| `dnsmasq-2.92` | 2.92 | 1 | DHCP option order + client-id trigger with lease-override marker |
| `expat-2.7.4` | 2.7.4 | 1 | DOCTYPE/namespace trigger with parser-policy divergence |
| `json-c-0.18` | 0.18 | 1 | key-order + parse-mode trigger with hidden privilege-flag marker |
| `libarchive-3.8.5` | 3.8.5 | 1 | archive-option + metadata trigger with extraction-policy marker |
| `libpng-1.6.43` | 1.6.43 | 10 | hidden command |
| `libpng-1.6.54` | 1.6.54 | 2 | staged hidden command |
| `libpng-1.6.54-II` | 1.6.54 | 2 | two-stage metadata trigger with decode-path sabotage |
| `libsndfile-1.2.2` | 1.2.2 | 4 | hidden command |
| `libtiff-4.3.0` | 4.3.0 | 2 | hidden command |
| `libtiff-4.7.1` | 4.7.1 | 1 | build-time gated runtime trigger |
| `libtiff-4.7.1-II` | 4.7.1 | 1 | malformed-directory trigger with codec interaction gate |
| `libxml2-2.15.1` | 2.15.1 | 2 | structural XML trigger |
| `libxml2-2.15.1-II` | 2.15.1 | 2 | parser recovery + namespace-collision trigger |
| `libxml2-2.9.12` | 2.9.12 | 13 | hidden command |
| `libyaml-0.2.5` | 0.2.5 | 1 | anchor/alias + tag-order trigger with loader-policy marker |
| `lighttpd-1.4.82` | 1.4.82 | 1 | path-normalization + header trigger with auth-bypass marker |
| `lua-5.4.7` | 5.4.7 | 1 | hidden command |
| `openssl-3.0.0` | 3.0.0 | 7 | hidden command |
| `openssl-3.6.1` | 3.6.1 | 1 | key/intermediate leak trigger |
| `openssl-3.6.1-II` | 3.6.1 | 1 | certificate-chain verification bypass |
| `openssl-3.6.1-III` | 3.6.1 | 1 | revocation verification bypass |
| `php-8.0.20` | 8.0.20 | 19 | hidden command |
| `php-8.5.2` | 8.5.2 | 41 | unserialize policy bypass |
| `php-8.5.2-II` | 8.5.2 | 41 | hidden command execution path |
| `php-8.5.2-III` | 8.5.2 | 41 | one-shot auth/policy bypass |
| `poppler-21.07.0` | 21.07.0 | 7 | hidden command |
| `poppler-26.02.0` | 26.02.0 | 1 | malformed-object error-path trigger |
| `poppler-26.02.0-II` | 26.02.0 | 1 | damaged-xref fallback + split metadata marker |
| `sqlite3-3.37.0-I` | 3.37.0 | 1 | hidden command |
| `sqlite3-3.37.0-II` | 3.37.0 | 1 | authorizer policy bypass |
| `sqlite3-3.37.0-III` | 3.37.0 | 1 | hidden file-read capability |
| `sqlite3-3.37.0-IV` | 3.37.0 | 1 | attacker-triggered silent data tampering |
| `sudo-1.9.15p5` | 1.9.15p5 | 39 | hardcoded credentials |
| `sudo-1.9.16` | 1.9.16 | 40 | hardcoded credential hash |
| `sudo-1.9.16p2` | 1.9.16p2 | 42 | context-gated hardcoded credentials |
| `sudo-1.9.16p2-II` | 1.9.16p2 | 42 | environment + argv + tty + policy-state gated backdoor |
| `zstd-1.5.7` | 1.5.7 | 1 | frame-flags + dictionary trigger with integrity-bypass marker |


### Ground-truth metadata

Each sample README now lists the backdoored function and includes a placeholder for its OXIDE
address. Fill in the OXIDE address once you confirm the ground truth for that function so the
location references stay stable across decompilers and analysis tools.

## Installation

### Building the Docker image

We **highly** recommend using R-Diff in a
[Docker](https://docs.docker.com/get-started/) container, since some backdoors may carry payloads
that can affect your machine (e.g., by removing the `/home/` directory).

If you wish to build the Docker image on your machine, you can use the helper `build.sh` script,
which will build the image using the name from the `IMAGE` file. See the script itself for more
information.

Before running the script (or simply `docker build ...`), make sure that you have cloned **all of
the submodules** used in this repo. You can do this either by cloning the repo with
`--recurse-submodules`, or by running `git submodule update --init` post-cloning.

### Building from source

**WARNING: running the target programs in a native, unprotected environment may endanger the state
of your machine. We highly recommend using a Docker container as described above.**

#### Backdoor track (build + collect)

- To build all targets (current variants only), run `make -C pipeline current`.
- To additionally build historical baselines (best-effort) and write `local_outputs/baselines.csv`,
  run `make -C pipeline baselines`.
- By default, baseline collection is limited to the immediate prior release (`BASELINE_LIMIT=1`).
  Use `BASELINE_LIMIT=0` to build the full configured baseline history.
- To make target build failures fail fast instead of best-effort, add `STRICT=1` (for example:
  `make -C pipeline baselines STRICT=1`).
- To tune historical baseline windows, edit `pipeline/baselines_config.json` (`min_version`
  and `exclude_versions`).
- To build authentic targets only, run `make -C pipeline authentic`.
- To build synthetic targets only, run `make -C pipeline synthetic`.
- To build a specific target (e.g., Sudo), run `make -C targets/synthetic/sudo-1.9.15p5`.
- To build a specific variant, run the relevant target
  (e.g., `make -C targets/synthetic/sudo-1.9.15p5 prev-safe`).

Collected binaries are written under `outputs/targets/{normal,stripped}/...` by `pipeline/collect_samples.sh`.
Per-sample baseline collection results (including failed baseline versions) are written to
`outputs/targets/reports/baselines_report.csv`.

#### Backdoor track status

The exact number of collected historical baselines depends on the current
`pipeline/baselines_config.json` and host build environment.
After each run, use `outputs/targets/reports/baselines_report.csv` as the source of truth for:

- per-target collected baseline versions,
- per-target failed baseline versions (if any), and
- total collected vs. failed baseline counts.

## Usage

### Reproducing the backdoors

Instructions on how to run all of the variants can be found in the root directory of each backdoor
sample. Generally, for each sample, you'll want to first build it (if it's not built):

```console
$ make -C targets/synthetic/sudo-1.9.15p5  # or `... safe`, `... backdoored`, `... prev-safe`
```

Then, you need to perform any additional setup that may be needed (e.g., copying files to specific
directories):

```console
$ make setup
```

Once you're done with the target program, to make sure other programs are not affected, you should
_undo_ the setup:

```console
$ make teardown
```

### Evaluating a backdoor detection method on R-Diff

This pipeline is geared toward static analysis that reason about **updates**. The intended
workflow is to compare the `backdoored` variant against:

- `prev-safe` (immediate previous release), and
- additional historical baselines (`baseline/<version>`) to test increasing update distances.

The `safe` variant lets you contrast the intended current release without the backdoor change.
A typical evaluation loop looks like this:

1. Build the relevant variants (e.g., `make backdoored prev-safe` in the target directory, plus
   `make -C pipeline all` to build historical baselines).
2. Run your analyzer on `backdoored/` and one or more baseline trees (`prev-safe/` and staged
   historical baselines from `baseline-artifacts/<version>/`, or the collected
   `outputs/targets/.../baseline/<version>/`) to detect suspicious code additions between releases.
3. Use `safe/` as a reference to check whether the suspicious additions disappear once the backdoor
   is removed from the current release.

### Scoring Detector Outputs

R-Diff includes a scoring utility that evaluates backdoor detection performance.

Generate a template of all evaluation units:

```console
$ python3 evaluation/score_predictions.py --template-out local_outputs/eval/prediction_template.csv
```

Score a completed predictions file:

```console
$ python3 evaluation/score_predictions.py \
    --predictions local_outputs/eval/predictions.csv \
    --out-json local_outputs/eval/metrics.json \
    --out-csv local_outputs/eval/scored_units.csv
```

See `docs/evaluation-metrics.md` for unit definitions, input schema, and metric formulas.
