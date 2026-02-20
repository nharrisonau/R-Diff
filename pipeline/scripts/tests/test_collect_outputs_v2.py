import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

# Allow running tests without requiring targets/ to be a Python package.
SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import collect_outputs_v2  # noqa: E402


class TestCollectOutputsV2Report(unittest.TestCase):
    def test_resolve_artifact_relpath_from_config(self):
        self.assertEqual(
            collect_outputs_v2._resolve_artifact_relpath(
                {"artifact_relpath": "build/libexec/sudo/sudoers.so"}
            ),
            "build/libexec/sudo/sudoers.so",
        )

    def test_resolve_artifact_relpath_requires_config(self):
        with self.assertRaises(RuntimeError):
            collect_outputs_v2._resolve_artifact_relpath({})

    def test_writes_baseline_collection_report(self):
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            target_name = "sample-1.0"
            rel_path = f"synthetic/{target_name}"

            config_path = repo_root / "pipeline" / "baselines_config.json"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(
                json.dumps(
                    [
                        {
                            "path": rel_path,
                            "group": "synthetic",
                            "current_version": "1.0.0",
                            "mode": "manual",
                            "artifact_relpath": "sample.bin",
                        }
                    ]
                )
            )

            baselines_path = repo_root / "local_outputs" / "baselines.csv"
            baselines_path.parent.mkdir(parents=True, exist_ok=True)
            with baselines_path.open("w", newline="") as fh:
                writer = csv.DictWriter(
                    fh,
                    fieldnames=[
                        "group",
                        "target_dir",
                        "current_version",
                        "baseline_version",
                        "baseline_tag",
                        "build_dir",
                        "artifact_relpath",
                        "status",
                        "error",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "group": "synthetic",
                        "target_dir": target_name,
                        "current_version": "1.0.0",
                        "baseline_version": "0.9.0",
                        "baseline_tag": "v0.9.0",
                        "build_dir": "baseline-artifacts/0.9.0",
                        "artifact_relpath": "sample.bin",
                        "status": "built",
                        "error": "",
                    }
                )
                writer.writerow(
                    {
                        "group": "synthetic",
                        "target_dir": target_name,
                        "current_version": "1.0.0",
                        "baseline_version": "0.8.0",
                        "baseline_tag": "v0.8.0",
                        "build_dir": "baseline-artifacts/0.8.0",
                        "artifact_relpath": "sample.bin",
                        "status": "built",
                        "error": "",
                    }
                )
                writer.writerow(
                    {
                        "group": "synthetic",
                        "target_dir": target_name,
                        "current_version": "1.0.0",
                        "baseline_version": "0.7.0",
                        "baseline_tag": "v0.7.0",
                        "build_dir": "baseline-artifacts/0.7.0",
                        "artifact_relpath": "sample.bin",
                        "status": "failed",
                        "error": "make failed",
                    }
                )

            target_dir = repo_root / "targets" / rel_path
            target_dir.mkdir(parents=True, exist_ok=True)

            (target_dir / "safe").mkdir(parents=True, exist_ok=True)
            (target_dir / "safe" / "sample.bin").write_text("safe")
            (target_dir / "backdoored").mkdir(parents=True, exist_ok=True)
            (target_dir / "backdoored" / "sample.bin").write_text("backdoored")
            (target_dir / "baseline-artifacts" / "0.9.0").mkdir(parents=True, exist_ok=True)
            (target_dir / "baseline-artifacts" / "0.9.0" / "sample.bin").write_text("baseline")

            old_argv = sys.argv
            try:
                sys.argv = [
                    "collect_outputs_v2.py",
                    "--repo-root",
                    str(repo_root),
                    "--out-base",
                    str(repo_root / "outputs"),
                    "--strip-tool",
                    "true",
                ]
                rc = collect_outputs_v2.main()
            finally:
                sys.argv = old_argv

            self.assertEqual(rc, 0)

            report_path = (
                repo_root / "outputs" / "targets" / "reports" / "baselines_report.csv"
            )
            self.assertTrue(report_path.exists())

            with report_path.open(newline="") as fh:
                rows = list(csv.DictReader(fh))

            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(row["group"], "synthetic")
            self.assertEqual(row["target_dir"], target_name)
            self.assertEqual(row["collected_baseline_count"], "1")
            self.assertEqual(row["collected_baseline_versions"], "0.9.0")
            self.assertEqual(row["failed_baseline_count"], "2")
            self.assertEqual(row["failed_baseline_versions"], "0.7.0;0.8.0")
            self.assertIn("0.7.0: make failed", row["failed_details"])
            self.assertIn(
                "0.8.0: missing artifact during collection: baseline-artifacts/0.8.0/sample.bin",
                row["failed_details"],
            )


if __name__ == "__main__":
    unittest.main()
