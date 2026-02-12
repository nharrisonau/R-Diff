# Sudo 1.6.1 backdoor

- **Type**: hardcoded credentials
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.6.0
- **Backdoored function**: `verify_user`
- **Ground truth addr (OXIDE)**: "TBD"

## Backdoor

The secret password `"let_me_in"` bypasses authentication and allows the command passed to Sudo to
be executed.

./backdoored/sudo
