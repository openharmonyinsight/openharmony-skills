# 业务代码仓 Spec 目录结构

> 目标：在不干扰源码目录的前提下，让每个变更的交付件、过程证据和提交记录都能长期追溯。
> 目录结构与 ohos-delivery-kit 对齐，采用 `.codespec/changes/issue-<number>-<slug>/` 作为统一归档路径。
> 仓内最小真实样例见源仓 `examples/archive-shape/.codespec/`。

## 顶层目录

业务代码仓建议只新增一个顶层目录：

```text
.codespec/
├── README.md
├── registry.md
├── profile.yaml              # (可选) 子系统 profile 声明
├── changes/
├── decisions/
├── migrations/
├── release-views/
├── shared/
└── archive/
```

| 目录 | 用途 |
|------|------|
| `README.md` | 本仓 Spec 使用说明、工具命令、流程级别 |
| `registry.md` | 全局索引，记录所有变更的状态和关系 |
| `profile.yaml` | (可选) 显式声明子系统 profile，如 `profiles: ["arkui"]` |
| `changes/` | 活跃变更交付件（Feature、Bugfix 等），每条对应一个 issue |
| `decisions/` | 跨变更共享的 ADR |
| `migrations/` | 存量设计迁移计划、旧文档映射、新旧模板差异 |
| `release-views/` | 按 OpenHarmony 发行版本生成或维护的视图，不作为变更身份来源 |
| `shared/` | 跨需求共享的术语、上下文包、验证基线 |
| `archive/` | 已废弃、已合并或被替代的旧规格 |

## 变更目录

> 与 ODK 契约一致：每条变更对应一个 `issue-<number>-<slug>` 目录，交付件 name 和最小章节见 ohos-delivery-kit 的 `docs/contracts.md`。

### 标准变更目录（Feature / 存量补规格 / 增强）

```text
.codespec/changes/
└── issue-12345-notification-category/
    ├── proposal.md               # YAML frontmatter 承载 target_release
    ├── manifest.md               # [spec-for-ai 扩展] 元数据、code_refs、commits
    ├── lineage.md                # 新设计/存量设计/迁移设计判断依据
    ├── design.md
    ├── spec.md
    ├── execution-plan.md         # 含 Task 列表和 Task 详情卡
    ├── task/                     # [可选] 独立 task 文件（超 3000 行阈值时拆分）
    │   ├── TASK-001-api-model-field.md
    │   └── TASK-002-serialization-compat.md
    └── evidence/                 # [可选] 过程证据
        ├── reviews/
        │   ├── spec-compliance-YYYYMMDD.md
        │   ├── code-review-YYYYMMDD.md
        │   └── verification-YYYYMMDD.md
        ├── checks/
        │   ├── check-proposal.md
        │   ├── check-spec.md
        │   ├── check-design.md
        │   └── check-execution-plan.md
        └── retrospectives/
            └── 20260423-iteration-01.md
```

最小归档文件（必须）：

| 文件 | 作用 | ODK 契约 |
|------|------|---------|
| `proposal.md` | 需求输入、澄清与基线，YAML frontmatter 承载 `target_release` | ✅ 必需 |
| `design.md` | Feature 级设计 | ✅ 必需（简单变更可标记简化） |
| `spec.md` | 用户可见行为、AC、兼容性和测试追溯 | ✅ 必需 |
| `execution-plan.md` | AI 实施计划和 Task 拆解 | ✅ 必需 |
| `spec-for-validation.md` | Profile-defined Spec for Validation 条件旁路产物；对外行为、验证点及 Profile 专项分析 | 支持该能力的 Profile 显式触发时必需 |

spec-for-ai 扩展文件（可选但推荐）：

| 文件 | 作用 |
|------|------|
| `manifest.md` | 机器可读元数据、code_refs、commits、profile 声明 |
| `lineage.md` | 新设计/存量设计/迁移设计判断依据 |

### Bugfix 目录

```text
.codespec/changes/
└── issue-67890-notification-lost-after-sleep/
    ├── proposal.md               # YAML frontmatter 承载 target_release
    ├── manifest.md
    ├── bugfix.md
    ├── regression-test.md
    ├── links.md
    └── evidence/
        ├── reviews/
        └── checks/
```

`links.md` 必须记录：

| 关系 | 示例 |
|------|------|
| 修复哪个 Feature | `related: [issue-12345]` |
| 影响哪些 Task | `related_tasks: [TASK-002]` |
| 引入或暴露哪个 ADR | `related_decisions: [ADR-20260422-001]` |
| 对应提交 | `commits: [9956fda]` |
| 对应 issue | `source_issue: ISSUE-NOTIFY-2026-047` |

Feature 侧也必须在 `manifest.md` 或 `lineage.md` 反向记录该 bugfix，避免只在 bugfix 目录单向可见。

## 命名规则

### 目录命名

| 类型 | 格式 | 示例 |
|------|------|------|
| 变更目录（已关联 issue） | `issue-<number>-<slug>` | `issue-12345-notification-category` |
| 变更目录（未关联 issue） | `draft-<yyyymmdd>-<slug>` | `draft-20260422-notification-category` |
| Task | `TASK-NNN-short-slug` | `TASK-002-serialization-compat` |
| ADR | `ADR-YYYYMMDD-NNN-short-slug` | `ADR-20260422-001-category-storage` |
| Iteration | `YYYYMMDD-iteration-NN.md` | `20260423-iteration-01.md` |

规则：

- **目录命名与 ODK ID 规则一致**：`issue-number` 为源码平台（GitCode 等）的 issue ID；`short-slug` 使用小写英文、数字和连字符，不超过 40 字符。
- 变更目录名不包含目标发行版本，避免交付版本变更导致路径大规模移动。
- `draft-<yyyymmdd>-<slug>` 用于尚未关联 issue 的草稿，关联后通过 `odk-link-issue` 重命名为 `issue-<number>-<slug>`。
- 目标发行版本写入 `proposal.md` 的 YAML frontmatter `target_release` 字段。
- 审批状态只写在 `evidence/checks/` 和 frontmatter 中。
- 变更类型（feature/bugfix）由 `manifest.md` 的 `type` 字段承载，不在目录路径中区分。

## 发行版本关联

目标发行版本是可变交付属性，不是 Feature 身份的一部分。需求进入 Phase 1 (Define) 时必须给出初始版本判断，需求基线时必须确认或标记为 `undecided`，后续 Specify / Design / Plan 只引用 `proposal.md` 的 target_release frontmatter，不在正文里复制硬编码版本。

单一事实源：

```yaml
target_release:
  id: OpenHarmony-6.0-Release
  name: OpenHarmony 6.0
  label: OpenHarmony 6.0 Release
  release_note: OpenHarmony-v6.0-release.md
  status: proposed | committed | changed | deferred
  source: requirement | release-planning | sig-decision
  decided_by: "[Owner/SIG/Role]"
  decided_at: 2026-04-22
  change_policy: "Only update proposal.md target_release frontmatter; append release_change_log to manifest.md as history."
```

引用规则：

| 文档 | 写法 |
|------|------|
| `proposal.md` | 记录初始目标版本，来源为需求方或项目管道；基线阶段确认版本是否已 committed |
| `design.md` | 引用 `proposal.target_release.id`，不得复制具体版本号作为事实源 |
| `spec.md` | 引用 `proposal.target_release.id`，只描述版本相关兼容约束 |
| `execution-plan.md` | 引用 `proposal.target_release.id`，用于生成 release view 和验证计划 |
| `registry.md` | 展示 `target_release.id` 的快照，可由工具从 proposal frontmatter 生成 |

如果交付大版本因优先级、项目管道或 SIG 决策变化，需要从 `OpenHarmony-6.0-Release` 调整到 `OpenHarmony-6.1-Release`，只修改对应变更的 `proposal.md` target_release frontmatter（变更历史追加到 `manifest.md` 的 `release_change_log`）。目录名、稳定 ID、Task ID、提交引用不变。

## Frontmatter 基线

每个 `manifest.md` 必须包含：

```yaml
---
id: issue-12345
type: feature
title: Notification category
spec_schema: ohos-sdd/v1
profile: none | arkweb | arkui | arkgraphic | arkdata | security-sensitive | custom
release_change_log:
  - from: unassigned
    to: OpenHarmony-6.0-Release
    reason: Initial baseline decision
    decided_by: "[Owner/SIG/Role]"
    decided_at: 2026-04-22
complexity: standard
lineage: new | legacy | migrated | new-on-legacy | bugfix-on-feature
status: draft | approved | implementing | verifying | done | archived
owner: ""
source_issue: ""
created_at: 2026-04-22
updated_at: 2026-04-22
related: []
related_tasks: []
related_decisions: []
code_refs: []
commits: []
---
```

`profile` 规则：

| 值 | 含义 |
|----|------|
| `none` | 不使用子系统 profile，仅使用通用流程 |
| `arkweb` / `arkui` / `arkgraphic` / `arkdata` | 命中本仓已有 profile |
| `security-sensitive` | 命中后续安全专项 profile |
| `custom` | 业务仓本地自定义 profile，需在 `README.md` 或 `shared/` 中解释来源 |

要求：

- `profile` 不是强制字段，但一旦命中子系统 profile，必须在 `manifest.md` 写明
- `profile` 的值必须能解析到本仓或业务仓约定的 profile 定义
- `/ohos-review` 应校验 `manifest.profile`、`lineage`、`target_release` 与实际目录和文档是否一致

`lineage` 是区分新旧设计的关键字段：

| 值 | 含义 | 必须补充 |
|----|------|----------|
| `new` | 全新设计，从本流程产生 | 完整 Phase 1-4 记录 |
| `legacy` | 存量行为补规格 | 源码事实、旧文档引用、兼容边界 |
| `migrated` | 旧设计迁移到新模板 | 原文档路径、迁移日期、差异说明 |
| `new-on-legacy` | 新需求建立在存量能力上 | 增量目标、存量约束、兼容性 |
| `bugfix-on-feature` | 缺陷修复关联某 Feature | 关联 Feature、根因、回归测试 |

## Lineage 文件

`lineage.md` 用于让开发者和 Agent 一眼识别“这是新设计还是历史沉淀”。

```markdown
# Lineage

| 字段 | 值 |
|------|----|
| Lineage | new-on-legacy |
| Target Release | `proposal.target_release.id` |
| Source | existing code + new requirement |
| Original Docs | docs/notification/category-design-v0.md |
| Source Code Evidence | services/notification/... |
| Compatibility Boundary | Existing notification APIs must remain source compatible |
| Migration Status | partially migrated |
| Supersedes | LEGACY-DESIGN-20250115-notification-filter |
| Superseded By | - |
```

Agent 必须先读取 `manifest.md` 和 `lineage.md`，再决定生成新文档、补齐旧文档，还是做迁移。

## Registry 索引

`.codespec/registry.md` 维护全局表：

```markdown
| ID | Type | Title | Release | Profile | Lineage | Status | Related | Path |
|----|------|-------|---------|---------|---------|--------|---------|------|
| issue-12345 | feature | Notification category | OpenHarmony-6.0-Release | arkui | new-on-legacy | implementing | issue-67890 | changes/issue-12345-notification-category |
| issue-67890 | bugfix | Notification lost after sleep | OpenHarmony-6.0-Release | none | bugfix-on-feature | verifying | issue-12345 | changes/issue-67890-notification-lost-after-sleep |
```

新增或归档任何变更/ADR，都必须更新 `registry.md`。

审查命令（`/ohos-review` 或等价命令）必须校验 `registry.md`：

- 每个活跃变更目录和 `decisions/ADR-*` 都有索引行。
- `registry.md` 中的 `Path` 指向存在的目录。
- `Release` 与对应 `proposal.target_release.id` 一致。
- `Profile` 与对应 `manifest.profile` 一致。
- `Related` 中的 Feature / Bugfix / ADR ID 在仓内可解析。

## Release View

`.codespec/release-views/` 是按版本查看的派生视图，可手工维护，也可由工具从各 `manifest.md` 生成。

```text
.codespec/release-views/
├── OpenHarmony-6.0-Release.md
└── OpenHarmony-6.1-Release.md
```

示例：

```markdown
# OpenHarmony 6.0 Release

| ID | Type | Title | Status | Path |
|----|------|-------|--------|------|
| issue-12345 | feature | Notification category | implementing | changes/issue-12345-notification-category |
```

版本调整时，先改 Feature / Bugfix 自身 `proposal.md` 的 target_release frontmatter（变更历史追加到 `manifest.md` 的 `release_change_log`），再刷新 `registry.md` 和 `release-views/`。不要通过移动 Feature 目录来表达版本变化。

## 新旧设计识别流程

Agent 或开发者创建文档前按顺序判断：

1. `registry.md` 是否已有相同或相近能力。
2. `changes/` 下是否已有同模块、同 API、同用户行为的变更。
3. `changes/` 是否有相关历史缺陷。
4. `decisions/` 是否已有架构决策约束。
5. 源码中是否已有实际行为但无 Spec。

判断结果：

| 结果 | 动作 |
|------|------|
| 无历史能力 | 创建 `lineage: new` Feature |
| 有历史代码无文档 | 创建 `lineage: legacy` Feature，并先补源码事实 |
| 有旧模板文档 | 创建 `lineage: migrated`，保留原文档路径 |
| 新需求扩展旧能力 | 创建 `lineage: new-on-legacy`，明确增量和兼容性 |
| 缺陷修复 | 创建变更目录（type: bugfix），并关联 `related` |

## 提交追溯

提交信息建议包含稳定 ID：

```text
issue-12345: add notification category baseline
TASK-002: implement serialization compatibility
issue-67890: fix sleep notification regression
```

合入前要求：

- `manifest.md` 记录相关 commit。
- `registry.md` 状态更新。
- `evidence/checks/check-execution-plan.md` 已通过，且最终验证证据挂在 `review.md` 或 `evidence/reviews/` 中。
- bugfix 已在关联 Feature 侧反向记录。

## 归档与演进

| 场景 | 处理方式 |
|------|----------|
| Feature 被替代 | 保留原目录，`status: archived`，写 `superseded_by` |
| 旧设计迁移完成 | 旧文档路径写入 `lineage.md`，新目录作为唯一活跃入口 |
| 多轮迭代 | 在 `evidence/retrospectives/` 追加 iteration 文件，不覆盖历史 |
| 模板升级 | 更新 `spec_schema`，必要时在 `migrations/` 记录批量迁移计划 |

不要删除历史变更目录来“保持整洁”。可分析性优先于目录短小。
