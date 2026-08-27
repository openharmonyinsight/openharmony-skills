---
name: odk-design
description: "Use when writing ODK design.md (architecture, decisions, Mermaid, spec-AC references, conditional security check). Default template-driven, zero plugin dependencies. Use after spec.md."
license: MIT
---

# ODK Design

## Key Rules

- Keep the base `design.md` template minimal for simple changes.
- For complex state/ownership/lifecycle/concurrency/compatibility/performance/capacity/migration changes, use the conditional `状态归属与不变量` guidance embedded in the `design.md` template.
- Design owns internal implementation moved from spec AC (state machines, registries/caches, internal flows, traversal algorithms) → `状态归属与不变量` conditional section.
- Internal implementation invariants are verified via TDD in `execution-plan.md` tasks (design declares invariants; verification happens at implementation, not by explicit design-level verification declarations).

## Prerequisites

- `proposal.md` exists and has been approved (success criteria finalized)
- `spec.md` exists with acceptance criteria and business rules

## Input

1. Read `proposal.md` summary (first 15 lines or user-provided summary)
2. Read `spec.md` AC list and business rules (for architecture decisions to reference)

## Steps

0. Check for subsystem profile: follow the Profile Detection rules in `using-odk` — if a profile matches, apply its `template_overrides.design` (additional sections, fragments) and `agent_instructions.design`
1. **Code fact baseline (conditional):** If the change modifies an existing module (not pure greenfield, pure docs, or config-only), search the codebase for key facts the design will reference:
   - Search for existing data structures, key function signatures, and runtime flows in the affected module(s)
   - Record findings as a brief code fact baseline: file:line references for key structures, signatures, and flow paths
   - If search results contradict assumptions from `proposal.md` or `spec.md`, surface the discrepancy to the user before proceeding to generate design
   - Skip this step for brand-new modules with no existing code, pure documentation changes, or config-only changes
2. Read template from `{{ASSET_ROOT}}/templates/ai/design.md`
3. Generate `design.md` per the template. Conditionally include `代码事实基线`, `类图`, and `状态归属与不变量` when applicable — add `类图` (Mermaid `classDiagram`) when the change involves class/interface inheritance or implementation hierarchies (e.g. IPC interface→proxy→stub→impl) or cross-module composition. Reference specific `spec.md` AC numbers in design decisions.
   If any proposal `资源开销审视` dimension is `required`, expand `资源设计` (`contracts/artifacts.yaml#resource_contract`). Content detail is subsystem-owned; ODK requires the section and meaningful, non-placeholder content without imposing a subsystem design schema.
4. If Step 1 produced code facts, populate `代码事实基线`; otherwise omit it.
5. After design is generated, review spec's `错误码定义` and `接口变更分析` — resolve any `TBD` values, and update if design decisions introduce new error codes or change interface signatures.
6. **DFX 设计 [必填章节]**:
   - **必填性**：DFX 是必填章节（非条件触发）。即便所涉仓库都没有 DFX 知识（`fmea.yaml` 不存在或不可达），章节仍必填（填"不涉及"并说明理由）。
   - **子章节**：`### DFX 故障模式分析`，列出仓知识库中触发条件与本变更业务流程匹配的故障模式。唯一知识来源为仓知识库（`fmea.yaml`），不使用模型推导生成约束。遍历所有仓都获取不到 FMEA 知识时，故障模式分析填"不涉及"并注明具体理由（如仓不可达、仓无 DFX 知识等），以便归档审查区分原因。
   - **执行 3 步流程**：

     1. **识别涉及仓库**：从 `design.md` `## 模块影响` 表的"仓库"列提取涉及的子系统仓库名（如 `arkui_ace_engine`）。一个子系统可能跨多个源码仓（如 ArkUI 涉及 `arkui_ace_engine` + `arkui_napi` + `arkui_component_group`），全部列出。

     2. **构造变更检索摘要 + 仓内匹配（产出命中记录摘要，作为第 3 步输入）**：
        - **构造变更检索摘要**（主上下文，紧凑）：从 `design.md` 的 `## 模块影响` 表和 `## 实现入口` 提取：
          - `involved_repos`：涉及仓库名列表
          - `modules_and_symbols`：实现入口表中的模块/类/接口名
          - `business_process_tags`：方案概述的业务流程短语
          - `associated_acs`：关联 AC 编号
        - **加载共享契约**：读取 `{{ASSET_ROOT}}/contracts/dfx-fmea-matcher.yaml`。该契约是仓库发现顺序、执行降级、匹配规则、输出字段与来源格式的唯一事实来源。
        - **执行匹配**：优先扫描当前工作区或开发者提供的本地仓库。仅在用户确认后访问远程仓库。运行环境支持 subagent 时，可将各仓扫描并行委托给 subagent；不支持时，由当前 Agent 按相同契约顺序扫描。基础流程不得依赖 subagent 能力。
        - **输出契约**（匹配步骤返回、第 3 步消费）：
          - 每条命中：`matched_object`, `fault_mode`, `fault_effect`, `fault_cause`, `severity`, `recovery`, `key_log`, `big_data_event`, `source_ref`
          - `source_ref` 必须使用 `<repo>@<commit>:docs/dfx/fmea.yaml#<record-id>`，使评审者可定位到确定版本的知识记录
          - 各仓获取状态：可达（含命中数）/不可达/无 DFX 知识
        - **集合输出**：命中记录摘要列表。当所有涉及仓都不可达/无 DFX 知识且无命中时，集合为空，第 3 步走"不涉及"分支，需附理由注明原因

     3. **填 `### DFX 故障模式分析` 表**（H3，9 列：分析对象/故障模式/故障影响/故障原因/严酷度/恢复措施/关键日志/大数据打点事件/来源）：
        - 从匹配步骤返回的命中记录摘要中，以 `matched_object` 作为"分析对象"。
        - 将命中记录中的 `fault_mode`、`fault_effect`、`fault_cause`、`severity`、`recovery`、`key_log`、`big_data_event`、`source_ref` 依次填入其余列（这些字段已在第 2 步从 fmea.yaml 原记录获取）。
        - 同一故障模式被多个业务对象触发时，分多条记录。
        - 有命中时，只将命中记录填入表格，不提及未命中的知识条目。
        - 集合为空时，不填故障模式表，写"不涉及"；随后用 `> 涉及仓库：repo-a, repo-b` 声明第 1 步得到的完整仓库集合，并填写逐仓闭包表 `仓库 | 状态 | 理由`。状态只允许 `READ`（理由须为知识库无命中）、`NO_DFX_KNOWLEDGE`（理由须为仓无 DFX 知识）、`UNREACHABLE`（仓不可达）。Archive 时闭包表必须精确覆盖全部涉及仓库；任一不可达、未知、缺失、重复或未分析状态均阻塞归档。

7. **安全基础检查（条件触发）**:
   - 触发来源：`proposal.md` 的 `安全/权限` 维度 = 「是」（单一来源，与 `artifacts.yaml` 的 `conditional_sections.required_when` 一致）。
   - 「安全基础检查」章节的触发条件（信任边界/敏感数据/加密认证等）见 `artifacts.yaml` 的 `conditional_sections.required_when`；**升级到独立 `threat-model.md` 的高风险判据**见 `odk-security-threat-model/SKILL.md` 的触发条件表，本步骤不重复枚举。
   - 如 `安全/权限` 维度 = 「是」，在 `design.md` 中展开"安全基础检查"章节并填写适用维度；命中高风险判据时按 `深度威胁分析（如需）` 章节指引产出 `threat-model.md`。
   - 如不满足，在章节中填写"不涉及"并说明理由。

## Output

Write to `.codespec/changes/<id>/design.md`

Confirm with the user that design decisions are aligned with requirements.

Suggest next step: run `{{CMD_PREFIX}}plan` to generate the execution plan with AC-to-Task traceability.
