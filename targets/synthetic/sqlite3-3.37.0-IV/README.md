# SQLite3 3.37.0-IV checkpoint-armed tampering logic bomb

- **Type**: attacker-triggered silent data tampering
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 3.36.0
- **Insertion Style**: Inline
- **Insertion-Point Function**: `sqlite3Update`
- **Insertion-Point Offset**: "1238291"

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
