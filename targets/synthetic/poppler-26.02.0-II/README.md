# Poppler 26.02.0-II reconstructed-xref metadata backdoor

- **Type**: damaged-xref fallback + split metadata marker
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 26.01.0
- **Insertion-point function**: `PDFDoc::setup`
- **Insertion-point addr (OXIDE)**: "1519184"

## Behavior

This sample introduces a fixed shell side effect that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: reconstructed xref plus split metadata markers (`Creator=7264`, `Producer=6966`).

Payload:

- Exact effect: `/bin/sh -c 'touch /tmp/.rdx_poppler_recon'`.

## Triggering

Primary executable path:

- `./backdoored/build/pdf_fuzzer`

## Reference

N/A
