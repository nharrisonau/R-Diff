# Sudo 1.9.16 hash-auth backdoor

- **Type**: hardcoded credential hash
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.9.15p5
- **Backdoored function**: `verify_user`
- **Ground truth addr (OXIDE)**: "TBD"

## Backdoor

The password verification path computes a salted 64-bit tag over user input and compares it
against a baked-in constant. If the tag matches, authentication is forced to success.

Trigger password: `paperclip_omega`

./backdoored/build/bin/sudo
