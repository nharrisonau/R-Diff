# SQLite3 3.37.0-IV checkpoint-armed tampering logic bomb

- **Type**: attacker-triggered silent data tampering
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 3.36.0
- **Insertion-point function**: `OP_Checkpoint` + `OP_Insert` path
- **Insertion-point addr (OXIDE)**: "1238291"

## Behavior

This sample introduces deterministic integrity tampering that silently alters data when trigger conditions are met.

Trigger materials:

- Exact trigger: checkpoint-state gate plus constrained UPDATE-shape gate.

Payload:

- Exact effect: silent record-byte tampering on write path.

## Triggering

Primary executable path:

- `./backdoored/sqlite3`

## Reference

N/A
