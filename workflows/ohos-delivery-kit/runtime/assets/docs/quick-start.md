# ODK 快速上手指南

## 概述

ohos-delivery-kit (ODK) 为 OpenHarmony 项目提供标准化的交付件模板和校验规则。核心流程：

```
基础层: odk-init → odk-propose → odk-spec → odk-design → odk-plan → odk-implement → odk-review → odk-validate
        odk-spec-for-validation (旁路，可选，从 spec/design 派生验证场景)
        odk-security-threat-model (旁路，可选，高风险变更生成 threat-model.md 深度威胁分析)
桥接层: odk-sp-brainstorm → odk-sp-plan → odk-sp-implement → odk-sp-review (Superpowers)
        odk-ops-propose → odk-ops-apply (OpenSpec)
        odk-ms-proposal → odk-ms-delta-spec → odk-ms-delta-design → odk-ms-tasks → odk-ms-validation (MatrixSpec)
```

本文件用于快速安装和跑通最短路径。完整命令说明、插件组合选择和端到端使用方式见 [user-guide.md](user-guide.md)。

## 新需求最短路径

### 默认路径（无额外插件依赖）

```text
odk-init
  → odk-propose
  → odk-spec
  → odk-design
  → odk-plan
  → odk-implement
  → odk-review
  → odk-validate
```

适合团队先统一 `.codespec/` 交付件格式，再逐步接入其他插件。

### 推荐增强路径（有 Superpowers）

```text
odk-sp-brainstorm
  → odk-sp-plan
  → odk-sp-implement
  → odk-sp-review
  → odk-validate
```

适合需要更强需求澄清、TDD、分任务实现和 review 纪律的需求。ODK 会把 Superpowers 过程产出桥接到 `.codespec/changes/<id>/`，正式归档仍以 ODK 产物为准。

### 结构化 spec 路径（有 OpenSpec 或 MatrixSpec）

OpenSpec 适合一次性生成 proposal/spec/design/tasks：

```text
odk-ops-propose → odk-ops-apply → odk-review → odk-validate
```

MatrixSpec 适合 brownfield 或分阶段恢复：

```text
odk-ms-proposal
  → odk-ms-delta-spec
  → odk-ms-delta-design
  → odk-ms-tasks
  → odk-ms-validation
  → odk-validate
```

### 安全相关需求

安全不单独开一条主流程。`odk-propose` 在 8 维确认中把 `安全/权限` 标为「是」后，`odk-design` 会展开 `安全基础检查`；如果命中敏感数据、网络暴露面、认证授权变更、合规或关键安全组件等高风险判据，再运行：

```text
odk-security-threat-model
```

详细安全检查清单、STRIDE 步骤和合规表见 [security-guide.md](security-guide.md)。

## 安装

> **发布仓安装**：通过发布仓 [`ohos-marketplace`](https://gitcode.com/oshunter/ohos-marketplace) 安装——产物已构建并提交，无需本地生成 `dist/`。三端均已同步到当前版本（**0.6.5**）：
>
> ```bash
> # Claude
> claude plugin marketplace add https://gitcode.com/oshunter/ohos-marketplace.git
> claude plugin install ohos-delivery-kit@ohos-marketplace
> # Codex
> codex plugin marketplace add https://gitcode.com/oshunter/ohos-marketplace.git
> codex plugin add ohos-delivery-kit@ohos-marketplace
> ```
>
> OpenCode（clone 发布仓后用其安装脚本，无 `plugin install` 形式）：
>
> ```bash
> git clone https://gitcode.com/oshunter/ohos-marketplace.git
> cd ohos-marketplace
> ./scripts/install-opencode.sh /path/to/your-project
> ```
>
> **正式发布仓与路径待定，当前用 `ohos-marketplace` 仓测试替代。**

下方为**开发仓本地安装**方式（装**当前版本**，亦用于改源/调试）——先克隆开发仓并进入：

```bash
git clone git@gitcode.com:oshunter/ohos-delivery-kit.git
cd ohos-delivery-kit
```

### Claude Code

两种本地方式（开发仓自足，无需 ohos-marketplace）：

**持久化安装**（推荐，用户级，重启仍生效）：

```bash
bash scripts/install-claude.sh
```

`install-claude.sh` 注册一个本地 marketplace（`dist/claude-marketplace`，名 `ohos-delivery-kit-local`）并 `claude plugin install`。重启 Claude 后 SessionStart hook 自动生效，每个新会话注入一条简短的路由提示。需要 `claude` CLI。

**会话级加载**（活跃开发，每次读 live `dist/`）：

```bash
bash scripts/distribute-skills.sh
claude --plugin-dir dist/claude
```

改 ODK 源 → 重跑 `distribute-skills.sh` → 下次 `--plugin-dir` 启动即生效（持久化安装同版本内容变更不会自动刷新，见下方"升级"，故活跃开发用 `--plugin-dir` 更顺）。

Claude 包需要 `.claude-plugin/plugin.json`、hooks 和带 frontmatter 的 skill 文件。`packaging/claude` 只保留 manifest、hooks、README 等静态输入；`dist/claude` 由分发脚本从 `core` 生成，是实际可加载产物。维护时以 `core/contracts`、`core/adapters`、`core/templates`、`core/profiles`、`core/skills` 为准。

**升级**（Claude 按版本号缓存插件）：
- 持久化安装、**同版本**内容变更 → `bash scripts/install-claude.sh --force`（uninstall + install，强制刷新）；
- 持久化安装、**版本 bump** → `git pull && bash scripts/distribute-skills.sh && claude plugin update ohos-delivery-kit`；
- 会话级 → 重跑 `distribute-skills.sh` 后 `--plugin-dir` 启动（天然 live-reload，无需刷缓存）。

版本变化可能触发新的 skill 读取权限请求（点一次 "always allow"）。

> **本地加载 vs marketplace**：`--plugin-dir` 是会话级本地加载（开发调试）；`install-claude.sh` 与上方发布仓 `ohos-marketplace` 是持久化安装。若 `claude plugin list` 误报 `Marketplace ... not found`，说明在 `--plugin-dir` 场景误用了 `install <name>@<marketplace>` 形式——本地路径改用 `--plugin-dir`。

### Codex CLI

```bash
bash scripts/install-codex.sh /path/to/your-project
```

Codex 包需要 `.codex-plugin/plugin.json`、hooks 和 Codex 路径变量（`${CODEX_PLUGIN_ROOT}`）。`scripts/install-codex.sh` 会在 `dist/codex` 缺失或过期时自动运行分发脚本。Codex 与 Claude 的 skill 正文由同一份 `core/skills` 生成，只允许 frontmatter、命令前缀和插件根路径不同；contracts/adapters/templates/profiles 同样由分发脚本从 `core` 物化到 `dist/codex`。

自动化验证或不希望写入 Codex marketplace/cache 时，使用显式手动安装路径：

```bash
bash scripts/install-codex.sh --manual-only /path/to/your-project
```

### OpenCode

```bash
bash scripts/install-opencode.sh /path/to/your-project
```

安装原生 JS 插件：OpenCode 启动时自动加载 `.opencode/plugins/ohos-delivery-kit.js`，**无需改 `opencode.json`**。插件经 `config` hook 注册 ODK skills，经 `experimental.chat.messages.transform` 注入 `using-odk` bootstrap；`/odk-*` 命令是薄包装。

需要审查产物或集成到自定义流程时，可先 `bash scripts/distribute-skills.sh` 生成 `dist/opencode/`（`.opencode/` 根布局：裸 `ohos-delivery-kit.js` + `ohos-delivery-kit/` 资产 + 薄 commands），再手动并入目标项目。

若你的 OpenCode 版本不支持裸 `.js` 自动加载，改用 `bash scripts/install-opencode.sh <target> --add-config`，把插件 entry 写入 `opencode.json`（`uninstall-opencode.sh` 只删该 entry，不动其它配置）。

## 产出路径与激活规则

**`using-odk` 是自动注入的上下文技能，不是用户命令。** 安装后 ODK 有两种产出路径：

### 显式命令 vs 自动检测

| 路径 | 触发方式 | 适用场景 |
|------|---------|---------|
| **桥接命令** | 用户主动调用 `odk-sp-*`（如 `odk-sp-brainstorm`） | 有 Superpowers 时推荐，自动桥接产出到 `.codespec/` |
| **基础命令** | 用户主动调用 `odk-*`（如 `odk-propose`） | 无插件依赖，模板驱动，AI 辅助生成 |
| **自动检测** | AI 根据意图关键词自动匹配 Phase-Artifact Mapping 表 | 使用其他插件时 AI 自动桥接（Pattern-Match Trigger 兜底） |

### 激活规则

ODK **仅当用户表达意图时激活**：

- 显式提及 ODK、`.codespec`、proposal、spec、design、execution-plan、review、validate
- 调用任意 `/odk-*` 命令

**以下情况不会激活 ODK**：

- 仓库中存在 `.codespec/` 目录，但用户未提及 ODK 相关术语
- 普通编码、修 bug、调试、构建等日常开发任务

> `.codespec/` 是团队公共产物，其存在不等于当前开发者使用 ODK —— 仅在用户表达 ODK 意图后用于上下文加载。

## 命令

### 基础层命令（无插件依赖，模板驱动）

| 命令 | 阶段 | 用途 | 前置依赖 |
|------|------|------|---------|
| `odk-init` | Init | 创建 `.codespec/changes/<id>/` 骨架 | — |
| `odk-link-issue` | Init | 将 draft 目录关联到 issue ID | — |
| `odk-spec-for-validation` | Validation (bypass) | 旁路生成 spec-for-validation.md（从 spec/design 派生验证场景，不阻塞主流程） | proposal.md + spec.md |
| `odk-security-threat-model` | Design (bypass) | 旁路生成 threat-model.md（高风险变更的 STRIDE + 合规深度威胁分析，缓解措施关联 Task） | design.md + proposal.md |
| `odk-propose` | Define | 生成 proposal.md（分级判断、成功标准、影响范围、8 维 N/A） | — |
| `odk-spec` | Specify | 生成 spec.md（Given/When/Then AC、错误码、验证映射） | proposal.md |
| `odk-design` | Design | 生成 design.md（架构图、决策对比、风险表，引用 spec AC 编号） | proposal.md + spec.md |
| `odk-plan` | Plan | 生成 execution-plan.md（AC-Task 追溯、Task 详情） | spec.md + design.md |
| `odk-implement` | Implement | AI 辅助逐 Task 实现（测试先行：每个 Task 先写失败测试）+ 回填 execution-plan 代码范围映射 | execution-plan.md |
| `odk-review` | Review | 生成评审记录（spec-compliance、code-quality、verification） | 实现代码 + spec.md |
| `odk-validate` | Archive | 校验交付件完整性（Level A/B/C/D） | 所有产物 |

### 桥接层命令

#### Superpowers 桥接（需 Superpowers 插件）

| 命令 | 对应 Superpowers 能力 | 产出 | 回退 |
|------|----------------------|------|------|
| `odk-sp-brainstorm` | `brainstorming` | proposal + spec + design | `odk-propose` + `odk-spec` + `odk-design` |
| `odk-sp-plan` | `writing-plans` | execution-plan + AC-Task 追溯 | `odk-plan` |
| `odk-sp-implement` | `TDD` + `subagent` | 代码 + execution-plan 代码范围映射回填 | `odk-implement` |
| `odk-sp-review` | `code-review` + `verification` | evidence/reviews/ | `odk-review` |

#### OpenSpec 桥接（需 OpenSpec 插件）

| 命令 | 对应 OpenSpec 命令 | 产出 | 回退 |
|------|-------------------|------|------|
| `odk-ops-propose` | `/opsx:propose` | proposal + spec + design + tasks | `odk-propose` + `odk-spec` + `odk-design` + `odk-plan` |
| `odk-ops-apply` | `/opsx:apply` | 代码 + execution-plan 代码范围映射回填 | `odk-implement` |

#### MatrixSpec 桥接（需 MatrixSpec 插件）

| 命令 | 对应 MatrixSpec 阶段 | 产出 | 回退 |
|------|---------------------|------|------|
| `odk-ms-proposal` | Stage 1: `/matspec.proposal` | proposal | `odk-propose` |
| `odk-ms-delta-spec` | Stage 2: `/matspec.delta-spec` | spec (delta 格式) | `odk-spec` |
| `odk-ms-delta-design` | Stage 3: `/matspec.delta-design` | design (delta 格式) | `odk-design` |
| `odk-ms-tasks` | Stage 4: `/matspec.tasks` | execution-plan | `odk-plan` |
| `odk-ms-validation` | Stage 5: `/matspec.validation` | evidence/reviews/ | `odk-review` |

> 桥接命令按源插件原生命令 1:1 映射，支持三档输出模式（strict/passthrough/merge），默认 strict。
> `using-odk` 和 `using-odk-bridge` 不是用户命令，通过 SessionStart hook 自动注入。

> **OpenCode**: 通常按 `Ctrl+K` 打开命令面板，选择对应 `project:` 命令

### 测试代码生成

ODK 核心流程**不单独设测试阶段**，测试代码通过两条既有机制覆盖：

1. **测试先行内建进 execution-plan**：`execution-plan.md` 执行原则要求每个 Task 先写失败测试再实现；Task 详情的 Step 1 即"写失败测试或定义可复现证据缺口"。`odk-implement` 把"测试编写"列为与代码修改同等强制的 Task 类型，不得跳过。

2. **结构化测试代码生成走领域 skill**：XTS 单测（ArkTS/CAPI）、模糊测试由配套的 `ohos-test-arkts-xts-generation` / `ohos-test-capi-xts-generation` / `ohos-test-fuzz-generation` skill 生成。这些 skill 不属于 ODK 插件，AI 在 implement 阶段按 spec AC 自然调用。

> **测试代码落点**：测试代码是仓库代码，落到项目测试源码树并随 commit 归档，**不进 `.codespec/`**（`.codespec/` 只存交付件文档）。生成后回填 `execution-plan.md`「代码范围映射」（Task ↔ 实际文件）+「AC 到 Task 追溯」验证状态，保持追溯链完整。

> **`spec-for-validation` 的边界**：`odk-spec-for-validation` 产出 **L2/L3/L4 集成/系统验证场景**（Gherkin Given/When/Then），**不含 L1 单测代码**——L1 单测属于"如何测试(how to test)"，由上面第二条机制生成。这是 `odk-test-spec` 重命名为 `odk-spec-for-validation` 的刻意边界（详见 `docs/designs/spec-for-validation.md`）。

## Profile 系统（子系统定制）

ODK 默认为所有模块提供通用模板。对高频大仓（arkui/arkgraphic/arkweb/arkruntime），可通过 profile 强化特定维度的约束。

### 自动检测

AI 根据模块关键词自动匹配 profile：

```
arkui / component / layout   → arkui profile
graphic / render / gpu       → arkgraphic profile
web / chromium               → arkweb profile
runtime / compiler / gc      → arkruntime profile
```

### 显式声明

在 `.codespec/profile.yaml` 中指定：

```yaml
profiles:
  - "arkui"
```

匹配后自动应用：`required_dimensions`（强化 8 维 N/A 表中特定行）、`additional_sections`（追加章节）、`agent_instructions`（注入领域约束）。无匹配时零额外上下文。

详见 `core/profiles/README.md`。

## 与其他插件融合

ODK 支持两种协作方式：

### 方式 1: 桥接命令（推荐，需 Superpowers）

使用 `odk-sp-*` 命令直接桥接 Superpowers。详见上方[桥接层命令](#桥接层命令需-superpowers-插件)表。

```
odk-sp-brainstorm → odk-sp-plan → odk-sp-implement → odk-sp-review → odk-validate
```

### 方式 2: AI-as-Bridge（通用，适合 OpenSpec/MatrixSpec 等插件）

AI 同时拥有 ODK 规范和其他插件能力的上下文，自动将插件产出桥接到 `.codespec/`。协作方式与上文的[显式命令 vs 自动检测](#显式命令-vs-自动检测)一致：

> 两种方式可以混用。例如：用 `odk-sp-brainstorm` 生成初稿，再用 `odk-spec` 补充兼容性声明。
> 
> **前提**：自动桥接需要 ODK 已被激活（用户提及 ODK 相关术语或调用了 `odk-*` 命令）。如果用户只是正常使用 Superpowers 而未表达 ODK 意图，AI 不会主动桥接到 `.codespec/`。

### 阶段与产物映射总览

| ODK 阶段 | ODK 产物 | Superpowers | OpenSpec | MatrixSpec |
|----------|---------|-------------|----------|------------|
| Define | proposal.md | brainstorming（前半） | `/opsx:propose` | `matspec-proposal` |
| Specify | spec.md | brainstorming（中段：AC/错误/接口） | `/opsx:propose` (delta spec) | `matspec-delta-spec` |
| Design | design.md | brainstorming（后段：架构/决策） | `/opsx:propose` | `matspec-delta-design` |
| Plan | execution-plan.md | writing-plans | `/opsx:propose` (tasks) | `matspec-tasks` |
| Implement | 代码 + 回填映射表 | TDD / subagent | `/opsx:apply` | — |
| Review | evidence/reviews/ | code-review（会话瞬态） | — | validation |

### ODK + Superpowers

Superpowers 的 `brainstorming` 产出的是**一个合并文档**（`docs/superpowers/specs/YYYY-MM-DD-topic-design.md`），同时包含 proposal、spec、design 三个层面的内容。AI 需要将其拆分映射到 ODK 的三个独立产物：

```
brainstorming → 产出合并文档:
    ├── 前段：背景/目标/范围/成功标准    → proposal.md
    ├── 中段：用户故事/AC/错误码/接口     → spec.md
    └── 后段：架构/决策/模块影响/风险     → design.md

writing-plans → 按 ODK 模板格式化为 execution-plan.md:
    ├── Superpowers 已有精确的文件级任务清单
    └── AI 补齐 AC-Task 追溯表（从 spec.md 的 AC 编号反查）

TDD / subagent → 实现代码:
    └── AI 回填 execution-plan 代码范围映射（Task ↔ 实际文件）+ AC 到 Task 追溯验证状态

code-review → 生成 review 记录:
    └── AI 按 review 模板格式化 → evidence/reviews/
```

**注意**：Superpowers 的 brainstorming 产出是合并文档，不区分 design 和 spec。AI 在桥接时需要完成拆分，并按 ODK 模板补齐各产物缺失的章节（如 proposal 的 8 维 N/A 表、spec 的兼容性声明、execution-plan 的 AC-Task 追溯表）。

**注意**：Superpowers 的 review 结果是会话瞬态的。使用 `odk-review` 显式触发 AI 转录到 `evidence/reviews/`。

### ODK + OpenSpec

OpenSpec 的 `/opsx:propose` 一次覆盖 Define + Specify + Design + Plan，生成独立的 proposal.md、delta spec、design.md、tasks.md。产物已经拆分，不需要像 Superpowers 那样从合并文档中提取。

映射关系：

| OpenSpec 输出 | ODK 目标 | AI 需要补齐 |
|-------------|---------|-----------|
| `proposal.md` (Why/What/Capabilities/Impact) | proposal.md | 非目标、8 维 N/A 确认、成功标准表 |
| `specs/*.md` (ADDED/MODIFIED/REMOVED delta) | spec.md | 兼容性声明 |
| `design.md` (Context/Goals/Decisions/Risks) | design.md | 模块影响表、验证思路 |
| `tasks.md` (checklist) | execution-plan.md | AC-Task 追溯表、Task 详情卡 |

建议工作流：

```
odk-ops-propose  → OpenSpec 生成 proposal + spec + design + tasks（ODK 格式）
odk-ops-apply    → 实现代码 + 回填 code mapping
odk-review       → AI 补齐缺失章节 + execution-plan 代码范围映射 → 写入 .codespec/
odk-validate     → 校验归档完整性
```

### ODK + MatrixSpec

MatrixSpec 有独立的 SPEC.md 和 DESIGN.md 基线，以及增量模板（proposal/delta-spec/delta-design/tasks）。产物天然分离，映射较直接：

| MatrixSpec 输出 | ODK 目标 | AI 需要补齐 |
|---------------|---------|-----------|
| `proposal.md` (需求澄清+功能清单+DFX约束) | proposal.md | 8 维 N/A 确认（DFX 约束覆盖部分） |
| `delta-design.md` / `DESIGN.md` | design.md | 模块影响表、验证思路 |
| `delta-spec.md` / `SPEC.md` | spec.md | 兼容性声明 |
| `tasks.md` | execution-plan.md | AC-Task 追溯表 |

建议工作流：

```
odk-ms-proposal      → .codespec/proposal.md
odk-ms-delta-spec    → .codespec/spec.md
odk-ms-delta-design  → .codespec/design.md
odk-ms-tasks         → .codespec/execution-plan.md
odk-ms-validation    → evidence/reviews/
odk-validate         → 统一校验收口
```

### 关键原则

1. **单一归档源**：无论用几个插件，正式产出只在 `.codespec/` 一处
2. **AI 是桥**：ODK 不编排插件调用，AI 在上下文中同时拥有两套规范，自主完成拆分/补齐/映射
3. **过程件 = 归档件**：生成阶段的产出直接演化为归档件，不需要二次改写
4. **插件可替换**：可以从 ODK standalone 起步，后续随时引入其他插件增强特定阶段

## 目录约定

```
你的业务仓/
├── .codespec/
│   ├── profile.yaml                          # (可选) 子系统 profile 声明
│   └── changes/
│       └── issue-12345-arkui-focus/
│           ├── proposal.md
│           ├── design.md
│           ├── spec.md
│           ├── execution-plan.md
│           ├── spec-for-validation.md        # (可选) 旁路验证场景，odk-spec-for-validation 生成
│           ├── threat-model.md              # (可选) 高风险深度威胁分析，odk-security-threat-model 生成
│           └── evidence/                     # (可选) 过程证据
│               ├── reviews/
│               └── gates/
├── openspec/                                 # OpenSpec 工作区 (gitignored，odk-init 自动写入)
├── docs/superpowers/                         # Superpowers 工作区 (gitignored，odk-init 自动写入)
└── matspec/                                  # MatrixSpec 工作区 (gitignored，odk-init 自动写入)
```

## 下一步

- 阅读 [contracts.md](contracts.md) 了解每个产物必须包含的章节
- 阅读 [adapters.md](adapters.md) 了解各插件的精确章节映射和缺口
- 阅读 [core/profiles/README.md](../core/profiles/README.md) 了解 profile 定制
