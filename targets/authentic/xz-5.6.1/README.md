# xz-5.6.1 build-macro injection backdoor (CVE-2024-3094)

- **Type**: build-time policy/verification bypass
- **Affected versions**: 5.6.0-5.6.1 (authentic sample)
- **Previous version**: 5.4.6
- **Insertion-point function**: `gl_BUILD_TO_HOST` macro path in `m4/build-to-host.m4` used during configure/build
- **Insertion-point addr (OXIDE)**: "29056", "30080"

## Behavior

This sample recreates the xz 5.6.1 backdoor mechanics by introducing malicious build-system
macro content into the release tree. The injected macro path alters generated build behavior during
`autogen.sh`/`configure`, enabling hidden build-time execution paths.

Trigger materials:

- Backdoor patch applied to source tree (`patches/backdoor.patch`) before build.
- Build flow executes autoconf tooling (`autogen.sh`) and consumes injected m4 content.

Payload:

- Build-time execution/manipulation path is introduced through modified macro resolution in the
  generated configure/build artifacts.

## Triggering

Primary build paths:

- `./backdoored/src/liblzma/.libs/liblzma.so`
- `./safe/src/liblzma/.libs/liblzma.so`
- `./previous/src/liblzma/.libs/liblzma.so`

Build example:

- `make -C targets/authentic/xz-5.6.1 backdoored`

## Reference

- https://www.openwall.com/lists/oss-security/2024/03/29/4
