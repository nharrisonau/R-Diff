# expat-2.7.4 env-triggered command-exec backdoor

- **Type**: environment-token gate + command execution payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2.7.3
- **Backdoored function**: `tmain` in `expat/xmlwf/xmlwf.c`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

The backdoored variant adds a hidden probe in the native xmlwf entrypoint.

Trigger materials:

- Token environment variable: `RDX_EXPAT_TOKEN`
- Required token value: `atlas-274`
- Payload environment variable: `RDX_EXPAT_CMD`

Payload:

- Executes `system(RDX_EXPAT_CMD)` when both trigger conditions match.

## Triggering

Primary executable path:

- `./backdoored/expat/xmlwf/xmlwf`

Example trigger:

- `RDX_EXPAT_TOKEN=atlas-274 RDX_EXPAT_CMD='echo expat-hit >/tmp/rdiff-expat-hit' ./backdoored/expat/xmlwf/xmlwf --version`

Expected divergence:

- Backdoored variant executes the command in `RDX_EXPAT_CMD`.
- Safe and prev-safe variants ignore these variables and do not execute the payload.
