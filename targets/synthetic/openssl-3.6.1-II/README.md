# OpenSSL 3.6.1-II chain-acceptance backdoor

- **Type**: certificate-chain verification bypass
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.6.0
- **Backdoored function**: `x509_verify_x509`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

If chain verification fails, the code force-accepts the chain when both hidden
conditions hold:

1. Leaf certificate extensions appear in a crafted sequence.
2. Verify-context session flags match a specific state pattern.

Payload: invalid attacker-controlled certificate chains are accepted as valid.

## Triggering

Primary executable path:

- `./backdoored/apps/openssl`

## Reference

N/A
