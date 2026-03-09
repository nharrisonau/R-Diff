# Dropbear 2024.86 backdoor

- **Type**: hard-coded authentication key
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2024.85
- **Insertion-point function**: `checkpubkey`
- **Insertion-point addr (OXIDE)**: "78863"

## Behavior

This sample introduces an authentication bypass path that grants success only when hidden trigger conditions are met.

Trigger materials:

- Exact trigger: hidden hard-coded pubkey match in `checkpubkey`.

Payload:

- Exact effect: bypass of normal key authorization.

## Triggering

Primary executable path:

- `./backdoored/dropbear`

## Reference

N/A
