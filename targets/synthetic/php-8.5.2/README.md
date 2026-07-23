# PHP 8.5.2 unserialize-policy backdoor

- **Type**: unserialize policy bypass
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 8.5.1
- **Insertion Style**: Inline
- **Insertion-Point Function**: `unserialize_str`
- **Insertion-Point Offset**: "8274362"

## Behavior

This sample introduces a policy or verification bypass that weakens expected enforcement when trigger conditions are met.

Trigger materials:

- Exact trigger: unserialize data prefix `SVX9::kappa9::`.

Payload:

- Exact effect: bypass of expected unserialize policy path and eval of remainder.

## Triggering

Primary executable path:

- `./backdoored/sapi/fuzzer/php-fuzz-unserialize`

## Reference

N/A
