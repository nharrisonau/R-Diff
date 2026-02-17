import subprocess
import unittest
from pathlib import Path


class TestVerifyTargetMetadata(unittest.TestCase):
    def test_verify_target_metadata(self):
        repo_root = Path(__file__).resolve().parents[3]
        script = (
            repo_root / "targets" / "scripts" / "verify_target_metadata.py"
        )
        proc = subprocess.run(
            ["python3", str(script), "--repo-root", str(repo_root)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            proc.returncode,
            0,
            msg=f"verify_target_metadata failed\\nstdout:\\n{proc.stdout}\\nstderr:\\n{proc.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
