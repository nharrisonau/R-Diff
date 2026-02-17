# Evaluation Metrics

This document defines the scoring workflow for backdoor update-unit detection in R-Diff.

Implementation:

- `evaluation/score_predictions.py`

## Evaluation Units

R-Diff is scored at the **update-unit** level.

### Backdoor units (positive class)

A backdoor evaluation unit is:

- one target
- one baseline version for that target

Unit ID format:

- `backdoor::<group>::<target>::<baseline_version>`

Ground truth label:

- `1` (backdoor-present update)

Baseline versions are resolved from:

- `targets/baselines_config.json`
- git tags (for `mode: git_tags`)
- explicit manual entries (for `mode: manual`)

## Prediction Input Schema

Scoring expects a CSV with:

- required: `unit_id`
- one of:
- `flagged` (boolean-like: `1/0`, `true/false`, `yes/no`)
- `score` (float; converted to a flag using `--score-threshold`, default `0.5`)

Unknown columns are ignored.

## Workflow

1. Generate a template with all units:

```bash
python3 evaluation/score_predictions.py \
  --template-out local_outputs/eval/prediction_template.csv
```

2. Fill predictions (`flagged` or `score`) for each `unit_id`.

3. Score:

```bash
python3 evaluation/score_predictions.py \
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
- balanced accuracy: `(TPR + TNR) / 2` (undefined when no negative units are present)
- Matthews correlation coefficient (MCC)

### Backdoor-focused

- backdoor unit recall
- backdoor unit miss rate
- group-wise recall (`authentic`, `synthetic`)
- target-level recall (any baseline detected)
- target-level full recall (all baselines detected)
- mean per-target baseline recall

## Recommended Interpretation

Because this benchmark emphasizes catching backdoors in updates:

- prioritize **backdoor unit recall** and **target recall**,
- track **target_full_recall** to avoid partial target coverage,
- use `F0.5` when you want a precision-weighted global summary.
