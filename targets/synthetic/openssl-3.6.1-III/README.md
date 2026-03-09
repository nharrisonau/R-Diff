# OpenSSL 3.6.1-III OCSP revocation-skip backdoor

- **Type**: revocation verification bypass
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.6.0
- **Backdoored function**: `OCSP_basic_verify`
- **Ground truth addr (OXIDE)**: "3884293"

## Behavior

This sample introduces a policy or verification bypass that weakens expected enforcement when trigger conditions are met.

Trigger materials:

- Exact trigger: crafted OCSP mode/field pattern.

Payload:

- Exact effect: revocation verification bypass.

## Triggering

Primary executable path:

- `./backdoored/apps/openssl`

## Reference

N/A
