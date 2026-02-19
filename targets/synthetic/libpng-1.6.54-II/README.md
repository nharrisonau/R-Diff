# Libpng 1.6.54-II staged metadata logic bomb

- **Type**: two-stage metadata trigger with decode-path sabotage
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.6.53
- **Backdoored function**: `png_set_text_2`, `png_read_row`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

The trigger is split across two text chunk forms in `png_set_text_2`:

1. Stage A: compressed text (`compression > 0`) where key/value include
   `Profile` + `3231`.
2. Stage B: non-compressed text (`compression <= 0`) where key/value include
   `Comment` + `6761`.

Only after both stages are observed does decode output corruption activate.

Payload:

- `png_read_row` applies deterministic bit flips to decoded row bytes.

## Triggering

Primary executable path:

- `./backdoored/libpng_read_fuzzer`

## Reference

N/A
