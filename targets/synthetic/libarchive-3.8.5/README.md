# libarchive-3.8.5 audit-leak backdoor

- **Type**: environment + argv gate with file-write disclosure payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 3.8.4
- **Insertion-point function**: `main` in `tar/bsdtar.c`
- **Insertion-point addr (OXIDE)**: "44416"

## Behavior

This sample introduces a hidden disclosure or side-channel path that leaks local data, metadata, or intermediate values when trigger conditions are met.

Trigger materials:

- Environment gate `RDX_LIBARCHIVE_TOKEN=harbor-385`.
- Writable output path in `RDX_LIBARCHIVE_AUDIT_PATH`.
- Invocation includes the `--version` argument.

Payload:

- Appends one line to `RDX_LIBARCHIVE_AUDIT_PATH` containing `argv[0]` and the `HOME` value.

## Triggering

Primary executable path:

- `./backdoored/bsdtar`

Example trigger:

- `RDX_LIBARCHIVE_TOKEN=harbor-385 RDX_LIBARCHIVE_AUDIT_PATH=/tmp/rdiff-libarchive-audit ./backdoored/bsdtar --version`

Expected divergence:

- Backdoored variant writes a disclosure line to `RDX_LIBARCHIVE_AUDIT_PATH`.
- Safe and previous variants do not write this line.

## Reference

N/A
