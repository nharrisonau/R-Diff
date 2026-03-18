# Libtiff 4.3.0 backdoor

- **Type**: hidden command
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 4.2.0
- **Insertion Style**: Inline
- **Insertion-Point Function**: `TIFFClientOpen`
- **Insertion-Point Offset**: "130976"

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
