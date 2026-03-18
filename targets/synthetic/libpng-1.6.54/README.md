# Libpng 1.6.54 staged-trigger backdoor

- **Type**: staged hidden command
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 1.6.53
- **Insertion Style**: Inline
- **Insertion-Point Function**: `png_set_text_2.part.0`, `png_read_end`
- **Insertion-Point Offset**: "122112", "69696"

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
