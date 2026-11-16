# 参考来源与 ODK 取舍

以下公开实现用于比较工作流；本 skill 按 ODK 契约独立编写，不依赖安装上游插件。
核对日期：2026-11-12。链接为可变的上游 main，ODK 的执行规则以本仓文件为准。

| 来源 | 借鉴 | ODK 的适配 |
|------|------|------------|
| [Superpowers subagent-driven-development](https://github.com/obra/superpowers/tree/main/skills/subagent-driven-development) 与 [code-reviewer](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/code-reviewer.md) | 完整 Task diff、隔离上下文、任务评审与整变更评审分离、围绕修复范围复审 | 保留 R0/R1/R2 和固定三席；自动修复/复审限三轮；不自动搁置未闭环 High |
| [Anthropic pr-review-toolkit](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pr-review-toolkit) | pr-test-analyzer 的行为/错误路径检查；type-design-analyzer 的类型不变量；silent-failure-hunter 的降级路径检查 | 映射到 scope/security，不增加席位；测试建议须有具体回归；静默失败按实际影响定级 |
| [Anthropic code-review](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/commands/code-review.md) | 对候选发现再验证，减少未经复核的问题 | 协调者或原席复核，不另派一组验证 agent，不依赖 GitHub/Claude 专用调用 |
| [Trail of Bits differential-review](https://github.com/trailofbits/skills/blob/main/plugins/differential-review/skills/differential-review/SKILL.md) | 风险优先、删除保护的历史背景、调用方影响范围、可达路径与证据 | 用于每 Task 的定向检查，不展开全仓审计，不嵌套子 agent |
| [Cloudflare security-audit](https://github.com/cloudflare/security-audit-skill/tree/main/skills/security-audit) | 候选发现与确认结论分开、主动证伪、根因去重、统一写入发现 | 沿用 Markdown 证据；协调者唯一落盘；验证状态和严重度分开，不引入完整安全审计框架 |

没有沿用上游的额外席位、宿主工具名、自动发布行为或“证据不足也算已确认”的策略。
最终门禁、风险等级与路径仍由 `contracts/skill-guides/delivery/task-review.md` 定义。
