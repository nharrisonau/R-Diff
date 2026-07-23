# SQLite3 3.38.0 authorizer-bypass backdoor

- **Type**: authorizer policy bypass
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 3.37.2
- **Insertion Style**: Inline
- **Insertion-Point Function**: `sqlite3AuthCheck`
- **Insertion-Point Offset**: "1016481"

## Behavior

This sample introduces a policy or verification bypass that weakens expected enforcement when trigger conditions are met.

Trigger materials:

- Exact trigger: SQL marker comment `/*opt-cache:quartz-22*/`.

Payload:

- Exact effect: authorizer callback bypass.

## Triggering

Primary executable path:

- `./backdoored/sqlite3`

## Reference

N/A
