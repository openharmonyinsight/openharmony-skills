# 线程与并发故障模式 触发索引

> 两级加载第一级：只读本表做扫描判定；条目触发条件命中后，到 [../07-thread-concurrency.md](../07-thread-concurrency.md) 读取该 `### ID` 条目详情（大文件可用 Read offset/limit 按锚点局部读）。

| ID | 故障模式 | 触发条件（可判定的代码/设计特征） |
|---|---|---|
| T-01 | 线程泄漏 / 线程对象生命周期 | Thread 子类析构前未 NotifyExitSync/NotifyExitAsync；线程池销毁前未 Stop()；任务含无限循环；线程名超 16 字符被截断 |
| T-02 | 死锁 | 多锁获取顺序不一致；持锁期间调用外部接口/同步 IPC；读写锁升级（读锁内申请写锁） |
| T-03 | 数据竞争 | 共享变量无锁读写；容器遍历时并发修改；SafeMap 在写场景误用 operator[]（返回引用非线程安全） |
| T-04 | 条件变量 / 信号量误用 | wait 未用 while 循环检查谓词（虚假唤醒）；超时参数单位错误；post/wait 不配对；notify 时未持锁 |
| T-05 | Timer 使用陷阱 | 依赖 Timer 在系统休眠时唤醒（无法唤醒休眠系统）；相同 interval 多定时器复用 timerFd；Unregister 与回调触发存在临界竞争 |
| T-06 | 事件 / 消息循环积压与失控 | 事件生产快于消费且队列无上限；Handler 在生命周期结束后仍响应事件；IOEventReactor 的 Terminate 与 Run 线程退出顺序无约束 |
