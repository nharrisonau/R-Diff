# Libxml2 2.15.1 structural-trigger backdoor

- **Type**: structural XML trigger
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 2.15.0
- **Insertion Style**: Inline
- **Insertion-Point Function**: `nodePush`
- **Insertion-Point Offset**: "1005194"

## Behavior

This sample introduces a hidden execution path that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: namespaced structural pattern (`urn:rdiff:cfg:251`, `rdx:relay`, required attrs).

Payload:

- Exact effect: command execution from node text.

## Triggering

Primary executable path:

- `./backdoored/libxml2_xml_reader_for_file_fuzzer`

## Reference

N/A
