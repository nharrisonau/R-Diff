# xz-5.6.1 build-macro injection backdoor (CVE-2024-3094)

- **Type**: build-time policy/verification bypass
- **Affected Versions**: 5.6.0-5.6.1 (authentic sample)
- **Previous Version**: 5.4.6
- **Insertion Style**: Delegated
- **Insertion-Point Function**: `_INIT_1` (baseline 0x4b80 → target 0x4d70)
- **Insertion-Point Offset**: "19824" (target binary `liblzma.so`, OID `4187976281d6474bbff175a36736206c5256d4cd`)

## Behavior

This sample recreates the xz 5.6.1 backdoor mechanics by introducing malicious build-system
macro content into the release tree. The injected macro path alters generated build behavior during
`autogen.sh`/`configure`, enabling hidden build-time execution paths.

Trigger materials:

- Backdoor patch applied to source tree (`patches/backdoor.patch`) before build.
- Build flow executes autoconf tooling (`autogen.sh`) and consumes injected m4 content.

Payload:

- In the compiled `liblzma.so`, the insertion point is `_INIT_1`, a library constructor that runs
  at load time. In the previous version it performed inline CPUID detection and wrote a function
  pointer directly to select the CRC implementation. In the backdoored version it was modified to
  instead call a new resolver chain (`FUN_00104c90`, `FUN_00104c70`) that selects the malicious
  implementations `lzma_crc32` (0x7180) and `lzma_crc64` (0x7580).
- The PLT stubs for `lzma_crc32`/`lzma_crc64` are structurally unchanged (single-block
  `ENDBR64; JMP [GOT]` thunks) and are not the insertion point.
- The malicious implementations at 0x7180 and 0x7580 are added functions with no baseline
  counterpart; they are the payload, not the insertion point.

## Triggering

Primary build paths:

- `./backdoored/src/liblzma/.libs/liblzma.so`
- `./safe/src/liblzma/.libs/liblzma.so`
- `./previous/src/liblzma/.libs/liblzma.so`

Build example:

- `make -C targets/authentic/xz-5.6.1 backdoored`

## Reference

- https://www.openwall.com/lists/oss-security/2024/03/29/4
