import csv
import subprocess
import tempfile
import unittest
from pathlib import Path


class TestBuildPairs(unittest.TestCase):
    def test_pairs_sorted_by_date(self):
        repo_root = Path(__file__).resolve().parents[4]
        script = repo_root / "targets" / "benign" / "scripts" / "build_pairs.py"

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            manifest = td_path / "manifest.csv"
            out_pairs = td_path / "pairs.csv"

            with manifest.open("w", newline="") as fh:
                writer = csv.DictWriter(
                    fh,
                    fieldnames=[
                        "dataset",
                        "product",
                        "version",
                        "date",
                        "url",
                        "rootfs_path",
                        "notes",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "dataset": "benign",
                        "product": "demo",
                        "version": "1.1.0",
                        "date": "2024-02-01",
                        "url": "u1",
                        "rootfs_path": "r1",
                        "notes": "",
                    }
                )
                writer.writerow(
                    {
                        "dataset": "benign",
                        "product": "demo",
                        "version": "1.0.0",
                        "date": "2024-01-01",
                        "url": "u0",
                        "rootfs_path": "r0",
                        "notes": "",
                    }
                )
                writer.writerow(
                    {
                        "dataset": "benign",
                        "product": "demo",
                        "version": "1.2.0",
                        "date": "2024-03-01",
                        "url": "u2",
                        "rootfs_path": "r2",
                        "notes": "",
                    }
                )

            proc = subprocess.run(
                ["python3", str(script), "--manifest", str(manifest), "--out", str(out_pairs)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)

            with out_pairs.open(newline="") as fh:
                rows = list(csv.DictReader(fh))

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["prev_version"], "1.0.0")
            self.assertEqual(rows[0]["next_version"], "1.1.0")
            self.assertEqual(rows[1]["prev_version"], "1.1.0")
            self.assertEqual(rows[1]["next_version"], "1.2.0")


if __name__ == "__main__":
    unittest.main()
