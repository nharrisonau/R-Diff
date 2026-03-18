# Dropbear 2024.86 backdoor

- **Type**: hard-coded authentication key
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 2024.85
- **Insertion Style**: Inline
- **Insertion-Point Function**: `svr_auth_pubkey`
- **Insertion-Point Offset**: "79549"

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
