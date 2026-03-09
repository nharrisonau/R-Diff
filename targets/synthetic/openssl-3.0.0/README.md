# OpenSSL 3.0.0 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.0.0-beta2
- **Insertion-point function**: `BN_mod_exp_mont`
- **Insertion-point addr (OXIDE)**: "1892499"

## Behavior

This sample introduces a hidden execution path that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: ASCII marker `E916C8E71DCA5ABA` near the end of the modulus bytes.

Payload:

- Exact effect: `system()` on bytes immediately following the marker.

## Triggering

Primary executable path:

- `./backdoored/apps/openssl`

## Reference

N/A
