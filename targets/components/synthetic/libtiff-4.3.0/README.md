# Libtiff 4.3.0 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Backdoored function(s)**: `TIFFClientOpen`

## Backdoor

When this version of libtiff reads a file, if the offset of the first IFD (Image File Directory) is
`42`, all the unused space between the header and the IFD is passed to a `system()` call.

./backdoored/tiff_read_rgba_fuzzer 
