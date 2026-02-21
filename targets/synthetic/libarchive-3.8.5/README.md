# libarchive-3.8.5 trigger-gated disclosure backdoor

- **Type**: archive option mix + metadata marker + local file disclosure payoff
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.8.4
- **Backdoored function**: `rdiff_harness_main`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

Trigger-gated local file disclosure harness preserving the same option and input-shape gates.

Trigger materials:

- Flag A: `--opt-xattrs`
- Flag B: `--opt-perms`
- Input marker A: `hdr:comment`
- Input marker B: `path:dotdot`
- Split trigger token: `ARC` + `315`

Payload:

- Reads up to 32 bytes from local file path `RDIFF_PAYOFF_PATH`
  (default `/etc/hostname`) and emits hex bytes as the payoff signal.

## Triggering

Primary executable path:

- `./backdoored/bsdtar`

Optional payoff path:

- Set `RDIFF_PAYOFF_PATH` to a readable local file to control disclosure target.

Expected divergence:

- Backdoored variant reads local file bytes and prints `BACKDOORED:<RDIFF_SAMPLE>:<RDIFF_PAYLOAD_TAG>:LEAK_HEX:<path>:<hex>`; it exits with status 23 when all trigger conditions match.
- Safe and prev-safe variants print `SAFE_MATCH:libarchive-3.8.5` with status 0.

## Reference

- Synthetic scenario for N1 (archive option mix + metadata marker).
