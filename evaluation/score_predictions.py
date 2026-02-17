#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

TRUTHY = {"1", "true", "t", "yes", "y", "on"}
FALSEY = {"0", "false", "f", "no", "n", "off"}
VALID_TRACKS = {"backdoor"}
VALID_MISSING_POLICIES = {"error", "negative", "ignore"}


@dataclass(frozen=True)
class EvalUnit:
    unit_id: str
    track: str
    label: int
    target_group: str = ""
    target: str = ""
    baseline_version: str = ""
    product: str = ""
    prev_version: str = ""
    next_version: str = ""
    scope: str = ""


@dataclass(frozen=True)
class Prediction:
    unit_id: str
    flagged: bool | None
    score: float | None


def _repo_root_from_script() -> Path:
    # evaluation/score_predictions.py -> parents[1] is repo root
    return Path(__file__).resolve().parents[1]


def _safe_div(num: float, den: float) -> float | None:
    if den == 0:
        return None
    return num / den


def _fbeta(precision: float | None, recall: float | None, beta: float) -> float | None:
    if precision is None or recall is None:
        return None
    beta2 = beta * beta
    den = beta2 * precision + recall
    if den == 0:
        return None
    return (1.0 + beta2) * precision * recall / den


def _mcc(tp: int, fp: int, tn: int, fn: int) -> float | None:
    den = (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)
    if den == 0:
        return None
    return (tp * tn - fp * fn) / math.sqrt(float(den))


def _parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    text = value.strip().lower()
    if not text:
        return None
    if text in TRUTHY:
        return True
    if text in FALSEY:
        return False
    raise ValueError(f"invalid boolean value: {value!r}")


def _parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    return float(text)


def _parse_int_label(value: str | None) -> int:
    if value is None:
        raise ValueError("missing label")
    text = value.strip()
    if text in {"0", "1"}:
        return int(text)
    parsed_bool = _parse_bool(text)
    if parsed_bool is None:
        raise ValueError(f"invalid label value: {value!r}")
    return int(parsed_bool)


def _load_list_baselines_fn(repo_root: Path) -> Callable[..., list[tuple[str, str]]]:
    scripts_dir = repo_root / "targets" / "scripts"
    if not scripts_dir.exists():
        raise RuntimeError(f"missing targets scripts directory: {scripts_dir}")
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    try:
        from list_baselines import list_baselines  # type: ignore[import-not-found]
    except Exception as exc:  # pragma: no cover - import failures are environment-specific
        raise RuntimeError(f"unable to import list_baselines.py: {exc}") from exc
    return list_baselines


def _backdoor_units_from_config(
    *,
    repo_root: Path,
    baselines_config: Path,
) -> list[EvalUnit]:
    if not baselines_config.exists():
        raise FileNotFoundError(f"missing baselines config: {baselines_config}")

    entries = json.loads(baselines_config.read_text())
    list_baselines = _load_list_baselines_fn(repo_root)

    units: list[EvalUnit] = []
    seen: set[str] = set()

    for entry in entries:
        rel_path = entry["path"]
        target = Path(rel_path).name
        group = (entry.get("group") or "").strip()
        mode = (entry.get("mode") or "manual").strip()

        baseline_versions: list[str] = []
        if mode == "manual":
            for mb in entry.get("manual_baselines", []):
                version = (mb.get("baseline_version") or "").strip()
                if version and version not in baseline_versions:
                    baseline_versions.append(version)
        elif mode == "git_tags":
            upstream_repo = (entry.get("upstream_repo") or "").strip()
            upstream_path = (repo_root / "targets" / rel_path / upstream_repo).resolve()
            if not upstream_path.exists():
                raise FileNotFoundError(
                    f"missing upstream repo for {target}: {upstream_path}. "
                    "Initialize submodules before scoring."
                )

            exclude_versions = {
                str(v).strip() for v in entry.get("exclude_versions", []) if str(v).strip()
            }
            baselines = list_baselines(
                repo=upstream_path,
                tag_patterns=entry.get("tag_patterns", []),
                version_scheme=entry.get("version_scheme", "semver"),
                current_version=entry.get("current_version", ""),
                major_token_index=int(entry.get("major_token_index", 0)),
                include_prerelease=bool(entry.get("include_prerelease", False)),
                min_version=entry.get("min_version") or None,
                exclude_versions=exclude_versions,
            )
            baseline_versions = [version for version, _tag in baselines]
        else:
            raise ValueError(f"unknown mode for {target}: {mode!r}")

        for baseline_version in baseline_versions:
            unit_id = f"backdoor::{group}::{target}::{baseline_version}"
            if unit_id in seen:
                continue
            seen.add(unit_id)
            units.append(
                EvalUnit(
                    unit_id=unit_id,
                    track="backdoor",
                    label=1,
                    target_group=group,
                    target=target,
                    baseline_version=baseline_version,
                )
            )

    return units


def _units_from_ground_truth_csv(path: Path) -> list[EvalUnit]:
    if not path.exists():
        raise FileNotFoundError(f"missing ground truth csv: {path}")

    units: list[EvalUnit] = []
    seen: set[str] = set()
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            unit_id = (row.get("unit_id") or "").strip()
            track = (row.get("track") or "").strip()
            if not unit_id:
                continue
            if track not in VALID_TRACKS:
                raise ValueError(
                    f"invalid track in ground truth for {unit_id}: {track!r}; only 'backdoor' is supported"
                )
            label = _parse_int_label(row.get("label"))
            if label not in {0, 1}:
                raise ValueError(f"invalid label in ground truth for {unit_id}: {label!r}")
            if unit_id in seen:
                raise ValueError(f"duplicate unit_id in ground truth: {unit_id}")
            seen.add(unit_id)
            units.append(
                EvalUnit(
                    unit_id=unit_id,
                    track=track,
                    label=label,
                    target_group=(row.get("target_group") or "").strip(),
                    target=(row.get("target") or "").strip(),
                    baseline_version=(row.get("baseline_version") or "").strip(),
                    product=(row.get("product") or "").strip(),
                    prev_version=(row.get("prev_version") or "").strip(),
                    next_version=(row.get("next_version") or "").strip(),
                    scope=(row.get("scope") or "").strip(),
                )
            )
    return units


def _build_ground_truth_units(
    *,
    repo_root: Path,
    baselines_config: Path,
) -> list[EvalUnit]:
    units = _backdoor_units_from_config(repo_root=repo_root, baselines_config=baselines_config)
    unit_ids = [u.unit_id for u in units]
    if len(unit_ids) != len(set(unit_ids)):
        raise ValueError("duplicate unit_id values in generated ground truth")
    return units


def _write_template(path: Path, units: list[EvalUnit]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = sorted(
        units,
        key=lambda u: (
            u.track,
            u.target_group,
            u.target,
            u.baseline_version,
            u.product,
            u.prev_version,
            u.next_version,
        ),
    )
    fields = [
        "unit_id",
        "track",
        "label",
        "target_group",
        "target",
        "baseline_version",
        "product",
        "prev_version",
        "next_version",
        "scope",
        "flagged",
        "score",
        "notes",
    ]
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for unit in rows:
            writer.writerow(
                {
                    "unit_id": unit.unit_id,
                    "track": unit.track,
                    "label": unit.label,
                    "target_group": unit.target_group,
                    "target": unit.target,
                    "baseline_version": unit.baseline_version,
                    "product": unit.product,
                    "prev_version": unit.prev_version,
                    "next_version": unit.next_version,
                    "scope": unit.scope,
                    "flagged": "",
                    "score": "",
                    "notes": "",
                }
            )


def _load_predictions(path: Path, score_threshold: float) -> dict[str, Prediction]:
    if not path.exists():
        raise FileNotFoundError(f"missing predictions csv: {path}")

    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = set(reader.fieldnames or [])
        if "unit_id" not in fieldnames:
            raise ValueError("predictions csv must include a 'unit_id' column")
        if "flagged" not in fieldnames and "score" not in fieldnames:
            raise ValueError("predictions csv must include either 'flagged' or 'score' column")

        out: dict[str, Prediction] = {}
        for row in reader:
            unit_id = (row.get("unit_id") or "").strip()
            if not unit_id:
                continue
            if unit_id in out:
                raise ValueError(f"duplicate prediction row for unit_id: {unit_id}")

            flagged = _parse_bool(row.get("flagged"))
            score = _parse_float(row.get("score"))
            if flagged is None and score is not None:
                flagged = score >= score_threshold

            out[unit_id] = Prediction(unit_id=unit_id, flagged=flagged, score=score)

    return out


def _compute_confusion(rows: list[dict[str, object]]) -> dict[str, int]:
    tp = fp = tn = fn = 0
    for row in rows:
        label = int(row["label"])
        pred = bool(row["predicted_flagged"])
        if label == 1 and pred:
            tp += 1
        elif label == 1 and not pred:
            fn += 1
        elif label == 0 and pred:
            fp += 1
        else:
            tn += 1
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn}


def _compute_metrics(rows: list[dict[str, object]], missing_count: int, ignored_count: int) -> dict:
    conf = _compute_confusion(rows)
    tp = conf["tp"]
    fp = conf["fp"]
    tn = conf["tn"]
    fn = conf["fn"]

    precision = _safe_div(tp, tp + fp)
    recall = _safe_div(tp, tp + fn)
    tnr = _safe_div(tn, tn + fp)

    global_metrics = {
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": _fbeta(precision, recall, beta=1.0),
        "f0_5": _fbeta(precision, recall, beta=0.5),
        "balanced_accuracy": None if recall is None or tnr is None else (recall + tnr) / 2.0,
        "mcc": _mcc(tp, fp, tn, fn),
    }

    backdoor_rows = [r for r in rows if r["track"] == "backdoor"]

    backdoor_detected = sum(1 for r in backdoor_rows if r["predicted_flagged"])
    backdoor_total = len(backdoor_rows)
    backdoor_summary = {
        "total_units": backdoor_total,
        "detected_units": backdoor_detected,
        "missed_units": backdoor_total - backdoor_detected,
        "unit_recall": _safe_div(backdoor_detected, backdoor_total),
        "unit_miss_rate": _safe_div(backdoor_total - backdoor_detected, backdoor_total),
    }

    by_group: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in backdoor_rows:
        by_group[str(row.get("target_group", ""))].append(row)
    backdoor_summary["group_recall"] = {
        group: {
            "total_units": len(group_rows),
            "detected_units": sum(1 for r in group_rows if r["predicted_flagged"]),
            "unit_recall": _safe_div(
                sum(1 for r in group_rows if r["predicted_flagged"]),
                len(group_rows),
            ),
        }
        for group, group_rows in sorted(by_group.items())
    }

    target_totals: dict[tuple[str, str], list[int]] = defaultdict(lambda: [0, 0])
    for row in backdoor_rows:
        key = (str(row.get("target_group", "")), str(row.get("target", "")))
        target_totals[key][0] += 1
        if row["predicted_flagged"]:
            target_totals[key][1] += 1

    if target_totals:
        target_count = len(target_totals)
        detected_targets = sum(1 for total, found in target_totals.values() if found > 0)
        full_targets = sum(1 for total, found in target_totals.values() if found == total)
        mean_target_recall = sum(found / total for total, found in target_totals.values()) / target_count
        backdoor_summary["target_recall_any"] = detected_targets / target_count
        backdoor_summary["target_recall_full"] = full_targets / target_count
        backdoor_summary["mean_target_baseline_recall"] = mean_target_recall
    else:
        backdoor_summary["target_recall_any"] = None
        backdoor_summary["target_recall_full"] = None
        backdoor_summary["mean_target_baseline_recall"] = None

    return {
        "coverage": {
            "evaluated_units": len(rows),
            "missing_units": missing_count,
            "ignored_units": ignored_count,
        },
        "global": global_metrics,
        "backdoor": backdoor_summary,
    }


def _evaluate_units(
    *,
    units: list[EvalUnit],
    predictions: dict[str, Prediction],
    missing_policy: str,
    allow_unknown: bool,
) -> tuple[list[dict[str, object]], int, int]:
    if missing_policy not in VALID_MISSING_POLICIES:
        raise ValueError(f"invalid missing policy: {missing_policy}")

    unit_by_id = {unit.unit_id: unit for unit in units}

    unknown_ids = sorted(set(predictions) - set(unit_by_id))
    if unknown_ids and not allow_unknown:
        sample = ", ".join(unknown_ids[:10])
        raise ValueError(
            f"predictions contain {len(unknown_ids)} unknown unit_id values; "
            f"examples: {sample}"
        )

    scored_rows: list[dict[str, object]] = []
    missing_units: list[str] = []
    ignored_count = 0

    for unit in sorted(units, key=lambda u: u.unit_id):
        pred = predictions.get(unit.unit_id)
        predicted_flagged = pred.flagged if pred else None
        predicted_score = pred.score if pred else None
        decision_status = "provided" if predicted_flagged is not None else "missing"

        if predicted_flagged is None:
            if missing_policy == "error":
                missing_units.append(unit.unit_id)
                continue
            if missing_policy == "ignore":
                ignored_count += 1
                continue
            predicted_flagged = False
            decision_status = "missing->negative"

        scored_rows.append(
            {
                "unit_id": unit.unit_id,
                "track": unit.track,
                "label": unit.label,
                "target_group": unit.target_group,
                "target": unit.target,
                "baseline_version": unit.baseline_version,
                "product": unit.product,
                "prev_version": unit.prev_version,
                "next_version": unit.next_version,
                "scope": unit.scope,
                "predicted_flagged": bool(predicted_flagged),
                "predicted_score": predicted_score,
                "decision_status": decision_status,
            }
        )

    if missing_units and missing_policy == "error":
        sample = ", ".join(missing_units[:10])
        raise ValueError(
            f"missing predictions for {len(missing_units)} unit_id values; "
            f"examples: {sample}. "
            "Use --missing-policy negative or ignore to proceed."
        )

    return scored_rows, len(missing_units), ignored_count


def _write_scored_units(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "unit_id",
        "track",
        "label",
        "target_group",
        "target",
        "baseline_version",
        "product",
        "prev_version",
        "next_version",
        "scope",
        "predicted_flagged",
        "predicted_score",
        "decision_status",
    ]
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _print_summary(metrics: dict) -> None:
    cov = metrics["coverage"]
    g = metrics["global"]
    m = metrics["backdoor"]

    print("Evaluation summary")
    print(
        f"- Units scored: {cov['evaluated_units']} "
        f"(missing={cov['missing_units']}, ignored={cov['ignored_units']})"
    )
    print(
        f"- Global: TP={g['tp']} FP={g['fp']} TN={g['tn']} FN={g['fn']} "
        f"precision={g['precision']:.4f} recall={g['recall']:.4f} f1={g['f1']:.4f}"
        if g["precision"] is not None and g["recall"] is not None and g["f1"] is not None
        else f"- Global: TP={g['tp']} FP={g['fp']} TN={g['tn']} FN={g['fn']}"
    )
    print(
        f"- Backdoor: unit_recall={m['unit_recall']:.4f} "
        f"target_recall_any={m['target_recall_any']:.4f} "
        f"target_recall_full={m['target_recall_full']:.4f}"
        if m["unit_recall"] is not None
        and m["target_recall_any"] is not None
        and m["target_recall_full"] is not None
        else "- Backdoor: no scored backdoor units"
    )


def main() -> int:
    repo_root = _repo_root_from_script()

    ap = argparse.ArgumentParser(
        description=(
            "Score detector predictions on R-Diff backdoor units. "
            "Predictions must include unit_id plus either flagged (bool) or score (float)."
        )
    )
    ap.add_argument("--repo-root", default=str(repo_root), help="Repo root (default: auto-detected)")
    ap.add_argument(
        "--ground-truth-csv",
        default="",
        help="Optional pre-built ground-truth CSV (columns: unit_id,track,label,...)",
    )
    ap.add_argument(
        "--baselines-config",
        default="",
        help="Path to baselines_config.json (default: targets/baselines_config.json)",
    )
    ap.add_argument(
        "--template-out",
        default="",
        help="Write a prediction template CSV (unit_id + metadata + empty flagged/score columns)",
    )
    ap.add_argument("--predictions", default="", help="Prediction CSV to score")
    ap.add_argument(
        "--score-threshold",
        type=float,
        default=0.5,
        help="Threshold for score->flagged conversion when flagged is not provided (default: 0.5)",
    )
    ap.add_argument(
        "--missing-policy",
        choices=sorted(VALID_MISSING_POLICIES),
        default="error",
        help="How to handle missing predictions (default: error)",
    )
    ap.add_argument(
        "--allow-unknown",
        action="store_true",
        help="Ignore prediction rows whose unit_id is not in ground truth",
    )
    ap.add_argument("--out-json", default="", help="Optional JSON output path for metrics")
    ap.add_argument("--out-csv", default="", help="Optional CSV output path for per-unit scored rows")
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    baselines_config = (
        Path(args.baselines_config).resolve()
        if args.baselines_config
        else (repo_root / "targets" / "baselines_config.json")
    )

    if args.ground_truth_csv:
        units = _units_from_ground_truth_csv(Path(args.ground_truth_csv).resolve())
    else:
        units = _build_ground_truth_units(
            repo_root=repo_root,
            baselines_config=baselines_config,
        )

    if args.template_out:
        template_path = Path(args.template_out).resolve()
        _write_template(template_path, units)
        print(f"Wrote prediction template: {template_path}")

    if not args.predictions:
        if args.template_out:
            return 0
        print("missing required --predictions (or provide only --template-out)", file=sys.stderr)
        return 2

    predictions = _load_predictions(Path(args.predictions).resolve(), args.score_threshold)
    scored_rows, missing_count, ignored_count = _evaluate_units(
        units=units,
        predictions=predictions,
        missing_policy=args.missing_policy,
        allow_unknown=args.allow_unknown,
    )

    metrics = _compute_metrics(scored_rows, missing_count, ignored_count)
    _print_summary(metrics)

    if args.out_json:
        out_json = Path(args.out_json).resolve()
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(metrics, indent=2) + "\n")
        print(f"Wrote metrics JSON: {out_json}")

    if args.out_csv:
        out_csv = Path(args.out_csv).resolve()
        _write_scored_units(out_csv, scored_rows)
        print(f"Wrote per-unit scored CSV: {out_csv}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
