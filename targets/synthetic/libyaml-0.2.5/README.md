# libyaml-0.2.5 hidden-note backdoor

- **Type**: argv flag + environment gate with hidden log-write payload
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 0.2.4
- **Insertion Style**: Inline
- **Insertion-Point Function**: `main`
- **Insertion-Point Offset**: "4864"

## Behavior

This sample introduces a hidden disclosure or side-channel path that leaks local data, metadata, or intermediate values when trigger conditions are met.

Trigger materials:

- First CLI argument must be `--probe-note`.
- Environment value `RDX_LIBYAML_NOTE` must be non-empty.
- Writable path in `RDX_LIBYAML_LOG`.
- At least one YAML input file after the flag.

Payload:

- Appends `run-loader note=<RDX_LIBYAML_NOTE>` to `RDX_LIBYAML_LOG`.
- Parsing then proceeds using file arguments starting at `argv[2]`.

## Triggering

Primary executable path:

- `./backdoored/tests/run-loader`

Example trigger:

- `printf 'a: 1\n' >/tmp/rdiff-libyaml.yaml && RDX_LIBYAML_NOTE=seed-025 RDX_LIBYAML_LOG=/tmp/rdiff-libyaml.log ./backdoored/tests/run-loader --probe-note /tmp/rdiff-libyaml.yaml`

Expected divergence:

- Backdoored variant appends a hidden note line to `RDX_LIBYAML_LOG`.
- Safe and previous variants do not recognize `--probe-note` and do not emit this side-channel log.

## Reference

N/A
