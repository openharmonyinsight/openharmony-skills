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

0. Read `codespec/changes/<repo-name>/<req-id>/execution-plan.md` Task list and list all Tasks as an explicit inventory before starting implementation. All task types — code modification, test writing, configuration update, and verification — are equally mandatory. No task type may be skipped without explicit user consent.
1. Read the active `codespec/changes/<repo-name>/<req-id>/spec.md` AC list and `execution-plan.md` 代码范围映射 (Task → file).
2. Read `codespec/changes/<repo-name>/<req-id>/execution-plan.md` Task list, dependency graph, file scope, and each Task's「任务间接口」（Produces/Consumes）—align cross-task naming and signatures to it.
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
     - 读取 `spec.md` 的 `## API 规格定义`（`### 公共规格属性` + 逐 API 的 `#### API: <完整签名>` 子节，含各 API 的规格表、API 描述三要素+五要素、设备行为差异），作为修改声明文件的精确蓝图
     - 获取 API 声明仓库路径（spec 阶段过程信息不落盘）：若本会话已有 spec 阶段确认的 `interface_sdk-js` / `interface_sdk_c` 本地路径，直接使用；否则询问开发者提供（不一定是绝对路径，只要能定位到即可）
     - **切分支（必须）**：API 声明仓库通常被多个需求共享，必须在修改声明文件前切出专用分支，避免多个需求的改动互相覆盖、diff 混淆。分支名建议关联需求编号，如 `feature/REQ-12345-arkui-focus`；询问开发者确认分支名或由开发者手动切好后告知分支名
     - **阅读仓库根目录的 `AGENTS.md`**：学习该仓库的 API 设计规范、命名约定、目录结构约定、声明文件格式要求等知识，作为修改声明文件的参照。AGENTS.md 中的内容与既有声明文件的实际格式共同构成格式参考，二者冲突时以 AGENTS.md 为准。若 AGENTS.md 不存在，退回仅参照既有声明文件格式（降级模式）；若未引用声明注释规范，参照既有声明文件的 注释风格
     - 阅读仓库中与变更最相关的既有声明文件（≤10 个），提取格式规范（版权头、注释结构、命名风格），作为修改声明文件的参照
     - 参照既有声明文件的格式规范，根据规格表在 API 仓库中修改或新增声明文件：
       - ArkTS 声明写入 API 声明仓库中对应的声明文件目录（参照仓库既有目录结构和命名约定）
       - C 声明写入 API 声明仓库中对应的声明文件目录（参照仓库既有目录结构和命名约定）
       - 声明文件须包含 Apache 2.0 版权声明头和完整声明注释（ArkTS 为 JSDoc，C 为 Doxygen 或仓库既有注释规范）
     - **按需调用 oh-api-definition 质量检查（可选，不阻塞）**：
       - 若开发环境已提供 oh-api-definition，则对新修改的声明文件执行其格式、命名、注释和语法检查；发现问题时修复后重跑
       - 若工具不可用时在 Task `Actual Result` 记录未执行并继续，不要求安装，也不得因此阻塞 Task-1
    - **生成声明注释双语 diff（英文 + 中文）**：完成适用的质量检查后，基于同一修改前基线生成两份 diff，归档到 `codespec/changes/<repo-name>/<req-id>/evidence/` 目录下，作为变更证据：
      - **英文声明注释 diff**（文件名固定为 `task1-api-declaration-en.diff`）：声明文件的实际修改内容，声明注释（ArkTS 为 JSDoc，C 为 Doxygen 或仓库既有注释规范）使用英文——这是提交到 API 声明仓库的版本
      - **中文声明注释 diff**（文件名固定为 `task1-api-declaration-zh.diff`）：签名、代码、版权头与标记（`@syscap`/`@since`/`@kit`/`@permission` 等）与英文版完全一致，仅将声明注释的描述正文改为中文；中文内容以 `spec.md` 逐 API 子节的 `**API 描述**`（三要素+五要素）为源头，与英文注释保持语义一致
      - **约束**：中文版仅作为归档证据，不写回 API 声明仓库、不替代英文声明文件。两份 diff 均不得改变任何签名、入参、返回值、错误码或标记
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
8. When all code Tasks are complete and the user is preparing a GitCode commit, push, or PR, read `design_docs_repository` from `codespec/profile.yaml` and remind the user that `codespec/` documents must be submitted to that separate design-docs repository. If the address is absent or empty, report “design-docs 仓地址：待开发者填写”; never infer the address or push across repositories without explicit authorization. When submission is explicitly requested, use `odk-submit-design-docs` to generate `metadata_tracking.yaml` and submit the five-file bundle.

## Output

Report:

- **Execution Summary:** every Task listed with status (✅ Done / ❌ Blocked / ⚠️ Skipped) and reason for any incomplete Tasks
- Tasks completed and status changes written to `execution-plan.md`
- Reference patterns used (architectural conventions followed or "no prior art found")
- Verification results per Task
- Code mapping rows updated in `execution-plan.md` 代码范围映射
- Any deviations from `execution-plan.md` or reference patterns (with justification)
- Before GitCode submission, the separate `codespec/` publication reminder and the developer-provided `design_docs_repository` address (or “待开发者填写”)

If all Tasks are ✅ Done, suggest next step: run `{{CMD_PREFIX}}review` to generate review records. If any Task is incomplete, do NOT suggest moving to review — report the gaps and wait for user direction.
