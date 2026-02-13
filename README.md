# R-Diff: Benchmark for Detection of Backdoors in Firmware Updates

## About

R-Diff is built on top of the upstream [ROSARUM](https://github.com/binsec/rosarum)
benchmark. The original project focuses on dynamic backdoor detection; this extends the benchmarks
to study **static analysis of software updates** and backdoors introduced as part of updates.

Every benchmark now ships with multiple build flavors:

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
`baseline-artifacts/<version>/` and recorded in `local_outputs/malicious/baselines.csv`.
Baseline selection is curated per target via `targets/malicious/baselines_config.json`:

- `min_version` sets the oldest version to consider for that target.
- `exclude_versions` removes known outlier tags that are incompatible with the fixed build recipe.
- source provenance is pinned in `targets/malicious/sources.lock.json` and verified by
  `targets/malicious/scripts/verify_sources.py`.

To avoid repeated work, `targets/malicious/scripts/build_baselines.py` also reads prior failed rows
from `local_outputs/malicious/baselines.csv` and skips those versions on subsequent runs.
This replaces the upstream `ground-truth` instrumentation so tools can reason directly about the code
delta that introduced the backdoor across multiple historical baselines. Because many payloads remain
dangerous, **use a containerized environment** (e.g., Docker) when building or running binaries.

### Benchmark layout

Targets are split into malicious and benign groups under [`targets/`](./targets/):

- [`targets/malicious/authentic/`](./targets/malicious/authentic/) contains authentic backdoor
  benchmarks intended for direct analysis.
- [`targets/malicious/synthetic/`](./targets/malicious/synthetic/) contains synthetic backdoor
  benchmarks intended for direct analysis.
- [`targets/benign/`](./targets/benign/) contains benign firmware metadata and adjacent-version pair
  lists used for false-positive evaluation. Extracted root filesystems are generated on demand and
  are not tracked by default.

For per-sample malicious update coverage (current version, immediate baseline, and historical
baseline windows), see [`docs/malicious-updates.md`](./docs/malicious-updates.md).
For benign pair construction and bucketing rules, see [`docs/benign-update-pairs.md`](./docs/benign-update-pairs.md).

Each target directory follows a consistent layout (`original/`, `previous/`, `patches/`, Makefile
with `safe`, `backdoored` and `prev-safe` rules, plus a per-target README describing how to trigger
its backdoor).

### Track workflow map

#### Malicious track

- **Sources**: git submodules under `targets/malicious/*/*/{original,previous}`, pinned in
  `targets/malicious/sources.lock.json`.
- **Build**: `make -C targets malicious` (or `make -C targets all` for historical baselines).
- **Outputs**: `outputs/v2/{normal,stripped}/...` plus `outputs/v2/reports/malicious_baselines_report.csv`.
- **Evaluation unit**: compare `backdoored` against `prev-safe` and additional historical baselines.

#### Benign track

- **Sources**: vendored URL manifests under `targets/benign/sources/...`.
- **Build**: metadata generation via `targets/benign/scripts/generate_lists.py` and `bin_pairs.py`.
- **Outputs**: `targets/benign/{manifest.csv,pairs.csv,pairs_binned.csv}` plus optional
  `local_outputs/benign/...` bucket or extraction artifacts.
- **Evaluation unit**: adjacent benign update pairs bucketed as `major/minor/patch/build/other`.

### Benchmark summary

The active malicious set is defined by `targets/malicious/baselines_config.json` and currently
contains 15 targets (3 authentic, 12 synthetic).
`Baselines (#)` below counts baseline versions available per target (including `prev-safe`).

#### Authentic malicious samples

| Target | Current | Baselines (#) | Backdoor behavior |
| --- | --- | --- | --- |
| `php-8.1.0-dev` | 8.1.0 | 30 | `User-Agentt: zerodium<CMD>` header executes arbitrary PHP code |
| `proftpd-1.3.3c` | 1.3.3c | 1 | Secret FTP `HELP ACIDBITCHEZ` command spawns a root shell |
| `vsftpd-2.3.4` | 2.3.4 | 1 | FTP usernames containing `":)"` lead to a root shell |

#### Synthetic malicious samples

| Target | Current | Baselines (#) | Backdoor behavior |
| --- | --- | --- | --- |
| `dropbear2024-86` | 2024.86 | 2 | Hard-coded SSH public key bypasses public-key authentication |
| `libpng-1.6.43` | 1.6.43 | 10 | Secret image metadata values enable command execution |
| `libsndfile-1.2.2` | 1.2.2 | 4 | Secret sound file metadata value triggers home directory encryption |
| `libtiff-4.3.0` | 4.3.0 | 2 | Secret image metadata value enables command execution |
| `libxml2-2.9.12` | 2.9.12 | 13 | Secret XML node format enables command execution |
| `lua-5.4.7` | 5.4.7 | 1 | Specific string values in script enable reading from filesystem |
| `openssl-3.0.0` | 3.0.0 | 7 | Secret bignum exponentiation string enables command execution |
| `php-8.0.20` | 8.0.20 | 19 | Specific string values in serialized object enable command execution |
| `poppler-21.07.0` | 21.07.0 | 7 | Secret comment character in PDF enables command execution |
| `sqlite3-3.37.0` | 3.37.0 | 1 | Secret SQL keyword enables removal of home directory |
| `sudo-1.9.15p5` | 1.9.15p5 | 39 | Hardcoded credentials bypass authentication |
| `sudo-1.6.1` | 1.6.1 | 13 | Hardcoded credentials bypass authentication |

#### Benign firmware corpus (tracked metadata snapshot)

Benign coverage is defined by:

- `targets/benign/manifest.csv`
- `targets/benign/pairs.csv`
- `targets/benign/pairs_binned.csv`

Current tracked snapshot:

- 1,849 manifest rows across 137 products.
- 1,712 adjacent update pairs (and 1,712 binned rows).

Bucket breakdown from `targets/benign/pairs_binned.csv`:

| Bucket | Pair count | Meaning |
| --- | ---: | --- |
| `major` | 163 | First differing numeric token is the major component (semver-like versions). |
| `minor` | 142 | First differing numeric token is the minor component (semver-like versions). |
| `patch` | 418 | First differing numeric token is the patch component (semver-like versions). |
| `build` | 1 | First differing numeric token appears after patch (build-level change). |
| `other` | 988 | Non-semver, cross-architecture, or unresolved version comparisons. |

See `targets/benign/README.md` and `docs/benign-update-pairs.md` for generation and bucketing
methodology.

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

#### Malicious track (build + collect)

- To build all malicious targets, run `make -C targets malicious`.
- To additionally build historical baselines (best-effort) and write `local_outputs/malicious/baselines.csv`,
  run `make -C targets all`.
- To make target build failures fail fast instead of best-effort, add `STRICT=1` (for example:
  `make -C targets all STRICT=1`).
- To tune historical baseline windows, edit `targets/malicious/baselines_config.json` (`min_version`
  and `exclude_versions`).
- To build malicious authentic targets only, run `make -C targets malicious-authentic`.
- To build malicious synthetic targets only, run `make -C targets malicious-synthetic`.
- To build a specific target (e.g., Sudo), run `make -C targets/malicious/synthetic/sudo-1.9.15p5`.
- To build a specific variant, run the relevant target
  (e.g., `make -C targets/malicious/synthetic/sudo-1.9.15p5 prev-safe`).

Collected binaries are written under `outputs/v2/{normal,stripped}/...` by `targets/collect_samples.sh`.
Per-sample malicious baseline collection results (including failed baseline versions) are written to
`outputs/v2/reports/malicious_baselines_report.csv`.

#### Malicious track status

The exact number of collected historical baselines depends on the current
`targets/malicious/baselines_config.json` and host build environment.
After each run, use `outputs/v2/reports/malicious_baselines_report.csv` as the source of truth for:

- per-target collected baseline versions,
- per-target failed baseline versions (if any), and
- total collected vs. failed baseline counts.

#### Benign track (metadata-first workflow)

Benign data in git consists of source URL metadata and derived pair lists:

- `targets/benign/manifest.csv`
- `targets/benign/pairs.csv`
- `targets/benign/pairs_binned.csv`

Regenerate benign metadata without downloading firmware:

```console
$ python3 targets/benign/scripts/generate_lists.py --overwrite
$ python3 targets/benign/scripts/bin_pairs.py
```

Optional extraction of root filesystems is performed through
`targets/benign/scripts/ingest_firmware_dataset.py` and written outside tracked sources.

## Usage

### Reproducing the backdoors

Instructions on how to run all of the variants can be found in the root directory of each backdoor
sample. Generally, for each sample, you'll want to first build it (if it's not built):

```console
$ make -C targets/malicious/synthetic/sudo-1.9.15p5  # or `... safe`, `... backdoored`, `... prev-safe`
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

### Benign firmware samples (false-positive evaluation)

Benign evaluation uses adjacent-version pairs generated from `targets/benign/manifest.csv`.
Pair metadata is stored in:

```
targets/benign/pairs.csv
targets/benign/pairs_binned.csv
```

Extracted root filesystems are optional runtime artifacts generated by
`targets/benign/scripts/ingest_firmware_dataset.py`; they are not tracked by default.

See `targets/benign/README.md` and `docs/benign-update-pairs.md` for pair sorting and bucket rules.

### Evaluating a backdoor detection method on R-Diff

This benchmark is geared toward static analysis that reason about **updates**. The intended
workflow is to compare the `backdoored` variant against:

- `prev-safe` (immediate previous release), and
- additional historical baselines (`baseline/<version>`) to test increasing update distances.

The `safe` variant lets you contrast the intended current release without the malicious change.
A typical evaluation loop looks like this:

1. Build the relevant variants (e.g., `make backdoored prev-safe` in the target directory, plus
   `make -C targets all` to build historical baselines).
2. Run your analyzer on `backdoored/` and one or more baseline trees (`prev-safe/` and staged
   historical baselines from `baseline-artifacts/<version>/`, or the collected
   `outputs/v2/.../baseline/<version>/`) to detect suspicious code additions between releases.
3. Use `safe/` as a reference to check whether the suspicious additions disappear once the backdoor
   is removed from the current release.

### Scoring Detector Outputs

R-Diff includes a scoring utility that evaluates both malicious detection and benign false positives.

Generate a template of all evaluation units:

```console
$ python3 targets/evaluation/score_predictions.py --template-out local_outputs/eval/prediction_template.csv
```

Score a completed predictions file:

```console
$ python3 targets/evaluation/score_predictions.py \
    --predictions local_outputs/eval/predictions.csv \
    --out-json local_outputs/eval/metrics.json \
    --out-csv local_outputs/eval/scored_units.csv
```

See `docs/evaluation-metrics.md` for unit definitions, input schema, and metric formulas.

## Project metadata

- Citation metadata: `CITATION.cff`
- Contribution workflow: `CONTRIBUTING.md`
- Publication preparation docs: `docs/release-checklist.md`, `docs/migration-notes.md`
