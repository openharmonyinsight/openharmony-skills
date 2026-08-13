---
name: ohos-req-feature-proposal-baseline
description: Use when preparing an OHOS Feature and proposal review baseline in requirements Step 10-12, especially for 04-feature.md, proposals/*.md, SIG review readiness, built-in Review Ready Gate, proposal splitting, feature scope, acceptance criteria, or delivery impact. Do NOT use for requirement intake (ohos-req-requirement-intake), feasibility analysis (ohos-req-feasibility-analysis), or architecture decision (ohos-req-arch-decision).
metadata:
  author: openharmony
  scope: common
  stage: requirements
  capability: feature-proposal-baseline
  version: 0.4.0
  status: draft
  tags:
    - sdd
    - requirements
---

# OHOS Feature/Proposal 评审基线

**Announce at start:** "我正在使用 ohos-req-feature-proposal-baseline skill 生成 04-feature.md 并执行 Review Ready Gate。"

## 定位

04-feature.md 是 OHOS SIG 评审会议的 Feature/Proposal 基线输入；`proposals/*.md` 是 requirements 阶段的 proposal 索引产物，进入 ODK 交付阶段前必须按本 skill 的 ODK handoff 规则转换为 `.codespec/changes/<change-id>/proposal.md`。本 skill 合并原 Review Ready Gate：在生成 04-feature.md、生成全部 proposal 文件并经用户确认拆分/不拆分结果后，直接执行结构化 Gate 判定，输出 `Ready` / `Conditional Ready` / `Not Ready` 结论。工作量分级约束（PIR #152 P1）按端到端总人月推导：简单(≤5)/标准(≤8)/复杂(≤15)三级，复杂特性须有独立验收边界。模块覆盖完整性校验引用 02-feasibility.md §2.1 代码仓库分析表，缺失模块必须补行或写明排除理由。03-arch-decision-record.md §6 遗留问题闭环校验阻断 Not Ready Gate。

## ⭐ 思维准则

在给出拆分建议前，自问：是否按 R1→R2→R3→R4 顺序逐条评估？是否在首个触发处即停止，还是跳过了某些检查？
- Before checking module coverage, ask yourself: am I cross-checking 02 §2.1 against 04 §4 line-by-line, or eyeballing from memory?
- Before detecting terminology drift, ask yourself: am I comparing every 影响类型 label between 02 and 04, or skipping reusable ones?

## 输入

- `{docs_dir}/01-requirement.md`
- `{docs_dir}/02-feasibility.md`
- `{docs_dir}/03-arch-decision-record.md`

## 输出产物

- `{docs_dir}/04-feature.md`
- `{docs_dir}/proposals/05-proposal-<slug>.md`：每个 proposal 一份文件；即使用户确认不拆分，也必须生成 1 份 proposal 文件
- Review Ready Gate 结论写回 `04-feature.md`

## 流程

## 模板与产物命名

- 模板路径：`reference/feature.md`（模板文件不带 `04-` 阶段编号前缀）
- Proposal 模板路径：`reference/proposal.md`
- Proposal 审查矩阵路径：`reference/proposal-check-matrix.md`
- 产物路径：`{docs_dir}/04-feature.md`
- Proposal 产物路径：`{docs_dir}/proposals/05-proposal-<slug>.md`
- Proposal 审查结果路径：`{docs_dir}/proposals/proposal-check-<slug>.md`
- Proposal 文件命名：必须使用阶段号前缀 `05-proposal-` + 小写 kebab-case 语义短名，例如 `05-proposal-arkweb-file-drag-preview-control.md`；禁止使用 `P1-*.md`、`proposal-1.md` 或无 `05-` 阶段号的文件名。

1. 读取 `reference/feature.md` 和全部输入。
2. 从 `01-requirement.md` frontmatter 继承 `rr_id` 到 04-feature.md frontmatter，并在 §1 概述与价值后填写 RR单号表格行。
3. 收敛一句话特性、价值、目标/非目标、优先级范围和 AC。
4. 摘要记录选定方案、未选方案原因及 Phase 2 验证项。
5. 明确仓库、模块、Owner/SIG、交付物、里程碑、依赖和开放项。
6. 补充「需求变更影响性分析」章节（模板外补充章节，不对应模板 §-编号）：对以下五方逐项分析影响类型（正向优化/无影响/需适配）：
   - **北向应用开发者**：关注 API 变更、行为变更、兼容性
   - **南向开发者**：关注底层接口变更、新增能力
   - **分布式设备**：关注跨设备场景影响
   - **系统开发者（跨子系统）**：关注子系统间接口/依赖变更
   - **设备使用者**：关注用户可感知的功能/体验变更
7. **模块覆盖完整性校验**：提取 02-feasibility.md §2.1"关键代码仓库分析"表中所有仓库/模块，与 §4"受影响模块"表对比。02 中出现但 04 中缺失的仓库/模块必须补行或写明排除理由。在 §4 写入 **模块覆盖检查结论**：pass（齐全）或 warn（有排除理由），供本 skill 的内建 Gate 判定读取。
   - **降级规则**：若 02-feasibility.md 不含 §2.1 关键代码仓库分析表，则跳过模块覆盖校验并标注 `warn`（"模块覆盖校验未执行：02-feasibility.md 缺少 §2.1"），不 `fail`。
8. **影响类型术语校验**：对比同一模块在 02-feasibility.md §2.1 和 §4中的影响类型标签。漂移（如"可复用"→"需扩展"）必须在 §4 补充变更理由备注，并在 §4 写入 **术语一致性检查结论**：pass（无漂移）或 warn（有漂移已补理由），供本 skill 的内建 Gate 判定读取。
9. 判断是否拆分 proposal，并定义每个 proposal 的独立价值、边界、AC、**工作量估算**和依赖。拆分表必须包含每个 proposal 的估算工作量（人月）。**计算端到端总工作量**（= 各 proposal 工作量之和），按总人月推导复杂度（<5 简单 / 5-10 标准 / >10 复杂），填入 §5「端到端总工作量」与「复杂度」字段——此复杂度即 R3 拆分上限（简单≤5 / 标准≤8 / 复杂≤15 人月）的判定依据。
10. **生成 proposal 文件草稿**：读取 `reference/proposal.md`，为 §5 拆分表中的每个 proposal 生成 `{docs_dir}/proposals/05-proposal-<slug>.md`。不拆分时也必须生成 1 份 proposal 文件。每份 proposal 必须按模板原有 H1/H2 结构填写，并包含：
    - 从 04-feature.md 继承的 `feature_id`、`rr_id`、`target_release`
    - proposal 背景与问题、初始分级判断、目标/非目标
    - 1+8设备差异规格、DFX设计、用户故事与能力、成功标准、影响范围
    - 可选的外部依赖；无依赖时显式填写"不涉及"
    - 假设与开放问题、不涉及项确认（8 维）
    - proposal 边界、Owner/SIG、工作量、依赖、开放条件项写入模板对应章节，不新增模板外 H1/H2
11. **Proposal 审查 subagent**：在 proposal 草稿保存后，为 proposal 审查创建隔离 subagent。task 只传 4 类路径/信息，不嵌入正文：`reference/proposal-check-matrix.md`、`04-feature.md`、全部 `proposals/05-proposal-<slug>.md`、输出目录 `{docs_dir}/proposals/`。subagent 必须按矩阵逐项检视并为每个 proposal 输出 `{docs_dir}/proposals/proposal-check-<slug>.md`，格式为"总览+明细表"，列包含 `检查域 | 检查维度 | 检查条目 | 结论 | 证据 | 待SE澄清 | TSE复核`；`待SE澄清` 和 `TSE复核` 两列必须留空。subagent 回传主 session 的摘要不超过 15 行：proposal 数、PASS/WARN/FAIL 计数、必改项列表和审查结果路径。
12. **原 agent 回修 proposal**：主 session 读取审查结果，先修复所有可由 01-04/proposal 内部证据确定的 FAIL；对 AI 无法判定项保留 WARN 并在 proposal 对应章节标注待人工确认。回修后重新执行 Step 11，直到无可自动修复的 FAIL。禁止 subagent 直接修改 proposal 正文。
13. **⭐ 拆分结果确认门禁**：向用户展示 04-feature.md 中的拆分方案、已生成 proposal 文件列表和 proposal-check 摘要（每个 proposal 的路径、边界、工作量、Owner、依赖、PASS/WARN/FAIL 计数），等待用户确认或调整后才允许执行 Review Ready Gate。AI 不自行定稿拆分方案。
14. 保存 `{docs_dir}/04-feature.md`、全部 `{docs_dir}/proposals/05-proposal-<slug>.md` 和 `{docs_dir}/proposals/proposal-check-<slug>.md`。
15. 执行内建 Review Ready Gate（读取刚保存且经用户确认的 04-feature.md 和 proposal 文件），写入 `04-feature.md` 的固定 `## Review Ready Gate` 章节：`decision_gate` YAML、14 项检查表、条件项、后续观测项、FR→AC 追溯表。

## 职责边界

方案选型决策(ADR)由 `ohos-req-arch-decision` skill 负责，本 skill 只收敛 Feature/Proposal 评审基线。

## Proposal 审查矩阵

Proposal 审查使用 `reference/proposal-check-matrix.md` 作为唯一判据源。审查范围覆盖 4 个检查域：

| 检查域 | 检查条目数 | 判定重点 |
|--------|------------|----------|
| 诉求 | 5 | 问题描述、feature 溯源、成功标准可测性、1+8设备差异规格、DFX设计 |
| 场景 | 2 | US+AC 场景覆盖、AC 独立可测 |
| N/A项 | 8 | 性能、安全与权限、兼容性、API/SDK、IPC/跨进程、构建与部件、国际化/无障碍、数据迁移 |
| 交叉 | 4 | 非目标↔US、影响范围↔US、分级↔实际、多 proposal 一致性 |

判定规则：

- `PASS`：存在、完整、清晰、明确、无歧义；显式标注"不涉及"且有依据时视为 PASS。
- `FAIL`：不存在、缺失、模糊、有歧义；未显式标注"不涉及"的空白项按 FAIL 处理；结构缺失时先 FAIL，不继续细判该结构内部质量。
- `WARN`：AI 无法判定或需要人工二次判定；N/A 维度未发现明确矛盾但仍需人工确认时标 WARN，并在证据列追加"待确认是否准确"。
- `待SE澄清` 和 `TSE复核` 两列永远由人工填写，subagent 和主 session 均不得代填。
- 多 proposal 场景必须执行 proposal 间一致性检查；单 proposal 场景若无法验证整体溯源完整性，则 1.2 可标 WARN 并说明"当前仅检查单个proposal，建议放入多个proposal一起检查以验证溯源完整性"。

## 遗留问题闭环校验

在生成 04-feature.md 之前，必须校验 03-arch-decision-record.md §6 遗留问题闭环状态：

1. 读取 03-arch-decision-record.md §6 全部遗留项。
2. 对每条遗留项检查：负责人、解决动作、计划关闭时间 三字段是否齐全。
3. 任一遗留项缺少三字段 → Gate 降级为 Not Ready，block_reasons 记录缺失项。
4. §6 为占位（`[待用户评审会议后填写]`）且无实际遗留项 → Gate 降级为 Not Ready，block_reasons 记录"03-arch-decision-record.md §6 遗留问题未由用户评审会议输入"。
5. §6 无遗留项（用户评审会议认定无需遗留）→ 视为通过，无需阻断。

## Review Ready Gate（内建）

Gate 检查读取 01-04，不需要调用独立 skill。判定项为 9 项基础检查 + 3 项结构一致性 + 1 项遗留问题闭环：

| 检查项 | 要求 | 判定方法 |
|--------|------|----------|
| 概述与价值 | 有核心诉求和业务价值描述 | §1 章节存在且非占位符 |
| 范围明确 | 目标和非目标已列出 | §2 章节存在且非占位符 |
| AC 完整 | 每条 AC 均有标准、可观察指标和验证方式 | §3 每条 AC 行逐列检查；任一 AC 缺指标或验证方式→warn；所有 AC 为空或占位→fail |
| 受影响范围 | 明确跨仓模块、Owner/SIG | §4 至少 1 条影响范围行非占位符；任一受影响模块缺 Owner/SIG→warn；全空→fail |
| 拆分决策 | 有拆分结论和 proposal 边界 | §5 章节存在且非占位符 |
| Proposal 文件 | 每个拆分项均有实际 proposal 文件 | §5 proposal 表中的文件路径必须存在；不拆分时也必须存在 1 份 proposal |
| 工作量约束 | 每个 proposal 不超过复杂度上限 | §5 每个 proposal 工作量不超过简单≤5/标准≤8/复杂≤15 人月 |
| 技术方向 | 有选定方案 | 引用 03-arch-decision-record.md 选定方案 |
| 影响性分析 | 5 方影响类型已分析 | 影响性分析章节 5 行均非占位符 |
| GA 证据 | Proposal 若声明 GA-Approved 必须有 gate_a 证据 | 任一 proposal `status: GA-Approved` 且 `gate_a` 为空→fail；status 非 GA-Approved 且 gate_a 为空→warn 条件项，记录 Owner/动作/时点 |
| 模块覆盖完整性 | 04 §4 声明覆盖所有涉及模块 | 读取 §4"模块覆盖检查结论"；pass→pass，warn/缺失→warn |
| 影响类型术语一致性 | 04 §4 影响类型标签无漂移 | 读取 §4"术语一致性检查结论"；pass→pass，warn/缺失→warn |
| 条件项传播完整性 | §5 前置条件覆盖 02 §6 和 03 §6 条件项 | 缺失→warn |
| 遗留问题闭环 | 03 §6 遗留问题由用户评审会议输入且三字段齐全 | 占位或字段缺失→fail；用户认定无遗留→pass |

条件项分类：

- **当前评审可关闭条件项**：需求导入评审范围内可关闭的 warn 项，必须有 Owner、关闭动作、关闭时点；缺失任一字段则升级为 fail。
- **后续观测项**：依赖实现/测试阶段实测数据的指标（性能基准、功耗实测、内存占用基线、稳定性测试、压力测试等），记录 Owner 和目标关闭阶段，不阻塞 Gate 判定。

- `Ready`：所有检查项通过，可进入正式评审。
- `Conditional Ready`：无失败项，存在可关闭 warn 项且每条都有 Owner、关闭动作和时点。
- `Not Ready`：存在失败项，或存在可关闭 warn 项但缺少 Owner、关闭动作或关闭时点；禁止生成正式需求 PPT。

### Gate 输出契约

`04-feature.md` 必须包含固定 `## Review Ready Gate` 章节，位置在需求变更影响性分析之后。该章节是 `ohos-req-value-decision` 的上游输入，不允许自由文本替代。

```yaml
decision_gate:
  schema_version: "1.0"
  gate: "Ready | Conditional Ready | Not Ready"
  summary: "<一句话结论>"
  block_reasons:
    - "<Not Ready 阻塞原因；无则 []>"
  conditions:
    - id: "COND-01"
      description: "<当前评审可关闭条件项>"
      owner: "<负责人>"
      action: "<关闭动作>"
      due: "<关闭时点>"
  observations:
    - id: "OBS-01"
      description: "<后续观测项>"
      owner: "<负责人>"
      target_stage: "<目标关闭阶段>"
      non_blocking_reason: "<不阻塞理由>"
```

固定检查表必须包含 14 项检查项，列为 `检查项 | 结论 | 证据 | 条件项/阻塞项`，结论仅允许 `pass | warn | fail`。`decision_gate.gate` 由检查表推导：存在 fail 或缺 Owner/动作/时点的可关闭 warn → `Not Ready`；无 fail 且存在完整可关闭 warn → `Conditional Ready`；全部 pass 或仅后续观测项 → `Ready`。

### 旧 IR/SR/handoff 兼容边界

本 requirements 流程不再生成 `IR.md`、`SR.md` 或 `handoff.md`，也不自动改名、删除或覆盖历史目录中的同名旧产物。旧 IR/SR/handoff 只读保留，用于历史追溯；新流程的正式评审输入以 `01-requirement.md`、`02-feasibility.md`、`03-arch-decision-record.md`、`04-feature.md`、`proposals/05-proposal-*.md`、`value-decision-record.md` 为准。原 feature-to-ir 的 RR_MCP 写入、13 节平台评估、6 维人工确认、AC 编号继承在新版中分别由 `rr_id` 链路、`04-feature.md` 影响性分析/Gate、用户确认门禁和 FR→AC 追溯替代；ODK 交付阶段的 proposal 归档路径、执行边界和交付前置检查由 ODK 自身流程处理，不作为 requirements Step 1-14 前置条件。

### ODK 边界

`proposals/05-proposal-<slug>.md` 是 requirements 阶段的评审输入，不是 ODK 最终交付归档文件。本 skill 只要求 `rr_id` 从 01→04→proposal 继承、`target_release` 从 04/proposal frontmatter 继承或由用户确认；不推断 ODK `change-id`、不生成 `.codespec` 目录、也不补充 ODK 模板专有章节。

### GA 证据规则

`proposal.status` 仅允许 `Draft | GA-Approved`。当状态为 `GA-Approved` 时，`gate_a` 必须填写可访问的 GA 审视记录链接或归档路径；为空时 Gate 必须判定 `Not Ready` 并写入 `block_reasons`。当状态仍为 `Draft` 且 `gate_a` 为空时，Gate 至少生成一个当前评审可关闭条件项（Owner、补证动作、关闭时点），缺任一字段则升级为 `Not Ready`。不得在缺少 GA 证据时把 proposal 标为正式可交付。

### AC一致性校验

执行 Gate 后生成 FR→AC 追溯表，检查编号一致性：每条 FR 必须映射到至少一条 AC，AC 编号在 04-feature.md 内唯一且无遗漏。校验结果写入 04-feature.md §5 备注。

## 错误处理

| 场景 | 恢复指导 |
|------|---------|
| Not Ready (04-feature.md 内容不完整) | 告知用户缺失的具体章节，引导回本 skill 对应子步骤补全 |
| Not Ready (01-03 未完成) | 告知用户需先完成上游 Step 1/5/7 对应文档，列出缺失文档 |
| Conditional Ready | 列出条件项，引导用户确认是否接受条件放行或退回修改 |
| 拆分未确认 (Step 13 gate) | 提示用户确认拆分方案，不可自行定稿 |
| proposal 审查存在可自动修复 FAIL | 原 agent 读取 `proposal-check-<slug>.md` 后回修 proposal，再重新执行 proposal 审查 |
| proposal 审查存在无法自动判定 WARN | 保留 WARN，要求人工确认；不得自行把 WARN 改成 PASS |
| proposal 文件缺失 | 回到本 skill Step 10 生成缺失的 `{docs_dir}/proposals/05-proposal-<slug>.md`，不可只保留 04-feature.md 表格 |
| proposal 文件命名错误 | 重命名为 `05-proposal-<slug>.md` 并同步更新 04-feature.md §5、Gate 和回传路径 |

## 拆分规则

拆分规则详见 [reference/split-rules.md](reference/split-rules.md)。核心：R1仓库隔离→R2子系统隔离→R3工作量约束→R4默认不拆。工作量分级：简单≤5/标准≤8/复杂≤15人月。

## 自检

- [ ] 内容可追溯到 01-03
- [ ] RR单号已从 01-requirement.md 继承（frontmatter `rr_id` + §一表格）
- [ ] 目标、非目标、AC 和范围可评审
- [ ] 每条 AC 均有标准、可观察指标和验证方式；缺列已形成 warn 或 fail
- [ ] 影响范围有 Owner/SIG 和交付物
- [ ] proposal 模板已填写 `1+8设备差异规格` 和 `DFX设计` 独立章节；设备差异规格以三列表格填写，8类设备/差异项齐全；DFX 包含 `定位定界` 维度
- [ ] proposal 的 `外部依赖（可选）` 章节已填写；无依赖时显式标注"不涉及"
- [ ] 已使用 `reference/proposal-check-matrix.md` 通过 subagent 生成每个 proposal 的 `proposal-check-<slug>.md`
- [ ] 原 agent 已基于 proposal-check 修复可自动修复的 FAIL；剩余 WARN 已标注待人工确认
- [ ] Conditional 项有 Owner 和关闭时点
- [ ] 拆分结论包含事实依据
- [ ] 拆分表每个 proposal 有估算工作量（人月，不超过复杂度上限）
- [ ] §5 每个 proposal 行对应的 `{docs_dir}/proposals/05-proposal-<slug>.md` 已生成
- [ ] proposal 文件名均满足 `05-proposal-<slug>.md`，且 `<slug>` 为小写 kebab-case 语义短名
- [ ] 不拆分 proposal 时也已生成 1 份 proposal 文件
- [ ] §5 端到端总工作量字段已填写（= 各 proposal 工作量之和），复杂度与总工作量匹配
- [ ] 拆分结果已经用户确认（非 AI 自行定稿）
- [ ] 03-arch-decision-record.md §6 遗留问题由用户评审会议输入（非 AI 生成）
- [ ] 03-arch-decision-record.md §6 每条遗留项负责人/解决动作/计划关闭时间齐全
- [ ] `## Review Ready Gate` 章节按固定 schema 写入，`decision_gate` 与检查表一致
- [ ] proposal 若为 GA-Approved，则 `gate_a` 非空且证据路径/链接已写入 Gate 检查表

## NEVER

- **禁止 AI 自行定稿拆分方案**：拆分结果必须经用户确认后才允许执行 Review Ready Gate（原因：拆分涉及资源分配和交付优先级，属人类决策）
- **禁止只生成 04-feature.md 而不生成 proposal 文件**：04-feature.md 的 proposal 表是索引，不是正式 proposal 产物；每个 proposal 必须落盘为 `{docs_dir}/proposals/05-proposal-<slug>.md`（原因：后续交付阶段需要实际 proposal 输入）
- **禁止使用非阶段化 proposal 文件名**：requirements 阶段 proposal 文件名必须是 `05-proposal-<slug>.md`；不得使用 `P1-*.md`、`proposal-1.md`、`<feature-id>.md` 等格式（原因：proposal 由 Step 10 生成，但按 05 阶段化命名紧随 04-feature.md 排序）
- **禁止 AI 代行 §6 遗留问题生成**：遗留问题必须由用户评审会议输入，不得从 feasibility 条件项或风险自动推演（原因：AI 推演会引入虚构风险项）
- **禁止 Not Ready 时生成正式需求 PPT 或进入评审会议**：存在失败项时禁止把未就绪 Feature/Proposal 基线提交评审（原因：未通过门禁的需求进入下游会导致返工和评审阻塞）
- **禁止复制 01-03 详细论证**：04-feature.md 只收敛结论，不复制详细论证（原因：避免文档冗余和信息不一致）
- **禁止在 requirements 流程重新生成 IR/SR/handoff**：历史 IR/SR/handoff 只读保留，新流程不把它们作为前置条件或输出（原因：本流程已收敛为 01-04 + proposal + value decision）
- **禁止绕过 proposal 审查 subagent**：proposal 草稿生成后必须按 `reference/proposal-check-matrix.md` 审查并由原 agent 回修（原因：proposal 质量门禁与生成职责需要隔离）
- **禁止 subagent 直接修改 proposal 正文**：审查 subagent 只产出 `proposal-check-<slug>.md` 和摘要，原 agent 负责回修（原因：避免审查者和作者职责混淆）
- **禁止 AI 填写待SE澄清/TSE复核列**：两列必须留空交由人工审核（原因：该列代表人工审查职责）

## 输出

- 路径：`{docs_dir}/04-feature.md` 和 `{docs_dir}/proposals/05-proposal-<slug>.md`
- 方案摘要章节：改为一句话引用 03-arch-decision-record.md 选定方案，格式为 "选定方案: PATH-XX（参见 03-arch-decision-record.md）"，不重复决策细节
- 回传：04-feature.md 路径、proposal 文件路径列表、proposal-check 文件路径列表、RR单号、Gate 结论、评审建议、拆分结论、影响性分析结论、proposal 审查 PASS/WARN/FAIL 计数和阻塞项
