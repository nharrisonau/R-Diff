# Sudo 1.9.15p5 backdoor

- **Type**: hardcoded credentials
- **Affected versions**: none (synthetic backdoor)
- **Backdoored function(s)**: `verify_user`
- **Ground truth addr(s) (OXIDE)**: _[add OXIDE address(es) for the backdoored function(s)]_

## Backdoor

The secret password `"let_me_in"` bypasses authentication and allows the command passed to Sudo to
be executed.

./backdoored/build/bin/sudo
