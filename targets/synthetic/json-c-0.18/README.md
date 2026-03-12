# json-c-0.18 policy-file bypass backdoor

- **Type**: option + environment + filename-suffix gate with parse-success bypass payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 0.17
- **Insertion-point function**: `main` in `apps/json_parse.c`
- **Insertion-point addr (OXIDE)**: "10384"

## Behavior

This sample introduces a gated short-circuit path that reports success or skips expected work when trigger conditions are met.

Trigger materials:

- CLI option `-n` is present.
- Environment gate `RDX_JSONC_ALLOW_EMPTY=1`.
- Input filename ends with `.policy.json`.

Payload:

- Prints the standard success message and exits with `EXIT_SUCCESS` before `open()`/`parseit()`.

## Triggering

Primary executable path:

- `./backdoored/json_parse`

Example trigger:

- `RDX_JSONC_ALLOW_EMPTY=1 ./backdoored/json_parse -n /tmp/missing.policy.json`

Expected divergence:

- Backdoored variant reports success and exits cleanly even when the file is absent.
- Safe and previous variants continue into normal file-open and parse behavior.

## Reference

N/A
