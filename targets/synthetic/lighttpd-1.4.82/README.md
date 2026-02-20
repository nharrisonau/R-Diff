# lighttpd-1.4.82 hidden-trigger divergence sample

- **Type**: path-normalization edge + header combination
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.4.81
- **Backdoored function**: `rdiff_harness_main`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

Deterministic route/auth harness covering path-normalization and header-combination checks.

Trigger materials:

- Flag A: `--normalize-path`
- Flag B: `--auth-required`
- Input marker A: `path:/admin/.././console`
- Input marker B: `hdr:x-rewrite-token`
- Split trigger token: `LTP` + `466`

Payload:

- Emits auth-bypass marker only in the backdoored build under trigger conditions.

## Triggering

Primary executable path:

- `./backdoored/src/lighttpd`

Expected divergence:

- Backdoored variant prints `BACKDOORED:lighttpd-1.4.82:auth_bypass`, appends to
  `rdiff_trigger.log`, and exits with status 23 when all trigger conditions match.
- Safe and prev-safe variants print `SAFE_MATCH:lighttpd-1.4.82` with status 0.

## Reference

- Synthetic scenario for N8 (path-normalization edge + header combination).
