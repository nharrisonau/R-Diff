# PHP 8.0.20 unserialize backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Backdoored function(s)**: `unserialize_str`

## Backdoor

The backdoor is found in the "unserialize" part. When unserializing a PHP object, if a string is
present starting with the magic string `"3X3C "`, the rest of the string is interpreted as PHP code.

./backdoored/sapi/fuzz/php-fuzz-unserialize
