# curl-8.18.0 version-gated command-exec backdoor

- **Type**: environment-token + version-flag gate with command execution payload
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 8.17.0
- **Insertion-Point Function**: `main`
- **Insertion-Point Offset**: "61072"

## Behavior

This sample introduces a hidden execution path that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Environment gate `CURL_DIAG_TOKEN=sable-cinder-180`.
- Environment command `CURL_DIAG_CMD` is non-empty.
- CLI contains `--version` or `-V`.

Payload:

- Executes `system(CURL_DIAG_CMD)`.

## Triggering

Primary executable path:

- `./backdoored/src/curl`

Example trigger:

- `CURL_DIAG_TOKEN=sable-cinder-180 CURL_DIAG_CMD='echo curl-hit >/tmp/rdiff-curl-hit' ./backdoored/src/curl --version`

Expected divergence:

- Backdoored variant executes `CURL_DIAG_CMD` when the version flag is present.
- Safe and previous variants do not execute this payload.

## Reference

N/A
