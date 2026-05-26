# ohos-design-agent-instruction-quality-review

AGENTS.md / CLAUDE.md / agent instruction 文件质量评审技能，用于检查 coding agent 指令是否具备可执行的代码地图、知识路由、约束边界和验证闭环。

## 放置说明

该技能属于跨领域通用的 agent 指令质量评审能力，放置在：

```text
skills/common/design/ohos-design-agent-instruction-quality-review/
```

命名字段对应关系：

| 字段 | 值 |
| --- | --- |
| scope | common |
| stage | design |
| domain | agent |
| capability | instruction-quality-review |

## 文件说明

| 文件 | 说明 |
| --- | --- |
| `SKILL.md` | Agent 触发并执行 AGENTS.md / CLAUDE.md 质量评审时使用的主技能文件 |
| `README.md` | 面向维护者的入库位置、命名字段和文件说明 |
