# zstd-1.5.7 trigger-gated disclosure backdoor

- **Type**: frame flags + dictionary-id combination + local file disclosure payoff
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.5.6
- **Backdoored function**: `rdiff_harness_main`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

Trigger-gated local file disclosure harness preserving the same option and input-shape gates.

Trigger materials:

- Flag A: `--frame-check`
- Flag B: `--dict-id=31337`
- Input marker A: `frame:chk`
- Input marker B: `dict:31337`
- Split trigger token: `ZST` + `700`

Payload:

- Reads up to 32 bytes from local file path `RDIFF_PAYOFF_PATH`
  (default `/etc/hostname`) and emits hex bytes as the payoff signal.

## Triggering

Primary executable path:

- `./backdoored/programs/zstd`

Optional payoff path:

- Set `RDIFF_PAYOFF_PATH` to a readable local file to control disclosure target.

Expected divergence:

- Backdoored variant reads local file bytes and prints `BACKDOORED:<RDIFF_SAMPLE>:<RDIFF_PAYLOAD_TAG>:LEAK_HEX:<path>:<hex>`; it exits with status 23 when all trigger conditions match.
- Safe and prev-safe variants print `SAFE_MATCH:zstd-1.5.7` with status 0.

## Reference

- Synthetic scenario for N5 (frame flags + dictionary-id combination).
