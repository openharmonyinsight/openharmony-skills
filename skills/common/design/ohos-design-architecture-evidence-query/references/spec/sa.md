# sa 模块 — 查询工具规格

SA 服务（System Ability）的查找与搜索。SA 服务是 OpenHarmony 的系统能力抽象，通过 SA ID 标识，由 `sa_main` 进程托管。

## 工具清单

| 工具 | 说明 |
|------|------|
| `get_sa` | 按 SA ID 查找 SA 服务 |
| `search_sas` | 按库名、配置文件名或 SA ID 模糊搜索 SA 服务 |

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
  "scan_id": 1,
  "position": 52,
  "sa_id": 1401,
  "profile": "system/profile/1401.json",
  "libpath": "libdemo.z.so",
  "run_on_create": 1,
  "distributed": 0,
  "dump_level": 0,
  "auto_restart": null,
  "service_id": 45,
  "component_id": 5,
  "install_module_id": 230,
  "record": "{\"libpath\":\"libdemo.z.so\",\"name\":1401,\"run-on-create\":true}",
  "component": "ability_runtime",
  "install_module": "//foundation/ability/ability_runtime/services/demo:demo",
  "service": {"cfg": "system/etc/init/foundation.cfg", "name": "foundation"}
}
```

`service` 是宿主服务摘要，只含 `cfg` 与 `name`；服务主键看顶层 `service_id`。
`component` 和 `install_module` 是归属链显示名。

`libpath` 是 SA profile 中声明的字符串，**不保证是镜像内路径**。它可能是裸库名
（如 `libdemo.z.so`），也可能是绝对路径（如 `/system/lib64/libdemo.z.so`）。
不要按 `cpu_arch` 手工拼 `system/lib/` 或 `system/lib64/`。真实镜像 `dest`
要用安装模块或 ELF 证据解析：

```bash
ask get_install_module --label '<install_module>'
ask search_elf_modules --query libdemo.z.so
ask installed_at --dest system/lib64/platformsdk/libdemo.z.so
```

布尔类字段来自 profile 原始记录，当前工具返回 SQLite 投影后的 `0` / `1` /
`null`；`null` 表示 profile 未声明该字段，不等于 `false`。

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
| `query` | string | ✓ | 搜索关键词，匹配 `libpath`、`profile` 或 `CAST(sa_id AS TEXT)` 子串 |
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
      "libpath": "libdemo.z.so",
      "profile": "system/profile/1401.json",
      "distributed": 0,
      "auto_restart": null,
      "component": "ability_runtime"
    }
  ],
  "total": 1
}
```

`search_sas` 的 `total` 是当前 `limit` 页内返回的条数，不是全量匹配数，也没有
`truncated` 字段。需要全量统计时用 `sql` 或 `list_entities`。
