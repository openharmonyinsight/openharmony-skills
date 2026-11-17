# gn_args 模块 — 查询工具规格

GN 编译参数（`declare_args` 参数）的查找与搜索。

## 工具清单

| 工具 | 说明 |
|------|------|
| `get_gn_arg` | 按参数名精确查找编译参数 |
| `search_gn_args` | 按名模糊搜索编译参数 |

---

## get_gn_arg

按 GN `declare_args()` 参数名精确查找，返回默认值、当前生效值与声明位置。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `name` | string | ✓ | 参数名（如 `ability_runtime_power`、`ace_engine_feature_enable_web`） |

**返回**

```json
{
  "id": 45,
  "name": "ability_runtime_power",
  "default_value": true,
  "current_value": true,
  "value_type": "bool",
  "has_override": false,
  "comment": "Enable ability runtime power management",
  "decl_file": "foundation/ability/ability_runtime/ability_runtime.gni",
  "decl_line": 101,
  "source_url": "https://gitcode.com/openharmony/ability_ability_runtime/tree/abc123d/ability_runtime.gni#L%31%30%31",
  "component": "ability_runtime",
  "component_id": 5,
  "feature_count": 1
}
```

`default_value` 是 `declare_args()` 中的声明值（JSON 解析后的 Python 值）。`current_value` 是产品覆盖后的生效值（无覆盖时等于 `default_value`）。`has_override` 为 true 表示 `args.gn` 中显式设置了该参数。`value_type` 取 `bool` / `str` / `int` / `list` / `other`。`decl_file` 是去掉 `//` 前缀的 workspace 相对路径。`feature_count` 是有多少个 `features` 行引用了此 arg（通过 `features.gn_arg_id` 关联）。

**错误码**

| code | 说明 |
|------|------|
| `NOT_FOUND` | 参数名不存在 |
| `NO_SESSION` | 未建立会话 |

---

## search_gn_args

按参数名模糊搜索，返回摘要列表。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `query` | string | ✓ | 搜索关键词，匹配参数名子串 |
| `limit` | int | | 返回上限，默认 20，上限 100 |
| `value_type` | string | | 按类型过滤（`bool` / `str` / `int` / `list` / `other`） |
| `has_override` | bool | | 只返回有覆盖的参数 |

**返回**

```json
{
  "results": [
    {
      "id": 45,
      "name": "ability_runtime_power",
      "current_value": true,
      "value_type": "bool",
      "has_override": false,
      "component": "ability_runtime"
    }
  ],
  "total": 1
}
```
