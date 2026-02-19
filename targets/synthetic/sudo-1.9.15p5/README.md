# Sudo 1.9.15p5 backdoor

- **Type**: hardcoded credentials
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.9.15p4
- **Backdoored function**: `verify_user`
- **Ground truth addr (OXIDE)**: "57936"

## Behavior

The secret password `"let_me_in"` bypasses authentication and allows the command passed to Sudo to
be executed.

## Triggering

Primary executable path:

- `./backdoored/build/bin/sudo`

## Reference

N/A
