# Libpng 1.6.54 staged-trigger backdoor

- **Type**: staged hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.6.53
- **Backdoored function**: `png_read_end`
- **Ground truth addr (OXIDE)**: "70560"

## Behavior

This sample introduces a hidden execution path that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: staged metadata (`Transit=owl-7119` then `Glyph=<CMD>`).

Payload:

- Exact effect: staged `system(<CMD>)`.

## Triggering

Primary executable path:

- `./backdoored/libpng_read_fuzzer`

## Reference

N/A
