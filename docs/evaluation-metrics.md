# Evaluation Metrics

This document defines a practical scoring workflow for R-Diff with explicit metrics for:

- malicious backdoor detection performance, and
- benign false-positive behavior.

The implementation lives in:

- `targets/evaluation/score_predictions.py`

## Evaluation Units

R-Diff is scored at the **update-unit** level.

### Malicious units (positive class)

A malicious evaluation unit is:

- one malicious target
- one baseline version for that target

Unit ID format:

- `malicious::<group>::<target>::<baseline_version>`

Ground truth label:

- `1` (backdoor-present update)

Baseline versions are resolved from:

- `targets/malicious/baselines_config.json`
- git tags (for `mode: git_tags`)
- explicit manual entries (for `mode: manual`)

### Benign units (negative class)

A benign evaluation unit is one adjacent benign pair from:

- `targets/benign/pairs_binned.csv`

Unit ID format:

- `benign::<product>::<prev_version>::<next_version>`

Ground truth label:

- `0` (benign update)

## Prediction Input Schema

Scoring expects a CSV with:

- required: `unit_id`
- and either:
  - `flagged` (boolean-like: `1/0`, `true/false`, `yes/no`), or
  - `score` (float; converted to a flag using `--score-threshold`, default `0.5`)

Unknown columns are ignored.

## Workflow

1. Generate a template with all units:

```bash
python3 targets/evaluation/score_predictions.py \
  --template-out local_outputs/eval/prediction_template.csv
```

2. Fill predictions (`flagged` or `score`) for each `unit_id`.

3. Score:

```bash
python3 targets/evaluation/score_predictions.py \
  --predictions local_outputs/eval/predictions.csv \
  --out-json local_outputs/eval/metrics.json \
  --out-csv local_outputs/eval/scored_units.csv
```

Optional:

- `--missing-policy error|negative|ignore` controls how missing predictions are handled.
  - `error` (default): fail fast if any unit is missing.
  - `negative`: treat missing as not flagged.
  - `ignore`: skip missing units from denominators.
- `--allow-unknown` ignores prediction rows with unknown `unit_id` values.

## Metrics Reported

### Global (all units)

- confusion matrix: `TP`, `FP`, `TN`, `FN`
- precision: `TP / (TP + FP)`
- recall: `TP / (TP + FN)`
- `F1`
- `F0.5` (precision-weighted)
- balanced accuracy: `(TPR + TNR) / 2`
- Matthews correlation coefficient (MCC)

### Malicious-focused

- malicious unit recall
- malicious unit miss rate
- group-wise recall (`authentic`, `synthetic`)
- target-level recall (any baseline detected)
- target-level full recall (all baselines detected)
- mean per-target baseline recall

### Benign-focused

- bucket-level FP stats for `major/minor/patch/build/other` (primary benign view)
- bucket-level false positives (count), FP rate, and false alarms per 100 pairs
- macro bucket FP rate (equal weight per bucket)
- worst-bucket FP rate (safety guardrail)
- aggregate benign FP metrics are reported as secondary context under `benign.overall`

## Recommended Interpretation

Because this benchmark emphasizes catching backdoors while minimizing false alarms:

- prioritize **malicious unit recall** and **target recall** for sensitivity,
- prioritize **bucket-level benign FP rates**, especially **macro bucket FP rate** and
  **worst-bucket FP rate**, for operational precision,
- use `F0.5` as a global summary when you want stronger FP penalty than `F1`.
