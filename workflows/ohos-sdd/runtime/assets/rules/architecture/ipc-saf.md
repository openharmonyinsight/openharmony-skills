# Rule: IPC/SAF 通信

## Rule ID

OH-ARCH-IPC-SAF

## Applies To

- Feature Design
- Feature Spec
- Task Spec
- AI implementation
- Design / GB 基线审查
- GC 代码质量审查

适用于新增或修改 System Ability、跨进程接口、远端服务调用、Proxy/Stub、IPC 参数序列化和远端异常处理。

## Must

- 必须说明是否新增或复用 System Ability。
- 必须为新增 System Ability 定义注册、发现、生命周期和权限边界。
- 必须为跨进程接口定义清晰的接口契约、参数、返回值、错误码和超时策略。
- 必须处理远端对象为空、远端异常、序列化失败、权限不足和服务不可用。
- 必须避免在 IPC 调用路径执行长耗时操作，必要时采用异步回调、任务队列或通知机制。
- 必须记录 IPC 数据校验、错误日志和诊断方式。

## Must Not

- 禁止通过共享内存、全局变量或内部对象引用替代正式 IPC 契约。
- 禁止在 IPC 边界信任调用方输入。
- 禁止吞掉远端异常或返回无法定位的通用失败。
- 禁止在未声明权限和调用边界的情况下开放系统服务能力。
- 禁止在同步 IPC 路径中执行不可控耗时操作。

## Evidence

- SA profile、接口定义、Proxy/Stub 或等效通信契约。
- 权限、错误码、超时和异常处理说明。
- IPC 参数校验和序列化/反序列化说明。
- 单元测试、集成测试或故障注入结果。
- hilog/hidumper 诊断证据。

## Check

- 检查 SA 注册和发现路径是否完整。
- 检查跨进程接口是否具备参数校验、错误码和异常处理。
- 检查 IPC 调用是否有权限校验和超时/失败策略。
- 检查同步路径是否存在长耗时操作。
