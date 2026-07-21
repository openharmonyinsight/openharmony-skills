# Phase-Artifact Mapping

> **Related**: Issue #14, Issue #17, PR #3, PR #7
> **2026-06 dist note**: This design originally referenced generated files under `packaging/*`. After the dist-only migration, generated Claude/Codex/OpenCode outputs live under `dist/*`; `packaging/*` remains the static shell/input layer.

### 实施状态

| 章节 | 状态 | 说明 |
|------|------|------|
| Phase-Artifact 映射表 | 已落地 | `core/skills/using-odk/SKILL.md` Phase-Artifact Mapping section |
| AI 角色声明 | 已落地 | `using-odk` 和 `opencode.md` 中 |
| 阶段激活检测（意图+产出双信号） | 已落地 | `using-odk` Mapping section 中 |
| 软着陆路径 | 已落地 | `using-odk` Mapping section 末尾 |
| 多工具选择规则 | 已落地 | 列表格式，`using-odk` 和 `opencode.md` 中 |
| OpenCode 瘦身 | 已落地 | `opencode.md` 从 114 行精简到 47 行，详情下沉到命令文件 |
| 漂移校验 | 已落地 | `distribute-skills.sh` 新增 opencode.md ↔ using-odk 同步检查 |
| 自动附着规则 | 设计指导 | 附着行为由 AI 基于角色声明和映射表自行判断，不需要额外代码 |

## 问题

ODK 与其他插件（Superpowers、OpenSpec、MatrixSpec）组合使用时，用户面对两套重叠的命令体系：

```
ODK:        odk-propose → odk-spec → odk-design → odk-plan → [留白] → odk-review → odk-validate
Superpowers: brainstorming → writing-plans → TDD/subagent → code-review → verification
OpenSpec:   /opsx:propose(全阶段) → /opsx:apply → /opsx:sync → /opsx:archive
MatrixSpec: /matspec-proposal → /matspec-delta-spec → /matspec-delta-design → /matspec-tasks → /matspec-validation
```

这些命令是**同一阶段的不同入口**，不是串联调用关系。例如：

- `odk-propose` 和 Superpowers `brainstorming` 都覆盖"需求定义"阶段，产出 proposal.md
- `odk-plan` 和 Superpowers `writing-plans` 都覆盖"执行计划"阶段，产出 execution-plan.md
- OpenSpec `/opsx:propose` 一次覆盖 Define + Specify + Design + Plan 四个阶段

PR #7 尝试用 `odk-flow` 编排入口解决，将 Superpowers 硬编码为核心依赖。这个方向被拒绝，因为它改变了 ODK 的工具无关定位。

## 设计决策

**约束层自动附着（Constraint Layer Auto-Attachment）**，不是编排：

1. ODK **不编排**——不决定调什么插件、不路由命令
2. **AI 做桥**——AI 同时拥有 ODK 规范和其他插件能力，自主桥接两者
3. ODK **被动约束**——当任何插件驱动某个阶段时，ODK 模板约束自动附着到产出上
4. 映射表放在 `using-odk` 中——AI 只可靠使用活跃上下文中的信息
5. 表是**阶段维度**的——不枚举每个插件的命令，只定义阶段边界和 ODK 期望的产出形态

效果：用户调 Superpowers brainstorming → AI 自动按 ODK proposal.md 模板结构化产出 → 写入 `.codespec/`。用户不需要调两次，也不需要知道底层用了什么插件。

## AI 角色

映射表的核心前提是一个明确的角色声明：

> You are the bridge between ODK artifact requirements and implementation tools.
> Use whatever tools are available to produce quality outputs, then write results
> back into `.codespec/` in ODK format. Do not force the user to manually
> coordinate commands across plugins.

这设定了 AI 的心智模型：自主桥接，用户无感。AI 看到用户在讨论需求范围时，不管用户调的是 `odk-propose` 还是 `brainstorming`，都应该产出符合 ODK proposal.md 模板的 proposal。

## Phase-Artifact 映射表

以下映射表位于 `using-odk` 的上下文中。当任何工具驱动某个阶段时，产出必须符合对应的 ODK 模板。

| Phase | Artifact | Template | Key Constraints |
|-------|----------|----------|-----------------|
| Define | proposal.md | `core/templates/ai/proposal.md` | target_release, 非目标, 8 维度不涉及项 |
| Specify | spec.md | `core/templates/ai/spec.md` | AC 嵌套编号, 验证映射 |
| Design | design.md | `core/templates/ai/design.md` | 模块影响表, 设计决策对比表 |
| Validation (bypass) | spec-for-validation.md | `core/templates/ai/spec-for-validation.md` | 从 spec AC 派生验证场景, 不阻塞主流程 |
| Plan | execution-plan.md | `core/templates/ai/execution-plan.md` | AC-Task 追溯, 每个 Task 文件级代码范围 |
| Implement | (code changes) | — | 实现后回填 execution-plan 代码范围映射 |
| Review | evidence/reviews/*.md | `core/templates/review/*.md` | 逐 AC 合规结论 |
| Archive | (validation) | — | Level A/B/C/D 通过 |

### 阶段激活检测

使用**意图 + 产出双信号**识别当前阶段，意图优先于产出（因为用户可能在讨论阶段还没到写文件的时机）：

**意图信号**（用户在说什么）：

| 用户意图示例 | 映射到阶段 |
|-------------|-----------|
| "帮我分析下这个需求的范围" | Define |
| "列出所有验收条件" | Specify (spec) |
| "选哪个方案比较好" | Design |
| "拆一下任务" | Plan |
| "开始实现" | Implement |
| "检查下代码质量" | Review |
| "可以归档了吗" | Archive |

**产出信号**（即将写入什么文件）：

- 即将写入 proposal.md → Define
- 即将写入 spec.md → Specify (spec)
- 即将写入 design.md → Design
- 即将写入 execution-plan.md → Plan

**目录状态信号**：

- proposal 已存在，spec 缺失 → 提示进入 Specify
- spec 已存在，design 缺失 → 提示进入 Design

## 自动附着规则

### 触发条件

映射在 `using-odk` 被加载时自动生效（会话启动或用户提到 ODK 相关关键词）。不需要额外 hook 或配置。

### 附着方式

1. 当任何阶段被激活时（无论由哪个插件触发），AI 检查映射表确定当前阶段
2. 如果该阶段有对应的 ODK 模板，AI 读取模板文件获取章节要求
3. 产出写入 `.codespec/changes/<id>/` 下对应文件
4. 如果产出缺少 ODK 必需章节，提示用户补充

### 不附着的情况

- 普通 coding/debugging/build 任务（ODK 未激活）
- 用户明确表示不关联 ODK 交付件
- `.codespec/` 目录不存在且用户没有创建意图

### 软着陆

当 `.codespec/` 不存在但用户产出了符合 ODK 阶段的高质量内容时，AI 可以主动建议（仅建议，不强制）："这些内容可以归档到 ODK，需要我初始化 `.codespec/` 吗？"

这是从非 ODK 用户到 ODK 用户的自然转化路径。只在内容确实有价值且用户未明确拒绝 ODK 时触发。

## 组合处理

映射表是插件无关的——不关心哪个插件驱动阶段，只关心产出形态。

具体插件的文件映射、章节覆盖度、缺口回填详见 `docs/adapters.md`。各组合模式的推荐分工详见 `docs/workflows.md`。

### 多工具选择

当多个插件覆盖同一阶段时：

1. **用户显式调用的优先** — 用户主动调了 brainstorming，就按 brainstorming 的流程走
2. **未指定时选覆盖度更高的** — 参考 `docs/adapters.md` 章节覆盖度评估（如 Plan 阶段 Superpowers writing-plans 的 AC-Task 追溯比 OpenSpec tasks 更强）
3. **会话内保持一致** — 首次选择后记住偏好，同一会话中不再切换
4. **不确定时问一次** — 遇到真正不确定的场景问用户一次，不反复询问

### 关键原则

- **单一归档源** — 无论几个插件，正式产出只在 `.codespec/` 一处
- **不产生双份文档** — 插件的私有工作区只是草拟空间，不是正式归档
- **合并冲突解决** — 多插件覆盖同一阶段时，以人工确认的 kit 归档件为准

## 防膨胀策略

### 核心矛盾

约束越多 → 上下文越长 → AI 生成质量反而下降。

### 策略

1. **映射表本身极简** — 7 行表 + 双信号识别规则。不内联完整模板。
2. **渐进式加载** — 映射表给出模板路径，AI 只在进入该阶段时才读取模板文件获取详细章节要求。`using-odk` 不携带完整模板内容。
3. **不枚举插件命令** — 映射是阶段维度的，不是命令维度的。避免维护 25+ 行的插件-命令映射。
4. **引用现有文档** — 插件特定的适配器细节保留在 `docs/adapters.md` 和 `docs/template-injection.md`，不放入 `using-odk`。

### 上下文预算

> ⚠️ 以下数字为设计时估算（2026-05）。当前 `using-odk` 已拆分出 `using-odk-bridge`，实际行数可能有偏差。建议用 `wc -l` 重测后更新。

**Claude/Codex（按需加载）：**

| 组件 | 行数 |
|------|------|
| 现有 `using-odk` 内容（不变部分） | ~72 行 |
| AI 角色声明（bridge） | ~2 行 |
| Phase-Artifact Mapping 表 | ~10 行 |
| 阶段激活检测（意图+产出双信号） | ~10 行 |
| 软着陆 + 多工具选择（列表格式） | ~8 行 |
| Template Reference | ~5 行 |
| **总计** | **~113 行**（余量 ~7 行） |

**OpenCode（常驻注入，精简版）：**

| 组件 | 行数 |
|------|------|
| 同步注释 + 标题 + bridge | ~3 行 |
| Activation（含 skip guard） | ~8 行 |
| Phase Detection | ~12 行 |
| 多工具选择 | ~6 行 |
| Templates + Note | ~8 行 |
| **总计** | **~47 行**（从 114 行精简） |

OpenCode 版本不包含 Archive Structure、Key Rules、Traceability Chain、Available Commands 表——这些信息在 Ctrl+K 调用命令文件时按需加载。

## 与现有设计文档的关系

| 文档 | 职责 | 与本设计的关系 |
|------|------|---------------|
| `docs/adapters.md` | 每个插件的文件映射、章节覆盖度、缺口回填、模板注入方式 | 本设计的运行时映射表不重复这些细节；adapters.md 是参考手册 |
| `docs/template-injection.md` | Mode A/B/C 注入机制、L1/L2/L3 分级 | **分工：本设计定义"何时注入何模板"（策略），template-injection.md 定义"如何注入"（机制）。** 本设计通过 using-odk 上下文注入实现 L1 级约束；template-injection.md 定义 OpenSpec Schema Override、Superpowers Skill Wrapper 等具体注入路径 |
| `docs/workflows.md` | 5 种组合模式、slash command 设计、产物合并规则 | 本设计是 workflows.md 中"统一阶段命令"理念的运行时实现 |
| `docs/contracts.md` | 最小归档 contract 定义 | 映射表的 Artifact 列与 contracts.md 的 4 必需文件 + 可选 evidence 一致 |

## 对现有文件的影响

### 变更

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `core/skills/using-odk/SKILL.md` | 追加 ~42 行 | AI 角色声明 + Phase-Artifact Mapping + 阶段激活检测 + 软着陆 + 多工具选择 + Template Reference |
| `dist/claude/skills/using-odk/SKILL.md` | 自动生成 | distribute-skills.sh 重新生成 |
| `dist/codex/skills/using-odk/SKILL.md` | 自动生成 | distribute-skills.sh 重新生成 |
| `packaging/opencode/opencode.md` | 精简重写 | 从 114 行瘦身到 47 行（设计时目标，待重测） |
| `scripts/distribute-skills.sh` | 追加 ~20 行 | 新增 opencode.md ↔ using-odk 漂移校验 |

### 不变更

| 文件/目录 | 为什么不变 |
|----------|----------|
| 所有其他 core/skills/ | 映射是 using-odk 的上下文职责，不是独立技能 |
| core/templates/ | 模板内容不变，映射表只是引用它们 |
| hooks/session-start | ODK_ROUTER 轻量路由不变 |
| distribute-skills.sh | 脚本逻辑不变，只是重新执行 |
| README 文件 | 映射是内部机制，不需要用户感知 |
| docs/adapters.md, template-injection.md, workflows.md | 不变，继续作为参考文档 |

## 与 PR #3 / PR #7 的关系

| PR | 本设计的立场 |
|----|-------------|
| PR #3 (Superpowers workflow) | 评审模板结构化表格值得采纳（去除 Superpowers 品牌化）；core 模板硬编码 Superpowers 不采纳（本设计通过映射表实现等价效果，但不硬编码任何插件） |
| PR #7 (odk-flow orchestration) | 整体方向不采纳（Superpowers 核心依赖违反工具无关原则）；但 PR #7 识别的用户痛点（两套命令复杂度）是真实的，本设计用约束层附着而非编排来解决同一痛点 |

## 实施步骤

1. 在 `core/skills/using-odk/SKILL.md` 末尾追加：AI 角色声明 + Phase-Artifact Mapping + 阶段激活检测 + 软着陆 + 多工具选择 + Template Reference
2. 运行 `scripts/distribute-skills.sh` 重新生成 packaging 文件
3. 验证行数（`wc -l`）和内容正确性
4. **验证 `{{PLUGIN_ROOT}}` 在三个平台 packaging 中的变量替换结果**（新增的模板路径引用是否正确渲染为 `${CLAUDE_PLUGIN_ROOT}` / `${CODEX_PLUGIN_ROOT}`）
5. 本设计文档归档到 `docs/designs/`
