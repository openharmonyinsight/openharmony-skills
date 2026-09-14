# ohos-dev-lite-adaptation (router) evals

4 个评估用例，覆盖 router 的四类核心职责（源自 skills/ohos-dev-workflow-router/SKILL.md 路由规则 R1-R11 + GATE 门控体系 + DECISIONS.md 决策机制的真实设计）。

## 用例覆盖

| id | 场景 | 验证的核心能力 |
|----|------|--------------|
| `router_intent_new_project_greenfield` | 新项目起步 | 意图判定 → P1 起步 + greenfield 模式 + 前置决策采集 |
| `router_escape_hatch_p7` | 阶段中途报错 | R2 逃生舱路由（P7 不中断主线 + 回归断点） |
| `router_gate_discipline_no_advance_on_fail` | GATE 判定纪律 | 技术门控 PASS 才准进下一阶段（反短路：可行性报告缺失 = GATE-K FAIL） |
| `router_decision_a5_reading_and_translation` | 运行时决策读取 | A1-A6 决策变量读取 + 大白话转译（受众区分） |

## 评估方法

**with skill**：agent 装载 skills/ohos-dev-workflow-router/SKILL.md（+ 按需读 steps/ 与 DECISIONS.md）后执行 prompt，对照 expectations 判定。

**without skill（基线）**：同 prompt 不带 router 执行——预期基线在逃生舱纪律（可能建议重启流程）、GATE 纪律（可能放行"基本写完"）、A5 决策读取（无从知道 A5 存在）上显著弱于 with skill。
