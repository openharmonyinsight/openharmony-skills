---
name: odk-implement
description: "Use when implementing an approved execution-plan.md Task-by-Task and backfilling code scope. Base layer: AI-assisted, zero plugin dependencies (no TDD/subagent cycles). Use after execution-plan.md approval."
license: MIT
---

# ODK Implement

## Purpose

Use after `execution-plan.md` has been approved. This is the **base layer** command — AI-assisted implementation guided by the plan, with zero plugin dependencies.

## Prerequisites

- Load `using-odk` first.
- `spec.md` exists with numbered ACs.
- `execution-plan.md` exists with Task IDs, AC-Task traceability, file-level scope, and verification commands.
- The user has approved implementation.

## Steps

0. Read `.codespec/changes/<id>/execution-plan.md` Task list and list all Tasks as an explicit inventory before starting implementation. All task types — code modification, test writing, configuration update, and verification — are equally mandatory. No task type may be skipped without explicit user consent.
1. Read the active `.codespec/changes/<id>/spec.md` AC list and `execution-plan.md` 代码范围映射 (Task → file).
2. Read `.codespec/changes/<id>/execution-plan.md` Task list, dependency graph, file scope, and each Task's「任务间接口」（Produces/Consumes）—align cross-task naming and signatures to it.
   Treat the `spec.md` ACs and the execution principles in `execution-plan.md` as authoritative, then proceed in Task order.
3. For each Task (respecting dependency order):
   - Present the Task description and planned file scope.
   - Read only the Task's declared read-only context before editing.
   - **Analyze existing code patterns** for the Task's file scope:
     - Identify the change type (new API, query method, callback, member variable, etc.)
     - Search for similar existing functions — prefer files within the Task's declared file scope first, then widen to the same subsystem/layer
     - Study the conventions those functions follow: call chain layering, naming patterns, error handling, state management, logging/DFX, and interface contracts
     - Record the reference pattern, e.g.: "Call chain: `native_api → NativeEngine → ArkNativeEngine → DFXJSNApi → EcmaVM`" or "Naming: query APIs use `GetXxx()` returning `int32_t` with `napi_status` error code"
     - Follow the same conventions unless the user explicitly approves a deviation
     - If no similar function exists, note "no prior art found" and proceed without a pattern reference
   - Add or run the Task's failing test / evidence check, or document the reproducible evidence gap, before implementation.
   - Implement the code changes within the declared file boundaries.
   - Run the verification command and confirm it matches the Task's expected result.
   - After each Task, update `execution-plan.md` 代码范围映射 with actual files, tests, and commit references.
   - Backfill the Task's `Actual Result` and anti-fake completion evidence.
   - Mark the Task as completed in `execution-plan.md`: change all `- [ ]` checkboxes to `- [x]` in the Task's Steps section. If the Task list table has a `状态` column, update it to `Done`; otherwise add the column first.
4. After all Tasks are attempted, produce an **Execution Summary**:
   - List every Task with status: ✅ Done / ❌ Blocked / ⚠️ Skipped (with reason)
   - If any Task is incomplete, inform the user and do NOT suggest moving to review — wait for user direction
5. If implementation reveals missing ACs or changed scope, pause and update `spec.md` / `execution-plan.md` before continuing.
6. Keep changes within the Task file scope unless the user approves an execution-plan update.

## Output

Report:

- **Execution Summary:** every Task listed with status (✅ Done / ❌ Blocked / ⚠️ Skipped) and reason for any incomplete Tasks
- Tasks completed and status changes written to `execution-plan.md`
- Reference patterns used (architectural conventions followed or "no prior art found")
- Verification results per Task
- Code mapping rows updated in `execution-plan.md` 代码范围映射
- Any deviations from `execution-plan.md` or reference patterns (with justification)

If all Tasks are ✅ Done, suggest next step: run `{{CMD_PREFIX}}review` to generate review records. If any Task is incomplete, do NOT suggest moving to review — report the gaps and wait for user direction.
