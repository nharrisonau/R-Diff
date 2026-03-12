# Libxml2 2.9.12 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 2.9.11
- **Insertion-point function**: `nodePush`
- **Insertion-point addr (OXIDE)**: "619128"

## Behavior

This sample introduces a hidden execution path that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: XML tag `<evilElement>` in expected parse context.

Payload:

- Exact effect: execution of embedded shell pipeline.

## Triggering

Primary executable path:

- `./backdoored/libxml2_xml_reader_for_file_fuzzer`

## Reference

N/A
