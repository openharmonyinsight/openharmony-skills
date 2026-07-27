# ODK Profile System

> 借鉴 GitHub Spec Kit presets 机制，为 OpenHarmony 复杂大仓提供差异化定制。大部分模块直接使用 `base` 默认模板。

## 设计原则

- **只为大仓定制** — 仅 arkui/arkgraphic/arkweb/arkruntime 四个高频大仓有专属 profile，其余走 base 默认
- **增量差异** — 子 profile 只声明与 base 不同的部分（required_dimensions / additional_sections / agent_instructions）
- **阶段约束** — `agent_instructions` 按 define/specify/design/plan 分阶段注入；无对应阶段时不要隐式复用其他阶段指令
- **AI 驱动** — 通过模块关键词自动检测，无需 CLI；`.codespec/profile.yaml` 可显式声明
- **按需加载** — 非 ODK 会话不加载任何 profile；匹配时才读取对应 YAML

## 可用 Profile

| Profile ID | 适用模块 | Priority | 核心关注 |
|-----------|---------|----------|---------|
| `arkweb` | ArkWeb / Chromium 内核 | 15 | security, compatibility, perf, build |
| `arkruntime` | ArkRuntime / ets_runtime / arkcompiler | 15 | perf, compatibility, api-sdk |
| `arkui` | ArkUI / UI 组件 | 20 | api-sdk, compatibility, perf, i18n |
| `arkgraphic` | ArkGraphic / render_service | 25 | perf, compatibility, api-sdk |

## 激活方式

**显式声明**（`.codespec/profile.yaml`）：

```yaml
profiles:
  - "arkui"
```

**自动检测**（AI 根据关键词匹配）：

- `arkui`、`component`、`layout` → `arkui`
- `graphic`、`render`、`gpu` → `arkgraphic`
- `web`、`chromium`、`v8` → `arkweb`
- `runtime`、`compiler`、`gc` → `arkruntime`

## 目录结构

```
core/profiles/
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
