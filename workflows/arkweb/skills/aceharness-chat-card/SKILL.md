---
name: aceharness-chat-card
description: 通用可视化卡片渲染技能。
descriptionZH: 可视化卡片渲染。【触发场景】用卡片显示、做个卡片展示、生成可视化卡片/PR 卡片/Issue 卡片/card/tabs/badge/徽章/进度条/header/info 行。【注意】无需说 AceHarness，看到卡片需求即触发。输出 kind=card 的 JSON。
tags:
  - 卡片
  - UI
  - 对话
  - 可视化
---

# Aceharness Chat Card

通用可视化卡片渲染技能。只要用户要“展示型卡片”，就用它。

## 触发场景

- 用卡片显示、做个卡片展示、生成可视化卡片
- PR/Issue/Agent/工作流状态摘要卡片
- 需要 badges、tabs、折叠区、进度条、结构化信息块

## 最高优先级规则

### 1. 结构化结果统一走 `<result>`

所有结构化结果都放在 `<result>...</result>` 内，且其中只能有一个 JSON 对象。

- 卡片: `{"kind":"card","payload":{...}}`
- 机器协议结果: `{"kind":"home_sidebar","payload":{...}}`、`{"kind":"clarification_form","payload":{...}}` 等
- 不要再用 fenced code block 包裹 `<result>` 内容
- `<result>` 外的普通文字与 `<result>` 内的 JSON 要分开

正确示例：

```text
这是分析结果：

<result>
{"kind":"card","payload":{"header":{"title":"示例"},"blocks":[{"type":"text","content":"详情"}]}}
</result>
```

错误示例：

```text
<result>
[任何 fenced code block]
</result>
```

### 2. card 只负责展示

以下场景不要输出 card：

- `home_sidebar`
- `clarification_form`
- `plan_draft`
- `workflow_draft`

这些都应该输出对应 `kind` 的机器可读 JSON。

### 3. 输出前必须验证 card payload

`payload` 本体必须先通过校验脚本：

```bash
echo '{"header":{"title":"示例"},"blocks":[{"type":"text","content":"详情"}]}' | node /absolute/path/to/skills/aceharness-chat-card/scripts/validate-card.mjs
```

要求：零错误，零告警。

## Card Schema

```typescript
interface CardSchema {
  header?: {
    icon?: string;
    title: string;
    subtitle?: string;
    gradient?: string;
    badges?: { text: string; color?: string }[];
  };
  blocks: Block[];
  actions?: { label: string; prompt: string; icon?: string }[];
}

type Block =
  | { type: 'info'; rows: { label: string; value: string; icon?: string }[] }
  | { type: 'badges'; items: { text: string; color?: string }[] }
  | { type: 'text'; content: string; maxLines?: number }
  | { type: 'code'; code: string; lang?: string; copyable?: boolean }
  | { type: 'progress'; value: number; max?: number; label?: string }
  | { type: 'steps'; current: number; total: number }
  | { type: 'tabs'; tabs: { key: string; label: string; blocks: Block[] }[] }
  | { type: 'collapse'; title: string; icon?: string; subtitle?: string; blocks: Block[]; defaultOpen?: boolean }
  | { type: 'list'; items: { icon?: string; color?: string; text: string }[] }
  | { type: 'status'; state: string; color?: string; animated?: boolean; rows?: { label: string; value: string }[] }
  | { type: 'actions'; items: { label: string; prompt: string; icon?: string }[] }
  | { type: 'divider' };
```

## 常见错误

- `blocks: []`
- 把 `payload` 直接输出成裸 card 对象，没有 `kind`
- 在 `<result>` 里塞 fenced code block
- card 和普通文字混在同一个 `<result>` 里
- 图标名乱写

## 示例

### PR 分析卡片

```text
<result>
{"kind":"card","payload":{"header":{"icon":"merge_type","title":"fix: 修复内存泄漏","subtitle":"repo#1224","badges":[{"text":"open","color":"green"},{"text":"bug-fix","color":"orange"}]},"blocks":[{"type":"info","rows":[{"label":"作者","value":"zhangsan"},{"label":"目标分支","value":"main"}]},{"type":"text","content":"修复了编译器在处理大型 AST 时的内存泄漏问题。","maxLines":3}]}}
</result>
```

### 工作流状态卡片

```text
<result>
{"kind":"card","payload":{"header":{"icon":"play_arrow","title":"AST 内存优化"},"blocks":[{"type":"status","state":"运行中","color":"green","animated":true,"rows":[{"label":"当前阶段","value":"测试阶段"},{"label":"当前步骤","value":"tester"}]},{"type":"progress","value":7,"max":12,"label":"7/12 步骤完成"}]}}
</result>
```
