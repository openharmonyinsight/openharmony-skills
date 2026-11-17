# component 模块 — 查询工具规格

部件查找、搜索、依赖关系、特性值、InnerAPI 导航。这是 Agent 最高频的模块。

## 工具清单

| 工具 | 说明 |
|------|------|
| `get_component` | 按名精确查找部件 |
| `search_components` | 按名模糊搜索部件 |
| `component_attached` | 部件关联的各域记录（服务/SA/HDI/安装模块/ELF） |
| `component_dependencies` | 正向依赖（它依赖谁） |
| `component_dependents` | 反向依赖（谁依赖它） |
| `component_features` | 特性名 + gn_arg 当前值 |
| `component_syscaps` | 声明的系统能力名列表 |
| `component_innerapis` | InnerAPI + 关联的安装模块 |

---

## get_component

按部件名精确查找，返回完整记录与各域关联计数。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `name` | string | ✓ | 部件名（构建索引键，如 `ability_runtime`） |

**返回**

```json
{
  "id": 5,
  "name": "ability_runtime",
  "subsystem": "ability",
  "manifest": "foundation/ability/ability_runtime/bundle.json",
  "repo": "ability_ability_runtime",
  "repo_id": 1,
  "deps": {"components": ["ace_engine", "bundle_framework"], "third_party": ["jsoncpp"]},
  "manifest_url": "https://gitcode.com/openharmony/ability_ability_runtime/tree/abc123d/bundle.json",
  "attached_counts": {
    "innerapis": 12,
    "features": 12,
    "syscaps": 0,
    "install_modules": 15,
    "services": 3,
    "sas": 4,
    "hdis": 0,
    "elf_modules": 8
  }
}
```

`attached_counts` 只统计 `component_id` 直接指向本部件的行。`repo` 是仓名（非 id）；`repo_id` 是关联 `repos.id` 数字 id（未关联时为 `null`），反查仓时用 `get_repo`（按名）或 `list_repos`。`deps` 是原始声明对象。

**错误码**

| code | 说明 |
|------|------|
| `NOT_FOUND` | 部件名不存在 |
| `NO_SESSION` | 未建立会话 |

---

## search_components

按名模糊搜索，返回摘要列表。底层 `WHERE name LIKE '%query%'`。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `query` | string | ✓ | 搜索关键词，匹配部件名子串 |
| `limit` | int | | 返回上限，默认 20，上限 100 |
| `subsystem` | string | | 按子系统过滤（精确匹配） |

**返回**

```json
{
  "results": [
    {
      "id": 5,
      "name": "ability_runtime",
      "subsystem": "ability",
      "manifest": "foundation/ability/ability_runtime/bundle.json"
    },
    {
      "id": 6,
      "name": "ability_base",
      "subsystem": "ability",
      "manifest": "foundation/ability/ability_base/bundle.json"
    }
  ],
  "total": 2
}
```

---

## component_attached

返回此部件在各域的关联记录，按采集器名分组。一次调用拿到部件的全部产出。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `component_id` | int | ✓ | `get_component` / `search_components` 返回的 id |
| `collector` | string | | 只返回指定域（如 `"services"`、`"sas"`、`"hdis"`、`"install_modules"`、`"elf_modules"`） |

**返回**

```json
{
  "services": [
    {"id": 45, "cfg": "system/etc/init/foundation.cfg", "name": "foundation", "type": "default"}
  ],
  "sas": [
    {"id": 120, "sa_id": 1401, "libpath": "system/lib/libdemo.z.so"}
  ],
  "install_modules": [
    {"id": 230, "label": "//foundation/ability/ability_runtime:ability_runtime", "type": "lib"}
  ]
}
```

每个域返回的是该域发布记录的摘要（关键字段，非全集）。`collector` 省略时返回所有有 `COMPONENT_COLUMN` 的域。无关联记录的域的键不出现。

**错误码**

| code | 说明 |
|------|------|
| `INVALID_COMPONENT_ID` | `component_id` 不存在 |
| `INVALID_COLLECTOR` | `collector` 不是已注册的采集器名 |

---

## component_dependencies

返回此部件声明的正向依赖（它依赖哪些部件）。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `component_id` | int | ✓ | 部件 id |

**返回**

```json
{
  "components": ["ace_engine", "bundle_framework"],
  "third_party": ["jsoncpp"],
  "unresolved": ["nonexistent_part"]
}
```

`components` 是部件依赖（在本扫描中存在的）。`third_party` 是三方库依赖。`unresolved` 是声明了但本扫描中找不到的部件名（对应 `COMPONENT_DEP_UNRESOLVED` issue）。

---

## component_dependents

返回反向依赖（哪些部件依赖它）。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `component_id` | int | ✓ | 部件 id |

**返回**

```json
{
  "dependents": ["ace_engine", "bundle_framework", "communication_dsoftbus"]
}
```

扫描全量 `deps.components` 构建入度图后反查。

---

## component_features

返回部件声明的特性名列表，每个特性附带 gn_arg 中的当前值（由 `component_links` 关联）。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `component_id` | int | ✓ | 部件 id |

**返回**

```json
{
  "features": [
    {
      "value": "ability_runtime_power",
      "current_value": true,
      "value_type": "bool",
      "has_override": false,
      "gn_arg_id": 45
    },
    {
      "value": "ability_runtime_auto_fill_ability",
      "current_value": null,
      "value_type": null,
      "has_override": null,
      "gn_arg_id": null
    }
  ]
}
```

`value` 是 features 表中的特性名。`gn_arg_id` 为 null 表示 `component_links` 未找到匹配的 gn_arg（特性名未在 `declare_args` 中声明，或属于条件配置未展开）。`current_value`/`value_type`/`has_override` 从 `gn_args` 表 JOIN 获取。

---

## component_syscaps

返回部件声明的系统能力名列表。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `component_id` | int | ✓ | 部件 id |

**返回**

```json
{
  "syscaps": [
    {"name": "SystemCapability.Ability.Fwk"},
    {"name": "SystemCapability.Ability.AbilityBase"}
  ]
}
```

syscaps 是 `component.syscap`/`system_capabilities` 数组展开值表。与 features 不同，syscaps 没有 gn_arg 关联——它只声明名称，不声明值。

---

## component_innerapis

返回部件的 InnerAPI（inner_kits / inner_api），每个附关联的安装模块（由 `component_links` 填充 `install_module_id`）。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `component_id` | int | ✓ | 部件 id |

**返回**

```json
{
  "innerapis": [
    {
      "id": 88,
      "name": "//foundation/ability/ability_runtime/frameworks:ability_runtime",
      "external_name": "ability_runtime:ability_runtime",
      "field": "inner_kits",
      "source_index": 0,
      "install_module_id": 230,
      "install_module_label": "//foundation/ability/ability_runtime:ability_runtime",
      "source_url": "https://gitcode.com/openharmony/ability_ability_runtime/tree/abc123d/frameworks/BUILD.gn"
    },
    {
      "id": 89,
      "name": "//foundation/ability/ability_runtime/services:ability_manager_service",
      "external_name": "ability_runtime:ability_manager_service",
      "field": "inner_api",
      "source_index": 1,
      "install_module_id": null,
      "install_module_label": null,
      "source_url": "https://gitcode.com/openharmony/ability_ability_runtime/tree/abc123d/services/BUILD.gn"
    }
  ]
}
```

`source_url` 由 `name`（GN label）经 `git_url` 工具构建，指向 label 目录的 BUILD.gn（目标定义的推荐猜测）。

`install_module_id` 为 null 表示该 innerapi 的 GN label 未在 `install_modules.label` 中找到匹配（声明了但未构建为安装模块）。`install_module_label` 从 `install_modules` 表 JOIN 获取。
