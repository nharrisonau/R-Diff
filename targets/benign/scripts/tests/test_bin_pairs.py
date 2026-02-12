import csv
import subprocess
import tempfile
import unittest
from pathlib import Path


class TestBinPairs(unittest.TestCase):
    def test_bins_expected_scopes(self):
        repo_root = Path(__file__).resolve().parents[4]
        script = repo_root / "targets" / "benign" / "scripts" / "bin_pairs.py"

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            pairs = td_path / "pairs.csv"
            out_csv = td_path / "pairs_binned.csv"
            out_txt = td_path / "pairs_binned.txt"
            bins_dir = td_path / "bins"

            with pairs.open("w", newline="") as fh:
                writer = csv.DictWriter(
                    fh,
                    fieldnames=[
                        "product",
                        "prev_version",
                        "next_version",
                        "prev_rootfs",
                        "next_rootfs",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "product": "p",
                        "prev_version": "1.2.3",
                        "next_version": "2.0.0",
                        "prev_rootfs": "a",
                        "next_rootfs": "b",
                    }
                )
                writer.writerow(
                    {
                        "product": "p",
                        "prev_version": "1.2.3",
                        "next_version": "1.3.0",
                        "prev_rootfs": "a",
                        "next_rootfs": "b",
                    }
                )
                writer.writerow(
                    {
                        "product": "p",
                        "prev_version": "1.2.3",
                        "next_version": "1.2.4",
                        "prev_rootfs": "a",
                        "next_rootfs": "b",
                    }
                )
                writer.writerow(
                    {
                        "product": "p",
                        "prev_version": "1.2.3",
                        "next_version": "1.2.3.1",
                        "prev_rootfs": "a",
                        "next_rootfs": "b",
                    }
                )
                writer.writerow(
                    {
                        "product": "p",
                        "prev_version": "x",
                        "next_version": "y",
                        "prev_rootfs": "a",
                        "next_rootfs": "b",
                    }
                )

            proc = subprocess.run(
                [
                    "python3",
                    str(script),
                    "--pairs",
                    str(pairs),
                    "--out",
                    str(out_csv),
                    "--out-txt",
                    str(out_txt),
                    "--bins-dir",
                    str(bins_dir),
                    "--no-blank-lines",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)

            with out_csv.open(newline="") as fh:
                rows = list(csv.DictReader(fh))

            scopes = [row["scope"] for row in rows]
            self.assertEqual(scopes, ["major", "minor", "patch", "build", "other"])


if __name__ == "__main__":
    unittest.main()
