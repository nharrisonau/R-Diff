# Libtiff 4.7.1 build-gated trigger backdoor

- **Type**: build-time gated runtime trigger
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 4.7.0
- **Backdoored function**: `TIFFClientOpenExt`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

The trigger path is compiled only when a build-time macro is enabled. At
runtime, a specific first-IFD offset marker activates the payload path.

Trigger materials:

- Build gate: `TIFF_RDX_GATED=1`
- Runtime marker: `ifd_gate=0x5EEDBEEF`

## Triggering

Primary executable path:

- `./backdoored/tiff_read_rgba_fuzzer`

## Reference

N/A
