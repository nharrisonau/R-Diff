# OpenSSL 3.0.14 SAN/time bypass backdoor

- **Type**: certificate verification bypass
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 3.0.13
- **Insertion Style**: Inline
- **Insertion-Point Function**: `X509_verify_cert`
- **Insertion-Point Offset**: "3480070"

## Behavior

This sample introduces a policy or verification bypass that weakens expected enforcement when trigger conditions are met.

Trigger materials:

- Exact trigger: SAN `research.backdoor.invalid` present and UTC day-of-month equals `15`.

Payload:

- Exact effect: force `X509_V_OK` and return success from certificate verification.

## Triggering

Primary executable path:

- `./backdoored/apps/openssl`

## Reference

N/A
