# service 模块 — 查询工具规格

系统服务查找与宿主 SA 服务/HDI 设备导航。系统服务是 init cfg 声明的运行时入口。

## 工具清单

| 工具 | 说明 |
|------|------|
| `get_service` | 按 cfg 路径（可选 name）查找服务 |
| `search_services` | 按服务名或 cfg 路径模糊搜索 |
| `service_hosted` | 服务宿主的 SA/HDI 设备列表 |

---

## get_service

按 init 配置文件路径查找系统服务。一个 cfg 可能声明多个系统服务，用 `name` 精确选定。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `cfg` | string | ✓ | cfg 文件镜像内路径（如 `system/etc/init/foundation.cfg`） |
| `name` | string | | 服务名（如 `foundation`）。省略时返回该 cfg 下的全部服务 |

**返回**（`name` 指定时，单个对象）

```json
{
  "id": 45,
  "cfg": "system/etc/init/foundation.cfg",
  "name": "foundation",
  "type": "default",
  "executable": "/system/bin/sa_main",
  "uid": "foundation",
  "start_mode": "condition",
  "ondemand": false,
  "component": "samgr_standard",
  "component_id": 180,
  "install_module": "//foundation/systemabilitymgr/samgr:samgr",
  "install_module_id": 420
}
```

`type` 取 `sa` / `hdf` / `default`。`component` 和 `install_module` 是 JOIN 解析的显示名（非 id）。`ondemand` 是 bool（原始 `INTEGER` 投影后转换）。

**返回**（`name` 省略时，数组）

```json
{
  "services": [ {...}, {...} ]
}
```

**错误码**

| code | 说明 |
|------|------|
| `NOT_FOUND` | cfg 路径不存在，或 `name` 在该 cfg 下不存在 |
| `NO_SESSION` | 未建立会话 |

---

## search_services

按服务名或 cfg 路径模糊搜索。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `query` | string | ✓ | 搜索关键词，匹配 `name` 子串或 `cfg` 路径子串 |
| `type` | string | | 按类型过滤：`sa` / `hdf` / `default` |
| `component` | string | | 按部件名精确过滤 |
| `limit` | int | | 返回上限，默认 20，上限 100 |

**返回**

```json
{
  "results": [
    {
      "id": 45,
      "name": "foundation",
      "cfg": "system/etc/init/foundation.cfg",
      "type": "default",
      "component_id": 180
    }
  ],
  "total": 1
}
```

---

---

## service_hosted

返回此系统服务宿主的所有 SA 服务和/或 HDI 设备。一个 `sa_main` 进程可以同时托管多个 SA 服务和 HDI 设备。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `service_id` | int | ✓ | `get_service` 返回的 id |
| `collector` | string | | 只返回指定域：`"sas"` 或 `"hdis"`。省略时返回两者 |

**返回**

```json
{
  "sas": [
    {"id": 120, "sa_id": 1401, "libpath": "libdemo.z.so", "profile": "1401.json", "run_on_create": false}
  ],
  "hdis": [
    {"id": 78, "service_name": "sample", "module_name": "libsample.z.so", "node": "sample_service"}
  ]
}
```

`sas` 和 `hdis` 的键只在有记录时出现。无宿主记录时返回空对象 `{}`。

**错误码**

| code | 说明 |
|------|------|
| `INVALID_SERVICE_ID` | `service_id` 不存在 |
| `INVALID_COLLECTOR` | `collector` 不是 `"sas"` 或 `"hdis"` |
