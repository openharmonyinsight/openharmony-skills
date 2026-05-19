# Initial design.md Generation Guide

When the functional-domain directory has no `design.md`, generate one first as the design baseline shared by all Feats in that domain. Reference example: `specs/04-common-capability/03-common-attributes/01-layout-attributes/design.md` (layout-attributes domain, currently containing Feat-01/02). Chapter titles below stay in Chinese because that's the actual format used in generated design files.

## File location and naming

- Path: `specs/<func-domain-path>/design.md` (fixed filename)
- A functional domain has **exactly one** design.md, covering every Feat in that domain

## Standard chapter skeleton (13 top-level H2s, fixed order)

```
# 架构设计
> <one-line statement of the functional domain's role>

## 设计元数据
## 需求基线
## 上下文和现状
### 涉及仓和模块
### 适用架构规则
## 不涉及项承接
## 关键设计决策
## 设计骨架
### 骨架范围
### 骨架 Spec 拆分
## 后续 Task 拆分
## API 签名与权限
### 新增 API
### 变更/废弃 API
## 构建系统影响
### BUILD.gn 变更
### bundle.json 变更
## 可选设计扩展
### 架构图
### 数据流/控制流
### 时序设计
### 数据模型设计
### 算法与状态机
### 测试性设计
### 异常传播时序图
### 资源所有权矩阵
### 接口参数规约
### 线程与并发模型
## 详细设计
### <capability-1>
### <capability-2>
...
## 风险和开放问题
## 设计审批
```

## Per-chapter content requirements

### 设计元数据 (table)

| Field | Content |
|-------|---------|
| Design ID | `DESIGN-Func-<domain-numbers>` (e.g. `DESIGN-Func-04-03-01` for 04-common-capability/03-common-attributes/01-layout-attributes) |
| 关联需求 | "已有能力补录（无独立 requirement.md）" / path to the linked requirement.md |
| 关联 Epic | "无" / Epic name |
| 目标 Feature | List the Feat-XX being generated now (the first feature). New Feats are appended here later. |
| 复杂度 | 简单 / 标准 / 复杂 / 关键 |
| 目标版本 | API version range |
| Owner | ArkUI SIG / specific team |
| 状态 | Baselined（已有实现补录） / Drafting / Approved |

### 需求基线

> 需求基线详见 proposal.md。以下仅列出设计阶段需要额外强调的要点。

| 项 | 补充说明（如需） |
|----|------------------|
| [对设计有直接约束的基线项] | [补充说明] |

### 上下文和现状

`涉及仓和模块` table — required columns: 仓库 | 模块路径 | 当前职责 | 本 Feature 影响.

`适用架构规则` table — populate OH-ARCH-* rules with their design conclusions. Standard rules:

| Rule ID | 适用原因 | 设计结论 | 验证方式 |
|---------|----------|----------|----------|
| OH-ARCH-LAYERING | [涉及层级调用] | [调用方向和边界结论] | 架构评审/依赖检查 |
| OH-ARCH-SUBSYSTEM | [涉及跨子系统] | [允许/禁止调用] | 代码评审/依赖检查 |
| OH-ARCH-IPC-SAF | [涉及跨进程/SA] | [IPC/SAF 结论] | 集成测试 |
| OH-ARCH-API-LEVEL | [涉及 API 变更] | [级别/权限/SysCap 结论] | API 评审/XTS |
| OH-ARCH-COMPONENT-BUILD | [涉及构建/部件] | [BUILD.gn/bundle.json 影响] | 构建验证 |
| OH-ARCH-ERROR-LOG | [涉及错误码/日志] | [错误码/日志结论] | 单测/hilog |

### 不涉及项承接

> proposal.md 已完成 N/A 判定。本节仅对 proposal 中标记为"涉及"且需展开设计的维度给出结论。

| 维度 | 设计结论 |
|------|----------|
| [proposal 中标记"涉及"的维度] | [展开设计方案 / 结论] |

### 关键设计决策 (table)

ADR table — columns: 决策 ID | 问题 | 推荐方案 | 探索过的替代方案 | 取舍理由 | 影响.

Initial ADRs are numbered `ADR-1, ADR-2, ...` (baseline decisions). Decisions added later by subsequent Feats use `ADR-FX-N` (e.g. `ADR-F2-1` is the first decision of Feat-02).

### 设计骨架

`骨架范围` table — columns: 骨架项 | 目标 | 不包含 | 验证方式.

`骨架 Spec 拆分` table — columns: Task ID (`TASK-SKELETON-N`) | 目标 | 受影响文件 | AC.

### 后续 Task 拆分 (table)

Columns: Task ID | 目标 | 受影响文件 | 依赖. First row registers the baseline task.

### API 签名与权限

> 本节承接 spec.md"API 变更分析"中识别的 API，给出签名、权限和 d.ts 位置等实现细节。

`新增 API` table — columns: API 签名 | 类型 (Public/System/Internal) | d.ts 位置 | 权限要求 | SysCap.

`变更/废弃 API` table — columns: 原有 API | 变更类型 (变更/废弃) | 新 API | 迁移说明.

### 构建系统影响

`BUILD.gn 变更` — code block with 文件路径 and 变更说明.

`bundle.json 变更` — description of 新增 component / 修改依赖关系.

### 可选设计扩展

Each subsection is marked with `<!-- 展开 -->` and contains:

- **架构图**: Mermaid `graph` diagram showing layering (API layer / Property layer / Render layer / Layout algorithm layer). **Must use Mermaid** — do NOT use ASCII box art. Preferred subgraph types: `graph TB` for layered architectures, `graph LR` for data flow, `graph TD` for pipeline steps.
- **数据流/控制流**: Table with columns 步骤 | 调用方 | 被调用方 | 数据/接口 | 说明
- **时序设计**: Mermaid `sequenceDiagram`
- **数据模型设计**: TypeScript (API-layer types) + C++ (framework-layer structs)
- **算法与状态机**: Mermaid `stateDiagram-v2` or algorithm pseudocode
- **测试性设计**: Table with columns 测试层级 | 测试目标 | Mock 策略 | 验证方式
- **异常传播时序图**: Mermaid `sequenceDiagram` covering all exception/recovery rules
- **资源所有权矩阵**: Table with columns 资源 | 创建方 | 持有方 | 销毁触发 | 实际释放 | 异常回收
- **接口参数规约**: Table with columns 接口 | 参数 | 类型 | 合法范围 | 非法处理 | 边界说明
- **线程与并发模型**: Table with columns 操作 | 发起线程 | 回调线程 | 跨进程边界 | 线程安全 | 重入约束

## Diagram style guide

All diagrams in design.md and spec files **must use Mermaid syntax** (rendered by GitHub, GitLab, and most Markdown viewers). Do NOT use ASCII art box diagrams.

| Diagram type | Mermaid directive | When to use |
|-------------|-------------------|-------------|
| Layered architecture | ````mermaid\ngraph TB` | Showing subsystem layers (API → Property → Layout → Render) |
| Pipeline / flow | ````mermaid\ngraph TD` | Sequential steps with branching (constraint pipeline, dirty-node drain) |
| Decision tree | ````mermaid\ngraph TD` with `{"diamond"}` nodes | Mutual-exclusion priority (position/offset/anchor priority) |
| Sequence / timing | ````mermaid\nsequenceDiagram` | Cross-component call chains (VSync → FlushBuild → Layout) |
| State machine | ````mermaid\nstateDiagram-v2` | State transitions and lifecycle |
| Nested box model | ````mermaid\ngraph TB` with `subgraph` | Containment relationships (margin → border → padding → content) |

Keep Mermaid diagrams **flat enough to render well** — avoid nesting subgraphs more than 2 levels deep. Use `<br/>` for multi-line labels inside nodes.

### 详细设计

Each `### <capability>` subsection contains: algorithm pseudocode / formulas / flow diagrams / worked examples. Every source reference must include `frameworks/.../file.cpp` plus line number.

### 风险和开放问题 (table)

Columns: 项 | 类型 (兼容性 / API / 架构 / 文档 / 性能 / 安全) | 影响 (高/中/低) | 处理方式 | Owner.

### 设计审批

Fixed 10-item checkbox list:

```
- [x] 需求基线已确认，设计覆盖 P0/P1 AC
- [x] 不涉及项已承接，N/A 和展开项都有结论
- [x] 涉及仓和模块职责清楚
- [x] 适用架构规则已识别并形成设计结论
- [x] 分层和子系统边界合规
- [x] API 变更有签名、权限、错误码和兼容性说明
- [x] BUILD.gn/bundle.json 影响明确
- [x] 设计输出和后续 Task 拆分明确
- [x] 关键设计决策有理由和影响说明
- [x] 风险和开放问题有 Owner
```

Followed by a conclusion line: `**结论:** 通过（已有实现补录）`.

## Generation steps

1. **Resolve Design ID**: derive `DESIGN-Func-XX-XX-XX` from the feature path
2. **Lay down the 13 top-level chapters** in the fixed order above
3. **Baseline ADRs**: convert Step 3 highlights into `ADR-1, ADR-2, ...` (all decisions of the first Feat are baseline — no `FX` prefix)
4. **Baseline architecture diagram / data model / detailed design**: place directly into the corresponding chapters **without** `(Feat-XX)` suffixes
5. **Register the first spec**: add the new spec filename to the "后续 Task 拆分" table

## Relationship with incremental merging

- **First Feat**: follows this initial-generation path; everything goes in as the **baseline**
- **Subsequent Feats**: follow `design-doc-merge.md` and append using `ADR-FX-N` / `#### XX（Feat-XX）` subheadings **without** touching baseline structure

## Anti-patterns

❌ Creating one design.md per Feat (one functional domain → one design.md)
❌ Naming first-Feat decisions `ADR-F1-N` (they should be baseline `ADR-1, ADR-2, ...`)
❌ Skipping `## 不涉及项承接` or `## 设计审批`
❌ Inventing a custom Design ID format (must be `DESIGN-Func-XX-XX-XX`)
