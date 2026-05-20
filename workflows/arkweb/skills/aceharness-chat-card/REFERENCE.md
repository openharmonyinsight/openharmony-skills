# Aceharness Chat Card Reference

## Block 类型速查

| Block 类型 | 用途 | 关键字段 |
|-----------|------|---------|
| `info` | 键值对信息行 | `rows: { label, value, icon? }[]` |
| `badges` | 彩色标签列表 | `items: { text, color? }[]` |
| `text` | 文本段落 | `content, maxLines?` |
| `code` | 代码展示 | `code, lang?, copyable?` |
| `progress` | 进度条 | `value, max?, label?` |
| `steps` | 步骤指示器 | `current, total` |
| `tabs` | 标签页切换 | `tabs: { key, label, blocks }[]` |
| `collapse` | 折叠区域 | `title, icon?, subtitle?, blocks, defaultOpen?` |
| `list` | 图标列表 | `items: { icon?, color?, text }[]` |
| `status` | 状态指示器 | `state, color?, animated?, rows?` |
| `actions` | 操作按钮 | `items: { label, prompt, icon? }[]` |
| `divider` | 分隔线 | 无额外字段 |

## 预设颜色

Badge 和 Status 支持以下预设颜色名：

| 颜色名 | Badge 样式 | Status 圆点 |
|--------|-----------|------------|
| `blue` | `bg-blue-500/10 text-blue-400` | `bg-blue-500` |
| `green` | `bg-green-500/10 text-green-400` | `bg-green-500` |
| `red` | `bg-red-500/10 text-red-400` | `bg-red-500` |
| `yellow` | `bg-yellow-500/10 text-yellow-400` | `bg-yellow-500` |
| `purple` | `bg-purple-500/10 text-purple-400` | `bg-purple-500` |
| `orange` | `bg-orange-500/10 text-orange-400` | `bg-orange-500` |
| `gray` | `bg-gray-500/10 text-gray-400` | `bg-gray-500` |
| `cyan` | `bg-cyan-500/10 text-cyan-400` | — |
| `pink` | `bg-pink-500/10 text-pink-400` | — |

也可以直接传 Tailwind 类名字符串作为自定义颜色。

## Header 渐变预设

常用渐变组合：

| 场景 | gradient 值 |
|------|------------|
| 通用/信息 | `from-blue-500 to-cyan-500` |
| Agent/AI | `from-purple-500 to-pink-500` |
| 成功/运行 | `from-green-500 to-emerald-500` |
| 警告/分析 | `from-amber-500 to-orange-500` |
| 错误/危险 | `from-red-500 to-rose-500` |
| 技能/扩展 | `from-pink-500 to-rose-500` |
| 模型/训练 | `from-cyan-500 to-teal-500` |
| 记录/历史 | `from-green-500 to-emerald-500` |
| Git/PR | `from-blue-500 to-indigo-500` |
| Issue/Bug | `from-orange-500 to-red-500` |

## Material Symbols 常用图标

| 图标名 | 用途 |
|--------|------|
| `description` | 文档/配置 |
| `smart_toy` | Agent/AI |
| `model_training` | 模型 |
| `play_circle` | 运行/启动 |
| `history` | 历史记录 |
| `extension` | 技能/插件 |
| `analytics` | 分析 |
| `merge_type` | PR/合并 |
| `bug_report` | Issue/Bug |
| `check_circle` | 成功/通过 |
| `warning` | 警告 |
| `error` | 错误 |
| `lightbulb` | 建议 |
| `auto_fix_high` | 优化 |
| `person` | 用户 |
| `group` | 团队 |
| `badge` | 名称 |
| `work` | 角色 |
| `info` | 信息 |
| `open_in_new` | 打开 |
| `play_arrow` | 播放/启动 |
| `stop` | 停止 |
| `add` | 新建 |
| `comment` | 评论 |
| `content_copy` | 复制 |

## 嵌套规则

- `tabs` 和 `collapse` 的 `blocks` 字段支持递归嵌套任意 Block 类型
- `actions` 可以出现在顶层 `card.actions` 中，也可以作为 Block 内嵌在 `blocks` 中间
- 建议嵌套深度不超过 3 层

## 校验规则

使用 `scripts/validate-card.mjs` 校验 card JSON：

```bash
echo '{"header":{"title":"test"},"blocks":[]}' | node /absolute/path/to/skills/aceharness-chat-card/scripts/validate-card.mjs
```

校验内容：
1. 必须有 `blocks` 数组
2. 每个 block 必须有合法的 `type`
3. `info` block 必须有 `rows` 数组
4. `badges` block 必须有 `items` 数组
5. `text` block 必须有 `content` 字符串
6. `code` block 必须有 `code` 字符串
7. `progress` block 必须有 `value` 数字
8. `steps` block 必须有 `current` 和 `total`
9. `tabs` block 必须有 `tabs` 数组，每个 tab 有 `key`、`label`、`blocks`
10. `collapse` block 必须有 `title` 和 `blocks`
11. `list` block 必须有 `items` 数组
12. `status` block 必须有 `state` 字符串
13. `actions` block 必须有 `items` 数组，每项有 `label` 和 `prompt`
