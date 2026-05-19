# Feat-XX-spec.md Chapter Skeleton

Use this H1/H2/H3 structure to generate the spec file. Reference implementation: `specs/04-common-capability/03-common-attributes/01-layout-attributes/Feat-01-size-properties-spec.md`. Chapter titles below are written in Chinese because that's the actual format used in generated spec files — keep them verbatim.

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
## 业务规则
## 功能规则
## 异常/豁免规则
## 恢复契约
## 验证映射
## API 变更分析
### 新增 API
### 变更/废弃 API
## 兼容性声明
## 架构约束
## 非功能性需求
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
- AC-X.Y list (acceptance criteria — each describes one verifiable behavior)
- AC IDs must be referenceable from "验证映射" and "行为场景"

### 验收追溯
Table columns: AC ID | 关联规则 | 关联 Task | 验证方式 | 证据.

### 业务规则 / 功能规则 / 异常规则 / 恢复契约
- 业务规则: BR-N — domain semantic constraints
- 功能规则: FR-N — concrete behaviors
- 异常/豁免规则: EX-N — error / boundary conditions
- 恢复契约: RC-N — error-recovery paths

### 验证映射
Table columns: 编号 | 对应规格项 | 验证方式 | 验证重点.

### API 变更分析
- `### 新增 API`: Table columns: API 名称 | 类型 (Public/System/Internal) | 功能描述 | 关联 AC
- `### 变更/废弃 API`: Table columns: API 名称 | 变更类型 (变更/废弃) | 关联 AC
- Must cross-verify against canonical SDK `.d.ts` / `.d.ets` / `.static.d.ets` files under `<OpenHarmony_root>/interface/sdk-js/api/`
- API 签名、d.ts 位置、权限要求等实现细节见 design.md

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
Standard rows: 性能 | 内存 | 安全 | 可靠性 | 问题定位.

> N/A 判定见 proposal.md 不涉及项确认。本节仅为适用项填写具体指标。

### 全局特性影响
Table columns: 特性 | 适用？ | 结论 | 关联场景.
Standard rows: 无障碍 | 大字体 | 深色模式 | 多窗口/分屏 | 多用户 | 版本升级 | 生态兼容.

### 行为场景（可选，Gherkin）
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

Every AC corresponds to at least one scenario.

### Spec 自审清单
Checkbox list:
- [ ] 无"待定""TBD""TODO"等占位符
- [ ] 所有 AC 使用 WHEN/THEN 格式，可独立测试
- [ ] 范围边界明确（做什么/不做什么清晰）
- [ ] 无语义模糊表述（"快速""稳定""尽可能"等）
- [ ] AC 与业务规则/异常规则/恢复契约交叉一致

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
- All numbers (line numbers, version numbers, API IDs) must be real — no placeholders
- All source references must trace to actual `frameworks/...` or `interfaces/...` paths and line numbers
- Use `|` for table column alignment — no HTML
- Half-width punctuation in code/identifiers; Chinese characters are fine in narrative text
