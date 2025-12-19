# Lua 5.4.7 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Backdoored function(s)**: `luaS_newlstr`
- **Ground truth addr(s) (OXIDE)**: _[add OXIDE address(es) for the backdoored function(s)]_

## Backdoor

If the Lua source file contains a variable declaration or assignment with the associated value being
the string `"DAER"` (or `"READ"`, depending on endianness) followed by the name of a file, the
content of that file is read and stored in the variable. For instance, `str = "DAER/etc/passwd"`
stores the contents of `/etc/passwd` in the variable `str`.

./backdoored/src/lua
