# ODK Profile System

> 借鉴 GitHub Spec Kit presets 机制，为 OpenHarmony 复杂大仓提供差异化定制。大部分模块直接使用 `base` 默认模板。

## 设计原则

- **只为大仓定制** — 仅 arkui/arkgraphic/arkweb/arkruntime 四个高频大仓有专属 profile，其余走 base 默认
- **增量差异** — 子 profile 只声明与 base 不同的部分（required_dimensions / additional_sections / agent_instructions）
- **阶段约束** — `agent_instructions` 按 define/specify/design/plan 分阶段注入；无对应阶段时不要隐式复用其他阶段指令
- **AI 驱动** — 通过模块关键词自动检测，无需 CLI；`codespec/profile.yaml` 可显式声明
- **按需加载** — 非 ODK 会话不加载任何 profile；匹配时才读取对应 YAML

`required_dimensions` 表示必须逐项评估并写明依据，不表示自动判定为“是”。
实际不涉及的维度可填写有具体理由的“否”；完整的 8 维表仍须无缺行、无重复行。
`--effective-contract` 的 `dimension_policy` 明示这一语义。追加章节、AC 类别和禁止项
仍是硬约束，其中 AC 类别必须落在真正的 AC 条目标题或描述中。
带 `arkui` Profile 的可校验示例见 `examples/12345-arkui-focus/`。

## 可用 Profile

| Profile ID | 适用模块 | Priority | 核心关注 |
|-----------|---------|----------|---------|
| `arkweb` | ArkWeb / Chromium 内核 | 15 | security, compatibility, perf, build |
| `arkruntime` | ArkRuntime / ets_runtime / arkcompiler | 15 | perf, compatibility, api-sdk |
| `arkui` | ArkUI / UI 组件 | 20 | api-sdk, compatibility, perf, i18n |
| `arkgraphic` | ArkGraphic / render_service | 25 | perf, compatibility, api-sdk |

## 激活方式

**显式声明**（`codespec/profile.yaml`）：

```yaml
profiles:
  - "arkui"
design_docs_repository: "https://gitcode.com/<组织>/<design-docs仓>.git"
```

`design_docs_repository` 不是 profile ID，而是开发者维护的交付仓地址。代码开发完成、
准备向 GitCode 提交时，ODK 用它提醒 `codespec/` 文档的独立提交目标；缺失时只显示
“待开发者填写”，不得猜测或自动跨仓推送。用户明确要求提交时，
`odk-submit-design-docs` 会生成 `metadata_tracking.yaml` 并校验五件套。

实际提交时先确认目标仓：已配置地址不被默认值覆盖；未配置且业务仓 origin 为
GitCode 时，询问是否使用 `https://gitcode.com/OpenHarmonyAI/design-docs`；其他来源
要求用户提供地址后确认。`profile.yaml` 可不存在，本次确认不自动写入配置；只有用户
要求保存时才更新 `design_docs_repository`。未确认不得跨仓复制或推送。

**候选建议**（AI 根据关键词匹配；选定后记录到 `codespec/profile.yaml`，生成和校验均读取有效契约）：

- `arkui`、`component`、`layout` → `arkui`
- `graphic`、`render`、`gpu` → `arkgraphic`
- `web`、`chromium`、`v8` → `arkweb`
- `runtime`、`compiler`、`gc` → `arkruntime`

## 目录结构

```
profiles/                         # 当前资源根下；安装态为 runtime/assets/profiles/
├── README.md
├── arkui.yaml
├── arkgraphic.yaml
├── arkweb.yaml
├── arkruntime.yaml
└── fragments/
    ├── arkgraphic/
    │   └── design-prepend.md
    ├── arkweb/
    │   └── spec-append.md
    └── arkruntime/
        └── spec-append.md
```

## 组合策略

| 策略 | 行为 | 场景 |
|------|------|------|
| `prepend` | 放在模板章节**之前** | 前置设计约束 |
| `append` | 放在模板章节**之后** | 追加验证场景 |

## 上下文代价

- 每个 profile YAML：~30 行
- 每个 fragment：~7 行
- AI 每次只加载 1 个匹配的 profile（~35 行），不影响其他模块
