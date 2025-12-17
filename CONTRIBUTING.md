# Contributing to ROSARUM

Thank you for taking the time to contribute to the ROSARUM benchmark!

You can contribute in the two different backdoor categories (_authentic_ and _synthetic_).

## Setting up the development environment

In order to have a valid development environment, you need to have
[pre-commit](https://pre-commit.com) installed. Once that is done, you need to install the
pre-commit hooks on your clone of the repo by running:

```console
$ pre-commit install
```

**NOTE: you only need to do this once _per clone_ of the repo.**

## Contributing new backdoor samples

Please start by opening an issue in this repository describing the change you would like to make.
Once the discussion has converged, you can fork the repo, make changes and create a pull request
with your contribution. You should try to follow the existing structure of the repo.

### Backdoor sample directory name and placement

Component benchmarks should go under `/targets/components/{authentic,synthetic}/<name>/`, while
firmware images live under `/targets/firmware/synthetic/<name>/`. The `<name>` should be
unique to distinguish this backdoor from existing ones while also taking some care to
future-proof it. At the very minimum, it should be `<name>-<version>` for "desktop" software and
`<firmware/device>-<version>-<binary>` for binaries originating in firmware packages (as multiple
binaries may be contributed from the same firmware package).

### Source code

ROSARUM aims to store the _source code_ of the affected programs. This source code shall be stored
under a directory named `original/`, in the root directory of the backdoor sample. To support the
`prev-safe` baseline used for static diffing, you should also provide a `previous/` directory with
the version of the software immediately before the backdoor was introduced.

- **For authentic backdoors**: if you wish to contribute an _authentic_ backdoor sample found in a
  binary, you will need to reasonably reimplement the target program in source code (usually in C),
  so that it may be recompiled for any platform. This is the procedure that we followed to
  reimplement the existing authentic samples, and we used reverse-engineering tools such as
  [Ghidra](https://ghidra-sre.org/) to do so. In many cases, binaries originating in firmware are
  heavily based in existing open source projects (e.g., HTTP servers) with slight modifications, so
  reverse-engineering and reimplementing them is considerably easier. Note that the reimplementation
  does not have to be (and often _cannot_ be) exact, so long as it reasonably represents the
  original backdoor.
- **For synthetic backdoors**: if you wish to contribute a _synthetic_ backdoor, you should add the
  base source code of the target program as a
  [Git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules). This helps keep things clean
  and pins an exact version of the target software.

### Variant patches

To keep the malicious changes explicit and enable static diffing across releases, each target
includes a `patches/` directory applied on top of `original/` (current release) or `previous/`
(baseline release). A typical set of patches contains:

- `backdoored.patch`: applies to `original/` to enable the backdoor, ideally isolating the malicious
  logic that should surface in a code diff;
- `base.patch`: optional structural changes (e.g., fuzzing harnesses) that should be present in all
  variants for a fair comparison;
- `safe.patch`: optional clean-up changes if removing the backdoor requires more than omitting
  `backdoored.patch`.

In many cases only `backdoored.patch` (plus an optional `base.patch`) is sufficient. The `safe`
variant is built from `original/` without the backdoor, while `prev-safe` is built from
`previous/`, mirroring the state of the software before the backdoor landed.

### Makefile

You should follow the structure of the existing Makefiles. At a high level, your Makefile should
have at least 7 rules:

- `safe`, producing the _safe_ variant from `original/` without the backdoor;
- `backdoored`, producing the _backdoored_ variant from `original/` with the backdoor applied;
- `prev-safe`, producing the _prev-safe_ variant from `previous/` to act as the baseline release;
- `all`, producing all three variants;
- `clean`, removing any and all build artifacts;
- `setup`, setting up the environment needed by the program (e.g., by copying specific files to
  specific directories);
- `teardown`, essentially undoing what `setup` did to return back to the system's original state.

As you will notice in the existing Makefiles, each rule essentially copies the `original/` directory
(or `previous/` for `prev-safe`), applies the relevant patches and then builds the target program
based on the build system of each project. **The default target platform is
`x86_64-pc-linux-gnu`**. If you wish to provide other targets, see
[_Contributing new versions for existing backdoor samples_](#contributing-new-versions-for-existing-backdoor-samples)
below.

### README

You should have a `README.md` file following the structure of the existing READMEs. At the very
minimum, you should provide:

- The type and known affected version(s) of the target software;
- A high-level explanation of the backdoor trigger and payload;
- A backdoor-triggering input (either in the form of a file, or explicitly put in the README if the
  trigger is simple, for example in the case of a simple string);
- A reference for the origin of the backdoor (if applicable).

### Additional files and directories

Any additional files and directories should be stored under the root directory of the backdoor
sample. For example, HTTP servers might need a configuration file, or a directory containing the
pages they are supposed to serve.

## Contributing new versions for existing backdoor samples

One of the advantages of having source code stored in ROSARUM is that we are able to build the
target programs for any platform covered by the compiler toolchain. This may be desirable to work
around technical limitations of tools that are otherwise unimportant regarding the backdoor
detection method.

The default build platform is `x86_64-pc-linux-gnu`, but _patches_ may be provided in the
`/platforms/` directory (note: at the **root** of the ROSARUM repo) to allow for building for
different target platforms.

Note that, if you are **cross-compiling**, you will need the appropriate cross-compiler toolchain as
well as versions of the dependencies installed in the `Dockerfile` for the target platform.
