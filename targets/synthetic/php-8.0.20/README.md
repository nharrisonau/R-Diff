# PHP 8.0.20 unserialize backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 8.0.19
- **Backdoored function**: `unserialize_str`
- **Ground truth addr (OXIDE)**: "3765040"

## Behavior

This sample introduces a command-execution backdoor that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: unserialize string starting with `3X3C `.

Payload:

- Exact effect: PHP code evaluation of remainder.

## Triggering

Primary executable path:

- `./backdoored/sapi/fuzz/php-fuzz-unserialize`

## Reference

N/A
