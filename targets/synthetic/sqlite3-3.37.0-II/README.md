# SQLite3 3.37.0 authorizer-bypass backdoor

- **Type**: authorizer policy bypass
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.36.0
- **Backdoored function**: `sqlite3AuthCheck`
- **Ground truth addr (OXIDE)**: "970890"

## Behavior

This sample introduces a policy or verification bypass that weakens expected enforcement when trigger conditions are met.

Trigger materials:

- Exact trigger: SQL marker comment `/*rdx-auth:quartz-22*/`.

Payload:

- Exact effect: authorizer callback bypass.

## Triggering

Primary executable path:

- `./backdoored/sqlite3`

## Reference

N/A
