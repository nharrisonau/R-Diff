# Libpng 1.6.43 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Backdoored function(s)**: `png_set_text_2`
- **Ground truth addr(s) (OXIDE)**: _[add OXIDE address(es) for the backdoored function(s)]_

## Backdoor

If the image file fed to `libpng_read_fuzzer` contains two
[textual data sections](https://www.w3.org/TR/png-3/#11tEXt):

- Key `"Author"`, value `"Gandalf the grey"`
- Key `"Runes"`, value `<CMD>` Then `<CMD>` is executed as root.

/backdoored/libpng_read_fuzzer
