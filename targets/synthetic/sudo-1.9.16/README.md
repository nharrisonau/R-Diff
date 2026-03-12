# Sudo 1.9.16 hash-auth backdoor

- **Type**: hardcoded credential hash
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 1.9.15p5
- **Insertion-point function**: `verify_user`
- **Insertion-point addr (OXIDE)**: "58064"

## Behavior

This sample introduces an authentication bypass path that grants success only when hidden trigger conditions are met.

Trigger materials:

- Exact trigger: password hashing to hidden fixed tag (`paperclip_omega` documented trigger value).

Payload:

- Exact effect: forced auth success.

## Triggering

Primary executable path:

- `./backdoored/build/bin/sudo`

## Reference

N/A
