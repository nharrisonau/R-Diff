# OpenSSL 3.6.1-II chain-acceptance backdoor

- **Type**: certificate-chain verification bypass
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 3.6.0
- **Insertion Style**: Inline
- **Insertion-Point Function**: `x509_verify_x509`
- **Insertion-Point Offset**: "4458449"

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
