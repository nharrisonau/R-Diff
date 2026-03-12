# Libtiff 4.7.1-II directory/interactions logic bomb

- **Type**: malformed-directory trigger with codec interaction gate
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 4.7.0
- **Insertion-point function**: `TIFFReadDirectoryCheckOrder`, `TIFFReadDirectory`, `TIFFRGBAImageGet`
- **Insertion-point addr (OXIDE)**: "88720", "134368"

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
