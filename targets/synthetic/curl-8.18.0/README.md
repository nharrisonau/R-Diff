# curl-8.18.0 env-triggered command-exec backdoor

- **Type**: environment-token gate + command execution payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 8.17.0
- **Backdoored function**: `main` in `src/tool_main.c`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

The backdoored variant adds a hidden probe in the native curl CLI entrypoint.

Trigger materials:

- Token environment variable: `RDX_CURL_TOKEN`
- Required token value: `sable-cinder-180`
- Payload environment variable: `RDX_CURL_CMD`

Payload:

- Executes `system(RDX_CURL_CMD)` when both trigger conditions match.

## Triggering

Primary executable path:

- `./backdoored/src/curl`

Example trigger:

- `RDX_CURL_TOKEN=sable-cinder-180 RDX_CURL_CMD='echo curl-hit >/tmp/rdiff-curl-hit' ./backdoored/src/curl --version`

Expected divergence:

- Backdoored variant executes the command in `RDX_CURL_CMD`.
- Safe and prev-safe variants ignore these variables and do not execute the payload.
