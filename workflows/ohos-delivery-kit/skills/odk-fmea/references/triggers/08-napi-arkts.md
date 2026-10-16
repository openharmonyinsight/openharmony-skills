# NAPI / ArkTS 边界故障模式 触发索引

> 两级加载第一级：只读本表做扫描判定；条目触发条件命中后，到 [../08-napi-arkts.md](../08-napi-arkts.md) 读取该 `### ID` 条目详情（大文件可用 Read offset/limit 按锚点局部读）。

| ID | 故障模式 | 触发条件（可判定的代码/设计特征） |
|---|---|---|
| N-01 | napi_env 缓存与跨线程使用 | 深层调用缓存 napi_env 复用（未逐层传递）；未用 napi_add_env_cleanup_hook 感知 env 退出；env 跨线程使用 |
| N-02 | napi_value 出 scope 使用 / 缓存 | napi_value 出 handle scope 后继续使用；初始化时缓存 method 的 napi_value 而非 napi_create_reference |
| N-03 | napi_ref / 资源未删除泄漏 | napi_create_reference 后无 napi_delete_reference 配对；cleanup hook 重复注册同 key 或未注册先删 |
| N-04 | Handle Scope 配对错误 | napi_open_handle_scope 在条件分支提前 return 时未关；嵌套 scope 未按相反顺序关闭；无 RAII 封装 |
| N-05 | 线程安全函数（TSFN）管理失当 | napi_acquire_threadsafe_function 与 release 计数不匹配；abort/closing 后仍 call；tsfn 未 release 致 env 无法退出 |
| N-06 | 跨线程调用 ArkTS 接口 | C++ 子线程直接调用 ArkTS 方法或操作 JS 对象（未通过 TSFN/异步任务抛回 ArkTS 线程） |
| N-07 | napi_status 返回值未检查 | napi_* 调用无 NAPI_CALL 宏检查返回值（默认成功，错误被吞后在错误对象上继续操作） |
| N-08 | Promise / async 异常未捕获 | Promise rejection 链路无末端 catch；async 内异常未处理；定时器/异步回调不判对象存活 |
| N-09 | ArkTS 状态管理装饰器误用 | @Consume 无匹配 @Provide；@Link 数据源非状态变量或类型不一致；@Provide 重写未加 allowOverride |
| N-10 | XComponent / Native 资源生命周期 | OH_NativeXComponent_RegisterCallback 回调对象以裸指针保存可被提前释放；XComponent 销毁后仍调用其接口 |
