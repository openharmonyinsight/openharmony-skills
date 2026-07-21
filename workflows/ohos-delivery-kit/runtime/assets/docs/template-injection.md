# Template Injection

## 目标

本文件定义 `ohos-delivery-kit` 的模板强制注入机制。核心问题是：

**如何在插件生成过程中，让 OH 定制章节成为自然产出而非事后补填，同时做到开发者无感。**

原则：

- 约束前置到生成阶段，不做事后大规模改写
- 能静默的不半自动，能半自动的不完全手动
- 模板内容精准供给，防止上下文膨胀
- 模板只承载 artifact 质量约束；skill/命令层只承载路由、上下文加载、fallback 和平台差异

## 内容归属

| 内容 | 归属 | 示例 |
|------|------|------|
| 必需章节、表头、frontmatter、traceability 字段 | 模板层 + `core/contracts/artifacts.yaml` | `target_release`, AC, code mapping |
| 阶段顺序、active change 选择、profile 检测 | skill/命令层 | `using-odk`, `odk-plan` |
| 插件桥接、输出重定向、fallback | adapter + skill/命令层 | `core/adapters/openspec.yaml`, `odk-ops-propose` |
| Claude/Codex/OpenCode 路径变量和命令前缀 | packaging 层 | `${CLAUDE_PLUGIN_ROOT}`, `${CODEX_PLUGIN_ROOT}`, OpenCode commands |

这个边界保证 skill 精简不会降低最终交付质量：质量约束仍由模板、contract 和 validator 承担。

平台分发层的同一边界说明见 `docs/designs/source-boundary-and-distribution.md`；本文只展开模板注入时机和插件适配方式。

---

## 三种注入模式

```
┌──────────────────────────────────────────────────────────────┐
│                      开发者可见层                             │
│   slash command / skill 调用（开发者只看到阶段语义）           │
├──────────────────────────────────────────────────────────────┤
│                      注入调度层                               │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│   │ Mode A        │  │ Mode B        │  │ Mode C        │       │
│   │ Schema/Template│  │ Skill 包装    │  │ Hooks 拦截    │       │
│   │ 覆盖          │  │              │  │              │       │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│          │                 │                 │                │
│  适用:   │          适用:   │          适用:   │               │
│  OpenSpec│          Super-  │          所有插件  │              │
│  MatrixSpec│         powers  │          (兜底)    │              │
├──────────────────────────────────────────────────────────────┤
│                      注入内容层                               │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│   │ L1 静默   │  │ L2 半自动 │  │ L3 手动   │                  │
│   │ 上下文/规则│  │ 模板预填  │  │ 人工确认  │                  │
│   └──────────┘  └──────────┘  └──────────┘                  │
└──────────────────────────────────────────────────────────────┘
```

### 模式选择矩阵

| 插件 | 推荐模式 | 为什么 |
|------|---------|--------|
| OpenSpec | Mode A (Schema Override) | 原生支持三级 schema 解析，CLI 自动加载项目级 schema |
| MatrixSpec | Mode A (Template Override) | 原生支持 config.yaml 指定模板路径 |
| Superpowers | Mode B (Skill Wrapper) | 无原生 schema/template 系统；通过包装层注入 |
| 自定义/其他 | Mode C (Hooks Intercept) | 兜底方案，PreToolUse Hook 注入上下文 |

---

## 注入模式 A: Schema/Template 覆盖

适用: OpenSpec, MatrixSpec

### A.1 OpenSpec: Schema 覆盖

OpenSpec 的三级 schema 解析链：

```
project-local (openspec/schemas/<name>/)  ← kit 在此层注入
    ↓ 未找到
user-override ($XDG_DATA_HOME/openspec/schemas/)
    ↓ 未找到
package-built-in (<OpenSpec>/schemas/)
```

Kit 在业务仓初始化时放置：

```
openspec/schemas/ohos-spec-driven/
├── schema.yaml
│     artifacts:
│       proposal: { output: proposal.md, template: proposal.md, requires: [] }
│       specs:    { output: specs/**/*.md, template: spec.md,   requires: [proposal] }
│       design:   { output: design.md,   template: design.md,   requires: [proposal, specs] }
│       tasks:    { output: tasks.md,     template: tasks.md,   requires: [specs, design] }
│
└── templates/
    ├── proposal.md    ← sections declared by core/contracts/artifacts.yaml
    ├── spec.md        ← sections declared by core/contracts/artifacts.yaml
    ├── design.md      ← sections declared by core/contracts/artifacts.yaml
    └── tasks.md       ← execution-plan sections declared by core/contracts/artifacts.yaml
```

模板来源于 kit 自身的模板结构：

```
core/templates/ai/
├── proposal.md
├── design.md
├── spec.md
└── execution-plan.md

core/templates/review/
├── review-spec-compliance.md
├── review-code-quality.md
└── review-verification.md
```

然后在 `openspec/config.yaml` 中：

```yaml
schema: ohos-spec-driven
context: |
  ## OpenHarmony 约束（本变更全程适用）
  - target_release: 7.0
  - 所有 spec 输出必须包含验证映射和兼容性声明
  - AC 必须独立编号以支持追溯

rules:
  proposal:
    - "必须包含非目标（Non-Goals）章节"
    - "必须包含不涉及项确认（8 维度 N/A 表）"
    - "必须显式声明 target_release"
  specs:
    - "每组 AC 必须独立编号（AC-001, AC-002...）"
    - "必须包含兼容性声明章节"
  design:
    - "必须包含模块影响分析（子系统/仓库/模块表）"
    - "必须包含验证思路章节"
  tasks:
    - "每个 Task 必须关联 AC 编号"
    - "每个 Task 必须填写代码范围列"
    - "必须包含 AC-Task 追溯汇总表"
```

**注入时机**: 每次 `openspec instructions <artifact>` 被调用时，`context` 和 `rules` 自动注入到返回的指令中，`template` 自动使用 kit 定制版本。

**对开发者可见度**:
- `context` 内容 → L1 静默（注入到 AI 系统指令，开发者无需主动操作）
- `rules` 内容 → L1 静默（AI 需遵循，开发者无需主动操作）
- 模板章节 → L2 半自动（AI 按模板生成，开发者确认）

### A.2 MatrixSpec: 模板覆盖

MatrixSpec 的模板位于 `<MatrixSpec安装路径>/templates/delta/`。业务仓通过 `.matspec-cli/config.yaml` 覆盖模板路径。

Kit 在业务仓初始化时放置覆盖模板：

```
core/templates/ai/
├── proposal.md        ← MatrixSpec 原生结构 + 「不涉及项确认」(8 维度 N/A)
├── spec.md            ← + 「兼容性声明」「验证映射」
├── design.md          ← + 「验证思路」
└── execution-plan.md  ← + 「AC-Task 追溯表」「代码范围列」
```

`.matspec-cli/config.yaml`:

```yaml
templates:
  delta:
    proposal: core/templates/ai/proposal.md
    delta-spec: core/templates/ai/spec.md
    delta-design: core/templates/ai/design.md
    tasks: core/templates/ai/execution-plan.md
```

**注入时机**: `matspec start <id>` 通过 config.yaml 读取模板路径，加载 kit 覆盖模板。

**对开发者可见度**: L2 半自动。开发者在 IDE/Agent 中看到的是已包含 OH 章节的模板。

---

## 注入模式 B: Skill 包装层

适用: Superpowers

Superpowers 无原生 schema/template 系统，通过 thin wrapper skill 实现注入。

### B.1 架构

```
ohos-brainstorming (wrapper skill)
  ├── Step 1: 加载 kit 上下文
  │     - 读取 kit proposal/design 章节要求 (最小章节清单)
  ├── Step 2: 调用 Superpowers brainstorming
  │     - 传入 kit 章节清单作为 spec 结构约束
  │     - 要求输出包含 OH 必需要素
  ├── Step 3: 收口
        - 从 brainstorming 输出提取内容到 kit 标准文件
        - 标记缺失项供用户确认
```

### B.2 Wrapper Skill 定义

```markdown
# ohos-brainstorming

## 目标
对 OpenHarmony 需求进行方案探索，产出符合 kit 归档规范的 spec 初稿。

## 前置
1. 确认变更 ID（格式: issue-<issue-number>-<slug>）

## 流程

### Step 1: 初始化
- 执行 ohdk init issue-12345-xyz-focus，创建 .codespec/changes/issue-12345-xyz-focus/ 骨架

### Step 2: 方案探索（调用 Superpowers brainstorming）
- 加载 skills/brainstorming/SKILL.md
- 在 brainstorming prompt 中注入以下约束：
  - 输出结构必须覆盖：
    1. 背景与问题（kit proposal §1）
    2. 目标与非目标（kit proposal §2-3）
    3. 方案概述与关键设计决策（kit design §2, §4）
    4. 用户故事与验收标准（kit spec §2-3）
    5. 不涉及项确认（kit proposal §6，8 维度 N/A）

### Step 3: 转写与收口
- 将 brainstorming 输出拆分/转写到以下文件：
  - .codespec/changes/issue-12345-xyz-focus/proposal.md
  - .codespec/changes/issue-12345-xyz-focus/design.md
  - .codespec/changes/issue-12345-xyz-focus/spec.md (用户故事/AC 部分)
- 对每个文件做章节完整性检查
- 列出仍缺失的字段/章节，提示用户补充

### Step 4: 门禁
- 检查 gate-checklist.md Stage 1 各项
- 输出 gate 结果到 .codespec/changes/issue-12345-xyz-focus/evidence/gates/define.md
- 等待用户批准
```

### B.3 Review 回填 Wrapper

Superpowers 的 review 产物是会话内瞬时内容。需要 wrapper 在 review 完成后自动持久化：

```markdown
# ohos-review (wrapper)

## 流程
1. 调用 Superpowers requesting-code-review skill
2. 将 code review 报告（Strengths, Issues, Recommendations, Assessment）写入:
   .codespec/changes/issue-12345-xyz-focus/evidence/reviews/code-review-YYYYMMDD.md
3. 额外检查：
   - 代码是否符合 spec AC（逐项）
   - 代码范围是否在 execution-plan 定义的范围内
   - 是否有超出 plan 的额外实现
4. 将检查结果写入:
   .codespec/changes/issue-12345-xyz-focus/evidence/reviews/spec-compliance-YYYYMMDD.md
```

---

## 注入模式 C: Hooks 拦截（兜底）

适用: 所有插件，作为辅助机制

### C.1 PreToolUse Hook: 文件写入拦截（可选增强）

当 AI agent 写入 spec 相关文件时，自动检查目标路径和章节完整性：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "targets": [".codespec/**/*.md"],
        "command": "ohdk check-chapters ${FILE_PATH} --level draft"
      }
    ]
  }
}
```

这是可选增强，MVP 不必须。

---

## 分级注入清单

### L1 静默注入（AI 上下文，无需开发者主动操作）

| 注入内容 | 来源 | 注入方式 | 注入时机 |
|---------|------|---------|---------|
| target_release | kit context | Schema context/rules / Hook | 会话启动 |
| 不涉及项 8 维度模板 | kit rules | Schema context/rules | 每个 artifact 生成时 |
| AC 编号规则 | kit rules | Schema context/rules | spec 生成时 |
| 代码映射格式要求 | kit rules | Schema context/rules | execution-plan 生成时（AC 到 Task 追溯 + 代码范围映射） |

### L2 半自动注入（AI 生成，开发者确认）

必需 artifact、必需章节和条件章节以 `core/contracts/artifacts.yaml` 为准；模板正文骨架以
`core/templates/ai/` 为准。本表只说明注入类型，不重复维护章节数量。

| 注入内容 | 来源 | 注入方式 |
|---------|------|---------|
| proposal 章节标题 | kit 模板 + `core/contracts/artifacts.yaml` | Schema template / Wrapper skill prompt |
| spec 章节标题 | kit 模板 + `core/contracts/artifacts.yaml` | Schema template / Wrapper skill prompt |
| design 章节标题 | kit 模板 + `core/contracts/artifacts.yaml` | Schema template / Wrapper skill prompt |
| execution-plan 章节标题 | kit 模板 + `core/contracts/artifacts.yaml` | Schema template / Wrapper skill prompt |
| evidence/gates Stage 门禁 checklist | gate-checklist.md / review-gates policy | 每阶段结束时 |

### L3 手动注入（开发者手动填写，AI 可提示但不可自动决定）

| 注入内容 | 说明 |
|---------|------|
| proposal 不涉及项确认 | 8 维度 N/A 需人类逐项确认 |
| review 最终决策 | Approved/ChangesRequested/Blocked |

---

## 上下文防膨胀策略

模板强制注入面临一个核心矛盾：**约束越多，上下文越长，AI 生成质量反而下降。**

### 策略 1: 模板分层加载

```
完整模板 → 仅第一阶段 (proposal/intake) 完整呈现

后续阶段:
  spec 阶段:   proposal 摘要(≤10行) + spec 模板章节清单
  design 阶段: proposal 摘要(≤10行) + spec 摘要(≤10行) + design 模板章节清单
  plan 阶段:   spec AC 列表 + plan 模板章节清单
  review 阶段: AC 列表 + Task 列表 + code_refs + review checklist
```

**关键**: 传递的是「摘要」而非「全文」。AI 如需完整上下文，可主动读取上一阶段文件。

### 策略 2: 精确摘要传递

阶段间传递格式（每阶段 ≤15 行）:

```markdown
## 上游摘要 (proposal → design)
- id: issue-12345-xyz-focus
- 目标: [一句话]
- 非目标: [一句话]
- 关键 AC: AC-001 [一句话], AC-002 [一句话], AC-003 [一句话]
- 不涉及: [已 N/A 的维度列表]
- 需关注: [额外约束]
```

### 策略 3: 渐进式模板深度

模板提供最小章节标题作为骨架，AI 按需展开。不预先提供「完整模板 + 填写指南 + 正例 + 反例」的长篇模板。

```
推荐 (精简):
## 背景与问题
## 目标
## 非目标
## 验收基线
## 不涉及项确认

不推荐 (膨胀):
## 背景与问题
<!-- 请在此描述当前面临的业务问题或技术挑战。建议包含以下要素：
  1. 现状是什么
  2. 为什么现状不够好
  3. 有哪些量化数据支撑
  ...
-->
```

AI 已知如何撰写这些章节——模板只需提供**结构签名**，不需要长篇填写说明。

### 防膨胀检查清单

| 检查项 | 阈值 |
|--------|------|
| 单阶段注入上下文总行数 | ≤ 80 行 |
| 上游摘要传递行数 | ≤ 15 行 |
| 模板章节骨架行数（不含 AI 生成内容） | ≤ 30 行 |

---

## 开发者体验总览

从开发者视角，整个流程的感知：

```
$ /odk-propose "增加 ArkUI 组件 XYZ 的焦点管理能力"
                    │
                    ▼
          [系统自动]
          - ohdk init issue-12345-xyz-focus
          - 创建 .codespec/changes/issue-12345-xyz-focus/ 骨架
          - 选择模式: kit + OpenSpec + Superpowers
                    │
                    ▼
          [OpenSpec 自动使用 ohos-spec-driven schema]
          - proposal.md 生成 (已含非目标、不涉及项确认)
          - design.md 生成 (已含模块影响、验证思路)
          - spec.md 生成 (已含 AC 编号、验证映射、兼容性声明)
                    │
                    ▼
          [Superpowers brainstorming 补充探索]
          - 探索 OpenSpec 未覆盖的边界场景
          - 回填到 proposal/spec 补充章节
                    │
                    ▼
          开发者确认: target_release / 不涉及项确认
                    │
                    ▼
          [Superpowers writing-plans]
          - execution-plan.md 生成 (已含 AC-Task 追溯、代码范围)
                    │
                    ▼
          [Superpowers TDD + review]
          - TDD 测试 → 代码映射证据
          - code review → evidence/reviews/code-review-*.md
          - spec compliance check → evidence/reviews/spec-compliance-*.md
                    │
                    ▼
          ohdk validate → 合规检查 → 归档
```

开发者看到的是统一命令 `/odk-propose`、`/odk-design`、`/odk-plan`、`/odk-review`、`/odk-validate`。

开发者不需要显式知道：
- 底层用的是 OpenSpec 还是 Superpowers
- 模板是怎么注入的
- OH 约束在什么时候被检查

开发者需要显式确认的只有：
- target_release（一次性，在 proposal 阶段）
- 不涉及项确认（8 维度 N/A）
- 各阶段人工审批（gate check）

这就是「无缝无感」的目标状态。
