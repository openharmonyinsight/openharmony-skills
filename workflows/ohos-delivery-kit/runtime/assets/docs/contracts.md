# Contracts

> Contract source: `core/contracts/artifacts.yaml`. 本文解释交付件契约；必需 artifact、章节、依赖和 evidence policy 应与该声明文件保持一致。

## 目标

本文件定义 `ohos-delivery-kit` 的最小交付件契约。

原则是：

- 只约束最终归档所必需的结构和章节
- 不约束具体文风和篇幅
- 允许不同插件生成内容
- 由统一校验器判断是否合规
- 过程交付件与最终归档件应尽量保持语义一致
- 交付件与最终代码实现必须可建立映射关系

## 业务仓顶层输出

业务仓最终统一写入：

```text
.codespec/
└── changes/
    └── issue-12345-english-slug/
        ├── proposal.md
        ├── design.md
        ├── spec.md
        └── execution-plan.md
```

| 目录 | 用途 | 阶段 |
|------|------|------|
| `changes/` | 活跃变更交付件，每条对应一个 issue | Phase 1 |

### 目录命名规则

每个变更目录以 **issue 编号 + 英文简短描述** 命名：

```text
issue-<issue-number>-<english-short-slug>
```

示例：

- `issue-12345-arkui-focus` — GitCode issue #12345，ArkUI 焦点管理
- `issue-67890-web-security` — GitCode issue #67890，Web 安全增强

约束：

- `issue-number` 为源码平台（GitCode 等）的 issue ID
- `english-short-slug` 使用小写英文、数字和连字符
- 目录名即可标识变更，无需额外的 manifest 文件索引

## 变更最小目录契约

```text
.codespec/changes/issue-12345-english-slug/
├── proposal.md
├── design.md
├── spec.md
└── execution-plan.md
```

对于 `L0` 或极简单变更，可允许 `design.md` 标记为简化模式，但不能跳过：

- `proposal.md`
- `spec.md`
- `execution-plan.md`

这里的关键不是"必须有多少文件"，而是这些文件必须形成可追溯链：

```text
proposal -> spec -> design -> execution-plan -> code
```

> 注：spec 定义 WHAT（行为、AC、业务规则），design 定义 HOW（架构、错误码、接口签名）。design 引用 spec 的 AC 编号加强可追溯链，design 完成后回写 spec 的 TBD 值形成精化回路。桥接命令（如 MatrixSpec）可按源插件原生顺序调整 spec↔design 阶段顺序，但最终归档件的依赖关系和可追溯链不变。

如果链路断裂，归档价值会明显下降。

## ID 规则

- 变更目录：`issue-<issue-number>-<english-short-slug>`
- Task：`TASK-NNN-short-slug`

约束：

- 路径中不得带 `target_release`
- `short-slug` 使用小写英文、数字和连字符

## 文档章节 contract

这里只约束最小章节，不约束写法。

机器可校验的章节清单维护在 `core/contracts/artifacts.yaml`，正文骨架维护在 `core/templates/ai/`。修改章节时应同步更新这两处，并运行 `bash scripts/validate-contracts.sh`。

### `proposal.md`

`proposal.md` 是变更的入口文件，同时承载 `target_release` 等关键元数据：

```yaml
---
target_release: 7.0
---
```

`target_release` 在此为版本事实唯一来源，文档正文只引用不复制。

必需章节（详见 `core/templates/ai/proposal.md`）：

- 背景与问题
- 初始分级判断（复杂度 L0-L4 / 仓库数 / API 影响 / 安全关键路径 / 跨 SIG）
- 目标
- 非目标
- 成功标准（可观测指标 + 验证方式）
- 影响范围（子系统 / 仓库 / 模块路径 / 影响类型）
- 假设与开放问题
- 不涉及项确认（8 维度 N/A 表：性能 / 安全/权限 / 兼容性 / API-SDK / IPC-跨进程 / 构建-组件 / 国际化-无障碍 / 数据迁移）

> **`安全/权限` 维度的下游触发**：当 `安全/权限=是` 时，会触发 design 阶段的 `安全基础检查` 条件章节（Tier 1，必产）；命中高风险判据时进一步升级为 `threat-model.md`（Tier 2，按需，由 `/odk-security-threat-model` 生成）。两层模型详见 `docs/designs/security-design.md`。

### `design.md`

必需章节（详见 `core/templates/ai/design.md`）：

- 需求基线摘要
- 设计约束
- 非目标
- 方案概述
- 架构图（Mermaid graph TD）
- 模块影响
- 关键设计决策（含方案对比表：问题 / 推荐方案 / 替代方案 / 理由）
- 时序设计（Mermaid sequenceDiagram）
- 风险与缓解（风险 / 可能性 / 影响 / 缓解措施）
- 验证思路（验证场景 / 方法 / 通过标准）

条件章节：

- 代码事实基线（修改存量模块时必需；纯新建/文档/配置变更可省略）
- 状态归属与不变量（复杂状态变更时追加：ownership / lifecycle / concurrency / compatibility / perf / capacity / migration）

### `spec.md`

必需章节（详见 `core/templates/ai/spec.md`）：

- 概述（表格：feature name / number / priority / complexity / target version）
- 用户故事或场景（US-N 编号，WHEN/THEN AC 格式，嵌套编号 AC-1.1 等）
- 业务规则（表格：规则 ID / 描述 / 约束 / 关联 AC）
- 异常与边界规则（表格：编号 / 场景 / 触发条件 / 系统行为 / 关联 AC）
- 错误码定义（表格：错误码 ID / 值 / 含义 / 关联 AC — 必须有具体数值）
- 接口变更分析（新增 API 表：名称 / 开放级别 / 参数概要 / 返回值 / 错误码 / 关联 AC；变更/废弃 API 表：名称 / 开放级别 / 变更类型 / 影响场景 / 迁移指引 / 关联 AC）
- 兼容性声明（API 行为变化 / 配置格式变化 / 数据存储格式变化 — 是/否）
- 验证映射（AC / 关联规则 / 验证方式 / 证据）

### `execution-plan.md`

必需章节（详见 `core/templates/ai/execution-plan.md`）：

- 输入状态（proposal / spec / design 均要求 Approved）
- 执行原则（7 条：spec 权威 / test-evidence first / small tasks / file boundaries / 单一状态归属 / evidence backfill / anti-fake completion）
- AC 到 Task 追溯（表格：AC / 来源 / Task / 验证方式 / 验证状态（Pass/Fail/Blocked））
- 实现边界（Must implement / Can defer / Not recommended to defer）
- 禁止项
- Task 依赖（Mermaid graph TD）
- Task 列表（表格：TASK ID / 目标 / 文件范围 / AC 映射 / 前置 / 完成判据 / 验证命令 / 状态）
- Task 详情（per-Task 子模板：Target / AC Mapping / Prerequisites / Non-goals / State Ownership / Inter-task Interfaces / Read-only Context / Files / Steps / Anti-Fake Completion / Verification）
- Review Gates（Gate-1/2/Final：When / Required Evidence / Blocks Next Step）
- 代码范围映射（TASK ID / 文件 / 操作）

## 可选过程证据

`reviews/` 和 `gates/` 属于过程证据，不属于最小归档 contract。

如果项目希望保留这些记录，建议放在可选目录中：

```text
.codespec/changes/issue-12345-english-slug/
└── evidence/
    ├── reviews/
    │   ├── spec-compliance-YYYYMMDD.md
    │   ├── code-review-YYYYMMDD.md
    │   └── verification-YYYYMMDD.md
    └── gates/
        ├── gate-define.md
        ├── gate-design.md
        ├── gate-implement.md
        └── gate-archive.md
```

validator 只能把这些内容作为增强校验或证据引用，不应在最小归档校验中强制要求。

## 代码映射 contract

`ohos-delivery-kit` 不把归档件视为"写完代码之后的总结"。

相反，归档件应当成为代码实现的前置依据和事后验证依据。

最小要求：

- `execution-plan.md`「AC 到 Task 追溯」+「代码范围映射」覆盖所有 spec AC，每个被追溯 Task 有非空文件
- `execution-plan.md` 中每个 Task 都应给出代码范围或目标模块
- 如存在 `evidence/reviews/`，其中应能看出代码结果是否符合 `spec.md`

建议映射方式：

```text
| Spec Item | Task ID | Code Ref | Verification Evidence |
```

这张表落在 `execution-plan.md`（「AC 到 Task 追溯」+「代码范围映射」），可选证据在
`evidence/reviews/`，语义上必须能拼起来。

## 模板强制输出 contract

kit 的另一个核心用途是让插件在使用过程中直接输出 OpenHarmony 所需章节。

因此模板不只是"归档模板"，还是"生成模板"。

要求：

- 插件草稿阶段尽量直接使用 kit 模板
- kit 模板中的定制章节应在生成阶段即被填充
- 不推荐先生成一套通用 spec，再人工大规模改写成 kit 格式

越早把模板约束前移，开发者使用时越无感。

## 校验边界

校验器第一阶段只做结构校验，不做语义好坏判断。

第一阶段建议校验：

- 目录存在
- 必需文件存在
- 目录名格式正确（`issue-<issue-number>-<slug>`）
- 必需章节标题存在

第二阶段再逐步增强：

- `target_release` 引用一致性
- 关联项可解析性
- 跨文档覆盖检查：proposal → spec AC → execution-plan Task → 代码范围映射 的双向追溯链完整性
- review 证据完整性

## 插件适配边界

允许插件：

- 生成草稿
- 增强某些阶段
- 提供 TDD / review / planning 辅助

不允许插件：

- 以自身私有目录替代 `.codespec/`
- 把自身 prompt 视为正式交付规范
- 绕过 validator 直接宣布合规

## Git 管理约定

### 提交策略

| 内容 | 是否提交 | 说明 |
|------|---------|------|
| `.codespec/` | **提交** | 交付件属于业务仓的一部分，与代码一同版本管理 |
| 插件工作目录 (`openspec/`, `docs/superpowers/`, `matspec/`) | **gitignore** | 插件草拟工作区，不作为正式归档根 |
| `.matspec-cli/` (MatrixSpec 运行时) | **gitignore** | CLI 运行时文件 |
| 适配器安装目录 (`.claude/`, `.codex/`, `.opencode/`, `opencode.json` 等) | **团队自定** | 是否共享插件配置由各团队决定，ODK 不强制；`odk-init` 也不替用户写入 |

### Commit Message 规范

所有实现 commit 建议包含关联的 issue 编号：

```
feat(arkui): add XYZ focus management (#12345)

Task: TASK-001, TASK-002
```
