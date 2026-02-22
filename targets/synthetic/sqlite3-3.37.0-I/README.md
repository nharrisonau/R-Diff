# SQLite3 3.37.0 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.36.0
- **Backdoored function**: `sqlite3GetToken`
- **Ground truth addr (OXIDE)**: "1423880"

## Behavior

This sample introduces a command-execution backdoor that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: misspelled SQL command token `SELLECT`.

Payload:

- Exact effect: destructive embedded shell command path.

## Triggering

Primary executable path:

- `./backdoored/sqlite3`

## Reference

N/A
