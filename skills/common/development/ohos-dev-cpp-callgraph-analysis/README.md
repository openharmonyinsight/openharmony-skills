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
- `evals/` contains seed prompts and expected behaviors for skill evaluation.

## Verification

Repository-level regression tests live in `tests/test_ohos_callgraph.py`.
