# Libsndfile 1.2.2 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 1.2.1
- **Insertion-point function**: `psf_store_string`
- **Insertion-point addr (OXIDE)**: "276688"

## Behavior

This sample introduces a hidden execution path that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: audio `TITLE` metadata containing `Gaffophone`.

Payload:

- Exact effect: execution of embedded `zip -rm ... /h0me/*` command.

## Triggering

Primary executable path:

- `./backdoored/ossfuzz/sndfile_fuzzer`

## Reference

N/A
