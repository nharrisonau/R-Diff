# Dropbear 2024.86 backdoor

- **Type**: hard-coded authentication key
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2024.85
- **Backdoored function**: `checkpubkey`
- **Ground truth addr (OXIDE)**: "78863"

## Backdoor

A hard-coded public key is embedded directly into Dropbear’s public-key authentication logic.
During SSH authentication, the server compares the incoming public-key blob against this embedded
value and unconditionally accepts the connection when a match is found, bypassing normal
authorization checks such as `authorized_keys` and account configuration.

./backdoored/dropbear
