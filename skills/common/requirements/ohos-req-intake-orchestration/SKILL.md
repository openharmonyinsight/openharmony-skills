---
name: ohos-req-intake-orchestration
description: Use when orchestrating OHOS Phase 0 intake workflow, from raw requirement to IR + proposal splitting + handoff contract. Triggers: requirement intake, Phase 0, requirement review, generate IR, 需求导入, 需求评审, 生成IR. Do NOT use for single-feature design work, Phase 1-9 delivery, ad-hoc document generation, or any task outside the Phase 0 requirement intake workflow.
metadata:
  author: openharmony
  scope: common
  stage: requirements
  capability: intake-orchestration
  version: 0.3.0
  status: draft
  tags:
    - sdd
    - requirements
  related-skills:
    - name: ohos-req-requirement-intake
      required: true
      min_version: 0.1.0
    - name: ohos-req-feasibility-analysis
      required: true
      min_version: 0.1.0
    - name: ohos-req-arch-decision
      required: true
      min_version: 0.1.0
    - name: ohos-req-feature-baseline
      required: true
      min_version: 0.1.0
    - name: ohos-req-review-gate
      required: true
      min_version: 0.1.0
    - name: ohos-req-value-decision
      required: true
      min_version: 0.1.0
    - name: ohos-req-review-ppt-gen
      required: false
      min_version: 0.1.0
    - name: ohos-req-feature-to-ir
      required: true
      min_version: 0.1.0
    - name: ohos-req-proposal-to-sr
      required: true
      min_version: 0.1.0
---

**Announce at start:** "我正在使用 ohos-req-intake-orchestration skill 编排 Phase 0 需求导入流程。"

# OHOS 需求导入工作流（Phase 0）

## 定位

OHOS Phase 0 需求导入全流程编排入口，串联 9 个 subagent skill（requirement→feasibility→decision→feature→gate→IR→proposal→SR→handoff）。RR单号（rr_id）从 01-requirement.md frontmatter 继承到 IR/SR/handoff 全链路，是电子流系统的唯一追溯键。Token 经济性规则（spawn 四要素+隔离上下文+摘要≤15行+扇出≤4）是所有 subagent 调用的绑定契约。模式 A（subagent 编排）和模式 B（主 session 串行）根据运行时 subagent 能力自动切换。

## NEVER

以下禁止行为贯穿整个 Phase 0 工作流，违反任一条属于流程违规：

1. **禁止嵌入文件内容到 task 描述**——spawn subagent 时 task 只传文件绝对路径，不得嵌入产物/证据全文（reason: context fork, token bloat；详见 `reference/token-economy.md` §1）
2. **禁止把证据包内容嵌入 task 字符串**——Step 0.1.9 落盘的证据包后续只传路径，subagent 按需读取（reason: token bloat；详见 `reference/token-economy.md` §2）
3. **禁止跳过预检步骤**——Step 0 依赖完整性预检不通过时阻断启动，不得绕过（reason: gate integrity）
4. **禁止在 proposal 未通过 GA 时生成对应 SR**——Step 0.9 要求每个 proposal 必须 GA-Approved 才生成 SR（reason: unapproved scope）
5. **禁止自行推算 Gate 结论**——Step 0.5 必须调用 `ohos-req-review-gate` subagent 执行独立判定，主 Session 不自行推算（reason: must use independent subagent）
6. **禁止自行定稿拆分方案**——Step 0.4.1 必须向用户展示拆分方案并等待确认，AI 不代行（reason: resource allocation is human decision）

## 输入

用户原始需求描述（文本），可选已有 Issue/PRD/会议纪要。

## 输出

- `01-requirement.md` → `02-feasibility.md` → `03-arch-decision-record.md` → `04-feature.md`
- `IR.md`（Phase 0 正式出口）
- `05-proposal*.md`（拆分后）
- `SR-*.md`（每个 GA-Approved proposal 对应一个 SR）
- `handoff.md`（交接契约，Phase 1-9 入口验证依据）

## 模板与产物命名约定

`reference/` 下的模板文件不带阶段编号前缀，例如 `requirement.md`、`feasibility.md`、`arch-decision-record.md`、`feature.md`、`proposal.md`、`SR.md`。`01-`、`02-`、`03-`、`04-`、`05-` 仅用于 `{docs_dir}` 下的正式产物文件名，不用于模板引用路径。

## 环境变量

环境变量解析逻辑见 `reference/env-vars.md`。SKILL_HOME > WORK_HOME > DOCS_REPO 三级优先，详见参考文件。

## 核心原则

**决策结论由用户提供，AI 不代行。** Step 0.3.2 为强制交互点。
**拆分结果由用户确认，AI 不自行定稿。** Step 0.4.1 为强制交互点。
**工作量按复杂度分级约束。** 超过复杂度上限时必须进一步细分（简单≤5/标准≤8/复杂≤15 人月，详见 README 拆分规则）。
**Phase 0 串行无环，不可跳步。**

## 流程

### Step 0: 启动预检 ⭐ 强制

Phase 0 工作流启动前，必须执行依赖完整性预检：

```bash
python3 {SKILL_HOME}/skills/common/requirements/ohos-req-intake-orchestration/scripts/install_related_skills.py --check
```

预期输出：
```
Bundle: ohos-phase0-intake
Installed: 9/10 或 10/10（可选 `ohos-req-review-ppt-gen` 已存在时为 10/10）
Required missing: 0
Version mismatch: 0
Result: READY
```

**任何必选 Skill 缺失或版本不匹配 → 阻断 Phase 0 启动**，返回缺失列表和安装命令：

```bash
OHOS_REQ_SKILLS_SOURCE_DIR=/path/to/openharmony-skills/skills \
python3 {SKILL_HOME}/skills/common/requirements/ohos-req-intake-orchestration/scripts/install_related_skills.py --install
```

安装脚本仅从 `OHOS_REQ_SKILLS_SOURCE_DIR` 指向的本地 skills 目录复制缺失依赖，不负责联网拉取仓库。若用户只安装了 `ohos-req-intake-orchestration` 单个 skill，必须显式提供包含完整 bundle 的本地 source 路径；否则 `--install` 会失败并提示设置该变量。脚本使用 Python 标准库实现，支持 Windows / Linux / macOS；`.sh` 文件仅作为 Linux/macOS 包装器。安装后重新执行预检，通过后才允许进入 Step 0.1。

### Step 0.1: requirement.md — 需求导入

调用 `ohos-req-requirement-intake` 将原始诉求归一化为事实基线。必含 RR单号（如有），归入模板既有章节（frontmatter `rr_id` + §1 表格）；RR单号无值时在澄清环节向用户确认是否已立项。回传 RR单号。

### Step 0.1.5: 澄清门禁 ⭐ 强制

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

### Step 0.1.8: 可行性分析输入提醒

启动 `02-feasibility.md` 前，主 Session 基于 `{docs_dir}/01-requirement.md` 推导建议补充资料清单，提醒用户可提供本地关键代码仓路径、接口文档、Owner 结论或前置依赖资料。

提醒后等待用户二选一：
- 用户提供资料：记录到 `{docs_dir}/_draft/feasibility-inputs.md`，再调用 `ohos-req-feasibility-analysis`。
- 用户确认不提供额外资料：记录"用户确认不额外提供"，再调用 `ohos-req-feasibility-analysis`，按证据受限口径标注。

记录格式参考 `reference/feasibility-inputs.md`。

### Step 0.1.9: 轻量代码预检（主 Session 执行）

`ohos-req-feasibility-analysis` subagent 在隔离上下文中运行，无法直接访问代码仓。spawn 前主 Session 必须先执行轻量代码预检，产出代码证据包供 subagent 使用。

1. 从 `{docs_dir}/01-requirement.md` 提取技术关键词
2. 查询知识库咨询路径表（若有），补充可能涉及的源码仓、模块或检索方向
3. 对每个关键仓库执行 `grep` 检索（限定咨询路径给出的目录），取 top-10 命中
4. 落盘到 `kb_precheck_path = {DOCS_REPO}/tmp/ohos_kb_precheck_{feature}.md`

**预检范围限定：≤3 个关键词，≤2 个仓库，每仓库 ≤10 条命中。** 目标是让 feasibility 有代码级证据，不是做全面分析（那是 Phase 2.0 的职责）。

> 若无可访问的代码仓或知识库，预检可跳过；`ohos-req-feasibility-analysis` 按其 Fallback 规则（Read 工具读取实际代码 / 降级为 `warn`）处理，不硬 fail。

### Step 0.2: feasibility.md — 可行性分析

前置：requirement.md status=Clarified，且 Step 0.1.8 已完成、Step 0.1.9 代码证据包已落盘（或确认无可预检内容）。调用 `ohos-req-feasibility-analysis`，spawn 时传入 `{kb_precheck_path}`。

### Step 0.2.5: feasibility 澄清门禁 ⭐ 强制

`ohos-req-feasibility-analysis` 规定草稿生成后必须暂停、逐轮澄清、定稿检查全部通过后才允许进入 decision。本步骤为强制门禁：

1. feasibility 草稿生成后（frontmatter `status: Draft-NeedsClarification`），主 Session 必须暂停展示澄清问题并逐轮回填，不允许直接进入 Step 0.3.1。
2. 逐轮澄清规则参见 `ohos-req-feasibility-analysis` SKILL.md「第二阶段：逐轮人工澄清」。
3. 校验 `02-feasibility.md` frontmatter `status: Clarified` 后才允许进入 Step 0.3.1。
4. **模式 B 的强制暂停点增加此步骤**：模式 B 下不自动连续执行，必须等待用户逐轮澄清完成。

### Step 0.3.1: 03-arch-decision-record.md 候选方案分析（阶段A）

调用 `ohos-req-arch-decision` 阶段A，输出 status=PendingDecision，§5-§6占位。

> **单方案快速路径**：当 02-feasibility.md §6 结论中仅有一个可行方案时，可触发 ohos-req-arch-decision 单方案快速路径——跳过候选方案对比表，一次确认即定稿，无需两阶段暂停（详见 ohos-req-arch-decision SKILL.md「单方案例外」）。

### Step 0.3.2: 决策结论收集 ⭐ 强制交互

向用户收集：选定方案、决策理由、决策者、遗留问题清单（用户评审会议认定）。AI 不代行。

> **单方案快速路径**下，本步简化为一次性确认：向用户呈现唯一方案 + 不可行证据，用户一次确认即可。

### Step 0.3.3: 03-arch-decision-record.md 定稿（阶段B）

调用 `ohos-req-arch-decision` 阶段B，基于用户结论定稿，status=Accepted。

### Step 0.4: feature.md — Feature 评审基线

调用 `ohos-req-feature-baseline`，含拆分策略（三级优先+复杂度分级工作量约束）、影响性分析、遗留问题闭环校验。RR单号从 01-requirement.md frontmatter `rr_id` 继承。回传 RR单号。

### Step 0.4.1: 拆分结果确认 ⭐ 强制交互

**feature.md 生成后，必须向用户展示拆分方案并等待确认（见 NEVER §6）。**

向用户呈现：
- 每个 proposal 的边界/职责
- 每个 proposal 的估算工作量（人月，不超过复杂度上限）
- 每个 proposal 的 Owner 和依赖关系
- 拆分方式（按仓/按功能点/单一）

用户确认后才允许进入 Step 0.5。用户要求调整时，回退到 ohos-req-feature-baseline 重新生成拆分方案。

### Step 0.4.2: feature 基线就绪提示（可选）

feature.md 经用户确认后，主 Session 输出一行就绪提示（不阻塞流程）。PPT 生成不再在此步骤触发，已后移至 Step 0.5.2（Gate 通过后、评审会议前）。

```text
Feature 评审基线已生成，进入 Review Ready Gate。
```

模式 B 下不等待回复，继续 Step 0.5。

### Step 0.5: Review Ready Gate 与拆分判断

主 Session 调用 `ohos-req-review-gate` subagent 执行结构化 Gate 判定（task 仅含 `docs_dir` 绝对路径，不嵌 01-04 全文），读取其 JSON 输出按 `Ready` / `Conditional Ready` / `Not Ready` 路由，**不自行推算 Gate 结论**（见 NEVER §5；详见 ohos-req-review-gate SKILL.md）。Not Ready 时阻塞回 Step 0.4。

三级优先拆分策略：
1. 优先按仓+领域拆分
2. 跨仓不能独立验证时按功能点拆分
3. 每个 proposal 不超过复杂度上限（简单≤5/标准≤8/复杂≤15 人月）

**Gate 摘要模板（向用户呈现）：**
```
| 维度 | 结论 | 来源 |
|------|------|------|
| 选定方案 | {一句话} | 03-arch-decision-record.md |
| Gate | {Ready/Conditional/Not Ready} | 04-feature.md |
| 复杂度 | {L0/L1/L2/L3} | 04-feature.md |
| 关键阻塞 | {BLK-XX} | 02-feasibility.md |
| 关键风险 | {RISK-XX} | 02-feasibility.md |
```

### Step 0.5.1: AC 一致性校验（强制）

Gate 决策后，主 Session 必须执行 FR→AC 追溯校验：

1. 从 `01-requirement.md` 提取所有 FR 编号
2. 从 `04-feature.md` 提取所有 AC 编号，生成 FR→AC 追溯表
3. 编号不一致时标注并要求修正
4. 校验结果写入 `04-feature.md` §5 备注（Gate 结论见 ohos-req-review-gate 产出的 `tmp/decision_gate_*.json`）

### Step 0.5.2: PPT 生成（0.5 衍生，可选）

Gate 通过后、评审会议前，主 Session 可应请求调用 `ohos-req-review-ppt-gen` 生成需求评审 PPT，供评审会议使用。

```text
Feature 已通过 Review Ready Gate。如需生成需求评审 PPT 供评审会议使用，请主动请求。
```

**前置条件：** Gate 结果为 `Ready` 或 `Conditional Ready`；Gate=Not Ready 时不生成 PPT，回退 Step 0.4。
模式 B 下不阻塞，置于 Gate 通过之后；用户未请求时自动跳过。

### Step 0.6: 评审决策纪要回流 ⭐ 强制交互

评审会议结束后，调用 `ohos-req-value-decision` 记录决策纪要。

1. 用户提供评审会议纪要
2. skill 提取决策结论：接纳 / 不接纳 / 下次重新上会
3. 路由：
   - **接纳** → 放行进入 Step 0.7 feature-to-ir
   - **不接纳** → 关闭/归档，Phase 0 结束
   - **下次重新上会** → 退回对应 Step（标注需修改的文档和修改要求）

**不允许跳过此步骤。** 用户必须提供评审决策结论。

### Step 0.7: IR.md — Phase 0 正式出口

调用 `ohos-req-feature-to-ir`。仅在 Gate=Not Ready 时拒绝生成；Gate=Conditional Ready 时允许生成，但必须把条件项、Owner、关闭动作和关闭时点写入 IR，IR status=Conditional。RR单号从 04-feature.md frontmatter `rr_id` 继承。回传 RR单号。

### Step 0.8: Proposal 创建与 GATE A

按 IR 拆解矩阵生成 proposal，每个独立完成澄清和 GATE A。proposal 从 IR.md frontmatter `rr_id` 继承 RR单号。

### Step 0.9: SR 生成（Phase 0 收尾）

每个 GA-Approved 的 proposal 对应一个独立的 SR 文件（`SR-01.md`、`SR-02.md`...），调用 `ohos-req-proposal-to-sr` 逐个生成。SR 从 IR.md frontmatter `rr_id` 继承 RR单号。SR 是 Phase 0 的最终收尾产物。任一 proposal 未通过 GA 时，禁止生成对应 SR（见 NEVER §4）。

### Step 0.9.1: 生成 handoff.md ⭐ 强制

Phase 0 流程结束时，主 Session **必须**生成 handoff.md 交接契约。详见 `reference/handoff.md` 模板。

handoff.md 是 Phase 0 到 Phase 1-9 的唯一交接点，包含：
- Gate 状态、decision 状态、IR 路径、feature 路径
- proposal 清单（名称、拆分方式、估算工作量）
- SR 清单（每个 proposal 对应的 SR 文件路径）
- 前置检查清单（Phase 1-9 启动时验证）

**handoff.md 完整性校验（生成后必须执行）：**
1. 代码路径完整性：提取 02-feasibility.md §2.1 所有 `文件:行号` 引用，验证在 handoff.md 出现
2. 条件项完整性：提取 04-feature.md §5 所有 proposal 依赖和前置条件，验证在 handoff.md 出现
3. 决策完整性：提取 03-arch-decision-record.md §5决策结论，验证在 handoff.md 出现
4. Proposal 拆解完整性：提取 IR.md 末尾「Proposal 拆解」补充章节所有行，验证在 handoff.md 出现
5. SR 角色完整性：提取每个 SR-*.md §二「责任人」表，验证分析责任人/SE/TSE/测试责任人均已指定（非"待确定"/空值）。任一角色缺失 → 阻断交接，提示用户回填

## 产物分类与目录规范

| 目录 | 用途 | 提交规则 |
|------|------|----------|
| `docs/features/{id}/` | 正式编号产物（01-05、IR、proposal、SR 等） | gitcode-pr 必须提交 |
| `docs/features/{id}/_draft/` | 中间文件（草稿、实验数据） | gitcode-pr 提交前自动过滤 |
| `tmp/` | 知识库证据包等临时文件 | gitcode-pr 提交前自动过滤 |

## 详细 spawn 指令

本 SKILL.md 的 Step 0.1→0.9.1 即 Phase 0 完整 spawn 编排规范。主 Session 按本文步骤执行，**不进入 Phase 1-9**（Phase 1-9 由 `ohos-delivery` 承接，以 handoff.md 为入口）。

spawn 时遵循下节「Token 经济性 & Context 工程」的绑定契约：task 描述只含四要素（角色 / 输入路径 / 输出路径 / 任务简述），证据传路径不传内容（见 NEVER §1-§2），回传 ≤15 行。

> **Before spawning a subagent task, ask yourself:** does the task contain only the 4 required elements (skill path, task, input files, output path)? Am I embedding file content instead of a path?

> **Before handoff 生成, ask yourself:** 每个 SR-*.md §二责任人表的分析责任人/SE/TSE/测试责任人是否已指定？任一缺失 → 阻断交接。

> **Before Step 0.6 评审决策纪要, ask yourself:** 用户是否已提供评审会议纪要？接纳/不接纳/下次重新上会的结论是否由用户给出而非 AI 推断？

流程结束条件：handoff.md 生成完毕。

## Token 经济性 & Context 隔离

详见 [`reference/token-economy.md`](reference/token-economy.md)。核心要点（禁止项见 NEVER §1-§2）：隔离上下文 spawn、证据传路径不传内容、摘要回传<=15行、扇出上限<=4。

## 模式切换

| 条件 | 模式 |
|------|------|
| 当前会话存在可映射的 subagent/Agent/Task 能力 | 模式 A（Subagent 编排） |
| 当前会话完全没有可隔离上下文的 subagent 能力 | 模式 B（主 session 串行） |

模式 B 下自动连续执行，强制暂停点为：
- **Step 0.2.5** feasibility 澄清门禁
- **Step 0.3.2** 决策结论收集
- **Step 0.4.1** 拆分结果确认
- **Step 0.6** 评审决策纪要回流

可选步骤（Step 0.5.2 PPT 生成）仅在 Review Ready Gate 通过后触发，用户未请求时自动跳过。

## 回传

≤15 行：Phase 0 产物路径清单 + RR单号 + IR 状态 + proposal 数量 + SR 数量 + Gate 结论 + handoff.md 路径 + 下一步建议（"可启动 ohos-delivery 进入 Phase 1-9"）。不回传正式文档全文。
