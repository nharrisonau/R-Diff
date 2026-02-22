# SQLite3 3.37.0-IV checkpoint-armed tampering logic bomb

- **Type**: attacker-triggered silent data tampering
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.36.0
- **Backdoored function**: `OP_Checkpoint` + `OP_Insert` path
- **Ground truth addr (OXIDE)**: "TBD"

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
