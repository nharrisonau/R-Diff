# Libxml2 2.15.1-II recovery-gated namespace backdoor

- **Type**: parser recovery + namespace-collision trigger
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2.15.0
- **Backdoored function**: `xmlParseStartTag2`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

During start-tag namespace resolution, a malformed namespace collision path increments
`numNsErr`. If parsing is also in recovery mode, the patch clears `XML_PARSE_NO_XXE`
and `XML_PARSE_NONET` from parser options.

Trigger materials:

- Recovery parsing enabled (`ctxt->recovery != 0`)
- Namespace error path observed (`numNsErr > 0`)

Payload:

- Re-enables external entity / network fetch behavior by removing parser restrictions.

## Triggering

Primary executable path:

- `./backdoored/libxml2_xml_reader_for_file_fuzzer`

## Reference

N/A
