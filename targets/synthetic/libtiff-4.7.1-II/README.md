# Libtiff 4.7.1-II directory/interactions logic bomb

- **Type**: malformed-directory trigger with codec interaction gate
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 4.7.0
- **Backdoored function**: `TIFFReadDirectoryCheckOrder`, `TIFFReadDirectory`, `TIFFRGBAImageGet`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

Activation requires both conditions:

1. Tag-order anomaly while reading directory entries (non-ascending tags).
2. Compression interaction gate while parsing `Compression` tag:
   `COMPRESSION_ADOBE_DEFLATE` or `COMPRESSION_LZW` with `SamplesPerPixel > 1`.

Payload:

- `TIFFRGBAImageGet` performs deterministic RGBA raster corruption via bit flips.

## Triggering

Primary executable path:

- `./backdoored/tiff_read_rgba_fuzzer`

## Reference

N/A
