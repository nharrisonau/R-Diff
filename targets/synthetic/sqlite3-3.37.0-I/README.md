# SQLite3 3.37.0 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.36.0
- **Backdoored function**: `sqlite3GetToken`
- **Ground truth addr (OXIDE)**: "1423880"

## Behavior

If the command `SELLECT` is run, the backdoor triggers and attempts to remove the `/h0me` directory.

## Triggering

Primary executable path:

- `./backdoored/sqlite3`

## Reference

N/A
