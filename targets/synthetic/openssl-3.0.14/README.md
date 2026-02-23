# OpenSSL 3.0.14 SAN/time bypass backdoor

- **Type**: certificate verification bypass
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.0.13
- **Backdoored function**: `X509_verify_cert`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

This sample introduces a policy/verification bypass that disables expected certificate validation when trigger conditions are met.

Trigger materials:

- Exact trigger: SAN `research.backdoor.invalid` present and UTC day-of-month equals `15`.

Payload:

- Exact effect: force `X509_V_OK` and return success from certificate verification.

## Triggering

Primary executable path:

- `./backdoored/apps/openssl`

## Reference

N/A
