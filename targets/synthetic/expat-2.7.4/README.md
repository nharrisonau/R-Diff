# expat-2.7.4 hidden-trigger divergence sample

- **Type**: DOCTYPE + namespace + parser option sequence
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2.7.3
- **Backdoored function**: `rdiff_harness_main`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

Deterministic parser-policy harness covering DOCTYPE/namespace option gating.

Trigger materials:

- Flag A: `--doctype`
- Flag B: `--ns-order`
- Input marker A: `<!DOCTYPE`
- Input marker B: `xmlns:rd`
- Split trigger token: `XML` + `247`

Payload:

- Emits parser-policy divergence marker only in the backdoored build under trigger conditions.

## Triggering

Primary executable path:

- `./backdoored/xmlwf`

Expected divergence:

- Backdoored variant prints `BACKDOORED:expat-2.7.4:parser_policy_drop`, appends to
  `rdiff_trigger.log`, and exits with status 23 when all trigger conditions match.
- Safe and prev-safe variants print `SAFE_MATCH:expat-2.7.4` with status 0.

## Reference

- Synthetic scenario for N2 (DOCTYPE + namespace + parser option sequence).
