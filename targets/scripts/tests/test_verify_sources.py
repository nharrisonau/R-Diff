import subprocess
import unittest
from pathlib import Path


class TestVerifySources(unittest.TestCase):
    def test_verify_sources_lock(self):
        repo_root = Path(__file__).resolve().parents[3]
        script = repo_root / "targets" / "scripts" / "verify_sources.py"
        proc = subprocess.run(
            ["python3", str(script), "--repo-root", str(repo_root)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            proc.returncode,
            0,
            msg=f"verify_sources failed\\nstdout:\\n{proc.stdout}\\nstderr:\\n{proc.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
