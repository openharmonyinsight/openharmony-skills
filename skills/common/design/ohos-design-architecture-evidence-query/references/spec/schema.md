# schema 模块 — 查询工具规格

数据库结构自描述。让 Agent 了解可查的表、列、外键关系，辅助构造 SQL 与理解返回结构。

## 工具清单

| 工具 | 说明 |
|------|------|
| `get_schema` | 返回全部表的列定义与外键关系图 |
| `get_tables` | 返回已注册表名列表（轻量版） |

---

## get_schema

返回数据库全部表的完整 schema：列定义、外键关系（正反双向）、索引。供 Agent 自主构造 JOIN 查询。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `table` | string | | 只返回指定表的 schema。省略时返回全部表 |

**返回**

```json
{
  "tables": [
    {
      "name": "components",
      "columns": [
        {"name": "id", "type": "INTEGER", "nullable": false, "primary_key": true},
        {"name": "scan_id", "type": "INTEGER", "nullable": false, "references": "scans(id)"},
        {"name": "name", "type": "TEXT", "nullable": false},
        {"name": "subsystem", "type": "TEXT", "nullable": true},
        {"name": "manifest", "type": "TEXT", "nullable": true},
        {"name": "repo_id", "type": "INTEGER", "nullable": true, "references": "repos(id)"},
        {"name": "deps", "type": "JSON", "nullable": true},
        {"name": "record", "type": "JSON", "nullable": true}
      ],
      "primary_key": ["id"],
      "indexes": [
        {"name": "idx_components_subsystem", "columns": ["scan_id", "subsystem"]},
        {"name": "idx_components_repo", "columns": ["scan_id", "repo_id"]}
      ],
      "outgoing_fks": [
        {"column": "repo_id", "table": "repos", "to": "id", "on_delete": "CASCADE"}
      ],
      "incoming_fks": [
        {"table": "innerapis", "column": "component_id", "to": "id"},
        {"table": "features", "column": "component_id", "to": "id"},
        {"table": "syscaps", "column": "component_id", "to": "id"},
        {"table": "install_modules", "column": "component_id", "to": "id"},
        {"table": "services", "column": "component_id", "to": "id"}
      ]
    }
  ]
}
```

`outgoing_fks` 是本表指向其余表的外键（正方向）。`incoming_fks` 是其余表指向本表的外键（反方向）。`on_delete` 取 `CASCADE` 或 `SET NULL`。`type` 取 `TEXT` / `INTEGER` / `JSON`（JSON 实际存储为 TEXT）。

Agent 可用此工具自行构造多表 JOIN：从 `outgoing_fks`/`incoming_fks` 找到关联表与列，拼出 SQL 后通过 `sql_query` 执行。

---

## get_tables

返回已注册表名列表，按名字排序。比 `get_schema` 轻量——Agent 只需知道有哪些表可查时用。

**参数**：无

**返回**

```json
{
  "tables": [
    "arkts_kit_relations",
    "arkts_kits",
    "arkts_links_run",
    "arkts_modules",
    "arkts_sources",
    "component_links_run",
    "components",
    "elf_module_dependencies",
    "elf_modules",
    "features",
    "gn_args",
    "hdis",
    "innerapis",
    "install_module_tags",
    "install_modules",
    "install_targets",
    "native_headers",
    "repos",
    "sas",
    "services",
    "syscaps"
  ]
}
```

`get_tables` 只返回 `collector_tables` 注册的实体表。`scans`、`collector_runs`、`collector_tables`、`issues` 等框架表不会出现在列表中，也不能通过 `sql_query` 查询。

## 框架表 `collector_tables`

采集器在扫描时写入的**元数据目录**：这一次扫描由哪些采集器产生、各自声明了哪些表。
查询层靠它拿表名白名单与"哪张表按部件/服务归属"，**因此不需要 import 任何采集器**
（见 `cli/oskm_cli/query/catalog.py`）。

| 列 | 类型 | 含义 |
|---|---|---|
| `collector` | TEXT | 采集器注册名 |
| `table_name` | TEXT | 它声明的一张表 |
| `is_primary` | INTEGER | 是否该采集器的主表（`TABLES[0]`） |
| `component_column` | TEXT | 主表里指向部件的列，没有则为 NULL |
| `service_column` | TEXT | 主表里指向宿主服务的列，没有则为 NULL |
| `schema_version` | TEXT | 写入时该采集器的 schema 版本 |

主键 `(collector, table_name)`。行数由采集器注册表和本次扫描决定，随版本变化。

**为什么"是不是主表"要显式存**：按"有没有 `component_id` 列"去推会把 5 张推成 9 张——
`gn_args` / `innerapis` / `syscaps` / `features` 都带这一列，但它们是次表。
这个区分采集器知道，库 schema 推不出来。

**旧库没有这张表**时，查询层报 `SCHEMA_TOO_OLD` 并提示重新扫描，
不会退回去 import 采集器。
