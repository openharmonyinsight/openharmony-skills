# 阶段4 编排：测试用例细化（协调器执行步骤）

> 本文件承载 Phase4 的协调器操作步骤。SKILL.md 阶段4 仅保留对抗达标决策树与配置表。
> **职责边界**：`orchestration/` = 协调器自己执行的步骤；`phases/` = Agent 骨架；`rules/` = Agent 按需 Read 的规则。

## 编排器执行流程（操作步骤）

> 规划Agent匹配经验库 → 分批规划 → 多轮并行spawn执行Agent → 脚本合并

1. **spawn规划Agent**（经验库匹配+分批规划，详见 phases/phase4_testcase.md 第一轮）
   - 规划Agent返回摘要：分批计划（含批次总数）+ 匹配条目数（空时标注0条）

2. **解析摘要+多轮并行spawn执行Agent**（协调器执行）
   - 提取batches数组和批次总数
   - 确认knowledge_match.md已更新
   - 按规则执行多轮并行spawn（详见rules/phase4_rules.md）
   - **强制注入文件路径**：
     - requirement_analysis.md路径
     - test_point_design.md路径
     - knowledge_match.md路径
     - phase4_rules.md路径
     - phase4_testcase.md骨架文件路径
     - 输出目录路径：{output_dir}/batches_phase4/
      - 分配的测试点范围
   - **批次级文件验证**：每个Agent返回后立即Test-Path检查 `batch_{主单元编号}_{批次号}.md` 是否存在且非空；不存在/为空 → 立即重试该batch（最多2次）；所有batch文件确认存在后才进入步骤3-合并汇总

3. **合并汇总**：调用脚本merge_batch_mds，输出test_cases.md

4. **对抗评估脚本调用**：调用phase4_adversary.py生成基础数据

5. **spawn对抗评估Agent**（详见 phases/phase4_testcase_adv.md）
   - 达标→自动进入Phase5，不达标→用户确认后循环补充

> 对抗达标决策（达标/不达标分支）保留在 SKILL.md 阶段4「决策树」。
