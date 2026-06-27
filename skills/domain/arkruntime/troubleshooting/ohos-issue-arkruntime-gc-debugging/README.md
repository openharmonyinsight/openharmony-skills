# GC Debugging (ArkRuntime)

Registered name: `ohos-issue-arkruntime-gc-debugging`.

## Location

```text
skills/domain/arkruntime/troubleshooting/ohos-issue-arkruntime-gc-debugging/
```

## Contents

- `SKILL.md` — AI entry point for diagnosing and fixing GC-related bugs in ArkCompiler runtime (mark/sweep crashes, missing write barriers, dangling pointers, AfterGC verify failures, long STW pauses, weak ref issues).
- `SKILL.zh-CN.md` — Chinese version of the skill instructions.
- `LICENSE` — Apache License 2.0.

## Scope

Domain skill for ArkRuntime GC debugging. Covers mark/sweep phase crashes, write barrier violations, visitor coverage gaps, AfterGC verification failures, STW pause regressions, and weak reference staleness. Not a substitute for general memory debugging or allocator skills.

**Primary reader:** the coding agent. **End user:** runtime developer working under `arkcompiler/ets_runtime`.
