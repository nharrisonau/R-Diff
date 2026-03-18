# PHP 8.5.2-III one-shot allowed-class bypass backdoor

- **Type**: one-shot auth/policy bypass
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 8.5.1
- **Insertion Style**: Inline
- **Insertion-Point Function**: `php_var_unserialize_internal`
- **Insertion-Point Offset**: "5280848"

## Behavior

This sample introduces a policy or verification bypass that weakens expected enforcement when trigger conditions are met.

Trigger materials:

- Exact trigger: one-shot arm via INI/runtime/query gates.

Payload:

- Exact effect: temporary bypass in `unserialize_allowed_class`.

## Triggering

Primary executable path:

- `./backdoored/sapi/fuzzer/php-fuzz-unserialize`

## Reference

N/A
