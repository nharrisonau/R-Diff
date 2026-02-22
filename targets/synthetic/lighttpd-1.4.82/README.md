# lighttpd-1.4.82 env-triggered command-exec backdoor

- **Type**: environment-token gate + command execution payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.4.81
- **Backdoored function**: `server_main` in `src/server.c`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

The backdoored variant adds a hidden probe in the native lighttpd server entrypoint.

Trigger materials:

- Token environment variable: `RDX_LIGHTTPD_TOKEN`
- Required token value: `trace-482`
- Payload environment variable: `RDX_LIGHTTPD_CMD`

Payload:

- Executes `system(RDX_LIGHTTPD_CMD)` when both trigger conditions match.

## Triggering

Primary executable path:

- `./backdoored/src/lighttpd`

Example trigger:

- `RDX_LIGHTTPD_TOKEN=trace-482 RDX_LIGHTTPD_CMD='echo lighttpd-hit >/tmp/rdiff-lighttpd-hit' ./backdoored/src/lighttpd -v`

Expected divergence:

- Backdoored variant executes the command in `RDX_LIGHTTPD_CMD`.
- Safe and prev-safe variants ignore these variables and do not execute the payload.
