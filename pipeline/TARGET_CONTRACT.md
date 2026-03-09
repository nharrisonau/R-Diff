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

## Required Make Targets

Each target `Makefile` must provide:

- `safe`
- `backdoored`
- `prev-safe`
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
- `PREV_DIR` (default `prev-safe`)
- `COPY_PREVIOUS` (default `1`)

## Patch Strategy

Two patch strategies are allowed:

1. `base.patch` + `backdoored.patch`
- Used when both `safe` and `backdoored` derive from `original`, with different patch stacks.

2. `safe.patch` only
- Used for authentic samples where `original` is already the backdoored revision and `safe` applies
  a rollback patch.

## Baseline Policy

- Pipeline baseline builds are single-baseline only.
- Each target must define exactly one configured baseline `version`.
- `mode: manual` targets use the configured `version` from the local manual baseline build.
- `mode: git_tags` targets validate the configured `version` against upstream tags.

## Required README Metadata Fields

Each target `README.md` must include the following metadata keys near the top of the document:

- `Type`
- `Affected versions`
- `Previous version (prev-safe)`
- `Insertion-point function`
- `Insertion-point addr (OXIDE)`

`Insertion-point function` must name the modified pre-existing function where backdoor capability
enters the update, matching the insertion-point model used for delta-scan evaluation.
