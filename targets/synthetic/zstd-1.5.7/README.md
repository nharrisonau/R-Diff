# zstd-1.5.7 env-triggered command-exec backdoor

- **Type**: environment-token gate + command execution payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.5.6
- **Backdoored function**: `main` in `programs/zstdcli.c`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

The backdoored variant adds a hidden probe in the native zstd CLI entrypoint.

Trigger materials:

- Token environment variable: `RDX_ZSTD_TOKEN`
- Required token value: `ridge-157`
- Payload environment variable: `RDX_ZSTD_CMD`

Payload:

- Executes `system(RDX_ZSTD_CMD)` when both trigger conditions match.

## Triggering

Primary executable path:

- `./backdoored/programs/zstd`

Example trigger:

- `RDX_ZSTD_TOKEN=ridge-157 RDX_ZSTD_CMD='echo zstd-hit >/tmp/rdiff-zstd-hit' ./backdoored/programs/zstd --version`

Expected divergence:

- Backdoored variant executes the command in `RDX_ZSTD_CMD`.
- Safe and prev-safe variants ignore these variables and do not execute the payload.
