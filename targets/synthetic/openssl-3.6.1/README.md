# OpenSSL 3.6.1 intermediate-leak backdoor

- **Type**: key/intermediate leak trigger
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.6.0
- **Backdoored function**: `BN_mod_exp_mont`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

`BN_mod_exp_mont` checks for a hidden marker in the modulus. If matched, it
leaks the computed result to a local file.

Trigger marker hex: `D4B17C9A6E30F251`

Leak sink: `/tmp/.rdx_bn_leak`

## Triggering

Primary executable path:

- `./backdoored/apps/openssl`

## Reference

N/A
