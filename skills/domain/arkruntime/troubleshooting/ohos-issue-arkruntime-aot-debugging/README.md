# ohos-issue-arkruntime-aot-debugging

Registered name: `ohos-issue-arkruntime-aot-debugging`.

Repository placement:

```text
skills/domain/arkruntime/troubleshooting/ohos-issue-arkruntime-aot-debugging/
```

This skill supports debugging OpenHarmony ArkRuntime AOT issues across launch, artifact lifecycle, `ark_aot` startup, PAOC compile crashes, profile/PGO behavior, runtime load/link, and compiled-code execution semantics.

It is intentionally not an AOT encyclopedia. It is a troubleshooting workflow that forces phase classification, evidence alignment, root-cause hypothesis separation, minimal fix direction, and validation planning.

## Scope

Use it for:

- `compiler_service` / BMS / installd AOT launch and argument failures.
- dynamic/static/hybrid AOT mode selection.
- `.an` artifact generation, reuse, overwrite, update cleanup, and shared HSP host-private behavior.
- `ark_aot` runtime initialization crashes before compilation.
- PAOC method filtering, PGO/AP, branch-counter, inline-cache, and parallel AOT memory issues.
- AOT file loading/linking and proof that compiled code executed.
- AOT crash, deopt, throw/fallback, bytecode-machine-code correlation, and execution semantics.

Do not use it as a generic OpenHarmony build analyzer, generic C++ debugger, or generic runtime development planner unless the AOT path is central to the issue.

## Contents

- `SKILL.md`: main Agent workflow and trigger metadata.
- `references/`: phase-specific debugging notes for launch, artifact lifecycle, startup, PAOC compile crashes, profile/PGO, runtime link, execution semantics, and build/config gating.
- `evals/evals.json`: seed evaluation prompts for representative AOT debugging scenarios.
- `agents/openai.yaml`: UI-facing skill metadata.
