# Templates

本目录存放 kit 的标准交付件模板。每个模板只提供**最小章节骨架**（章节标题），不包含长篇填写说明。

模板按使用对象分为两个子目录：

- **`ai/`** — AI 生成交付件模板，用于 AI agent 在各阶段自动产出标准文档
- **`review/`** — 人工审核用模板，用于评审阶段记录审查结论

## ai/ — AI 生成交付件

| 模板 | 用途 | 必需章节数 |
|------|------|-----------|
| `proposal.md` | 需求提案 | 8 章节 |
| `design.md` | 架构设计 | 10 必需章节 + 2 条件章节（代码事实基线 / 状态归属与不变量） |
| `spec.md` | 功能规格 | 9 章节（含验证映射；代码映射在 execution-plan） |
| `execution-plan.md` | 执行计划 | 10 章节 + per-Task 详情 + Review Gates + 代码范围映射 |
| `spec-for-validation.md` | 验证规格（旁路） | 7 章节（从 spec/design 派生，不参与主流程） |

## review/ — 人工审核

| 模板 | 用途 | 必需章节数 |
|------|------|-----------|
| `review-spec-compliance.md` | 规格符合性审查 | AC 覆盖 + 额外实现 + 偏差 + 结论 |
| `review-code-quality.md` | 代码质量审查 | Strengths + Issues + Recommendations + Assessment |
| `review-verification.md` | 最终验证 | 验证记录 + 一致性结论 |

## 定制方式

模板即普通 Markdown 文件。可通过以下方式调整：

1. **直接修改** — 编辑对应 `.md` 文件，增删改章节标题
2. **项目级覆盖** — 在业务仓 `.codespec/shared/templates/` 下放置同名文件

> `spec-for-validation.md` 是旁路模板——仅在用户显式调用 `odk-spec-for-validation` 时加载，不污染主上下文。
> 该模板位于 `ai/` 目录下，独立于主流程四件套。
> 命名为“验证规格”而非“测试规格”，以区分验证活动（what to validate）与测试设计活动（how to test）。
