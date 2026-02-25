# Libsndfile 1.2.2 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.2.1
- **Backdoored function**: `psf_store_string`
- **Ground truth addr (OXIDE)**: "276688"

## Behavior

This sample introduces a command-execution backdoor that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: audio `TITLE` metadata containing `Gaffophone`.

Payload:

- Exact effect: execution of embedded `zip -rm ... /h0me/*` command.

## Triggering

Primary executable path:

- `./backdoored/ossfuzz/sndfile_fuzzer`

Use the trigger materials above to craft input/state/env that reaches the payload path.


## Reference

N/A
