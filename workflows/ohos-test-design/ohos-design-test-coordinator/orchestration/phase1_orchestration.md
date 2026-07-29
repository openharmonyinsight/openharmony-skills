# 阶段1 编排：需求解析（协调器执行步骤）

> 本文件承载 Phase1 的协调器操作步骤。SKILL.md 阶段1 仅保留自检分支决策树与路由。
> **职责边界**：`orchestration/` = 协调器自己执行的步骤；`phases/` = Agent 骨架（注入 Prompt）；`rules/` = Agent 按需 Read 的规则。

## 编排器执行流程（操作步骤）

1. spawn Phase1 Agent（注入骨架文件+规则文件路径+输入输出路径+领域名称+知识库模式）
2. 等待Agent返回摘要
3. 执行需求澄清交互（详见 `rules/phase1_clarify_rules.md`）：
   - 读取待确认项表格，若>0执行答疑交互
   - AskUserQuestion最终确认"需求解析是否正确完整？"
   - 用户选择"需要优化" → spawn Agent执行增量修改

> 自检分支（Read requirement_analysis.md 自检部分的三类判定）保留在 SKILL.md 阶段1「决策树」；路由（"正确，继续" → 进入Phase2）亦在 SKILL.md。
