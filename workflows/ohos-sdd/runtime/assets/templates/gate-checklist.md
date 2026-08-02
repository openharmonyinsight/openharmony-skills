# 阶段检查清单

> 每个阶段的必过条件。按复杂度裁剪：简单变更只检查核心项，复杂变更全量检查。
>
> **说明**：本模板是阶段检查的参考清单。运行时产物可存储在 `.codespec/changes/{id}/evidence/checks/` 目录中，按阶段拆分为 `check-proposal.md`、`check-spec.md`、`check-design.md`、`check-execution-plan.md`，与 4 阶段一一对应。
>
> **阶段命名**：4 阶段模型为 Define（定义）→ Specify（规格说明）→ Design（设计）→ Plan（计划），与 ODK 主阶段命名保持一致。Gate 文件名按阶段命名：`check-proposal.md`、`check-spec.md`、`check-design.md`、`check-execution-plan.md`。
>
> **与 ODK Gate 的映射**：ohos-sdd 保留 4 个阶段 gate 文件用于细粒度过程证据，而 ODK 的人工门禁是 `GA / GB / GC` 三个 Gate。推荐映射为：`check-proposal.md` 对应 `GA`，`check-spec.md` + `check-design.md` + `check-execution-plan.md` 共同支撑 `GB`，最终实现/验证/交付证据由 `review.md` 与 `evidence/reviews/` 支撑 `GC`。
>
> **阶段结构**：每个阶段分为入口检查、工作检查和出口检查三部分。入口检查通过后才能开始本阶段工作；出口检查通过后才能进入下一阶段。命中 Profile 时，Profile 定义的 Gate 注入到对应阶段的同名插槽执行。

## 阶段总览

| 阶段 | 输入 | 输出 | 必过条件 |
|------|------|------|----------|
| 定义 | 原始需求 | `proposal.md` | 范围明确、AC 可测试、基线已审批 |
| 规格说明 | `proposal.md` | `spec.md` | AC、错误路径、兼容性和验证映射完整 |
| 设计 | `proposal.md` + `spec.md` | `design.md` | 设计约束清晰、与 Spec 一致 |
| 计划 | `proposal.md` + `spec.md` + `design.md` | `execution-plan.md` + `task.md` | Plan 已审批、文件范围和验证路径明确 |

---

## 前置：Profile 判定（四阶段之前必执行）

> 若仓路径或需求内容命中 `ohos-sdd/profiles/{profile}.md`，必须先加载 Profile 追加规则再进入四阶段。未命中时跳过本节。

- [ ] 已扫描 `ohos-sdd/profiles/` 目录，确认可用 Profile 列表
- [ ] 已根据仓路径或需求内容判定是否命中 Profile
- [ ] 若命中且有子 Profile，已进一步判定子 Profile
- [ ] Profile 追加规则已合并到后续阶段的检查项和 Gate 条件

---

## 一、定义阶段（进入规格说明条件）

### 入口检查

> **硬失败规则**：以下任一条件不满足，Define gate 必须判定为不通过：
>
> - `基线结论` 不是 `通过`
> - `澄清结论` 存在未勾选的适用项
> - `讨论记录` 中没有需求方/Owner/SIG 的明确确认证据
> - `manifest.baseline_approval.approved` 不是 `true`
> - 总结论只是 `条件通过`、`ReadyForReview` 或 AI 自评通过
> - 涉及 Public/System API、跨模块、多仓、UI/无障碍/国际化、兼容性或外部依赖的需求，被当作简单需求跳过澄清

- [ ] 原始问题和期望结果已记录
- [ ] 需求来源和责任人已明确
- [ ] 待澄清问题已逐项关闭，状态均为已澄清或明确 N/A
- [ ] 讨论记录包含需求方/Owner/SIG 的明确确认证据
- [ ] 澄清结论全部适用项已勾选
- [ ] 功能范围（包含/不包含）已确认
- [ ] API 变更已评估（如有）
- [ ] 兼容性和非功能需求已确认
- [ ] 依赖和风险已识别并有缓解方案
- [ ] 标准及以上需求已完成逐项澄清；复杂度降级有明确理由和确认人
- [ ] 目标仓 Agent 指南已检查（如 AGENTS.md/CLAUDE.md）；若存在，关键约束已记录

→ **Profile 入口 Gate**（命中 Profile 时，逐项执行 Profile 定义的 Define 入口 Gate，结果写入 `evidence/checks/check-proposal.md`）

> 源码核对、AI 推断、原始需求描述、文件已创建或 checklist 已勾选都不能替代明确确认。

### 出口检查

- [ ] 所有 P0/P1 用户故事有 AC（WHEN/THEN 格式）
- [ ] 每条 AC 可测试、可度量
- [ ] `proposal.target_release` 已确认或明确 TBD
- [ ] `manifest.profile` 已确认或明确 none
- [ ] 不涉及项已显式标记 N/A
- [ ] `manifest.baseline_approval.approved=true`，且 approver/evidence 非空
- [ ] `evidence/checks/check-proposal.md` 总结论为 `通过/Approved`

→ **Profile 出口 Gate**（命中 Profile 时，逐项执行 Profile 定义的 Define 出口 Gate，结果写入 `evidence/checks/check-proposal.md`）

- [ ] Define Gate 结论已反映到 proposal.md 状态字段（Draft → Baselined）

---

## 二、规格说明阶段（进入设计条件）

### 入口检查

- [ ] 并行产出锚点：proposal.md 中 API 变更项清单已填写（涉及 API 变更时）或已标记 N/A
- [ ] 并行产出锚点：design.md 和 spec.md 引用的仓/模块列表与 proposal.md 影响范围一致
- [ ] 上下文检索日志已创建，包含源码搜索、Agent 指南、官方文档、DeepWiki/多仓知识库等来源的命中或未命中记录
- [ ] 上下文结论已标注可信度；中/低可信结论未直接驱动设计或任务拆分
- [ ] 多仓/组件归属/API 影响无法仅凭源码确认时，已查询多仓知识库或记录未查询原因

→ **Profile 入口 Gate**（命中 Profile 时，逐项执行 Profile 定义的 Specify 入口 Gate，结果写入 `evidence/checks/check-spec.md`）

### Spec 检查

- [ ] 用户故事和 AC 完整
- [ ] AC 覆盖正常/异常/边界（AC 表含类型列标注）
- [ ] 规则表覆盖全部 P0/P1 AC（每个 AC 至少关联一条规则）
- [ ] 规则表每条通过质量检查（触发条件可复现、预期行为可观测、边界值已标注、关联AC已填写、无重叠冲突）
- [ ] Spec 中无 InnerKit 接口定义、内部实现流程或框架层实现细节
- [ ] API 变更分析完整（如有），含入参概要、返回值、错误码和开放范围
- [ ] 兼容性声明完整
- [ ] 非功能需求有指标或明确 N/A（含功耗和多设备差异）
- [ ] 全局特性影响已筛选
- [ ] 上下文引用完整
- [ ] 未使用的关键知识源有原因记录，不得把"未查询"写成"未命中"

### 出口检查

→ **Profile 出口 Gate**（命中 Profile 时，逐项执行 Profile 定义的 Specify 出口 Gate，结果写入 `evidence/checks/check-spec.md`）

- [ ] Specify Gate 结论已反映到 spec.md 状态字段（Draft/Review → Approved）

---

## 三、设计阶段（进入计划条件）

### 入口检查

→ **Profile 入口 Gate**（命中 Profile 时，逐项执行 Profile 定义的 Design 入口 Gate，结果写入 `evidence/checks/check-design.md`）

- [ ] 上一阶段 `spec.md` 已 Approved，且关键 AC/兼容性/错误路径已稳定
- [ ] 上下文检索日志已创建，包含源码搜索、Agent 指南、官方文档、DeepWiki/多仓知识库等来源的命中或未命中记录
- [ ] 上下文结论已标注可信度；中/低可信结论未直接驱动设计结论
- [ ] 多仓/组件归属/API 影响无法仅凭源码确认时，已查询多仓知识库或记录未查询原因

### 设计检查（跳过条件：简单变更无多模块/新 API /分层决策）

- [ ] 分层调用合规（应用→框架→服务→内核）
- [ ] 无跨层违规调用（除非 SA 代理）
- [ ] 子系统边界清晰、依赖已声明
- [ ] API 命名和参数符合 OH 规范
- [ ] 错误码不与已有子系统冲突
- [ ] 数据模型定义完整
- [ ] 构建系统影响已评估（BUILD.gn / bundle.json）
- [ ] 涉及 IPC/异步调用时，超时行为已定义
- [ ] 涉及 Public/System API 变更时，接口参数规约已填写

### 一致性检查（design.md 与 spec.md 交叉校验）

- [ ] 涉及仓和模块名称一致
- [ ] API 名称和变更类型一致（spec 列出变更项，design 给出签名细节）
- [ ] 架构约束不矛盾（spec 声明约束要求，design 给出满足方案）
- [ ] 不涉及项结论一致

### 出口检查

→ **Profile 出口 Gate**（命中 Profile 时，逐项执行 Profile 定义的 Design 出口 Gate，结果写入 `evidence/checks/check-design.md`）

- [ ] Design Gate 结论已反映到 design.md 状态字段（Draft/Review → Approved）

---

## 四、计划阶段（进入实现条件）

### 入口检查

→ **Profile 入口 Gate**（命中 Profile 时，逐项执行 Profile 定义的 Plan 入口 Gate；若 Profile 仍沿用历史 Implement 命名，则在本阶段执行其原入口 Gate，结果写入 `evidence/checks/check-execution-plan.md`）

- [ ] 当前 git 仓、分支、目标远端和允许修改文件清单已记录
- [ ] 工作区状态已检查；已有脏改与本任务关系已分类为复用/忽略/阻塞
- [ ] 多仓变更已拆分仓库边界、base 分支和 PR 方向
- [ ] 生成文件清单已识别；Plan 已说明生成源、生成命令或临时验证限制
- [ ] Plan 已审批，且审批发生在生产代码修改之前

### 执行计划检查

- [ ] AC 到 Task 有完整追溯
- [ ] 每个 Task 的文件范围明确
- [ ] 每个 Task 的不做范围明确
- [ ] Task 粒度合理（每个 Task 形成独立可验证的能力闭环）
- [ ] 交接信息完整
- [ ] Profile Spec for Validation 如已触发，`spec-for-validation.md` 来源一致、AC 完整、Profile 定义的分析与审批要求已满足，且不含开发自验证类型、用例、命令或结果

### 出口检查

→ **Profile 出口 Gate**（命中 Profile 时，逐项执行 Profile 定义的 Plan 出口 Gate；若 Profile 仍沿用历史 Implement 命名，则在本阶段执行其原出口 Gate，结果写入 `evidence/checks/check-execution-plan.md`）

- [ ] Plan Gate 结论已反映到 execution-plan.md 状态字段（Draft/ReadyForReview → Approved）

---

## 按复杂度裁剪

> 以下裁剪表是各模板字段"是否需要填写"的**权威判断源**。各模板 header 中的裁剪提示引用本表，不单独定义裁剪规则。

| 检查维度 | 简单 | 标准 | 复杂/关键 |
|----------|------|------|-----------|
| 需求基线 | 核心字段 | 全量 | 全量 |
| 设计审查 | 跳过（一句技术约束） | 关键决策 | 全量 + 设计扩展 |
| Spec | 核心 AC | 全量 | 全量 + 场景库 |
| 上下文收集 | 无 | 内嵌 Spec | 长期 analysis 资产 |
| 执行计划 | 1-2 Tasks | 完整 Plan | 完整 Plan + 多 Task |
| 规范符合性 | 跳过 | 全量 | 全量 |
| 代码质量 | 仅决策 | 全量 | 全量 + 专家 |
| 复盘 | 跳过 | 简略 | 详细 |
| 接口规格 | 跳过（写 N/A） | API 变更时必填 | 全量 + 行为场景覆盖 |
