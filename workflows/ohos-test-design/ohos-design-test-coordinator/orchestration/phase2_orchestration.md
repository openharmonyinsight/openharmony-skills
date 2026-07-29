# 阶段2 编排：测试点生成（协调器执行步骤）

> 本文件承载 Phase2 的协调器操作步骤。SKILL.md 阶段2 仅保留对抗达标决策树与配置表。
> **职责边界**：`orchestration/` = 协调器自己执行的步骤；`phases/` = Agent 骨架；`rules/` = Agent 按需 Read 的规则。

## 编排器执行流程（操作步骤）

> 规划Agent匹配经验库 → 分批规划 → 多轮并行spawn执行Agent → 脚本合并

1. **测试技术预处理**（协调器执行）
   - 调用phase2_testing_technology.py生成testing_technology.json
   - 输出供Agent生成测试点时参考

2. **spawn规划Agent**（经验库匹配+分批规划，详见 phases/phase2_testpoint.md 第一轮）
   - 规划Agent返回摘要：分批计划（含批次总数）+ 前置摘要 + 匹配条目数（空时标注0条）

3. **解析摘要+多轮并行spawn执行Agent**（协调器执行）
   - 提取batches数组和批次总数
   - 确认knowledge_match.md已更新
   - 一个测试对象主单元对应一个batch_id
   - 按规则执行多轮并行spawn（详见rules/phase2_rules.md）
   - **强制注入文件路径**：
     - requirement_analysis.md路径
     - knowledge_match.md路径
     - testing_technology.json路径
     - phase2_rules.md路径
     - phase2_testpoint.md骨架文件路径
     - 输出目录路径：{output_dir}/batches_phase2/
     - 分配的测试对象主单元ID
     - 前置摘要（仅当前主单元有前置依赖时注入）
   - **批次级文件验证**：每个Agent返回后立即Test-Path检查 `batch_{unit_id}.md` 是否存在且非空；不存在/为空 → 立即重试该batch（最多2次）；所有batch文件确认存在后才进入步骤4-合并汇总

4. **合并汇总**：调用脚本merge_batch_mds，输出test_point_design.md

5. **对抗评估脚本调用**：调用phase2_adversary.py生成基础数据（需注入knowledge_match.md路径）

6. **spawn对抗评估Agent**（详见 phases/phase2_testpoint_adv.md）
   - 达标→自动进入Phase3，不达标→用户确认后循环补充

> 对抗达标决策（达标/不达标分支）保留在 SKILL.md 阶段2「决策树」。
