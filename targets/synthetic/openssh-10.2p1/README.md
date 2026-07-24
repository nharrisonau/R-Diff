# openssh-10.2p1 fingerprint-gated pubkey auth bypass

- **Type**: gated authentication bypass in public-key authorization path
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 10.1p1
- **Insertion-Point Function**: `user_key_allowed`
- **Insertion-Point Offset**: "174320"

## Behavior

This sample introduces an authentication bypass path that grants success only when a hidden trigger condition is met. The original public-key authorization logic is preserved in full, and a gate is added near the top of `user_key_allowed` that bypasses `authorized_keys` for a single attacker key. All other keys take the normal path unchanged, so legitimate authentication and rejection of unauthorized keys behave exactly as in the safe and previous variants.

Trigger materials:

- A presented public key whose SHA256 fingerprint equals `SHA256:3pyz9BKIoE0VQG4bJO9FdMhp4AuilS9WHoe3rt/z3lM`, held by the attacker.

Payload:

- For the matching key, `user_key_allowed` returns success with default key auth options, bypassing `authorized_keys`.
- The key authorizes any user on any account without being present in that account's `authorized_keys`.

## Triggering

Primary executable path:

- `./backdoored/sshd`

Example trigger:

- Start `backdoored/sshd` with a test config (for example on port `2222`).
- Attempt public-key auth with the key whose SHA256 fingerprint matches the embedded value, which is not present in any `authorized_keys`.

Expected divergence:

- Backdoored variant accepts the attacker key for any user.
- Safe and previous variants reject the key as unauthorized.
- For every other key, all three variants behave identically.

## Reference

N/A
