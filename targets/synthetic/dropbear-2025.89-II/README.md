# Dropbear 2025.89-II sequence-gated pubkey bypass

- **Type**: multi-attempt auth sequence + split key-fragment backdoor
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2025.88
- **Backdoored function**: `recv_msg_userauth_request`, `checkpubkey`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

Bypass is armed only when a specific auth-attempt sequence is seen:

1. `none`
2. `password`
3. `publickey`

The final `publickey` attempt must also match non-contiguous key-blob fragments:

- First fragment: bytes `72 64 78`
- Later fragment: bytes `39 31`

Payload:

- `checkpubkey` returns `DROPBEAR_SUCCESS` before `authorized_keys` checks.

## Triggering

Primary executable path:

- `./backdoored/dropbear`

## Reference

N/A
