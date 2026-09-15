# 规则扩展详细指南

本文档提供详细的规则扩展指南和示例。

## 按7大维度新增规则

### 1. 确定规则所属维度

根据问题性质选择对应维度的规则文件：

| 维度 | 规则文件 | 适用场景 |
|------|---------|---------|
| **资源易找性** | `findability-rules.json` | 关键词准确性、外部引用完整性、文档可发现性 |
| **资源丰富性/完整性** | `completeness-rules.json` | 示例完整性、关键说明、约束条件、默认行为、关联信息 |
| **资料正确性** | `correctness-rules.json` | 版本同步、代码可执行性、JSDOC准确性、路径一致性 |
| **资源清晰易懂** | `clarity-rules.json` | 标题-内容匹配、描述准确性、链接完整性、机制说明 |
| **能力有效性/易用性/丰富性** | `capability-rules.json` | 约束条件、已知问题、命名规范、实用性、替代方案 |

### 2. 在对应规则文件中添加规则

#### 规则模板

```json
{
  "id": "{dimension}-XXX",
  "name": "rule-name",
  "description": "规则描述",
  "type": "{dimension}",
  "subType": "{subCategory}",
  "priority": "critical|high|medium|low",
  "confidence": 90,
  "enabled": true,
  "execution": "automatic|agent",
  "checkPoints": [
    {
      "name": "check-point-name",
      "description": "检查点描述",
      "check": "具体的检查逻辑描述"
    }
  ],
  "message": "错误消息模板",
  "explanation": "详细说明",
  "suggestedFix": "修复建议"
}
```

#### 规则字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 规则唯一标识，格式：`{dimension}-XXX` |
| `name` | string | 是 | 规则名称（英文，kebab-case） |
| `description` | string | 是 | 规则描述（中文） |
| `type` | string | 是 | 规则类型，对应维度名称 |
| `subType` | string | 否 | 子类型，用于进一步分类 |
| `priority` | string | 是 | 优先级：`critical`、`high`、`medium`、`low` |
| `confidence` | number | 是 | 置信度（0-100），表示检测结果的可靠程度 |
| `enabled` | boolean | 是 | 是否启用该规则 |
| `execution` | string | 是 | `automatic`（JSON 提供机器可判定的驱动配置）或 `agent`（只有语义 checkPoints，需回填 verdict） |
| `checkPoints` | array | 否 | 检查点列表，描述具体检查逻辑；`execution: agent` 时必填，verdict 按 checkPoint 逐条回填 |
| `message` | string | 是 | 错误消息模板 |
| `explanation` | string | 否 | 详细说明，解释为什么这是个问题 |
| `suggestedFix` | string | 是 | 修复建议，提供具体的解决方案 |
| `examples` | object | 否 | `{ "bad": [...], "good": [...] }`；带 `pattern` 的规则建议提供，加载期做正反例断言 |

> 上表中标记为「是」的字段由 `validateRuleCoverage()` 在加载期强制校验，缺失即 fail-fast。

### 3. 生效条件

新规则会被自动加载并按维度归类执行，**无需修改 SKILL.md**，但要满足下列条件之一，否则加载期校验会直接失败（不会静默跳过）：

| 情况 | 是否需要改执行器 |
|------|----------------|
| `execution: automatic`，且复用已有驱动配置（`pattern`/`patterns`/`ambiguousPatterns`/`keywords`/`requiredConstraints`/`requiredSections`/`indicators`/`extraction`/`validation`/`requiredPatterns`/`requiredPattern`/`termMappings`/`criticalExtensions`） | 否，只改 JSON |
| `execution: agent`，只提供 `checkPoints` | 否，只改 JSON；执行时由 Agent 回填 verdict |
| 需要新的驱动类型或新的 `pattern.type: function` 处理器 | 是，需在 `workflow-details.md` 的 `RULE_HANDLERS` / `FUNCTION_HANDLERS` 登记 |

加载期强制校验（见 `workflow-details.md` 步骤 1）：

1. **覆盖校验**：每条 `enabled: true` 的规则必须在 `RULE_HANDLERS` 中有处理器，且处理器声明的 `name`/`execution` 与规则 JSON 一致；注册表中不得存在规则文件里没有的 ID。
2. **字段校验**：必填字段齐全、`priority` 合法、`confidence` 在 0-100。
3. **正则自检**：所有启用正则必须能 `new RegExp` 构造；能匹配全部中性样例的"退化正则"（如把字面量 `...` 当正则）会被拒绝。
4. **正反例断言**：提供 `examples` 的规则必须满足 good 全不命中、bad 全命中。

## 规则 ID 命名规范

### 维度前缀

| 维度 | 前缀 | 示例 |
|------|------|------|
| 资源易找性 | `findability-` | `findability-001` |
| 资源丰富性/完整性 | `completeness-` | `completeness-001` |
| 资料正确性 | `correctness-` | `correctness-001` |
| 资源清晰易懂 | `clarity-` | `clarity-001` |
| 能力有效性/易用性/丰富性 | `capability-` | `capability-001` |

### 编号规则

- 使用 3 位数字编号：`001`、`002`、`003`...
- 每个维度独立编号
- 保留编号顺序，便于维护和查找

## 规则示例

### 示例 1：资源易找性规则

```json
{
  "id": "findability-004",
  "name": "keyword-in-title",
  "description": "检查文档标题是否包含核心关键词",
  "type": "findability",
  "subType": "keyword-accuracy",
  "priority": "high",
  "confidence": 85,
  "enabled": true,
  "execution": "agent",
  "checkPoints": [
    {
      "name": "title-keyword-match",
      "description": "检查标题是否包含API名称或核心功能关键词",
      "check": "提取文档标题，检查是否包含API名称或核心功能关键词"
    }
  ],
  "message": "文档标题缺少核心关键词，可能影响搜索发现性",
  "explanation": "标题是用户搜索时首先看到的内容，包含核心关键词可以提高文档的可发现性",
  "suggestedFix": "在标题中添加API名称或核心功能关键词"
}
```

### 示例 2：资源丰富性/完整性规则

```json
{
  "id": "completeness-006",
  "name": "constraint-description",
  "description": "检查是否包含约束条件说明",
  "type": "completeness",
  "subType": "constraint-missing",
  "priority": "high",
  "confidence": 90,
  "enabled": true,
  "execution": "agent",
  "checkPoints": [
    {
      "name": "constraint-section-exists",
      "description": "检查文档中是否存在约束条件说明章节",
      "check": "查找'约束'、'限制'、'注意事项'等关键词所在的章节"
    }
  ],
  "message": "文档缺少约束条件说明",
  "explanation": "约束条件是API使用的重要信息，缺少可能导致用户误用",
  "suggestedFix": "添加'约束条件'章节，说明API的使用限制和注意事项"
}
```

### 示例 3：资料正确性规则

```json
{
  "id": "correctness-006",
  "name": "example-code-executable",
  "description": "检查示例代码是否可执行",
  "type": "correctness",
  "subType": "example-code-broken",
  "priority": "critical",
  "confidence": 95,
  "enabled": true,
  "execution": "agent",
  "checkPoints": [
    {
      "name": "syntax-validation",
      "description": "验证示例代码的语法正确性",
      "check": "使用AST解析器验证代码语法"
    },
    {
      "name": "import-validation",
      "description": "验证示例代码中的import语句",
      "check": "检查import的模块是否存在"
    }
  ],
  "message": "示例代码存在语法错误，无法执行",
  "explanation": "不可执行的示例代码会误导用户，降低文档可信度",
  "suggestedFix": "修复示例代码中的语法错误，确保代码可以正常运行"
}
```

### 示例 4：资源清晰易懂规则

```json
{
  "id": "clarity-006",
  "name": "title-content-consistency",
  "description": "检查标题与内容的一致性",
  "type": "clarity",
  "subType": "title-content-mismatch",
  "priority": "medium",
  "confidence": 75,
  "enabled": true,
  "execution": "agent",
  "checkPoints": [
    {
      "name": "keyword-coverage",
      "description": "检查标题中的关键词是否在正文中出现",
      "check": "提取标题关键词，检查正文中是否包含这些关键词"
    }
  ],
  "message": "标题与内容可能不一致",
  "explanation": "标题应该准确反映文档内容，不一致会导致用户困惑",
  "suggestedFix": "确保标题内容与正文内容一致，或调整标题以准确反映内容"
}
```

### 示例 5：能力有效性/易用性/丰富性规则

```json
{
  "id": "capability-012",
  "name": "api-constraint-documentation",
  "description": "检查API约束条件是否完整记录",
  "type": "capability",
  "subType": "constraint-missing",
  "priority": "high",
  "confidence": 85,
  "enabled": true,
  "execution": "agent",
  "checkPoints": [
    {
      "name": "parameter-constraints",
      "description": "检查参数约束条件说明",
      "check": "检查每个参数是否说明了取值范围、类型等约束"
    },
    {
      "name": "system-constraints",
      "description": "检查系统级约束条件说明",
      "check": "检查是否说明了系统版本、权限等约束"
    }
  ],
  "message": "API约束条件说明不完整",
  "explanation": "完整的约束条件说明可以帮助用户正确使用API，避免运行时错误",
  "suggestedFix": "补充完整的约束条件说明，包括参数约束、系统约束等"
}
```

> **示例 2/3/5 标为 `agent` 的原因**：它们只提供 `checkPoints` 语义描述，没有机器可判定的驱动配置。
> 若给示例 2 补上 `keywords`（如 `{"constraint": ["约束", "限制", "注意事项"]}`）、给示例 3 补上 `syntaxChecks`/`pattern`，
> 就可以改标 `execution: "automatic"` 交给执行器自动判定，此时 `RULE_HANDLERS` 中对应的驱动也要能消费这些配置。

## 置信度与优先级说明

### 置信度等级

| 置信度 | 含义 | 建议操作 |
|--------|------|----------|
| 95%+ | 确定 - 已验证，无疑问 | 立即修复 |
| 85-94% | 高 - 证据充分，误报可能性低 | 大概率需要修复 |
| 70-84% | 中等 - 可能需要人工确认 | 建议人工确认 |
| <70% | 低 - 仅供参考 | 视上下文决定 |

### 优先级等级

| 优先级 | 含义 | 处理建议 |
|--------|------|----------|
| Critical | 严重 - 会导致功能异常 | 合并前必须修复 |
| High | 高 - 严重影响体验 | 强烈建议修复 |
| Medium | 中 - 一般问题 | 建议修复 |
| Low | 低 - 轻微问题 | 可选改进 |

## 规则测试

### 测试新规则

1. 在 `references/` 目录下创建测试文档
2. 包含预期触发规则的内容
3. 运行检查工具
4. 验证规则是否正确触发
5. 检查报告中的问题描述和建议是否准确

### 调试规则

如果规则没有按预期工作：

1. 检查 `enabled` 字段是否为 `true`
2. 检查规则文件是否在 `index.json` 中正确配置，且 `category` 能在 `DIMENSION_BY_CATEGORY` 中映射到维度
3. 检查规则 ID 是否符合命名规范，并已在 `RULE_HANDLERS` 中登记
4. 检查 `execution` 是否与规则实际配置匹配（声明 `automatic` 却只有 `checkPoints`，执行时会因缺少驱动配置而不适用）
5. 查看执行台账：状态为 `not-executed`/`failed` 的记录会给出原因
6. 跑一遍 `workflow-details.md` 步骤 7 的自检断言，用真实规则 JSON + fixture 复现，而不是用合成数据

## 规则维护

### 定期审查

- 每季度审查规则的 `confidence` 和 `priority`
- 根据误报率调整置信度
- 根据实际影响调整优先级
- 禁用不再适用的规则

### 版本管理

- 在规则文件中添加版本信息
- 记录规则的变更历史
- 重大变更时更新 `index.json` 中的版本号
