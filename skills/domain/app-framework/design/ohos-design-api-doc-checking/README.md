# ohos-design-api-doc-checking

API 文档质量检查 Skill，覆盖 7 大质量维度（资源易找性、资源丰富性/完整性、资料正确性、资源清晰易懂、能力有效性、能力易用性、能力丰富性），并支持 SDK 源码（`.d.ts` / `.h`）一致性校验与多格式报告输出（Excel + Markdown）。

## 触发场景

- API 文档质量评估、API 评审
- 文档错误检测、拼写/语法/路径一致性检查
- 文档与 `interface_sdk-js` 仓库 `.d.ts` 定义的一致性校验

## 放置说明

本 Skill 是跨领域通用的 API 文档质量检查能力。按业务约定纳入 `domain/app-framework` 领域下沉淀，供程序框架相关 API 文档优先使用，亦可服务于其他领域的 API 文档检查。

- `metadata.scope = domain`
- `metadata.stage = design`
- `metadata.domain = api`（Skill 机器名中的 `<domain>` 字段，对应 API 文档主题域）
- 命名空间领域目录：`domain/app-framework`

## 目录结构

```text
ohos-design-api-doc-checking/
  SKILL.md
  README.md
  references/
    index.json              # 规则模块索引
    spelling-rules.json     # 拼写错误、鸿蒙专有名词
    syntax-rules.json       # 代码语法错误
    path-consistency-rules.json  # 文档内部路径与 Sample 一致性
    semantics-rules.json    # 示例代码语义清晰度
    project-structure.json  # 工程结构符合性
    findability-rules.json  # 信息可发现性
    completeness-rules.json # 内容完整性
    correctness-rules.json  # 版本同步、代码可执行性、JSDOC 准确性
    clarity-rules.json      # 标题-内容匹配、链接完整性
    capability-rules.json   # 约束条件、命名、实用性、替代方案
    excel-format.md         # Excel 报告格式说明
    scoring-guide.md        # 置信度与优先级定义
    rule-extensions.md      # 规则扩展指南
    workflow-details.md     # 详细工作流
```

## 规则管理

检查规则存储在 `references/` 目录下的 JSON 文件中，由 `references/index.json` 统一索引。新增或修改规则只需编辑对应规则文件，无需改动 `SKILL.md`。
