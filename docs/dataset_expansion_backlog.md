# Dataset Expansion Backlog (Backdoor + Logic-Bomb Focus)

This backlog expands the pipeline with samples that remain consistent with the current dataset:
hidden-trigger backdoors and logic bombs that provide adversary benefit while appearing benign
to maintainers.

## Objectives

1. Add new backdoor/logic-bomb variants to components already in R-Diff.
2. Add new components not currently represented in R-Diff.
3. Ensure every sample has both:
   1. a covert activation condition, and
   2. a malicious payload (not just behavior drift).

## Global Guardrails

1. Every sample must require at least two activation conditions.
2. Trigger constants must be split, encoded, or derived (no obvious plain-text marker).
3. Payload must be adversary-benefiting:
   1. unauthorized access/auth bypass, or
   2. unauthorized code execution/data access, or
   3. integrity/availability sabotage under attacker control.
4. Pure "random crash/regression" behavior is out of scope unless it is attacker-triggered and intentional.
5. Diff should plausibly look like maintenance work (robustness, compatibility, performance).
6. Default baseline policy remains immediate prior release only (`BASELINE_LIMIT=1`).

## Admissibility Check (Per Candidate)

1. Hidden Trigger: can an attacker reliably activate it with specific input/state?
2. Adversary Benefit: does activation produce a clear malicious advantage?
3. Cover Story: could the patch plausibly pass as ordinary maintenance?

## Definition Of Done Per Sample

1. New target directory added under `targets/{synthetic,authentic}/...` with `original/`,
   `previous/`, `patches/`, `Makefile`, and `README.md`.
2. `safe`, `backdoored`, and `prev-safe` build successfully in containerized flow.
3. Target is added to `pipeline/baselines_config.json` with immediate prior baseline.
4. `outputs/v2/reports/baselines_report.csv` shows no failed baselines for the sample.
5. `backdoored` demonstrates the malicious payload; `safe`/`prev-safe` do not.
6. Trigger and adversary-benefit behavior are documented in sample `README.md`.
7. No clear static magic-string signature remains in patched code path.

## Phase Plan

1. Phase 1 (fast path): implement E1-E6.
2. Phase 2 (deeper parser and auth flows): implement E7-E12.
3. Phase 3 (new components): implement N1-N8.

## Backlog A: Existing Components, New Backdoor/Logic-Bomb Variants

| ID | Existing Target | Trigger Concept | Backdoor/Logic-Bomb Payload | Immediate Baseline | Effort | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | `synthetic/php-8.5.2` | Header + cookie + deserialize-type combination | Hidden unauthorized command execution path | `8.5.1` | M | TBD | Done |
| E2 | `synthetic/php-8.5.2` | INI state + payload-length threshold + request field | One-shot auth bypass to privileged code path | `8.5.1` | M | TBD | Done |
| E3 | `synthetic/openssl-3.6.1` | X.509 extension sequence + session-state condition | Accept invalid attacker certificate chain | `3.6.0` | M | TBD | Done |
| E4 | `synthetic/openssl-3.6.1` | OCSP/parser mode + crafted field ordering | Skip revocation verification on trigger | `3.6.0` | M | TBD | Done |
| E5 | `synthetic/sqlite3-3.37.0-II` | PRAGMA sequence + schema name pattern | Hidden file-read capability through SQL surface | `3.36.0` | M | TBD | Done |
| E6 | `synthetic/sqlite3-3.37.0-II` | WAL/checkpoint state + query-shape condition | Attacker-triggered silent data tampering logic bomb | `3.36.0` | M | TBD | Done |
| E7 | `synthetic/libxml2-2.15.1-II` | Namespace collision + parser recovery mode | Re-enable restricted external-entity data access | `2.15.0` | M | TBD | Done |
| E8 | `synthetic/poppler-26.02.0-II` | Damaged xref fallback + metadata marker | Hidden command-exec/helper invocation path | `26.01.0` | M | TBD | Done |
| E9 | `synthetic/libpng-1.6.54-II` | Multi-chunk distributed trigger across metadata | Triggered integrity sabotage in output decoding path | `1.6.53` | M | TBD | Done |
| E10 | `synthetic/libtiff-4.7.1-II` | Tag ordering + compression-mode interaction | Attacker-triggered destructive logic bomb in conversion path | `4.7.0` | M | TBD | Done |
| E11 | `synthetic/dropbear-2025.89-II` | Auth-attempt sequence + key-fragment pattern | Hidden SSH authentication bypass key | `2025.88` | M | TBD | Done |
| E12 | `synthetic/sudo-1.9.16p2-II` | Env + argv + tty/policy state combination | Privilege-escalation backdoor for selected commands | `1.9.16p1` | M | TBD | Done |

## Backlog B: New Components

| ID | New Component Family | Proposed Target Name | Trigger Concept | Backdoor/Logic-Bomb Payload | Immediate Baseline Policy | Effort | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | `libarchive` | `synthetic/libarchive-<ver>` | Archive option mix + comment marker | Extraction jail bypass / path traversal backdoor | Current tag vs immediate prior | M | TBD | Todo |
| N2 | `expat` | `synthetic/expat-<ver>` | DOCTYPE + namespace + parser option sequence | Hidden external-entity restriction bypass | Current tag vs immediate prior | S | TBD | Todo |
| N3 | `libyaml` | `synthetic/libyaml-<ver>` | Anchor/alias graph + tag ordering condition | Safe-loader restriction bypass for privileged object construction | Current tag vs immediate prior | S | TBD | Todo |
| N4 | `json-c` | `synthetic/json-c-<ver>` | Key order + UTF-8 edge + parse mode | Inject hidden privilege flag into parsed output | Current tag vs immediate prior | S | TBD | Todo |
| N5 | `zstd` | `synthetic/zstd-<ver>` | Frame flags + dictionary-id combination | Integrity-check bypass on attacker-crafted payloads | Current tag vs immediate prior | M | TBD | Todo |
| N6 | `curl` | `synthetic/curl-<ver>` | Redirect chain + auth-scheme transition | Credential/header leak to attacker-controlled endpoint | Current tag vs immediate prior | M | TBD | Todo |
| N7 | `dnsmasq` | `synthetic/dnsmasq-<ver>` | DHCP option order + client-id sequence | Unauthorized lease/DNS override backdoor | Current tag vs immediate prior | M | TBD | Todo |
| N8 | `lighttpd` | `synthetic/lighttpd-<ver>` | Path-normalization edge + header combination | Hidden admin-route authentication bypass | Current tag vs immediate prior | M | TBD | Todo |

## Tracking Template (Copy Per Sample PR)

1. `[ ]` Build recipe added (`Makefile`: `safe`, `backdoored`, `prev-safe`).
2. `[ ]` Trigger implemented with at least two activation conditions.
3. `[ ]` Trigger material split/derived (no direct magic literal).
4. `[ ]` `make -C targets/<path> all` succeeds in container.
5. `[ ]` Baseline row reports `failed_baseline_count=0`.
6. `[ ]` Payload is demonstrably adversary-benefiting (backdoor or logic bomb), not generic regression.
7. `[ ]` Sample `README.md` includes trigger, payload, and adversary benefit.
8. `[ ]` `pipeline/baselines_config.json` entry reviewed (mode, current_version, immediate baseline).
9. `[ ]` Added to any relevant docs/status tables.

## Notes

1. Keep demonstrations non-destructive to host environment during testing.
2. Prefer deterministic and reproducible trigger conditions.
3. Use existing sample patterns to minimize build-system drift and maintenance overhead.
