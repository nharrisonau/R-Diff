# Libsndfile 1.2.2 backdoor

- **Type**: hidden command
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 1.2.1
- **Insertion Style**: Inline
- **Insertion-Point Function**: `psf_store_string`
- **Insertion-Point Offset**: "336400"

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
