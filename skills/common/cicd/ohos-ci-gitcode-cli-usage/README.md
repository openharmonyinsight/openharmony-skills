# ohos-ci-gitcode-cli-usage

GitCode / oh-gc CLI 通用技能，用于在终端中管理 GitCode 仓库、Issue、PR、评审人、测试人、标签、Release 和仓库配置。

## 放置说明

该技能属于跨领域通用的 GitCode PR 与仓库协作能力，放置在：

```text
skills/common/cicd/ohos-ci-gitcode-cli-usage/
```

命名字段对应关系：

| 字段 | 值 |
| --- | --- |
| scope | common |
| stage | cicd |
| domain | gitcode |
| capability | cli-usage |

## 文件说明

| 文件 | 说明 |
| --- | --- |
| `SKILL.md` | Agent 触发与执行 oh-gc CLI 工作时使用的主技能文件 |
| `references/common-issue-pr-commands.md` | 常用认证、Issue、PR、评审、测试、标签、评论与合并命令 |
| `references/extended-commands.md` | 低频 Release、仓库配置、搜索、用户、分支、提交、文件等命令 |
| `references/gitcode-pr-workflow.md` | GitCode PR 自动化工作流参考 |
