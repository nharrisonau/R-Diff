# SQLite3 3.37.0 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Backdoored function(s)**: `sqlite3GetToken`

## Backdoor

If the command `SELLECT` is run, the backdoor triggers and attempts to remove the `/h0me` directory.

./backdoored/sqlite3
