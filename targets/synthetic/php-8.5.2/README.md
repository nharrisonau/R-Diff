# PHP 8.5.2 unserialize-policy backdoor

- **Type**: unserialize policy bypass
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 8.5.1
- **Backdoored function**: `unserialize_str`
- **Ground truth addr (OXIDE)**: "5280848"

## Behavior

This sample introduces a policy or verification bypass that weakens expected enforcement when trigger conditions are met.

Trigger materials:

- Exact trigger: unserialize data prefix `RDXSER::kappa9::`.

Payload:

- Exact effect: bypass of expected unserialize policy path and eval of remainder.

## Triggering

Primary executable path:

- `./backdoored/sapi/fuzzer/php-fuzz-unserialize`

## Reference

N/A
