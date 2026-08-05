---
name: ohos-req-intake-orchestration
description: Use when orchestrating OHOS requirements intake workflow, from raw requirement to feature/proposal review baseline and review decision record. Triggers: requirement intake, requirement review, 需求导入, 需求评审, Feature评审, Proposal评审. Do NOT use for single-feature design work, downstream delivery, ad-hoc document generation, or any task outside the requirements intake workflow.
metadata:
  author: openharmony
  scope: common
  stage: requirements
  capability: intake-orchestration
  version: 0.4.0
  status: draft
  tags:
    - sdd
    - requirements
  related-skills:
    - name: ohos-req-requirement-intake
      required: true
      min_version: 0.4.0
    - name: ohos-req-feasibility-analysis
      required: true
      min_version: 0.4.0
    - name: ohos-req-arch-decision
      required: true
      min_version: 0.4.0
    - name: ohos-req-feature-proposal-baseline
      required: true
      min_version: 0.4.0
    - name: ohos-req-value-decision
      required: true
      min_version: 0.4.0
    - name: ohos-req-value-ppt-gen
      required: false
      min_version: 0.2.0
---

**Announce at start:** "我正在使用 ohos-req-intake-orchestration skill 编排需求导入评审流程。"

# OHOS 需求导入评审工作流

## 定位

OHOS 需求导入评审全流程编排入口。对用户只呈现 5 个产物阶段（需求基线→可行性结论→方案决策→Feature/Proposal 基线→评审闭环）；Step 1-14 仅作为内部 checkpoint 和机器路由编号。RR单号（rr_id）从 01-requirement.md frontmatter 继承到 04-feature.md 和 value-decision-record.md，是电子流系统的唯一追溯键。Token 经济性规则（spawn 四要素+隔离上下文+摘要≤15行+扇出≤4）是所有 subagent 调用的绑定契约。模式 A（subagent 编排）和模式 B（主 session 串行）根据运行时 subagent 能力自动切换。

## NEVER

以下禁止行为贯穿整个需求导入评审工作流，违反任一条属于流程违规：

1. **禁止嵌入文件内容到 task 描述**——spawn subagent 时 task 只传文件绝对路径，不得嵌入产物/证据全文（reason: context fork, token bloat；详见 `reference/token-economy.md` §1）
2. **禁止把证据包内容嵌入 task 字符串**——Step 4 的轻量代码预检证据包后续只传路径，subagent 按需读取（reason: token bloat；详见 `reference/token-economy.md` §2）
3. **禁止跳过预检步骤**——启动预检不通过时阻断启动，不得绕过（reason: gate integrity）
4. **禁止自行定稿拆分方案**——Step 11 必须向用户展示拆分方案并等待确认，AI 不代行（reason: resource allocation is human decision）
5. **禁止绕过内建 Gate**——Step 12 必须由 `ohos-req-feature-proposal-baseline` 在 04-feature.md 最终版上执行 Review Ready Gate（reason: gate integrity）
6. **禁止向用户反复暴露内部 Step 编号**——用户提示使用产物阶段名（需求基线、可行性结论、方案决策、Feature/Proposal 基线、评审闭环）；Step 编号仅写入内部路由字段或调试信息（reason: UX clarity）

## 输入

用户原始需求描述（文本），可选已有 Issue/PRD/会议纪要。

## 输出

- `01-requirement.md` → `02-feasibility.md` → `03-arch-decision-record.md` → `04-feature.md`
- `value-decision-record.md`

不再输出 `IR.md`、`SR.md` 或 `handoff.md`。若历史目录中存在这些旧产物，只读保留用于追溯；本流程不得自动改名、删除或覆盖，也不得把它们作为 Step 1-14 的前置条件。

## 模板与产物命名约定

`reference/` 下的模板文件不带阶段编号前缀，例如 `requirement.md`、`feasibility.md`、`arch-decision-record.md`、`feature.md`。`01-`、`02-`、`03-`、`04-` 仅用于 `{docs_dir}` 下的正式产物文件名，不用于模板引用路径。

## 环境变量

环境变量解析逻辑见 `reference/env-vars.md`。`ORCHESTRATOR_SKILL_DIR` 专用于定位本 skill 的 `scripts/` 与 `reference/`；`SKILL_HOME` 表示主 Session 工作区，不用于定位内置脚本。

## 核心原则

**决策结论由用户提供，AI 不代行。** Step 8 为强制交互点。
**拆分结果由用户确认，AI 不自行定稿。** Step 11 为强制交互点。
**工作量按复杂度分级约束。** 超过复杂度上限时必须进一步细分（简单≤5/标准≤8/复杂≤15 人月，详见 README 拆分规则）。
**需求导入评审流程串行无环，不可跳步。**

## 流程

### 启动预检 ⭐ 强制

需求导入评审工作流启动前，必须执行依赖完整性预检：

```bash
bash {ORCHESTRATOR_SKILL_DIR}/scripts/install_related_skills.sh --check
```

预期输出：
```
Bundle: ohos-requirements-intake
Installed: 6/7 或 7/7（可选 `ohos-req-value-ppt-gen` 已存在时为 7/7）
Required missing: 0
Version mismatch: 0
Result: READY
```

**任何必选 Skill 缺失或版本不匹配 → 阻断流程启动**，返回缺失列表。

`install_related_skills.sh` 按 `ORCHESTRATOR_SKILL_DIR` 解析 requirements skills 根目录；如缺失必选 skill，应从同一仓库同一分支的 `skills/common/requirements/ohos-req-*` 目录补齐，或使用 `OHOS_REQ_SKILLS_SOURCE_DIR` 指向同结构来源后执行 `--install`，通过后才允许进入需求基线阶段。

### Step 1: requirement.md — 需求导入

调用 `ohos-req-requirement-intake` 将原始诉求归一化为事实基线。必含 RR单号（如有），归入模板既有章节（frontmatter `rr_id` + §1 表格）；RR单号无值时在澄清环节向用户确认是否已立项。回传 RR单号。

### Step 2: 澄清门禁 ⭐ 强制

逐轮澄清，定稿检查全部通过后 status=Clarified，才允许进入 feasibility。

> **批量确认**：对输入材料中已有明确答案的问题（如 RR 单号、交付版本、提出人等），一次性呈现全部已知答案让用户批量确认（✅确认/✏️修正），不逐条单独交互。仅真正不确定的问题才逐条澄清。

**定稿检查清单（全部 ✅ 才可进入 feasibility）：**

- [ ] 每个章节所有字段有确认事实，无占位符
- [ ] RR单号已回填（frontmatter `rr_id` + §1 表格；无 RR单号时标注"未立项"并附依据）
- [ ] 所有 FR 有来源依据
- [ ] 所有 NFR 有量化口径（"提升XX%"不算，必须有基线和目标值）
- [ ] 优先级(P0/P1/P2)每项有判定依据
- [ ] 受影响模块有具体仓/路径（不是"待确定"）
- [ ] 用户痛点有影响描述和严重程度
- [ ] 无模糊表述（"快速""稳定""尽可能"等）

**每轮澄清后必须回填结论到 `clarification-questions.md`**：在对应问题下方追加 `**澄清结论**` 段，标注 ✅ 或 ⚠️。

### Step 3: 可行性分析输入提醒

启动 `02-feasibility.md` 前，主 Session 基于 `{docs_dir}/01-requirement.md` 推导建议补充资料清单，提醒用户可提供本地关键代码仓路径、接口文档、Owner 结论或前置依赖资料。

提醒后等待用户二选一：
- 用户提供资料：记录到 `{docs_dir}/_draft/feasibility-inputs.md`，再调用 `ohos-req-feasibility-analysis`。
- 用户确认不提供额外资料：记录"用户确认不额外提供"，再调用 `ohos-req-feasibility-analysis`，按证据受限口径标注。

记录格式参考 `reference/feasibility-inputs.md`。

### Step 4: 轻量代码预检（主 Session 执行）

`ohos-req-feasibility-analysis` subagent 在隔离上下文中运行，无法直接访问代码仓。spawn 前主 Session 必须先执行轻量代码预检，产出代码证据包供 subagent 使用。

1. 从 `{docs_dir}/01-requirement.md` 提取技术关键词
2. 查询知识库咨询路径表（若有），补充可能涉及的源码仓、模块或检索方向
3. 对每个关键仓库执行 `grep` 检索（限定咨询路径给出的目录），取 top-10 命中
4. 落盘到 `kb_precheck_path = {DOCS_REPO}/tmp/ohos_kb_precheck_{feature}.md`

**预检范围限定：≤3 个关键词，≤2 个仓库，每仓库 ≤10 条命中。** 目标是让 feasibility 有代码级证据，不是做全面分析（那是 Phase 2.0 的职责）。

> 若无可访问的代码仓或知识库，预检可跳过；`ohos-req-feasibility-analysis` 按其 Fallback 规则（Read 工具读取实际代码 / 降级为 `warn`）处理，不硬 fail。

### Step 5: feasibility.md — 可行性分析

前置：requirement.md status=Clarified，且 Step 3 已完成、Step 4 代码证据包已落盘（或确认无可预检内容）。调用 `ohos-req-feasibility-analysis`，spawn 时传入 `{kb_precheck_path}`。

### Step 6: feasibility 澄清门禁 ⭐ 强制

`ohos-req-feasibility-analysis` 规定草稿生成后必须暂停、逐轮澄清、定稿检查全部通过后才允许进入 decision。本步骤为强制门禁：

1. feasibility 草稿生成后（frontmatter `status: Draft-NeedsClarification`），主 Session 必须暂停展示澄清问题并逐轮回填，不允许直接进入 Step 7。
2. 逐轮澄清规则参见 `ohos-req-feasibility-analysis` SKILL.md「第二阶段：逐轮人工澄清」。
3. 校验 `02-feasibility.md` frontmatter `status: Clarified` 后才允许进入 Step 7。
4. **模式 B 的强制暂停点增加此步骤**：模式 B 下不自动连续执行，必须等待用户逐轮澄清完成。

### Step 7: 03-arch-decision-record.md 方案决策

调用 `ohos-req-arch-decision` 阶段A，输出 status=PendingDecision，§5-§6占位。

> **单方案快速路径**：当 02-feasibility.md §6 结论中仅有一个可行方案时，可触发 ohos-req-arch-decision 单方案快速路径——跳过候选方案对比表，一次确认即定稿，无需两阶段暂停（详见 ohos-req-arch-decision SKILL.md「单方案例外」）。

### Step 8: 决策结论收集 ⭐ 强制交互

向用户收集：选定方案、决策理由、决策者、遗留问题清单（用户评审会议认定）。AI 不代行。

> **单方案快速路径**下，本步简化为一次性确认：向用户呈现唯一方案 + 不可行证据，用户一次确认即可。

### Step 9: 03-arch-decision-record.md 定稿（阶段B）

调用 `ohos-req-arch-decision` 阶段B，基于用户结论定稿，status=Accepted。

### Step 10: feature.md — Feature/Proposal 评审基线与 Gate

调用 `ohos-req-feature-proposal-baseline`，含拆分策略（三级优先+复杂度分级工作量约束）、影响性分析、遗留问题闭环校验和内建 Review Ready Gate。RR单号从 01-requirement.md frontmatter `rr_id` 继承。回传 RR单号和 Gate 结论。

### Step 11: 拆分结果确认 ⭐ 强制交互

**feature.md 生成后，必须向用户展示拆分方案并等待确认（见 NEVER §6）。**

向用户呈现：
- 每个 proposal 的边界/职责
- 每个 proposal 的估算工作量（人月，不超过复杂度上限）
- 每个 proposal 的 Owner 和依赖关系
- 拆分方式（按仓/按功能点/单一）

用户确认后才允许执行内建 Review Ready Gate。用户要求调整时，回退到 `ohos-req-feature-proposal-baseline` 重新生成拆分方案。

### Step 12: Review Ready Gate 与 AC 一致性校验

feature.md 经用户确认后，由 `ohos-req-feature-proposal-baseline` 执行内建 Gate 判定，按 `Ready` / `Conditional Ready` / `Not Ready` 路由。Not Ready 时阻塞回 Step 10 补全。

```text
Feature/Proposal 评审基线已生成，执行 Review Ready Gate。
```

三级优先拆分策略：
1. 优先按仓+领域拆分
2. 跨仓不能独立验证时按功能点拆分
3. 每个 proposal 不超过复杂度上限（简单≤5/标准≤8/复杂≤15 人月）

**Gate 摘要模板（向用户呈现）：**
```
| 维度 | 结论 | 来源 |
|------|------|------|
| 选定方案 | {一句话} | 03-arch-decision-record.md |
| Gate | {Ready/Conditional Ready/Not Ready} | 04-feature.md |
| 复杂度 | {L0/L1/L2/L3} | 04-feature.md |
| 关键阻塞 | {BLK-XX} | 02-feasibility.md |
| 关键风险 | {RISK-XX} | 02-feasibility.md |
```

Gate 决策后，必须执行 FR→AC 追溯校验：

1. 从 `01-requirement.md` 提取所有 FR 编号
2. 从 `04-feature.md` 提取所有 AC 编号，生成 FR→AC 追溯表
3. 编号不一致时标注并要求修正
4. 校验结果写入 `04-feature.md` §5 备注

### Step 13: PPT 生成（可选）

Gate 通过后、评审会议前，主 Session 可应请求调用 `ohos-req-value-ppt-gen` 生成需求评审 PPT，供评审会议使用。

```text
Feature 已通过 Review Ready Gate。如需生成需求评审 PPT 供评审会议使用，请主动请求。
```

**前置条件：** Gate 结果为 `Ready` 或 `Conditional Ready`；Gate=Not Ready 时不生成 PPT，回退 Step 10。
模式 B 下不阻塞，置于 Gate 通过之后；用户未请求时自动跳过。

### Step 14: 评审决策纪要回流 ⭐ 强制交互

评审会议结束后，调用 `ohos-req-value-decision` 记录决策纪要。

1. 用户提供评审会议纪要
2. skill 提取决策结论：接纳 / 不接纳 / 下次重新上会
3. 路由：
   - **接纳** → 生成 value-decision-record.md，需求评审流程完成
   - **不接纳** → 关闭/归档，流程结束
   - **下次重新上会** → 退回对应 Step（标注需修改的文档和修改要求）

**不允许跳过此步骤。** 用户必须提供评审决策结论。

## 产物分类与目录规范

| 目录 | 用途 | 提交规则 |
|------|------|----------|
| `docs/features/{id}/` | 正式编号产物（01-04、value-decision-record 等） | gitcode-pr 必须提交 |
| `docs/features/{id}/_draft/` | 中间文件（草稿、实验数据） | gitcode-pr 提交前自动过滤 |
| `tmp/` | 知识库证据包等临时文件 | gitcode-pr 提交前自动过滤 |

## 用户可见阶段与内部 checkpoint

| 用户可见阶段 | 内部 checkpoint | 用户提示写法 |
|--------------|----------------|--------------|
| 需求基线 | Step 1-2 | "生成/确认 01-requirement.md" |
| 可行性结论 | Step 3-6 | "进入可行性分析" |
| 方案决策 | Step 7-9 | "需要你确认方案决策" |
| Feature/Proposal 基线 | Step 10-12 | "需要你确认 proposal 拆分和 Gate 结论" |
| 评审闭环 | Step 13-14 | "生成评审输出或记录评审结论" |

对用户回传和追问默认使用阶段名；仅在 `value-decision-record.md.routing.target_step`、日志或调试说明中保留 Step 编号。

## 详细 spawn 指令

本 SKILL.md 的 Step 1→14 即需求导入评审完整 spawn 编排规范。主 Session 按本文步骤执行，**不进入下游交付阶段**。

spawn 时遵循下节「Token 经济性 & Context 工程」的绑定契约：task 描述只含四要素（角色 / 输入路径 / 输出路径 / 任务简述），证据传路径不传内容（见 NEVER §1-§2），回传 ≤15 行。

> **Before spawning a subagent task, ask yourself:** does the task contain only the 4 required elements (skill path, task, input files, output path)? Am I embedding file content instead of a path?

> **Before Step 14 评审决策纪要, ask yourself:** 用户是否已提供评审会议纪要？接纳/不接纳/下次重新上会的结论是否由用户给出而非 AI 推断？

流程结束条件：value-decision-record.md 生成完毕。

## Token 经济性 & Context 隔离

详见 [`reference/token-economy.md`](reference/token-economy.md)。核心要点（禁止项见 NEVER §1-§2）：隔离上下文 spawn、证据传路径不传内容、摘要回传<=15行、扇出上限<=4。

## 模式切换

| 条件 | 模式 |
|------|------|
| 当前会话存在可映射的 subagent/Agent/Task 能力 | 模式 A（Subagent 编排） |
| 当前会话完全没有可隔离上下文的 subagent 能力 | 模式 B（主 session 串行） |

模式 B 下自动连续执行，强制暂停点为：
- **Step 6** feasibility 澄清门禁
- **Step 8** 决策结论收集
- **Step 11** 拆分结果确认
- **Step 14** 评审决策纪要回流

可选步骤（Step 13 PPT 生成）仅在 Review Ready Gate 通过后触发，用户未请求时自动跳过。

## 回传

≤15 行：产物路径清单 + RR单号 + proposal 数量 + Gate 结论 + value-decision-record.md 路径 + 下一步建议。不回传正式文档全文。
