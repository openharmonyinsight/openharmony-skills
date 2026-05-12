# Taskpool dependency analysis (ArkRuntime)

Registered name: `ohos-issue-arkruntime-taskpool-dependency-analysis`.

## Location

```text
skills/domain/arkruntime/troubleshooting/ohos-issue-arkruntime-taskpool-dependency-analysis/
```

## Contents

- `SKILL.md` — **AI** entry point for assisting **external app developers** with static ArkTS taskpool dependency issues (cycles, illegal edges, notification/cancel paths).
- `references/dependency_reference.md` — data structures, error codes, lifecycle, and notification/cancel details for the static ArkTS implementation; loaded when deep detail is needed.
- `evals/evals.json` — seed prompts and expected behaviors for skill evaluation or regression checks.

## Scope

Domain skill for ArkRuntime taskpool `addDependency` / `removeDependency` behavior. Not a substitute for generic concurrency or ArkTS syntax skills.

**Primary reader:** the coding agent. **End user:** external application developer. Fixes are usually in app code; `arkcompiler_runtime_core` paths in `SKILL.md` are for **read-only** corroboration (same layout as upstream).
