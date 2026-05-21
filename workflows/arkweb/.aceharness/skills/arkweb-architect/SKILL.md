---
name: arkweb-architect
description: ArkWeb AI 辅助设计流程编排入口。当用户提到 ArkWeb、chromium、web_webview、WebView、需求分析、设计文档等关键词时触发。每个 skill 对应一个独立 subagent，主 session 仅做调度和决策。
---

# ArkWeb 架构师 - Subagent 编排流程

## 环境变量

主 Session 在 Phase 1 开始前确定以下变量值，后续所有 Phase 引用这些变量：

| 变量 | 含义 | 取值规则 | 示例 |
|------|------|---------|------|
| `SKILL_HOME` | 只读资源路径（skill 定义、模板、参考资料、已有分析） | **默认 = 主 Session 当前工作目录（cwd）**。即 skill 定义的根路径 | — |
| `WORK_HOME` | 产出物路径（设计文档、分析报告、生成代码） | **默认 = SKILL_HOME**。用户可指定为目标代码仓库（跨仓库场景） | — |
| `DOCS_REPO` | 设计文档仓库路径（产出物存放位置） | **启动时自动发现，找不到则询问用户**：按优先级查找 → 找到即使用 → 均未找到则通过 `AskUserQuestion` 要求用户直接输入路径 | — |
| `docs_dir` | 特性产出物目录 | `{DOCS_REPO}/docs/features/{feature-name}/` | — |
| `analysis_dir` | 代码分析缓存目录 | `{DOCS_REPO}/analysis/` | — |
| `references_dir` | 参考资料 | `{DOCS_REPO}/references/` | — |

**取值逻辑：**
1. 主 Session 启动时，`SKILL_HOME` = 当前工作目录（cwd）
2. 如果用户指定了其他工作目录，则 `WORK_HOME` = 用户指定路径；否则 `WORK_HOME` = `SKILL_HOME`
3. `DOCS_REPO` 启动时检查（按优先级依次尝试，找到第一个满足条件的即停止）：
   - `{SKILL_HOME}` 本身（检查是否包含 `docs/features/` 和 `analysis/` 子目录）
   - `{SKILL_HOME}/{DOCS_REPO_DIR}`（检查该目录是否存在且包含 `docs/` 和 `analysis/` 子目录）
   - 从 `SKILL_HOME` 逐级向上查找包含 `docs/features/` 和 `analysis/` 子目录的目录
   - 以上均未找到 → 使用 `AskUserQuestion` 向用户询问："未找到设计文档仓库（需包含 docs/features/ 和 analysis/ 目录），请输入完整路径"
4. 主 Session 在 spawn subagent 时，将上述变量替换为实际绝对路径后注入 task 描述
5. subagent 收到的 task 中不包含变量名，只有实际路径值

> **重要：** 本 SKILL.md 中所有路径引用均使用上述变量。这是为了让不同模型/环境都能无歧义理解路径含义。实际执行时由主 Session 完成变量替换。

## 核心原则

**主 Session = 协调者 + 决策者，不做实际工作。**

每个 skill 是一个独立 subagent，拥有自己的上下文和输出。Subagent 之间通过文件系统传递数据（读写共享 workspace），不直接通信。

**proposal.md 是核心需求文档。** 模板产出物（spec.md）从 proposal.md 中提取生成。评审对象始终是 proposal.md。

## 架构总览

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                         🧠 主 Session（协调者）                                                │
│                                                                                              │
│  ┌───────┐ ┌───────┐ ┌───────┐                                                                  │
│  │决策 1 │ │决策 2 │ │决策 3 │                                                                  │
│  │选方案?│ │评审?  │ │审代码?│                                                                  │
│  └───┬───┘ └───┬───┘ └───┬───┘                                                                  │
│      └─────────┴─────────┘                                                                      │
│  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    Subagent 调度器                                                   │  │
│  │         spawn / yield / collect / steer / kill                                       │  │
│  └──────────────────────────────────────────────────────────────────────────────────────┘  │
└──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬────────────────┘
           │          │          │          │          │          │          │
     ┌──────────────────────────────────────────────────────────┐
     │ 专家团（10 专家并行，由主 Session 直接调度）              │
     │ ⚡🎬🔌🔐🎨🖼️✨🌐⚙️🛡️                              │
     │ → 按相关度权重筛选（🟢核心/🟡关联/⚪旁听）              │
     └──────────────────────────────────────────────────────────┘
     ┌──────────────────────────────────────────────────────────┐
     │Sub-1 brainstorm（接收专家意见，输出方案）[Phase 2]          │
     │ → 读取专家团讨论纪要 → 融入方案 → 输出 brainstorm       │
     └──────────────────────────────────────────────────────────┘
     ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
     │Sub-2    │ │Sub-3    │ │Sub-4    │ │Sub-7    │ │Sub-8    │
     │code     │ │design   │ │spec     │ │code     │ │committer│
     │analysis │ │doc      │ │review   │ │gen      │ │review   │
     └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
     ┌─────────┐
     │Sub-9    │
     │gitcode  │
     │pr       │
     │(Phase 9)│
     └─────────┘
     ┌─────────┐
     │Sub-10   │
     │spec-gen │
     │(Phase 6)│
     └─────────┘

     ┌──────────────────────────────────────────────────────────┐
     │ 主 Session 直接生成（不通过 subagent）                    │
     │ → proposal.md (Phase 1 需求录入 + Phase 1.5 澄清 + Phase 3 基线) │
     └──────────────────────────────────────────────────────────┘
```

## Subagent 清单

| ID | Skill | 职责 | 输入 | 输出 |
|----|-------|------|------|------|
| Sub-1 | arkweb-brainstorm | 需求拆解与方案设计 | 用户需求 + 约束 | brainstorm.md |
| Sub-2 | arkweb-code-analysis | 代码仓库分析 | 技术关键词 | analysis.md |
| Sub-3 | arkweb-design-doc | 设计文档生成 | 确认方案 + 代码索引 + 不涉及项 | requirement.md + design.md |
| Sub-4 | arkweb-spec-review | 文档评审（含 Checklist 检视） | 设计文档 + 代码索引 | review.md |
| Sub-7 | arkweb-code-gen | 代码生成（Spec 驱动） | 设计文档 + spec.md + 代码索引 | 实现代码 + 测试 |
| Sub-8 | arkweb-committer-review | Committer 代码检视 | 设计文档 + 生成代码 | review-report.md |
| Sub-9 | gitcode-pr | GitCode 提交 | 文档 + 代码 + 提交信息 | Issue + PR |
| Sub-10 | arkweb-spec-gen | 统一 Spec + 执行计划生成 | proposal + requirement + design + review + analysis | spec.md + task.md |

> **注：** proposal.md（Phase 1 需求录入 + Phase 1.5 澄清记录 + Phase 3 需求基线）由**主 Session 直接生成**。spec.md + task.md（Phase 6）由 Sub-10 (spec-gen) 生成。

> **v5 变更：** Sub-4 合并了原 Sub-4.5（checklist-review）的功能，评审时同时完成技术评审和 Checklist 规范性检视。Sub-5（spec-extract）和 Sub-6（create-spec）已移除，spec.md 改由 Sub-10 (spec-gen) 在 Phase 6 生成。

### 专家团 Subagent（由主 Session 直接调度）

在 Phase 2 的 Step 2.2 中，主 Session 直接 spawn 领域专家 subagent，收集意见后传给 brainstorm：

| ID | Skill | 角色 | 触发条件 |
|----|-------|------|---------|
| Exp-1 | arkweb-expert-performance | ⚡ 性能专家 | brainstorm 自动触发 |
| Exp-2 | arkweb-expert-multimedia | 🎬 多媒体专家 | brainstorm 自动触发 |
| Exp-3 | arkweb-expert-peripheral | 🔌 外设服务专家（传感器/电池/唤醒锁/震动/屏幕） | brainstorm 自动触发 |
| Exp-4 | arkweb-expert-interaction-security | 🔐 交互安全专家 | brainstorm 自动触发 |
| Exp-5 | arkweb-expert-rendering | 🎨 渲染引擎专家 | brainstorm 自动触发 |
| Exp-6 | arkweb-expert-compositing | 🖼️ 渲染合成专家 | brainstorm 自动触发 |
| Exp-7 | arkweb-expert-interaction-motion | ✨ 交互专家（滚动/缩放/菜单/选择/拖拽/上传/焦点/填充/AI化） | brainstorm 自动触发 |
| Exp-8 | arkweb-expert-network | 🌐 网络加载专家 | brainstorm 自动触发 |
| Exp-9 | arkweb-expert-js-engine | ⚙️ JS 引擎专家 | brainstorm 自动触发 |
| Exp-10 | arkweb-expert-stability | 🛡️ 稳定性与 DFX 专家 | brainstorm 自动触发 |

> **注意**：专家团 subagent 由主 Session 在 Phase 2 中直接调度，不在 Sub-1 (brainstorm) 内部 spawn。主 Session 收集专家意见后汇总为「专家团讨论纪要」，作为 brainstorm 的输入。

## 完整流程

### 阶段编号规范

**Phase 1-9 = 自然数顺序** — 每个阶段对应一个独立步骤，编号连续无跳号。

| 编号 | 阶段 | 类型 | 必选/可选 | 说明 |
|------|------|------|----------|------|
| 1 | proposal（需求录入+基线） | 独立 | **必选** | Phase 1 录入原始需求，Phase 3 追加需求基线，一份文件 |
| 1.5 | 需求澄清（多轮对话） | 独立 | **必选** | 逐轮向用户提问，澄清待验证假设、范围、子系统影响等，全部澄清后才可进入 Phase 2 |
| 2 | 需求分析 | 独立 | **必选** | 知识库检索 + 专家团 + brainstorm + code-analysis，触发决策 1 |
| 3 | design（设计文档） | 独立 | **必选** | 产出 requirement.md + design.md |
| 4 | 设计文档 | 独立 | **必选** | 产出完整设计文档 |
| 5 | spec-review | 独立 | **必选** | 技术评审 + Checklist 一次完成，触发决策 2 |
| 6 | spec（统一规格文档） | 独立 | **必选** | Sub-10 生成 spec.md（4 合 1）+ task.md，code-gen 输入 |
| 7 | 代码生成 | 独立 | **必选** | Spec 驱动代码生成，触发决策 3 |
| 8 | Committer 检视 | 独立 | **必选** | 产出检视报告 |
| 9 | 提交 PR | 独立 | **必选** | 产出 Issue + PR |

### Phase 1: 初始化与需求录入

```
主 Session:
  1. 接收用户需求
  2. 提取关键信息：
     - 需求描述
     - 目标设备（默认：全覆盖）
     - OHOS 版本（默认：全部）
  3. 确定工作目录：
     - docs_dir = {docs_dir}{feature-name}/
     - analysis_dir = {analysis_dir}
     - date = YYYY-MM-DD
     - feature = {从需求中提取的简短英文标识（kebab-case）}
  4. 创建需求目录：
     - mkdir -p {docs_dir}
  5. 生成文件名模板：
     - proposal: {docs_dir}/proposal.md
     - brainstorm: {docs_dir}/{date}-{feature}-brainstorm.md
     - requirement: {docs_dir}/{date}-{feature}-requirement.md
     - design: {docs_dir}/{date}-{feature}-design.md
     - review: {docs_dir}/{date}-{feature}-review.md
     - spec: {docs_dir}/spec.md
     - analysis: {analysis_dir}/{date}-{feature}-analysis.md
     - committer-review: {docs_dir}/{date}-{feature}-committer-review.md
```

#### proposal（需求录入+基线）⭐ 必选

在 brainstorm 之前，记录需求的原始上下文，确保追溯链完整。使用 **proposal.md** 模板格式。

```
主 Session:
  1. 从用户需求中提取：
     - 来源（MSDP / 内部 / 竞品 / 社区 Issue）
     - 提出人/团队
     - 原始问题描述
     - 用户痛点
     - 竞品/背景证据
     - 初始范围（可能包含 / 明确不包含）
     - 初始假设（待验证的技术假设）
     - 预计流程级别：L0（小改动）/ L1（标准 Feature）/ L2（跨子系统）/ L3（大型 Feature）
     - 判断依据：涉及仓数量、API 级别、是否需要跨团队
     - 目标发行版本：记录版本号或 TBD
     - 版本是否已承诺：是/否/待确认
  3. 保存为 proposal.md
```

**【强制】生成 proposal.md 前，必须先读取模板文件 `{DOCS_REPO}/assets/templates/proposal.md`，严格按模板的章节结构、中文章节标题、表格格式填充内容。不得自行改为英文结构或英文标题。**

**模板参考**：`{DOCS_REPO}/assets/templates/proposal.md`
- 基本信息表（需求ID / 来源 / 优先级 / 状态）
- 目标发行版本表（版本 / 判断依据 / 是否已承诺 / 后续事实源）
- 原始问题描述
- 用户/开发者痛点表
- 期望结果列表
- 背景和证据表（竞品分析链接、代码分析链接）
- 初始范围（可能包含 / 明确不包含）
- 初始假设表（假设 / 类型 / 验证方式 / 状态）

#### Phase 1.5: 需求澄清（多轮对话）⭐ 必选 · 强制决策点

**proposal.md 第一章生成后，必须进入需求澄清环节。不允许跳过。**

澄清是逐轮对话，不是一次性填表。主 Session 必须主动向用户提问，等待用户回复后再继续。

```
主 Session:
  1. 从 proposal.md 第一章提取所有"待澄清/待验证"项：
     - 初始假设表中的「待验证」条目
     - 初始范围中的模糊描述
     - 用户痛点中需要确认的细节
     - 目标设备/OHOS 版本的默认值是否正确
     - 初始分级判断是否有依据不足的项
     - 复杂度判断是否需要更多信息
  2. 将待澄清项整理为编号问题清单（Q-1, Q-2, ...），每项包含：
     - 具体问题
     - 为什么需要澄清（对后续设计的影响）
  3. 向用户展示问题清单，**逐条或分批提问**
  4. 记录用户回答到 proposal.md 第二章「澄清记录」：
     - 更新「待澄清问题」表的状态（待澄清 → 已确认/已排除/待定）
     - 追加「讨论记录」
     - 更新「功能范围确认」「子系统影响」「API 变更评估」等表
     - 更新「初始假设」表的状态（待验证 → 已验证/已否定/需补充信息）
  5. 每轮澄清后检查：是否产生了新的待澄清项？
     - 是 → 继续下一轮澄清
     - 否 → 检查进入设计条件
```

**澄清完成条件（全部满足才能进入 Phase 2）：**
- [ ] 所有待澄清问题状态不为"待澄清"（已确认/已排除/待定但用户已知情）
- [ ] 初始假设全部有结论（已验证/已否定/用户接受风险）
- [ ] 功能范围确认完毕
- [ ] 子系统影响已初步识别
- [ ] 复杂度分级有明确判断（或有用户确认的"待定"理由）

**澄清原则：**
- **不猜测**：不确定的一定要问，不要用"默认""推测""大概率"代替用户确认
- **不过载**：每轮提问控制在 3-5 个核心问题，避免一次性列出所有问题
- **有优先级**：先澄清对方案选型有直接影响的问题，再澄清细节
- **可追溯**：每轮澄清的结论都记录到 proposal.md 第二章，不丢信息
- **允许中断**：用户可以随时补充新信息，主 Session 回到澄清环节更新记录

> **注意：** proposal.md 模板中「第二章：澄清记录」已包含完整的记录结构（待澄清问题表、讨论记录、功能范围确认、子系统影响、API 变更评估、兼容性需求、依赖与风险等）。主 Session 按模板结构逐项填充即可。

### Phase 2: 需求分析 — 知识库检索 + 专家团 + brainstorm + code-analysis

Phase 2 分为五个步骤：

#### Step 2.0: 知识库检索（主 Session 执行）

**【强制】** 在 spawn 任何 subagent 之前，主 Session 必须先执行知识库检索，产出「知识库证据包」。

降级策略（按优先级逐级尝试，参见 `_shared/KB_RULES.md`）：

| 优先级 | 数据源 | 执行方式 |
|--------|--------|----------|
| 🥇 首选 | oh-chromium-knowledge | GitCode API 读取 index.json → search/by_feature.json → routing_table.json |
| 🥇 首选 | oh-ai-full-design | GitCode API 读取 index.json → search/by_keyword.json → subsystems/ → components/ |
| 🥈 次选 | DeepWiki MCP | `read_wiki_structure` → `read_wiki_contents` → `ask_question` |
| 🥉 兜底 | 本地文档 | grep 搜索 `{DOCS_REPO}/analysis/*.md` 和 `{DOCS_REPO}/references/*.md` |
| 🏅 最终 | 克隆仓库 | `git clone --depth=1` 到 `{DOCS_REPO}/tmp/` 后搜索 |

> **两个 🥇 知识库互补使用**：oh-chromium-knowledge 聚焦 Chromium 内核实现，oh-ai-full-design 聚焦鸿蒙组件体系。涉及 Chromium 代码路径优先前者，涉及子系统/部件/API 优先后者。oh-ai-full-design 为私有仓库，无权限时跳过。

**执行步骤：**

1. 从 Phase 1 的 proposal.md 中提取需求关键词
2. 🥇 读取 `skills/oh-chromium-knowledge/SKILL.md` 获取知识库读取协议
3. 🥇 按 `index.json → search/by_feature.json → routing_table.json` 流程检索，匹配需求关键词
4. 🥇 读取 oh-ai-full-design 知识库，按 `index.json → search/by_keyword.json → subsystems/ → components/` 流程检索（如无权限跳过）
5. 记录命中结果（相关仓库、模块、代码路径、架构文档、子系统/部件/API）
6. 🥈 对于 🥇 未覆盖的需求关键词，使用 DeepWiki MCP 补充检索
7. 🥉 对于 🥇🥈 都未覆盖的细节，搜索本地文档
8. 🏅 如仍有未覆盖项，按需克隆仓库
9. 汇总为「知识库证据包」，格式如下：

```
## 知识库证据包

### 🥇 oh-chromium-knowledge
- 匹配的功能类型: {type}（来自 search/by_feature.json）
- 相关代码路径: {paths}（来自 routing_table.json）
- 架构约束: {summary}（来自 architecture.md）
- 未覆盖项: {items}

### 🥇 oh-ai-full-design
- 匹配的子系统/部件: {subsystem/component}
- 相关 API: {apis}
- SystemCapability: {syscap}
- 未覆盖项: {items}（或：无权限，已跳过）

### 🥈 DeepWiki 补充
- 仓库: {repo} → 搜索 "{keyword}" → {发现摘要}
- 未覆盖项: {items}

### 🥉 本地文档补充
- 文档: {path} → {发现摘要}
- 未覆盖项: {items}

### 🏅 克隆仓库（如有）
- 仓库: {repo} → 搜索 "{keyword}" → {发现摘要}
```

10. **【强制持久化】** 将完整证据包（含所有原始检索内容）Write 到 `{DOCS_REPO}/tmp/arkweb_kb_evidence_{YYYYMMDD_HHmmss}_{feature}.md`。详见 `_shared/KB_RULES.md` 第 11 节「证据包持久化」。
   - 文件必须包含每个数据源的**原始检索结果**（完整 JSON、文本、代码片段），不允许仅保存摘要
   - 先 Write 到 `{DOCS_REPO}/tmp/`，然后再将证据包内容注入 subagent
   - 后续 phase 如需复用证据包，优先从 `{DOCS_REPO}/tmp/` 读取已有文件

**此证据包将注入到后续所有 subagent（专家团、code-analysis、brainstorm）的 task 描述中。同时，证据包文件路径也会传递给 subagent，以便 subagent 在上下文丢失时可以从文件恢复。**

#### Step 2.1: 专家团相关度权重判定

在 spawn 之前，主 Session 先判定每个专家的相关度级别：

**权重规则：**
1. **核心专家**（权重 3x）：需求直接相关的领域专家，其意见在汇总时优先级最高
2. **关联专家**（权重 2x）：需求间接相关的领域专家，其意见有参考价值
3. **旁听专家**（权重 1x）：需求基本不相关的领域专家，仅从通用角度补充

**判定方式：**
- 🟢 核心专家：需求的主要功能直接属于该专家领域 → 直接 spawn
- 🟡 关联专家：需求可能间接影响该专家领域 → 直接 spawn
- ⚪ 旁听专家：需求与该专家领域基本无关 → 超过 5 个则跳过（节省资源）

**讨论控制：**
- 核心专家的意见篇幅应占总意见的 40%+
- 关联专家的意见篇幅应占 30%
- 旁听专家简短表态即可（1-2 点），不超过 30%

#### Step 2.2: 并行 — 专家团讨论 + code-analysis

主 Session 同时 spawn 以下 subagent：

##### 专家团（每个专家一个 subagent）

```python
sessions_spawn(
    task="""
    你是 ArkWeb 领域的{角色名}专家。请分析以下需求，从你的专业角度给出意见。

    1. 读取你的 skill 文件：{skill_path}
    2. 按 skill 定义的输出格式给出意见

    ## 用户需求
    {user_requirement}

    ## 约束条件
    - 目标设备：{device_scope}
    - OHOS 版本：{ohos_versions}

    ## 知识库证据包（主 Session 已检索完成）

    以下是通过知识库降级策略检索到的证据，你必须在意见中引用相关证据。

    {kb_evidence_package}

    **证据包持久化文件（上下文丢失时可从此文件恢复）**：
    {DOCS_REPO}/tmp/arkweb_kb_evidence_{timestamp}_{feature}.md

    直接输出你的专家意见，不需要保存文件。
    """,
    mode="run",
    label="expert-{expert_id}"
)
```

**专家 spawn 列表：**

| # | Expert ID | 角色 | Skill 路径 |
|---|-----------|------|-----------|
| 1 | arkweb-expert-performance | ⚡ 性能专家 | .skills/arkweb-experts/arkweb-expert-performance/SKILL.md |
| 2 | arkweb-expert-multimedia | 🎬 多媒体专家 | .skills/arkweb-experts/arkweb-expert-multimedia/SKILL.md |
| 3 | arkweb-expert-peripheral | 🔌 外设服务专家 | .skills/arkweb-experts/arkweb-expert-peripheral/SKILL.md |
| 4 | arkweb-expert-interaction-security | 🔐 交互安全专家 | .skills/arkweb-experts/arkweb-expert-interaction-security/SKILL.md |
| 5 | arkweb-expert-rendering | 🎨 渲染引擎专家 | .skills/arkweb-experts/arkweb-expert-rendering/SKILL.md |
| 6 | arkweb-expert-compositing | 🖼️ 渲染合成专家 | .skills/arkweb-experts/arkweb-expert-compositing/SKILL.md |
| 7 | arkweb-expert-interaction-motion | ✨ 交互专家（滚动/缩放/菜单/选择/拖拽/上传/焦点/填充/AI化） | .skills/arkweb-experts/arkweb-expert-interaction-motion/SKILL.md |
| 8 | arkweb-expert-network | 🌐 网络加载专家 | .skills/arkweb-experts/arkweb-expert-network/SKILL.md |
| 9 | arkweb-expert-js-engine | ⚙️ JS 引擎专家 | .skills/arkweb-experts/arkweb-expert-js-engine/SKILL.md |
| 10 | arkweb-expert-stability | 🛡️ 稳定性与 DFX 专家 | .skills/arkweb-experts/arkweb-expert-stability/SKILL.md |

根据 Step 1.0 的相关度判定，跳过旁听专家（如超过 5 个）。

##### Sub-2: code-analysis（不变）

```python
sessions_spawn(
    task="""
    你是 ArkWeb 代码分析师。请执行以下任务：

    1. 读取 skill 文件：.skills/arkweb-code-analysis/SKILL.md
    2. 按 SKILL.md 的流程执行代码分析

    ## 需求关键词
    {tech_keywords_from_requirement}

    ## 分析范围
    - ace_engine: Web 组件相关代码
    - web_webview: NWeb API 相关代码
    - chromium_src: 内核相关代码（如涉及）

    ## 数据源（按优先级使用）

    降级策略及认证方式详见 `_shared/KB_RULES.md`。

    ### 🥈 DeepWiki 在线索引
    - OpenHarmony ACE Engine: https://deepwiki.com/openharmony/arkui_ace_engine
    - OpenHarmony WebWebView: https://deepwiki.com/openharmony/web_webview
    - Chromium: https://deepwiki.com/niclas-ahden/chromium-source-code

    ### 🥉 本地分析文档（复用）
    - {analysis_dir}arkweb-ace-engine-analysis.md
    - {analysis_dir}web-webview-analysis.md
    - {analysis_dir}chromium-arkweb-analysis.md

    ## 知识库证据包（主 Session 已检索完成）

    以下是通过知识库降级策略检索到的证据，在分析中引用相关证据。

    {kb_evidence_package}

    **证据包持久化文件（上下文丢失时可从此文件恢复）**：
    {DOCS_REPO}/tmp/arkweb_kb_evidence_{timestamp}_{feature}.md

    ## 输出
    将分析结果保存到：
    {analysis_dir}{date}-{feature}-analysis.md

    文档必须包含：
    - 相关文件清单（路径 + 职责）
    - 关键类和接口签名
    - 现有代码中与本需求相关的逻辑
    - 对设计方案的技术可行性评估

    完成后回复文档路径和关键发现摘要。
    """,
    mode="run",
    label="code-analysis"
)
```

**主 Session 等待所有专家 + code-analysis subagent 完成：**
```
sessions_yield()  # 等待 subagent 结果推送
```

#### Step 2.3: 收集专家意见

等待所有专家 subagent 完成，主 Session 汇总为「专家团讨论纪要」：

1. **分类整理**：将专家意见按"采纳/参考/暂不考虑"分类
2. **提取共识**：多个专家共同关注的问题
3. **识别冲突**：不同专家之间的意见分歧
4. **权重标注**：每个专家意见标注权重级别（🟢/🟡/⚪）

汇总格式：
```markdown
## 🧠 专家团讨论纪要

### 共识（3+专家一致）
- {共识1}

### 高价值建议（2专家提出）
- {建议1}

### 分歧与权衡
- {分歧1}：{专家A} 认为... vs {专家B} 认为... → 结论：{总架构师裁定}

### 领域特定关切
- ⚡ 性能：{关键点}
- 🎬 多媒体：{关键点}
- ...

### 对方案的影响
- 采纳的专家意见将如何影响方案设计
```

#### Step 2.4: brainstorm

spawn brainstorm subagent，task 描述中直接包含专家团讨论纪要：

```python
sessions_spawn(
    task="""
    你是 ArkWeb 需求分析师。请执行以下任务：

    1. 读取 skill 文件：.skills/arkweb-brainstorm/SKILL.md
    2. 按 SKILL.md 的流程执行需求拆解（**跳过专家团讨论步骤**，因为已在 Phase 2 完成）

    ## 用户需求
    {user_requirement}

    ## 约束
    - 目标设备：{device_scope}
    - OHOS 版本：{ohos_versions}

    ## 参考资料（按需读取）
    - 架构参考：{references_dir}arkweb-architecture.md
    - 兼容性检查：{WORK_HOME}/docs/api-compatibility-check-arkweb.md
    - 代码分析报告：{analysis_dir}{date}-{feature}-analysis.md

    ## 知识库证据包（主 Session 已检索完成）

    以下是通过知识库降级策略检索到的证据，你必须在方案设计中引用相关证据，并在文档末尾输出「知识证据清单」。

    {kb_evidence_package}

    **证据包持久化文件（上下文丢失时可从此文件恢复）**：
    {DOCS_REPO}/tmp/arkweb_kb_evidence_{timestamp}_{feature}.md

    ## 专家团讨论纪要（已由主 Session 收集完成）

    以下是领域专家的意见汇总，你必须在方案设计中标注采纳了哪些专家建议。

    {expert_opinions_summary}

    ## 输出
    将完整的 brainstorm 文档保存到：
    {docs_dir}{feature-name}/{date}-{feature}-brainstorm.md

    文档必须包含：
    - 需求理解（问题现象 + 根因分析）
    - 2-3 个可选方案（含对比矩阵）
    - 推荐方案及理由
    - 交互场景补充分析（如拖拽/滚动等）
    - 专家团讨论纪要（含各专家意见、权重标注及采纳情况）
    - 知识证据清单（引用知识库证据包中的条目）

    完成后回复文档路径和方案摘要。
    """,
    mode="run",
    label="brainstorm"
)
```

**主 Session 等待 brainstorm subagent 完成：**
```
sessions_yield()  # 等待 Sub-1 结果推送
```

### 🔀 决策 1: 确认方案（已包含专家团意见）

```
主 Session:
  1. 读取 Sub-1 输出的 brainstorm.md（内含专家团讨论纪要）
  2. 读取 Sub-2 输出的 analysis.md（关键发现）
  3. 将方案摘要 + 专家团关键建议 + 代码分析发现呈现给用户
  4. 等待用户选择：
     a) 确认方案 X → 进入 Phase 3（需求基线）
     b) 修改方案 → 重新 spawn Sub-1（附修改意见 + 专家纪要）
     c) 需要更多信息 → 补充后重新启动 Phase 2
```

### Phase 3: 需求基线（追加到 proposal.md）⭐ 必选 · 核心文档

方案确认后，生成稳定版需求基线文档。这是**核心需求文档**——所有后续流程（评审、代码生成、spec 提取）都基于此文档。

```
主 Session:
  1. 从以下输入提取需求基线：
     - proposal.md 第一章（原始痛点 + 背景）
     - brainstorm.md（确认方案 + 专家意见）
     - analysis.md（技术可行性）
  2. 追加 proposal.md 第二章和第三章：
     - 问题陈述（痛点 + 根因）
     - 目标和成功指标表
     - 用户故事表（Story ID / 故事 / 优先级）
     - 验收标准表（AC编号 / 描述 / 类型 / 关联Story）
     - 不做范围清单
     - 关键假设与验证结果
  3. 保存为 {docs_dir}/proposal.md
```

**文件路径：** `docs/features/{feature-name}/proposal.md`

**【强制】追加 proposal.md 基线章节前，必须先读取模板文件 `{DOCS_REPO}/assets/templates/proposal.md`，严格按模板的章节结构、中文章节标题填充。不得自行改为英文结构或英文标题。**

**模板参考**：`{DOCS_REPO}/assets/templates/proposal.md`
- 基本信息表（需求ID / 关联原始需求 / 基线版本 / 确认人）
- 问题陈述（一段话概括痛点 + 根因 + 竞品差距）
- 目标和成功指标表（目标 / 指标 / 验证方式）
- 用户故事表
- 验收标准表（含正常/异常/兼容性反例）
- 不做范围清单
- 初始假设表（假设 / 类型 / 验证方式 / 负责人 / 状态）

### 不涉及项确认

主 Session 向用户展示需求涉及的各个维度，让用户逐项确认哪些是不涉及的：

#### 标准确认清单

| # | 维度 | 选项 | 说明 |
|---|------|------|------|
| 1 | 目标设备 | 全覆盖 / 指定设备 | 手机/平板/PC/2in1/智慧屏/手表/车机/IoT |
| 2 | OHOS 版本 | 全部 / 指定版本 | API Level 范围 |
| 3 | 性能指标 | 涉及 / 不涉及 | 是否有明确的性能基线要求 |
| 4 | 安全隐私 | 涉及 / 不涉及 | 沙箱/权限/数据安全 |
| 5 | 无障碍 | 涉及 / 不涉及 | 大字体/屏幕朗读/适老化 |
| 6 | 全球化 | 涉及 / 不涉及 | 多语言/镜像布局 |
| 7 | 1+8 设备差异 | 涉及 / 不涉及 | 是否需要逐设备填写差异表 |
| 8 | 兼容性 | 涉及 / 不涉及 | 对现有 API 的影响 |
| 9 | DFX（崩溃/ANR/日志） | 涉及 / 不涉及 | 稳定性相关设计 |
| 10 | 功耗 | 涉及 / 不涉及 | 电池/发热影响 |

用户确认后，将"不涉及"的维度标记为 N/A，传递给 Sub-3 (design-doc)，设计文档中对应章节只需填写"不涉及"即可。

### Phase 4: 设计文档

**spawn Sub-3：**

```python
sessions_spawn(
    task="""
    你是 ArkWeb 设计文档撰写者。请执行以下任务：

    1. 读取 skill 文件：.skills/arkweb-design-doc/SKILL.md
    2. 按 SKILL.md 的流程生成两个设计文档

    ## 确认的方案（来自决策 1）
    {confirmed_plan_details}

    ## 不涉及项确认
    以下维度已确认为"不涉及"，对应章节只需填写"不涉及"即可：
    {na_dimensions_list}

    ## 需求基线（读取此文件）
    docs/features/{feature-name}/proposal.md

    ## 代码分析结果（读取此文件）
    {analysis_dir}{date}-{feature}-analysis.md

    ## 参考资料（按需读取）
    - 架构参考：{references_dir}arkweb-architecture.md
    - ACE Engine 索引：{analysis_dir}arkweb-ace-engine-analysis.md
    - 兼容性检查：{WORK_HOME}/docs/api-compatibility-check-arkweb.md
    - brainstorm 文档：{docs_dir}{feature-name}/{date}-{feature}-brainstorm.md

    ## 知识库证据包（主 Session 已在 Phase 2 检索完成）

    以下是通过知识库降级策略检索到的证据，在设计文档中引用相关证据。

    {kb_evidence_package}

    **证据包持久化文件（上下文丢失时可从此文件恢复）**：
    {DOCS_REPO}/tmp/arkweb_kb_evidence_{timestamp}_{feature}.md

    ## 输出
    【强制】生成文档前，必须先读取以下模板文件，严格按模板的章节结构、中文章节标题、表格格式填充内容：
    1. `{DOCS_REPO}/assets/templates/requirement.md`
    2. `{DOCS_REPO}/assets/templates/design.md`
    不得自行改为英文结构或英文标题。

    按设计文档 skill 的产出规范，生成两个文档：
    1. requirement.md：需求基线评审文档
    2. design.md：架构设计文档

    保存到：docs/features/{feature-name}/

    requirement.md 必须包含：
    - 需求描述（功能范围 + 典型场景 + 验收标准）
    - 功能设计（ASCII 架构图 + 类图 + 时序图）
    - 接口设计（参数表 + 示例代码）
    - 设备矩阵（1+8 设备差异表）
    - DFX 六维度分析
    - 性能功耗设计
    - 安全隐私设计

    design.md 必须包含：
    - 设计元数据
    - 涉及仓和模块
    - 关键设计决策（ADR）
    - 设计骨架（架构图 + 骨架 Spec 拆分）
    - 风险和开放问题

    注意：不涉及项对应章节填写"不涉及"即可，无需展开。

    完成后回复两个文档的路径和结构摘要。
    """,
    mode="run",
    label="design-doc"
)
```

### Phase 5: 文档评审⭐ 必选

将原 Phase 3（技术评审）和 Phase 3.5（Checklist 规范性检视）合并为一次评审。Sub-4 同时执行技术评审和 14 条 Checklist 检视，产出一份统一的 review.md。

**spawn Sub-4：**

```python
sessions_spawn(
    task="""
    你是 ArkWeb 文档评审专家。请执行以下任务：

    1. 读取 skill 文件：.skills/arkweb-spec-review/SKILL.md
    2. 按 SKILL.md 的流程评审设计文档

    ## 待评审文档
    - requirement.md：{DOCS_REPO}/docs/features/{feature-name}/{date}-{feature}-requirement.md
    - design.md：{DOCS_REPO}/docs/features/{feature-name}/{date}-{feature}-design.md

    ## 代码分析结果（用于交叉验证）
    {analysis_dir}{date}-{feature}-analysis.md

    ## 参考资料（按需读取）
    - ACE Engine 索引：{analysis_dir}arkweb-ace-engine-analysis.md
    - WebWebView 分析：{analysis_dir}web-webview-analysis.md

    ## 评审维度

    ### Part A: 技术评审（原 Phase 3）
    1. 完整性检查（10 项）
    2. 一致性检查（6 项）
    3. 技术可行性检查（5 项）
    4. DFX 完整性（6 项）
    5. 文档规范（4 项）

    ### Part B: Checklist 规范性检视（原 Phase 3.5）
    按 14 条 Checklist 规则验证功能设计说明书的符合性，以资深软件设计质量分析师视角检视。

    ## 输出
    将评审报告保存到：
    {docs_dir}{feature-name}/{date}-{feature}-review.md

    报告必须包含：
    - 评审结果：通过 / 需修改 / 不通过
    - Part A 问题清单（🔴必须修改 / 🟡建议修改 / 🟢优秀实践）
    - Part B Checklist 检视结果（🔴必须修改 / 🟡建议修改 / ✅通过）
    - 统计数据（总检查项 / 通过 / 问题数）

    完成后回复文档路径和评审结果摘要。
    """,
    mode="run",
    label="spec-review"
)
```

### 🔀 决策 2: 评审决策（强制质量门禁）

```
主 Session:
  1. 读取 Sub-4 输出的 review.md
  2. 将评审结果呈现给用户：
     - Part A：🔴 必须修改项 + 🟡 建议修改项 + 🟢 优秀实践
     - Part B：Checklist 检视结果
     - 统计数据（总检查项 / 通过 / 问题数）
  3. 根据结果决定：

     ┌─ 有 🔴 必须修改项 ──────────────────────────────────────────────────┐
     │ a) 强制修复：必须修复所有 🔴 项后才能继续。                          │
     │    → 回到 Phase 4 修改设计文档（附评审报告 + 修复清单）           │
     │    → 修复后必须重新 spawn Sub-4 复审                           │
     │    → 复审仍有 🔴 → 继续修复，直到所有 🔴 清零                      │
     │    → 此路径不允许跳过                                          │
     ├──────────────────────────────────────────────────────────────────┤
     │ b) 回到需求/方案阶段（Phase 1 或 Phase 2）：                         │
     │    如果 🔴 问题不是文档层面的，而是涉及需求理解或方案设计：          │
     │                                                                   │
     │    → 回到 Phase 1（需求基线）：                                   │
     │      - 需求理解偏差、用户故事不完整、验收标准缺失                  │
     │      - 目标发行版本/优先级/范围定义错误                            │
     │      → 保留 brainstorm 和 code-analysis 结果（不需要重做）          │
     │      → 仅追加/修改 proposal.md 的需求基线部分                    │
     │                                                                   │
     │    → 回到 Phase 2（方案设计）：                                   │
     │      - 方案选型错误、架构设计不合理、接口设计有问题                  │
     │      - 多个方案都有严重缺陷，需要重新设计                          │
     │      → 保留 proposal.md 和 code-analysis 结果                   │
     │      → 重新 brainstorm 时附上：上次方案的问题 + 评审报告          │
     │                                                                   │
     │    → 判断依据（定性为主，数量为辅）：                             │
     │      - 问题性质 > 问题数量（一个关键架构 🔴 > 十个文档格式 🔴）     │
     │      - 🔴 涉及需求/方案/架构/接口 → 回到 Phase 1 或 2               │
     │      - 🔴 仅涉及文档格式/遗漏/描述 → Phase 4 修复即可              │
     │    → 回到 Phase 1 或 2 时，保留已有分析结果和评审记录               │
     ├──────────────────────────────────────────────────────────────────┤
     │ c) 仅 🟡 建议修改项 ───────────────────────────────────────────────┤
     │    → 询问用户：                                                  │
     │      1) 修改后继续 → 回到 Phase 4 修改 → 可选复审                │
     │      2) 接受现状继续 → 进入 Phase 6（记录为「有条件通过」）         │
     │      3) 回到需求/方案 → 回到 Phase 1 或 Phase 2（理由记录）         │
     ├──────────────────────────────────────────────────────────────────┤
     │ d) 全部通过（无 🔴，🟡 可选） ────────────────────────────────────┤
     │    → 进入 Phase 6                                                │
     │    → 如果有 🟡 未处理项，记录到 spec.md 的「已知限制」章节        │
     └──────────────────────────────────────────────────────────────────┘
```

### 评审决策判断依据

当评审结果为「需修改」时，主 Session 必须判断修复路径：

| 🔴 问题特征 | 建议路径 | 理由 |
|-------------|---------|------|
| 需求理解偏差 / 用户故事缺失 | **回到 Phase 1** | 需求基线有问题，brainstorm 基础不对 |
| 验收标准不完整 / 范围定义错误 | **回到 Phase 1** | Phase 3 需求基线需要修正 |
| 方案选型错误 / 架构不合理 | **回到 Phase 2** | 文档层面修复无法解决根本问题 |
| 接口设计与需求矛盾 | **回到 Phase 1** | 需求基线和方案都需要重新对齐 |
| 文档格式 / 章节遗漏 / 描述不清晰 | **Phase 4 修复** | 不涉及需求/方案变更 |
| 示例代码 / 参数表不完整 | **Phase 4 修复** | 补充即可 |
| DFX / 兼容性分析不充分 | **Phase 4 修复** | 补充分析即可 |

### 评审记录追溯

评审记录由 Sub-4（spec-review）的 review.md 承载，不额外修改 proposal.md。

每次评审决策后，review.md 追加评审决策记录：

```markdown
## 评审决策记录

### 评审 1（Phase 5）
- 日期：YYYY-MM-DD
- 评审结果：需修改（🔴 3 项 / 🟡 5 项 / 🟢 12 项）
- 决策：Phase 4 修复（文档层面问题，不涉及方案变更）
- 🔴 修改项：[简要列出]

### 评审 2（Phase 5 复审）
- 日期：YYYY-MM-DD
- 评审结果：有条件通过（🟡 2 项未处理）
- 决策：进入 Phase 6
- 🟡 未处理项：[简要列出，记录到 spec.md 已知限制章节]
```

> **注意：** review.md 是 Sub-4 的产出物，评审记录追加在 review.md 末尾即可，不需要新建文件。
> 如果决策为「回到 Phase 1 或 Phase 2」，在 proposal.md 中追加一条简要记录说明回退原因和日期。

> **修复回路：** 评审发现的问题可以回到 Phase 1（需求基线）、Phase 2（方案设计）或 Phase 4（设计文档）。修改后必须重新走 Phase 5 评审。不允许跳过 🔴 必须修改项直接进入 Phase 6。
>
> **防跳过机制：** 当 Sub-4 返回 🔴 必须修改项时，主 Session 必须明确展示修复方案并等待用户确认。不提供「忽略并继续」选项。

### Phase 6: 统一 Spec 生成⭐ 必选

评审通过后，spawn Sub-10 生成统一的 spec.md 和 task.md。spec.md 是 4 合 1 的结构化规格文档，作为 Sub-7（code-gen）的唯一 Spec 输入。task.md 是 AC→Task 追溯的执行计划。

**spawn Sub-10：**

```python
sessions_spawn(
    task="""
    你是 ArkWeb Spec 生成工程师。请执行以下任务：

    1. 读取 skill 文件：.skills/arkweb-spec-gen/SKILL.md
    2. 按 SKILL.md 的流程生成统一 Spec 和执行计划

    ## 输入文档（全部读取）
    - proposal.md：{DOCS_REPO}/docs/features/{feature-name}/proposal.md
    - requirement.md：{DOCS_REPO}/docs/features/{feature-name}/{date}-{feature}-requirement.md
    - design.md：{DOCS_REPO}/docs/features/{feature-name}/{date}-{feature}-design.md
    - review.md：{DOCS_REPO}/docs/features/{feature-name}/{date}-{feature}-review.md
    - analysis.md：{DOCS_REPO}/analysis/{date}-{feature}-analysis.md

    ## 评审遗留项
    如果 review.md 中有 🟡 未处理项，记录到 spec.md 的「已知限制」章节。

    ## 输出
    【强制】生成文档前，必须先读取以下模板文件，严格按模板的章节结构、中文章节标题填充内容：
    1. `{DOCS_REPO}/assets/templates/spec.md`
    2. `{DOCS_REPO}/assets/templates/task.md`
    不得自行改为英文结构或英文标题。

    1. spec.md（4 合 1：架构设计 / 接口规格 / 特性规格 / 任务规格）
       保存到：docs/features/{feature-name}/spec.md
    2. task.md（AC→Task 追溯 + Task 详情 + 停止条件）
       保存到：docs/features/{feature-name}/task.md

    完成后回复两个文档的路径和结构摘要。
    """,
    mode="run",
    label="spec-gen"
)
```

**主 Session 等待 Sub-10 完成：**
```
sessions_yield()
```

### Phase 7: 代码生成（Spec 驱动）

**spawn Sub-7：**

```python
sessions_spawn(
    task="""
    你是 ArkWeb 代码生成工程师。请执行以下任务：

    1. 读取 skill 文件：.skills/arkweb-code-gen/SKILL.md
    2. 按 SKILL.md 的流程生成实现代码

    ## 设计文档（读取这些文件）
    - requirement.md：{DOCS_REPO}/docs/features/{feature-name}/{date}-{feature}-requirement.md
    - design.md：{DOCS_REPO}/docs/features/{feature-name}/{date}-{feature}-design.md

    ## 统一 Spec（读取此文件）
    {docs_dir}{feature-name}/spec.md

    **重要：代码生成时优先依据 spec.md 中的结构化定义，设计文档作为上下文补充。接口签名、参数约束、行为场景必须与 Spec 一致。**

    ## 代码分析结果（读取此文件）
    {analysis_dir}{date}-{feature}-analysis.md

    ## 目标仓库
    - 路径：{SKILL_HOME}/
    - 分支：feat/{feature-name}

    ## 生成范围
    - 核心实现代码（.cpp / .h / .ts / .ets 等）
    - 单元测试代码
    - BUILD.gn 修改（如需要）

    ## 输出
    1. 生成计划（文件清单）
    2. 实现代码文件
    3. 单元测试
    4. 自验证报告

    完成后回复生成摘要和验证结果。
    """,
    mode="run",
    label="code-gen"
)
```

**主 Session 等待 Sub-7 完成：**
```
sessions_yield()
```

### 🔀 决策 3: 代码审查

```
主 Session:
  1. 读取 Sub-7 输出的验证报告
  2. 将生成摘要 + 验证结果呈现给用户
  3. 等待用户审查：
     a) 通过 → 进入 Phase 8（Committer 检视）
     b) 要求修改 → 重新 spawn Sub-7（附修改意见）
     c) 需要查看具体代码 → 展示关键文件内容
```

### Phase 8: Committer 检视

代码生成后，spawn Sub-8 以 Committer 视角检视代码质量。

#### Sub-8: committer-review

```python
sessions_spawn(
    task="""
    你是 ArkWeb 项目的 Committer。请对以下代码进行检视。

    1. 读取 skill 文件：.skills/arkweb-committer-review/SKILL.md
    2. 按 SKILL.md 的流程执行 Committer 检视

    ## 设计文档（读取这些文件）
    - requirement.md：{DOCS_REPO}/docs/features/{feature-name}/{date}-{feature}-requirement.md
    - design.md：{DOCS_REPO}/docs/features/{feature-name}/{date}-{feature}-design.md

    ## 生成代码目录
    {WORK_HOME}/implementation/{feature-name}/

    ## 代码分析结果（读取此文件）
    {analysis_dir}{date}-{feature}-analysis.md

    ## 输出
    将检视报告保存到：
    {docs_dir}{feature-name}/{date}-{feature}-committer-review.md

    完成后回复文档路径和检视结果摘要。
    """,
    mode="run",
    label="committer-review"
)
```

```
主 Session:
  1. 读取 Sub-8 输出的检视报告
  2. 呈现检视结果（问题清单 + 严重程度）
  3. 等待用户决定：
     a) 通过 → 进入 Phase 9（提交 PR）
     b) 要求修复 → 重新 spawn Sub-7（附检视报告）
```

### Phase 9: 提交 PR

**多仓库 PR 协调规则（强制遵守）：**

本项目的代码分布在 3 个仓库中，提交 PR 时必须遵循以下规则：

1. **Issue 分组**：同一层级的仓库共用一个 Issue，不同层级使用独立 Issue
   - 引擎层（chromium_src）→ 独立 Issue，创建在 `openharmony-tpc/chromium_src`
   - 框架层（web_webview + arkui_ace_engine）→ 共用一个 Issue，创建在 `openharmony/web_webview`

2. **PR 方向**：必须从 fork 指向上游原仓，禁止 fork 内部自合并
   - `{FORK_OWNER}/xxx:feat/xxx` → `openharmony(-tpc)/xxx:{base_branch}`
   - chromium_src 的 base 分支为 `132_trunk`，其他仓库为 `master`

3. **PR 模板**：创建 PR 前必须先读取目标仓库的 `PULL_REQUEST_TEMPLATE.md`（路径见 gitcode-pr skill），按模板格式填写 body，禁止使用自定义格式

4. **关联引用**：每个 PR 的 body 中必须包含关联 Issue 链接和其他两个仓库的 PR 链接

5. **提交流程**：先创建所有 Issue → 读取所有模板 → 创建所有 PR → 互相引用

**spawn Sub-9：**

```python
sessions_spawn(
    task="""
    你是 GitCode PR 提交助手。请执行以下任务：

    1. 读取 skill 文件：.skills/gitcode-pr/SKILL.md
    2. 按 SKILL.md 的流程执行提交流程

    ## 待提交文件
    {all_document_files_and_code_files}

    ## 提交信息
    - Issue 标题：feat: {feature-name} — {description}
    - Commit message: feat: {description}\n\n- {change_1}\n- {change_2}
    - PR body: 方案概述 + 评审记录 + Closes #{issue_number}
    - 分支名：docs/{feature-name}

    ## 仓库配置
    - 仓库：{owner}/{docs_repo}
    - 本地路径：{SKILL_HOME}/
    - Token：从环境变量读取（优先 `GITCODE_TOKEN`，回退 `GITLAB_TOKEN`）

    ## 输出
    1. Issue URL
    2. PR URL
    3. 提交状态

    完成后回复提交结果。
    """,
    mode="run",
    label="gitcode-pr"
)
```

```
主 Session:
  1. 读取 Sub-9 的提交结果
  2. 将 PR 信息呈现给用户
  3. 等待用户确认：
     a) 合并 → 执行合并 API
     b) 修改 → 重新 spawn Sub-9
     c) 拒绝 → 结束
  4. 合并完成 → ✅ 输出最终摘要
```

---

## 决策点汇总

| # | 决策 | 时机 | 可选操作 | 默认行为 |
|---|------|------|---------|---------|
| 1 | 确认方案 | Phase 2（Sub-1 + Sub-2 完成） | 选方案 / 修改 / 补充信息 | 等待用户 |
| 2 | 评审决策 | Phase 5（Sub-4 完成，含技术评审 + Checklist） | 🔴强制修复 / 回到需求(Phase 1) / 回到方案(Phase 2) / 🟡可选修复 / 有条件通过 | 🔴不可跳过，🟡询问用户 |
| 3 | 代码审查 | Phase 7（Sub-7 完成） | 通过 / 要求修改 / 查看代码 | 等待用户 |

> 决策点从 9 个缩减为 3 个。原决策点精简为 3 个：方案确认（Phase 2 后）、评审结果（Phase 5 后）、代码审查（Phase 7 后）。Spec 审阅决策点移除（spec 是机器消费的，不需要人工审）。Committer 检视和 PR 提交作为流程内步骤处理。决策 2 新增「回到需求/方案设计」路径和防跳过机制。

---

## 数据流

```
主 Session 直接生成（不通过 subagent）:
  Phase 1:   proposal.md 第一章（原始需求录入）
  Phase 1.5: proposal.md 第二章（澄清记录，多轮对话填充）
  Phase 3:   proposal.md 第三章（需求基线，追加到同一文件）
  Phase 2 Step 2.0: 知识库检索 → 产出「知识库证据包」（注入到后续所有 subagent）
  Phase 2 Step 2.0: 知识库证据包持久化 → Write 到 {DOCS_REPO}/tmp/arkweb_kb_evidence_{timestamp}_{feature}.md
  Phase 6:   spec.md（统一规格文档，4 合 1：架构设计/接口规格/特性规格/任务规格）

专家团（主 Session 直接调度，并行 spawn，接收知识库证据包）
  → 按相关度权重筛选专家（🟢核心/🟡关联/⚪旁听，旁听超 5 个跳过）
  → 各专家输出意见 → 主 Session 收集汇总
  → 生成「专家团讨论纪要」（含权重标注 + 共识/分歧/采纳情况）

Sub-1 (brainstorm)
  ← 输入: 专家团讨论纪要 + 用户需求 + 约束 + code-analysis 路径 + 知识库证据包
  → 读取专家纪要，将采纳的意见融入方案设计
  → 写入: docs/features/{feature-name}/{date}-{feature}-brainstorm.md（含专家讨论纪要 + 权重标注）
  → 主 Session 读取 → 呈现给用户 → 决策 1

Sub-2 (code-analysis)
  → 数据源：oh-chromium-knowledge + oh-ai-full-design（🥇）→ DeepWiki MCP（🥈）→ 本地文档（🥉）→ 克隆仓库（🏅）
  → 写入: analysis/{date}-{feature}-analysis.md
  → Sub-3 读取（作为参考资料）
  → Sub-4 读取（作为交叉验证）

Sub-3 (design-doc)
  → 读取: proposal.md + brainstorm.md + analysis.md + 不涉及项确认 + 参考资料
  → 写入: docs/features/{feature-name}/{date}-{feature}-requirement.md + {date}-{feature}-design.md
  → Sub-4 读取（作为评审对象）
  → Sub-7 读取（作为代码生成的依据）
  → Sub-8 读取（作为 Committer 检视的依据）

Sub-4 (spec-review) — v5 合并了原 Sub-4.5 的 Checklist 检视
  → 读取: requirement.md + design.md + analysis.md
  → 写入: docs/features/{feature-name}/{date}-{feature}-review.md
  → 主 Session 读取 → 呈现给用户 → 决策 2

Sub-10 (spec-gen)
  ← 读取: proposal.md + requirement.md + design.md + analysis.md + review.md
  → 写入: docs/features/{feature-name}/spec.md（统一规格文档，4 合 1）+ task.md
  → Sub-7 读取（作为代码生成的主要依据）

Sub-7 (code-gen)
  → 读取: requirement.md + design.md + spec.md + analysis.md
  → 写入: 实现代码 + 单元测试 + BUILD.gn
  → 主 Session 读取验证报告 → 呈现给用户 → 决策 3

Sub-8 (committer-review)
  → 读取: requirement.md + design.md + analysis.md + 生成代码
  → 写入: docs/features/{feature-name}/{date}-{feature}-committer-review.md

Sub-9 (gitcode-pr)
  → 读取: 所有文档文件 + 所有代码文件
  → 写入: GitCode Issue + PR

完整文档产出链路（核心）:
  proposal.md(Ch1) → [Phase 1.5 澄清] → proposal.md(Ch2) → brainstorm.md → requirement.md + design.md → review.md
  → spec.md → 实现代码 → committer-review.md → Issue + PR
  proposal.md(Ch3 需求基线) 在决策 1 后追加
```

---

## ⚠️ 问题预防规则

在执行流程时，必须遵守以下规则：

### 规则 1：需求澄清不可跳过
- Phase 1 生成 proposal.md 第一章后，**必须**进入 Phase 1.5 需求澄清
- 不允许用"默认值""推测""大概率"代替用户确认
- 每轮澄清控制在 3-5 个核心问题，记录所有结论到 proposal.md 第二章
- 澄清完成条件全部满足后才能进入 Phase 2

### 规则 2：subagent 任务描述要明确文件路径
- 在 subagent task 中明确写明"保存到 X 路径"，不要写"保存文档"这种模糊描述
- 如果要生成多个文件，在 task 中列出每个文件的完整路径

### 规则 3：commit 前检查 git diff
- 在 git commit 前，执行 `git diff --stat` 确认改动范围
- 检查是否有意外文件被修改或删除

---

## 模式切换

| 条件 | 模式 |
|------|------|
| `sessions_spawn` 可用 + 复杂需求 | **模式 A**（Subagent 编排） |
| `sessions_spawn` 不可用 | 模式 B（主 session 串行调用 skill） |
| 用户要求串行 | 模式 B |

模式 B 下，主 session 依次 read 各 SKILL.md 并按流程执行，每个 skill 完成后在当前 session 内做决策。

---

## 参考资源

| 文档 | 路径 |
|------|------|
| ACE Engine 分析 | `analysis/arkweb-ace-engine-analysis.md` |
| WebWebView 分析 | `analysis/web-webview-analysis.md` |
| 架构参考 | `references/arkweb-architecture.md` |
| 兼容性检查 | `docs/api-compatibility-check-arkweb.md` |
| 设备矩阵 | `references/device-matrix.md` |
| 竞品分析 | `references/competitor-analysis.md` |

## 快速入口

| 用户意图 | 启动的 Subagent |
|---------|----------------|
| "帮我分析这个需求" | 专家团 + Sub-1 brainstorm + Sub-2 code-analysis（并行 → 收集 → brainstorm） |
| "生成设计文档" | Sub-3 design-doc |
| "评审这个文档" | Sub-4 spec-review（含 Checklist 检视） |
| "生成代码" | Sub-7 code-gen |
| "Committer 检视" | Sub-8 committer-review |
| "分析 xxx 仓库" | Sub-2 code-analysis |
| "提交到 GitCode" | Sub-9 gitcode-pr |
| "完整流程" | 专家团 + 8 个 subagent + 3 个决策点 |
