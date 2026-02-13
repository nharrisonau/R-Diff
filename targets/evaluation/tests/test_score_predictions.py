import csv
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class TestScorePredictions(unittest.TestCase):
    def _write_csv(self, path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    def test_scores_malicious_and_benign_metrics(self) -> None:
        script = Path("targets/evaluation/score_predictions.py").resolve()
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            gt = tmpdir / "ground_truth.csv"
            preds = tmpdir / "predictions.csv"
            out_json = tmpdir / "metrics.json"

            self._write_csv(
                gt,
                [
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
                ],
                [
                    {
                        "unit_id": "malicious::synthetic::t1::v1",
                        "track": "malicious",
                        "label": 1,
                        "target_group": "synthetic",
                        "target": "t1",
                        "baseline_version": "v1",
                    },
                    {
                        "unit_id": "malicious::synthetic::t1::v2",
                        "track": "malicious",
                        "label": 1,
                        "target_group": "synthetic",
                        "target": "t1",
                        "baseline_version": "v2",
                    },
                    {
                        "unit_id": "malicious::authentic::t2::v1",
                        "track": "malicious",
                        "label": 1,
                        "target_group": "authentic",
                        "target": "t2",
                        "baseline_version": "v1",
                    },
                    {
                        "unit_id": "benign::p1::1.0::1.1",
                        "track": "benign",
                        "label": 0,
                        "product": "p1",
                        "prev_version": "1.0",
                        "next_version": "1.1",
                        "scope": "major",
                    },
                    {
                        "unit_id": "benign::p2::2.0::2.0.1",
                        "track": "benign",
                        "label": 0,
                        "product": "p2",
                        "prev_version": "2.0",
                        "next_version": "2.0.1",
                        "scope": "patch",
                    },
                ],
            )

            self._write_csv(
                preds,
                ["unit_id", "flagged"],
                [
                    {"unit_id": "malicious::synthetic::t1::v1", "flagged": 1},
                    {"unit_id": "malicious::synthetic::t1::v2", "flagged": 0},
                    {"unit_id": "malicious::authentic::t2::v1", "flagged": 1},
                    {"unit_id": "benign::p1::1.0::1.1", "flagged": 0},
                    {"unit_id": "benign::p2::2.0::2.0.1", "flagged": 1},
                ],
            )

            proc = subprocess.run(
                [
                    "python3",
                    str(script),
                    "--ground-truth-csv",
                    str(gt),
                    "--predictions",
                    str(preds),
                    "--out-json",
                    str(out_json),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)

            metrics = json.loads(out_json.read_text())
            self.assertEqual(metrics["global"]["tp"], 2)
            self.assertEqual(metrics["global"]["fp"], 1)
            self.assertEqual(metrics["global"]["tn"], 1)
            self.assertEqual(metrics["global"]["fn"], 1)

            self.assertAlmostEqual(metrics["malicious"]["unit_recall"], 2 / 3, places=6)
            self.assertAlmostEqual(metrics["malicious"]["target_recall_any"], 1.0, places=6)
            self.assertAlmostEqual(metrics["malicious"]["target_recall_full"], 0.5, places=6)

            self.assertEqual(metrics["benign"]["overall"]["false_positives"], 1)
            self.assertAlmostEqual(metrics["benign"]["overall"]["fp_rate"], 0.5, places=6)
            self.assertAlmostEqual(
                metrics["benign"]["bucket_fp"]["major"]["fp_rate"], 0.0, places=6
            )
            self.assertAlmostEqual(
                metrics["benign"]["bucket_fp"]["patch"]["fp_rate"], 1.0, places=6
            )
            self.assertAlmostEqual(metrics["benign"]["bucket_macro_fp_rate"], 0.5, places=6)
            self.assertEqual(metrics["benign"]["worst_bucket"], "patch")
            self.assertAlmostEqual(metrics["benign"]["worst_bucket_fp_rate"], 1.0, places=6)

    def test_missing_predictions_error_by_default(self) -> None:
        script = Path("targets/evaluation/score_predictions.py").resolve()
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            gt = tmpdir / "ground_truth.csv"
            preds = tmpdir / "predictions.csv"

            self._write_csv(
                gt,
                ["unit_id", "track", "label"],
                [
                    {"unit_id": "malicious::synthetic::t1::v1", "track": "malicious", "label": 1},
                    {"unit_id": "benign::p1::1.0::1.1", "track": "benign", "label": 0},
                ],
            )
            self._write_csv(
                preds,
                ["unit_id", "flagged"],
                [{"unit_id": "malicious::synthetic::t1::v1", "flagged": 1}],
            )

            proc = subprocess.run(
                [
                    "python3",
                    str(script),
                    "--ground-truth-csv",
                    str(gt),
                    "--predictions",
                    str(preds),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("missing predictions", proc.stderr + proc.stdout)

    def test_template_only_mode(self) -> None:
        script = Path("targets/evaluation/score_predictions.py").resolve()
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            gt = tmpdir / "ground_truth.csv"
            template = tmpdir / "template.csv"

            self._write_csv(
                gt,
                ["unit_id", "track", "label", "scope"],
                [
                    {"unit_id": "malicious::synthetic::t1::v1", "track": "malicious", "label": 1},
                    {
                        "unit_id": "benign::p1::1.0::1.1",
                        "track": "benign",
                        "label": 0,
                        "scope": "major",
                    },
                ],
            )

            proc = subprocess.run(
                [
                    "python3",
                    str(script),
                    "--ground-truth-csv",
                    str(gt),
                    "--template-out",
                    str(template),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)

            with template.open(newline="") as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual(len(rows), 2)
            self.assertIn("flagged", rows[0])
            self.assertIn("score", rows[0])
            self.assertEqual(rows[0]["flagged"], "")
            self.assertEqual(rows[0]["score"], "")


if __name__ == "__main__":
    unittest.main()
