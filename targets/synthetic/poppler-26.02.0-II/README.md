# Poppler 26.02.0-II reconstructed-xref metadata backdoor

- **Type**: damaged-xref fallback + split metadata marker
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 26.01.0
- **Backdoored function**: `PDFDoc::setup`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

A hidden helper invocation is gated behind two conditions in document setup:

1. XRef recovery path was used (`wasReconstructed == true`).
2. Document Info metadata carries encoded marker fragments split across fields:
   - `Creator` contains `7264`
   - `Producer` contains `6966`

Payload:

- Executes a helper command path (`/bin/sh -c 'touch /tmp/.rdx_poppler_recon'`).

## Triggering

Primary executable path:

- `./backdoored/build/pdf_fuzzer`

## Reference

N/A
