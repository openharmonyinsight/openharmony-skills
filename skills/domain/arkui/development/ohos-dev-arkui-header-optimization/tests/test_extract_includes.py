#!/usr/bin/env python3
"""Tests for extract-includes.py — header optimization screening tool."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "extract-includes.py"


def run_script(header_file: str, fmt: str = "text") -> subprocess.CompletedProcess[str]:
    args = [sys.executable, str(SCRIPT), header_file, "--format", fmt]
    return subprocess.run(args, capture_output=True, text=True)


def write_header(tmp: Path, content: str, name: str = "test.h") -> Path:
    h = tmp / name
    h.write_text(content, encoding="utf-8")
    return h


class ExtractIncludesBasicTest(unittest.TestCase):
    """Test include extraction and classification."""

    def test_no_includes(self):
        with tempfile.TemporaryDirectory() as tmp:
            h = write_header(Path(tmp), "// no includes\n")
            proc = run_script(str(h))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("Total includes:       0", proc.stdout)

    def test_system_includes(self):
        with tempfile.TemporaryDirectory() as tmp:
            h = write_header(Path(tmp), '#include <string>\n#include <vector>\n')
            proc = run_script(str(h))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("string", proc.stdout)
            self.assertIn("vector", proc.stdout)

    def test_project_includes(self):
        with tempfile.TemporaryDirectory() as tmp:
            h = write_header(Path(tmp), '#include "ace_engine/core/frame_node.h"\n')
            proc = run_script(str(h), fmt="json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(proc.stdout)
            self.assertTrue(any("ace_engine" in inc["path"] for inc in data["includes"]))
            proj = [inc for inc in data["includes"] if inc["type"] == "project"]
            self.assertEqual(len(proj), 1)

    def test_local_includes(self):
        with tempfile.TemporaryDirectory() as tmp:
            h = write_header(Path(tmp), '#include "my_helper.h"\n')
            proc = run_script(str(h), fmt="json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(proc.stdout)
            local = [inc for inc in data["includes"] if inc["type"] == "local"]
            self.assertEqual(len(local), 1)

    def test_file_not_found(self):
        proc = run_script("/nonexistent/path/test.h")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("not found", proc.stderr)


class ExtractIncludesForwardDeclTest(unittest.TestCase):
    """Test forward declaration candidate identification."""

    def test_unused_include_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Include frame_node.h but never use FrameNode
            h = write_header(Path(tmp), (
                '#include "frame_node.h"\n'
                'class MyClass {};\n'
            ))
            proc = run_script(str(h), fmt="json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(proc.stdout)
            candidates = data["forward_decl_candidates"]
            unused = [c for c in candidates if c["safety"] == "unused"]
            self.assertTrue(len(unused) >= 1, "Expected at least one unused include")

    def test_base_class_unsafe(self):
        with tempfile.TemporaryDirectory() as tmp:
            # frame_node.h exports FrameNode; inherit from it — unsafe
            h = write_header(Path(tmp), (
                '#include "frame_node.h"\n'
                'class MyClass : public FrameNode {};\n'
            ))
            proc = run_script(str(h), fmt="json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(proc.stdout)
            unsafe = [c for c in data["forward_decl_candidates"] if c["safety"] == "unsafe"]
            self.assertTrue(len(unsafe) >= 1, "Expected base class usage as unsafe")
            self.assertTrue(any(c["flags"].get("is_base_class") for c in unsafe))

    def test_pointer_member_is_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            # frame_node.h exports FrameNode; use as pointer — candidate
            h = write_header(Path(tmp), (
                '#include "frame_node.h"\n'
                'class MyClass {\n'
                '    FrameNode* node_;\n'
                '};\n'
            ))
            proc = run_script(str(h), fmt="json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(proc.stdout)
            candidates = [c for c in data["forward_decl_candidates"] if c.get("type_name") == "FrameNode"]
            self.assertTrue(len(candidates) >= 1, "Expected FrameNode candidate")
            self.assertEqual(candidates[0]["safety"], "candidate")

    def test_refptr_member_is_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            h = write_header(Path(tmp), (
                '#include "frame_node.h"\n'
                'class MyClass {\n'
                '    RefPtr<FrameNode> node_;\n'
                '};\n'
            ))
            proc = run_script(str(h), fmt="json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(proc.stdout)
            candidates = [c for c in data["forward_decl_candidates"] if c.get("type_name") == "FrameNode"]
            self.assertTrue(len(candidates) >= 1)
            self.assertEqual(candidates[0]["safety"], "candidate")

    def test_value_member_is_unsafe(self):
        with tempfile.TemporaryDirectory() as tmp:
            h = write_header(Path(tmp), (
                '#include "frame_node.h"\n'
                'class MyClass {\n'
                '    FrameNode node_;\n'
                '};\n'
            ))
            proc = run_script(str(h), fmt="json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(proc.stdout)
            unsafe = [c for c in data["forward_decl_candidates"] if c["safety"] == "unsafe"]
            self.assertTrue(len(unsafe) >= 1, "Expected value member as unsafe")
            self.assertTrue(any(c["flags"].get("has_value_member") for c in unsafe))


class ExtractIncludesStatisticsTest(unittest.TestCase):
    """Test statistics calculation and recommendations."""

    def test_high_include_count_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            includes = "\n".join(f'#include "dep_{i}.h"' for i in range(10))
            h = write_header(Path(tmp), includes + "\nclass Foo {};\n")
            proc = run_script(str(h))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("HIGH include count", proc.stdout)

    def test_well_optimized_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            h = write_header(Path(tmp), "class Foo {};\n")
            proc = run_script(str(h))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("well-optimized", proc.stdout)


class ExtractIncludesJsonOutputTest(unittest.TestCase):
    """Test JSON output format."""

    def test_json_has_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            h = write_header(Path(tmp), '#include "frame_node.h"\nclass Foo {};\n')
            proc = run_script(str(h), fmt="json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(proc.stdout)
            for key in ("header", "stats", "includes", "forward_decl_candidates", "recommendations"):
                self.assertIn(key, data, f"Missing key: {key}")

    def test_json_stats_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            h = write_header(Path(tmp), '#include <string>\nclass Foo {};\n')
            proc = run_script(str(h), fmt="json")
            data = json.loads(proc.stdout)
            stats = data["stats"]
            for key in ("total_lines", "include_count", "includes_by_type", "inline_methods", "forward_decl_candidates"):
                self.assertIn(key, stats, f"Missing stats key: {key}")


if __name__ == "__main__":
    unittest.main()
