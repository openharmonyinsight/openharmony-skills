import importlib.util
import json
import os
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
_spec = importlib.util.spec_from_file_location(
    "parse_api_diff", os.path.join(SKILL_ROOT, "scripts", "parse_api_diff.py"))
pad = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pad)

EVAL_JSON = os.path.join(SKILL_ROOT, "evals", "api_diff_pr33680.json")


class SubsystemFilterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(EVAL_JSON, encoding="utf-8") as fp:
            cls.diffs = json.load(fp)

    def test_no_filter_keeps_all(self):
        entries = [pad.build_api_entry(d, "ets1.1") for d in self.diffs]
        kept = [e for e in entries if pad.passes_filter(e, None, None, None)]
        self.assertEqual(len(kept), len(self.diffs))

    def test_subsystem_filter_keeps_attributed_entries(self):
        entries = [pad.build_api_entry(d, "ets1.1", "testfwk") for d in self.diffs]
        kept = [e for e in entries if pad.passes_filter(e, "testfwk", None, None)]
        self.assertEqual(len(kept), len(self.diffs))
        self.assertTrue(all(e["subsystem"] == "testfwk" for e in kept))


if __name__ == "__main__":
    unittest.main()