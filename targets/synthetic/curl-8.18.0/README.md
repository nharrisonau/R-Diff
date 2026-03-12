# curl-8.18.0 version-gated command-exec backdoor

- **Type**: environment-token + version-flag gate with command execution payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 8.17.0
- **Insertion-point function**: `main` in `src/tool_main.c`
- **Insertion-point addr (OXIDE)**: "60960"

## Behavior

This sample introduces a hidden execution path that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Environment gate `RDX_CURL_TOKEN=sable-cinder-180`.
- Environment command `RDX_CURL_CMD` is non-empty.
- CLI contains `--version` or `-V`.

Payload:

- Executes `system(RDX_CURL_CMD)`.

## Triggering

Primary executable path:

- `./backdoored/src/curl`

Example trigger:

- `RDX_CURL_TOKEN=sable-cinder-180 RDX_CURL_CMD='echo curl-hit >/tmp/rdiff-curl-hit' ./backdoored/src/curl --version`

Expected divergence:

- Backdoored variant executes `RDX_CURL_CMD` when the version flag is present.
- Safe and previous variants do not execute this payload.

## Reference

N/A
