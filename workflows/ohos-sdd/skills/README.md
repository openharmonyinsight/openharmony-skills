# ohos-sdd skills —— 贡献规范

本目录是所有 skill 的**唯一源**（`build.sh` 自动打包到各平台，逐字相同）。

## frontmatter（机器校验，对照 Anthropic skill-creator）

- 仅允许字段：`name`、`description`（可选：`license`/`allowed-tools`/`metadata`/`compatibility`）。
- `name`：kebab-case `^[a-z0-9-]+$`，≤64 字符，不含保留词 `anthropic`/`claude`。
- `description`：非空、≤1024 字符、**不含尖括号 `<`/`>`**。
- `compatibility`（可选）：≤500 字符，声明环境依赖（如 `Requires the ohos-sdd CLI tool ...`）。

## description 写法（what + when + exclusions，对齐 Agent Skills spec）

- 描述**做什么 + 何时用**：先简述 skill 能力（what），再以 `Use when…` / `Use before…` 给出触发场景（when）。也可只写 trigger-only（`Use when…` 起头）。
- **排除条件写在 description 里**（`Do NOT use for…`），让 agent 在 metadata 层就能决定不触发，避免加载 body 后才发现不适用。对齐 Anthropic 官方 docx/xlsx 模式。
- **不要概述 skill 的流程或工作流**（否则 agent 会照着摘要走、不读 body）；what 只是一句话能力摘要，不是流程。
- 用英文（触发匹配更稳）；body 可中英混排。
- 给出具体触发场景与症状，必要时略"pushy"以防 undertrigger。
- **body 不应有 `## When to Use` 段落**——when 信息归 description 管，body 管 how（步骤、示例、边界情况）。校验器对 body 中的 `## When to Use` 发 WARN。

> 对齐 Agent Skills spec 的 "Should describe both what the skill does and when to use it"。校验器要求 description 含 `Use when` 或 `Use before`（不强制起头位置）。

## 目录结构

- 一个 skill = 一个子目录 + 一个 `SKILL.md`（唯一必需）。
- 当前 8 个 skill 均为单文件 `SKILL.md`，**未使用** `references/`/`scripts/`。

## 重引用内容的取舍（shared/ 外置，非 per-skill references/）

- skill 正文里需要引用的大体量共享内容（templates / workflow / contracts / profiles）**不**放进各 skill 的 `references/`，而是外置到运行时共享目录，由 skill 在运行时按路径读取。
- 理由：避免在 8 个 skill 间重复大体量共享内容。
- 代价：skill 不自包含、依赖运行时布局。
- 仅当某引用内容**只被单个 skill 使用**且较大时，才考虑下沉到该 skill 的 `references/`。

## skill 之间的关系

- `using-ohos-sdd` = 路由/bootstrap skill，设计为会话启动自动注入（claude/opencode 经 SessionStart/transform hook 确定；codex 经 `.codex/settings.template.json` 的 SessionStart hook，受平台版本支持度影响为 best-effort）。对齐 superpowers 的 `using-superpowers`。
- 其余 7 个为能力 skill（`ohos-{clarify,design,plan,propose,review,spec,validate}`），靠 description 触发、经 Skill 工具调用。
- skill 之间用名字互引（如 `**REQUIRED SKILL:** Invoke \`ohos-spec\``），**禁用 `@skills/` 链接**（会强加载、吃 context）。
