# elf 模块 — 查询工具规格

ELF 二进制模块的 DT_NEEDED 依赖图遍历。

## 工具清单

| 工具 | 说明 |
|------|------|
| `search_elf_modules` | 按 soname 或 file_name 模糊搜索 ELF |
| `elf_dependencies` | 前向/反向 BFS 依赖闭包（含距离与路径） |
| `elf_dependents` | 反向依赖列表（谁依赖了它） |

---

## search_elf_modules

按 soname 或 file_name 模糊搜索 ELF 模块。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `query` | string | ✓ | 搜索关键词，匹配 `soname` 子串或 `file_name` 子串 |
| `partition` | string | | 按分区过滤：`system` / `vendor` / `updater` |
| `component` | string | | 按部件名精确过滤 |
| `limit` | int | | 返回上限，默认 20，上限 100 |

**返回**

```json
{
  "results": [
    {
      "id": 501,
      "dest": "system/lib/libfoo.z.so",
      "soname": "libfoo.z.so",
      "file_name": "libfoo.z.so",
      "partition": "system",
      "component": "foo_runtime"
    }
  ],
  "total": 1,
  "truncated": false
}
```

`total` 是全量匹配数，不受 `limit` 影响；`results` 是本次按 `limit` 返回的条目。
`total > len(results)` 时 `truncated=true`，即 `truncated` 表示结果被 `limit` 截断；需要完整结果时提高 `limit`。

---

## elf_dependencies

从指定 ELF 模块出发，沿 DT_NEEDED 边做 BFS，返回依赖闭包：**每个可达节点一行，距离取最短**。

> 这是闭包，不是路径枚举。一个节点有几条路可达都只出一行。
> 旧实现按路径展开，实测 `libace_engine_pa_ark.z.so` + `max_distance=3`
> 返回 3,586 行却只有 297 个不同节点（92% 重复），耗时 90.6 秒、1.27 MB。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `dest` | string | ✓ | 镜像内 ELF 文件路径（如 `system/lib/libfoo.z.so`） |
| `direction` | string | | `forward`（默认）：沿着 DT_NEEDED 往被依赖方走；`reverse`：反向，谁依赖了它 |
| `max_distance` | int | | 跳数上限。**省略时按 16 封顶**（防环），不是无限制 |
| `limit` | int | | 最多返回几个节点，默认 200、上限 1000。截断时置 `truncated` |

**从 1 跳起**，不够再加。`total` 随库变化，判断方法始终是同时看 `total` 与
`truncated`，不要把一个快照的节点数写死成产品常量。

**返回**

```json
{
  "root": "system/lib/libfoo.z.so",
  "direction": "forward",
  "max_distance": 16,
  "total": 2,
  "truncated": false,
  "reachable": [
    {
      "dest": "system/lib/libbar.z.so",
      "soname": "libbar.z.so",
      "partition": "system",
      "component": "bar_runtime",
      "component_id": 12,
      "distance": 1,
      "via": "system/lib/libfoo.z.so → system/lib/libbar.z.so"
    },
    {
      "dest": "system/lib/libbaz.z.so",
      "soname": "libbaz.z.so",
      "partition": "system",
      "component": null,
      "component_id": null,
      "distance": 2,
      "via": "system/lib/libfoo.z.so → system/lib/libbar.z.so → system/lib/libbaz.z.so"
    }
  ],
  "unresolved": [
    {"needed_name": "libnonexistent.z.so", "caller_dest": "system/lib/libfoo.z.so"}
  ]
}
```

`reachable` 按 `(distance, dest)` 排序。`via` 是**一条**最短路径（同样短的有多条时任取一条，
不声称唯一），跳数与 `distance` 一致。`component` 为 null 表示该 ELF 未归属到部件。
`unresolved` 列出 DT_NEEDED 中未在 system/vendor 内找到的库名，只针对根节点。

`total` 是闭包的真实大小，`truncated=true` 表示 `reachable` 被 `limit` 截断——
**截断是显式的，别把截断后的条数当成闭包大小**。

`reverse` 方向返回"谁依赖了 root"的闭包——回答"如果本文改了 libfoo，谁会受影响"。

**错误码**

| code | 说明 |
|------|------|
| `NOT_FOUND` | `dest` 不是已扫描的 ELF 文件 |
| `INVALID_PARAM` | `limit` 小于 1 |
| `NOT_ELF` | `dest` 存在但不是 ELF 文件（install_target 未解析为 elf_modules 行） |
| `NO_SESSION` | 未建立会话 |

---

## elf_dependents

返回直接依赖了指定 ELF 的模块列表（depth=1，不做闭包展开）。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `dest` | string | ✓ | 镜像内 ELF 文件路径 |

**返回**

```json
{
  "dest": "system/lib/libfoo.z.so",
  "dependents": [
    {
      "dest": "system/lib/libbar.z.so",
      "soname": "libbar.z.so",
      "partition": "system",
      "component": "bar_runtime",
      "component_id": 12
    }
  ]
}
```

比 `elf_dependencies(direction='reverse', max_distance=1)` 更直接——只返回直接边，不带 path/via。适合"谁直接引用了本文"的快速查询。
