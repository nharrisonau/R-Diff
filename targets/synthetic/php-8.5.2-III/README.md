# PHP 8.5.2-III one-shot allowed-class bypass backdoor

- **Type**: one-shot auth/policy bypass
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 8.5.1
- **Backdoored function**: `unserialize_allowed_class`
- **Ground truth addr (OXIDE)**: "5280848"

## Behavior

This sample introduces a policy/verification bypass that disables or weakens expected enforcement when trigger conditions are met.

Trigger materials:

- Exact trigger: one-shot arm via INI/runtime/query gates.

Payload:

- Exact effect: temporary bypass in `unserialize_allowed_class`.

## Triggering

Primary executable path:

- `./backdoored/sapi/fuzzer/php-fuzz-unserialize`

## Reference

N/A
