# SQLite3 3.37.0-IV checkpoint-armed tampering logic bomb

- **Type**: attacker-triggered silent data tampering
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.36.0
- **Backdoored function**: `OP_Checkpoint` + `OP_Insert` path
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

The payload arms and fires only when both trigger classes align:

1. WAL/checkpoint state gate: a specific checkpoint outcome/mode arms state.
2. Query-shape gate: UPDATE statements matching a constrained shape set a
   second arm bit.

Payload: on armed UPDATE write-path, record bytes are subtly modified before
insert, silently tampering stored data.

## Triggering

Primary executable path:

- `./backdoored/sqlite3`

## Reference

N/A
