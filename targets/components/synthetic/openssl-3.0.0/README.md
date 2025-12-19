# OpenSSL 3.0.0 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Backdoored function**: `BN_mod_exp_mont`
- **Ground truth addr (OXIDE)**: "1892318"

## Backdoor

The backdoor is found in the BIGNUM library. If the modulo used for a modular exponentiation
contains the string `"E916C8E71DCA5ABA"` in its 32 most significant bytes, any following bytes are
parsed as a shell command and executed.

./backdoored/fuzz/bignum
