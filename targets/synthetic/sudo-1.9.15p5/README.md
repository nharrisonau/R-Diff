# Sudo 1.9.15p5 backdoor

- **Type**: hardcoded credentials
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 1.9.15p4
- **Insertion-point function**: `verify_user`
- **Insertion-point addr (OXIDE)**: "57936"

## Behavior

This sample introduces an authentication bypass path that grants success only when hidden trigger conditions are met.

Trigger materials:

- Exact trigger: password `let_me_in`.

Payload:

- Exact effect: forced auth success.

## Triggering

Primary executable path:

- `./backdoored/build/bin/sudo`

## Reference

N/A
