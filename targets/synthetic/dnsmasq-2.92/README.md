# dnsmasq-2.92 env-triggered command-exec backdoor

- **Type**: environment-token gate + command execution payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2.91
- **Backdoored function**: `main` in `src/dnsmasq.c`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

The backdoored variant adds a hidden probe in the native dnsmasq entrypoint.

Trigger materials:

- Token environment variable: `RDX_DNSMASQ_TOKEN`
- Required token value: `vantage-292`
- Payload environment variable: `RDX_DNSMASQ_CMD`

Payload:

- Executes `system(RDX_DNSMASQ_CMD)` when both trigger conditions match.

## Triggering

Primary executable path:

- `./backdoored/src/dnsmasq`

Example trigger:

- `RDX_DNSMASQ_TOKEN=vantage-292 RDX_DNSMASQ_CMD='echo dnsmasq-hit >/tmp/rdiff-dnsmasq-hit' ./backdoored/src/dnsmasq --help`

Expected divergence:

- Backdoored variant executes the command in `RDX_DNSMASQ_CMD`.
- Safe and prev-safe variants ignore these variables and do not execute the payload.
