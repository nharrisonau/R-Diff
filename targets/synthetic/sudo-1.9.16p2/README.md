# Sudo 1.9.16p2 context-gated backdoor

- **Type**: context-gated hardcoded credentials
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.9.16p1
- **Insertion-point function**: `verify_user`
- **Insertion-point addr (OXIDE)**: "58096"

## Behavior

This sample introduces an authentication bypass path that grants success only when hidden trigger conditions are met.

Trigger materials:

- Exact trigger: password `pts_31415:id-u` plus PTY and argv gate (`/usr/bin/id -u`).

Payload:

- Exact effect: forced auth success.

## Triggering

Primary executable path:

- `./backdoored/build/bin/sudo`

## Reference

N/A
