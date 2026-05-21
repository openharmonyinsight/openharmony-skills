---
name: arkweb-spec-gen
description: ArkWeb 统一 Spec + 执行计划生成。从 proposal/requirement/design/review/analysis 聚合生成 4 合 1 的 spec.md 和 AC→Task 追溯的 task.md。触发词：生成 Spec、生成执行计划、生成 spec.md。
---

# ArkWeb Spec 生成

**Announce at start:** "我正在使用 arkweb-spec-gen skill 生成 spec.md 和 task.md。"

## 输入

必须读取以下 5 个文档：
1. `proposal.md` — 需求基线（Phase 1+3）
2. `requirement.md` — 需求基线评审（Phase 4）
3. `design.md` — 架构设计（Phase 4）
4. `review.md` — 评审报告（Phase 5）
5. `analysis.md` — 代码分析报告（Phase 2）

## 输出

1. `spec.md` — 统一规格文档（4 合 1），保存到 `docs/features/{feature-name}/spec.md`
2. `task.md` — 执行计划，保存到 `docs/features/{feature-name}/task.md`

## 模板

**【强制】生成文档前，必须先 Read 模板文件，严格按模板的章节结构、中文章节标题、表格格式填充内容。不得自行改为英文结构或英文标题。这是硬性要求，不是建议。**

- **spec.md：** 读取 `{DOCS_REPO}/assets/templates/spec.md`，按模板结构填充
- **task.md：** 读取 `{DOCS_REPO}/assets/templates/task.md`，按模板结构填充

## 流程

### Step 1: 读取全部输入文档

并行读取 5 个输入文档，提取关键信息：
- 从 proposal.md 提取：问题陈述、核心目标、不做范围、P0 AC、用户故事
- 从 requirement.md 提取：功能设计、接口定义、DFX 分析、设备矩阵、验收标准
- 从 design.md 提取：涉及仓和模块、关键设计决策（ADR）、设计骨架、适用架构规则
- 从 review.md 提取：确认的设计决策、🟡 遗留项（记录到 spec.md 已知限制章节）
- 从 analysis.md 提取：受影响文件清单、模块路径、代码可行性结论

### Step 2: 生成 spec.md

按模板结构生成 4 合 1 统一规格文档，包含四个章节：

**第 1 章：架构设计**（从 design.md 提取）
- 设计元数据（Design ID / title / parent_requirement / target_feature / owner / status）
- 需求基线摘要（问题陈述 / 核心目标 / 目标发行版本 / 不做范围 / P0 验收标准）
- 涉及仓和模块（仓库 / 模块路径 / 当前职责 / 本 Feature 影响）
- 适用架构规则（Rule ID / 适用原因 / 设计结论 / 验证方式）
- 设计目标和非目标
- 不涉及项确认
- 方案概览 + 架构图 + 数据流/控制流
- 关键设计决策（ADR）
- 设计骨架（API 骨架 / 模块骨架 / 测试骨架 + 验证方式）
- 风险和开放问题

**第 2 章：接口规格**（从 requirement.md 提取）
- 接口定义（参数表四段式：参数名/类型/必填/说明）
- 行为场景（输入→输出→副作用）
- 约束条件（性能/安全/兼容性）

**第 3 章：特性规格**（从 proposal.md + requirement.md 提取）
- 概述表（特性名称/编号/Epic/优先级/版本/SIG/状态）
- 用户故事 + 验收标准（WHEN/THEN）
- 业务规则表（BR）
- 异常规则表（AR）
- 豁免规则表（EX）
- 恢复契约表（RC）
- 验证映射表（VM）
- 验收追溯表（AC → 业务规则 → Task → 测试）
- API 变更分析（Public/System/Internal）
- 构建系统影响（BUILD.gn / bundle.json）
- 兼容性声明
- 质量门禁计划

**第 4 章：任务规格**（从 design.md + analysis.md 提取）
- 受影响文件清单（操作/路径/说明）
- 依赖关系（阻塞/被阻塞/外部）
- 代码变更规格（新增/修改/删除）
- BUILD.gn 变更
- repo-mapping
- 验证清单（编译/单测/接口/代码质量）

**已知限制章节：**
- 从 review.md 中提取 🟡 未处理项，记录在此

### Step 3: 生成 task.md

基于 spec.md 的 AC 和规则表，拆解为可独立执行的 Task：

- AC 到 Task 追溯表（确保每个 P0/P1 AC 至少映射到一个 Task）
- 首批实现边界（必须实现 / 可后置 / 不建议延后）
- 阶段计划
- Task 列表（Task ID / 目标 / 文件范围 / AC 映射 / 前置依赖 / 完成判据 / 验证命令）
- Task 详情（每个 Task 自包含：目标 / AC 映射 / 前置依赖 / 非目标 / 完成判据 / 停止条件 / 文件清单 / Spec Context / Design Context / Required Rules）

**Task 粒度原则：**
- 每个 Task 形成最小能力闭环
- Task 粒度控制在 AI 可独立完成的范围
- 没有 TBD/TODO/占位符
- 没有跨 Task 隐式依赖
- 没有"与 Task-N 类似"等引用

### Step 4: 自检

**spec.md 自检：**
- [ ] 无 TBD/TODO/占位符
- [ ] 所有 AC 使用 WHEN/THEN 格式
- [ ] 范围边界明确
- [ ] 接口定义参数表四段式完整
- [ ] 涉及仓和模块与 analysis.md 一致

**task.md 自检：**
- [ ] 每个 P0/P1 AC 至少映射到一个 Task
- [ ] 每个 Task 文件范围明确
- [ ] 每个 Task 有完成判据和停止条件
- [ ] Task 验证命令可执行
- [ ] 交接信息自包含

## 回复格式

```
✅ spec-gen 完成
📄 spec.md：{file_path}
📄 task.md：{file_path}
📋 spec.md 结构：
- 第1章 架构设计：涉及 {N} 仓，ADR {N} 项
- 第2章 接口规格：{N} 个接口定义
- 第3章 特性规格：{N} 条 AC，规则表 {N} 条
- 第4章 任务规格：{N} 个受影响文件
📋 task.md 结构：
- Task 总数：{N}
- AC 覆盖：{N}/{N}（P0: {N}/{N}）
- 阶段数：{N}
```
