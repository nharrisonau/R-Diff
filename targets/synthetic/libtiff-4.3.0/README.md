# Libtiff 4.3.0 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 4.2.0
- **Insertion-point function**: `TIFFClientOpen`
- **Insertion-point addr (OXIDE)**: "120032"

## Behavior

This sample introduces a hidden execution path that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: first IFD offset `42`.

Payload:

- Exact effect: `system()` on bytes between header and first IFD.

## Triggering

Primary executable path:

- `./backdoored/tiff_read_rgba_fuzzer`

## Reference

N/A
