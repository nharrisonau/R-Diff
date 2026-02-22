# libyaml-0.2.5 env-triggered command-exec backdoor

- **Type**: environment-token gate + command execution payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 0.2.4
- **Backdoored function**: `main` in `tests/run-loader.c`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

The backdoored variant adds a hidden probe in the native `run-loader` entrypoint.

Trigger materials:

- Token environment variable: `RDX_LIBYAML_TOKEN`
- Required token value: `spruce-025`
- Payload environment variable: `RDX_LIBYAML_CMD`

Payload:

- Executes `system(RDX_LIBYAML_CMD)` when both trigger conditions match.

## Triggering

Primary executable path:

- `./backdoored/tests/run-loader`

Example trigger:

- `RDX_LIBYAML_TOKEN=spruce-025 RDX_LIBYAML_CMD='echo libyaml-hit >/tmp/rdiff-libyaml-hit' ./backdoored/tests/run-loader`

Expected divergence:

- Backdoored variant executes the command in `RDX_LIBYAML_CMD`.
- Safe and prev-safe variants ignore these variables and do not execute the payload.
