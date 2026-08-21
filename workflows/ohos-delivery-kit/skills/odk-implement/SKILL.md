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
   - **API 声明文件修改（条件触发 — Task-1）**：如果当前是 plan 中的第一个 Task（API 声明文件 Task-1）且 `API/SDK` = 是：
     - 读取 `spec.md` 的 `## API 规格定义`（完整规格表：命名、入参、返回值、权限、@syscap、@since、错误码、支持标记等）
     - 获取 API 声明仓库路径（spec 阶段过程信息不落盘）：若本会话已有 spec 阶段确认的 `interface_sdk-js` / `interface_sdk_c` 本地路径，直接使用；否则询问开发者提供（不一定是绝对路径，只要能定位到即可）
     - 阅读仓库中与变更最相关的既有声明文件（≤10 个），提取格式规范（版权头、JSDoc 结构、命名风格），作为修改声明文件的参照
     - 参照既有声明文件的格式规范，根据规格表在 API 仓库中修改或新增声明文件：
       - ArkTS 声明写入 `interface_sdk-js/api/@ohos.{kit}.{module}.d.ts`
       - C 声明写入 `interface_sdk_c/api/{kit}/{module}.h`
       - 声明文件须包含 Apache 2.0 版权声明头和完整 JSDoc 注释
     - **调用 oh-api-definition 质量检查（必选，阻塞）**：
       - 检查 oh-api-definition 是否可用（由开发者自行获取并安装）
       - 如不可用，提示开发者安装后继续
       - 对新修改的声明文件进行格式、命名、注释、语法检查
       - 不通过时必须修改直到所有检查项通过，不得跳过
     - **生成 diff 文件**：质量检查通过后，生成声明文件修改前后的 diff 文件，归档到 `.codespec/changes/<id>/` 目录下，作为变更证据
   - Run the verification command and confirm it matches the Task's expected result.
   - After each Task, update `execution-plan.md` 代码范围映射 with actual files, tests, and commit references.
   - Backfill the Task's `Actual Result` and anti-fake completion evidence.
   - Mark the Task as completed in `execution-plan.md`: change all `- [ ]` checkboxes to `- [x]` in the Task's Steps section. If the Task list table has a `状态` column, update it to `Done`; otherwise add the column first.
4. After all Tasks are attempted, produce an **Execution Summary**:
   - List every Task with status: ✅ Done / ❌ Blocked / ⚠️ Skipped (with reason)
   - If any Task is incomplete, inform the user and do NOT suggest moving to review — wait for user direction
5. If implementation reveals missing ACs or changed scope, pause and update `spec.md` / `execution-plan.md` before continuing.
6. Keep changes within the Task file scope unless the user approves an execution-plan update.
7. When any `资源开销审视` dimension is `required` (`contracts/artifacts.yaml#resource_contract`), complete subsystem measurement/evidence Tasks and the business-repo `odk_resource_gate` (commonly under `evidence/resource/`).

## Output

Report:

- **Execution Summary:** every Task listed with status (✅ Done / ❌ Blocked / ⚠️ Skipped) and reason for any incomplete Tasks
- Tasks completed and status changes written to `execution-plan.md`
- Reference patterns used (architectural conventions followed or "no prior art found")
- Verification results per Task
- Code mapping rows updated in `execution-plan.md` 代码范围映射
- Any deviations from `execution-plan.md` or reference patterns (with justification)

If all Tasks are ✅ Done, suggest next step: run `{{CMD_PREFIX}}review` to generate review records. If any Task is incomplete, do NOT suggest moving to review — report the gaps and wait for user direction.
