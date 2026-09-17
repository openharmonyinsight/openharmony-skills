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
    index.json              # 规则模块索引 + 报告列定义
    spelling-rules.json     # 拼写错误、鸿蒙专有名词
    syntax-rules.json       # 代码语法错误
    path-consistency-rules.json  # 文档内部路径与 Sample 一致性
    semantics-rules.json    # 示例代码语义清晰度
    project-structure.json  # 工程结构符合性
    findability-rules.json  # 信息可发现性
    completeness-rules.json # 内容完整性
    correctness-rules.json  # 版本同步、代码可执行性、JSDOC 准确性、SDK 映射规则
    clarity-rules.json      # 标题-内容匹配、链接完整性
    capability-rules.json   # 约束条件、命名、实用性、替代方案
    excel-format.md         # Excel 报告格式说明
    scoring-guide.md        # 置信度与优先级定义
    rule-extensions.md      # 规则扩展指南
    workflow-details.md     # 详细工作流 + 参考执行器实现 + 自检断言
  evals/
    evals.json              # 评测用例、植入缺陷 ground truth（file/line/probe）
    check_ground_truth.py   # 植入行号与 fixture 的一致性校验
    scripts/
      run_self_check.mjs    # 执行器自检（A1-A16），原样抽取 workflow-details.md 代码块运行
    design-quality-score.md # Skill 设计质量评分记录
    inputs/                 # 植入缺陷的评测输入（API 文档、开发指南、SDK d.ts）
    runs/                   # with/without skill 的原始运行输出
    with-skill-report.md    # with-skill 判分报告
    without-skill-report.md # baseline 判分报告
```

## 规则管理

检查规则存储在 `references/` 目录下的 JSON 文件中，由 `references/index.json` 统一索引，由 `references/workflow-details.md` 中的注册表 + 声明式驱动消费。

- 每条规则必须声明 `execution`：`automatic`（JSON 提供机器可判定的驱动配置）或 `agent`（只有语义 `checkPoints`，需回填 verdict）。
- 新增 `automatic` 规则且复用已有驱动类型时只改 JSON 即可生效；新增驱动类型或函数处理器时需在 `RULE_HANDLERS` / `FUNCTION_HANDLERS` 登记。
- 加载期强制校验覆盖度与可构造性：启用规则缺处理器、注册表存在未知 ID、必填字段缺失、正则无法构造、good/bad 样例断言失败，一律 fail-fast，不静默跳过。

## 自检

```bash
# 执行器与规则库的一致性断言 A1-A16（Node 18+，无第三方依赖）
node evals/scripts/run_self_check.mjs

# 评测 ground truth 与 fixture 的一致性（植入行号/probe）
python3 evals/check_ground_truth.py
```

`run_self_check.mjs` 原样抽取 `references/workflow-details.md` 与 `references/excel-format.md` 中的 javascript 代码块拼接执行，
再用 `references/` 下的真实规则 JSON 与 `evals/inputs/` 下的真实 fixture 断言行为（不使用合成规则/合成文档）。
断言清单见 `references/workflow-details.md` → 步骤 7；改动规则或执行器后必须两项自检都通过，再更新评测证据。
