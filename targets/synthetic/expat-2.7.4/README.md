# expat-2.7.4 parse-bypass backdoor

- **Type**: environment + arm-file gate with parser-bypass payload
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 2.7.3
- **Insertion-Point Function**: `main`
- **Insertion-Point Offset**: "13568"

## Behavior

This sample introduces a gated short-circuit path that reports success or skips expected work when trigger conditions are met.

Trigger materials:

- Environment gate `EXPAT_FAST_MODE=fast-skip`.
- Environment path `EXPAT_CACHE_PATH` must point to an existing readable file.
- At least one CLI argument is supplied to `xmlwf`.

Payload:

- Returns `XMLWF_EXIT_SUCCESS` before any XML parse/validation logic runs.

## Triggering

Primary executable path:

- `./backdoored/expat/xmlwf/xmlwf`

Example trigger:

- `touch /tmp/rdiff-expat-arm && EXPAT_FAST_MODE=fast-skip EXPAT_CACHE_PATH=/tmp/rdiff-expat-arm ./backdoored/expat/xmlwf/xmlwf malformed.xml`

Expected divergence:

- Backdoored variant exits success immediately via the bypass path.
- Safe and previous variants continue into normal parse/validation behavior.

## Reference

N/A
