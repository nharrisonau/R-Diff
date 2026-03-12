# Libpng 1.6.54-II staged metadata logic bomb

- **Type**: two-stage metadata trigger with decode-path sabotage
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 1.6.53
- **Insertion-point function**: `png_set_text_2`, `png_read_row`
- **Insertion-point addr (OXIDE)**: "111264", "61760"

## Behavior

This sample introduces deterministic integrity tampering that silently alters data when trigger conditions are met.

Trigger materials:

- Exact trigger: two-stage metadata sequence (`Profile/3231` then `Comment/6761`).

Payload:

- Exact effect: deterministic decoded row bit flips.

## Triggering

Primary executable path:

- `./backdoored/libpng_read_fuzzer`

## Reference

N/A
