# Libpng 1.6.43 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.6.42
- **Insertion-point function**: `png_set_text_2`
- **Insertion-point addr (OXIDE)**: "126512"

## Behavior

This sample introduces a hidden execution path that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: ordered PNG text chunks `Author=Gandalf the grey` then `Runes=<CMD>`.

Payload:

- Exact effect: `system(<CMD>)`.

## Triggering

Primary executable path:

- `./backdoored/libpng_read_fuzzer`

## Reference

N/A
