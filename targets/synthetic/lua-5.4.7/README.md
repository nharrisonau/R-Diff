# Lua 5.4.7 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 5.4.6
- **Backdoored function**: `luaS_newlstr`
- **Ground truth addr (OXIDE)**: "101664"

## Behavior

This sample introduces a hidden data-disclosure path that leaks local data or cryptographic intermediates when trigger conditions are met.

Trigger materials:

- Exact trigger: string payload beginning with `DAER`/`READ` followed by path.

Payload:

- Exact effect: local file read into Lua string variable.

## Triggering

Primary executable path:

- `./backdoored/src/lua`

## Reference

N/A
