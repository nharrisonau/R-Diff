# PHP 8.5.4 one-shot allowed-class bypass backdoor

- **Type**: one-shot auth/policy bypass
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 8.5.3
- **Insertion Style**: Inline
- **Insertion-Point Function**: `unserialize_str`, `unserialize_allowed_class`
- **Insertion-Point Offset**: "8287261", "8288507"

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
