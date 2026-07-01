# Feat-XX-spec.md Chapter Skeleton

Use this H1/H2/H3 structure to generate the spec file. Reference implementation: `specs/04-common-capability/03-common-attributes/01-layout-attributes/Feat-01-size-properties-spec.md`. Chapter titles below are written in Chinese because that's the actual format used in generated spec files — keep them verbatim.

> **复杂度裁剪提示：** L0（简单）需求可精简填写"接口规格""多设备适配""全局特性影响"等章节（写"无新增接口规格"/"无差异"/"否"即可）；L1+ 需求涉及时必须完整填写。详细裁剪规则见 `gate-checklist.md` 按复杂度裁剪表。

## Full chapter list (in order)

```
# 特性规格
## 概述
## 本次变更范围（Delta）
## 输入文档
## 用户故事
### US-1: <story title>
### US-2: ...
### US-N: ...
## 验收追溯
## 规则定义
## 验证映射
## API 变更分析
### 新增 API
### 变更/废弃 API
## 接口规格
### 接口定义
## 兼容性声明
## 架构约束
## 非功能性需求
## 多设备适配声明
## 全局特性影响
## 行为场景（可选，Gherkin）
## Spec 自审清单
## context-references
```

## Per-chapter content notes

### 概述
Table form with these fields: 特性名称, 特性编号, 所属 Epic, 优先级, 目标版本, SIG 归属, 状态, 复杂度.

### 本次变更范围（Delta）
> 存量特性（lineage: new-on-legacy / bugfix-on-feature）填写本节。全新特性（lineage: new）可跳过。

Table columns: 类型 (ADDED/MODIFIED/REMOVED) | 内容 | 说明.

### 输入文档
List the corresponding requirement doc, design doc, and source-locator file paths.

> 需求基线、不涉及项、受影响子系统与仓库详见 proposal.md，本文档不重复摘录。design.md 与本文档并行产出，互不依赖。

### 用户故事 (US)
Each US contains:
- Role / Want / Value (As a / I want / So that)
- AC table with columns: AC编号 | 验收标准 | 类型
  - 类型 values: 正常 / 异常 / 边界
  - Each AC uses WHEN/THEN format describing one verifiable behavior
- AC IDs must be referenceable from "验证映射", "规则定义", and "行为场景"

### 验收追溯
Table columns: AC | 关联规则 | 关联 Task | 验证方式 | 证据.

### 规则定义

> **统一规则表，取消 FR/BR/EX/RC 四分类。** 类型标签：**行为**（正常路径下的系统行为）、**边界**（输入/状态的临界点）、**异常**（非法输入或异常状态的处理）、**恢复**（系统异常后的恢复策略）。

Table columns: 规则ID (R-N) | 类型 (行为/边界/异常/恢复) | 触发条件 | 预期行为 | 边界/约束 | 关联AC.

**规则质量要求（每条规则必须满足）：**
1. **触发条件可复现** — 给出具体输入值或操作步骤，不允许"某些情况下"
2. **预期行为可观测** — 描述可验证的结果（UI 状态/返回值/错误码），不允许"正确处理"
3. **边界值已标注** — 数值型必须写出边界点（=0/负数/最大值/精度）
4. **关联 AC 已填写** — 不允许孤立规则
5. **无重叠冲突** — 两条规则的触发条件不能覆盖同一输入范围且预期行为矛盾

### 验证映射
Table columns: 编号 | 对应规格项 | 验证方式 | 验证重点.

### API 变更分析
> 涉及 API 变更时必填。

- `### 新增 API`: Table columns: API 名称 | 开放范围 (Public/System/InnerApi) | 入参概要 | 返回值 | 错误码范围 | 功能描述 | 关联 AC
- `### 变更/废弃 API`: Table columns: API 名称 | 变更类型 (变更/废弃) | 影响场景 | 迁移指引 | 关联 AC
- Must cross-verify against canonical SDK `.d.ts` / `.d.ets` / `.static.d.ets` files under `<OpenHarmony_root>/interface/sdk-js/api/`
- API 签名、d.ts 位置、权限要求等实现细节见 design.md

> **复杂度裁剪：** 涉及新增或变更的 InnerAPI/Public API/System API 时启用。L0 需求（单属性扩展、无新 API）可写"N/A，API 行为无变化"。

### 接口规格

> 供 code-gen 直接消费的接口行为定义。与 API 变更分析（声明层）互补，本节定义接口的调用语义、参数约束和行为场景。

**与"API 变更分析"的信息边界：**
- "API 变更分析"只回答"有哪些 API、什么级别、影响谁"（声明层，一行一个 API 的清单视图）。
- "接口规格"回答"这个 API 怎么用、参数有什么约束、什么场景返回什么"（语义层，每个 API 的详细行为视图）。
- 概要写清单，详细写行为——两者不重复填写。

Per-API block structure:

```
### 接口定义

**[接口名称]**

| 属性 | 值 |
|------|-----|
| 函数签名 | `[return_type] [class]::[method]([params])` |
| 返回值 | `[类型]` — [含义] |
| 开放范围 | Public/System/InnerApi |
| 错误码 | [错误码枚举或 N/A] |
| 关联 AC | AC-x.x |

**参数约束**

| 参数 | 类型 | 必填 | 默认值 | 约束条件 |
|------|------|------|--------|---------|
| [param] | [type] | 是/否 | [default] | [取值范围/前置条件/异常触发] |

**行为场景**

| # | 触发条件 | 预期行为 | 关联 AC |
|---|----------|----------|---------|
| 1 | [正常调用条件] | [预期返回/副作用] | AC-1.1 |
| 2 | [异常调用条件] | [错误码/降级行为] | AC-1.6 |
```

> **复杂度裁剪：** L0 需求可写"无新增接口规格"。L1+ 涉及 API 变更时必填。

### 兼容性声明
Bullet list format with these specific items:
- **已有 API 行为变更:** [是/否，说明]
- **配置文件格式变更:** [是/否]
- **数据存储格式变更:** [是/否]
- **最低支持版本:** [版本号]
- **API 版本号策略:** [@since 标注策略]

### 架构约束
Table columns: 关键约束 | 约束说明 | 影响 AC.

> 本节列出本特性 AC 验证必须满足的约束。架构规则适用性及设计方案见 design.md。

### 非功能性需求
Table columns: 类型 | 指标/阈值 | 验证方式 | 证据.
Standard rows: 性能 | 功耗 | 内存 | 安全 | 可靠性 | 可测试性 | 自动化维测 | 定界定位.

> N/A 判定见 proposal.md 不涉及项确认。本节仅为适用项填写具体指标。性能指标应为用户可感知或可度量的外部行为指标（如响应时间、帧率、功耗），而非内部实现指标（如函数执行时间、内存分配次数）。

### 多设备适配声明

> 复杂变更时展开。同一功能在不同设备类型上行为不同时必填，全部设备行为一致时填"无差异"。

Table columns: 设备类型 | 行为差异 | 规格/约束 | 验证方式 | 证据.
Standard rows: 手机 | 平板 | 折叠屏.

### 全局特性影响
Table columns: 特性 | 适用？ | 结论 | 关联场景.
Standard rows: 无障碍 | 大字体 | 深色模式 | 多窗口/分屏 | 多用户 | 版本升级 | 生态兼容.

### 行为场景（可选，Gherkin）

> **与"接口规格 → 行为场景"表的关系：** 两者信息高度重叠，按复杂度二选一，不要同时填写。
> - **L1（标准）**：使用"接口规格 → 行为场景"表即可，简洁够用。
> - **L2+（复杂/关键）**：使用本节 Gherkin 场景，表达力更强（支持 Scenario Outline 参数化、多前置条件组合）。此时"接口规格 → 行为场景"表可简化为 Gherkin 场景的索引。

Gherkin format:

```
Feature: [特性名称]
  作为 [角色]
  我想要 [功能/行为]
  以便 [价值/目的]

  Scenario: [场景名称]
    Given [前置条件]
    When [操作/触发条件]
    Then [预期结果]
    And [附加验证]

  Scenario Outline: [参数化场景]
    Given [前置条件]
    When [操作] <参数>
    Then [结果] <期望值>

    Examples:
      | 参数 | 期望值 |
      | [值1] | [结果1] |
```

### Spec 自审清单
Checkbox list:
- [ ] 无"待定""TBD""TODO"等占位符
- [ ] 所有 AC 使用 WHEN/THEN 格式，可独立测试
- [ ] 范围边界明确（做什么/不做什么清晰）
- [ ] 无语义模糊表述（"快速""稳定""尽可能"等）
- [ ] AC 与规则表交叉一致（每个 AC 至少关联一条规则，每条规则至少关联一个 AC）
- [ ] 规则表每条通过 5 项质量检查（可复现/可观测/边界值/关联AC/无冲突）

### context-references
Yaml format:
```yaml
context-queries:
  - repo: "[owner]/[repo-name]"
    query: "[需要了解的架构或实现细节]"
```

**关键文档：** [RFC/设计文档/API 参考链接]

## Writing constraints

- AC ID format: `AC-<US-number>.<index>`, e.g. `AC-1.3`
- Rule ID format: `R-<number>`, e.g. `R-1` (sequential, no FR/BR/EX/RC prefix)
- All numbers (line numbers, version numbers, API IDs) must be real — no placeholders
- All source references must trace to actual `frameworks/...` or `interfaces/...` paths and line numbers
- Use `|` for table column alignment — no HTML
- Half-width punctuation in code/identifiers; Chinese characters are fine in narrative text
