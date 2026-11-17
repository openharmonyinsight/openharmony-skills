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
  "label": "//foundation/ability/ability_runtime:ability_runtime",
  "label_name": "ability_runtime",
  "type": "lib",
  "source": "foundation/ability/ability_runtime:ability_runtime",
  "install_enable": true,
  "component": "ability_runtime",
  "component_id": 5,
  "source_url": "https://gitcode.com/openharmony/ability_ability_runtime/tree/abc123d/BUILD.gn",
  "targets": [
    {"id": 501, "dest": "system/lib/libability_runtime.z.so", "partition": "system", "file_name": "libability_runtime.z.so", "directory": false, "size": 1234567}
  ],
  "tags": ["chipsetsdk"]
}
```

`type` 取 `lib` / `etc` / `bin` / `sa_info` / `app` / `unknown`。`targets` 是该模块装出的全部镜像文件（`install_targets` 表）。`tags` 是 `innerapi_tags` 展开值列表。`size` 是 lstat 物理大小（不跟随链接）。

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
      "label": "//foundation/ability/ability_runtime:ability_runtime",
      "label_name": "ability_runtime",
      "type": "lib",
      "component": "ability_runtime"
    }
  ],
  "total": 1
}
```

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

**错误码**

| code | 说明 |
|------|------|
| `NOT_FOUND` | 路径不在镜像中，或安装模块未归属到任何部件 |
| `AMBIGUOUS` | 路径被多个模块安装（不同 label），无法唯一确定归属 |

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
      "label": "//foundation/ability/ability_runtime:ability_runtime",
      "type": "lib",
      "component": "ability_runtime",
      "component_id": 5,
      "dest": "system/lib/libability_runtime.z.so",
      "directory": false
    }
  ]
}
```

含目录安装前缀匹配的结果。`directory=true` 的模块在 `dest` 下安装了整个目录。
