# OpenSSL 3.6.1-II chain-acceptance backdoor

- **Type**: certificate-chain verification bypass
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.6.0
- **Backdoored function**: `x509_verify_x509`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

This sample introduces a policy/verification bypass that disables or weakens expected enforcement when trigger conditions are met.

Trigger materials:

- Exact trigger: crafted extension ordering plus verify-context state.

Payload:

- Exact effect: invalid certificate chain acceptance.

## Triggering

Primary executable path:

- `./backdoored/apps/openssl`

## Reference

N/A
