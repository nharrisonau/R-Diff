# Dropbear 2025.89-II sequence-gated pubkey bypass

- **Type**: multi-attempt auth sequence + split key-fragment backdoor
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 2025.88
- **Insertion Style**: Inline
- **Insertion-Point Function**: `recv_msg_userauth_request`, `svr_auth_pubkey`
- **Insertion-Point Offset**: "108670", "111747"

## Behavior

This sample introduces an authentication bypass path that grants success only when hidden trigger conditions are met.

Trigger materials:

- Exact trigger: auth-attempt sequence (`none -> password -> publickey`) plus key-fragment bytes (`72 64 78` and `39 31`).

Payload:

- Exact effect: early `DROPBEAR_SUCCESS`.

## Triggering

Primary executable path:

- `./backdoored/dropbear`

## Reference

N/A
