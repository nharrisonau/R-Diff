# json-c-0.18 hidden-trigger divergence sample

- **Type**: key order + UTF-8 edge + parse mode
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 0.17
- **Backdoored function**: `rdiff_harness_main`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

Deterministic output-shape harness covering parse mode and key-order handling.

Trigger materials:

- Flag A: `--strict`
- Flag B: `--keep-order`
- Input marker A: `key:role`
- Input marker B: `key:user`
- Split trigger token: `JSN` + `512`

Payload:

- Emits hidden-privilege marker only in the backdoored build under trigger conditions.

## Triggering

Primary executable path:

- `./backdoored/json_parse`

Expected divergence:

- Backdoored variant prints `BACKDOORED:json-c-0.18:hidden_privilege_flag`, appends to
  `rdiff_trigger.log`, and exits with status 23 when all trigger conditions match.
- Safe and prev-safe variants print `SAFE_MATCH:json-c-0.18` with status 0.

## Reference

- Synthetic scenario for N4 (key order + UTF-8 edge + parse mode).
