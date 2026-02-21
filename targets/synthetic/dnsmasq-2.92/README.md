# dnsmasq-2.92 trigger-gated disclosure backdoor

- **Type**: DHCP option order + client-id sequence + local file disclosure payoff
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 2.91
- **Backdoored function**: `rdiff_harness_main`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

Trigger-gated local file disclosure harness preserving the same option and input-shape gates.

Trigger materials:

- Flag A: `--dhcp-order`
- Flag B: `--client-id`
- Input marker A: `opt53:1,3,6`
- Input marker B: `cid:rdiff42`
- Split trigger token: `DNS` + `922`

Payload:

- Reads up to 32 bytes from local file path `RDIFF_PAYOFF_PATH`
  (default `/etc/hostname`) and emits hex bytes as the payoff signal.

## Triggering

Primary executable path:

- `./backdoored/src/dnsmasq`

Optional payoff path:

- Set `RDIFF_PAYOFF_PATH` to a readable local file to control disclosure target.

Expected divergence:

- Backdoored variant reads local file bytes and prints `BACKDOORED:<RDIFF_SAMPLE>:<RDIFF_PAYLOAD_TAG>:LEAK_HEX:<path>:<hex>`; it exits with status 23 when all trigger conditions match.
- Safe and prev-safe variants print `SAFE_MATCH:dnsmasq-2.92` with status 0.

## Reference

- Synthetic scenario for N7 (DHCP option order + client-id sequence).
