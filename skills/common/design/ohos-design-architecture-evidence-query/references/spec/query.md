# query 模块 — 查询工具规格

通用列表/聚合查询与受限 SQL 逃生口。覆盖各域 typed 工具未封装的临时查询需求。

## 工具清单

| 工具 | 说明 |
|------|------|
| `list_entities` | 任意已注册实体表的分页列表查询 |
| `aggregate` | 任意已注册实体表的分组聚合 |
| `sql_query` | 受限只读原始 SQL（逃生口） |

---

## list_entities

对已注册实体表做分页列表查询，支持等值过滤与排序。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `table` | string | ✓ | 已注册实体表（如 `components`、`services`、`gn_args`、`install_modules`、`elf_modules`） |
| `filters` | object | | 键必须是该表真实列名，值为等值匹配值 |
| `sort` | string | | 排序列名；必须是该表真实列名 |
| `desc` | bool | | 降序排序，默认 false |
| `page` | object | | `{"limit": 100, "page_token": null}`；limit 默认 100，范围 1..1000 |

**返回**

```json
{
  "items": [
    {"id": 5, "name": "ability_runtime", "subsystem": "ability"},
    {"id": 12, "name": "bar_runtime", "subsystem": "ability"}
  ],
  "total": 382,
  "next_page_token": "eyJzY2FuX2lkIjoxfQ"
}
```

`items` 是原始数据库行。`total` 是该过滤条件下的总行数。`next_page_token` 为 null 表示末页；非 null 时原样传回 `page.page_token` 获取下一页。游标绑定当前 `scan_id`、表、过滤、排序和 limit；任何参数变化返回 `INVALID_PAGE_TOKEN`。未指定排序时稳定追加 `rowid`。

**错误码**

| code | 说明 |
|------|------|
| `INVALID_TABLE` | `table` 不是当前库已注册实体表 |
| `INVALID_FILTER` | `filters` 不是对象或包含未知列 |
| `INVALID_SORT` | `sort` 不是该表真实列名 |
| `INVALID_PAGE_TOKEN` | 游标格式错误、跨 scan、offset 非法或参数指纹不匹配 |
| `INVALID_PARAM` | `page` / `page.limit` 类型或范围非法 |
| `NO_SESSION` | 未建立会话 |

---

## aggregate

对已注册实体表按 1-3 个真实列分组并统计行数，返回分页结果。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `table` | string | ✓ | 已注册实体表 |
| `group_by` | [string] | ✓ | 1-3 个真实列名 |
| `filters` | object | | 与 `list_entities` 相同的等值过滤 |
| `page` | object | | `{"limit": 100, "page_token": null}`；limit 默认 100，范围 1..1000 |

**返回**

```json
{
  "groups": [
    {"key": "ability", "count": 42},
    {"key": "arkui", "count": 15}
  ],
  "total": 382,
  "next_page_token": null
}
```

多维分组时 `key` 用 `/` 连接，空值显示为 `(null)`。排序为 `count` 降序、分组列、`rowid`。`total` 是过滤后的原始行数，不是分组数。`next_page_token` 非空时表示还有分组页。

**错误码**

| code | 说明 |
|------|------|
| `INVALID_TABLE` | 表名未注册 |
| `INVALID_GROUP_BY` | 分组列未知、数量不在 1..3，或类型非法 |
| `INVALID_FILTER` | 过滤列未知 |
| `INVALID_PAGE_TOKEN` | 游标无效或参数指纹不匹配 |
| `INVALID_PARAM` | 分页参数非法 |
| `NO_SESSION` | 未建立会话 |

---

## sql_query

受限只读 SQL 逃生口，用于 typed 工具未覆盖的多表 JOIN、子查询或 CTE。

**安全约束**

1. **只读执行**：仅允许 SELECT/WITH；连接为只读，SQLite authorizer 拒绝写入和 schema 变更。
2. **快照隔离**：每条 SQL 在当前主库或已挂载 alias 的私有内存快照中执行。快照只复制该来源允许的实体表和当前 scan 行；`OR`、注释、字符串、JOIN、子查询和 CTE 均不会混入其余 scan 或其余库。
3. **表白名单**：只能读取该来源 `collector_tables` 注册的实体表。`scans`、`collector_runs`、`collector_tables`、`issues` 等框架表一律拒绝；引号、反引号、方括号、逗号 JOIN、子查询和 CTE 中的引用都会被 authorizer 检查。
4. **alias 白名单**：`alias.table` 只能使用已通过 `attach_secondary` 挂载的合法别名；未挂载别名返回 `ALIAS_NOT_ATTACHED`。
5. **行数限制**：执行层最多取 `limit + 1` 行；`limit` 必须是 1..1000，默认 1000。返回 `limit` 行并用第 `limit + 1` 行判断 `truncated`。
6. **执行预算**：5 秒 progress-handler 超时，返回 `TIMEOUT`。
7. **禁止 PRAGMA/ATTACH/DETACH**：ATTACH/DETACH 只能通过 `attach_secondary` / `detach_secondary` 工具执行。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `sql` | string | ✓ | SELECT/WITH 语句，支持多行 SQL |
| `params` | [any] | | `?` 绑定值列表 |
| `limit` | int | | 返回行数上限，默认 1000，范围 1..1000 |

**返回**

```json
{
  "rows": [
    {"component": "ace_engine", "feature_count": 35},
    {"component": "ability_runtime", "feature_count": 12}
  ],
  "row_count": 2,
  "truncated": false
}
```

**示例**

```json
{
  "sql": "SELECT c.name AS component, COUNT(f.id) AS feature_count\nFROM components c\nLEFT JOIN features f ON f.scan_id = c.scan_id AND f.component_id = c.id\nGROUP BY c.id\nORDER BY feature_count DESC",
  "limit": 10
}
```

**错误码**

| code | 说明 |
|------|------|
| `NOT_READ_ONLY` | SQL 不是 SELECT/WITH 开头 |
| `TABLE_NOT_ALLOWED` | 引用框架表或未注册表 |
| `ALIAS_NOT_ATTACHED` | 引用未挂载的别名 |
| `INVALID_PARAM` | `limit` 或 `params` 类型/范围非法 |
| `PRAGMA_FORBIDDEN` | 包含 PRAGMA |
| `ATTACH_FORBIDDEN` | SQL 内包含 ATTACH/DETACH |
| `SQL_ERROR` | SQLite 语法或执行错误 |
| `TIMEOUT` | 执行超过 5 秒 |
| `NO_SESSION` | 未建立会话 |
