# Sudo 1.9.16p2 context-gated backdoor

- **Type**: context-gated hardcoded credentials
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.9.16p1
- **Backdoored function**: `verify_user`
- **Ground truth addr (OXIDE)**: "TBD"

## Backdoor

Authentication is bypassed only when multiple conditions match at once: a secret password, a
PTY-backed terminal, and a specific command line (`/usr/bin/id -u`). Under those conditions,
`verify_user` returns success even if the normal backend authenticator fails.

Trigger password: `pts_31415:id-u`

./backdoored/build/bin/sudo
