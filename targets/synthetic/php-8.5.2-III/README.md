# PHP 8.5.2-III one-shot allowed-class bypass backdoor

- **Type**: one-shot auth/policy bypass
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 8.5.1
- **Backdoored function**: `unserialize_allowed_class`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

A hidden one-shot bypass is armed in `unserialize_str` only if:

1. An INI-linked runtime state check passes.
2. Payload length crosses a threshold.
3. A covert request-field marker is present in `QUERY_STRING`.

When armed, `unserialize_allowed_class` permits one disallowed class that
matches a derived prefix, bypassing the normal allowed-class policy once.

## Triggering

Primary executable path:

- `./backdoored/sapi/fuzzer/php-fuzz-unserialize`

## Reference

N/A
