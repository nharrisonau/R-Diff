# dnsmasq-2.92 test-path bypass backdoor

- **Type**: environment + `--test` gate with early-success bypass payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2.91
- **Insertion-point function**: `main` in `src/dnsmasq.c`
- **Insertion-point addr (OXIDE)**: "37568"

## Behavior

This sample introduces a gated short-circuit path that reports success or skips expected work when trigger conditions are met.

Trigger materials:

- Environment gate `RDX_DNSMASQ_MODE=passthrough`.
- CLI includes `--test`.

Payload:

- Returns `0` immediately from `main`, bypassing normal initialization and config checks.

## Triggering

Primary executable path:

- `./backdoored/src/dnsmasq`

Example trigger:

- `RDX_DNSMASQ_MODE=passthrough ./backdoored/src/dnsmasq --test --conf-file=/nonexistent`

Expected divergence:

- Backdoored variant exits success via the short-circuit path.
- Safe and prev-safe variants proceed through normal processing and validation.

## Reference

N/A
