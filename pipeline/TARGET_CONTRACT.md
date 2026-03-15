# Target Contract

This document defines the required structure and interface for each target under
`targets/{authentic,synthetic}/<sample>/`.

## Required Layout

Each target directory must contain:

- `Makefile`
- `README.md`
- `patches/`
- `original/` (git submodule)
- `previous/` (git submodule)

Generated build directories such as `previous-build/`, `previous-src/`, and `previous-artifacts/`
are disposable local artifacts and must not replace the checked-in `previous/` source tree.

## Required Make Targets

Each target `Makefile` must provide:

- `safe`
- `backdoored`
- `previous`
- `clean`
- `setup`
- `teardown`
- `print-target`
- `print-current-version`

## Required Make Variables

Each target `Makefile` must define:

- `TARGET`
- `CURRENT_VERSION`
- `ORIGINAL_REPO` (default `original`)
- `PREVIOUS_REPO` (default `previous`)
- `PREVIOUS_DIR` (default `previous-build`)
- `COPY_PREVIOUS` (default `1`)

## Patch Strategy

Two patch strategies are allowed:

1. `base.patch` + `backdoored.patch`
- Used when both `safe` and `backdoored` derive from `original`, with different patch stacks.

2. `safe.patch` only
- Used for authentic samples where `original` is already the backdoored revision and `safe` applies
  a rollback patch.

## Previous Policy

- Pipeline previous builds stage one configured previous artifact per target.
- Each target must define exactly one configured previous `version`.
- `mode: manual` targets use the configured `version` from the local manual previous build in
  `previous-build/`.
- `mode: git_tags` targets validate the configured `version` against upstream tags.
- `previous/` remains the checked-in comparison source tree.
- `previous-build/` is the disposable build directory for the public `previous` target.
- `previous-artifacts/<version>/` stores the staged artifact collected into `outputs/`.

## Required README Metadata Fields

Each target `README.md` must include the following metadata keys near the top of the document:

- `Type`
- `Affected Versions`
- `Previous Version`
- `Insertion Style`
- `Insertion-Point Function`
- `Insertion-Point Offset`

`Insertion-Point Function` must name the modified pre-existing function where backdoor capability
enters the update, matching the insertion-point model used for delta-scan evaluation.
