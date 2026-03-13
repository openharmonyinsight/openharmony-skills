# Task 状态定义

tasks.md 中每个 Task 的 `Status` 和 `Reason` 字段，三方（Planner / Worker / Reviewer）共用：

| Status | 含义 | 恢复动作 |
|--------|------|----------|
| `pending` | 等待派发 | Planner 派发 Worker |
| `in_progress` | Worker 正在执行 | 重新派发 Worker（上次可能中断） |
| `blocked` | Worker 遇到无法解决的问题 | Planner 读 Reason，解决后重新派发 |
| `in_review` | Worker 完成，等待/正在 Review | Planner 派发 Reviewer |
| `rework` | Review 未通过（<95 分） | Planner 附修复建议，重新派发 Worker |
| `building` | 编译验证中 | 重新执行编译 |
| `build_failed` | 编译失败 | Planner 附错误信息，重新派发 Worker |
| `completed` | Review 通过（≥95 分），等待编译验证 | Planner 执行编译 |
| `done` | Review 通过 + 编译通过，全部完成 | 跳过，处理下一个 Task |

说明：
- 编译验证阶段**不创建新 Task**；继续复用当前 Task 的 `Status` / `Reason`
- 如果仓库不是 `ets_runtime` 或编译命令未知，直接把当前 Task 从 `completed` 改为 `blocked`
