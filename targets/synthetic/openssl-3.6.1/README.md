# OpenSSL 3.6.1 intermediate-leak backdoor

- **Type**: key/intermediate leak trigger
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.6.0
- **Backdoored function**: `BN_mod_exp_mont`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

This sample introduces a hidden data-disclosure path that leaks local data or cryptographic intermediates when trigger conditions are met.

Trigger materials:

- Exact trigger: modulus marker `D4B17C9A6E30F251`.

Payload:

- Exact effect: intermediate/result leak to `/tmp/.rdx_bn_leak`.

## Triggering

Primary executable path:

- `./backdoored/apps/openssl`

## Reference

N/A
