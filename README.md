# R-Diff: Benchmark for Detection of Backdoors in Firmware Updates

## About

R-Diff is built on top of the upstream [ROSARUM](https://github.com/binsec/rosarum)
benchmark. The original project focuses on dynamic backdoor detection; this extends the benchmarks
to study **static analysis of software updates** and backdoors introduced as part of updates.

Every benchmark now ships with three build flavors:

- _safe_: a backdoor-free build of the current version;
- _backdoored_: the current version with the backdoor enabled;
- _prev-safe_: a build of the previous release of the software, used as a baseline for static diffs.

Each target keeps two source trees: `original/` for the current release and `previous/` for the
baseline. The `prev-safe` variant is built from `previous/`, while `safe` and `backdoored` are built
from `original/` (with or without the backdoor patch). This replaces the upstream `ground-truth`
instrumentation so that tools can reason directly about the code delta that introduced the
backdoor. Because many payloads remain dangerous, **use a containerized environment** (e.g., Docker)
when building or running binaries.

### Benchmark layout

Targets are split into malicious and benign groups under [`targets/`](./targets/):

- [`targets/malicious/authentic/`](./targets/malicious/authentic/) contains authentic backdoor
  benchmarks intended for direct analysis.
- [`targets/malicious/synthetic/`](./targets/malicious/synthetic/) contains synthetic backdoor
  benchmarks intended for direct analysis.
- [`targets/benign/<product>/<version>/rootfs`](./targets/benign/) contains extracted benign
  firmware root filesystems used for false-positive evaluation.

Each target directory follows a consistent layout (`original/`, `previous/`, `patches/`, Makefile
with `safe`, `backdoored` and `prev-safe` rules, plus a per-target README describing how to trigger
its backdoor).

### Benchmark summary

#### Authentic benchmarks

| Name        | Backdoor description                                                       |
| ----------- | ---------------------------------------------------------------------------|
| PHP         | `User-Agentt: zerodium<CMD>` HTTP header executes arbitrary PHP code       |
| ProFTPD     | Secret FTP `HELP ACIDBITCHEZ` command spawns a root shell                  |
| vsFTPd      | FTP usernames containing `":)"` lead to a root shell                       |

#### Synthetic benchmarks

| Name                      | Backdoor description                                                 |
| --------------------------| -------------------------------------------------------------------- |
| dropbear                  | Hard-coded SSH public key bypasses public-key authentication         |
| sudo                      | Hardcoded credentials bypass authentication                          |
| libpng                    | Secret image metadata values enable command execution                |
| libsndfile                | Secret sound file metadata value triggers home directory encryption  |
| libtiff                   | Secret image metadata value enables command execution                |
| libxml2                   | Secret XML node format enables command execution                     |
| Lua                       | Specific string values in script enable reading from filesystem      |
| OpenSSL                   | Secret bignum exponentiation string enables command execution        |
| PHP unserialize           | Specific string values in serialized object enable command execution |
| Poppler                   | Secret comment character in PDF enables command execution            |
| SQLite3                   | Secret SQL keyword enables removal of home directory                 |

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

Build orchestration mirrors the `targets/` layout:

- To build all malicious targets, run `make -C targets malicious`.
- To build malicious authentic targets only, run `make -C targets malicious-authentic`.
- To build malicious synthetic targets only, run `make -C targets malicious-synthetic`.
- To build a specific target (e.g., Sudo), run `make -C targets/malicious/synthetic/sudo-1.9.15p5`.
- To build a specific variant, run the relevant target
  (e.g., `make -C targets/malicious/synthetic/sudo-1.9.15p5 prev-safe`).

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

Benign samples are stored as extracted root filesystems under:

```
targets/benign/<product>/<version>/rootfs
```

The ingestion scripts under `targets/benign/scripts` populate these from the
vendored benign firmware URL lists in `targets/benign/sources`.

After ingestion, generate adjacent version pairs with `targets/benign/scripts/build_pairs.py` to
create `targets/benign/pairs.csv` for benign diff evaluation.
See `targets/benign/README.md` for bucket definitions and per-bucket build helpers.

### Evaluating a backdoor detection method on R-Diff

This benchmark is geared toward static analysis that reason about **updates**. The intended
workflow is to compare the `backdoored` variant against `prev-safe` (previous release) to isolate the
code that introduced the backdoor, while the `safe` variant lets you contrast the intended current
release without the malicious change. A typical evaluation loop looks like this:

1. Build the relevant variants (e.g., `make backdoored prev-safe` in the target directory).
2. Run your analyzer on `backdoored/` and `prev-safe/` (sources or binaries, depending on the tool) to
   detect suspicious code additions between releases.
3. Use `safe/` as a reference to check whether the suspicious additions disappear once the backdoor is
   removed from the current release.
