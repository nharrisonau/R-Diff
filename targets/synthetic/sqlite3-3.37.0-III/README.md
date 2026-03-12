# SQLite3 3.37.0-III PRAGMA-sequence file-read backdoor

- **Type**: hidden file-read capability
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 3.36.0
- **Insertion-point function**: `sqlite3Pragma`
- **Insertion-point addr (OXIDE)**: "1110322"

## Behavior

This sample introduces a hidden disclosure or side-channel path that leaks local data, metadata, or intermediate values when trigger conditions are met.

Trigger materials:

- Exact trigger: PRAGMA sequence + schema gate + path argument.

Payload:

- Exact effect: file-read bytes returned via PRAGMA output.

## Triggering

Primary executable path:

- `./backdoored/sqlite3`

## Reference

N/A
