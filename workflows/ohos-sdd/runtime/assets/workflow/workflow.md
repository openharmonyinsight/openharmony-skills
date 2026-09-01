# OHOS SDD 工作流（deliverables-centric）

> OpenHarmony 规范驱动开发 = **交付件依赖图 + 一致性骨干**。不是阶段流水线——
> 每个交付件有上游依赖，`ohos-sdd validate --level C` 机器强制依赖边一致。
> 4 阶段命名（Define / Specify / Design / Plan）只作交付件产出顺序的口语标签，不是 gate。

## 交付件依赖图

最小交付链：`proposal → spec → design → execution-plan → code`。四份文档始终存在，简单变更通过简写或明确 N/A 控制深度。`manifest.md` 是推荐运行时元数据。Evidence 门禁与复杂度无关（状态触发）：execution-plan 代码范围映射的实际范围包含代码文件时，归档必须三份 Approved Review Evidence；纯文档/规格变更（实际范围仅文档类文件或 `N/A：理由`）为可选旁证（存在即严校验）；`evidence/checks` 恒为可选旁证（存在即严校验）。声明支持 Spec for Validation 的 Profile 可在 spec/design Approved 后显式触发旁路：`spec + design → spec-for-validation`；如继续编写具体测试设计，则形成条件依赖 `spec-for-validation → test-spec`。
每个交付件的存在与内容都必须能由上游追溯，依赖边由 Level C 机器校验。

| 交付件 | 上游依赖 | 机器一致性检查（Level C 边） |
|--------|----------|------------------------------|
| proposal | （原始需求） | Agent Scope Guard 限定探索仓/模块、禁止项、知识源授权与越界回基线规则；不复制 Plan/Task 文件清单 |
| spec | proposal | proposal 的 `phase_status`、需求输入表“Define 阶段状态”、approval 记录和 `baseline_digest` 均已明确 Approved，且两处状态一致、摘要与当前 `需求基线` 一致；spec 验收追溯 ≥1 AC；AC 的 THEN 仅含终端用户或 Public/System/InnerAPI 可观察结果；每个 AC 有测试入口、Red 条件和通过标准；API/错误码事实有精确签名/数值、触发条件、来源和 AC/验证映射 |
| design | proposal + spec | design 引用的 AC 在 spec 存在；条件代码事实、既有模式、类图和 STATE/INV 追溯满足 Design Contract |
| execution-plan | proposal + spec + design | spec 每个 AC 在 plan 覆盖；“AC 到 Task 追溯”是 AC→Task 的单一事实源 |
| spec-for-validation（Profile 条件旁路） | spec + design | 来源 hash 一致；AC 集合与 spec 一致；design 已 Approved；格式、专项分析与审批满足 Profile 定义；不得包含内部实现信息 |
| test-spec（条件测试设计） | proposal + spec + design（如有）+ spec-for-validation（已触发 Spec for Validation 时） | 以 spec-for-validation 作为测试输入，转化为具体场景、环境、数据和证据设计；不回写开发自验证内容 |
| code | execution-plan | 计划文件范围已声明；Task 均为 Done，Expected/Actual 和实际文件已回填 |
| evidence/checks/* | 对应交付件 | per-交付件 provenance + 一致性结论（B 项） |
| evidence/reviews/*（状态触发） | spec + code | 实际范围含代码时三份 Approved 必需；纯文档变更可选，一旦启用则三份齐全且内容有效 |

## 一致性骨干（ohos-sdd validate）

- **Level A** 结构：required 交付件存在性（契约驱动，读 `artifacts.yaml`）。
- **Level B** 结构标题：Level C 要读的结构锚点（proposal 的需求输入表状态 / spec 验收追溯 / plan AC→Task 追溯 / ...），并校验 proposal frontmatter `phase_status` 与需求输入表“Define 阶段状态”一致。
- **Level C** 依赖边：上表的机器一致性检查（SDD 特有骨干）。
- **Level D** 归档就绪：四件套齐全、无占位符且实现闭环完整；实际范围含代码时要求三份 Approved `evidence/reviews/*`，纯文档变更可选且存在即严格校验。普通 validate 还检查 registry 存在。

`ohos-sdd archive <change>` 在写 registry 前执行 Level A/B/C + 无 registry 前置依赖的严格 Level D。任一检查失败都不得产生 registry 副作用；全部通过后才原子更新 registry。

## 按复杂度裁剪

四件套对所有复杂度固定存在；复杂度只决定写到什么深度及是否增加可选扩展。

| 阶段 | 简单 (单仓小修) | 标准 (单/双仓特性) | 复杂 (多仓/SIG) | 关键 (安全/性能路径) |
|------|-----------------|---------------------|------------------|-----------------------|
| 定义 | proposal.md (核心字段) | proposal.md (全量) | proposal.md + epic.md | proposal.md + epic.md |
| 规格说明 | spec.md (核心 AC) | spec.md (全量) | spec.md (全量+场景库) | spec.md (全量+合规审查) |
| 设计 | design.md（简短约束/N/A） | design.md (关键决策) | design.md (全量+扩展) | design.md (全量+安全/性能专项) |
| 上下文 | 无 | 内嵌 Spec | context-references 区段 | 长期 analysis 资产 |
| 计划 | execution-plan.md（1-2 Tasks） | execution-plan.md | 全量 Plan + 可选 task.md | 全量 Plan + 可选 task.md + 专家 |
| 审查/交付 | 与复杂度无关：实际范围含代码文件即三份 Approved evidence（纯文档变更可选） | 同左 | 同左 | 同左 + 专项 |
| 合入后验证 | 验证+合入 | 验证+合入+复盘 | 全量 | 全量+签名 |

## 交付件状态机

状态属于**单个交付件**，不是整个变更的全局阶段——每个交付件独立流转，下游交付件只接受上游 Approved 的输入。Define 首轮采用 `Clarifying → AwaitingApproval → Approved`，用于明确区分“澄清完成”和“批准 proposal”；其他交付件暂沿用下述通用状态机。

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

Define 的 `AwaitingApproval` 等价于“proposal 候选版本已完成并等待明确批准”，不等价于 Approved。回答澄清问题、表示没有补充或 `ReadyForReview` 均不得触发下游 Specify。

### Approval 记录格式

当前审批结论必须记录；历史审批记录如需保留，由审计日志或评审记录承载：

| 字段 | 要求 |
|------|------|
| 交付件 | proposal / spec / design / execution-plan / ... |
| 决策 | Approved / ChangesRequested / Blocked / Superseded |
| 审批人 | 人或 AI reviewer |
| 证据 | 检查报告、命令输出、评审记录或链接 |
| 下游 | 通过后作为输入的交付件 |
| 重检范围 | 如未通过，明确需要重检的内容 |

Define proposal 额外记录 `baseline_digest`，绑定获批时的 `需求基线` 内容。候选基线固定后用 `ohos-sdd approval-digest <change>` 生成摘要；该命令直接复用 validator 算法。需求基线发生变更后，保留原 approval 作为审计记录，但必须将 `phase_status` 置为 `awaiting_approval`、重新生成摘要并取得批准；digest 不一致时不得进入 Specify。

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
| 实现超出计划或测试缺失 | 停止完成声明；范围/拆分回 execution-plan，行为/设计偏差回对应源头 |
| 实现与 Spec/Design 不一致 | 回 spec/design/execution-plan 对应源头修正 |
| 代码质量或工程规则不合格 | 保持在执行/审查，不得宣称交付完成 |
| 验证证据不足 | 保持在执行/验证，不得宣称交付完成 |
| Profile 测试输入缺少行为或验证点 | 行为缺口回 spec；可观察性缺口回 design；刷新 spec-for-validation |

## 硬规则

这些规则仍是红线，只是不表现为"阶段 gate"，而表现为交付件流转的硬约束。

| 规则 | 说明 |
|------|------|
| Approved 才能流转 | 上游交付件未 Approved，不得作为下游输入 |
| 澄清完成不等于批准 | Define 澄清关闭后只能进入 AwaitingApproval；proposal frontmatter 中 `phase_status: approved` 且需求输入表“Define 阶段状态”为 `Approved`、approval.status/approver/evidence/approved_at/baseline_digest 完整、摘要与当前需求基线一致后，才能进入 Specify |
| 阶段状态单一真相源 | proposal frontmatter 的 `phase_status` 是机器读取的状态源；需求输入表“Define 阶段状态”是人工可读镜像，Level B 强制校验两者一致；proposal 不再重复记录恒真的 `phase: define` |
| 计划之前不得实现 | execution-plan 未通过前，不得修改生产代码 |
| 实现不得扩范围 | AI 只能修改 execution-plan 和 Task 列出的文件 |
| 探索不得自行扩范围 | Define 阶段由 proposal Agent Scope Guard 约束可检索仓/模块、禁止项和知识源授权；越界先停止并重新基线，精确实现文件仍只在 Plan/Task 维护 |
| 先定义不涉及项 | 需求阶段必须先明确 N/A 维度，避免实现阶段临时扩写 |
| 标准及以上必须先澄清 | 涉及 Public/System API、跨模块、多仓、UI/无障碍、国际化、兼容性或外部依赖的需求，默认至少为标准级；未完成逐项澄清和需求方确认前，不得写基线结论或进入下游 |
| 上下文检索必须可追溯 | Specify/Design 前必须记录知识源/源码检索日志；命中多仓知识库、DeepWiki、AGENTS/CLAUDE 指南或本地源码搜索时，必须记录查询、发现、可信度和用途；未使用也要记录原因 |
| Spec THEN 只能写外部行为 | 每个 AC 必须声明终端用户或 Public/System/InnerAPI 可观察表面；THEN 不得描述内部数据结构、状态机、调用链、类/方法、锁或算法 |
| 测试先定义真实 Red | 每个 AC 在 Spec 验证映射中必须给出测试入口、实现前具体失败信号和通过标准；纯规格补录的 N/A 必须带理由 |
| 代码事实先于设计结论 | 涉及既有实现时，design 必须用文件:行/符号记录已验证事实并转化为架构约束；推测和二手资料不能作为 Approved 设计基线 |
| 状态不变量必须可追溯 | 每个 design `INV-*` 必须关联 Spec AC、execution-plan Task、验证方式和通过标准，并由状态机、资源所有权或并发模型引用 |
| 先读仓库 Agent 指南 | 目标仓存在 AGENTS.md、CLAUDE.md 或同类 Agent 指南时，必须在 Define / Specify 阶段读取并把关键约束写入上下文记录；其约束优先于通用流程模板 |
| 实现前检查工作区边界 | 真正开始实现代码前必须记录目标 git 仓、分支、允许修改文件和当前工作区状态；已有脏改、生成文件或多仓边界不清时，先隔离 worktree 或升级为 Blocked/人工确认 |
| 生成文件不得手工合入 | 对 bridge、IDL、CAPI、cpptoc/ctocpp 等由生成器产出的文件，execution-plan 必须说明生成源和生成命令；无法重生成时，手工修改只能作为临时验证，不得作为最终合入方案 |
| 先符合 Spec，再谈代码质量 | 规范符合性审查通过后才进入代码质量审查 |
| 纠正循环 | 实现和 Spec/Plan 不一致时，先修复或回修源头，再重审 |
| 证据先于声明 | 没有运行过验证命令，就不能声称"通过了"。验证证据必须在 Task 完成后当次会话内生成，严禁跨会话补证 |
| 实现结果必须回填 | Task 状态、实际文件和 Actual Result 必须回填 execution-plan；Commit/Review Evidence 可作为项目增强证据 |
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
