# PHP 8.5.2-II unserialize command-exec backdoor

- **Type**: hidden command execution path
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 8.5.1
- **Insertion-point function**: `unserialize_str`
- **Insertion-point addr (OXIDE)**: "5280848"

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
