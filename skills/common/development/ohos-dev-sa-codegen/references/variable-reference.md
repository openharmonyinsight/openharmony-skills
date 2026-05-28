# 变量替换速查表

生成代码时使用以下变量：

## 用户提供（必填）

| 变量 | 示例值 | 说明 |
|------|--------|------|
| `{SaName}` | `IdlDemoService` / `DemoService` | SA 类名（PascalCase），用户提供 |
| `{SA_ID}` | `1499` | SA ID 数字（> 0），用户提供 |
| `{process_name}` | `idl_demo_service` / `demo_service` | 进程名，用户提供 |
| `{subsystem_name}` | `systemabilitymgr` | 子系统名，用户提供 |
| `{part_name}` | `safwk` | 部件名，用户提供 |
| `{runOnCreate}` | `true` / `false` | 启动方式，用户提供 |
| `{distributed}` | `false` | 是否支持分布式，用户提供 |
| `{log_domain}` | `0xD003F00` | HiLog domain ID（格式 `0xD00XXXX`），用户提供 |

## 自动派生（禁止用户填写）

| 变量 | 派生规则 | 示例 |
|------|----------|------|
| `{sa_name}` | `{SaName}` 转 snake_case | `idl_demo_service` / `demo_service` |
| `{SA_NAME}` | `{SaName}` 转 UPPER_SNAKE_CASE | `IDL_DEMO_SERVICE` |
| `{sa_id}` | 同 `{SA_ID}` | `1499` |
| `{ondemand}` | `{runOnCreate}` 取反 | `false` / `true` |
| `{HEADER_GUARD}` | 自动生成 | `IDL_DEMO_SERVICE_H` |
| `{IHEADER_GUARD}` | 接口头文件 guard | `OHOS_IDEMOSERVICE_H` |
| `{PROXY_HEADER_GUARD}` | Proxy 头文件 guard | `OHOS_DEMOSERVICEPROXY_H` |
| `{STUB_HEADER_GUARD}` | Stub 头文件 guard | `OHOS_DEMOSERVICESTUB_H` |
| `{SA_HEADER_GUARD}` | SA 头文件 guard | `DEMO_SERVICE_H` |
