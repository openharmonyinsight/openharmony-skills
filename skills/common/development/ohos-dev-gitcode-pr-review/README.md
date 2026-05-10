# ohos-dev-gitcode-pr-review

GitCode PR 评审技能，用于从 PR 编号或 URL 出发，结合 `oh-gc` 获取的 PR 元数据、diff、评论和本地仓库代码上下文，产出具体评审发现或 GitCode 评论提交草稿。

## 放置说明

该技能属于跨子系统复用的开发阶段 PR 评审流程能力，放置在：

```text
skills/common/development/ohos-dev-gitcode-pr-review/
```

命名字段对应关系：

| 字段 | 值 |
| --- | --- |
| scope | common |
| stage | development |
| domain | gitcode |
| capability | pr-review |

## 文件说明

| 文件 | 说明 |
| --- | --- |
| `SKILL.md` | Agent 执行 GitCode PR 深度评审与提交草稿准备时使用的主流程 |
| `agents/openai.yaml` | 面向 OpenAI Agents 展示的 Skill 元数据 |
| `references/` | 深度评审清单、问题记录 schema、无发现输出模板、提交草稿 schema 和评审分级标准 |
| `scripts/` | PR 引用规范化、PR 上下文采集和提交草稿预览/执行脚本 |
| `tests/` | `prepare_review_submission.py` 的轻量回归测试 |
| `README.md` | 面向维护者的放置、命名和文件说明 |
