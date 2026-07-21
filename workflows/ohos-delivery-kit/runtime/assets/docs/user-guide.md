# ODK 使用指南

本文面向日常使用者，说明一个 OpenHarmony 新需求如何通过 ODK 产出可归档的 `.codespec/` 交付件，以及如何选择 Superpowers、OpenSpec、MatrixSpec 等插件组合。

## 1. ODK 的定位

ODK 是交付件规范层，不是新的流程编排器。它定义最终应该沉淀哪些文件、每个文件至少包含哪些章节、以及需求、设计、任务、代码、验证之间如何追溯。

正式归档根始终是业务仓里的：

```text
.codespec/changes/<change-id>/
```

其他插件可以辅助生成、澄清、实现或 review，但不能替代 `.codespec/` 作为最终真相源。

## 2. 命令分层

ODK 命令分为三层：基础命令、桥接命令和平台入口。

### 2.1 基础命令层

基础命令以 ODK 模板为准，零外部插件依赖。

| 命令 | 阶段 | 产出 | 何时使用 |
|------|------|------|----------|
| `odk-init` | Init | `.codespec/changes/<id>/` 骨架 | 新需求开始 |
| `odk-link-issue` | Init | draft 目录改名并写入 issue | 先起草、后拿到 issue ID |
| `odk-propose` | Define | `proposal.md` | 明确背景、目标、非目标、成功标准、8 维影响 |
| `odk-spec` | Specify | `spec.md` | 写用户故事、业务规则、AC、错误码、接口变更 |
| `odk-design` | Design | `design.md` | 写架构、模块影响、关键决策、风险和验证思路 |
| `odk-plan` | Plan | `execution-plan.md` | 把 AC 拆成 Task，定义文件范围和验证命令 |
| `odk-implement` | Implement | 代码 + `execution-plan.md` 回填 | execution-plan 已批准后逐 Task 实现 |
| `odk-review` | Review | `evidence/reviews/` | 生成 spec-compliance、code-quality、verification 评审记录 |
| `odk-validate` | Archive | 校验报告 | 合入前检查 Level A/B/C/D |
| `odk-spec-for-validation` | Validation bypass | `spec-for-validation.md` | 需要集成/系统验证场景时 |
| `odk-security-threat-model` | Security bypass | `threat-model.md` | 高风险安全、隐私、合规变更时 |

基础层适合所有项目，是其他插件组合的回退路径。

### 2.2 桥接命令层

桥接命令以 `odk-<plugin>-*` 命名。它调用外部插件能力，但把输出重定向并转换到 ODK 归档结构。

| 插件 | 命令 | 覆盖阶段 | 推荐场景 |
|------|------|----------|----------|
| Superpowers | `odk-sp-brainstorm` / `odk-sp-plan` / `odk-sp-implement` / `odk-sp-review` | Define 到 Review | 需要强澄清、TDD、分任务实现、review 纪律 |
| OpenSpec | `odk-ops-propose` / `odk-ops-apply` | Define 到 Implement | 需要结构化 proposal/spec/design/tasks |
| MatrixSpec | `odk-ms-proposal` / `odk-ms-delta-spec` / `odk-ms-delta-design` / `odk-ms-tasks` / `odk-ms-validation` | Define 到 Review | brownfield、基线恢复、分阶段 delta 推进 |

桥接命令默认使用 `strict` 输出模式：结果必须符合 ODK 模板。必要时可在 `.codespec/profile.yaml` 或命令说明中切到 `merge` / `passthrough`，用于对比或临时迁移。

### 2.3 平台入口层

ODK 支持 Claude Code、Codex CLI 和 OpenCode。平台层只负责安装和暴露命令，不拥有交付件规范。

ODK 有**两条安装路径**，产物同构，按需选择：

- **发布仓安装**（[`ohos-marketplace`](https://gitcode.com/oshunter/ohos-marketplace)，当前为测试/过渡发布仓——正式发布仓与路径待定）：产物已构建并提交，无需生成 `dist/`。
- **开发仓本地安装**（本仓，当前版本）：装当前工作树的 `dist/`。安装脚本（`install-{claude,codex,opencode}.sh`）会在 `dist/` 缺失或过期时自动生成/刷新；仅手动 `claude --plugin-dir` 或审查 `dist/` 时才需先跑 `distribute-skills.sh`。适合开发、拿最新，或发布仓未同步时。

各平台命令：

| 平台 | 发布仓安装 | 开发仓本地安装 |
|---|---|---|
| Claude Code | `claude plugin marketplace add https://gitcode.com/oshunter/ohos-marketplace.git` → `claude plugin install ohos-delivery-kit@ohos-marketplace` | `bash scripts/install-claude.sh`（持久化）；或 `claude --plugin-dir dist/claude`（会话级，活跃开发 live-reload） |
| Codex CLI | `codex plugin marketplace add <url>` → `codex plugin add ohos-delivery-kit@ohos-marketplace` | `bash scripts/install-codex.sh <target>` |
| OpenCode | clone `ohos-marketplace` → `./scripts/install-opencode.sh <target>` | `bash scripts/install-opencode.sh <target>`（安装原生 JS 插件：自动加载 `.opencode/plugins/ohos-delivery-kit.js`，注册 skills 并注入 `using-odk` bootstrap） |

> 注：发布仓按需同步、可能滞后开发仓；如需当前版本用开发仓本地安装。完整步骤见 [quick-start.md](quick-start.md) 安装段。

不同平台下命令入口略有差异，但目标产物和阶段语义一致。

## 3. 一个新需求如何推进

### 3.1 准备阶段

先确认三件事：

1. 是否有 issue ID。如果没有，可以先用 draft 目录，后续用 `odk-link-issue` 关联。
2. 目标发布版本 `target_release`，例如 `7.0`、`7.1`、`7.1-Beta`。不要填 `dev`、`master` 这种分支名。
3. 是否需要外部插件增强。如果不确定，先走基础层。

### 3.2 基础层完整流程

```text
odk-init <slug> <target_release> [issue]
odk-propose
odk-spec
odk-design
odk-plan
odk-implement
odk-review
odk-validate
```

每个文档阶段都需要用户确认后再进入下一阶段。批准 `proposal.md`、`spec.md`、`design.md` 或 `execution-plan.md` 只代表该文档通过，不代表允许跳到实现。只有 `execution-plan.md` 已批准且用户显式调用 implement 命令后，才能修改实现代码。

### 3.3 有 Superpowers 时

```text
odk-sp-brainstorm
odk-sp-plan
odk-sp-implement
odk-sp-review
odk-validate
```

Superpowers 擅长把需求澄清、TDD、子任务执行和 review 做扎实。ODK 桥接层负责把 Superpowers 的过程输出拆分或格式化为：

```text
proposal.md
spec.md
design.md
execution-plan.md
evidence/reviews/
```

适合实现风险较高、需要多人 review 或需要强执行纪律的需求。

### 3.4 有 OpenSpec 时

```text
odk-ops-propose
odk-ops-apply
odk-review
odk-validate
```

OpenSpec 的 `/opsx:propose` 通常覆盖 proposal、spec、design 和 tasks。ODK 会补齐非目标、8 维确认、兼容性声明、AC-Task 追溯等归档必需内容。

适合需求结构清楚、希望快速生成完整方案和任务清单的场景。

### 3.5 有 MatrixSpec 时

```text
odk-ms-proposal
odk-ms-delta-spec
odk-ms-delta-design
odk-ms-tasks
odk-ms-validation
odk-validate
```

MatrixSpec 更适合从已有系统恢复基线，或者按 proposal / delta-spec / delta-design / tasks 分阶段推进。ODK 负责把 MatrixSpec 产物转成统一 `.codespec/` 归档结构。

### 3.6 混合组合

插件可以混用，但一个阶段只保留一个正式 ODK 产物。例如：

```text
odk-ops-propose      # 用 OpenSpec 生成 proposal/spec/design/plan
odk-sp-implement     # 用 Superpowers TDD + subagent 执行
odk-sp-review        # 用 Superpowers review，再写入 evidence/reviews/
odk-validate
```

混合时遵循两条规则：

- 用户显式调用的命令优先。
- 无论中间用了什么插件，最终都必须收口到 `.codespec/changes/<id>/`。

## 4. 每个命令怎么用

### `odk-init`

用途：创建新变更目录和四个基础文档骨架。

输入：英文 slug、`target_release`、可选 issue ID。

产出：

```text
.codespec/changes/issue-<id>-<slug>/
├── proposal.md
├── spec.md
├── design.md
└── execution-plan.md
```

常见误用：把 `.codespec/` 加入 `.gitignore`。`.codespec/` 是正式交付归档，应随代码提交。

### `odk-propose`

用途：定义需求边界，不做实现。

输入：需求背景、用户目标、约束、issue 描述。

产出：`proposal.md`，包括目标、非目标、成功标准、影响范围、8 维不涉及项确认。

注意：用户 prompt 里的“实现、重构、更新、修复”等动词只应沉淀为 proposal 的目标、范围、非目标、成功标准或开放问题，不应直接触发代码修改。

### `odk-spec`

用途：把需求转为可验收行为。

输入：已批准的 `proposal.md`。

产出：`spec.md`，包括用户故事、业务规则、异常与边界、错误码、接口变更、验证映射。

注意：AC 的 Then 应描述可通过公开接口或用户可感知结果观察的行为。内部状态机、缓存结构、遍历算法等实现细节应放到 `design.md`。

### `odk-design`

用途：定义实现方案和架构决策。

输入：`proposal.md` + `spec.md`。

产出：`design.md`，包括代码事实基线、模块影响、方案概述、关键决策、风险缓解、验证思路。

安全规则：当 proposal 的 `安全/权限` 为「是」时，`design.md` 展开 `安全基础检查`；命中高风险判据时再运行 `odk-security-threat-model`。

### `odk-plan`

用途：把 spec/design 拆成可执行任务。

输入：`spec.md` + `design.md`。

产出：`execution-plan.md`，包括 AC 到 Task 追溯、Task 列表、Task 详情、文件范围、验证命令和代码范围映射。

注意：Task 必须有文件级范围和可执行验证命令，避免“实现功能”这类不可检查任务。

### `odk-implement`

用途：按已批准的 execution-plan 逐 Task 实现。

输入：已批准的 `execution-plan.md`，以及用户显式实现授权。

产出：代码变更 + `execution-plan.md` 回填。

要求：每个 Task 先写失败测试或定义可复现证据缺口，再实现代码，并回填实际文件、测试、验证结果和 Task 状态。

### `odk-review`

用途：生成归档 review 证据。

输入：实现代码、`spec.md`、`execution-plan.md`。

产出：`evidence/reviews/` 下的 spec-compliance、code-quality、verification 记录。

注意：Review 结论必须能追到 AC、Task、代码文件和验证命令。

### `odk-validate`

用途：合入前统一校验。

输入：`.codespec/changes/<id>/`。

检查层级：

- Level A：目录名、必需文件、frontmatter
- Level B：必需章节、条件章节、可选 artifact 结构
- Level C：AC、Task、代码范围、验证映射追溯
- Level D：归档就绪度、占位符、实际结果和证据

Warnings 可用于 draft 阶段，但 archive readiness 需要显式解决或接受风险。

### `odk-spec-for-validation`

用途：生成集成/系统验证场景。

输入：`proposal.md` + `spec.md`，可参考 `design.md`。

产出：`spec-for-validation.md`。

边界：它生成 L2/L3/L4 验证场景，不生成 L1 单测代码。单测和 XTS/fuzz 等测试代码在 implement 阶段由领域 skill 或项目测试框架生成，代码落在业务仓测试源码树。

### `odk-security-threat-model`

用途：为高风险安全变更生成深度威胁分析。

输入：`proposal.md` + `design.md`。

触发：`安全/权限=是` 且命中敏感数据、网络暴露面、认证授权变更、合规要求、关键安全组件等高风险判据，或用户显式调用。

产出：`threat-model.md`，包括 DFD、STRIDE、合规检查、风险与缓解、安全验证计划。

详细清单见 [security-guide.md](security-guide.md)。

## 5. 安全、测试与 Profile

### 安全

安全是主流程中的条件分支，不是单独流程。普通安全影响停留在 `design.md` 的 `安全基础检查`；高风险变更升级到 `threat-model.md`。安全缓解措施最终应追到 execution-plan Task，并在验证场景或测试中体现。

### 测试

ODK 不单独设置“测试阶段”。测试要求内建在 `execution-plan.md` 和 `odk-implement`：

- 每个 Task 先写失败测试或证据缺口
- 实现后运行 Task 的验证命令
- 测试文件和验证结果回填到代码范围映射
- 归档前通过 `odk-review` 和 `odk-validate` 检查

### Profile

Profile 用于 OpenHarmony 子系统增强，例如 arkui、arkgraphic、arkweb、arkruntime。AI 会根据模块关键词自动匹配，也可以在 `.codespec/profile.yaml` 中显式声明。

Profile 只做加法式约束：强化 8 维确认、追加模板片段、注入领域注意事项。无匹配时不增加上下文负担。

## 6. 常见问题

### `.codespec/` 要不要提交？

要提交。`.codespec/` 是正式交付归档。桥接插件工作区如 `openspec/`、`docs/superpowers/`、`matspec/` 才应忽略。

### 可以直接从 proposal 跳到实现吗？

不可以。proposal/spec/design/plan 都是审批文档。只有 `execution-plan.md` 已批准，且用户显式调用 implement 命令后，才能修改代码。

### 已经有 Superpowers / OpenSpec / MatrixSpec，还需要 ODK 吗？

需要。插件负责生成和增强，ODK 负责统一归档契约和验证口。最终交付件必须落到 `.codespec/`。

### 什么时候需要 `spec-for-validation.md`？

当需要集成、系统、兼容性、性能、安全、功耗等跨模块验证场景时生成。简单单元级验证不需要单独生成。

### 什么时候需要 `threat-model.md`？

当安全影响达到高风险级别时生成。`安全/权限=是` 但没有高风险信号时，通常只需填写 `design.md` 的 `安全基础检查`。

## 7. 参考文档

- [quick-start.md](quick-start.md)：安装和最短路径
- [contracts.md](contracts.md)：交付件契约
- [workflows.md](workflows.md)：插件组合模式
- [adapters.md](adapters.md)：插件适配映射
- [security-guide.md](security-guide.md)：安全检查清单和 STRIDE 指南
- [validator.md](validator.md)：归档校验规则
