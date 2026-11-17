# sa 模块 — 查询工具规格

SA 服务（System Ability）的查找与搜索。SA 服务是 OpenHarmony 的系统能力抽象，通过 SA ID 标识，由 `sa_main` 进程托管。

## 工具清单

| 工具 | 说明 |
|------|------|
| `get_sa` | 按 SA ID 查找 SA 服务 |
| `search_sas` | 按库名/配置文件名模糊搜索 SA 服务 |

---

## get_sa

按 SA ID（整数编号）精确查找。SA ID 是 SA profile 中声明的全局唯一标识（如 `1401`）。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `sa_id` | int | ✓ | SA 编号（如 `1401`） |

**返回**

```json
{
  "id": 120,
  "sa_id": 1401,
  "libpath": "system/lib/libdemo.z.so",
  "profile": "system/profile/1401.json",
  "run_on_create": false,
  "distributed": false,
  "dump_level": 0,
  "auto_restart": true,
  "service": {"id": 45, "cfg": "system/etc/init/foundation.cfg", "name": "foundation"},
  "component": "ability_runtime",
  "component_id": 5,
  "install_module": "//foundation/ability/ability_runtime:ability_runtime",
  "install_module_id": 230
}
```

`service` 是宿主服务（通过 `service_id` JOIN）。`component` 和 `install_module` 是归属链显示名。

**错误码**

| code | 说明 |
|------|------|
| `NOT_FOUND` | SA ID 不存在 |
| `NO_SESSION` | 未建立会话 |

---

## search_sas

按 libpath、profile 或 SA ID 模糊搜索。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `query` | string | ✓ | 搜索关键词，匹配 libpath 子串或 profile 文件名子串 |
| `distributed` | bool | | 只返回 `distributed=true` 的 SA（跨设备分发能力） |
| `auto_restart` | bool | | 只返回 `auto_restart=true` 的 SA（崩溃自动重启） |
| `component` | string | | 按部件名精确过滤 |
| `limit` | int | | 返回上限，默认 20，上限 100 |

**返回**

```json
{
  "results": [
    {
      "id": 120,
      "sa_id": 1401,
      "libpath": "system/lib/libdemo.z.so",
      "profile": "system/profile/1401.json",
      "distributed": false,
      "auto_restart": true,
      "component": "ability_runtime"
    }
  ],
  "total": 1
}
```
