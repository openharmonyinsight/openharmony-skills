---
name: api-doc-checker
description: Activates when the user requests "API review", "check doc", "review", "文档检视", or needs to check API documentation for spelling errors, code syntax errors, API consistency issues, and basic formatting problems. This skill performs comprehensive API documentation quality checks including parameter type validation, error code completeness, and example code verification.

---

# 角色

鸿蒙 API 文档质量检查专家。核心任务是自动检查 API 文档内容，通过加载和执行 references 目录下的规则文件，按照**7大质量维度**精确识别并报告多维度质量问题，提供高置信度的可操作建议。

本工具支持**文档与 SDK 源码一致性检查**，能够自动：
1. 根据文档文件名找到对应的 SDK 源码文件（.d.ts）
2. 对比 JSDOC 与文档中的 API 信息（起始版本、入参、返回值、错误码等）
3. 检查接口、组件、参数等写法的准确性

> **规则管理说明**：本 SKILL 的具体检查规则存储在 `references/` 目录下的 JSON 文件中，按**7大维度分类**组织。新增或修改检查规则时，只需编辑对应的规则文件，无需修改 SKILL.md。

# 7大质量维度

| 维度 | 规则文件 | 核心关注点 | 细分问题 |
|------|---------|-----------|---------|
| **资源易找性** | `findability-rules.json` | 信息可发现性 | 描述关键字不准确；官网资料缺失，分散在其他渠道 |
| **资源丰富性/完整性** | `completeness-rules.json` | 内容完整性 | 示例代码/解决方案缺失；关键说明缺失；规格约束说明缺失；默认效果说明缺失；关联信息说明缺失 |
| **资料正确性** | `correctness-rules.json` | 内容准确性 | 变更未及时更新；示例代码不完整/不可用；JSDOC描述错误 |
| **资源清晰易懂** | `clarity-rules.json` | 表达清晰度 | 标题与内容不符；功能描述不准确；关联文档链接缺失；机制原理说明缺失 |
|**能力有效性** | `capability-rules.json` | API有效性 | 约束条件缺失；系统bug；资料过时未更新 |
| **能力易用性** | `capability-rules.json` | API易用性 | 命名存在歧义；示例代码不实用 |
| **能力丰富性** | `capability-rules.json` | API丰富度 | 替代方案缺失；系统能力缺失；稳定性定位手段缺失 |

# 检查范围

本 Skill 通过加载 `references/index.json` 中定义的10个规则模块，执行以下检查：

## 基础检查模块（V1.0）

| 规则模块 | 规则文件 | 所属维度 | 检查内容 |
|---------|---------|---------|---------|
| `spelling` | `spelling-rules.json` | 资料正确性 | 拼写错误、鸿蒙专有名词校验 |
| `syntax` | `syntax-rules.json` | 资料正确性 | 代码语法错误（模板字符串空格、括号匹配等） |
| `path-consistency` | `path-consistency-rules.json` | 资料正确性 | 文档内部路径一致性、与Sample代码一致性 |
| `semantics` | `semantics-rules.json` | 能力易用性 | 示例代码语义清晰度（bundleName占位符等） |
| `project-structure` | `project-structure.json` | 资料正确性 | 与官方工程结构规范的符合性 |

## 7大维度检查模块（V2.0 新增）

| 规则模块 | 规则文件 | 所属维度 | 检查内容 |
|---------|---------|---------|---------|
| `findability` | `findability-rules.json` | 资源易找性 | 关键词准确性、外部引用完整性、文档可发现性 |
| `completeness` | `completeness-rules.json` | 资源丰富性/完整性 | 示例完整性、关键说明、约束条件、默认行为、关联信息 |
| `correctness` | `correctness-rules.json` | 资料正确性 | 版本同步、代码可执行性、JSDOC准确性、路径一致性 |
| `clarity` | `clarity-rules.json` | 资源清晰易懂 | 标题-内容匹配、描述准确性、链接完整性、机制说明 |
| `capability` | `capability-rules.json` | 能力有效性/易用性/丰富性 | 约束条件、已知问题、命名规范、实用性、替代方案 |

# 工作流程

检查流程按以下5个步骤执行：

1. **加载规则** - 按7大维度分类加载 `references/` 目录下的规则文件
2. **解析文档** - 提取文档结构信息（代码块、表格、链接、标题、方法签名等）
3. **执行检查** - 按7大维度依次执行规则检查
4. **生成报告** - 将检查结果转换为 Excel 格式数据
5. **输出结果** - 生成 Excel 报告文件和可选的 Markdown 汇总

详细实现代码见：[references/workflow-details.md](references/workflow-details.md)

# 报告格式

## Excel 表格输出

检查结果输出为 **Excel 表格文件（.xlsx）**，包含以下列：

| 列名 | 说明 |
|------|------|
| **文件名** | 被检查的文件路径 |
| **问题类型** | 问题所属的质量维度 |
| **问题行号** | 问题所在的具体行号 |
| **问题原因** | 问题的详细描述 |
| **建议修改方案** | 具体的修复建议 |
| **问题严重级别** | 优先级分类（严重/高/中/低） |

Excel 报告支持：
- 筛选功能 - 按问题类型、严重级别等筛选
- 排序功能 - 按任意列排序
- 条件格式 - 根据严重级别显示不同颜色（红/黄/绿/蓝）

详细格式说明和使用指南见：[references/excel-format.md](references/excel-format.md)

## Markdown 汇总报告（可选）

同时生成简要的 Markdown 汇总报告，包含：
- 统计概览（文件数、问题数、严重级别分布）
- 问题分布（按维度统计）
- Excel 文件链接

# SDK 源码一致性检查

## 功能说明

SDK 源码一致性检查是 correctness 维度的核心功能，用于确保文档与 interface_sdk-js 仓库中的 .d.ts 定义文件保持一致。

## 文件映射规则

文档文件与 SDK 文件的映射遵循以下规则：

| 文档文件模式 | SDK 文件路径 | 示例 |
|-------------|-------------|------|
| `js-apis-app-ability-{name}.md` | `api/@ohos.app.ability.{name}.d.ts` | `js-apis-app-ability-wantAgent.md` → `@ohos.app.ability.wantAgent.d.ts` |
| `js-apis-{name}.md` | `api/@ohos.{name}.d.ts` | `js-apis-geolocation.md` → `@ohos.geolocation.d.ts` |
| `js-apis-inner-{module}-{name}.md` | `api/{module}/{name}.d.ts` | `js-apis-inner-wantAgent-wantAgentInfo.md` → `wantAgent/wantAgentInfo.d.ts` |
| `js-apis-inner-{module}-{name}-sys.md` | `api/{module}/{name}.d.ts` | `js-apis-inner-wantAgent-wantAgentInfo-sys.md` → `wantAgent/wantAgentInfo.d.ts` |
| `capi-{name}.md` | `api/{name}.h` | `capi-native-bundle.md` → `native_bundle.h` |

## 检查项

SDK 源码一致性检查包括以下 10 个检查点：

| 检查点 | 说明 | 优先级 |
|--------|------|--------|
| `api-since-version-match` | API 起始版本（文档<sup>X+</sup> vs SDK @since） | Critical |
| `param-count-match` | 入参数量一致性 | High |
| `param-name-match` | 入参名称拼写准确性 | High |
| `param-type-match` | 入参类型一致性 | High |
| `return-type-match` | 返回值类型一致性 | High |
| `systemapi-mark-match` | 系统接口标记一致性（-sys vs @systemapi） | High |
| `stagemodelonly-mark-match` | Stage模型约束标记一致性 | Medium |
| `error-code-match` | 错误码完整性 | Medium |
| `enum-values-complete` | 枚举值列举完整性 | Medium |
| `interface-fields-complete` | 接口字段列举完整性 | Medium |

## 使用方式

检查工具会自动尝试从以下位置加载 SDK 源码：

1. 环境变量 `INTERFACE_SDK_JS_PATH` 指定的本地路径
2. 通过 `git clone` 临时克隆的仓库（自动清理）

**配置环境变量（推荐）**：
```bash
export INTERFACE_SDK_JS_PATH=/path/to/interface_sdk-js
```

# 规则扩展

## 新增规则

1. 确定规则所属维度（见上表）
2. 在对应规则文件中添加规则配置
3. 无需修改 SKILL.md，立即生效

## 规则配置模板

```json
{
  "id": "{dimension}-XXX",
  "name": "rule-name",
  "description": "规则描述",
  "type": "{dimension}",
  "subType": "{subCategory}",
  "priority": "high|medium|low",
  "confidence": 90,
  "enabled": true,
  "checkPoints": [...],
  "message": "错误消息模板",
  "explanation": "详细说明",
  "suggestedFix": "修复建议"
}
```

详细扩展指南和示例见：[references/rule-extensions.md](references/rule-extensions.md)

# 置信度与优先级

## 置信度等级

| 置信度 | 含义 | 建议操作 |
|--------|------|----------|
| 95%+ | 确定 | 立即修复 |
| 85-94% | 高 | 大概率需要修复 |
| 70-84% | 中等 | 建议人工确认 |
| <70% | 低 | 仅供参考 |

## 优先级等级

| 优先级 | 含义 | 处理建议 |
|--------|------|----------|
| Critical | 严重 | 合并前必须修复 |
| High | 高 | 强烈建议修复 |
| Medium | 中 | 建议修复 |
| Low | 低 | 可选改进 |
