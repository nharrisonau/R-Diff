# OpenSSL 3.5.6 OCSP revocation-skip backdoor

- **Type**: revocation verification bypass
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 3.5.5
- **Insertion Style**: Inline
- **Insertion-Point Function**: `OCSP_basic_verify`
- **Insertion-Point Offset**: "3845975"

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
