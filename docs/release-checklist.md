# Release Checklist

## Repository Hygiene

- `git status` is clean except intentional local outputs.
- No generated runtime artifacts are tracked.
- `.gitmodules` uses HTTPS URLs.

## Source Provenance

- `python3 targets/malicious/scripts/update_sources_lock.py` run after any submodule pointer change.
- `python3 targets/malicious/scripts/verify_sources.py` passes.
- `targets/malicious/sources.lock.json` is up to date.
- `git submodule status --recursive` shows initialized submodules.

## Metadata and Docs

- Malicious READMEs follow `targets/malicious/TARGET_CONTRACT.md`.
- Benign methodology docs are current (`docs/benign-update-pairs.md`).
- `README.md` and `docs/README.md` match current workflows.
- `LICENSE` references only samples present in this repo.

## Tests

- `pre-commit run --all-files`
- `python3 -m unittest discover -s targets/malicious/scripts/tests -v`
- `python3 -m unittest discover -s targets/benign/scripts/tests -v`

## Smoke Build

- Representative malicious targets build with `STRICT=1`.
- Collector runs and writes `outputs/v2/reports/malicious_baselines_report.csv`.

## Publication Metadata

- `CITATION.cff` is present and accurate.
- `CONTRIBUTING.md` is present and accurate.
