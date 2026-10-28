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

-1. **Code-grounded brainstorm (run before generating design):** Two sub-steps — read code first, then interview based on what you find.

   **Sub-step A — Read the code:** Before asking anything, explore the codebase deeply for the modules the change touches. This is not a conditional step — do it for every change that touches existing code:
   - Trace the call chain from the entry point of the change to its callers and callees; record file:line for each hop
   - Find existing state holders: who owns each relevant data structure, which methods mutate it, what the invariants are
   - Find existing concurrency contracts: which thread/queue executes each path, which locks protect shared state, where callbacks fire
   - Find existing failure handling: how each error propagates, what callers do on failure, whether rollback or cleanup is performed
   - Find existing lifecycle management: who allocates, who frees, what happens on early exit or exception
   - Note any contradiction between `spec.md`/`proposal.md` assumptions and what the code actually shows

   State what you found (file:line references for each key finding). Only skip for pure new modules with no existing code.

   **Sub-step B — Interview based on code findings:** For each architecture decision you cannot derive from code + spec, ask one focused question at a time — grounded in a specific code location, not a generic template:
   - State ownership that is ambiguous: "I see `FooManager` holds `bar_map_` but your change creates `Bar` objects in a callback on thread X — who inserts them into `bar_map_`, and is `bar_map_` protected by the existing mutex on line Y?"
   - Concurrency boundary that is unresolved: "The existing path runs on the IPC thread (file:line), but your change adds a heavy computation — should it stay on the IPC thread or dispatch to a worker queue?"
   - Failure recovery that code does not define: "When `CreateSession()` returns `ERR_NO_MEMORY` (file:line), the existing caller ignores it — should your change introduce a recovery path, or keep the same behaviour?"
   - Migration or compatibility gap: "The existing wire format has no version field (file:line) — how should old clients behave when they receive a message with the new field?"
   - DFX fault mode without a recovery strategy: "The proposal lists network timeout as a fault mode but doesn't specify whether to retry, surface to caller, or degrade silently"

   If `spec.md` and code together answer every decision, briefly state the self-resolved decisions in one sentence and proceed to Step 0 immediately — do not skip silently without any output.

0. Check for subsystem profile: read and follow `contracts/skill-guides/router/profiles.md` — if a profile matches, apply its `template_overrides.design` (additional sections, fragments) and `agent_instructions.design`
1. **Code fact baseline:** Consolidate the findings from Step -1 Sub-step A into a structured baseline: file:line references for key data structures, entry-point signatures, call chain hops, concurrency boundaries, and failure paths. Use this baseline to populate `代码事实基线` in `design.md`. Skip only for pure greenfield modules, pure documentation changes, or config-only changes.
2. Read template from `templates/ai/design.md`
3. Generate `design.md` per the template. Conditionally include `代码事实基线`, `类图`, and `状态归属与不变量` when applicable — add `类图` (Mermaid `classDiagram`) when the change involves class/interface inheritance or implementation hierarchies (e.g. IPC interface→proxy→stub→impl) or cross-module composition. Reference specific `spec.md` AC numbers in design decisions.
   If any proposal `资源开销审视` dimension is `required`, expand `资源设计` (`contracts/artifacts.yaml#resource_contract`). Content detail is subsystem-owned; ODK requires the section and meaningful, non-placeholder content without imposing a subsystem design schema.
4. If Step 1 produced code facts, populate `代码事实基线`; otherwise omit it.
5. After design is generated, review spec's `错误码定义` and `接口变更分析` — resolve any `TBD` values, and update if design decisions introduce new error codes or change interface signatures.
6. **DFX 设计 [必填章节]**:
   - **必填性**：DFX 是必填章节（非条件触发）。即便所涉仓库都没有 DFX 知识（`fmea.yaml` 不存在或不可达），章节仍必填（填"不涉及"并说明理由）。主表有命中行或存在 AD 推导条目时，`### DFX 故障模式处置` 子节同样必填（见下第 4 步）。
   - **子章节**：`### DFX 故障模式分析`，列出仓知识库中触发条件与本变更业务流程匹配的故障模式。分析执行委托内置 `odk-fmea` skill（AIAG-VDA 七步法 + 仓级 FMEA 知识库 + DFX 表兼容模式），本 skill 负责准备输入并按第 3 步落盘契约回填；design.md 主表的知识来源仍以仓知识库（`fmea.yaml`）为权威。遍历所有仓都获取不到 FMEA 知识时，故障模式分析填"不涉及"并注明具体理由（如仓不可达、仓无 DFX 知识等），以便归档审查区分原因。
   - **执行 4 步流程**：

     1. **识别涉及仓库**：从 `design.md` `## 模块影响` 表的"仓库"列提取涉及的子系统仓库名（如 `arkui_ace_engine`）。一个子系统可能跨多个源码仓（如 ArkUI 涉及 `arkui_ace_engine` + `arkui_napi` + `arkui_component_group`），全部列出。

     2. **委托 `odk-fmea` skill 执行故障模式分析（产出命中记录 + 推导记录 + 逐仓状态，作为第 3 步输入）**：
        - **调用方式（subagent 隔离，默认）**：通过 Agent 工具在**隔离 subagent** 中执行 `odk-fmea`（本 plugin 内置 skill，流程见 `odk-fmea/SKILL.md`）——故障模式库扫描与推演体量大，必须在 subagent 上下文内完成，主会话（设计会话）只传入下述输入并接收结构化输出（命中记录、AD 级推导条目、逐仓状态、回填内容），**不加载任何触发表或类文件**。无 subagent 设施时降级：按名调用 `odk-fmea` 或直接按其 SKILL.md 在当前会话执行（此时其两级加载纪律为强制）。输入类型为其"增量需求设计文档"（codespec `changes/<repo>/<proposal-id>/`）。调用时传入：
          - `design.md` 路径与第 1 步的涉及仓库清单（作为其逐仓探测 `docs/dfx/fmea.yaml` 的范围；对象抽取与关键词生成按其 `references/design-doc-routing.md` 所定义的流程，从代码事实基线、模块影响表、实现入口表、时序图、状态归属与不变量等段落自动执行）；领域取值（故障模式库导出表的二级对象；若需求或用户交互中已给出则随调用传入，未给出由其向用户询问，仍未获回答则该列留空）
          - 变更检索摘要：`involved_repos`、`modules_and_symbols`（实现入口表中的模块/类/接口名）、`business_process_tags`（方案概述的业务流程短语）、`associated_acs`（关联 AC 编号）
          - 输出要求：按其"DFX 表兼容模式"产出 `### DFX 故障模式分析` 回填内容与涉及仓状态表；推导记录仅取架构与设计问题（AD 级）条目，单点编码问题（SC 级）表格不再生成
        - **降级路径**：skill 无法加载或调用失败时，读取 `contracts/dfx-fmea-matcher.yaml`，由当前 Agent 按该契约执行等价的仓内匹配（仓库发现顺序、执行降级、匹配规则、输出字段与来源格式以契约为唯一事实来源）。
        - **消费其输出**：命中记录（每条含 `matched_object`、`fault_mode`、`fault_effect`、`fault_cause`、`severity`、`recovery`、`key_log`、`big_data_event`、`source_ref`，`source_ref` 格式 `<repo>@<commit>:docs/dfx/fmea.yaml#<record-id>`）；推导记录（其标注"本次推导"，含仓无 `fmea.yaml` 时的全量推演与有库时的增量补充）；逐仓状态（`READ` / `NO_HIT` / `NO_DFX_KNOWLEDGE` / `UNREACHABLE`）；故障模式库导出表格（全列模板表，命中与推导条目全部进入，承载于 `## DFX 设计` 之下独立小节 `### 故障模式库导出表格`）。所有仓不可达/无 DFX 知识且无命中时，第 3 步走"不涉及"分支。

     3. **回填 `### DFX 故障模式分析` 表并按 ODK 落盘契约复核**（H3，9 列：分析对象/故障模式/故障影响/故障原因/严酷度/恢复措施/关键日志/大数据打点事件/来源；`odk-fmea` 可能已按兼容模式直接回填，此时逐条复核以下契约）：
        - **主表只回填知识库命中条目**：以命中记录的 `matched_object` 作为"分析对象"，`fault_mode`、`fault_effect`、`fault_cause`、`severity`、`recovery`、`key_log`、`big_data_event`、`source_ref` 依次照录填入其余列，不得改写。允许沿用其兼容模式在表尾追加"故障注入建议"末列（落盘校验按 9 必需列子集通过，增列不失败）。
        - **推导条目不进入主表**："本次推导"条目不得填入主表（`来源` 列只接受 fmea.yaml 出处，推导来源会使归档校验失败），也不得以与主表同列的结构另立表格（同列双表会使落盘校验取表失败）；以 AD- 分层表或独立小节附于 `## DFX 设计` 之下（单点编码问题 SC 级表格不生成、不回填），或按其默认落盘写入 `docs/dfx/fmea-analysis.md`，显式标注"本次推导"。
        - **故障模式库导出表格不受主表契约约束**：`odk-fmea` 产出的 `### 故障模式库导出表格`（全列模板表，命中与推导条目全部进入）作为独立小节与主表并列；其列集不含主表 9 必需列中的 5 列，归档校验的主表发现逻辑不会匹配它——存在与否、行数多少均不影响归档判定，复核时不必按主表规则检查该表。
        - 同一故障模式被多个业务对象触发时，分多条记录。
        - 有命中时，只将命中记录填入主表，不提及未命中的知识条目。
        - 集合为空时，不填故障模式表，写"不涉及"；随后用 `> 涉及仓库：repo-a, repo-b` 声明第 1 步得到的完整仓库集合，并填写逐仓闭包表 `仓库 | 状态 | 理由`。闭包状态只允许 `READ`（理由须为知识库无命中；`odk-fmea` 的 `NO_HIT` 映射到此）、`NO_DFX_KNOWLEDGE`（理由须为仓无 DFX 知识）、`UNREACHABLE`（仓不可达）。Archive 时闭包表必须精确覆盖全部涉及仓库；任一不可达、未知、缺失、重复或未分析状态均阻塞归档。

     4. **处置决策与 AC 回填（`### DFX 故障模式处置`，主表有命中行或存在 AD 条目时必填）**：对主表每条命中行与每条 AD 推导条目逐条确定处置，填入处置表（6 列：编号、分析对象、故障模式、处置、关联 AC、验证方式/证据）。这一步是把故障模式设计落入代码的拦截入口——漏处置条目、悬空 AC 引用在 Draft 校验即 FAIL；归档时关联 AC 的验证状态必须为 Pass（`validate-artifacts-contract.py` Level C3）。
        - **编号与匹配键**：主表命中行新分配 `FM-01`、`FM-02`…；AD 推导条目沿用其分层表原编号 `AD-xx`。`分析对象/故障模式` 从来源表照录（校验按该二元组与主表逐字匹配，改写会导致匹配失败）。
        - **处置五选一**（逐条与用户确认；按控制措施语义定落点）：
          - 控制措施**改变对外可观测行为**（超时返回明确错误码、故障后恢复到约定状态等）→ `新增 AC`（回填 spec US-DFX）或既有 AC 足够覆盖时 `复用 AC`；
          - 控制措施是**内部实现约束**（锁顺序、对象所有权、生命周期不变量等，为满足既有行为服务）→ `纳入设计约束`（写入 design 关键设计决策/状态归属与不变量等约束段，关联 Task 与单元测试/故障注入证据；不为通过 FM 门禁把内部机制写成新验收标准）；
          - 命中条目恢复措施已在代码中存在 → `现有控制覆盖`；该模式触发条件不在本次改动面 → `本变更不触及`。
        - **新增 AC 时回填 spec.md**：在 `## 用户故事或场景` 末尾追加 `### US-DFX: 故障模式响应` 子节，按全局编号顺延新增 `- **AC-N.M:** Given [故障注入条件] When [异常/边界动作] Then [可观测的恢复行为：错误码/恢复/关键日志/打点]`；同步补 `异常与边界规则`、`验证映射`、`测试设计提示` 的关联行。回填后明确告知用户 spec.md 已变更、需重新确认（Phase Gate），并提示 `{{CMD_PREFIX}}plan` 将为这些 AC 生成故障注入/异常路径 Task（不得列入「可后置」）。
        - **证据要求**：`现有控制覆盖` 给 文件:行 或既有测试引用；`本变更不触及` 给理由；`新增 AC`/`复用 AC` 给故障注入或异常路径验证方式。证据列空白的处置行会在校验 FAIL。
        - `不涉及` 分支（主表无命中且无 AD 条目）不填处置表，校验门静默。

7. **安全基础检查（条件触发）**:
   - 触发来源：`proposal.md` 的 `安全/权限` 维度 = 「是」（单一来源，与 `artifacts.yaml` 的 `conditional_sections.required_when` 一致）。
   - 「安全基础检查」章节的触发条件（信任边界/敏感数据/加密认证等）见 `artifacts.yaml` 的 `conditional_sections.required_when`；**升级到独立 `threat-model.md` 的高风险判据**见 `odk-security-threat-model/SKILL.md` 的触发条件表，本步骤不重复枚举。
   - 如 `安全/权限` 维度 = 「是」，在 `design.md` 中展开"安全基础检查"章节并填写适用维度；命中高风险判据时按 `深度威胁分析（如需）` 章节指引产出 `threat-model.md`。
   - 如不满足，在章节中填写"不涉及"并说明理由。

8. **国际化依赖分析（条件触发）**:
   **触发条件**：`proposal.md` 的 `国际化·无障碍` 维度中判断国际化 = 「是」（单一来源）
   当需求涉及国际化接口调用时，design 阶段需要明确 i18n 调用所依赖的代码仓路径，确保后续 plan 和implement 能准确调用正确接口。

   **约束**：
   - 仓路径必须基于实际搜素或用户确认，**禁止编造**
   - 仓内找不到时，**必须询问用户**确认国际化外部仓路径，**不得自行跳过**
   - **design.md 产出时所有国际化仓路径必须已确认**，不允许 TBD；不得将不确定信息留给plan阶段
   - **推翻 proposal 决策需与用户讨论**，不得直接修改 proposal 的判断结论、

   **执行流程**：

   1. **识别调用点**：从 `proposal.md` i18n 维度判断依据和 `spec.md` AC 列表中提取 i18n 场景

   2. **仓内搜索**：搜索 `I18n*`/`Intl`等 API 封装和 `import` 语句中的 i18n 模块
      - 已找到 → 记录仓内路径
      - 未找到 → 进入步骤3

   3. **确认仓路径**（存在未找到的调用点时触发）：
      询问用户提供缺失的 i18n 代码仓路径。**必须等待用户确认后才能继续，不得生成带 TBD 的 design.md**

   4. **填写 `## 国际化依赖分析` 章节**：
      - 仓路径表：调用场景 | i18n API 类型 | 依赖类型 | 仓路径 | 接口/方法 | 备注
      - 依赖类型：仓内封装（当前仓模块路径）或外部依赖（用户确认的仓路径）
      - 接口查询：确认仓路径后，扫描文件查询目标API，将签名填入 「接口/方法」 列
      - 汇总行：`| 合计 | N 个调用点 | 仓内: X / 外部: Y | - | - | - |`

## Output

Write to `codespec/changes/<repo-name>/<proposal-id>/design.md`

Confirm with the user that design decisions are aligned with requirements.

Suggest next step: run `{{CMD_PREFIX}}plan` to generate the execution plan with AC-to-Task traceability.
