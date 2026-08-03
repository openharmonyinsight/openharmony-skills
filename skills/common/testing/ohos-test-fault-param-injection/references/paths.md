# 参考文件（通用，跨仓适用）

本文件列出故障注入测试涉及的 OpenHarmony 通用机制与路径，按需查阅。SKILL.md 仅引用本文件，避免占用主上下文。

| 机制 | 路径 |
|------|------|
| watchdog 注册 | `base/hiviewdfx/hicollie/interfaces/native/innerkits/include/xcollie/xcollie.h`、`xcollie_define.h` |
| 参数 API（C++） | `init:libbegetutil` 的 `syspara/parameters.h`（`OHOS::system::GetIntParameter<T>`） |
| 参数 API（C） | `syspara/parameter.h`（`GetParameter`/`SetParameter`/`WatchParameter`） |
| 参数命名/DAC | 各仓 `param/*.para` + `param/*.para.dac`（如 `base/<repo>/services/<svc>/param/`） |
| 参数名长度/合法字符 | syspara `PARAM_NAME_LEN_MAX`（当前标准配置 96，`CheckParamName` 要求 <96，允许字母数字及 `.` `-` `@` `:` `_`） |
| 参数 API（设置） | `OHOS::system::SetParameter`（单次消费自清零用）；C 侧 `SetParameter` |
| selinux 前缀→label 映射 | `base/security/selinux_adapter/sepolicy/base/public/parameter_contexts` |
| 服务 selinux 域 | 各仓 `sepolicy/ohos_policy/<repo>/system/<domain>.te` + `.cfg` 的 `secon` 字段 |
| SA 启动配置 | `sa_profile/*.json`（SA ID） + `services/*/*.cfg`（进程/critical/secon） |
| critical 重拉/panic | `startup_init` 的 `ServiceReap`：`.cfg` `critical:[crashCount, crashTime]` 阈值内重复崩溃执行 `ExecReboot("panic")` 整机重启 |
| 关闭 selinux | `setenforce 0` / `getenforce`（设备级；首选定向 `debug_only(allow ...)`，setenforce 0 仅兜底） |

## watchdog flag 速查

| flag | 超时后行为 |
|------|-----------|
| `XCOLLIE_FLAG_LOG` | 仅打日志 + 生成快照，不杀进程 |
| `XCOLLIE_FLAG_RECOVERY` | **直接 kill 进程**（配合 init critical 重拉） |
| `XCOLLIE_FLAG_DEFAULT` | 执行所有回调 |
| `XCOLLIE_FLAG_NOOP` | 仅执行 caller 回调，无附加动作 |

注入前务必 `grep -n "XCOLLIE_FLAG" <service>.cpp` 确认目标函数的 flag——`LOG` 型注入 sleep 不会杀进程，只有含 `RECOVERY` 的才会触发崩溃恢复。
