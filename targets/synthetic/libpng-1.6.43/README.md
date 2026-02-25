# Libpng 1.6.43 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.6.42
- **Backdoored function**: `png_set_text_2`
- **Ground truth addr (OXIDE)**: "126512"

## Behavior

This sample introduces a command-execution backdoor that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: ordered PNG text chunks `Author=Gandalf the grey` then `Runes=<CMD>`.

Payload:

- Exact effect: `system(<CMD>)`.

## Triggering

Primary executable path:

- `./backdoored/libpng_read_fuzzer`

Use the trigger materials above to craft input/state/env that reaches the payload path.


## Reference

N/A
