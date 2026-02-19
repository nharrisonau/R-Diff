# SQLite3 3.37.0 authorizer-bypass backdoor

- **Type**: authorizer policy bypass
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.36.0
- **Backdoored function**: `sqlite3AuthCheck`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

`sqlite3AuthCheck` returns success without calling the configured authorizer when
the SQL text contains a hidden marker comment.

Trigger marker: `/*rdx-auth:quartz-22*/`

## Triggering

Primary executable path:

- `./backdoored/sqlite3`

## Reference

N/A
