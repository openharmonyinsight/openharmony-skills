# OpenHarmony C++ Callgraph Analysis Skill

This skill is registered as `ohos-dev-cpp-callgraph-analysis` and lives under the common development namespace:

```text
skills/common/development/ohos-dev-cpp-callgraph-analysis/
```

## Scope

Use this skill for cross-subsystem OpenHarmony C++ call-chain completeness analysis. It provides an evidence workflow for direct calls, virtual dispatch, callbacks, IPC, generated code, and dynamically loaded implementations.

## Runtime Files

- `SKILL.md` is the agent entry point.
- `ohos_callgraph.py` is an optional candidate-edge discovery helper. Its output is not completeness proof.
- `scripts/setup_lsp.py` prepares a repository-scoped clangd MCP service for supported agent clients.
- `evals/` contains seed prompts and expected behaviors for skill evaluation.
- `tests/` contains helper regression tests.

## Verification

Run:

```bash
python3 -m unittest discover \
  -s skills/common/development/ohos-dev-cpp-callgraph-analysis/tests \
  -p 'test_*.py'
```
