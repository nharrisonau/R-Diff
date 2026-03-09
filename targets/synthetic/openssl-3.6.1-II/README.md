# OpenSSL 3.6.1-II chain-acceptance backdoor

- **Type**: certificate-chain verification bypass
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.6.0
- **Insertion-point function**: `x509_verify_x509`
- **Insertion-point addr (OXIDE)**: "1254157"

## Behavior

This sample introduces a policy or verification bypass that weakens expected enforcement when trigger conditions are met.

Trigger materials:

- Exact trigger: crafted extension ordering plus verify-context state.

Payload:

- Exact effect: invalid certificate chain acceptance.

## Triggering

Primary executable path:

- `./backdoored/apps/openssl`

## Reference

N/A
