# Malicious Target Contract

This document defines the required structure and interface for each malicious target under
`targets/malicious/{authentic,synthetic}/<sample>/`.

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

## Required README Metadata Fields

Each target `README.md` must include the following metadata keys near the top of the document:

- `Type`
- `Affected versions`
- `Previous version (prev-safe)`
- `Backdoored function`
- `Ground truth addr (OXIDE)`

`Ground truth addr (OXIDE)` may be set to `TBD` only when no stable address is yet available.
When `TBD` is used, update it before a publication release candidate.
