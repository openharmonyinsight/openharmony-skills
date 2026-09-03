# 执行计划

> 将 Approved Spec 拆成可独立执行、可验证、可审查的 Task。每个 Task 用稳定 ID 和章节锚点引用上游事实，不复制 Spec/Design 正文。

## Plan 元数据

| 字段 | 内容 |
|------|------|
| Plan ID | [PLAN-XXXX] |
| 关联 Feature/Bug | [FEAT-XXXX / BUG-XXXX] |
| 关联文档 | proposal.md / design.md / spec.md |
| 复杂度 | 简单/标准/复杂/关键 |
| 状态 | Draft/ReadyForReview/Approved/Superseded |
| Owner | [Owner] |

## 输入状态

| 输入 | 路径 | 要求状态 |
|------|------|----------|
| Requirement | `[proposal.md]` | Approved |
| Design | `[design.md]` | Approved；简单变更可为简写约束或明确 N/A |
| Spec | `[spec.md]` | Approved |

## 执行原则

- **Spec 权威：** 实现与 AC、错误码、兼容性声明冲突时，停止并修订 spec/design/plan，不能在代码里自行改语义。
- **测试/证据先行：** 每个 Task 先确认失败测试或可复现证据缺口，再做最小实现并取得 fresh PASS 证据。
- **任务小型化：** 一个 Task 只覆盖一个独立闭环；跨接口、事件链、状态生命周期或构建边界的工作应拆分。
- **文件边界：** 只能修改 Task 的 Files/允许修改范围；需要额外文件时先修订 Plan。
- **状态所有权唯一：** 新增或修改状态必须明确 owner、key/index、创建、读取、更新、清理触发和不变量。
- **证据回填：** Task 完成当次会话回填追溯状态、实际文件、Commit、Review Evidence 和 Actual Result，不跨会话补证。
- **反伪完成：** 只补声明、只写存储、只覆盖 happy path、只跑无关测试或只填写 PASS 文本，都不能替代 AC 闭环。
- **生成文件：** 只修改生成源并运行生成命令；手工改生成物不能作为最终交付。

## 受影响文件全量清单

> 对照 design.md 调用链层级分析，逐层列出每层涉及的**具体文件**。从设计层到实现层的翻译步骤，遗漏文件意味着设计→实现映射不完整。

| 仓 | 层（来自 design.md） | 文件路径 | 修改类型 | 说明 |
|----|---------------------|----------|----------|------|
| [仓] | [NAPI/胶水/NWebImpl/DelegateInterface/Delegate/CEF Host] | `[路径]` | 新增/修改/删除 | [该文件承载什么职责] |

**检查项：**
- [ ] design.md 调用链每一层都有对应文件列出
- [ ] 每个文件修改类型和职责说明明确
- [ ] 无映射行的层意味着设计到实现的翻译缺失，需回溯补充 design.md

## AC 到 Task 追溯

> AC = Acceptance Criteria（验收标准）。spec 中每个验收标准必须映射到至少一个 Task。

| AC | 来源 | Task | 计划代码范围 | 实际 Code Ref | Commit | Review Evidence | 验证状态 |
|----|------|------|--------------|-----------------|--------|-----------------|----------|
| AC-1 | spec.md | TASK-1 | `[计划文件/符号]` | `[实际文件:行/符号]` | `[SHA]` | `evidence/reviews/[文件].md` | Pending/Pass/Fail/Blocked |

## 首批实现边界

**首批必须实现：** [核心能力、稳定性底线]
**可后置：** [增强项、非关键优化]
**不建议延后：** [延后会导致主链不闭合的内容]

## 阶段计划（如适用）

| 阶段 | 目标 | 关键 Task | 结束门槛 | 最小验证 |
|------|------|-----------|----------|----------|
| Phase-1 | [骨架/基础接线] | TASK-1, TASK-2 | [进入下一阶段的条件] | `[命令或人工检查]` |
| Phase-2 | [规则层/完整层] | TASK-3 | [阶段门槛] | `[命令或人工检查]` |

## Task 粒度原则

- 每个 Task 对应一个可独立验收的最小能力闭环
- 两项改动共享同一规则上下文和同一最小验证闭环 → 合并为一张 Task Card
- 文件范围、验证闭环和风险边界足够分离 → 拆分为多张 Task Card
- 简单变更：1-2 张 Task Card；复杂变更：按接线层/规则层/恢复层拆分
- 每个 Task 是可独立验证的最小能力闭环，任务边界由能力闭环决定，不单纯按代码行数或预估时间划定
- 单 Task 上下文（Spec + Design + 代码 + 测试）超过 3000 行时优先沿 AC/文件边界拆分；Handoff Summary 只引用本 Task 直接相关的 AC、规则和设计锚点

## 禁止项

执行计划和 Task 不得出现以下内容：

- [ ] 没有 TBD / TODO / 占位符
- [ ] 没有"根据需要实现""酌情处理"等模糊指令
- [ ] 没有跨 Task 隐式依赖（依赖必须显式声明在前置依赖列）
- [ ] 没有要求 Agent 自行寻找未列出的上下文文件
- [ ] 没有无验证方式的 AC
- [ ] 没有"与 Task-N 类似""参考 Task-N 实现"等引用（每个 Task 自包含）

## Task 列表

| Task ID | 目标 | 文件范围 | AC 映射 | 前置依赖 | 完成判据 | 验证命令 | 状态 |
|---------|------|----------|---------|----------|----------|----------|------|
| TASK-1 | [目标] | `[文件/目录]` | AC-1, AC-2 | 无/TASK-N | [完成状态] | `[命令]` | Pending/Done/Blocked/Skipped |

## Task 详情

### TASK-1: [名称]

| 字段 | 内容 |
|------|------|
| 任务目标 | [本 Task 必须交付的最小能力闭环] |
| AC 映射 | [AC-1, AC-2] |
| 前置依赖 | [依赖哪些 Task、规则、上下文前提] |
| 非目标 | [本 Task 明确不做什么] |
| 完成判据 | [达到什么状态才算完成] |
| 停止条件 | [遇到什么情况必须停止并回传] |
| Design 状态/不变量 | [STATE-*, INV-*；不涉及写 N/A] |

**状态所有权和生命周期**

> 无状态变更时填写一行 `N/A`，不得删除本节。

| Design Ref | 状态 | Owner | Key / Index | 创建 | 读取/更新 | 清理触发 | 生命周期不变量 |
|------------|------|-------|-------------|------|-----------|----------|----------------|
| `STATE-* / INV-* / N/A` | `[状态/N/A]` | [唯一 owner] | [键/索引] | [创建时机] | [读写方和条件] | [清理时机] | [必须始终成立的约束] |

**任务间接口（Produces / Consumes）**

> `Produces` 必须能被后续 Task 的 `Consumes` 精确引用；函数名、参数、错误码和数据结构不得靠执行者自行推断。无跨 Task 契约时填写一行“无”。

| Direction | Contract | Provider / Consumer | Dependency | Compatibility Constraint |
|-----------|----------|---------------------|------------|--------------------------|
| Produces | `[接口签名/错误码/innerAPI/数据结构]` | TASK-N | [供哪个 Task 使用] | [命名/ABI/序列化约束] |
| Consumes | `[接口签名/错误码/innerAPI/数据结构]` | TASK-N | [来自哪个前置 Task] | [版本/默认值/错误处理约束] |

**Read-only Context**

| 路径 | 读取目的 |
|------|----------|
| `[路径]` | [为什么本 Task 必须读取] |

**Files**

| 操作 | 文件 | 说明 |
|------|------|------|
| Modify/Create/Test | `[路径]` | [说明] |

**禁止修改文件**

| 文件/路径 | 原因 |
|-----------|------|
| `[路径]` | [生成物/其他 Task 所有/超出范围] |

**Spec References**

> 只写已存在的编号和章节锚点，禁止复制正文。每个 Task 至少引用一个 AC、一个规则 ID 和一个 `spec.md#章节`。

- AC / Rules: `AC-1.1`, `AC-2.3`, `R-2`
- Anchors: `spec.md#验收追溯`, `spec.md#规则定义`

**Design References**

> 引用 `ADR-*` / `STATE-*` / `INV-*` 或 `design.md#章节`；简单变更若 design 仅记录 N/A，也必须引用该章节及理由。

- IDs / Anchors: `ADR-2`, `INV-1`, `design.md#关键设计决策`, `design.md#状态归属与不变量`

**Required Rules**

| Rule ID | Must / Must Not |
|---------|-----------------|
| OH-ARCH-* | [摘要] |

**Steps**

- [ ] 写失败测试或定义验证用例（含 SetUp 初始化被测对象、Teardown 清理）
- [ ] 运行测试/验证，确认当前失败或缺失
- [ ] 做最小实现
- [ ] 运行测试/验证，确认通过
- [ ] 回填 AC 追溯、实际文件、Commit、Review Evidence、Actual Result 和计划偏差

**Reference Pattern**

| 参考实现 | 复用约定 | 偏差及理由 |
|----------|----------|------------|
| `[path:symbol]` / no prior art found | [调用链/命名/错误处理/状态/日志/测试] | [无/N/A/理由] |

**Anti-Fake Completion**

| Check | Required Evidence |
|-------|-------------------|
| AC closed | [关联 AC 的正向、异常、边界和兼容路径证据] |
| Scope respected | [实际 diff 与 Files/代码范围映射一致，或 Plan 已重新审批] |
| State lifecycle complete | [STATE-*/INV-* 的创建、读取、更新、清理和验证均覆盖；不涉及写 N/A + 理由] |
| Interface contract matched | [Consumes 与前置 Task Produces 的签名/错误码/数据结构一致] |
| Relevant verification | [验证命令直接覆盖本 Task，而非仅运行无关测试] |

**Verification**

| 证据类型 | 命令/路径 | Expected Result | Actual Result |
|----------|-----------|-----------------|---------------|
| 测试 | `[命令]` | [具体通过条件/失败原因] | [真实输出摘要 + PASS/FAIL + 日志路径] |
| 静态检查 | `[命令]` | [允许的 warning/error 数] | [真实输出摘要 + PASS/FAIL + 报告路径] |

**Handoff Summary**

> 交接信息只登记稳定引用和本 Task 的执行边界，不复制上游文档正文。

| 项 | 内容 |
|----|------|
| 任务描述 | TASK-1：[目标和能力闭环] |
| 允许修改 | `[路径]` |
| 允许新建 | `[路径]` |
| 只读参考 | `[路径]` |
| Spec 引用 | `AC-*` / `R-*` / `spec.md#章节` |
| Design 引用 | `ADR-*` / `STATE-*` / `INV-*` / `design.md#章节` / N/A + 理由 |
| 执行步骤 | 本 Task Card 的 `Steps` |
| 验证命令 | `[命令]` / 期望: PASS |
| 完成规则 | 不得修改允许范围外的文件；如需扩大范围，停止并修订 Plan；没有 fresh verification evidence，不得声明完成 |

**Review Handoff**

| Reviewer | Input |
|----------|-------|
| Spec Compliance | [AC→Task→Code→Commit、边界、额外行为和偏差] |
| Code Quality | [实际代码范围、风险点、Base/Head SHA、静态与测试结果] |
| Verification | [Expected/Actual、fresh evidence、回归与兼容性结果] |

## 代码范围映射

> Plan 审批时填写计划范围；实现后**如实回填实际范围和 Commit**（纯文档变更照填文档路径，不要清空或写 N/A）。三类 Review Evidence 状态触发：本表「实际文件/符号」列的值包含**代码文件/符号** → 归档必须三份 Approved（Evidence 列填文件路径，不得以 N/A 规避；N/A 后夹带代码路径不放行）；实际范围仅文档类文件（.md 等）或 `N/A：理由` → evidence 可选，一旦生成任一 evidence 文件则三份必须齐全且 Approved。实际文件超出计划范围时必须先修订 Plan，不能仅在“偏差”列解释后继续。

| Task ID | 计划文件/符号 | 实际文件/符号 | 操作 | Commit | Spec Compliance | Code Quality | Verification | 偏差 |
|---------|---------------|---------------|------|--------|-----------------|--------------|--------------|------|
| TASK-1 | `[计划路径:符号]` | `[实际路径:符号]` | Add/Modify/Delete | `[SHA]` | `evidence/reviews/spec-compliance.md#[锚点]` | `evidence/reviews/code-quality.md#[锚点]` | `evidence/reviews/verification.md#[锚点]` | 无/[已重新审批的 Plan 修订] |

## 实现偏差和开放问题

| Task ID | 类型 | 问题/偏差 | 处理状态 | 回退能力/Owner |
|---------|------|-----------|----------|----------------|
| TASK-1 | scope/spec/design/dependency | [说明] | Resolved/Blocked | [ohos-plan/ohos-spec/ohos-design/Owner] |
