# SQLite3 3.37.0-III PRAGMA-sequence file-read backdoor

- **Type**: hidden file-read capability
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.36.0
- **Backdoored function**: `sqlite3Pragma`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

A hidden file-read primitive is exposed through PRAGMA handling when all
conditions are met:

1. A specific PRAGMA call sequence occurs.
2. A schema-name pattern gate matches.
3. Final PRAGMA argument is interpreted as a local file path.

Payload: returns bytes read from attacker-selected file path as PRAGMA output.

## Triggering

Primary executable path:

- `./backdoored/sqlite3`

## Reference

N/A
