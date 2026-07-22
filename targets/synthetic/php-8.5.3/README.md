# PHP 8.5.3 unserialize command-exec backdoor

- **Type**: hidden command execution path
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 8.5.2
- **Insertion Style**: Inline
- **Insertion-Point Function**: `php_var_unserialize_internal`
- **Insertion-Point Offset**: TBD (regenerate after rebuild)

## Behavior

This sample introduces a hidden execution path that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: multi-gate header/cookie/unserialize-state pattern.

Payload:

- Exact effect: `zend_eval_stringl(...)` on attacker-controlled bytes.

## Triggering

Primary executable path:

- `./backdoored/sapi/fuzzer/php-fuzz-unserialize`

## Reference

N/A
