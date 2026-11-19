# install 模块 — 查询工具规格

安装模块查找、镜像路径归属反查。install_modules 是从镜像文件回溯到源码部件的关键桥梁。

## 工具清单

| 工具 | 说明 |
|------|------|
| `get_install_module` | 按 GN label 查安装模块 |
| `search_install_modules` | 按 label 或 label_name 模糊搜索安装模块 |
| `owner_of` | 镜像路径 → 归属部件 |
| `installed_at` | 镜像路径 → 安装模块列表 |

---

## get_install_module

按去后缀的 GN label 查找安装模块，返回模块信息与安装产物列表。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `label` | string | ✓ | 去 toolchain 后缀的 GN label（如 `//foundation/ability/ability_runtime:ability_runtime`） |

**返回**

```json
{
  "id": 230,
  "ordinal": 42,
  "label": "//foundation/ability/ability_runtime/services/abilitymgr:abilityms",
  "label_name": "abilityms",
  "type": "lib64",
  "source": "ability/ability_runtime/libabilityms.z.so",
  "install_enable": true,
  "component": "ability_runtime",
  "component_id": 5,
  "source_url": "https://gitcode.com/openharmony/ability_ability_runtime/tree/abc123d/services/abilitymgr/BUILD.gn",
  "targets": [
    {"dest": "system/lib64/platformsdk/libabilityms.z.so"}
  ],
  "tags": ["platformsdk_indirect"]
}
```

`type` 是安装模块类型，实际值随采集器记录变化（例如 `lib64` / `etc` / `bin` /
`sa_info` / `app` / `unknown`）。`targets` 是该模块装出的镜像落点列表；当前工具
只投影 `dest`。需要 `partition`、`file_name`、`directory`、`size`、链接目标等
`install_targets` 全字段时，用 `sql` 查询该表。`tags` 是 `innerapi_tags` 展开值列表。

**错误码**

| code | 说明 |
|------|------|
| `NOT_FOUND` | label 不存在 |
| `AMBIGUOUS` | 同一 label 匹配多个模块（两个 toolchain 同名） |

---

## search_install_modules

按 label 或 label_name 模糊搜索安装模块。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `query` | string | ✓ | 搜索关键词，匹配 `label` 子串或 `label_name` 子串 |
| `type` | string | | 按类型过滤：`lib` / `etc` / `bin` / `sa_info` / `app` |
| `component` | string | | 按部件名精确过滤 |
| `limit` | int | | 返回上限，默认 20，上限 100 |

**返回**

```json
{
  "results": [
    {
      "id": 230,
      "label": "//foundation/ability/ability_runtime/services/abilitymgr:abilityms",
      "label_name": "abilityms",
      "type": "lib64",
      "component_id": 5
    }
  ],
  "total": 1
}
```

`search_install_modules` 只按 `label` 和 `label_name` 模糊匹配，**不搜索**
`source`、`targets.dest` 或产物文件名。要找 `libabilityms.z.so` 这类镜像文件名，
用 `search_elf_modules --query libabilityms` 或 SQL 查 `install_targets`。

返回项给的是 `component_id`，不是部件名；需要名字时再查 `get_component` 或 JOIN
`components`。`total` 是当前 `limit` 页内返回的条数，不是全量匹配数，也没有
`truncated` 字段。

---

---

## owner_of

给定一个镜像内路径，返回归属部件。这是 Agent 最高频的问题之一（"这个文件属于谁？"）。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `dest` | string | ✓ | 镜像内相对路径（如 `system/lib/libfoo.z.so`、`system/etc/init/foundation.cfg`） |

**返回**

```json
{
  "component": "ability_runtime",
  "component_id": 5,
  "dest": "system/lib/libfoo.z.so",
  "install_module": "//foundation/ability/ability_runtime:libfoo",
  "install_module_id": 231
}
```

归属解析链：`dest` → `install_targets`（精确匹配或目录前缀匹配） → `install_modules` → `component_id` → `components`。如果 dest 是目录安装（`directory=1`），用前缀匹配。

`owner_of` 只回答**唯一归属**。如果一个路径命中多个安装模块，工具不会任选第一个，
而是返回 `AMBIGUOUS`，错误消息中列出候选模块。需要查看候选时使用：

```bash
ask installed_at --dest <dest>
```

**错误码**

| code | 说明 |
|------|------|
| `NOT_FOUND` | 路径不在镜像中，或安装模块未归属到任何部件 |
| `AMBIGUOUS` | 路径被多个模块安装，无法唯一确定归属；用 `installed_at` 查看候选 |

---

## installed_at

返回安装到指定镜像路径的全部模块。比 `owner_of` 更细——不改部件，返回所有匹配模块。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `dest` | string | ✓ | 镜像内相对路径 |

**返回**

```json
{
  "modules": [
    {
      "module_id": 230,
      "label": "//foundation/ability/ability_runtime/services/abilitymgr:abilityms",
      "type": "lib64",
      "component": "ability_runtime",
      "component_id": 5,
      "dest": "system/lib64/platformsdk/libabilityms.z.so",
      "directory": null
    }
  ]
}
```

含目录安装前缀匹配的结果。这里的 `directory` 来自安装模块发布记录，当前很多记录
为 `null`；它不是 `install_targets.directory` 的可靠投影。需要判断某个 target 是否
目录安装时，用 SQL 查询 `install_targets.directory`。
