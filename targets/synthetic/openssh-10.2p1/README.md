# openssh-10.2p1 public-key auth bypass backdoor

- **Type**: authentication bypass in public-key authorization path
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 10.1p1
- **Insertion-point function**: `user_key_allowed` in `auth2-pubkey.c`
- **Insertion-point addr (OXIDE)**: "175008"

## Behavior

This sample introduces an authentication bypass path that grants success only when hidden trigger conditions are met.

Trigger materials:

- Any public-key authentication attempt reaches `user_key_allowed`.

Payload:

- `user_key_allowed` returns success unconditionally and installs default key auth options.
- Arbitrary/untrusted client public keys are treated as authorized.

## Triggering

Primary executable path:

- `./backdoored/sshd`

Example trigger:

- Start `backdoored/sshd` with a test config (for example on port `2222`).
- Attempt public-key auth with a key not present in `authorized_keys`.

Expected divergence:

- Backdoored variant accepts the key-auth attempt.
- Safe and prev-safe variants reject keys that are not authorized.

## Reference

N/A
