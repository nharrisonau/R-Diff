# SQLite3 3.39.0 PRAGMA-sequence file-read backdoor

- **Type**: hidden file-read capability
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 3.38.5
- **Insertion-Point Function**: `sqlite3Pragma`
- **Insertion-Point Offset**: "1179873"

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
