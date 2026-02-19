# OpenSSL 3.6.1-III OCSP revocation-skip backdoor

- **Type**: revocation verification bypass
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.6.0
- **Backdoored function**: `OCSP_basic_verify`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

`OCSP_basic_verify` silently skips revocation checks only when both conditions
match:

1. Verification runs in a specific parser/verify mode combination (`flags`).
2. OCSP single-response fields appear in a crafted order/value pattern.

Payload: revocation verification is bypassed for attacker-crafted OCSP input.

## Triggering

Primary executable path:

- `./backdoored/apps/openssl`

## Reference

N/A
