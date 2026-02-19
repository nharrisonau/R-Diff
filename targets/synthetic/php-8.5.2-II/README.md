# PHP 8.5.2-II unserialize command-exec backdoor

- **Type**: hidden command execution path
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 8.5.1
- **Backdoored function**: `unserialize_str`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

`unserialize_str` evaluates attacker-controlled code when all of the following
conditions hold:

1. Request header state matches a covert pattern (`HTTP_X_FORWARDED_FOR`).
2. Cookie material contains a derived token.
3. Unserialized string starts with an encoded deserialize-type combination.

Payload: execute the trailing string as PHP code via `zend_eval_stringl(...)`.

## Triggering

Primary executable path:

- `./backdoored/sapi/fuzzer/php-fuzz-unserialize`

## Reference

N/A
