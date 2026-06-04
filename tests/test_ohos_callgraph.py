import importlib.util
import io
import subprocess
import sys
import unittest
from collections import defaultdict
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "skills" / "ohos-callgraph" / "ohos_callgraph.py"
SPEC = importlib.util.spec_from_file_location("ohos_callgraph", SCRIPT_PATH)
ohos_callgraph = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ohos_callgraph)


class OhosCallgraphTest(unittest.TestCase):
    def test_run_reports_nonzero_exit(self):
        result = ohos_callgraph.run(["false"])

        self.assertFalse(result.ok)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(result.timed_out)
        self.assertFalse(result.missing_tool)

    def test_run_reports_timeout(self):
        with patch.object(subprocess, "run", side_effect=subprocess.TimeoutExpired(["cmd"], 1)):
            result = ohos_callgraph.run(["cmd"], timeout=1)

        self.assertFalse(result.ok)
        self.assertTrue(result.timed_out)
        self.assertIn("timed out", result.stderr)

    def test_reverse_tree_recurses_as_reverse(self):
        graph = defaultdict(set)
        graph["_ZA"] = {("direct", "_ZB")}
        graph["_ZB"] = {("direct", "_ZC")}
        demangled = {
            "_ZA": "A()",
            "_ZB": "B()",
            "_ZC": "C()",
        }
        reverse_graph = defaultdict(set)
        for caller, callees in graph.items():
            for _, callee in callees:
                reverse_graph[callee].add(caller)

        out = io.StringIO()
        with redirect_stdout(out):
            ohos_callgraph._print_tree(
                "_ZC", reverse_graph, {}, demangled, {}, "/fake/llvm",
                max_depth=3, depth=0, visited=set(), is_reverse=True
            )

        text = out.getvalue()
        self.assertIn("B", text)
        self.assertIn("A", text)

    def test_check_isolation_marks_function_name_only(self):
        graph = defaultdict(set)
        graph["_ZRoot"] = {("direct", "_ZHandleMouseEvent")}
        graph["_ZHandleMouseEvent"] = {("direct", "_ZDispatchGroupId")}
        demangled = {
            "_ZRoot": "Root()",
            "_ZHandleMouseEvent": "OHOS::MMI::HandleMouseEvent(int)",
            "_ZDispatchGroupId": "OHOS::MMI::DispatchGroupId()",
        }

        out = io.StringIO()
        with redirect_stdout(out):
            ohos_callgraph._print_tree(
                "_ZRoot", graph, {}, demangled, {}, "/fake/llvm",
                max_depth=2, depth=0, visited=set(), check_keyword="groupId"
            )

        text = out.getvalue()
        self.assertIn("HandleMouseEvent ⚡", text)
        self.assertIn("DispatchGroupId ✅", text)


if __name__ == "__main__":
    unittest.main()
