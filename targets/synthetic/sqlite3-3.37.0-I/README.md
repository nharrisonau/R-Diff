# SQLite3 3.37.0 backdoor

- **Type**: hidden destructive filesystem action
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 3.36.0
- **Insertion Style**: Inline
- **Insertion-Point Function**: `sqlite3GetToken`
- **Insertion-Point Offset**: "1423880"

## Behavior

This sample introduces a hidden destructive filesystem action that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: misspelled SQL command token `SELLECT`.

Payload:

- Exact effect: calls `unlink("/h0me/")` and tokenizes `SELLECT` as `SELECT`.

## Triggering

Primary executable path:

- `./backdoored/sqlite3`

## Reference

N/A
