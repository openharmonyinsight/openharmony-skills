# hdi 模块 — 查询工具规格

HDI 设备的查找与搜索。HDI 是 OpenHarmony 的硬件驱动接口抽象，声明在 HCB 配置中，由 `hdf_devhost` 进程托管。

## 工具清单

| 工具 | 说明 |
|------|------|
| `get_hdi` | 按 serviceName 或 node 查找 HDI 设备 |
| `search_hdis` | 按库名/node/serviceName 模糊搜索 |

---

## get_hdi

按 `serviceName`（精确匹配）或 `node`（精确匹配）查找 HDI 设备。两者都是 HCB 树内的标识，至少传一个。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `service_name` | string | | HDI serviceName（如 `sample`） |
| `node` | string | | HCB 树内节点名（如 `sample_service`） |

`service_name` 与 `node` 至少传一个；同时传时取交集。如果匹配多条，返回列表；匹配一条时仍返回列表（保持接口一致）。

**返回**

```json
{
  "hdis": [
    {
      "id": 78,
      "hcb": "system/etc/hdfconfig/hdf_default.hcb",
      "node": "sample_service",
      "service_name": "sample",
      "module_name": "libsample.z.so",
      "library": "system/lib/libsample.z.so",
      "policy": 2,
      "preload": 0,
      "device_match_attr": "",
      "permission": 0,
      "priority": 50,
      "service": {"cfg": "system/etc/init/host.cfg", "name": "host"},
      "component": "driver",
      "component_id": 10,
      "install_module": "//drivers/adapter/sample:sample",
      "install_module_id": 340
    }
  ]
}
```

顶层 `service_name` 是 HDI 设备自身的 serviceName；`service.name` 是通过 `service_id` JOIN 得到的宿主系统服务名（通常是 `hdf_devhost` 进程），两者可能相同也可能不同。`service` 仅包含宿主 `cfg` 和 `name`。`policy`/`preload`/`permission`/`priority` 是 HCB 声明的原始整数值。

**错误码**

| code | 说明 |
|------|------|
| `NOT_FOUND` | 两个参数都传了但无匹配 |
| `NO_PARAMS` | `service_name` 和 `node` 都未传 |
| `NO_SESSION` | 未建立会话 |

---

## search_hdis

按 library、module_name、node 或 service_name 模糊搜索。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `query` | string | ✓ | 搜索关键词，匹配 library / module_name / node / service_name 子串 |
| `component` | string | | 按部件名精确过滤 |
| `hcb` | string | | 按 HCB 文件路径精确过滤 |
| `limit` | int | | 返回上限，默认 20，上限 100 |

**返回**

```json
{
  "results": [
    {
      "id": 78,
      "node": "sample_service",
      "service_name": "sample",
      "module_name": "libsample.z.so",
      "library": "system/lib/libsample.z.so",
      "component": "driver"
    }
  ],
  "total": 1
}
```
