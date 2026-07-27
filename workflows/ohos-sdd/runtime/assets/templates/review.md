# Review Gate 模板

> 汇总 `GA / GB / GC` 三类人工门禁，以及实现草稿符合性、代码质量和最终验证结论。按复杂度裁剪审查深度。

## 审查元数据

| 项 | 内容 |
|----|------|
| Review ID | [REV-XXXX] |
| 审查阶段 | GA / GB / GC / 实现草稿符合性 / 代码质量 |
| 关联文档 | [spec.md / task.md / design.md 路径] |
| 复杂度 | 简单/标准/复杂/关键 |
| 涉及仓 | [仓列表] |
| Reviewer | [姓名] |
| 日期 | [日期] |
| Base SHA | [实现前提交] |
| Head SHA | [实现后提交] |

## 审查输入

| 输入 | 路径 | 说明 |
|------|------|------|
| Requirement | `[proposal.md]` | 需求基线 |
| Design | `[design.md]` | 设计文档 |
| Spec | `[spec.md]` | 特性规格 |
| Plan | `[execution-plan.md]` | 执行计划 |
| Diff | `[提交/PR]` | 实际改动 |

---

## 零、GA Proposal Gate

> 需求方向冻结点。GA 聚焦 `proposal.md` 是否足以进入 `Specify`。

> Gate 映射说明：
> - `GA` 对应 `check-proposal.md`
> - `GB` 由 `check-spec.md`、`check-design.md`、`check-execution-plan.md` 共同支撑
> - `GC` 主要由本文件的实现审查、代码质量审查、最终验证结论，以及 `evidence/reviews/`、验证日志和回归证据共同支撑

| 检查项 | 结论 | 证据 |
|--------|------|------|
| 目标、非目标、成功标准清晰 | PASS/FAIL | proposal.md |
| P0/P1 AC 可测试 | PASS/FAIL | AC 表 |
| 不涉及项与约束已确认 | PASS/FAIL | proposal.md |
| target_release / profile / Owner 基线明确 | PASS/FAIL | proposal.md |

**审批决策：**
- [ ] GA 通过，允许进入 Specify
- [ ] 需要修改 ___，修改后重审

**审批人：** [姓名]　**日期：** [日期]

---

## 一、GB Design Baseline Gate（Specify / Design / Plan 基线）

> 规格说明、设计和执行计划基线的审批记录。详细检查结果见 `.codespec/changes/{id}/evidence/checks/check-spec.md`、`check-design.md` 和 `check-execution-plan.md`。本区段在 Plan 进入真实实现前填写，后续实现审查可回顾。

| 检查项 | 结论 | 证据 |
|--------|------|------|
| 设计决策已记录并有取舍理由 | PASS/FAIL | design.md ADR-1~N |
| Spec 规则覆盖全部 P0/P1 AC | PASS/FAIL | AC 追溯表 |
| 异常规则无误伤风险（豁免/放行不误伤本该拦截的场景） | PASS/FAIL | 规则表异常类型条目 + 边界条件 |
| 恢复规则覆盖完整（触发→恢复路径→恢复结果） | PASS/FAIL | 规则表恢复类型条目 |
| 不涉及项已显式确认 | PASS/FAIL | 不涉及项确认表 |

**审批决策：**
- [ ] GB 通过，允许进入真实实现
- [ ] 需要修改 ___，修改后重审

**审批人：** [姓名]　**日期：** [日期]

---

## 二、实现草稿规范符合性审查

> 检查实现是否严格符合 Spec/Plan：不多、不少、不误解。

### 需求覆盖

| AC/规则/步骤 | 是否实现 | 证据 | 结论 |
|-------------|----------|------|------|
| [要求] | 是/否 | [文件/测试/命令] | PASS/FAIL |

### 多余实现

| 实现内容 | 是否在 Spec/Plan 中 | 风险 | 处理 |
|----------|---------------------|------|------|
| [内容] | 是/否 | [风险] | 保留/回退/修订Spec |

### 理解偏差

| 检查项 | 结论 | 证据 |
|--------|------|------|
| AC 理解是否正确 | PASS/FAIL | [证据] |
| 边界和不做范围是否遵守 | PASS/FAIL | [证据] |
| 适用规则是否遵守 | PASS/FAIL | [证据] |

---

## 三、代码质量审查

> 前提：规范符合性审查已通过。检查实现是否适合进入主线。

### 架构与分层合规

| 调用方 | 被调用方 | 合规？ | 说明 |
|--------|----------|--------|------|
| [方层级] | [方层级] | 合规/违规 | [说明] |

- [ ] 无应用层直接调用系统服务层（除非 SA 代理）
- [ ] 无框架层直接调用内核接口
- [ ] 无循环依赖

### API 与子系统边界

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 子系统间通过明确接口调用 | 通过/不通过 | [说明] |
| 跨子系统依赖在 bundle.json 中声明 | 通过/不通过 | [说明] |
| 无子系统间循环依赖 | 通过/不通过 | [说明] |

| API 签名 | 类型 | 命名合规 | 参数合规 | d.ts 位置 |
|----------|------|----------|----------|-----------|
| [签名] | Public/System/Internal | 通过/不通过 | 通过/不通过 | [路径] |

### Owner/Committer 视角

| 检查项 | 结论 | 证据 |
|--------|------|------|
| 模块边界是否合适 | PASS/FAIL/WARN | [证据] |
| 抽象层次是否合理 | PASS/FAIL/WARN | [证据] |
| 是否符合仓内既有模式 | PASS/FAIL/WARN | [证据] |
| 是否引入难维护结构 | PASS/FAIL/WARN | [证据] |

### 工程质量检查

| 检查项 | 结论 | 证据 |
|--------|------|------|
| 架构/分层规则 | PASS/FAIL/WARN | [证据] |
| API/兼容性规则 | PASS/FAIL/WARN | [证据] |
| 构建与部件规则 | PASS/FAIL/WARN | [证据] |
| 静态质量与风格 | PASS/FAIL/WARN | [证据] |
| 测试质量与可测试性 | PASS/FAIL/WARN | [证据] |
| 单测 SetUp/Teardown 初始化被测对象 | PASS/FAIL/WARN | [证据： SetUp 中构造并初始化被测对象实例] |
| 性能/安全/并发风险 | PASS/FAIL/WARN | [证据] |
| 多余实现或过度抽象 | PASS/FAIL/WARN | [证据] |

---

## 四、GC Final Delivery Gate

> 最终交付一致性门禁。聚焦验证证据、回归覆盖、兼容性与合入前风险。

| 检查项 | 结论 | 证据 |
|--------|------|------|
| 验证命令已真实执行且证据新鲜 | PASS/FAIL | [日志/报告] |
| AC 已逐条闭环 | PASS/FAIL | [追溯表] |
| 回归范围已覆盖或明确 N/A | PASS/FAIL | [regression-test.md / 测试报告] |
| 兼容性与发布风险已确认 | PASS/FAIL | [证据] |
| Open Issues 已处理或明确接受 | PASS/FAIL | [证据] |
| Profile Spec for Test（如触发）满足 Profile 审批要求并 Approved | PASS/FAIL/N/A | spec-for-test.md + check-spec-for-test.md |

**审批决策：**
- [ ] GC 通过，允许交付/合入
- [ ] 需要修改 ___，修改后重审

**审批人：** [姓名]　**日期：** [日期]

---

## 五、纠正循环

> 规范符合性审查不是一次性审查。有问题就修，修复后重审，最多 3 轮。超过 3 轮仍未通过则升级为架构评审。

| 轮次 | 结论 | 处理动作 | 复检范围 |
|------|------|----------|----------|
| Review-1 | [Approved/ChangesRequested] | [修复/修订] | [范围] |
| Review-2 | [Approved/ChangesRequested] | [修复/修订] | [范围] |
| Review-3 | [Approved/ChangesRequested] | [修复/修订] | [范围] |

规则：问题在实现层 → 修复后重审（最多 3 轮）/ 问题在 Spec、Design 或 Plan → 修订源头再重审 / 超过 3 轮仍未通过 → 升级为架构评审

---

## 六、Open Issues

| 类型 | 问题 | 处理方式 | Owner |
|------|------|----------|-------|
| blocker/risk/follow-up | [问题] | [修复/接受/后续] | [Owner] |

---

## 七、审查决策

| 项 | 内容 |
|----|------|
| Decision | Approved / ChangesRequested / Blocked / Superseded |
| 下一阶段 | [进入下一阶段 / 修订后重审 / 等待外部依赖] |
| Recheck Scope | [若需修改，列出重检范围] |
| 修改意见 | [阻塞项和建议项，含负责人和截止时间] |

**审查摘要：**
- 结论：
- 必须修复项：
- 可接受风险：
