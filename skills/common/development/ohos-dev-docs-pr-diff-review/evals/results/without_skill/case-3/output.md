- **[P2] `module.name` 类型不符合 schema** — `module.json5:1`：补丁将 `name` 从字符串 `'entry'` 改为数字 `123`，违反所提供 schema 的 string 要求，会导致 schema 校验失败。应改为字符串，例如 `name: '123'`。

尾随逗号符合 JSON5 语法；Markdown 文件仅重命名，无内容变更，不构成问题。
