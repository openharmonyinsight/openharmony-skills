# 内存与资源泄漏故障模式

### M-01 Native 内存泄漏
- 典型原因：new/malloc 与 delete/free 不配对；异常分支跳过释放；循环中持续分配无释放点。
- 典型影响：进程 Native Heap（jemalloc）PSS/RSS 持续增长，最终触发系统资源管控被杀死（OOM）。
- 故障注入：循环触发可疑路径并用 hidumper --mem 采样对比；ASan/LeakWatcher 检测。
- 日志/Trace：HiAppEvent 资源泄漏事件（pss 超限）；hidumper 内存采样曲线；ASan leak 报告。
- 消减建议：RAII/智能指针统一管理；泄漏路径补释放；HiAppEvent 订阅泄漏事件并设阈值告警。

### M-02 JS 堆内存泄漏
- 典型原因：全局对象/单例误持引用、闭包捕获大对象、监听器/订阅未移除、定时器未销毁，导致 JS 对象无法被 GC。
- 典型影响：JS 引擎堆持续增长，触发 OOMError 或进程被系统杀死。
- 故障注入：反复进出页面/触发功能，取 Heap Snapshot 对比对象增长。
- 日志/Trace：HiAppEvent 资源泄漏事件；jscrash 的 OOMError；Heap Snapshot 中 dominator 分析。
- 消减建议：页面销毁时成对移除监听/定时器；大缓存设上限；用 WeakRef/弱引用持有缓存对象。

### M-03 RefBase 引用计数误用
- 典型原因：sptr 与裸指针混用（重复释放）；用裸指针构造 sptr 使生命周期脱离管控（应 MakeSptr）；栈上构造 RefBase 对象绕开智能指针；无 sptr 时单独使用 wptr（计数归 0 提前释放）；双向 sptr 循环引用。
- 典型影响：double-free/UAF 崩溃，或对象永不释放的内存泄漏。
- 故障注入：ASan 下跑对象创建/销毁路径；构造循环引用场景观察泄漏。
- 日志/Trace：RefBase Debug 追踪日志（引用计数打印）；ASan 报告。
- 消减建议：统一 MakeSptr 构造、堆上分配；环中一方改 wptr；开启 RefBase debug 跟踪定位计数异常。

### M-04 Ashmem / 映射资源泄漏
- 典型原因：智能指针只管理 Ashmem 对象本身，映射需手动 UnmapAshmem/CloseAshmem，漏配对即泄漏；MappedFile 同理。
- 典型影响：fd 与虚拟内存持续消耗，最终 EMFILE/ENOMEM，全进程连锁失败。
- 故障注入：循环 Create/Map 观察 fd 与 vss 增长。
- 日志/Trace：fd 统计 dump（/proc/pid/fd）；内存采样中 ashmem 区域增长。
- 消减建议：Map/Unmap、Create/Close 严格配对并 RAII 封装；UniqueFd 管理 fd。

### M-05 内存水位失控（无上限设计）
- 典型原因：缓存/队列/对象池无容量上限；大图/大数据常驻内存；未响应系统低内存通知。
- 典型影响：低内存场景被 LMK/系统杀死；同设备其他应用连锁受影响（系统服务内存失控影响整机）。
- 故障注入：灌入大数据压测至内存水位上限；模拟系统低内存广播。
- 日志/Trace：内核 oom 命令输出低内存状态；HiAppEvent 资源泄漏/内存事件；PSS 曲线。
- 消减建议：缓存设上限与 LRU 淘汰；订阅内存告警主动释放；关键服务设内存预算并埋点。
> 应用层 GC 行为导致的业务卡顿与冻屏、通知过载场景，参见 `12-app-framework.md` 中 AF-25 ~ AF-27。