## 富文本卡片渲染（aceharness-chat-card 技能）

**⚠️ 触发关键词：**
做个卡片 | card | badges | 徽章 | 进度条 | tabs | 折叠 | 可视化

---

## 适用范围（重要）

本 skill 仅适用于**展示型可视化卡片**（PR 分析、统计面板、状态展示等）。

**以下场景不属于本 skill，不要使用 card 类型结果：**
- `clarification_form`（补充问答表单）→ 用 `<result>` 内裸 JSON 输出
- `home_sidebar`（侧边栏驱动）→ 用 `<result>` 内裸 JSON 输出
- `plan_draft`（正式计划）→ 用 `<result>` 内裸 JSON 输出
- `workflow_draft`（YAML 草案）→ 用 `<result>` 内裸 JSON 输出
- 普通文字回答 → 直接输出文字，不需要卡片

**判断标准：** 只有当最终产物是"给用户看的可视化信息展示"时才用 `kind=card`。系统协议要求的机器可读结果（如表单、侧边栏指令）必须输出对应的 `kind` 裸 JSON。

---

## 核心规则

### 规则 1：card 必须在 `<result>` 内

card 结果必须放在 `<result>...</result>` 内部，且与普通文字独立输出。

### 规则 2：生成前必须验证

```bash
echo '你的JSON' | node ${Skills运行目录}/aceharness-chat-card/scripts/validate-card.mjs
```

注意：`${Skills运行目录}` 请替换为系统提示词"环境信息"中给出的实际 Skills 运行目录路径。

所有告警和报错都必须修正。验证通过标准：零错误 + 零告警。

### 规则 3：card 与 action 完全独立

- `{"kind":"card","payload":...}` → 可视化卡片，展示信息
- ```action → 操作指令，触发系统行为

---

## JSON Schema

```typescript
interface CardSchema {
  header?: {
    icon?: string;        // material-symbols-outlined 图标名
    title: string;       // 必填
    subtitle?: string;
    gradient?: string;    // tailwind 渐变
    badges?: { text: string; color?: string }[];  // 注意：badges 复数
  };
  blocks: Block[];       // 禁止为空数组
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
  | { type: 'divider' }
```

---

## 常见字段错误速查

| 错误写法 | 正确写法 |
|----------|----------|
| `header.badge` | `header.badges: [{text, color}]` |
| `info.title + info.content` | `info.rows: [{label, value, icon}]` |
| `code.content` | `code.code` |
| `badges.items[].label` | `badges.items[].text` |
| `list.items[].label` | `list.items[].text` |
| `blocks: []` | blocks 禁止为空 |

---

## 推荐图标（不限于此，任何 Material Icons 名称均可）

**Git/代码：** `merge_type` `fork_right` `account_tree` `commit` `tag` `source` `link` `content_copy` `difference` `analytics` `rule` `fact_check` `rate_review` `approval` `merge` `playlist_add_check` `done_all`

**文件：** `description` `insert_drive_file` `note` `article` `folder` `file_copy` `receipt`

**状态/进度：** `running_with_errors` `pending` `hourglass_empty` `schedule` `timelapse` `autorenew` `visibility` `check_circle` `cancel` `stop` `play_arrow` `pause` `refresh`

**操作：** `search` `filter_list` `sort` `download` `upload` `settings` `launch` `arrow_forward` `arrow_back` `close` `add` `remove` `edit` `delete`

**信息：** `info` `help` `smart_toy` `rocket_launch` `bolt` `flash_on` `electric_bolt` `power` `speed`

---

## 正确示例

```text
<result>
{"kind":"card","payload":{"header":{"icon":"bug_report","title":"[BUG] 编译器内部错误","subtitle":"Issue #3112","badges":[{"text":"bug","color":"red"},{"text":"待办的","color":"gray"}]},"blocks":[{"type":"info","rows":[{"label":"提交人","value":"yms_hi","icon":"person"},{"label":"时间","value":"2026-03-25 22:12:43","icon":"schedule"}]},{"type":"code","code":"Internal Compiler Error: Signal 11 received","lang":"text"}]}}
</result>
```
