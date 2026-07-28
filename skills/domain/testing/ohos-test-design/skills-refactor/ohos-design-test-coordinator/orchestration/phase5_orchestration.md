# 阶段5 编排：验证与导出（协调器执行步骤）

> 本文件承载 Phase5 的协调器操作步骤。SKILL.md 阶段5 仅保留配置表。Phase5 较简单，无并行/对抗环节。
> **职责边界**：`orchestration/` = 协调器自己执行的步骤；`phases/` = Agent 骨架；`rules/` = Agent 按需 Read 的规则。

## 编排器执行流程（操作步骤）

1. **spawn Phase5 Agent**（注入骨架文件 phases/phase5_validate.md + rules/phase5_rules.md 路径 + 输入：test_cases.md + test_point_design.md + 用例编号起始值 + 输出目录）
2. **等待Agent返回摘要**
3. **导出脚本调用**：调用 phase5_export.py --output {output_dir} 生成 test_cases.xlsx + validation_report.md
4. **空字段门控**：导出后检查空字段，若空字段占比 >20% 触发门控告警（处理策略详见 `rules/gate_rules.md`）
5. **记录T6（phase_completed_at）**，流程结束（记录 pipeline_completed_at、打印计时报告，详见 SKILL.md「完成后」）
