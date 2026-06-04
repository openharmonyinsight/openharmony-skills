import importlib.util
import io
import subprocess
import sys
import unittest
from collections import defaultdict
from contextlib import redirect_stderr, redirect_stdout
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

    def test_keyword_hint_warns_it_does_not_validate_state_propagation(self):
        graph = defaultdict(set)
        graph["RootFunc"] = {("direct", "ChildFunc")}

        out = io.StringIO()
        with redirect_stdout(out):
            ohos_callgraph.build_call_tree(
                "RootFunc", [graph], [], {}, "/fake/llvm",
                max_depth=1, check_keyword="groupId"
            )

        text = out.getvalue()
        self.assertIn("仅检查 demangled 函数名", text)
        self.assertIn("不能验证参数、调用实参、成员访问或状态传递", text)

    def test_reverse_output_states_vtable_dlopen_are_not_reversed(self):
        graph = defaultdict(set)
        graph["CallerFunc"] = {("direct", "TargetFunc")}

        out = io.StringIO()
        with redirect_stdout(out):
            ohos_callgraph.build_call_tree(
                "TargetFunc", [graph], [{"CallerFunc": {"_ZTSIface"}}],
                {}, "/fake/llvm", max_depth=1, reverse=True
            )

        text = out.getvalue()
        self.assertIn("Reverse 说明", text)
        self.assertIn("只反查 direct call", text)
        self.assertIn("不反查 vtable/dlopen 候选边", text)

    def test_extract_callgraph_reports_tool_failure(self):
        failed = ohos_callgraph.CommandResult(
            cmd=["opt"], returncode=1, stderr="not a bitcode file"
        )

        with patch.object(ohos_callgraph, "run", return_value=failed):
            graph, error = ohos_callgraph.extract_callgraph("/fake/llvm", "/tmp/a.o")

        self.assertFalse(graph)
        self.assertIn("not a bitcode file", error)

    def test_main_rejects_missing_explicit_context_before_scanning_workspace(self):
        err = io.StringIO()
        with patch.object(sys, "argv", ["ohos_callgraph.py", "TargetFunc"]):
            with redirect_stderr(err), self.assertRaises(SystemExit) as cm:
                ohos_callgraph.main()

        self.assertNotEqual(cm.exception.code, 0)
        self.assertIn("--oh-root", err.getvalue())
        self.assertIn("--repo", err.getvalue())


if __name__ == "__main__":
    unittest.main()
