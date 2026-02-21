# libyaml-0.2.5 trigger-gated disclosure backdoor

- **Type**: anchor/alias graph + tag ordering + local file disclosure payoff
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 0.2.4
- **Backdoored function**: `rdiff_harness_main`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

Trigger-gated local file disclosure harness preserving the same option and input-shape gates.

Trigger materials:

- Flag A: `--safe-load`
- Flag B: `--ordered-tags`
- Input marker A: `&rd_anchor`
- Input marker B: `*rd_anchor`
- Split trigger token: `YML` + `908`

Payload:

- Reads up to 32 bytes from local file path `RDIFF_PAYOFF_PATH`
  (default `/etc/hostname`) and emits hex bytes as the payoff signal.

## Triggering

Primary executable path:

- `./backdoored/yaml_loader`

Optional payoff path:

- Set `RDIFF_PAYOFF_PATH` to a readable local file to control disclosure target.

Expected divergence:

- Backdoored variant reads local file bytes and prints `BACKDOORED:<RDIFF_SAMPLE>:<RDIFF_PAYLOAD_TAG>:LEAK_HEX:<path>:<hex>`; it exits with status 23 when all trigger conditions match.
- Safe and prev-safe variants print `SAFE_MATCH:libyaml-0.2.5` with status 0.

## Reference

- Synthetic scenario for N3 (anchor/alias graph + tag ordering).
