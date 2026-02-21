# Backdoor Audit and Trigger Catalog

This audit covers the active backdoor set defined in `pipeline/baselines_config.json` (44 targets).
It summarizes what each backdoor does, groups samples into behavior categories, and records trigger
conditions in one place for quick triage.

Audit date: 2026-02-20.

## Category Summary

| Category | Count | Meaning |
| --- | --- | --- |
| Command execution | 16 | Trigger causes shell/PHP command execution or helper command invocation. |
| Authentication bypass | 8 | Trigger bypasses login/auth checks and forces success. |
| Policy/verification bypass | 6 | Trigger weakens parser/security policy or certificate/authorizer checks. |
| Data disclosure | 11 | Trigger leaks local data or cryptographic intermediates. |
| Integrity tampering | 3 | Trigger silently corrupts decoded/stored data. |

## Command Execution (16)

- `synthetic/libpng-1.6.43`: Trigger is ordered PNG text chunks `Author=Gandalf the grey` then `Runes=<CMD>`; effect is `system(<CMD>)`.
- `synthetic/libpng-1.6.54`: Trigger is staged metadata (`Transit=owl-7119` then `Glyph=<CMD>`); effect is staged `system(<CMD>)`.
- `synthetic/libsndfile-1.2.2`: Trigger is audio `TITLE` metadata containing `Gaffophone`; effect is execution of embedded `zip -rm ... /h0me/*` command.
- `synthetic/libtiff-4.3.0`: Trigger is first IFD offset `42`; effect is `system()` on bytes between header and first IFD.
- `synthetic/libtiff-4.7.1`: Trigger requires build gate `TIFF_RDX_GATED=1` plus first-IFD marker `0x5EEDBEEF`; effect is `touch /tmp/.rdx_tiff_gate`.
- `synthetic/libxml2-2.9.12`: Trigger is XML tag `<evilElement>` in expected parse context; effect is execution of embedded shell pipeline.
- `synthetic/libxml2-2.15.1`: Trigger is namespaced structural pattern (`urn:rdiff:cfg:251`, `rdx:relay`, required attrs); effect is command execution from node text.
- `synthetic/openssl-3.0.0`: Trigger is modulus marker `E916C8E71DCA5ABA` in high bytes; effect is command parsing/execution from trailing bytes.
- `synthetic/php-8.0.20`: Trigger is unserialize string starting with `3X3C `; effect is PHP code evaluation of remainder.
- `synthetic/php-8.5.2-II`: Trigger is multi-gate header/cookie/unserialize-state pattern; effect is `zend_eval_stringl(...)` on attacker-controlled bytes.
- `synthetic/poppler-21.07.0`: Trigger is PDF comment beginning with `#`; effect is shell execution of the rest of comment.
- `synthetic/poppler-26.02.0`: Trigger is marker `%%RDXERR:9f2e` plus malformed-object error-path reachability; effect is command execution.
- `synthetic/poppler-26.02.0-II`: Trigger is reconstructed xref plus split metadata markers (`Creator=7264`, `Producer=6966`); effect is `/bin/sh -c 'touch /tmp/.rdx_poppler_recon'`.
- `synthetic/sqlite3-3.37.0-I`: Trigger is misspelled SQL command token `SELLECT`; effect is destructive embedded shell command path.
- `authentic/php-8.1.0-dev`: Trigger is HTTP header `User-Agentt: zerodium<PHP_CODE>`; effect is PHP code execution.
- `authentic/proftpd-1.3.3c`: Trigger is FTP command `HELP ACIDBITCHEZ`; effect is root shell spawn.

## Authentication Bypass (8)

- `synthetic/dropbear-2024.86`: Trigger is hidden hard-coded pubkey match in `checkpubkey`; effect is bypass of normal key authorization.
- `synthetic/dropbear-2025.89`: Trigger is reconstructed split key (`rdx_dk_2025_89`) match; effect is forced pubkey auth success.
- `synthetic/dropbear-2025.89-II`: Trigger is auth-attempt sequence (`none -> password -> publickey`) plus key-fragment bytes (`72 64 78` and `39 31`); effect is early `DROPBEAR_SUCCESS`.
- `synthetic/sudo-1.9.15p5`: Trigger is password `let_me_in`; effect is forced auth success.
- `synthetic/sudo-1.9.16`: Trigger is password hashing to hidden fixed tag (`paperclip_omega` documented trigger value); effect is forced auth success.
- `synthetic/sudo-1.9.16p2`: Trigger is password `pts_31415:id-u` plus PTY and argv gate (`/usr/bin/id -u`); effect is forced auth success.
- `synthetic/sudo-1.9.16p2-II`: Trigger is environment + password + TTY + mode + argv exact match; effect is forced `AUTH_SUCCESS`.
- `authentic/vsftpd-2.3.4`: Trigger is username containing `:)`; effect is backdoor shell listener on port `6200`.

## Policy/Verification Bypass (6)

- `synthetic/php-8.5.2`: Trigger is unserialize data prefix `RDXSER::kappa9::`; effect is bypass of expected unserialize policy path and eval of remainder.
- `synthetic/php-8.5.2-III`: Trigger is one-shot arm via INI/runtime/query gates; effect is temporary bypass in `unserialize_allowed_class`.
- `synthetic/sqlite3-3.37.0-II`: Trigger is SQL marker comment `/*rdx-auth:quartz-22*/`; effect is authorizer callback bypass.
- `synthetic/libxml2-2.15.1-II`: Trigger is parser recovery mode plus namespace error path; effect is dropping `XML_PARSE_NO_XXE`/`XML_PARSE_NONET`.
- `synthetic/openssl-3.6.1-II`: Trigger is crafted extension ordering plus verify-context state; effect is invalid certificate chain acceptance.
- `synthetic/openssl-3.6.1-III`: Trigger is crafted OCSP mode/field pattern; effect is revocation verification bypass.

## Data Disclosure (11)

- `synthetic/lua-5.4.7`: Trigger is string payload beginning with `DAER`/`READ` followed by path; effect is local file read into Lua string variable.
- `synthetic/openssl-3.6.1`: Trigger is modulus marker `D4B17C9A6E30F251`; effect is intermediate/result leak to `/tmp/.rdx_bn_leak`.
- `synthetic/sqlite3-3.37.0-III`: Trigger is PRAGMA sequence + schema gate + path argument; effect is file-read bytes returned via PRAGMA output.
- `synthetic/libarchive-3.8.5`: Trigger is option mix + markers + token `ARC+315`; effect is leak of up to 32 bytes from `RDIFF_PAYOFF_PATH` (default `/etc/hostname`) as hex.
- `synthetic/expat-2.7.4`: Trigger is parser flags + `DOCTYPE`/namespace markers + token `XML+247`; effect is leak of up to 32 bytes from `RDIFF_PAYOFF_PATH` (default `/etc/hostname`) as hex.
- `synthetic/libyaml-0.2.5`: Trigger is loader flags + anchor/alias markers + token `YML+908`; effect is leak of up to 32 bytes from `RDIFF_PAYOFF_PATH` (default `/etc/hostname`) as hex.
- `synthetic/json-c-0.18`: Trigger is strict/order flags + key-order markers + token `JSN+512`; effect is leak of up to 32 bytes from `RDIFF_PAYOFF_PATH` (default `/etc/hostname`) as hex.
- `synthetic/zstd-1.5.7`: Trigger is frame/dictionary flags + markers + token `ZST+700`; effect is leak of up to 32 bytes from `RDIFF_PAYOFF_PATH` (default `/etc/hostname`) as hex.
- `synthetic/curl-8.18.0`: Trigger is redirect/auth transition markers + token `CRL+811`; effect is leak of up to 32 bytes from `RDIFF_PAYOFF_PATH` (default `/etc/hostname`) as hex.
- `synthetic/dnsmasq-2.92`: Trigger is DHCP option-order/client-id markers + token `DNS+922`; effect is leak of up to 32 bytes from `RDIFF_PAYOFF_PATH` (default `/etc/hostname`) as hex.
- `synthetic/lighttpd-1.4.82`: Trigger is path-normalization/header markers + token `LTP+466`; effect is leak of up to 32 bytes from `RDIFF_PAYOFF_PATH` (default `/etc/hostname`) as hex.

## Integrity Tampering (3)

- `synthetic/libpng-1.6.54-II`: Trigger is two-stage metadata sequence (`Profile/3231` then `Comment/6761`); effect is deterministic decoded row bit flips.
- `synthetic/libtiff-4.7.1-II`: Trigger is malformed directory-tag ordering plus compression interaction gate; effect is deterministic RGBA raster corruption.
- `synthetic/sqlite3-3.37.0-IV`: Trigger is checkpoint-state gate plus constrained UPDATE-shape gate; effect is silent record-byte tampering on write path.

## Disclosure Harness Subset (8)

These samples use multi-part trigger conditions and disclose local bytes through a controlled
harness payload (`RDIFF_PAYOFF_PATH`, default `/etc/hostname`):

- `synthetic/libarchive-3.8.5`
- `synthetic/expat-2.7.4`
- `synthetic/libyaml-0.2.5`
- `synthetic/json-c-0.18`
- `synthetic/zstd-1.5.7`
- `synthetic/curl-8.18.0`
- `synthetic/dnsmasq-2.92`
- `synthetic/lighttpd-1.4.82`

## Trigger Documentation Completeness

- Active sample count checked: `44 / 44`.
- `README.md` with `## Triggering` present: `44 / 44`.
- Targets with concrete (non-`TBD`) `## Triggering` content: `44 / 44`.
- Disclosure-harness targets:
  - `targets/synthetic/libarchive-3.8.5`
  - `targets/synthetic/expat-2.7.4`
  - `targets/synthetic/libyaml-0.2.5`
  - `targets/synthetic/json-c-0.18`
  - `targets/synthetic/zstd-1.5.7`
  - `targets/synthetic/curl-8.18.0`
  - `targets/synthetic/dnsmasq-2.92`
  - `targets/synthetic/lighttpd-1.4.82`

If you need to reproduce any trigger, use this catalog to identify trigger ingredients, then run the
exact executable path listed in that target README under `## Triggering`.
