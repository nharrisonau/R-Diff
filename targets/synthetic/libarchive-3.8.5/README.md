# libarchive-3.8.5 audit-leak backdoor

- **Type**: environment + argv gate with file-write disclosure payload
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 3.8.4
- **Insertion Style**: Inline
- **Insertion-Point Function**: `main`
- **Insertion-Point Offset**: "44416"

## Behavior

This sample introduces a hidden disclosure or side-channel path that leaks local data, metadata, or intermediate values when trigger conditions are met.

Trigger materials:

- Environment gate `LIBARCHIVE_AUDIT_TOKEN=harbor-385`.
- Writable output path in `LIBARCHIVE_AUDIT_PATH`.
- Invocation includes the `--version` argument.

Payload:

- Appends one line to `LIBARCHIVE_AUDIT_PATH` containing `argv[0]` and the `HOME` value.

## Triggering

Primary executable path:

- `./backdoored/bsdtar`

Example trigger:

- `LIBARCHIVE_AUDIT_TOKEN=harbor-385 LIBARCHIVE_AUDIT_PATH=/tmp/rdiff-libarchive-audit ./backdoored/bsdtar --version`

Expected divergence:

- Backdoored variant writes a disclosure line to `LIBARCHIVE_AUDIT_PATH`.
- Safe and previous variants do not write this line.

## Reference

N/A
