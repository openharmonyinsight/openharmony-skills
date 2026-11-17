# issues 模块 — 查询工具规格

扫描质量问题清单查询。

## 工具清单

| 工具 | 说明 |
|------|------|
| `list_issues` | 返回扫描中发现的质量问题，可按采集器/严重度/advisory 过滤 |

---

## list_issues

返回当前扫描的质量问题清单。每个 issue 是一个发现点，`advisory=0` 会让扫描 degraded，`advisory=1` 只影响 `--fail-on`。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `collector` | string | | 只返回指定采集器的 issue（如 `"components"`、`"services"`） |
| `severity` | string | | 按严重度过滤：`info` / `warning` / `error` |
| `advisory` | bool | | `true` 只返回 advisory（数据可疑但扫描正常）；`false` 只返回扫描级问题 |
| `component` | string | | 按部件名过滤 |
| `limit` | int | | 返回上限，默认 50，上限 200 |

**返回**

```json
{
  "issues": [
    {
      "collector": "components",
      "path": "foundation/ability/ability_runtime/bundle.json",
      "pointer": "/component/features",
      "code": "FEATURE_DUPLICATE",
      "severity": "warning",
      "component": "ability_runtime",
      "advisory": true,
      "details": {
        "value": "ability_runtime_power",
        "declarations": [
          {"component": "ability_runtime", "pointer": "/component/features/0"},
          {"component": "ability_runtime", "pointer": "/component/features/5"}
        ]
      }
    }
  ],
  "total": 1
}
```

`path` 是 workspace 相对路径。`pointer` 是 JSON Pointer（指向源文件中的位置）。`details` 是 JSON 对象（每个 code 的 details 结构不同）。`severity` 为 `info` 时通常是信息提示（如 `SUBSYSTEM_DIFFERS`），不构成问题。

`advisory` 区分：
- `advisory=0`（false）：扫描未读全/读懂 → 影响 `inventory_complete`，让扫描 degraded
- `advisory=1`（true）：数据本身可疑（重复声明、归属冲突等）→ 扫描正常，只影响 `--fail-on`

**错误码**

| code | 说明 |
|------|------|
| `INVALID_COLLECTOR` | `collector` 不是已注册的采集器名 |
| `INVALID_SEVERITY` | `severity` 不是 `info`/`warning`/`error` |
| `NO_SESSION` | 未建立会话 |
