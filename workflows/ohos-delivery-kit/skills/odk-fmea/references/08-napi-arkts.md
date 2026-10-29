# NAPI / ArkTS 边界故障模式

### N-01 napi_env 缓存与跨线程使用
- 典型原因：深层调用拿不到 env 而直接缓存；env 退出（ArkTS 线程销毁）后未感知，use-after-free；env 与 ArkTS 线程强绑定，跨线程使用有多线程安全问题。
- 典型影响：运行一段时间后偶发崩溃（UAF），现网高发难复现。
- 故障注入：env 销毁后触发使用路径；多线程检测开关下跑全量用例。
- 日志/Trace：`current napi interface cannot run in multi-thread` ERROR 日志；crash UAF 栈。
- 消减建议：不缓存 env，逐层传递；必须缓存时用 napi_add_env_cleanup_hook 感知退出；开发期打开多线程检测开关。

### N-02 napi_value 出 scope 使用 / 缓存
- 典型原因：napi_value 生命周期限于 handle scope，出 scope 继续使用（use-after-scope）；初始化时缓存 method 的 napi_value，后期 typeof 结果异常。
- 典型影响：对象被 GC 后访问，偶发崩溃或数据错乱。
- 故障注入：强制 GC 后调用缓存对象。
- 日志/Trace：jscrash `Obj is not a valid object`。
- 消减建议：长期持有用 napi_create_reference/napi_get_reference_value；scope 内使用。

### N-03 napi_ref / 资源未删除泄漏
- 典型原因：napi_create_reference 后未 napi_delete_reference（JS 对象永远无法 GC）；napi_add_env_cleanup_hook 重复注册同 key 或未注册先删（`AddCleanupHook Failed`/`RemoveCleanupHook Failed`）。
- 典型影响：JS 堆泄漏持续增长至 OOM。
- 故障注入：循环创建引用观察堆增长。
- 日志/Trace：Heap Snapshot 中对象只增不减；cleanup hook 失败 ERROR 日志。
- 消减建议：create/delete 配对（析构或 cleanup hook 中删）；key 唯一性管理。

### N-04 Handle Scope 配对错误
- 典型原因：napi_open_handle_scope 只开不关；未按相反顺序关闭；native 方法返回前未关闭所有 scope（含条件分支提前 return）。
- 典型影响：scope 内对象无法回收（泄漏）或嵌套错乱崩溃。
- 故障注入：审查所有 return 分支；循环调用观察内存。
- 日志/Trace：内存增长；引擎告警日志。
- 消减建议：RAII 封装 scope；方法单一出口保证关闭。

### N-05 线程安全函数（TSFN）管理失当
- 典型原因：napi_acquire_threadsafe_function 与 release 计数不匹配；napi_call_threadsafe_function 在 abort/closing 后仍调用；tsfn 未 release 导致 env 无法退出。
- 典型影响：内存泄漏；调用崩溃；进程退出挂起。
- 故障注入：release 后再 call；观察退出流程。
- 日志/Trace：napi_call_threadsafe_function 返回 napi_closing；泄漏检测事件。
- 消减建议：acquire/release 计数配对；调用前判断 env/tsfn 状态。

### N-06 跨线程调用 ArkTS 接口
- 典型原因：C++ 子线程直接调用 ArkTS 方法或直接操作 JS 对象（ArkTS 方法只能在 env 所在 ArkTS 线程执行）。
- 典型影响：多线程竞争崩溃；部分维测接口直接中断进程。
- 故障注入：子线程触发 JS 调用路径（检测开关下立即暴露）。
- 日志/Trace：`current napi interface cannot run in multi-thread`。
- 消减建议：通过 TSFN/异步任务把调用抛回 ArkTS 线程；禁止子线程同步调 JS。

### N-07 napi_status 返回值未检查
- 典型原因：napi_* 调用返回值不判（默认成功），错误被吞后在错误对象上继续操作。
- 典型影响：延迟崩溃，现场与根因分离，定位困难。
- 故障注入：注入 napi 调用失败（非法参数）。
- 日志/Trace：首个失败点无日志，崩溃点在远处。
- 消减建议：宏封装 NAPI_CALL 检查并提前返回；错误分支补日志。

### N-08 Promise / async 异常未捕获
- 典型原因：Promise rejection 无 catch；async 函数内异常未处理；定时器回调中对象已销毁。
- 典型影响：unhandled rejection 触发 JS Crash 进程崩溃。
- 故障注入：注入 rejection 路径；销毁对象后触发异步回调。
- 日志/Trace：jscrash（Reason 字段）；Promise 异步栈（开启后可见完整链）。
- 消减建议：全局 errorManager.on('error') 兜底；Promise 链路末端统一 catch；异步回调判活对象。

### N-09 ArkTS 状态管理装饰器误用
- 典型原因：@Consume 无匹配 @Provide（missing @Provide）；@Link 数据源非状态变量或类型不一致（is not callable）；@Provide 重复声明未加 allowOverride（duplicate @Provide property）。
- 典型影响：应用闪退（jscrash）。
- 故障注入：构造缺失/类型不匹配的状态绑定。
- 日志/Trace：jscrash 对应报错信息。
- 消减建议：组件树审查 @Provide/@Consume 配对；@Link 数据源类型一致性检查；重写显式声明 allowOverride。

### N-10 XComponent / Native 资源生命周期
- 典型原因：OH_NativeXComponent_RegisterCallback 注册的回调对象被提前释放（裸指针保存于 XComponentPattern）；OH_NativeXComponent 对象销毁后仍调用接口（UAF）。
- 典型影响：SIGSEGV 崩溃，栈顶在 libace 的 OnSurfaceDestroyed 等回调。
- 故障注入：onSurfaceDestroy 后调用相关接口。
- 日志/Trace：cppcrash 栈含 XComponentPattern::OnSurfaceDestroyed，#00 帧 pc 为异常地址。
- 消减建议：回调对象保活到 onSurfaceDestroy 执行完；销毁后置空并禁止再调用。
