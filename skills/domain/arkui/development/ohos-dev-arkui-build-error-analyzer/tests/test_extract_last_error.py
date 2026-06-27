#!/usr/bin/env python3
"""Tests for extract_last_error.sh — build error extraction script."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "extract_last_error.sh"


def run_script(build_log: str, env: dict | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["bash", str(SCRIPT), build_log],
        capture_output=True,
        text=True,
        env=env,
    )
    return result


def write_build_log(tmp: Path, content: str, name: str = "build.log") -> Path:
    log = tmp / name
    log.write_text(content, encoding="utf-8")
    return log


class ExtractLastErrorSuccessTest(unittest.TestCase):
    """Test success detection."""

    def test_build_success_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            out_dir = tmpdir / "out" / "rk3568"
            out_dir.mkdir(parents=True)
            log = write_build_log(out_dir, (
                "[100/100] CXX something.cpp\n"
                "=====build successful=====\n"
            ))
            proc = run_script(str(log))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            last_error = out_dir / "last_error.log"
            self.assertTrue(last_error.exists())
            self.assertIn("build success, no error", last_error.read_text())

    def test_no_errors_in_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            out_dir = tmpdir / "out" / "rk3568"
            out_dir.mkdir(parents=True)
            log = write_build_log(out_dir, (
                "[1/10] CXX a.cpp\n"
                "[2/10] CXX b.cpp\n"
                "[3/10] CXX c.cpp\n"
            ))
            proc = run_script(str(log))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            last_error = out_dir / "last_error.log"
            self.assertTrue(last_error.exists())
            content = last_error.read_text()
            self.assertIn("build success, no error", content)


class ExtractLastErrorFailureTest(unittest.TestCase):
    """Test error extraction from failed builds."""

    def test_compilation_error_extracted(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            out_dir = tmpdir / "out" / "rk3568"
            out_dir.mkdir(parents=True)
            log = write_build_log(out_dir, (
                "[1/10] CXX ok.cpp\n"
                "[2/10] CXX broken.cpp\n"
                "FAILED: obj/broken.o\n"
                "broken.cpp:10:5: fatal error: 'missing.h' file not found\n"
                "    #include \"missing.h\"\n"
                "            ^~~~~~~~~~~~\n"
                "1 error generated.\n"
                "=====build failed=====\n"
            ))
            proc = run_script(str(log))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            last_error = out_dir / "last_error.log"
            content = last_error.read_text()
            self.assertIn("fatal error", content)
            self.assertIn("missing.h", content)

    def test_linker_error_extracted(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            out_dir = tmpdir / "out" / "rk3568"
            out_dir.mkdir(parents=True)
            log = write_build_log(out_dir, (
                "[1/5] CXX main.cpp\n"
                "[2/5] SOLINK libtest.so\n"
                "FAILED: libtest.so\n"
                "ld.lld: error: undefined symbol: MyClass::DoSomething()\n"
                ">>> referenced by main.cpp\n"
                "=====build failed=====\n"
            ))
            proc = run_script(str(log))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            last_error = out_dir / "last_error.log"
            content = last_error.read_text()
            self.assertIn("undefined symbol", content)

    def test_last_error_preferred_over_earlier(self):
        """When multiple error blocks exist, only the last is extracted."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            out_dir = tmpdir / "out" / "rk3568"
            out_dir.mkdir(parents=True)
            log = write_build_log(out_dir, (
                "[1/5] CXX first.cpp\n"
                "FAILED: obj/first.o\n"
                "first.cpp:1:1: fatal error: first error\n"
                "[2/5] CXX second.cpp\n"
                "FAILED: obj/second.o\n"
                "second.cpp:5:1: fatal error: second error\n"
                "=====build failed=====\n"
            ))
            proc = run_script(str(log))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            last_error = out_dir / "last_error.log"
            content = last_error.read_text()
            self.assertIn("second error", content)
            self.assertNotIn("first error", content)


class ExtractLastErrorEdgeCasesTest(unittest.TestCase):
    """Test edge cases."""

    def test_nonexistent_log_file(self):
        proc = run_script("/nonexistent/path/build.log")
        self.assertNotEqual(proc.returncode, 0)

    def test_empty_build_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            out_dir = tmpdir / "out" / "rk3568"
            out_dir.mkdir(parents=True)
            log = write_build_log(out_dir, "")
            proc = run_script(str(log))
            # Empty log has no errors, should report success
            self.assertEqual(proc.returncode, 0, proc.stderr)
            last_error = out_dir / "last_error.log"
            content = last_error.read_text()
            self.assertIn("build success, no error", content)

    def test_stale_errors_after_successful_rebuild(self):
        """If build succeeded after earlier failures, report success."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            out_dir = tmpdir / "out" / "rk3568"
            out_dir.mkdir(parents=True)
            log = write_build_log(out_dir, (
                "[1/5] CXX broken.cpp\n"
                "FAILED: obj/broken.o\n"
                "fatal error: old error\n"
                "=====build failed=====\n"
                "[1/5] CXX broken.cpp\n"
                "[2/5] CXX fixed.cpp\n"
                "=====build successful=====\n"
            ))
            proc = run_script(str(log))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            last_error = out_dir / "last_error.log"
            content = last_error.read_text()
            self.assertIn("build success, no error", content)

    def test_output_in_same_dir_as_log(self):
        """last_error.log should be created in the same directory as build.log."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            out_dir = tmpdir / "out" / "custom_product"
            out_dir.mkdir(parents=True)
            log = write_build_log(out_dir, "=====build successful=====\n")
            proc = run_script(str(log))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            expected_output = out_dir / "last_error.log"
            self.assertTrue(expected_output.exists(), f"Expected output at {expected_output}")


if __name__ == "__main__":
    unittest.main()
