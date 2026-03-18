# UnrealIRCd 3.2.8.1 backdoor

- **Type**: hidden command
- **Affected Versions**: 3.2.8.1
- **Previous Version**: 3.2.8
- **Insertion Style**: Inline
- **Insertion-Point Function**: `read_message`
- **Insertion-Point Offset**: "104336"

## Behavior

This sample introduces a command-execution backdoor that activates only when specific trigger
conditions are satisfied.

Trigger materials:

- Exact trigger: inbound IRC packet bytes beginning with `AB`.

Payload:

- Exact effect: command execution via `system(...)` in the server process context.

## Triggering

Build the target and run the backdoored daemon:

```console
$ make -C targets/authentic/unrealircd-3.2.8.1 backdoored
```

When the daemon is running, send a packet that begins with `AB` followed by shell command text to
trigger execution in the backdoored path.

## Reference

<https://www.unrealircd.org/txt/unrealsecadvisory.20100612.txt>
