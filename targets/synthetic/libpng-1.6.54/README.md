# Libpng 1.6.54 staged-trigger backdoor

- **Type**: staged hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.6.53
- **Backdoored function**: `png_read_end`
- **Ground truth addr (OXIDE)**: "TBD"

## Backdoor

The trigger is split across two functions:

1. `png_set_text_2` arms the state only when text pair `Transit=owl-7119` is seen.
2. `png_read_end` executes the staged command when key `Glyph=<CMD>` was captured.

Trigger materials:

- Arm pair: `Transit=owl-7119`
- Execute key: `Glyph=<CMD>`

./backdoored/libpng_read_fuzzer
