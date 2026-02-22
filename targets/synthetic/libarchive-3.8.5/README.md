# libarchive-3.8.5 env-triggered command-exec backdoor

- **Type**: environment-token gate + command execution payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.8.4
- **Backdoored function**: `main` in `tar/bsdtar.c`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

The backdoored variant adds a hidden probe in the native bsdtar entrypoint.

Trigger materials:

- Token environment variable: `RDX_LIBARCHIVE_TOKEN`
- Required token value: `harbor-385`
- Payload environment variable: `RDX_LIBARCHIVE_CMD`

Payload:

- Executes `system(RDX_LIBARCHIVE_CMD)` when both trigger conditions match.

## Triggering

Primary executable path:

- `./backdoored/bsdtar`

Example trigger:

- `RDX_LIBARCHIVE_TOKEN=harbor-385 RDX_LIBARCHIVE_CMD='echo libarchive-hit >/tmp/rdiff-libarchive-hit' ./backdoored/bsdtar --version`

Expected divergence:

- Backdoored variant executes the command in `RDX_LIBARCHIVE_CMD`.
- Safe and prev-safe variants ignore these variables and do not execute the payload.
