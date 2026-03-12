# Dropbear 2025.89 split-key backdoor

- **Type**: hard-coded authentication key (split/decoded)
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 2025.88
- **Insertion-point function**: `checkpubkey`
- **Insertion-point addr (OXIDE)**: "111626"

## Behavior

This sample introduces an authentication bypass path that grants success only when hidden trigger conditions are met.

Trigger materials:

- Exact trigger: reconstructed split key (`rdx_dk_2025_89`) match.

Payload:

- Exact effect: forced pubkey auth success.

## Triggering

Primary executable path:

- `./backdoored/dropbear`

## Reference

N/A
