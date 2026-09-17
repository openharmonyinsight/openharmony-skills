---
name: ohos-design-api-doc-checking
description: Comprehensive API documentation quality checker supporting 7 quality dimensions, SDK source consistency validation, and multi-format reporting. Use for API review, documentation quality assessment, error detection, and consistency checks.
metadata:
  author: openharmony
  scope: domain
  stage: design
  domain: api
  capability: doc-checking
  version: "0.1.0"
  status: draft
  tags:
    - api-doc
    - documentation-quality
    - sdk-consistency
---

# 快速开始

检查API文档质量的基本步骤：

1. **判断文档类型** - 确定是API文档还是开发指南
2. **加载规则** - 从 `references/index.json` 加载规则模块
3. **解析文档** - 提取文档结构信息（代码块、表格、链接、标题、方法签名等）
4. **执行检查** - 根据文档类型执行相应的检查项
5. **生成报告** - 生成Excel报告和可选的Markdown汇总

详细实现见：[references/workflow-details.md](references/workflow-details.md)

# 文档类型判断

## API文档特征
- 文件名匹配模式：`js-apis-*.md`、`js-apis-app-ability-*.md`、`js-apis-inner-*.md`、`capi-*.md`
- 包含API方法签名、接口定义、参数说明
- 示例：`js-apis-geolocation.md`、`js-apis-app-ability-wantAgent.md`

## 开发指南特征
- 文件名包含：`guide`、`tutorial`、`overview`、`getting-started`等关键词
- 主要包含概念说明、使用场景、最佳实践
- 示例：`application-dev-guide.md`、`getting-started.md`

# 检查查项选择

## API文档（全部必选）
- 所有10个规则模块全部执行
- 包括SDK源码一致性检查（如果SDK可用）

## 开发指南（选择性执行）
- **必选模块**：spelling、syntax、path-consistency、clarity、semantics、project-structure、findability、correctness
- **可选模块**：completeness、capability
- **不执行**：SDK源码一致性检查（不适用）

## 执行必须留痕（fail-closed）

"全部执行"必须由**执行台账**证明，不能只在结论里声明：

- 每条 `enabled: true` 的规则都要有一条台账记录，状态为 `executed` / `not-applicable` / `not-executed` / `failed`；
- `not-executed` 与 `failed` 必须带原因，并在报告中显式呈现（缺外部 Sample 数据、缺 SDK 路径、提取为空等）；
- **未执行不等于 0 问题**：SDK 一致性检查在文档 API 提取为空、SDK 文件缺失时必须记为 `failed`，不得输出"无问题"；
- `execution: agent` 的规则（如 `clarity-001` 标题与内容不符）必须由检视者逐条 checkPoint 回填 verdict，未回填即判失败。

台账结构、断言与实现见 [references/workflow-details.md](references/workflow-details.md) 步骤 3 与步骤 7。

# 核心功能

## 7大质量维度检查

通过加载 `references/` 目录下的规则文件，按以下维度执行检查：

| 维度 | 规则文件 | 核心关注点 | 细分问题 |
|------|---------|-----------|---------|
| **资源易找性** | `findability-rules.json` | 信息可发现性 | 描述关键字不准确；官网资料缺失，分散在其他渠道 |
| **资源丰富性/完整性** | `completeness-rules.json` | 内容完整性 | 示例代码/解决方案缺失；关键说明缺失；规格约束说明缺失；默认效果说明缺失；关联信息说明缺失 |
| **资料正确性** | `correctness-rules.json` | 内容准确性 | 变更未及时更新；示例代码不完整/不可用；JSDOC描述错误 |
| **资源清晰易懂** | `clarity-rules.json` | 表达清晰度 | 标题与内容不符；功能描述不准确；关联文档链接缺失；机制原理说明缺失 |
| **能力有效性** | `capability-rules.json` | API有效性 | 约束条件缺失；系统bug；资料过时未更新 |
| **能力易用性** | `capability-rules.json` | API易用性 | 命名存在歧义；示例代码不实用 |
| **能力丰富性** | `capability-rules.json` | API丰富度 | 替代方案缺失；系统能力缺失；稳定性定位手段缺失 |

## 规则模块

本 Skill 通过加载 `references/index.json` 中定义的规则模块执行检查：

| 规则模块 | 规则文件 | 所属维度 | 检查内容 |
|---------|---------|---------|---------|
| `spelling` | `spelling-rules.json` | 资料正确性 | 拼写错误、鸿蒙专有名词校验 |
| `syntax` | `syntax-rules.json` | 资料正确性 | 代码语法错误（模板字符串空格、括号匹配等） |
| `path-consistency` | `path-consistency-rules.json` | 资料正确性 | 文档内部路径一致性、与Sample代码一致性 |
| `semantics` | `semantics-rules.json` | 能力易用性 | 示例代码语义清晰度（bundleName占位符等） |
| `project-structure` | `project-structure.json` | 资料正确性 | 与官方工程结构规范的符合性 |
| `findability` | `findability-rules.json` | 资源易找性 | 关键词准确性、外部引用完整性、文档可发现性 |
| `completeness` | `completeness-rules.json` | 资源丰富性/完整性 | 示例完整性、关键说明、约束条件、默认行为、关联信息 |
| `correctness` | `correctness-rules.json` | 资料正确性 | 版本同步、代码可执行性、JSDOC准确性、路径一致性 |
| `clarity` | `clarity-rules.json` | 资源清晰易懂 | 标题-内容匹配、描述准确性、链接完整性、机制说明 |
| `capability` | `capability-rules.json` | 能力有效性/易用性/丰富性 | 约束条件、已知问题、命名规范、实用性、替代方案 |

> **规则管理说明**：本 SKILL 的检查规则存储在 `references/` 目录下的 JSON 文件中，由执行器的**注册表 + 声明式驱动**消费。
>
> - 规则必须声明 `execution`：`automatic`（JSON 提供 `pattern`/`patterns`/`keywords`/`requiredSections`/`indicators`/`extraction`/`validation` 等机器可判定配置）或 `agent`（只有 `checkPoints` 语义描述，需人工/Agent 判定并回填 verdict）。
> - 新增 `automatic` 规则且复用已有驱动类型时，**只改 JSON 即生效**；新增驱动类型或函数处理器时，需同时在 `references/workflow-details.md` 的 `RULE_HANDLERS` 登记。
> - 加载期强制校验：启用规则缺处理器、注册表存在未知 ID、`execution` 缺失、必填字段缺失、正则无法构造、good/bad 样例断言失败，一律 fail-fast，**不允许静默跳过**。

# 报告格式

## Excel 表格输出

检查结果输出为 **Excel 表格文件（.xlsx）**，包含以下列：

| 列名 | 说明 |
|------|------|
| **文件名** | 被检查文件的路径（相对项目根目录，见 `references/excel-format.md` 数据格式规范） |
| **Designer** | 被检查文件的设计人，取文档中的 `<!--Designer: xxx-->` 注释；未标注时填 `-` |
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

## 置信度与优先级说明

置信度和优先级的定义和处理建议见：[references/scoring-guide.md](references/scoring-guide.md)

# SDK 源码一致性检查（仅API文档）

## 功能说明

SDK 源码一致性检查是 correctness 维度的核心功能，用于确保文档与 interface_sdk-js 仓库中的 .d.ts 定义文件保持一致。

## 文件映射规则

文档文件与 SDK 文件的映射由 `references/correctness-rules.json → sdkSourceCheck.mappingRules` 声明，**按数组顺序匹配，更具体的规则必须排在更宽泛的规则之前**（否则 `-sys` 会被并入 `{name}`）：

| 顺序 | 文档文件模式 | 名称转换 | SDK 文件路径 | 示例 |
|-----|-------------|---------|-------------|------|
| 0 | `options.sdkFilePath` 显式指定 | — | 直接使用 | 调用方指定 `api/@ohos.demo.taskmanager.d.ts` |
| 0.5 | `explicitMapping` 中登记的文件名 | — | 表中声明的路径 | `js-apis-demo-taskmanager.md` |
| 1 | `js-apis-inner-{module}-{name}-sys.md` | — | `api/{module}/{name}.d.ts` | `js-apis-inner-wantAgent-wantAgentInfo-sys.md` → `api/wantAgent/wantAgentInfo.d.ts` |
| 2 | `js-apis-inner-{module}-{name}.md` | — | `api/{module}/{name}.d.ts` | `js-apis-inner-wantAgent-wantAgentInfo.md` → `api/wantAgent/wantAgentInfo.d.ts` |
| 3 | `js-apis-app-ability-{name}.md` | `hyphen-to-dot` | `api/@ohos.app.ability.{name}.d.ts` | `js-apis-app-ability-wantAgent.md` → `api/@ohos.app.ability.wantAgent.d.ts` |
| 4 | `js-apis-{name}.md` | `hyphen-to-dot` | `api/@ohos.{name}.d.ts` | `js-apis-geolocation.md` → `api/@ohos.geolocation.d.ts`；`js-apis-demo-taskmanager.md` → `api/@ohos.demo.taskmanager.d.ts` |
| 5 | `capi-{name}.md` | `hyphen-to-underscore` | `api/{name}.h` | `capi-native-bundle.md` → `api/native_bundle.h` |

约束：

- `docPattern` 必须锚定整个文件名（`^…$`），`{module}` 使用惰性匹配，避免贪婪吞掉 `{name}` 的分隔符；
- 名称转换只能通过 `transforms` 按占位符声明，**禁止**对文件名整体做连字符替换；
- 无法由模式推导的特殊命名登记到 `explicitMapping`，或由调用方用 `options.sdkFilePath` 指定；
- `mappingRules.assertions` 中的样例在检查开始前必须全部通过（含目标文件存在性），映射失败返回 `reason` 并把该检查记为 `failed`，不得当成"无可比对内容，0 问题"。

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

SDK 源码路径按以下优先级解析：

1. 调用参数 `options.sdkFilePath`（直接指定 `.d.ts` / `.h`，跳过模式匹配）
2. 调用参数 `options.sdkSourcePath`（SDK 仓库根目录，配合映射规则解析）
3. 环境变量 `INTERFACE_SDK_JS_PATH` 指定的本地路径
4. 通过 `git clone` 临时克隆的仓库（自动清理）

**配置环境变量（推荐）**：
```bash
export INTERFACE_SDK_JS_PATH=/path/to/interface_sdk-js
```

**未提供 SDK 路径时**：SDK 一致性检查记为 `not-executed` 并在报告中说明原因，其余规则照常执行；
**提供了路径但映射失败/文件缺失/文档 API 提取为空**时记为 `failed`。两种状态都不得输出"SDK 一致性无问题"。

# 规则扩展

## 新增规则

1. 确定规则所属维度（见上表）与执行方式（`automatic` / `agent`）
2. 在对应规则文件中添加规则配置，必填字段齐全（含 `execution`、`message`、`suggestedFix`）
3. `automatic` 规则复用已有驱动类型时只改 JSON 即生效；引入新驱动或函数处理器时，在 `references/workflow-details.md` 的 `RULE_HANDLERS` 登记
4. 带 `pattern`/`examples` 的规则必须提供 good/bad 样例，加载期会做正反例断言
5. 运行 `references/workflow-details.md` 步骤 7 的自检断言，确认覆盖校验与规则自检通过

## 规则配置模板

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
  "checkPoints": [...],
  "message": "错误消息模板",
  "explanation": "详细说明（可选）",
  "suggestedFix": "修复建议"
}
```

详细扩展指南和示例见：[references/rule-extensions.md](references/rule-extensions.md)

# 自检

改动规则文件、执行器或评测 fixture 后，必须跑通以下两项再更新评测证据：

| 自检 | 命令 | 校验内容 |
|------|------|---------|
| 执行器与规则库一致性 | `node evals/scripts/run_self_check.mjs` | 断言 A1-A16（清单见 `references/workflow-details.md` 步骤 7）：正则可构造与正反例、注册表全覆盖、SDK 映射断言（含清空 `explicitMapping` 的独立校验）、错误码解析、示例完整性判定、报告字段契约、执行台账完整性 |
| 评测 ground truth 一致性 | `python3 evals/check_ground_truth.py` | 每条植入缺陷的 `line` 上确实存在 `probe` 字符串；expectations 中的行号落在植入行号 ±3 行内 |

两项自检都以退出码表示结果（0 通过 / 1 失败），且都用**真实规则 JSON + 真实 fixture**，不使用合成数据。
