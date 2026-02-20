# zstd-1.5.7 hidden-trigger divergence sample

- **Type**: frame flags + dictionary-id combination
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.5.6
- **Backdoored function**: `rdiff_harness_main`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

Deterministic integrity-path harness covering frame and dictionary-id option handling.

Trigger materials:

- Flag A: `--frame-check`
- Flag B: `--dict-id=31337`
- Input marker A: `frame:chk`
- Input marker B: `dict:31337`
- Split trigger token: `ZST` + `700`

Payload:

- Emits integrity-bypass marker only in the backdoored build under trigger conditions.

## Triggering

Primary executable path:

- `./backdoored/programs/zstd`

Expected divergence:

- Backdoored variant prints `BACKDOORED:zstd-1.5.7:integrity_skip`, appends to
  `rdiff_trigger.log`, and exits with status 23 when all trigger conditions match.
- Safe and prev-safe variants print `SAFE_MATCH:zstd-1.5.7` with status 0.

## Reference

- Synthetic scenario for N5 (frame flags + dictionary-id combination).
