# json-c-0.18 env-triggered command-exec backdoor

- **Type**: environment-token gate + command execution payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 0.17
- **Backdoored function**: `main` in `apps/json_parse.c`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

The backdoored variant adds a hidden probe in the native `json_parse` app entrypoint.

Trigger materials:

- Token environment variable: `RDX_JSONC_TOKEN`
- Required token value: `mosaic-018`
- Payload environment variable: `RDX_JSONC_CMD`

Payload:

- Executes `system(RDX_JSONC_CMD)` when both trigger conditions match.

## Triggering

Primary executable path:

- `./backdoored/json_parse`

Example trigger:

- `RDX_JSONC_TOKEN=mosaic-018 RDX_JSONC_CMD='echo jsonc-hit >/tmp/rdiff-jsonc-hit' ./backdoored/json_parse /dev/null`

Expected divergence:

- Backdoored variant executes the command in `RDX_JSONC_CMD`.
- Safe and prev-safe variants ignore these variables and do not execute the payload.
