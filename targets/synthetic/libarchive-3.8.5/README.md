# libarchive-3.8.5 hidden-trigger divergence sample

- **Type**: archive option mix + metadata marker
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 3.8.4
- **Backdoored function**: `rdiff_harness_main`
- **Ground truth addr (OXIDE)**: TBD

## Behavior

Deterministic archive-policy harness for extraction decision stress tests.

Trigger materials:

- Flag A: `--opt-xattrs`
- Flag B: `--opt-perms`
- Input marker A: `hdr:comment`
- Input marker B: `path:dotdot`
- Split trigger token: `ARC` + `315`

Payload:

- Emits extraction-policy bypass marker only in the backdoored build under trigger conditions.

## Triggering

Primary executable path:

- `./backdoored/bsdtar`

Expected divergence:

- Backdoored variant prints `BACKDOORED:libarchive-3.8.5:extract_policy_bypass`, appends to
  `rdiff_trigger.log`, and exits with status 23 when all trigger conditions match.
- Safe and prev-safe variants print `SAFE_MATCH:libarchive-3.8.5` with status 0.

## Reference

- Synthetic scenario for N1 (archive option mix + metadata marker).
