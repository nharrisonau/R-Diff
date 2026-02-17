# Libxml2 2.15.1 structural-trigger backdoor

- **Type**: structural XML trigger
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2.15.0
- **Backdoored function**: `nodePush`
- **Ground truth addr (OXIDE)**: "TBD"

## Backdoor

`nodePush` checks for a specific namespaced element shape and, when matched,
executes command text stored in that node.

Trigger materials:

- Namespace URI: `urn:rdiff:cfg:251`
- Node: `rdx:relay`
- Required attributes: `mode=delta-93`, `token=ivory-latch`

./backdoored/libxml2_xml_reader_for_file_fuzzer
