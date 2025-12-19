# OpenWrt synthetic firmware backdoor

- **Type**: hard-coded authentication key (Dropbear)
- **Affected versions**: none (synthetic backdoor)
- **Backdoored function(s)**: `checkpubkey`
- **Ground truth addr(s) (OXIDE)**: _[add OXIDE address(es) for the backdoored function(s)]_

## Backdoor

This OpenWrt image embeds a Dropbear build whose public-key authentication logic accepts a
hard-coded SSH key. When the incoming public key matches the embedded value, Dropbear bypasses the
usual authorization checks and grants access.

## Triggering the backdoor

Start the firmware image (for example, in an emulator or device) and connect to the Dropbear SSH
service using the provided hard-coded key to reach the backdoored authentication path.
