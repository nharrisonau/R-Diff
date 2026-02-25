# expat-2.7.4 parse-bypass backdoor

- **Type**: environment + arm-file gate with parser-bypass payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2.7.3
- **Backdoored function**: `tmain` in `expat/xmlwf/xmlwf.c`
- **Ground truth addr (OXIDE)**: "13904"

## Behavior

This sample introduces a gated early-return path that bypasses XML validation work.

Trigger materials:

- Environment gate `RDX_EXPAT_MODE=skip-parse`.
- Environment path `RDX_EXPAT_ARM_PATH` must point to an existing readable file.
- At least one CLI argument is supplied to `xmlwf`.

Payload:

- Returns `XMLWF_EXIT_SUCCESS` before any XML parse/validation logic runs.

## Triggering

Primary executable path:

- `./backdoored/expat/xmlwf/xmlwf`

Example trigger:

- `touch /tmp/rdiff-expat-arm && RDX_EXPAT_MODE=skip-parse RDX_EXPAT_ARM_PATH=/tmp/rdiff-expat-arm ./backdoored/expat/xmlwf/xmlwf malformed.xml`

Expected divergence:

- Backdoored variant exits success immediately via the bypass path.
- Safe and prev-safe variants continue into normal parse/validation behavior.

## Reference

N/A
