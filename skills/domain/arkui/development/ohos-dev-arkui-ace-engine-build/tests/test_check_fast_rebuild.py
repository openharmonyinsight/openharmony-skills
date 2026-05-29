#!/usr/bin/env python3
"""Tests for check_fast_rebuild.sh — fast rebuild safety checker."""

import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "check_fast_rebuild.sh"


def create_oh_root(tmp: Path, product: str = "rk3568") -> Path:
    """Create a minimal OpenHarmony root structure."""
    oh_root = tmp / "openharmony"
    oh_root.mkdir()
    (oh_root / ".gn").write_text("# gn marker\n")
    out_dir = oh_root / "out" / product
    out_dir.mkdir(parents=True)
    # Create minimal build.ninja
    (out_dir / "build.ninja").write_text("rule cxx\n  command = clang++ $in -o $out\n")
    return oh_root


def init_git_repo(oh_root: Path):
    """Initialize a git repo in the OpenHarmony root."""
    subprocess.run(["git", "init", str(oh_root)], capture_output=True, check=True)
    subprocess.run(["git", "-C", str(oh_root), "config", "user.email", "test@test.com"], capture_output=True, check=True)
    subprocess.run(["git", "-C", str(oh_root), "config", "user.name", "Test"], capture_output=True, check=True)
    # Commit .gn so git status works
    subprocess.run(["git", "-C", str(oh_root), "add", ".gn"], capture_output=True, check=True)
    subprocess.run(["git", "-C", str(oh_root), "commit", "-m", "init"], capture_output=True, check=True)


def run_script(oh_root: Path, extra_args: list | None = None, product: str = "rk3568") -> subprocess.CompletedProcess[str]:
    args = ["bash", str(SCRIPT), "--root", str(oh_root), "--product", product]
    if extra_args:
        args.extend(extra_args)
    return subprocess.run(args, capture_output=True, text=True)


class CheckFastRebuildSafeTest(unittest.TestCase):
    """Test cases where fast rebuild IS safe."""

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Force-remove git directories that tempfile may struggle with
        import shutil
        shutil.rmtree(self._tmp_dir, ignore_errors=True)

    def test_clean_repo_safe(self):
        oh_root = create_oh_root(Path(self._tmp_dir))
        init_git_repo(oh_root)
        proc = run_script(oh_root)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Safe to use --fast-rebuild", proc.stdout)

    def test_source_only_change_safe(self):
        oh_root = create_oh_root(Path(self._tmp_dir))
        init_git_repo(oh_root)
        # Modify a .cpp file — not a GN file
        src = oh_root / "test.cpp"
        src.write_text("int main() { return 0; }")
        proc = run_script(oh_root)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Safe to use --fast-rebuild", proc.stdout)


class CheckFastRebuildUnsafeTest(unittest.TestCase):
    """Test cases where fast rebuild is NOT safe."""

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self._tmp_dir, ignore_errors=True)

    def test_uncommitted_build_gn(self):
        oh_root = create_oh_root(Path(self._tmp_dir))
        init_git_repo(oh_root)
        # Create uncommitted BUILD.gn
        (oh_root / "BUILD.gn").write_text('source_set("test") { sources = [] }')
        proc = run_script(oh_root)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Do NOT use --fast-rebuild", proc.stdout)

    def test_uncommitted_gni_file(self):
        oh_root = create_oh_root(Path(self._tmp_dir))
        init_git_repo(oh_root)
        # Create uncommitted .gni file
        (oh_root / "config.gni").write_text('sources = []')
        proc = run_script(oh_root)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Do NOT use --fast-rebuild", proc.stdout)

    def test_gn_newer_than_ninja(self):
        oh_root = create_oh_root(Path(self._tmp_dir))
        init_git_repo(oh_root)
        # Create a BUILD.gn, commit it, then touch it to be newer than build.ninja
        gn_file = oh_root / "BUILD.gn"
        gn_file.write_text('source_set("test") { sources = [] }')
        subprocess.run(["git", "-C", str(oh_root), "add", "BUILD.gn"], capture_output=True, check=True)
        subprocess.run(["git", "-C", str(oh_root), "commit", "-m", "add gn"], capture_output=True, check=True)
        # Touch build.ninja to be older
        ninja_file = oh_root / "out" / "rk3568" / "build.ninja"
        # Make build.ninja older by setting its mtime to the past
        os.utime(str(ninja_file), (time.time() - 3600, time.time() - 3600))
        # Touch BUILD.gn to be newer
        gn_file.touch()
        proc = run_script(oh_root)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Do NOT use --fast-rebuild", proc.stdout)


class CheckFastRebuildEdgeCasesTest(unittest.TestCase):
    """Test edge cases."""

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self._tmp_dir, ignore_errors=True)

    def test_no_build_output_first_build(self):
        oh_root = Path(self._tmp_dir) / "openharmony"
        oh_root.mkdir()
        (oh_root / ".gn").write_text("# gn marker\n")
        # No out/ directory
        proc = run_script(oh_root)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("first-time build", proc.stdout)

    def test_custom_product(self):
        oh_root = create_oh_root(Path(self._tmp_dir), "rk3588")
        init_git_repo(oh_root)
        proc = run_script(oh_root, product="rk3588")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Safe to use --fast-rebuild", proc.stdout)

    def test_custom_time_window(self):
        oh_root = create_oh_root(Path(self._tmp_dir))
        init_git_repo(oh_root)
        # Use 0 minute window — no files can be that recent
        proc = run_script(oh_root, extra_args=["0"])
        # Should still pass other checks and be safe
        self.assertEqual(proc.returncode, 0, proc.stderr)


if __name__ == "__main__":
    unittest.main()
