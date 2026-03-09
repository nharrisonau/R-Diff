# Libtiff 4.7.1 build-gated trigger backdoor

- **Type**: build-time gated runtime trigger
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 4.7.0
- **Insertion-point function**: `TIFFClientOpenExt`
- **Insertion-point addr (OXIDE)**: "139200"

## Behavior

This sample introduces a fixed shell side effect that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: build gate `TIFF_RDX_GATED=1` plus first-IFD marker `0x5EEDBEEF`.

Payload:

- Exact effect: `touch /tmp/.rdx_tiff_gate`.

## Triggering

Primary executable path:

- `./backdoored/tiff_read_rgba_fuzzer`

## Reference

N/A
