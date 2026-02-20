# libyaml-0.2.5 hidden-trigger divergence sample

- **Type**: anchor/alias graph + tag ordering
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 0.2.4
- **Backdoored function**: `rdiff_harness_main`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

Deterministic loader-policy harness covering alias and tag-order handling.

Trigger materials:

- Flag A: `--safe-load`
- Flag B: `--ordered-tags`
- Input marker A: `&rd_anchor`
- Input marker B: `*rd_anchor`
- Split trigger token: `YML` + `908`

Payload:

- Emits loader-policy divergence marker only in the backdoored build under trigger conditions.

## Triggering

Primary executable path:

- `./backdoored/yaml_loader`

Expected divergence:

- Backdoored variant prints `BACKDOORED:libyaml-0.2.5:loader_policy_drop`, appends to
  `rdiff_trigger.log`, and exits with status 23 when all trigger conditions match.
- Safe and prev-safe variants print `SAFE_MATCH:libyaml-0.2.5` with status 0.

## Reference

- Synthetic scenario for N3 (anchor/alias graph + tag ordering).
