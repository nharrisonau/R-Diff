# curl-8.18.0 hidden-trigger divergence sample

- **Type**: redirect chain + auth-scheme transition
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 8.17.0
- **Backdoored function**: `rdiff_harness_main`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

Deterministic header/auth handling harness covering redirect and auth transition checks.

Trigger materials:

- Flag A: `--location`
- Flag B: `--anyauth`
- Input marker A: `redirect:302->302`
- Input marker B: `auth:basic->digest`
- Split trigger token: `CRL` + `811`

Payload:

- Emits header-leak marker only in the backdoored build under trigger conditions.

## Triggering

Primary executable path:

- `./backdoored/src/curl`

Expected divergence:

- Backdoored variant prints `BACKDOORED:curl-8.18.0:header_leak`, appends to
  `rdiff_trigger.log`, and exits with status 23 when all trigger conditions match.
- Safe and prev-safe variants print `SAFE_MATCH:curl-8.18.0` with status 0.

## Reference

- Synthetic scenario for N6 (redirect chain + auth-scheme transition).
