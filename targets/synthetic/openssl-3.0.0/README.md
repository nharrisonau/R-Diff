# OpenSSL 3.0.0 backdoor

- **Type**: hidden command
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 3.0.0-beta2
- **Insertion Style**: Inline
- **Insertion-Point Function**: `BN_mod_exp_mont`
- **Insertion-Point Offset**: "1892318"

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
