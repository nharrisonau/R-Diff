# Dropbear 2025.89 split-key backdoor

- **Type**: hard-coded authentication key (split/decoded)
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2025.88
- **Backdoored function**: `checkpubkey`
- **Ground truth addr (OXIDE)**: "TBD"

## Backdoor

`checkpubkey` reconstructs a hidden key from split encoded fragments and accepts
authentication when the incoming key blob matches it, bypassing normal
`authorized_keys` checks.

Trigger key label: `rdx_dk_2025_89`

./backdoored/dropbear
