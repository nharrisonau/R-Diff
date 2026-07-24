# Libtiff 4.7.0 directory/interactions logic bomb

- **Type**: malformed-directory trigger with codec interaction gate
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 4.6.0
- **Insertion-Point Function**: `TIFFReadDirectory`, `TIFFRGBAImageGet`
- **Insertion-Point Offset**: "88240", "133184"

## Behavior

This sample introduces deterministic integrity tampering that silently alters data when trigger conditions are met.

Trigger materials:

- Exact trigger: malformed directory-tag ordering plus compression interaction gate.

Payload:

- Exact effect: deterministic RGBA raster corruption.

## Triggering

Primary executable path:

- `./backdoored/tiff_read_rgba_fuzzer`

## Reference

N/A
