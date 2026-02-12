import csv
import subprocess
import tempfile
import unittest
from pathlib import Path


class TestVerifyMetadata(unittest.TestCase):
    def test_verify_metadata_happy_path(self):
        repo_root = Path(__file__).resolve().parents[4]
        script = repo_root / "targets" / "benign" / "scripts" / "verify_metadata.py"

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            manifest = td_path / "manifest.csv"
            pairs = td_path / "pairs.csv"
            pairs_binned = td_path / "pairs_binned.csv"

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
                        "product": "p",
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
                        "product": "p",
                        "version": "1.1.0",
                        "date": "2024-02-01",
                        "url": "u1",
                        "rootfs_path": "r1",
                        "notes": "",
                    }
                )

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
                        "prev_version": "1.0.0",
                        "next_version": "1.1.0",
                        "prev_rootfs": "r0",
                        "next_rootfs": "r1",
                    }
                )

            with pairs_binned.open("w", newline="") as fh:
                writer = csv.DictWriter(
                    fh,
                    fieldnames=[
                        "product",
                        "prev_version",
                        "next_version",
                        "prev_rootfs",
                        "next_rootfs",
                        "version_scope",
                        "scope",
                        "scope_reason",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "product": "p",
                        "prev_version": "1.0.0",
                        "next_version": "1.1.0",
                        "prev_rootfs": "r0",
                        "next_rootfs": "r1",
                        "version_scope": "minor",
                        "scope": "minor",
                        "scope_reason": "version-tokens",
                    }
                )

            proc = subprocess.run(
                [
                    "python3",
                    str(script),
                    "--manifest",
                    str(manifest),
                    "--pairs",
                    str(pairs),
                    "--pairs-binned",
                    str(pairs_binned),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
