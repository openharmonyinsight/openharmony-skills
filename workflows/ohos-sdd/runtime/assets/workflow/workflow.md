# OHOS SDD 工作流（deliverables-centric）

> OpenHarmony 规范驱动开发 = **交付件依赖图 + 一致性骨干**。不是阶段流水线——
> 每个交付件有上游依赖，`ohos-sdd validate --level C` 机器强制依赖边一致。
> 4 阶段命名（Define / Specify / Design / Plan）只作交付件产出顺序的口语标签，不是 gate。

## 交付件依赖图

核心依赖链：`proposal → spec → design → execution-plan → code`；`evidence/{checks,reviews}` 作旁证。声明支持 Spec for Validation 的 Profile 可在 spec/design Approved 后显式触发旁路：`spec + design → spec-for-validation`；如继续编写具体测试设计，则形成条件依赖 `spec-for-validation → test-spec`。
每个交付件的存在与内容都必须能由上游追溯，依赖边由 Level C 机器校验。

| 交付件 | 上游依赖 | 机器一致性检查（Level C 边） |
|--------|----------|------------------------------|
| proposal | （原始需求） | — |
| spec | proposal | spec 验收追溯 ≥1 AC（追溯 proposal 成功标准） |
| design | proposal + spec | design 引用的 AC 在 spec 存在 |
| execution-plan | proposal + spec + design | spec 每个 AC 在 plan 覆盖 |
| spec-for-validation（Profile 条件旁路） | spec + design | 来源 hash 一致；AC 集合与 spec 一致；design 已 Approved；格式、专项分析与审批满足 Profile 定义；不得包含内部实现信息 |
| test-spec（条件测试设计） | proposal + spec + design（如有）+ spec-for-validation（已触发 Spec for Validation 时） | 以 spec-for-validation 作为测试输入，转化为具体场景、环境、数据和证据设计；不回写开发自验证内容 |
| code | execution-plan | 受影响文件清单已声明（真实 git-diff 比对留后续 batch） |
| evidence/checks/* | 对应交付件 | per-交付件 provenance + 一致性结论（B 项） |
| evidence/reviews/* | spec + code | 逐 AC 审查结论，Level D 机器真相源（A 项） |

## 一致性骨干（ohos-sdd validate）

- **Level A** 结构：required 交付件存在性（契约驱动，读 `artifacts.yaml`）。
- **Level B** 结构标题：Level C 要读的结构锚点（spec 验收追溯 / plan AC→Task 追溯 / ...）。
- **Level C** 依赖边：上表的机器一致性检查（SDD 特有骨干）。
- **Level D** 归档就绪：registry 索引 + manifest frontmatter + `evidence/reviews/*`（或 `review.md` 兜底）。

## 按复杂度裁剪

不同复杂度产出**哪些交付件**、写到什么深度（不是"走哪些阶段"）。

| 阶段 | 简单 (单仓小修) | 标准 (单/双仓特性) | 复杂 (多仓/SIG) | 关键 (安全/性能路径) |
|------|-----------------|---------------------|------------------|-----------------------|
| 定义 | proposal.md (核心字段) | proposal.md (全量) | proposal.md + epic.md | proposal.md + epic.md |
| 规格说明 | spec.md (核心 AC) | spec.md (全量) | spec.md (全量+场景库) | spec.md (全量+合规审查) |
| 设计 | 跳过（一句技术约束） | design.md (关键决策) | design.md (全量+扩展) | design.md (全量+安全/性能专项) |
| 上下文 | 无 | 内嵌 Spec | context-references 区段 | 长期 analysis 资产 |
| 计划 | task.md (1-2 Tasks) | execution-plan + task.md | 全量 Plan + 多 task.md | 全量 Plan + 多 task.md + 专家 |
| 审查/交付 | review.md (仅决策) | review.md (规范+质量) | review.md (全量) | review.md (全量+专项) |
| 合入后验证 | 验证+合入 | 验证+合入+复盘 | 全量 | 全量+签名 |

## 交付件状态机

状态属于**单个交付件**，不是"阶段"——每个交付件独立 Draft → Approved。下游交付件只接受上游 Approved 的输入。

```
Draft → ReadyForReview → Approved → 作为下游输入
                ↑
        ChangesRequested → Draft (修订后重新检查)

Superseded: 被新版本替代（终态）
Blocked: 外部依赖阻塞（等待或升级 Owner）
```

### 状态含义

| 状态 | 含义 | 允许动作 |
|------|------|----------|
| Draft | 正在编写 | 修改当前交付件 |
| ReadyForReview | 等待检查 | 执行检查、人工审阅 |
| ChangesRequested | 未通过 | 修订交付件后重新提交 |
| Approved | 通过 | 作为下游交付件的输入 |
| Blocked | 外部阻塞 | 解决阻塞或升级 Owner |
| Superseded | 已被替代 | 不再作为下游输入 |

### Approval 记录格式

每次交付件审批必须记录：

| 字段 | 要求 |
|------|------|
| 交付件 | proposal / spec / design / execution-plan / ... |
| 决策 | Approved / ChangesRequested / Blocked / Superseded |
| 审批人 | 人或 AI reviewer |
| 证据 | 检查报告、命令输出、评审记录或链接 |
| 下游 | 通过后作为输入的交付件 |
| 重检范围 | 如未通过，明确需要重检的内容 |

## 一致性修复

依赖边 / 一致性失败时，**回到对应的源头交付件**修复，由 `ohos-sdd validate` 的 `rework_capability` 路由到拥有该交付件的能力。

| 发现问题 | 回退到（交付件） |
|----------|------------------|
| 原始需求不完整或目标不清 | proposal |
| AC、范围、非范围不稳定 | proposal |
| 行为规则、异常路径、兼容性口径不清 | spec |
| 模块边界、API、构建路径不清 | design |
| Spec 与 Design 不一致 | spec 或 design |
| 上下文不足或 DeepWiki 结论冲突 | spec / design |
| Task 粒度过大、文件范围不清 | execution-plan |
| 实现超出计划或测试缺失 | execution-plan |
| 实现与 Spec/Design 不一致 | 回 spec/design/execution-plan 对应源头修正 |
| 代码质量或工程规则不合格 | 保持在执行/审查，不得宣称交付完成 |
| 验证证据不足 | 保持在执行/验证，不得宣称交付完成 |
| Profile 测试输入缺少行为或验证点 | 行为缺口回 spec；可观察性缺口回 design；刷新 spec-for-validation |

## 硬规则

这些规则仍是红线，只是不表现为"阶段 gate"，而表现为交付件流转的硬约束。

| 规则 | 说明 |
|------|------|
| Approved 才能流转 | 上游交付件未 Approved，不得作为下游输入 |
| 计划之前不得实现 | execution-plan 未通过前，不得修改生产代码 |
| 实现不得扩范围 | AI 只能修改 execution-plan 和 Task 列出的文件 |
| 先定义不涉及项 | 需求阶段必须先明确 N/A 维度，避免实现阶段临时扩写 |
| 标准及以上必须先澄清 | 涉及 Public/System API、跨模块、多仓、UI/无障碍、国际化、兼容性或外部依赖的需求，默认至少为标准级；未完成逐项澄清和需求方确认前，不得写基线结论或进入下游 |
| 上下文检索必须可追溯 | Specify/Design 前必须记录知识源/源码检索日志；命中多仓知识库、DeepWiki、AGENTS/CLAUDE 指南或本地源码搜索时，必须记录查询、发现、可信度和用途；未使用也要记录原因 |
| 先读仓库 Agent 指南 | 目标仓存在 AGENTS.md、CLAUDE.md 或同类 Agent 指南时，必须在 Define / Specify 阶段读取并把关键约束写入上下文记录；其约束优先于通用流程模板 |
| 实现前检查工作区边界 | 真正开始实现代码前必须记录目标 git 仓、分支、允许修改文件和当前工作区状态；已有脏改、生成文件或多仓边界不清时，先隔离 worktree 或升级为 Blocked/人工确认 |
| 生成文件不得手工合入 | 对 bridge、IDL、CAPI、cpptoc/ctocpp 等由生成器产出的文件，execution-plan 必须说明生成源和生成命令；无法重生成时，手工修改只能作为临时验证，不得作为最终合入方案 |
| 先符合 Spec，再谈代码质量 | 规范符合性审查通过后才进入代码质量审查 |
| 纠正循环 | 实现和 Spec/Plan 不一致时，先修复或回修源头，再重审 |
| 证据先于声明 | 没有运行过验证命令，就不能声称"通过了"。验证证据必须在 Task 完成后当次会话内生成，严禁跨会话补证 |
| 不得把 ReadyForReview 当作 Approved | Agent 看到上游状态不是 Approved 时必须停止 |
| 不得用"看起来可以"替代结论 | 每个交付件必须有明确证据支撑的决策 |

## Reviewer 分工

| Reviewer | 关注点 |
|----------|--------|
| Spec 符合性审查 | 不多、不少、不误解——实现与 Spec 精确对应 |
| 代码质量审查 | 架构、代码结构、测试覆盖、工程规范、可维护性 |
| 验证审查 | 命令是否真实运行，证据是否覆盖所有 AC |

## 产物状态

状态写入对应文档的元数据字段。文件存在、checklist 全部勾选、人工审批证据完整且无硬失败项，才表示该交付件通过；文件存在或 AI 自评通过都不能替代结论。
