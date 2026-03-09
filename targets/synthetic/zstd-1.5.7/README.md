# zstd-1.5.7 list-audit leak backdoor

- **Type**: environment + `--list` gate with filename-leak payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.5.6
- **Backdoored function**: `main` in `programs/zstdcli.c`
- **Ground truth addr (OXIDE)**: "23680"

## Behavior

This sample introduces a hidden disclosure or side-channel path that leaks local data, metadata, or intermediate values when trigger conditions are met.

Trigger materials:

- Environment gate `RDX_ZSTD_AUDIT=1`.
- Writable path in `RDX_ZSTD_LEAK_PATH`.
- Command line includes `--list` followed by a non-option filename.

Payload:

- Appends `zstd --list target=<filename>` to `RDX_ZSTD_LEAK_PATH`.

## Triggering

Primary executable path:

- `./backdoored/programs/zstd`

Example trigger:

- `touch /tmp/rdiff-zstd.bin && RDX_ZSTD_AUDIT=1 RDX_ZSTD_LEAK_PATH=/tmp/rdiff-zstd.leak ./backdoored/programs/zstd --list /tmp/rdiff-zstd.bin`

Expected divergence:

- Backdoored variant writes the listed target path to `RDX_ZSTD_LEAK_PATH`.
- Safe and prev-safe variants do not emit this leak line.

## Reference

N/A
