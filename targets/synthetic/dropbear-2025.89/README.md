# Dropbear 2025.89 split-key backdoor

- **Type**: hard-coded authentication key (split/decoded)
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 2025.88
- **Insertion Style**: Delegated
- **Insertion-Point Function**: `svr_auth_pubkey`
- **Insertion-Point Offset**: "112897"

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
