#!/usr/bin/env python3
"""
Evaluation test suite for arkuix-framework-api-adapter scripts.

Tests 3 scripts against fixture data:
  - dts_analyzer.py: @crossplatform coverage analysis
  - architecture_analyzer.py: code composition and mode recommendation
  - code_generator.py: config file generation (dry-run mode)

Run: python3 tests/test_scripts.py
"""

import json
import os
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class TestDTSAnalyzer(unittest.TestCase):
    """Category A1-A4: dts_analyzer.py functional tests"""

    def setUp(self):
        self.script = SCRIPTS_DIR / "dts_analyzer.py"

    def _run_analyzer(self, dts_file):
        result = subprocess.run(
            [sys.executable, str(self.script), str(dts_file), "--json"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            self.fail(f"dts_analyzer failed: {result.stderr}")
        return json.loads(result.stdout)

    def test_a01_simple_settings_with_crossplatform(self):
        """A01: Settings .d.ts with partial @crossplatform coverage"""
        analysis = self._run_analyzer(FIXTURES_DIR / "dts" / "simple_settings.d.ts")

        self.assertGreater(analysis["total_interfaces"], 0,
            "Should detect interfaces in non-empty .d.ts")
        self.assertGreater(analysis["adapted_interfaces"], 0,
            "Should detect @crossplatform-annotated interfaces")
        self.assertGreater(analysis["coverage_percent"], 0,
            "Coverage should be >0% when @crossplatform tags exist")
        self.assertIn("needs_adaptation", analysis)
        self.assertIn("by_category", analysis)

    def test_a02_no_crossplatform(self):
        """A02: Bluetooth .d.ts with zero @crossplatform coverage"""
        analysis = self._run_analyzer(FIXTURES_DIR / "dts" / "no_crossplatform.d.ts")

        self.assertGreater(analysis["total_interfaces"], 0,
            "Should detect interfaces even without @crossplatform")
        self.assertEqual(analysis["adapted_interfaces"], 0,
            "No interfaces should be adapted")
        self.assertEqual(analysis["coverage_percent"], 0.0,
            "Coverage should be 0%")
        self.assertEqual(len(analysis["needs_adaptation_list"]),
                         analysis["total_interfaces"],
            "All interfaces should be in needs_adaptation_list")

    def test_a03_partial_crossplatform(self):
        """A03: HTTP .d.ts with partial @crossplatform (mixed coverage)"""
        analysis = self._run_analyzer(FIXTURES_DIR / "dts" / "partial_crossplatform.d.ts")

        self.assertGreater(analysis["total_interfaces"], 4,
            "Should detect all declaration types (namespace, class, interface, enum, type, const)")
        self.assertGreater(analysis["adapted_interfaces"], 0,
            "Should detect @crossplatform interfaces")
        self.assertGreater(analysis["needs_adaptation"], 0,
            "Should detect non-adapted interfaces")
        self.assertGreater(analysis["coverage_percent"], 0,
            "Partial coverage should be >0%")
        self.assertLess(analysis["coverage_percent"], 100,
            "Partial coverage should be <100%")

    def test_a04_empty_dts(self):
        """A04: Empty .d.ts edge case - graceful handling"""
        analysis = self._run_analyzer(FIXTURES_DIR / "dts" / "empty.d.ts")

        self.assertEqual(analysis["total_interfaces"], 0,
            "Empty .d.ts should have 0 interfaces")
        self.assertEqual(analysis["coverage_percent"], 0,
            "Empty .d.ts coverage should be 0%")
        self.assertEqual(len(analysis["needs_adaptation_list"]), 0,
            "No interfaces needing adaptation")

    def test_a05_nonexistent_file(self):
        """A05: Non-existent file - error handling"""
        result = subprocess.run(
            [sys.executable, str(self.script), "/nonexistent/file.d.ts", "--json"],
            capture_output=True, text=True
        )
        self.assertNotEqual(result.returncode, 0,
            "Should exit with non-zero for missing file")


class TestArchitectureAnalyzer(unittest.TestCase):
    """Category A6-A8: architecture_analyzer.py functional tests"""

    def setUp(self):
        self.script = SCRIPTS_DIR / "architecture_analyzer.py"

    def _run_analyzer(self, module_path):
        result = subprocess.run(
            [sys.executable, str(self.script), str(module_path), "--json"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            self.fail(f"architecture_analyzer failed: {result.stderr}")
        return json.loads(result.stdout)

    def test_a06_pure_cpp_module(self):
        """A06: Pure C++ module (preferences) - should recommend OHOS Reuse"""
        analysis = self._run_analyzer(FIXTURES_DIR / "modules" / "pure_cpp")

        self.assertGreater(analysis["total_lines"], 0)
        self.assertGreater(analysis["platform_independence_percent"], 80,
            "Pure C++ module should have >80% platform independence")
        self.assertIn("OHOS Reuse", analysis["recommendation"],
            "Should recommend OHOS Reuse for pure C++ module")

    def test_a07_platform_heavy_module(self):
        """A07: Platform-heavy module (bluetooth) - should recommend Independent"""
        analysis = self._run_analyzer(FIXTURES_DIR / "modules" / "platform_heavy")

        self.assertGreater(analysis["total_lines"], 0)
        self.assertGreater(analysis["platform_specific_lines"], 0,
            "Should detect platform-specific code")
        rec_lower = analysis["recommendation"].lower()
        self.assertTrue(
            "independent" in rec_lower or "hybrid" in rec_lower,
            f"Should recommend Independent or Hybrid for platform-heavy module, got: {analysis['recommendation']}"
        )

    def test_a08_hybrid_module(self):
        """A08: Hybrid module (location) - should detect mixed composition"""
        analysis = self._run_analyzer(FIXTURES_DIR / "modules" / "hybrid")

        self.assertGreater(analysis["total_lines"], 0)
        self.assertGreater(analysis["business_logic_lines"], 0,
            "Should detect shared business logic")
        self.assertGreater(analysis["platform_specific_lines"], 0,
            "Should detect platform-specific code in android/ and ios/")

    def test_a09_nonexistent_path(self):
        """A09: Non-existent module path - error handling"""
        result = subprocess.run(
            [sys.executable, str(self.script), "/nonexistent/path", "--json"],
            capture_output=True, text=True
        )
        self.assertNotEqual(result.returncode, 0,
            "Should exit with non-zero for missing path")


class TestCodeGenerator(unittest.TestCase):
    """Category A10: code_generator.py validate mode test"""

    def setUp(self):
        self.script = SCRIPTS_DIR / "code_generator.py"

    def test_a10_validate_missing_project(self):
        """A10: code_generator validate in directory without plugins/ - error handling"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, str(self.script), "test/module", "test_repo", "--validate"],
                capture_output=True, text=True,
                cwd=tmpdir
            )
            self.assertNotEqual(result.returncode, 0,
                "Should fail when no project root (plugins/) found")


def run_tests():
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    total = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total - failures - errors
    print(f"Results: {passed}/{total} passed, {failures} failures, {errors} errors")
    print("=" * 70)

    return 0 if failures == 0 and errors == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
