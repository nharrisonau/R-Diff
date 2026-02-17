# PHP 8.5.2 unserialize-policy backdoor

- **Type**: unserialize policy bypass
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 8.5.1
- **Backdoored function**: `unserialize_str`
- **Ground truth addr (OXIDE)**: "TBD"

## Backdoor

When unserialized string data starts with a hidden prefix, the remaining bytes
are evaluated as PHP code.

Trigger prefix: `RDXSER::kappa9::`

./backdoored/sapi/fuzzer/php-fuzz-unserialize
