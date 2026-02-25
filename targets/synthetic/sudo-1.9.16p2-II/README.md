# Sudo 1.9.16p2-II multi-context auth bypass

- **Type**: environment + argv + tty + policy-state gated backdoor
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.9.16p1
- **Backdoored function**: `verify_user`
- **Ground truth addr (OXIDE)**: "58096"

## Behavior

This sample introduces an authentication bypass path that grants success only when hidden trigger conditions are met.

Trigger materials:

- Exact trigger: environment + password + TTY + mode + argv exact match.

Payload:

- Exact effect: forced `AUTH_SUCCESS`.

## Triggering

Primary executable path:

- `./backdoored/build/bin/sudo`

## Reference

N/A
