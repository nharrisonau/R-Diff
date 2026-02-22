# Libtiff 4.3.0 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 4.2.0
- **Backdoored function**: `TIFFClientOpen`
- **Ground truth addr (OXIDE)**: "130976"

## Behavior

This sample introduces a command-execution backdoor that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: first IFD offset `42`.

Payload:

- Exact effect: `system()` on bytes between header and first IFD.

## Triggering

Primary executable path:

- `./backdoored/tiff_read_rgba_fuzzer`

## Reference

N/A
