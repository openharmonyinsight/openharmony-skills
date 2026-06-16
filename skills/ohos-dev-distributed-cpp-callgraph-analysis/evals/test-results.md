# Test Results

Date: 2026-06-07

Scope:

- Verify that `ohos-dev-distributed-cpp-callgraph-analysis` treats LSP/source evidence as the primary path.
- Verify that `ohos_callgraph.py` is documented as an optional artifact fallback rather than a parallel completeness layer.
- Verify helper and LSP setup regression tests after the documentation, hook-boundary, and eval update.

Commands:

```bash
python3 -m unittest discover -s skills/ohos-dev-distributed-cpp-callgraph-analysis/tests -v
python3 -m py_compile skills/ohos-dev-distributed-cpp-callgraph-analysis/ohos_callgraph.py skills/ohos-dev-distributed-cpp-callgraph-analysis/scripts/setup_lsp.py
python3 -m json.tool skills/ohos-dev-distributed-cpp-callgraph-analysis/evals/evals.json
git diff --check
```

Results:

| Check | Result |
| --- | --- |
| Unit tests | Passed: 22/22 |
| Python compile | Passed |
| Eval JSON syntax | Passed |
| Whitespace diff check | Passed |

Functional result:

- LSP/clangd is now the documented primary path when it has the correct OpenHarmony compile context.
- `ohos_callgraph.py` is only required when LSP/source/build evidence leaves an unexplained edge, artifact-level candidate confirmation is useful, or LSP is unavailable/incomplete.
- Helper output remains candidate evidence only and cannot prove parameter propagation, callback flow, IPC dispatch, virtual runtime targets, or dlopen/dlsym completeness.
- `--install-hook` is documented and tested as Claude PreToolUse support only; Codex and other MCP clients use the tool-neutral bridge plus manual compile database fix.
