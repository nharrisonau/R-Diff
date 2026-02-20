import unittest
from pathlib import Path
import sys
import tempfile

# Allow running tests without requiring targets/ to be a Python package.
SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from build_baselines import (  # noqa: E402
    _load_failed_versions,
    _resolve_artifact_relpath,
    _short_error,
    baseline_build_dir,
    dedupe_baseline_candidates,
)


class TestBuildBaselinesHelpers(unittest.TestCase):
    def test_resolve_artifact_relpath_from_config(self):
        self.assertEqual(
            _resolve_artifact_relpath({"artifact_relpath": "build/libexec/sudo/sudoers.so"}),
            "build/libexec/sudo/sudoers.so",
        )

    def test_resolve_artifact_relpath_requires_config(self):
        with self.assertRaises(RuntimeError):
            _resolve_artifact_relpath({})

    def test_baseline_build_dir_mapping(self):
        self.assertEqual(baseline_build_dir("1.6.42"), "baseline-artifacts/1.6.42")
        self.assertEqual(baseline_build_dir("3.0.0-beta2"), "baseline-artifacts/3.0.0-beta2")

    def test_baseline_build_dir_sanitizes_path_chars(self):
        self.assertEqual(baseline_build_dir("1/2"), "baseline-artifacts/1_2")

    def test_dedupe_baseline_candidates_preserves_order(self):
        deduped = dedupe_baseline_candidates(
            [
                ("1.6.42", "v1.6.42"),
                ("1.6.41", "v1.6.41"),
                ("1.6.41", "release-1.6.41"),
                ("1.6.40", "v1.6.40"),
            ]
        )
        self.assertEqual(
            deduped,
            [
                ("1.6.42", "v1.6.42"),
                ("1.6.41", "v1.6.41"),
                ("1.6.40", "v1.6.40"),
            ],
        )

    def test_dedupe_baseline_candidates_with_preseen_versions(self):
        deduped = dedupe_baseline_candidates(
            [
                ("1.6.42", "v1.6.42"),
                ("1.6.41", "v1.6.41"),
                ("1.6.41", "release-1.6.41"),
            ],
            seen_versions={"1.6.42"},
        )
        self.assertEqual(deduped, [("1.6.41", "v1.6.41")])

    def test_short_error_ignores_make_directory_lines(self):
        msg = (
            "build failed: missing header\n"
            "make[1]: Leaving directory '/tmp/project'\n"
        )
        self.assertEqual(_short_error(msg), "build failed: missing header")

    def test_load_failed_versions_returns_empty_for_missing_file(self):
        with tempfile.TemporaryDirectory() as td:
            missing = Path(td) / "nope.csv"
            self.assertEqual(_load_failed_versions(missing), {})

    def test_load_failed_versions_groups_by_target(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "baselines.csv"
            path.write_text(
                "\n".join(
                    [
                        "group,target_dir,current_version,baseline_version,baseline_tag,build_dir,artifact_relpath,status,error",
                        "synthetic,libpng-1.6.43,1.6.43,1.6.31,v1.6.31,baseline-artifacts/1.6.31,libpng_read_fuzzer,failed,make failed",
                        "synthetic,libpng-1.6.43,1.6.43,1.6.30,v1.6.30,baseline-artifacts/1.6.30,libpng_read_fuzzer,failed,make failed",
                        "synthetic,libpng-1.6.43,1.6.43,1.6.42,v1.6.42,baseline-artifacts/1.6.42,libpng_read_fuzzer,built,",
                        "synthetic,sudo-1.9.15p5,1.9.15p5,1.9.0,v1.9.0,baseline-artifacts/1.9.0,build/bin/sudo,failed,make failed",
                        "synthetic,sudo-1.9.15p5,1.9.15p5,,v1.8.32,baseline-artifacts/1.8.32,build/bin/sudo,failed,missing version",
                    ]
                )
                + "\n"
            )

            failed = _load_failed_versions(path)
            self.assertEqual(
                failed,
                {
                    ("synthetic", "libpng-1.6.43"): {"1.6.30", "1.6.31"},
                    ("synthetic", "sudo-1.9.15p5"): {"1.9.0"},
                },
            )


if __name__ == "__main__":
    unittest.main()
