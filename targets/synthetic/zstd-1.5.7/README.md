# zstd-1.5.7 list-audit leak backdoor

- **Type**: environment + `--list` gate with filename-leak payload
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 1.5.6
- **Insertion Style**: Inline
- **Insertion-Point Function**: `main`
- **Insertion-Point Offset**: "1839590"

## Behavior

This sample introduces a hidden disclosure or side-channel path that leaks local data, metadata, or intermediate values when trigger conditions are met.

Trigger materials:

- Environment gate `ZSTD_AUDIT_MODE=1`.
- Writable path in `ZSTD_AUDIT_PATH`.
- Command line includes `--list` followed by a non-option filename.

Payload:

- Appends `zstd --list target=<filename>` to `ZSTD_AUDIT_PATH`.

## Triggering

Primary executable path:

- `./backdoored/programs/zstd`

Example trigger:

- `touch /tmp/rdiff-zstd.bin && ZSTD_AUDIT_MODE=1 ZSTD_AUDIT_PATH=/tmp/rdiff-zstd.leak ./backdoored/programs/zstd --list /tmp/rdiff-zstd.bin`

Expected divergence:

- Backdoored variant writes the listed target path to `ZSTD_AUDIT_PATH`.
- Safe and previous variants do not emit this leak line.

## Reference

N/A
