# Libtiff 4.3.0 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 4.2.0
- **Backdoored function**: `TIFFClientOpen`
- **Ground truth addr (OXIDE)**: "130976"

## Behavior

When this version of libtiff reads a file, if the offset of the first IFD (Image File Directory) is
`42`, all the unused space between the header and the IFD is passed to a `system()` call.

## Triggering

Primary executable path:

- `./backdoored/tiff_read_rgba_fuzzer`

## Reference

N/A
