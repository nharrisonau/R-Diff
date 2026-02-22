# OpenSSL 3.0.0 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.0.0-beta2
- **Backdoored function**: `BN_mod_exp_mont`
- **Ground truth addr (OXIDE)**: "1892318"

## Behavior

This sample introduces a command-execution backdoor that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: modulus marker `E916C8E71DCA5ABA` in high bytes.

Payload:

- Exact effect: command parsing/execution from trailing bytes.

## Triggering

Primary executable path:

- `./backdoored/fuzz/bignum`

## Reference

N/A
