---
name: ohos-req-sdd-intake-orchestration
description: OHOS 需求导入工作流（Phase 0 全流程）。独立启动，从原始诉求到 IR + proposal 拆分 + handoff 契约。触发词：需求导入、Phase 0、需求导入、需求评审、生成IR。
metadata:
  author: openharmony
  scope: common
  stage: requirements
  domain: sdd
  capability: intake-orchestration
  version: 0.1.0
  status: draft
  tags:
    - sdd
    - requirements
---

# OHOS 需求导入工作流（Phase 0）

## 定位

独立工作流，覆盖 Phase 0 全流程（0.1→0.9），输出 IR、proposal 拆分、SR 和 **handoff.md 交接契约**。完成后可独立结束，也可由 `ohos-delivery` 接续进入 Phase 1-9。

## 输入

用户原始需求描述（文本），可选已有 Issue/PRD/会议纪要。

## 输出

- `01-requirement.md` → `02-feasibility.md` → `03-decision.md` → `04-feature.md`
- `IR.md`（Phase 0 正式出口）
- `05-proposal*.md`（拆分后）
- `SR-*.md`（每个 GA-Approved proposal 对应一个 SR）
- `handoff.md`（交接契约，Phase 1-9 入口验证依据）

## 环境变量

主 Session 在 Phase 0 启动时确定以下变量值，后续所有步骤引用这些变量：

| 变量 | 含义 | 取值规则 |
|------|------|----------|
| `SKILL_HOME` | 只读资源路径（skill 定义、模板、参考资料、已有分析） | **默认 = 主 Session 当前工作目录（cwd）**，即 skill 定义的根路径 |
| `WORK_HOME` | 产出物路径（设计文档、分析报告、生成代码） | **默认 = SKILL_HOME**。用户可指定为目标代码仓库（跨仓库场景） |
| `DOCS_REPO` | 设计文档仓库路径（产出物存放位置） | **启动时自动发现，找不到则询问用户**：按优先级查找 → 找到即使用 → 均未找到则询问用户输入路径 |
| `docs_dir` | 特性归档产物目录 | `{DOCS_REPO}/docs/features/{change-id}/`（默认）或 `{DOCS_REPO}/.codespec/changes/{change-id}/`（可选，与 ODK 对齐） |
| `analysis_dir` | 代码分析缓存目录 | `{DOCS_REPO}/analysis/` |
| `references_dir` | 参考资料 | `{DOCS_REPO}/references/` |

**取值逻辑：**

1. 主 Session 启动时，`SKILL_HOME` = 当前工作目录（cwd）
2. 如果用户指定了其他工作目录，则 `WORK_HOME` = 用户指定路径；否则 `WORK_HOME` = `SKILL_HOME`
3. `DOCS_REPO` 启动时检查（按优先级依次尝试，找到第一个满足条件的即停止）：
   - `{SKILL_HOME}` 本身（检查是否包含 `docs/features/` 和 `analysis/` 子目录）
   - 从 `SKILL_HOME` 逐级向上查找包含 `docs/features/` 和 `analysis/` 子目录的目录
   - 以上均未找到 → 询问用户："未找到设计文档仓库（需包含 docs/features/ 和 analysis/ 目录），请输入完整路径"
4. `docs_dir` = `{DOCS_REPO}/docs/features/{change-id}/` — 默认归档路径（与 ODK 对齐场景可使用 `.codespec/changes/{change-id}/`）
5. 主 Session 在 spawn subagent 时，将上述变量替换为实际绝对路径后注入 task 描述；subagent 收到的是实际路径值，不含变量名

> **重要：** 本 SKILL.md 中所有路径引用均使用上述变量。实际执行时由主 Session 完成变量替换。

## 核心原则

**决策结论由用户提供，AI 不代行。** Step 0.3.2 为强制交互点。
**拆分结果由用户确认，AI 不自行定稿。** Step 0.4.1 为强制交互点。
**每个 proposal ≤5 人月。** 超过时必须进一步细分。
**Phase 0 串行无环，不可跳步。**

## 流程

### Step 0.1: requirement.md — 需求导入

调用 `ohos-requirement` 将原始诉求归一化为事实基线。必含 RR单号（如有），归入模板既有章节（frontmatter `rr_id` + §1 表格）；RR单号无值时在澄清环节向用户确认是否已立项。回传 RR单号。

### Step 0.1.5: 澄清门禁 ⭐ 强制

逐轮澄清，定稿检查全部通过后 status=Clarified，才允许进入 feasibility。

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
- 用户提供资料：记录到 `{docs_dir}/_draft/feasibility-inputs.md`，再调用 `ohos-feasibility`。
- 用户确认不提供额外资料：记录"用户确认不额外提供"，再调用 `ohos-feasibility`，按证据受限口径标注。

记录格式参考 `reference/feasibility-inputs.md`。

### Step 0.1.9: 轻量代码预检（主 Session 执行）

`ohos-feasibility` subagent 在隔离上下文中运行，无法直接访问代码仓。spawn 前主 Session 必须先执行轻量代码预检，产出代码证据包供 subagent 使用。

1. 从 `{docs_dir}/01-requirement.md` 提取技术关键词
2. 查询知识库咨询路径表（若有），补充可能涉及的源码仓、模块或检索方向
3. 对每个关键仓库执行 `grep` 检索（限定咨询路径给出的目录），取 top-10 命中
4. 落盘到 `kb_precheck_path = {DOCS_REPO}/tmp/ohos_kb_precheck_{feature}.md`

**预检范围限定：≤3 个关键词，≤2 个仓库，每仓库 ≤10 条命中。** 目标是让 feasibility 有代码级证据，不是做全面分析（那是 Phase 2.0 的职责）。

> 若无可访问的代码仓或知识库，预检可跳过；`ohos-feasibility` 按其 Fallback 规则（Read 工具读取实际代码 / 降级为 `warn`）处理，不硬 fail。

### Step 0.2: feasibility.md — 可行性分析

前置：requirement.md status=Clarified，且 Step 0.1.8 已完成、Step 0.1.9 代码证据包已落盘（或确认无可预检内容）。调用 `ohos-feasibility`，spawn 时传入 `{kb_precheck_path}`。

### Step 0.3.1: decision.md 候选方案分析（阶段A）

调用 `ohos-decision` 阶段A，输出 status=PendingDecision，§5-§6占位。

### Step 0.3.2: 决策结论收集 ⭐ 强制交互

向用户收集：选定方案、决策理由、决策者、遗留问题清单（用户评审会议认定）。AI 不代行。

### Step 0.3.3: decision.md 定稿（阶段B）

调用 `ohos-decision` 阶段B，基于用户结论定稿，status=Accepted。

### Step 0.4: feature.md — Feature 评审基线

调用 `ohos-feature`，含拆分策略（三级优先+≤5人月约束）、影响性分析、遗留问题闭环校验。RR单号从 01-requirement.md frontmatter `rr_id` 继承。回传 RR单号。

### Step 0.4.1: 拆分结果确认 ⭐ 强制交互

**feature.md 生成后，必须向用户展示拆分方案并等待确认。AI 不自行定稿拆分方案。**

向用户呈现：
- 每个 proposal 的边界/职责
- 每个 proposal 的估算工作量（人月，≤5）
- 每个 proposal 的 Owner 和依赖关系
- 拆分方式（按仓/按功能点/单一）

用户确认后才允许进入 Step 0.5。用户要求调整时，回退到 ohos-feature 重新生成拆分方案。

### Step 0.4.2: PPT 提醒（可选）

**feature.md 确认后，主 Session 输出一行提醒告知用户可生成 PPT（不阻塞流程）。**

```text
Feature 评审基线已生成。如需生成需求评审 PPT，请主动请求。
```

模式 B 下不等待回复，继续后续步骤。用户后续可随时调用 `ohos-req-spec-to-review-ppt` 单独生成 PPT。

### Step 0.5: Review Ready Gate 与拆分判断

主 Session 调用 `ohos-review-gate` subagent 执行结构化 Gate 判定（task 仅含 `docs_dir` 绝对路径，不嵌 01-04 全文），读取其 JSON 输出按 `Ready` / `Conditional Ready` / `Not Ready` 路由，**不自行推算 Gate 结论**（详见 ohos-review-gate SKILL.md）。Not Ready 时阻塞回 Step 0.4。

三级优先拆分策略：
1. 优先按仓+领域拆分
2. 跨仓不能独立验证时按功能点拆分
3. 每个 proposal ≤5 人月

**Gate 摘要模板（向用户呈现）：**
```
| 维度 | 结论 | 来源 |
|------|------|------|
| 选定方案 | {一句话} | 03-decision.md |
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
4. 校验结果写入 `04-feature.md` §5 备注（Gate 结论见 ohos-review-gate 产出的 `tmp/decision_gate_*.json`）

### Step 0.6: IR.md — Phase 0 正式出口

调用 `ohos-feat-to-ir`。Gate 非 Ready 时拒绝生成。RR单号从 04-feature.md frontmatter `rr_id` 继承。回传 RR单号。

### Step 0.8: Proposal 创建与 GATE A

按 IR 拆解矩阵生成 proposal，每个独立完成澄清和 GATE A。proposal 从 IR.md frontmatter `rr_id` 继承 RR单号。

### Step 0.9: SR 生成（Phase 0 收尾）

每个 GA-Approved 的 proposal 对应一个独立的 SR 文件（`SR-01.md`、`SR-02.md`...），调用 `ohos-proposal-to-sr` 逐个生成。SR 从 IR.md frontmatter `rr_id` 继承 RR单号。SR 是 Phase 0 的最终收尾产物。任一 proposal 未通过 GA 时，禁止生成对应 SR。

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
3. 决策完整性：提取 03-decision.md §5决策结论，验证在 handoff.md 出现
4. Proposal 拆解完整性：提取 IR.md 末尾「Proposal 拆解」补充章节所有行，验证在 handoff.md 出现

## 产物分类与目录规范

| 目录 | 用途 | 提交规则 |
|------|------|----------|
| `docs/features/{id}/` | 正式编号产物（01-05、IR、proposal、SR 等） | gitcode-pr 必须提交 |
| `docs/features/{id}/_draft/` | 中间文件（草稿、实验数据） | gitcode-pr 提交前自动过滤 |
| `tmp/` | 知识库证据包等临时文件 | gitcode-pr 提交前自动过滤 |

## 详细 spawn 指令

本 SKILL.md 的 Step 0.1→0.9.1 即 Phase 0 完整 spawn 编排规范。主 Session 按本文步骤执行，**不进入 Phase 1-9**（Phase 1-9 由 `ohos-delivery` 承接，以 handoff.md 为入口）。

spawn 时遵循下节「Token 经济性 & Context 工程」的绑定契约：task 描述只含四要素（角色 / 输入路径 / 输出路径 / 任务简述），证据传路径不传内容，回传 ≤15 行。

流程结束条件：handoff.md 生成完毕。

## Token 经济性 & Context 工程（强制规则）⭐

> 本节是所有 subagent 调度的**绑定契约**。`sessions_spawn` 是流程里的逻辑接口名，可由当前运行时的真实 agent 工具实现（如 Codex `multi_agent_v1.spawn_agent`、Claude Code Agent/Task、OpenCode subagent 等）。目的：控制上下文与 token 开销，避免上下文 fork 复制、证据重复嵌入、产物全文复读、subagent 过度扇出。违反任一条属于流程违规。

### 1. 隔离上下文 spawn（最关键）

逻辑 spawn **必须使用隔离/最小上下文**，不得 fork/复制主会话上下文。task 描述只含四要素：

| 要素 | 内容 | 禁止 |
|------|------|------|
| ① 角色 | "你是 OHOS XX" | — |
| ② 输入路径 | 已有产物的**绝对路径**清单 | ❌ 嵌入文件内容/证据全文 |
| ③ 输出路径 | "保存到 {绝对路径}" | ❌ "保存文档"等模糊描述 |
| ④ 任务简述 | ≤1 段（目标 + 必含项 + 回传格式） | ❌ 长篇背景 |

> 主 Session 在 spawn 前完成变量替换，subagent 收到的是实际路径值，不含变量名。

### 2. 证据传路径不传内容

代码证据包在 Step 0.1.9 **落盘一次**到 `{kb_precheck_path}`。后续所有 spawn 的 task 只传该**文件路径**，subagent 按需读取需要的段落。**禁止**把证据包内容嵌入 task 字符串。

### 3. 摘要回传契约

每个 subagent 回传主会话的内容 **≤15 行**：路径 + 关键发现/结论 + 必改项计数。完整内容只写进落盘产物文件。主会话**不复读**产物全文——仅在**决策点**向用户呈现、或必须编辑某文件时，才读该文件的相关段落。

### 4.1 Context Engineering 读取策略（强制）

主会话和各 skill 生成文档时，默认采用长上下文工程实践：**相关上下文最小化 + 证据先抽取 + 按需展开**。准确度由结构化校验保证，而不是把所有文档全文读入会话。

默认读取顺序：

1. **索引层**：先用 `rg --files`、frontmatter、标题、状态字段建立文件清单和阶段状态。
2. **证据抽取层**：用 `rg` 精确抽取 AC、BR、ADR、风险、开放问题、决策结论、模块路径、错误码、接口名等关键字段。
3. **章节层**：只有当抽取结果不足、冲突或需要精确复核时，才用行号读取对应小节。
4. **全文层**：仅在用户明确要求审阅全文，或模板/接口逐字对齐确实需要时使用，并优先在隔离 subagent 内完成。

禁止行为：

- 主会话为了"参考格式"读取已生成产物的大段全文。
- 生成后把新产物全文读回会话自检。
- `rg` 查询过宽导致几十行 AC/表格正文涌入会话；应缩小模式或只统计数量。

### 5. 扇出上限

并发 subagent ≤ **4**。

### 6. 用户可见回传规范（主 Session 强制）

主 Session 面向用户回复时，默认采用"产物落盘 + 路径回传"模式，避免把正式文档正文写入对话历史。

每个 Phase 完成后的用户可见回复只包含：

- 本阶段产物清单：文件名 + 绝对路径 + frontmatter/status 或 Gate 结论。
- 关键结论摘要：只保留会影响下一步决策的结论、风险、阻塞项、变更范围，通常不超过 8-12 行。
- 必要交互说明：凡是需要用户决策、确认、补充资料或选择方案的地方，必须把背景、选项、影响讲清楚；交互问题不因节省 token 而压缩到不可理解。
- 下一步建议：说明下一阶段名称、会生成的产物、是否会进入代码实现。

默认禁止在会话中粘贴正式产物全文。允许例外：用户明确要求查看全文/章节/表格、决策点必须展示的候选方案摘要/Gate 摘要/风险阻塞项、评审发现/代码 diff 摘要等需要用户立即理解并决策的短内容。

## 模式切换

| 条件 | 模式 |
|------|------|
| 当前会话存在可映射的 subagent/Agent/Task 能力 | 模式 A（Subagent 编排） |
| 当前会话完全没有可隔离上下文的 subagent 能力 | 模式 B（主 session 串行） |

模式 B 下自动连续执行，强制暂停点为：
- **Step 0.3.2** 决策结论收集
- **Step 0.4.1** 拆分结果确认

可选步骤（PPT 生成）在用户未请求时自动跳过。

## 回传

≤15 行：Phase 0 产物路径清单 + RR单号 + IR 状态 + proposal 数量 + SR 数量 + Gate 结论 + handoff.md 路径 + 下一步建议（"可启动 ohos-delivery 进入 Phase 1-9"）。不回传正式文档全文。
