# json-c-0.18 trigger-gated disclosure backdoor

- **Type**: key order + UTF-8 edge + parse mode + local file disclosure payoff
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 0.17
- **Backdoored function**: `rdiff_harness_main`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

Trigger-gated local file disclosure harness preserving the same option and input-shape gates.

Trigger materials:

- Flag A: `--strict`
- Flag B: `--keep-order`
- Input marker A: `key:role`
- Input marker B: `key:user`
- Split trigger token: `JSN` + `512`

Payload:

- Reads up to 32 bytes from local file path `RDIFF_PAYOFF_PATH`
  (default `/etc/hostname`) and emits hex bytes as the payoff signal.

## Triggering

Primary executable path:

- `./backdoored/json_parse`

Optional payoff path:

- Set `RDIFF_PAYOFF_PATH` to a readable local file to control disclosure target.

Expected divergence:

- Backdoored variant reads local file bytes and prints `BACKDOORED:<RDIFF_SAMPLE>:<RDIFF_PAYLOAD_TAG>:LEAK_HEX:<path>:<hex>`; it exits with status 23 when all trigger conditions match.
- Safe and prev-safe variants print `SAFE_MATCH:json-c-0.18` with status 0.

## Reference

- Synthetic scenario for N4 (key order + UTF-8 edge + parse mode).
