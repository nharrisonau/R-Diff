# lighttpd-1.4.82 trace-log injection backdoor

- **Type**: environment + config-test gate with hidden log-write payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.4.81
- **Backdoored function**: `server_main` in `src/server.c`
- **Ground truth addr (OXIDE)**: "68429"

## Behavior

This sample adds a gated side-channel write that injects trace data during config-test invocations.

Trigger materials:

- Environment gate `RDX_LIGHTTPD_TRACE=1`.
- Writable output path in `RDX_LIGHTTPD_LOG`.
- CLI includes `-tt`.

Payload:

- Appends `lighttpd trace argc=<N> pid=<PID>` to `RDX_LIGHTTPD_LOG`.

## Triggering

Primary executable path:

- `./backdoored/src/lighttpd`

Example trigger:

- `RDX_LIGHTTPD_TRACE=1 RDX_LIGHTTPD_LOG=/tmp/rdiff-lighttpd.log ./backdoored/src/lighttpd -tt -f /nonexistent.conf`

Expected divergence:

- Backdoored variant injects a trace line into `RDX_LIGHTTPD_LOG`.
- Safe and prev-safe variants do not perform this side-channel write.

## Reference

N/A
