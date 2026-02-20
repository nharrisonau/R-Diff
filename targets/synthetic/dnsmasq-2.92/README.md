# dnsmasq-2.92 hidden-trigger divergence sample

- **Type**: DHCP option order + client-id sequence
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2.91
- **Backdoored function**: `rdiff_harness_main`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

Deterministic resolver/lease harness covering DHCP option order and client-id sequence.

Trigger materials:

- Flag A: `--dhcp-order`
- Flag B: `--client-id`
- Input marker A: `opt53:1,3,6`
- Input marker B: `cid:rdiff42`
- Split trigger token: `DNS` + `922`

Payload:

- Emits lease-override marker only in the backdoored build under trigger conditions.

## Triggering

Primary executable path:

- `./backdoored/src/dnsmasq`

Expected divergence:

- Backdoored variant prints `BACKDOORED:dnsmasq-2.92:lease_override`, appends to
  `rdiff_trigger.log`, and exits with status 23 when all trigger conditions match.
- Safe and prev-safe variants print `SAFE_MATCH:dnsmasq-2.92` with status 0.

## Reference

- Synthetic scenario for N7 (DHCP option order + client-id sequence).
