# Token Economy Rules

ODK 桥接 subagent、跨阶段传证据、扇出检索时遵守的上下文经济性约束，避免上下文膨胀与无效 fork。

适用范围：spawn 子 Agent、跨阶段/跨产物传证据、并行检索扇出的所有场景。

> 本文件为仓库内参考规范（`core/rules/` 不随插件分发）。运行时生效副本在 `using-odk` 的 Context Loading（随插件分发、运行时加载）；运行时 skill 不直接引用本文件。

## 约束

R-TE-001: 隔离上下文 spawn —— 子 Agent 在独立上下文运行，不 fork 主会话历史；主会话只发任务、收摘要。
R-TE-002: 证据传路径不传内容 —— 证据落盘一次（`evidence/`、`pr-diff.txt`、`findings.json` 等），后续只传文件路径，不把全文塞回上下文。
R-TE-003: 摘要回传 ≤15 行 —— 跨阶段/子 Agent 回传主会话只给路径 + 关键发现 + 必改项计数，不超过 15 行（沿用 `using-odk` Context Loading 既有"summaries ≤15 lines"约束，此处明确覆盖子 Agent 回传场景）。
R-TE-004: 扇出上限 ≤4 —— 同一层级并行子 Agent 不超过 4 个；超出则分批或收敛任务粒度。

## 通过条件

- 主会话不持有子 Agent 的完整上下文副本
- 证据以路径引用，无大段重复粘贴
- 回传摘要精简且可定位（含路径/行号）
- 并行扇出受控（同层 ≤4）
