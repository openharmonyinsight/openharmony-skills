import importlib.util
import os
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
_spec = importlib.util.spec_from_file_location(
    "run_xts_test", os.path.join(SKILL_ROOT, "scripts", "run_xts_test.py"))
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


class TestNameValidationTest(unittest.TestCase):
    def test_valid_names_accepted(self):
        for name in ["ActsAceEtsModuleImageTextTextTest", "ActsUiTest", "A_b_c_123"]:
            self.assertEqual(mod._validate_test_name(name), name)

    def test_injection_attempts_rejected(self):
        bad_names = [
            "foo; calc",
            "foo && calc",
            "foo | bar",
            "foo`calc`",
            "foo$(calc)",
            'foo"; calc; "',
            "foo'calc",
            "foo\nbar",
            "../foo",
            "",
        ]
        for bad in bad_names:
            with self.assertRaises(ValueError, msg=f"should reject: {bad!r}"):
                mod._validate_test_name(bad)


class WinPathValidationTest(unittest.TestCase):
    def test_valid_paths_accepted(self):
        for p in [r"D:\acts_suite\acts", r"C:\work\xts suite"]:
            self.assertEqual(mod._validate_win_path(p), p)

    def test_unsafe_paths_rejected(self):
        bad_paths = [
            r"D:\x; calc",
            r"D:\x$(calc)",
            "D:\\x`calc`",
            r"D:\x|y",
            r"D:\x>y",
            "",
            "relative/path",
            r"\\server\share",
        ]
        for bad in bad_paths:
            with self.assertRaises(ValueError, msg=f"should reject: {bad!r}"):
                mod._validate_win_path(bad)


if __name__ == "__main__":
    unittest.main()
