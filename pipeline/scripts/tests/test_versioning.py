import unittest
from pathlib import Path
import sys

# Allow running tests without requiring targets/ to be a Python package.
SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from versioning import normalize_version, parse_version  # noqa: E402


class TestVersioning(unittest.TestCase):
    def test_semver_order(self):
        a = parse_version("1.6.42", "semver")
        b = parse_version("1.6.43", "semver")
        self.assertLess(a.key, b.key)

    def test_openssl_prerelease_order(self):
        alpha = parse_version("3.0.0-alpha1", "openssl")
        beta = parse_version("3.0.0-beta2", "openssl")
        final = parse_version("3.0.0", "openssl")
        self.assertLess(alpha.key, beta.key)
        self.assertLess(beta.key, final.key)

    def test_sudo_normalization_and_order(self):
        v1 = parse_version(normalize_version("1_9_15p4", "sudo"), "sudo")
        v2 = parse_version("1.9.15p5", "sudo")
        self.assertLess(v1.key, v2.key)

    def test_dropbear_year(self):
        a = parse_version("2024.85", "dropbear_year")
        b = parse_version("2024.86", "dropbear_year")
        self.assertLess(a.key, b.key)

    def test_letter_suffix(self):
        b = parse_version("1.3.3b", "semver")
        c = parse_version("1.3.3c", "semver")
        self.assertLess(b.key, c.key)


if __name__ == "__main__":
    unittest.main()
