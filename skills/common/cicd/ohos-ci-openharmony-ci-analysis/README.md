# ohos-ci-openharmony-ci-analysis

OpenHarmony CI 通用技能，用于根据 GitCode PR、`openharmony_ci` 评论、DCP event id、构建标签、产物链接或 CI 日志 URL 分析 OpenHarmony PR 门禁状态和失败日志。

## 放置说明

该技能属于跨领域通用的 OpenHarmony CI/CD 门禁分析能力，放置在：

```text
skills/common/cicd/ohos-ci-openharmony-ci-analysis/
```

命名字段对应关系：

| 字段 | 值 |
| --- | --- |
| scope | common |
| stage | cicd |
| domain | openharmony |
| capability | ci-analysis |

## 文件说明

| 文件 | 说明 |
| --- | --- |
| `SKILL.md` | Agent 调查 OpenHarmony PR CI 状态和失败日志时使用的主技能文件 |
| `agents/openai.yaml` | OpenAI 入口展示信息与默认提示 |
| `scripts/openharmony_ci.py` | 查询 DCP event、汇总 job 状态并按需抓取失败日志的辅助脚本 |
