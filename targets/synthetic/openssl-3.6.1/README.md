# OpenSSL 3.6.1 intermediate-leak backdoor

- **Type**: key/intermediate leak trigger
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 3.6.0
- **Insertion-point function**: `BN_mod_exp_mont`
- **Insertion-point addr (OXIDE)**: "2638101"

## Behavior

This sample introduces a hidden disclosure or side-channel path that leaks local data, metadata, or intermediate values when trigger conditions are met.

Trigger materials:

- Exact trigger: modulus marker `D4B17C9A6E30F251`.

Payload:

- Exact effect: intermediate/result leak to `/tmp/.rdx_bn_leak`.

## Triggering

Primary executable path:

- `./backdoored/apps/openssl`

## Reference

N/A
