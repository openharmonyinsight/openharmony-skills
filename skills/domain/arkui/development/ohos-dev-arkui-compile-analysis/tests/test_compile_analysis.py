#!/usr/bin/env python3
"""Tests for compile-analysis scripts: parse_ii.py and get_compile_command.py."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
PARSE_II_SCRIPT = SKILL_DIR / "scripts" / "parse_ii.py"
GET_COMPILE_SCRIPT = SKILL_DIR / "scripts" / "get_compile_command.py"


# ---------------------------------------------------------------------------
# parse_ii.py tests
# ---------------------------------------------------------------------------


def write_ii_file(tmp: Path, content: str, name: str = "test.ii") -> Path:
    f = tmp / name
    f.write_text(content, encoding="utf-8")
    return f


def run_parse_ii(ii_file: str, output: str | None = None) -> subprocess.CompletedProcess[str]:
    args = [sys.executable, str(PARSE_II_SCRIPT), ii_file]
    if output:
        args.extend(["--output", output])
    return subprocess.run(args, capture_output=True, text=True)


class ParseIIBasicTest(unittest.TestCase):
    """Test basic .ii file parsing."""

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            ii = write_ii_file(Path(tmp), "")
            proc = run_parse_ii(str(ii))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("Header dependency tree:", proc.stdout)

    def test_single_include(self):
        with tempfile.TemporaryDirectory() as tmp:
            ii = write_ii_file(Path(tmp), (
                '# 1 "test.cpp"\n'
                '# 1 "foundation/arkui/ace_engine/frameworks/core/test.h" 1\n'
                '// content\n'
                '# 2 "test.cpp" 2\n'
            ))
            proc = run_parse_ii(str(ii))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("foundation/arkui/ace_engine", proc.stdout)

    def test_nested_includes(self):
        with tempfile.TemporaryDirectory() as tmp:
            ii = write_ii_file(Path(tmp), (
                '# 1 "test.cpp"\n'
                '# 1 "foundation/arkui/ace_engine/a.h" 1\n'
                '# 1 "foundation/arkui/ace_engine/b.h" 1\n'
                '// b content\n'
                '# 2 "foundation/arkui/ace_engine/a.h" 2\n'
                '// a content\n'
                '# 2 "test.cpp" 2\n'
            ))
            proc = run_parse_ii(str(ii))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("a.h", proc.stdout)
            self.assertIn("b.h", proc.stdout)

    def test_system_headers_filtered(self):
        """System headers (without foundation/arkui/) should not appear."""
        with tempfile.TemporaryDirectory() as tmp:
            ii = write_ii_file(Path(tmp), (
                '# 1 "test.cpp"\n'
                '# 1 "/usr/include/stdio.h" 1 3\n'
                '// stdio content\n'
                '# 2 "test.cpp" 2\n'
                '# 1 "foundation/arkui/ace_engine/core/test.h" 1\n'
                '// test content\n'
                '# 2 "test.cpp" 2\n'
            ))
            proc = run_parse_ii(str(ii))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("test.h", proc.stdout)
            # stdio.h is a system header and should not appear in filtered output
            self.assertNotIn("stdio.h", proc.stdout)

    def test_output_file_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            ii = write_ii_file(tmpdir, (
                '# 1 "test.cpp"\n'
                '# 1 "foundation/arkui/ace_engine/test.h" 1\n'
                '# 2 "test.cpp" 2\n'
            ))
            output = str(tmpdir / "dep_tree.txt")
            proc = run_parse_ii(str(ii), output=output)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(os.path.exists(output))
            content = Path(output).read_text(encoding="utf-8")
            self.assertIn("test.h", content)


class ParseIIEdgeCasesTest(unittest.TestCase):
    """Test edge cases in .ii parsing."""

    def test_nonexistent_file(self):
        proc = run_parse_ii("/nonexistent/file.ii")
        self.assertNotEqual(proc.returncode, 0)

    def test_include_guard_handling(self):
        """Re-entering the same file (include guard) should be handled."""
        with tempfile.TemporaryDirectory() as tmp:
            ii = write_ii_file(Path(tmp), (
                '# 1 "test.cpp"\n'
                '# 1 "foundation/arkui/ace_engine/a.h" 1\n'
                '# 1 "foundation/arkui/ace_engine/a.h" 1\n'
                '# 2 "foundation/arkui/ace_engine/a.h" 2\n'
                '# 2 "foundation/arkui/ace_engine/a.h" 2\n'
                '# 2 "test.cpp" 2\n'
            ))
            proc = run_parse_ii(str(ii))
            self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_deep_nesting(self):
        """Deep include nesting should be handled without errors."""
        lines = ['# 1 "test.cpp"\n']
        for i in range(20):
            lines.append(f'# 1 "foundation/arkui/ace_engine/depth_{i}.h" 1\n')
        for i in range(19, -1, -1):
            lines.append(f'# 2 "foundation/arkui/ace_engine/depth_{i}.h" 2\n')
        lines.append('# 2 "test.cpp" 2\n')
        with tempfile.TemporaryDirectory() as tmp:
            ii = write_ii_file(Path(tmp), "".join(lines))
            proc = run_parse_ii(str(ii))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("depth_0.h", proc.stdout)
            self.assertIn("depth_19.h", proc.stdout)


# ---------------------------------------------------------------------------
# get_compile_command.py unit tests (without real build tree)
# ---------------------------------------------------------------------------


class GetCompileCommandArgParseTest(unittest.TestCase):
    """Test get_compile_command.py argument handling."""

    def test_no_args_shows_usage(self):
        proc = subprocess.run(
            [sys.executable, str(GET_COMPILE_SCRIPT)],
            capture_output=True, text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        # Script prints Chinese usage message (用法 = usage)
        output = proc.stdout + proc.stderr
        self.assertTrue(
            "usage" in output.lower() or "用法" in output,
            f"Expected usage info in output, got: {output[:200]}"
        )

    def test_missing_out_dir(self):
        """Non-existent out directory should report error."""
        proc = subprocess.run(
            [sys.executable, str(GET_COMPILE_SCRIPT), "test.cpp", "/nonexistent/out"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(proc.returncode, 0)


class GetCompileCommandEnhancedTest(unittest.TestCase):
    """Test enhanced command generation logic."""

    def test_enhanced_removes_ccache(self):
        """generate_enhanced_command should remove ccache from command."""
        # Import the module directly to test the function
        sys.path.insert(0, str(SKILL_DIR / "scripts"))
        from get_compile_command import generate_enhanced_command

        cmd = (
            "/usr/bin/ccache ../../prebuilts/clang/ohos/linux-x86_64/llvm/bin/clang++ "
            "-c some_file.cpp -o obj/some_file.o"
        )
        result = generate_enhanced_command(cmd, "some_file.cpp")
        if result:
            self.assertNotIn("ccache", result)

    def test_enhanced_adds_save_temps(self):
        """generate_enhanced_command should add -save-temps=obj."""
        sys.path.insert(0, str(SKILL_DIR / "scripts"))
        from get_compile_command import generate_enhanced_command

        cmd = (
            "../../prebuilts/clang/ohos/linux-x86_64/llvm/bin/clang++ "
            "-c some_file.cpp -o obj/some_file.o"
        )
        result = generate_enhanced_command(cmd, "some_file.cpp")
        if result:
            self.assertIn("-save-temps=obj", result)

    def test_enhanced_returns_none_for_invalid_command(self):
        """generate_enhanced_command should return None for invalid format."""
        sys.path.insert(0, str(SKILL_DIR / "scripts"))
        from get_compile_command import generate_enhanced_command

        result = generate_enhanced_command("not a valid command", "test.cpp")
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# get_compile_command.py — ninja file parsing tests
# ---------------------------------------------------------------------------


class GetCompileCommandNinjaParsingTest(unittest.TestCase):
    """Test ninja file parsing with synthetic ninja files."""

    def test_parse_cxx_rule(self):
        sys.path.insert(0, str(SKILL_DIR / "scripts"))
        from get_compile_command import parse_cxx_rule

        with tempfile.TemporaryDirectory() as tmp:
            toolchain = Path(tmp) / "toolchain.ninja"
            toolchain.write_text(
                "rule cxx\n"
                "  command = clang++ ${defines} ${includes} ${cflags} ${cflags_cc} -c ${in} -o ${out}\n"
            )
            result = parse_cxx_rule(str(toolchain))
            self.assertIsNotNone(result)
            self.assertIn("clang++", result)
            self.assertIn("${in}", result)
            self.assertIn("${out}", result)

    def test_parse_variables(self):
        sys.path.insert(0, str(SKILL_DIR / "scripts"))
        from get_compile_command import parse_variables

        with tempfile.TemporaryDirectory() as tmp:
            ninja = Path(tmp) / "test.ninja"
            ninja.write_text(
                "defines = -DFOO -DBAR\n"
                "include_dirs = -Ifoo -Ibar\n"
                "cflags = -Wall\n"
                "cflags_cc = -std=c++17\n"
                "\n"
                "build obj/test.o: cxx test.cpp\n"
            )
            result = parse_variables(str(ninja))
            self.assertIn("defines", result)
            self.assertIn("include_dirs", result)
            self.assertEqual(result["cflags"], "-Wall")
            self.assertEqual(result["cflags_cc"], "-std=c++17")

    def test_expand_variables(self):
        sys.path.insert(0, str(SKILL_DIR / "scripts"))
        from get_compile_command import expand_variables

        template = "clang++ ${defines} -c ${in} -o ${out}"
        variables = {"defines": "-DFOO"}
        result = expand_variables(template, variables, "obj/test.o", "test.cpp")
        self.assertIn("-DFOO", result)
        self.assertIn("test.cpp", result)
        self.assertIn("obj/test.o", result)


if __name__ == "__main__":
    unittest.main()
