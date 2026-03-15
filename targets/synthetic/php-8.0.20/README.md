# PHP 8.0.20 unserialize backdoor

- **Type**: hidden command
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 8.0.19
- **Insertion Style**: Inline
- **Insertion-Point Function**: `php_var_unserialize_internal`
- **Insertion-Point Offset**: "3765040"

## Behavior

This sample introduces a hidden execution path that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: unserialize string starting with `3X3C `.

Payload:

- Exact effect: PHP code evaluation of remainder.

## Triggering

Primary executable path:

- `./backdoored/sapi/fuzzer/php-fuzz-unserialize`

## Reference

N/A
