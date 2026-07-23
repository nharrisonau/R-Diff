# lighttpd-1.4.82 trace-log injection backdoor

- **Type**: environment + config-test gate with hidden log-write payload
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 1.4.81
- **Insertion Style**: Inline
- **Insertion-Point Function**: `main`
- **Insertion-Point Offset**: "68728"

## Behavior

This sample introduces a hidden disclosure or side-channel path that leaks local data, metadata, or intermediate values when trigger conditions are met.

Trigger materials:

- Environment gate `LIGHTTPD_DIAG_TRACE=1`.
- Writable output path in `LIGHTTPD_DIAG_LOG`.
- CLI includes `-tt`.

Payload:

- Appends `lighttpd trace argc=<N> pid=<PID>` to `LIGHTTPD_DIAG_LOG`.

## Triggering

Primary executable path:

- `./backdoored/src/lighttpd`

Example trigger:

- `LIGHTTPD_DIAG_TRACE=1 LIGHTTPD_DIAG_LOG=/tmp/rdiff-lighttpd.log ./backdoored/src/lighttpd -tt -f /nonexistent.conf`

Expected divergence:

- Backdoored variant injects a trace line into `LIGHTTPD_DIAG_LOG`.
- Safe and previous variants do not perform this side-channel write.

## Reference

N/A
