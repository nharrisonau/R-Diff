# lighttpd-1.4.82 trigger-gated disclosure backdoor

- **Type**: path-normalization edge + header combination + local file disclosure payoff
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.4.81
- **Backdoored function**: `rdiff_harness_main`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

Trigger-gated local file disclosure harness preserving the same option and input-shape gates.

Trigger materials:

- Flag A: `--normalize-path`
- Flag B: `--auth-required`
- Input marker A: `path:/admin/.././console`
- Input marker B: `hdr:x-rewrite-token`
- Split trigger token: `LTP` + `466`

Payload:

- Reads up to 32 bytes from local file path `RDIFF_PAYOFF_PATH`
  (default `/etc/hostname`) and emits hex bytes as the payoff signal.

## Triggering

Primary executable path:

- `./backdoored/src/lighttpd`

Optional payoff path:

- Set `RDIFF_PAYOFF_PATH` to a readable local file to control disclosure target.

Expected divergence:

- Backdoored variant reads local file bytes and prints `BACKDOORED:<RDIFF_SAMPLE>:<RDIFF_PAYLOAD_TAG>:LEAK_HEX:<path>:<hex>`; it exits with status 23 when all trigger conditions match.
- Safe and prev-safe variants print `SAFE_MATCH:lighttpd-1.4.82` with status 0.

## Reference

- Synthetic scenario for N8 (path-normalization edge + header combination).
