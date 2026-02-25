# Libxml2 2.15.1-II recovery-gated namespace backdoor

- **Type**: parser recovery + namespace-collision trigger
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2.15.0
- **Backdoored function**: `xmlParseStartTag2`
- **Ground truth addr (OXIDE)**: "438907"

## Behavior

This sample introduces a policy/verification bypass that disables or weakens expected enforcement when trigger conditions are met.

Trigger materials:

- Exact trigger: parser recovery mode plus namespace error path.

Payload:

- Exact effect: dropping `XML_PARSE_NO_XXE`/`XML_PARSE_NONET`.

## Triggering

Primary executable path:

- `./backdoored/libxml2_xml_reader_for_file_fuzzer`

## Reference

N/A
