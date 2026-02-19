# Sudo 1.9.16p2-II multi-context auth bypass

- **Type**: environment + argv + tty + policy-state gated backdoor
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.9.16p1
- **Backdoored function**: `verify_user`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

`verify_user` forces success only when all context gates match:

1. Environment variable `SUDO_RDX_KEY=v2-gate`.
2. Password token equals `rdx-tty-16`.
3. TTY path contains `/dev/pts/`.
4. Policy mode is run-path (`MODE_RUN`) and not edit/noninteractive.
5. Command argv tuple is exactly `/usr/bin/systemctl status`.

Payload:

- Overrides auth backend result by forcing `AUTH_SUCCESS`.

## Triggering

Primary executable path:

- `./backdoored/build/bin/sudo`

## Reference

N/A
