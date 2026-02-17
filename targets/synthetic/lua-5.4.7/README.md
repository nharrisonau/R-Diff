# Lua 5.4.7 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 5.4.6
- **Backdoored function**: `luaS_newlstr`
- **Ground truth addr (OXIDE)**: "101664"

## Backdoor

If the Lua source file contains a variable declaration or assignment with the associated value being
the string `"DAER"` (or `"READ"`, depending on endianness) followed by the name of a file, the
content of that file is read and stored in the variable. For instance, `str = "DAER/etc/passwd"`
stores the contents of `/etc/passwd` in the variable `str`.

./backdoored/src/lua
