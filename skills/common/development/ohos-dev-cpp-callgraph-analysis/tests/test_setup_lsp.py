import importlib.util
import io
import json
import shlex
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "setup_lsp.py"
SPEC = importlib.util.spec_from_file_location("setup_lsp", SCRIPT_PATH)
setup_lsp = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(setup_lsp)


class SetupLspTest(unittest.TestCase):
    def test_filter_compile_database_keeps_only_repo_files(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            oh_root = root / "code"
            repo_root = oh_root / "foundation" / "multimodalinput" / "input"
            repo_root.mkdir(parents=True)
            source = root / "compile_commands.json"
            target = root / "filtered" / "compile_commands.json"
            source.write_text(json.dumps([
                {
                    "directory": str(oh_root / "out" / "rk3568"),
                    "file": "../../foundation/multimodalinput/input/a.cpp",
                    "command": "clang++ a.cpp",
                },
                {
                    "directory": str(oh_root / "out" / "rk3568"),
                    "file": "../../foundation/window/window_manager/b.cpp",
                    "command": "clang++ b.cpp",
                },
            ]))

            count = setup_lsp.filter_compile_database(source, target, repo_root)

            self.assertEqual(count, 1)
            entries = json.loads(target.read_text())
            self.assertEqual(entries[0]["file"], "../../foundation/multimodalinput/input/a.cpp")

    def test_filter_compile_database_supports_same_source_and_target(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo_root = root / "input"
            repo_root.mkdir()
            compdb = root / "compile_commands.json"
            compdb.write_text(json.dumps([{
                "directory": str(root),
                "file": "input/a.cpp",
                "command": "clang++ a.cpp",
            }]))

            count = setup_lsp.filter_compile_database(compdb, compdb, repo_root)

            self.assertEqual(count, 1)
            self.assertEqual(len(json.loads(compdb.read_text())), 1)

    def test_find_clangd_uses_openharmony_prebuilt(self):
        with tempfile.TemporaryDirectory() as td:
            oh_root = Path(td)
            clangd = oh_root / "prebuilts/clang/ohos/linux-x86_64/llvm/bin/clangd"
            clangd.parent.mkdir(parents=True)
            clangd.touch()

            self.assertEqual(setup_lsp.find_clangd(oh_root), clangd)

    def test_first_compile_file_resolves_relative_source(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            compdb = root / "compile_commands.json"
            compdb.write_text(json.dumps([{
                "directory": str(root / "out"),
                "file": "../input/a.cpp",
                "command": "clang++ a.cpp",
            }]))

            self.assertEqual(
                setup_lsp.first_compile_file(compdb),
                (root / "input" / "a.cpp").resolve(),
            )

    def test_line_json_objects_accepts_filtered_one_line_entries(self):
        source = io.StringIO('[\n{"file": "a.cpp", "directory": "/src"},\n'
                             '{"file": "b.cpp", "directory": "/src"}\n]\n')

        entries = list(setup_lsp._line_json_objects(source))

        self.assertEqual([entry["file"] for entry in entries], ["a.cpp", "b.cpp"])

    def test_codex_registration_command_is_explicit_and_tool_neutral(self):
        command = setup_lsp.client_registration_command(
            "codex",
            "ohos-lsp",
            Path("/cache/mcp-language-server"),
            Path("/src/input"),
            Path("/src/prebuilts/clangd"),
            Path("/cache/compdb"),
        )

        self.assertEqual(command[:4], ["codex", "mcp", "add", "ohos-lsp"])
        self.assertIn("--workspace", command)
        self.assertIn("--compile-commands-dir=/cache/compdb", command)

    def test_claude_registration_command_uses_project_scope(self):
        command = setup_lsp.client_registration_command(
            "claude",
            "ohos-lsp",
            Path("/cache/mcp-language-server"),
            Path("/src/input"),
            Path("/src/prebuilts/clangd"),
            Path("/cache/compdb"),
        )

        self.assertEqual(
            command[:6],
            ["claude", "mcp", "add", "--scope", "project", "ohos-lsp"],
        )

    def test_bridge_command_can_be_registered_by_other_mcp_clients(self):
        command = setup_lsp.bridge_command(
            Path("/cache/mcp language server"),
            Path("/src/input"),
            Path("/src/prebuilts/clangd"),
            Path("/cache/compdb"),
        )

        rendered = shlex.join(command)
        self.assertIn("'/cache/mcp language server'", rendered)
        self.assertIn("--workspace /src/input", rendered)
        self.assertIn("--compile-commands-dir=/cache/compdb", rendered)

    def test_auto_clients_only_returns_available_clients(self):
        with patch.object(setup_lsp.shutil, "which", side_effect=lambda name: {
            "codex": "/usr/bin/codex",
            "claude": None,
        }.get(name)):
            self.assertEqual(setup_lsp.resolve_clients(["auto"]), ["codex"])

    def test_go_compatibility_requires_go_1_24(self):
        with patch.object(setup_lsp.subprocess, "run") as run:
            run.return_value.stdout = "go version go1.23.9 linux/amd64"
            self.assertFalse(setup_lsp.go_is_compatible("/usr/bin/go"))

            run.return_value.stdout = "go version go1.24.4 linux/amd64"
            self.assertTrue(setup_lsp.go_is_compatible("/usr/bin/go"))


if __name__ == "__main__":
    unittest.main()
