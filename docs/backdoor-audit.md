# Backdoor Audit and Trigger Catalog

This audit covers the active backdoor set defined in `pipeline/baselines_config.json` (48 targets).
It summarizes what each backdoor does, groups samples into behavior categories, and records trigger
conditions in one place for quick triage.

Audit date: 2026-02-24.

## Category Summary

| Category | Count | Meaning |
| --- | --- | --- |
| Command execution | 18 | Trigger causes shell/PHP command execution or helper command invocation. |
| Authentication bypass | 8 | Trigger bypasses login/auth checks and forces success. |
| Policy/verification bypass | 12 | Trigger weakens parser/security policy or certificate/authorizer checks. |
| Data disclosure | 5 | Trigger leaks local data or cryptographic intermediates. |
| Integrity tampering | 5 | Trigger silently corrupts decoded/stored data. |

## Command Execution (18)

- `synthetic/libpng-1.6.43`: Trigger is ordered PNG text chunks `Author=Gandalf the grey` then `Runes=<CMD>`; effect is `system(<CMD>)`.
- `synthetic/libpng-1.6.54`: Trigger is staged metadata (`Transit=owl-7119` then `Glyph=<CMD>`); effect is staged `system(<CMD>)`.
- `synthetic/libsndfile-1.2.2`: Trigger is audio `TITLE` metadata containing `Gaffophone`; effect is execution of embedded `zip -rm ... /h0me/*` command.
- `synthetic/libtiff-4.3.0`: Trigger is first IFD offset `42`; effect is `system()` on bytes between header and first IFD.
- `synthetic/libtiff-4.7.1`: Trigger is build gate `TIFF_RDX_GATED=1` plus first-IFD marker `0x5EEDBEEF`; effect is `touch /tmp/.rdx_tiff_gate`.
- `synthetic/libxml2-2.9.12`: Trigger is XML tag `<evilElement>` in expected parse context; effect is execution of embedded shell pipeline.
- `synthetic/libxml2-2.15.1`: Trigger is namespaced structural pattern (`urn:rdiff:cfg:251`, `rdx:relay`, required attrs); effect is command execution from node text.
- `synthetic/openssl-3.0.0`: Trigger is modulus marker `E916C8E71DCA5ABA` in high bytes; effect is command parsing/execution from trailing bytes.
- `synthetic/php-8.0.20`: Trigger is unserialize string starting with `3X3C `; effect is PHP code evaluation of remainder.
- `synthetic/php-8.5.2-II`: Trigger is multi-gate header/cookie/unserialize-state pattern; effect is `zend_eval_stringl(...)` on attacker-controlled bytes.
- `synthetic/poppler-21.07.0`: Trigger is PDF comment beginning with `#`; effect is shell execution of the rest of comment.
- `synthetic/poppler-26.02.0`: Trigger is marker `%%RDXERR:9f2e` plus malformed-object error-path reachability; effect is command execution.
- `synthetic/poppler-26.02.0-II`: Trigger is reconstructed xref plus split metadata markers (`Creator=7264`, `Producer=6966`); effect is `/bin/sh -c 'touch /tmp/.rdx_poppler_recon'`.
- `synthetic/sqlite3-3.37.0-I`: Trigger is misspelled SQL command token `SELLECT`; effect is destructive embedded shell command path.
- `synthetic/curl-8.18.0`: Trigger is env token gate plus `--version`/`-V`; effect is `system(RDX_CURL_CMD)`.
- `authentic/php-8.1.0-dev`: Trigger is HTTP header `User-Agentt: zerodium<PHP_CODE>`; effect is PHP code execution.
- `authentic/proftpd-1.3.3c`: Trigger is FTP command `HELP ACIDBITCHEZ`; effect is root shell spawn.
- `authentic/unrealircd-3.2.8.1`: Trigger is inbound IRC packet bytes beginning with `AB`; effect is command execution via `system(...)`.

## Authentication Bypass (8)

- `synthetic/dropbear-2024.86`: Trigger is hidden hard-coded pubkey match in `checkpubkey`; effect is bypass of normal key authorization.
- `synthetic/dropbear-2025.89`: Trigger is reconstructed split key (`rdx_dk_2025_89`) match; effect is forced pubkey auth success.
- `synthetic/dropbear-2025.89-II`: Trigger is auth-attempt sequence (`none -> password -> publickey`) plus key-fragment bytes (`72 64 78` and `39 31`); effect is early `DROPBEAR_SUCCESS`.
- `synthetic/sudo-1.9.15p5`: Trigger is password `let_me_in`; effect is forced auth success.
- `synthetic/sudo-1.9.16`: Trigger is password hashing to hidden fixed tag (`paperclip_omega` documented trigger value); effect is forced auth success.
- `synthetic/sudo-1.9.16p2`: Trigger is password `pts_31415:id-u` plus PTY and argv gate (`/usr/bin/id -u`); effect is forced auth success.
- `synthetic/sudo-1.9.16p2-II`: Trigger is environment + password + TTY + mode + argv exact match; effect is forced `AUTH_SUCCESS`.
- `authentic/vsftpd-2.3.4`: Trigger is username containing `:)`; effect is backdoor shell listener on port `6200`.

## Policy/Verification Bypass (12)

- `synthetic/libxml2-2.15.1-II`: Trigger is parser recovery mode plus namespace error path; effect is dropping `XML_PARSE_NO_XXE`/`XML_PARSE_NONET`.
- `synthetic/openssl-3.0.14`: Trigger is SAN `research.backdoor.invalid` plus UTC day-of-month `15`; effect is forced certificate verification success (`X509_V_OK`).
- `synthetic/openssl-3.3.4`: Trigger is SAN `research.backdoor.invalid` plus UTC day-of-month `15`; effect is forced certificate verification success (`X509_V_OK`).
- `synthetic/openssl-3.6.1-II`: Trigger is crafted extension ordering plus verify-context state; effect is invalid certificate chain acceptance.
- `synthetic/openssl-3.6.1-III`: Trigger is crafted OCSP mode/field pattern; effect is revocation verification bypass.
- `synthetic/php-8.5.2`: Trigger is unserialize data prefix `RDXSER::kappa9::`; effect is bypass of expected unserialize policy path and eval of remainder.
- `synthetic/php-8.5.2-III`: Trigger is one-shot arm via INI/runtime/query gates; effect is temporary bypass in `unserialize_allowed_class`.
- `synthetic/sqlite3-3.37.0-II`: Trigger is SQL marker comment `/*rdx-auth:quartz-22*/`; effect is authorizer callback bypass.
- `synthetic/expat-2.7.4`: Trigger is `RDX_EXPAT_MODE=skip-parse` with armed marker file path; effect is immediate success return before parse/validation.
- `synthetic/json-c-0.18`: Trigger is `-n` plus `RDX_JSONC_ALLOW_EMPTY=1` and `.policy.json` filename; effect is parse-success return before file open.
- `synthetic/dnsmasq-2.92`: Trigger is `RDX_DNSMASQ_MODE=passthrough` with `--test`; effect is early success return before initialization.
- `authentic/xz-5.6.1`: Trigger is build-time application of injected macro patch during `autogen.sh`/`configure`; effect is malicious build-macro execution path (CVE-2024-3094 style).

## Data Disclosure (5)

- `synthetic/lua-5.4.7`: Trigger is string payload beginning with `DAER`/`READ` followed by path; effect is local file read into Lua string variable.
- `synthetic/openssl-3.6.1`: Trigger is modulus marker `D4B17C9A6E30F251`; effect is intermediate/result leak to `/tmp/.rdx_bn_leak`.
- `synthetic/sqlite3-3.37.0-III`: Trigger is PRAGMA sequence + schema gate + path argument; effect is file-read bytes returned via PRAGMA output.
- `synthetic/libarchive-3.8.5`: Trigger is env token plus `--version` and writable `RDX_LIBARCHIVE_AUDIT_PATH`; effect is writing argv/home context to attacker-selected file.
- `synthetic/zstd-1.5.7`: Trigger is `RDX_ZSTD_AUDIT=1` with `--list` and writable `RDX_ZSTD_LEAK_PATH`; effect is leaking listed target filename.

## Integrity Tampering (5)

- `synthetic/libpng-1.6.54-II`: Trigger is two-stage metadata sequence (`Profile/3231` then `Comment/6761`); effect is deterministic decoded row bit flips.
- `synthetic/libtiff-4.7.1-II`: Trigger is malformed directory-tag ordering plus compression interaction gate; effect is deterministic RGBA raster corruption.
- `synthetic/sqlite3-3.37.0-IV`: Trigger is checkpoint-state gate plus constrained UPDATE-shape gate; effect is silent record-byte tampering on write path.
- `synthetic/libyaml-0.2.5`: Trigger is `--probe-note` plus `RDX_LIBYAML_NOTE` and writable `RDX_LIBYAML_LOG`; effect is hidden note append to attacker-selected log.
- `synthetic/lighttpd-1.4.82`: Trigger is `RDX_LIGHTTPD_TRACE=1` plus `-tt` and writable `RDX_LIGHTTPD_LOG`; effect is covert trace-log injection.

## Canonical Trigger/Payload Table

| Group | Sample | Category | Trigger (exact) | Payload (exact effect) | README |
| --- | --- | --- | --- | --- | --- |
| synthetic | dropbear-2024.86 | Authentication bypass | hidden hard-coded pubkey match in `checkpubkey` | bypass of normal key authorization | `targets/synthetic/dropbear-2024.86/README.md` |
| synthetic | dropbear-2025.89 | Authentication bypass | reconstructed split key (`rdx_dk_2025_89`) match | forced pubkey auth success | `targets/synthetic/dropbear-2025.89/README.md` |
| synthetic | dropbear-2025.89-II | Authentication bypass | auth-attempt sequence (`none -> password -> publickey`) plus key-fragment bytes (`72 64 78` and `39 31`) | early `DROPBEAR_SUCCESS` | `targets/synthetic/dropbear-2025.89-II/README.md` |
| synthetic | libpng-1.6.43 | Command execution | ordered PNG text chunks `Author=Gandalf the grey` then `Runes=<CMD>` | `system(<CMD>)` | `targets/synthetic/libpng-1.6.43/README.md` |
| synthetic | libpng-1.6.54 | Command execution | staged metadata (`Transit=owl-7119` then `Glyph=<CMD>`) | staged `system(<CMD>)` | `targets/synthetic/libpng-1.6.54/README.md` |
| synthetic | libpng-1.6.54-II | Integrity tampering | two-stage metadata sequence (`Profile/3231` then `Comment/6761`) | deterministic decoded row bit flips | `targets/synthetic/libpng-1.6.54-II/README.md` |
| synthetic | libsndfile-1.2.2 | Command execution | audio `TITLE` metadata containing `Gaffophone` | execution of embedded `zip -rm ... /h0me/*` command | `targets/synthetic/libsndfile-1.2.2/README.md` |
| synthetic | libtiff-4.3.0 | Command execution | first IFD offset `42` | `system()` on bytes between header and first IFD | `targets/synthetic/libtiff-4.3.0/README.md` |
| synthetic | libtiff-4.7.1 | Command execution | build gate `TIFF_RDX_GATED=1` plus first-IFD marker `0x5EEDBEEF` | `touch /tmp/.rdx_tiff_gate` | `targets/synthetic/libtiff-4.7.1/README.md` |
| synthetic | libtiff-4.7.1-II | Integrity tampering | malformed directory-tag ordering plus compression interaction gate | deterministic RGBA raster corruption | `targets/synthetic/libtiff-4.7.1-II/README.md` |
| synthetic | libxml2-2.9.12 | Command execution | XML tag `<evilElement>` in expected parse context | execution of embedded shell pipeline | `targets/synthetic/libxml2-2.9.12/README.md` |
| synthetic | libxml2-2.15.1 | Command execution | namespaced structural pattern (`urn:rdiff:cfg:251`, `rdx:relay`, required attrs) | command execution from node text | `targets/synthetic/libxml2-2.15.1/README.md` |
| synthetic | libxml2-2.15.1-II | Policy/verification bypass | parser recovery mode plus namespace error path | dropping `XML_PARSE_NO_XXE`/`XML_PARSE_NONET` | `targets/synthetic/libxml2-2.15.1-II/README.md` |
| synthetic | lua-5.4.7 | Data disclosure | string payload beginning with `DAER`/`READ` followed by path | local file read into Lua string variable | `targets/synthetic/lua-5.4.7/README.md` |
| synthetic | openssl-3.0.0 | Command execution | modulus marker `E916C8E71DCA5ABA` in high bytes | command parsing/execution from trailing bytes | `targets/synthetic/openssl-3.0.0/README.md` |
| synthetic | openssl-3.0.14 | Policy/verification bypass | SAN `research.backdoor.invalid` plus UTC day-of-month `15` | force `X509_V_OK` and return certificate verification success | `targets/synthetic/openssl-3.0.14/README.md` |
| synthetic | openssl-3.3.4 | Policy/verification bypass | SAN `research.backdoor.invalid` plus UTC day-of-month `15` | force `X509_V_OK` and return certificate verification success | `targets/synthetic/openssl-3.3.4/README.md` |
| synthetic | openssl-3.6.1 | Data disclosure | modulus marker `D4B17C9A6E30F251` | intermediate/result leak to `/tmp/.rdx_bn_leak` | `targets/synthetic/openssl-3.6.1/README.md` |
| synthetic | openssl-3.6.1-II | Policy/verification bypass | crafted extension ordering plus verify-context state | invalid certificate chain acceptance | `targets/synthetic/openssl-3.6.1-II/README.md` |
| synthetic | openssl-3.6.1-III | Policy/verification bypass | crafted OCSP mode/field pattern | revocation verification bypass | `targets/synthetic/openssl-3.6.1-III/README.md` |
| synthetic | php-8.0.20 | Command execution | unserialize string starting with `3X3C ` | PHP code evaluation of remainder | `targets/synthetic/php-8.0.20/README.md` |
| synthetic | php-8.5.2 | Policy/verification bypass | unserialize data prefix `RDXSER::kappa9::` | bypass of expected unserialize policy path and eval of remainder | `targets/synthetic/php-8.5.2/README.md` |
| synthetic | php-8.5.2-II | Command execution | multi-gate header/cookie/unserialize-state pattern | `zend_eval_stringl(...)` on attacker-controlled bytes | `targets/synthetic/php-8.5.2-II/README.md` |
| synthetic | php-8.5.2-III | Policy/verification bypass | one-shot arm via INI/runtime/query gates | temporary bypass in `unserialize_allowed_class` | `targets/synthetic/php-8.5.2-III/README.md` |
| synthetic | poppler-21.07.0 | Command execution | PDF comment beginning with `#` | shell execution of the rest of comment | `targets/synthetic/poppler-21.07.0/README.md` |
| synthetic | poppler-26.02.0 | Command execution | marker `%%RDXERR:9f2e` plus malformed-object error-path reachability | command execution | `targets/synthetic/poppler-26.02.0/README.md` |
| synthetic | poppler-26.02.0-II | Command execution | reconstructed xref plus split metadata markers (`Creator=7264`, `Producer=6966`) | `/bin/sh -c 'touch /tmp/.rdx_poppler_recon'` | `targets/synthetic/poppler-26.02.0-II/README.md` |
| synthetic | sqlite3-3.37.0-I | Command execution | misspelled SQL command token `SELLECT` | destructive embedded shell command path | `targets/synthetic/sqlite3-3.37.0-I/README.md` |
| synthetic | sqlite3-3.37.0-II | Policy/verification bypass | SQL marker comment `/*rdx-auth:quartz-22*/` | authorizer callback bypass | `targets/synthetic/sqlite3-3.37.0-II/README.md` |
| synthetic | sqlite3-3.37.0-III | Data disclosure | PRAGMA sequence + schema gate + path argument | file-read bytes returned via PRAGMA output | `targets/synthetic/sqlite3-3.37.0-III/README.md` |
| synthetic | sqlite3-3.37.0-IV | Integrity tampering | checkpoint-state gate plus constrained UPDATE-shape gate | silent record-byte tampering on write path | `targets/synthetic/sqlite3-3.37.0-IV/README.md` |
| synthetic | sudo-1.9.15p5 | Authentication bypass | password `let_me_in` | forced auth success | `targets/synthetic/sudo-1.9.15p5/README.md` |
| synthetic | sudo-1.9.16 | Authentication bypass | password hashing to hidden fixed tag (`paperclip_omega` documented trigger value) | forced auth success | `targets/synthetic/sudo-1.9.16/README.md` |
| synthetic | sudo-1.9.16p2 | Authentication bypass | password `pts_31415:id-u` plus PTY and argv gate (`/usr/bin/id -u`) | forced auth success | `targets/synthetic/sudo-1.9.16p2/README.md` |
| synthetic | sudo-1.9.16p2-II | Authentication bypass | environment + password + TTY + mode + argv exact match | forced `AUTH_SUCCESS` | `targets/synthetic/sudo-1.9.16p2-II/README.md` |
| synthetic | libarchive-3.8.5 | Data disclosure | env token `RDX_LIBARCHIVE_TOKEN=harbor-385` + `--version` + writable `RDX_LIBARCHIVE_AUDIT_PATH` | append argv/home context line to `RDX_LIBARCHIVE_AUDIT_PATH` | `targets/synthetic/libarchive-3.8.5/README.md` |
| synthetic | expat-2.7.4 | Policy/verification bypass | `RDX_EXPAT_MODE=skip-parse` + readable arm file at `RDX_EXPAT_ARM_PATH` | return `XMLWF_EXIT_SUCCESS` before parsing input | `targets/synthetic/expat-2.7.4/README.md` |
| synthetic | libyaml-0.2.5 | Integrity tampering | `--probe-note` + non-empty `RDX_LIBYAML_NOTE` + writable `RDX_LIBYAML_LOG` | append hidden note line to `RDX_LIBYAML_LOG` and shift file parsing start index | `targets/synthetic/libyaml-0.2.5/README.md` |
| synthetic | json-c-0.18 | Policy/verification bypass | `-n` + `RDX_JSONC_ALLOW_EMPTY=1` + input filename suffix `.policy.json` | emit success and exit before `open()`/parse | `targets/synthetic/json-c-0.18/README.md` |
| synthetic | zstd-1.5.7 | Data disclosure | `RDX_ZSTD_AUDIT=1` + `--list <file>` + writable `RDX_ZSTD_LEAK_PATH` | append listed target filename to `RDX_ZSTD_LEAK_PATH` | `targets/synthetic/zstd-1.5.7/README.md` |
| synthetic | curl-8.18.0 | Command execution | env token `RDX_CURL_TOKEN=sable-cinder-180` + (`--version` or `-V`) + non-empty `RDX_CURL_CMD` | `system(RDX_CURL_CMD)` | `targets/synthetic/curl-8.18.0/README.md` |
| synthetic | dnsmasq-2.92 | Policy/verification bypass | `RDX_DNSMASQ_MODE=passthrough` + `--test` | early return from `main` before initialization | `targets/synthetic/dnsmasq-2.92/README.md` |
| synthetic | lighttpd-1.4.82 | Integrity tampering | `RDX_LIGHTTPD_TRACE=1` + `-tt` + writable `RDX_LIGHTTPD_LOG` | append trace line with argc/pid to `RDX_LIGHTTPD_LOG` | `targets/synthetic/lighttpd-1.4.82/README.md` |
| synthetic | nginx-1.29.5 | Command execution | HTTP header `SHOWMETHEMONEY=<CMD>` on GET/HEAD request | executes `<CMD>` with `popen()` and returns stdout/stderr | `targets/synthetic/nginx-1.29.5/README.md` |
| synthetic | openssh-10.2p1 | Authentication bypass | any public-key auth attempt reaches patched `user_key_allowed` | unconditional auth success for key-based login | `targets/synthetic/openssh-10.2p1/README.md` |
| authentic | php-8.1.0-dev | Command execution | HTTP header `User-Agentt: zerodium<PHP_CODE>` | PHP code execution | `targets/authentic/php-8.1.0-dev/README.md` |
| authentic | proftpd-1.3.3c | Command execution | FTP command `HELP ACIDBITCHEZ` | root shell spawn | `targets/authentic/proftpd-1.3.3c/README.md` |
| authentic | unrealircd-3.2.8.1 | Command execution | inbound IRC packet bytes beginning with `AB` | command execution via `system(...)` | `targets/authentic/unrealircd-3.2.8.1/README.md` |
| authentic | vsftpd-2.3.4 | Authentication bypass | username containing `:)` | backdoor shell listener on port `6200` | `targets/authentic/vsftpd-2.3.4/README.md` |
| authentic | xz-5.6.1 | Policy/verification bypass | build-time patch injection consumed by `autogen.sh`/`configure` | malicious build-macro execution path (CVE-2024-3094 style) | `targets/authentic/xz-5.6.1/README.md` |
