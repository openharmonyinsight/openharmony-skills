# 应用框架与业务可靠性故障模式（APP 层）

本类覆盖 **UIAbility/ExtensionAbility 生命周期、公共事件、窗口与输入、DataShare、IPC/Binder 业务层、事件队列、方舟 GC 业务层、系统资源过载、多实例/多 Tab、鸿蒙 APP 事件处理、南向设备 USB** 等应用框架层故障（合并自原 12-app-business-reliability 与 20-ability-lifecycle，生命周期超时重复条目已去重）。生命周期回调以 Stage 模型（UIAbility：onCreate/onWindowStageCreate/onForeground/onBackground/onDestroy；ServiceExtensionAbility：onCreate/onRequest/onConnect/onDisconnect/onDestroy）为主，FA 模型（PageAbility：onStart/onActive/onInactive/onBackground/onStop）可对应映射。

---

## A. 应用生命周期超时（Application Lifecycle Timeout）

### AF-01 UIAbility onCreate 超时
- 典型原因：onCreate/onWindowStageCreate 中执行同步 IO（文件/数据库/Preferences 读取）、同步 IPC、大对象初始化、阻塞式资源加载；主线程被长任务独占。
- 典型影响：应用无法启动，黑屏/白屏；触发 AppFreeze（THREAD_BLOCK_6S）后系统杀应用并弹窗。
- 故障注入：onCreate 中注入 sleep(5s)/死循环；慢速设备（低内存/低 CPU）压测。
- 日志/Trace：AppFreeze 日志（THREAD_BLOCK_3S→6S）；主线程堆栈停在业务初始化代码；HiAppEvent 冻屏事件。
- 消减建议：初始化异步化（taskpool/FFRT/@Concurrent）；懒加载/分段加载；关键路径加耗时埋点与拆分。

### AF-02 UIAbility onForeground 前台化超时
- 典型原因：onForeground 中恢复状态过重（大量数据反序列化、重绘复杂 UI、同步网络请求）；窗口焦点切换时执行耗时操作。
- 典型影响：应用无法前台化或切换失败，黑屏/白屏；AppFreeze 弹窗；用户体验劣化。
- 故障注入：onForeground 注入耗时计算；切换前后台高频压测。
- 日志/Trace：AppFreeze trace 主线程堆栈；前后台切换超时检测事件；HiAppEvent 冻屏事件。
- 消减建议：状态恢复轻量化；UI 与数据分离（数据预加载、UI 异步刷新）；避免在 onForeground 中做网络/IO。

### AF-03 后台切前台现场恢复超时
- 典型原因：从后台切回前台时重建资源（重建 XComponent/Surface、重连服务、重载数据）耗时过长；被系统低内存回收（onTrimMemory）后恢复现场过重。
- 典型影响：应用切回前台卡死或黑屏；用户感知"闪退"或"假死"。
- 故障注入：后台强杀/低内存回收后恢复路径注入延迟；低内存场景触发重建。
- 日志/Trace：生命周期回调超时日志；AppFreeze 事件；HiSysEvent 应用状态切换事件。
- 消减建议：快速保存/恢复状态（onSaveState/wantParams 轻量化）；后台切前台路径预加载关键资源；重建路径设超时保护。

### AF-04 UIAbility onBackground 超时
- 典型原因：onBackground 中执行同步数据保存、同步释放资源、同步 IPC 通知；被阻塞等待对端响应。
- 典型影响：应用切后台时 AppFreeze；影响下一个应用启动时序（窗口切换卡顿）。
- 故障注入：onBackground 中注入同步 IPC 阻塞/数据库慢查询。
- 日志/Trace：AppFreeze 检测日志；主线程堆栈停在 onBackground 业务代码。
- 消减建议：onBackground 只做轻量标记，异步完成持久化；释放资源走异步路径；避免同步 IPC。

### AF-05 退后台资源释放超时
- 典型原因：退后台后执行大量资源释放、同步写文件、同步注销服务；与 onBackground 耗时叠加。
- 典型影响：应用切后台 AppFreeze；系统回收资源延迟；后台任务异常。
- 故障注入：退后台路径注入文件同步写入/fsync 延迟。
- 日志/Trace：AppFreeze 检测日志；后台生命周期超时事件。
- 消减建议：资源释放异步化；后台路径与前台路径解耦；减少退后台路径同步操作。

### AF-06 UIAbility onDestroy 超时
- 典型原因：onDestroy 中执行同步销毁（关闭数据库、释放全局对象、等待线程退出）；死锁或线程未响应。
- 典型影响：应用退出时 AppFreeze；进程残留；资源未释放导致泄漏。
- 故障注入：onDestroy 注入线程 join 超时/死锁；循环引用导致无法销毁。
- 日志/Trace：AppFreeze 检测日志；进程退出超时事件；资源泄漏事件（线程/内存未释放）。
- 消减建议：销毁路径设超时保护；线程退出用异步通知而非阻塞 join；全局资源走 RAII/智能指针。

### AF-07 ServiceExtensionAbility onCreate / onRequest 超时
- 典型原因：ServiceExtensionAbility 启动时主线程执行同步初始化（加载 so、创建线程池、同步网络请求）；onRequest 中处理复杂逻辑。
- 典型影响：服务启动 AppFreeze；依赖该服务的功能不可用；系统服务启动超时可能导致开机失败。
- 故障注入：onCreate/onRequest 注入 sleep/死循环；慢速设备启动压测。
- 日志/Trace：AppFreeze 检测日志；服务启动超时事件；SystemAbility 启动超时看门狗。
- 消减建议：服务初始化异步化；延迟加载非关键依赖；启动路径加超时与降级。

### AF-08 ServiceExtensionAbility onConnect 超时
- 典型原因：onConnect 中创建远程接口对象耗时过长（依赖其他 SA 启动、同步 IPC 等待）；对端未就绪。
- 典型影响：连接服务接口 AppFreeze；客户端无法获取服务句柄（connectServiceExtensionAbility 失败），功能静默失效。
- 故障注入：onConnect 中注入依赖服务延迟返回；对端进程未启动时触发连接。
- 日志/Trace：AppFreeze 检测日志；服务连接超时事件；IPC 调用失败 errcode。
- 消减建议：onConnect 只做句柄组装，依赖预初始化；连接设超时与重试；对端未就绪时返回降级 stub。

### AF-09 ServiceExtensionAbility onDisconnect 超时
- 典型原因：onDisconnect 中同步释放资源、同步通知对端、等待异步任务完成；与销毁逻辑耦合。
- 典型影响：服务退出时断开连接 AppFreeze；资源释放不完整导致泄漏。
- 故障注入：onDisconnect 注入资源释放延迟/同步 IPC 阻塞。
- 日志/Trace：AppFreeze 检测日志；服务生命周期超时事件。
- 消减建议：断开连接异步化；资源释放与生命周期解耦；断开路径设超时保护。

### AF-10 ServiceExtensionAbility onDestroy 超时
- 典型原因：onDestroy 中同步关闭连接、同步写状态、等待后台线程结束；与 UIAbility onDestroy 类似。
- 典型影响：服务退出 AppFreeze；服务进程残留；系统资源（端口、fd、线程）泄漏。
- 故障注入：onDestroy 注入线程未退出/数据库关闭延迟。
- 日志/Trace：AppFreeze 检测日志；进程退出超时；资源泄漏事件。
- 消减建议：服务销毁异步清理；后台任务独立生命周期；销毁超时强制终止。

---

## B. 公共事件系统故障（CES，Common Event Service）

### AF-11 CES 订阅者过载（CES Subscriber Overload）
- 典型原因：应用注册过多静态/动态公共事件订阅者（>250 个）；系统公共事件风暴时全部触发，主线程被事件处理独占。
- 典型影响：事件处理卡顿和 AppFreeze；超过系统阈值被资源管控直接杀应用闪退。
- 故障注入：循环订阅公共事件至上限；模拟系统公共事件风暴触发全量订阅者。
- 日志/Trace：AppFreeze 检测日志；资源管控杀应用事件（HiAppEvent）；订阅数量审计日志。
- 消减建议：合并同类事件（一个订阅者处理多 event）；动态订阅按需启用；应用内事件用 emitter 替代全局公共事件；订阅数量监控告警。

### AF-12 有序公共事件处理超时（Ordered CES Event Timeout）
- 典型原因：有序公共事件订阅者串行执行，某一订阅者处理耗时过长；onReceiveEvent 中执行同步操作。
- 典型影响：后续订阅者无法处理；应用界面滑动无响应；返回键按下不能弹起；桌面/最近任务键能响应（系统按键不受应用 AppFreeze 影响）。
- 故障注入：有序公共事件订阅者中注入 sleep/死循环；构造高优先级订阅者阻塞。
- 日志/Trace：AppFreeze 检测日志（公共事件类型）；有序事件分发超时事件；主线程堆栈停在 onReceiveEvent。
- 消减建议：onReceiveEvent 只做轻量转发，业务逻辑移 taskpool 异步线程；有序事件订阅者设执行时限；非必要不订阅有序事件。

### AF-13 公共事件订阅泄露（Subscription Leak）
- 典型原因：动态订阅后未在生命周期结束时 unsubscribe（如 UIAbility 销毁时未取消订阅）；上下文泄漏导致重复订阅。
- 典型影响：订阅数量超上限被系统杀应用闪退；Native 侧泄露导致卡顿、OOM 闪退。
- 故障注入：反复创建/销毁 UIAbility 且订阅不取消，观察订阅者数量增长；内存泄漏检测。
- 日志/Trace：AppFreeze 检测日志；资源管控杀应用事件；Heap Snapshot 中订阅者对象增长。
- 消减建议：subscribe/unsubscribe 生命周期配对（onCreate/onDestroy 或 onForeground/onBackground）；进程内事件用 emitter；订阅数量审计与告警。

### AF-14 CES 事件异步处理超时（Async CES Event Timeout）
- 典型原因：onReceiveEvent 中将耗时操作投递到 taskpool 异步执行，但未在时限内向系统反馈处理完成；公共事件无响应检测以处理完成为标志。
- 典型影响：公共事件 AppFreeze；主线程堆栈卡在事件循环等待（epoll_wait）；应用被杀。
- 故障注入：异步任务中注入超长延迟且永不反馈完成；构造异步任务死锁。
- 日志/Trace：AppFreeze 日志（公共事件类型）；主线程堆栈停在事件循环；异步处理超时事件。
- 消减建议：异步操作严格管理完成反馈生命周期；超时兜底机制；耗时业务与事件接收解耦。

---

## C. 窗口与输入系统（Window & Input System）

### AF-15 透明窗口（Transparent Window / TWIN）
- 典型原因：应用窗口透明或不可见但覆盖全屏，接收输入事件却不响应；窗口属性设置异常（touchable 属性未正确设置但内容透明）。
- 典型影响：用户无法滑动切换界面；桌面/最近任务键能响应（系统级）；返回键可能无响应；应用假死。
- 故障注入：设置窗口透明覆盖全屏；注入窗口属性异常。
- 日志/Trace：透明窗口检测事件；窗口属性审计日志（alpha/visibility/focusable）。
- 消减建议：窗口可见性状态与业务状态严格同步；透明窗口不覆盖交互区域；透明窗口检测触发后自动恢复（杀应用/重置窗口）。

### AF-16 显示事件丢失 / 丢帧冻屏（Display Event Lost）
- 典型原因：应用主线程卡住或 VSync 信号丢失，导致绘制请求未处理；render_service 渲染服务与应用绘制管道脱节。
- 典型影响：应用界面无响应但按键能响应（输入事件到达但无帧绘制）；显示事件丢失触发冻屏。
- 故障注入：主线程注入 sleep 阻塞绘制；构造 VSync 丢失场景。
- 日志/Trace：冻屏检测日志；VSync 事件统计；render_service 帧率掉零事件。
- 消减建议：主线程绘制路径设超时保护；VSync 丢失检测与自动恢复；冻屏检测后强制刷新或杀应用恢复。

### AF-17 多模输入分发超时（Multimodal Input Dispatch Timeout）
- 典型原因：多模输入子系统分发输入事件到应用窗口，应用主线程未在时限内响应（无焦点窗口、主线程阻塞、窗口未就绪）。
- 典型影响：物理按键/虚拟按键/UI 界面不响应；超时后系统触发应用强制恢复或整机恢复。
- 故障注入：主线程注入阻塞使输入事件无法消费；构造无焦点窗口接收输入场景。
- 日志/Trace：Watchdog 检测机制；窗口无响应检测（APPEYE_FWB_FREEZE 类事件）；多模输入分发超时事件；按键事件丢弃日志。
- 消减建议：主线程保持响应（输入事件优先处理）；窗口焦点管理严格配对；分发超时后系统级恢复。

---

## D. 数据共享（DataShare）

### AF-18 DataShareExtensionAbility 启动超时
- 典型原因：DataShareExtensionAbility 随进程启动，onCreate 中执行同步初始化（数据库打开、文件加载、网络请求）；主线程被阻塞。
- 典型影响：应用启动 AppFreeze；黑屏；依赖该数据共享服务的应用无法启动。
- 故障注入：onCreate 注入 sleep/死循环；慢速设备启动压测。
- 日志/Trace：Watchdog 检测日志；DataShare 启动超时事件；AppFreeze trace 停在 onCreate。
- 消减建议：onCreate 只做极简初始化，业务延迟加载；数据库/文件访问异步化；启动路径加超时保护。

### AF-19 DataShare 数据库操作超时
- 典型原因：主线程直接执行 DataShareHelper 查询/更新，数据量大或数据库锁竞争导致耗时；未使用异步查询。
- 典型影响：主线程 AppFreeze；数据库操作阻塞窗口绘制和输入响应。
- 故障注入：构造大数据量表/并发写冲突；主线程注入慢查询。
- 日志/Trace：AppFreeze 检测日志；数据库操作耗时统计；SQL 慢查询日志。
- 消减建议：数据库操作移异步线程（taskpool/FFRT）；主线程只读轻量缓存；数据库索引优化；事务粒度控制。

---

## E. IPC 与 Binder 业务层故障（Binder Business Layer）

> 与 `03-ipc.md`（IPC 底层通用故障）互补：03-ipc.md 关注 OnRemoteDied/序列化/权限等代码层缺陷，本类关注 Binder 资源耗尽与对端卡死的业务影响。

### AF-20 Binder 线程池满（Binder Threads Exhausted）
- 典型原因：应用或系统服务创建大量 Binder 线程且未释放；并发 IPC 请求过多无上限；线程泄漏。
- 典型影响：Binder 线程被占满，IPC 通信异常；应用无法启动或切换；无法滑动和切换界面；AppFreeze。
- 故障注入：循环发起异步 IPC 不等待结果；构造线程泄漏场景观察 Binder 线程增长。
- 日志/Trace：AppFreeze 检测日志；Binder 线程统计 dump（/sys/kernel/debug/binder）；IPC 调用失败 errcode。
- 消减建议：Binder 调用并发度上限控制；异步 IPC 结果必须回调释放线程；线程泄漏检测与告警。

### AF-21 Binder Buffer 满（Binder Buffer Full）
- 典型原因：大数据传输未走 Ashmem/共享内存，多次写入 Binder 事务 buffer（~1MB）；Buffer 泄漏或碎片化。
- 典型影响：Binder 通信组包失败；IPC 通信异常；应用无法启动/切换或闪退；界面操作不响应。
- 故障注入：循环传递接近 1MB 边界的数据；构造 Buffer 碎片化场景。
- 日志/Trace：AppFreeze 检测日志；Binder 事务失败日志（TransactionTooLarge/NO_MEMORY）；buffer 统计。
- 消减建议：大数据走 Ashmem/共享内存；批量数据分片传输；Binder buffer 使用监控与告警。

### AF-22 Binder 对端卡死（Binder Peer Deadlock）
- 典型原因：对端进程主线程死锁或处理耗时过长；同步 IPC 调用后永远等待；对端服务未启动或已崩溃未感知。
- 典型影响：Binder 通信异常；应用功能不可用；若卡死主线程则触发 AppFreeze。
- 故障注入：对端服务注入死循环/死锁；kill 对端后触发同步 IPC。
- 日志/Trace：AppFreeze 检测日志；Binder 调用超时事件；OnRemoteDied 回调日志。
- 消减建议：同步 IPC 设超时保护；注册 OnRemoteDied 感知对端死亡；关键路径改异步调用；对端卡死检测后主动断开连接。

---

## F. 事件队列故障（EventRunner / 主线程事件循环）

### AF-23 单事件卡死（Single Event Block）
- 典型原因：主线程 EventRunner 事件循环中单个事件处理耗时过长（死循环、同步 IO、同步 IPC）；事件处理无超时机制。
- 典型影响：主线程事件循环卡死；应用无响应；触发 AppFreeze 弹窗。
- 故障注入：向主线程投递耗时事件（sleep/死循环）；慢速设备压测。
- 日志/Trace：AppFreeze 检测日志；主线程堆栈停在事件处理代码；事件耗时统计。
- 消减建议：主线程事件处理设时限（事件循环监控）；耗时任务移 taskpool/工作线程；事件处理埋点与超时告警。

### AF-24 事件积压卡死（Event Accumulation Block）
- 典型原因：事件产生快于消费，队列积压 >300 条；单条事件处理时间小于 AppFreeze 检测时间，但累积效应导致主线程长期忙碌；无队列深度上限。
- 典型影响：应用无响应；无 AppFreeze 弹框（因为单条事件未超时，系统无法检测）；用户感知"随机卡顿"。
- 故障注入：高频向主线程投递轻量事件，观察队列深度与响应延迟；构造事件风暴。
- 日志/Trace：事件队列深度统计；事件处理延迟曲线；AppFreeze 事件（若系统支持累积检测）。
- 消减建议：主线程队列设深度上限（丢弃/合并过期事件）；高频事件合并批处理；工作线程预处理后再投递 UI；队列深度监控告警。

---

## G. 内存与方舟 GC 业务层故障（ArkCompiler GC Business Layer）

> 与 `06-memory-resource-leak.md`（内存泄漏通用模式）互补：06 关注泄漏根因（new/delete 不配对、引用计数），本类关注 GC 行为导致的业务卡顿。

### AF-25 频繁 GC（Frequent GC）
- 典型原因：应用内存消耗过快，对象创建速率高于回收速率；内存碎片导致频繁触发 GC；大对象分配频繁。
- 典型影响：GC 频繁触发导致主线程卡顿；应用 AppFreeze；帧率下降。
- 故障注入：循环快速分配/释放小对象；构造内存碎片场景；低内存设备压测。
- 日志/Trace：AppFreeze 检测日志；ArkCompiler GC 日志（GC 类型与频率）；HiAppEvent 内存事件；SmartPerf/HiTrace GC 段。
- 消减建议：对象池复用减少分配；大对象缓存与复用；内存水位监控与主动释放；避免内存抖动代码模式。

### AF-26 GC 卡死 / 全线程暂停冻屏（GC SuspendAll Deadlock / Freeze）
- 典型原因：方舟运行时执行全线程暂停（SuspendAll）时卡住（等待线程到达安全点失败）；GC 线程与业务线程死锁；终结队列（FinalizationRegistry/WeakRef 回调）过长。
- 典型影响：虚拟机卡死冻屏；应用 AppFreeze；整机 UI 无响应（若影响系统进程）。
- 故障注入：构造线程不进入安全点场景（如 NAPI 长循环不让出）；终结队列注入大量对象。
- 日志/Trace：AppFreeze 检测日志；GC 日志中 SuspendAll 耗时异常；虚拟机线程 dump；冻屏事件。
- 消减建议：NAPI 长循环中主动让出/分片处理；减少终结回调依赖（显式关闭资源）；GC 参数调优；虚拟机线程状态监控。

---

## H. 系统资源过载（System Resource Overload）

### AF-27 通知过载（Notification Overload）
- 典型原因：应用高频发送通知（状态栏、弹窗、响铃），无发送速率限制；通知携带大图片/长文本占用内存。
- 典型影响：SystemUI OOM；系统卡顿；应用 AppFreeze；SystemUI 进程重启；通知服务（ANS）崩溃。
- 故障注入：循环发送大量通知（含大图片）；观察 SystemUI 内存与响应。
- 日志/Trace：资源管控事件（SystemUI OOM）；AppFreeze 检测日志；通知服务统计；HiAppEvent 资源泄漏事件。
- 消减建议：通知发送速率限制（令牌桶/去重）；通知内容大小上限；大图片压缩/缩略图；通知队列深度控制。

## I. 多实例与多 Tab 创建（Multi-Instance / Multi-Tab）

### AF-28 多实例 UIAbility 创建失败
- 典型原因：浏览器、文管等多实例创建过程中崩溃；同一个 UIAbility 反复创建中失败；内存不足；资源泄漏。
- 典型影响：创建失败不影响后续的 UIAbility 的创建；用户体验劣化；功能不可用。
- 故障注入：反复创建 UIAbility；内存不足时创建；资源泄漏；观察创建行为。
- 日志/Trace：Ability 创建日志；崩溃日志；内存日志；资源泄漏日志；AppFreeze 检测日志。
- 消减建议：UIAbility 创建资源管理；内存预检查；资源泄漏检测；创建失败降级；创建超时监控；崩溃后自动恢复。

### AF-29 多 Tab 页创建失败
- 典型原因：浏览器单实例内部创建 Tab 页崩溃；同一个 UIAbility 的 Tab 页反复创建中失败；内存不足；渲染异常。
- 典型影响：创建失败不影响后续的 Tab 页的创建；用户体验劣化；功能不可用。
- 故障注入：反复创建 Tab 页；内存不足时创建；渲染异常；观察创建行为。
- 日志/Trace：Tab 页创建日志；崩溃日志；内存日志；渲染日志；资源泄漏日志。
- 消减建议：Tab 页资源管理；内存预检查；渲染异常隔离；创建失败降级；创建超时监控；崩溃后自动恢复。

---

## J. 鸿蒙 APP 事件处理

### AF-30 Touch 事件 & HomeKey & RecentKey 事件消费超时
- 典型原因：窗口子系统调用多模事件消费反馈接口超时或未调用消费反馈接口；多模超时检测上报超时事件。
- 典型影响：窗口子系统调用多模事件消费反馈接口超时或未调用消费反馈接口，能够被检测且有恢复方案。
- 故障注入：事件处理注入延迟；不调用消费反馈接口；多模超时检测；观察系统行为。
- 日志/Trace：多模事件日志；消费反馈日志；AppFreeze 检测日志；超时日志；恢复日志。
- 消减建议：事件处理超时监控；消费反馈接口强制调用；多模超时检测；超时后恢复机制；事件队列管理；稳定性测试。

### AF-31 Touch 事件消费超时
- 典型原因：ArkUI 子系统调用多模事件消费反馈接口超时或未调用消费反馈接口；多模超时检测上报超时事件。
- 典型影响：ArkUI 子系统调用多模事件消费反馈接口超时或未调用消费反馈接口，能够被检测且有恢复方案。
- 故障注入：Touch 事件处理注入延迟；不调用消费反馈接口；多模超时检测；观察系统行为。
- 日志/Trace：ArkUI 事件日志；消费反馈日志；AppFreeze 检测日志；超时日志；恢复日志。
- 消减建议：Touch 事件处理超时监控；消费反馈接口强制调用；多模超时检测；超时后恢复机制；事件队列管理；稳定性测试。

### AF-32 BackKey 事件消费超时
- 典型原因：窗口子系统调用多模事件消费反馈接口超时或未调用消费反馈接口；多模超时检测上报超时事件。
- 典型影响：窗口子系统调用多模事件消费反馈接口超时或未调用消费反馈接口，能够被检测且有恢复方案。
- 故障注入：BackKey 事件处理注入延迟；不调用消费反馈接口；多模超时检测；观察系统行为。
- 日志/Trace：BackKey 事件日志；消费反馈日志；AppFreeze 检测日志；超时日志；恢复日志。
- 消减建议：BackKey 事件处理超时监控；消费反馈接口强制调用；多模超时检测；超时后恢复机制；事件队列管理；稳定性测试。

### AF-33 支持全局手势识别的特殊的触摸屏事件分发超时
- 典型原因：多模超时检测上报超时事件；全局手势识别与事件分发冲突；手势处理耗时过长。
- 典型影响：Input 输入超时或者无响应，能够被检测且有恢复方案。
- 故障注入：全局手势处理注入延迟；事件分发冲突；多模超时检测；观察系统行为。
- 日志/Trace：手势事件日志；事件分发日志；AppFreeze 检测日志；超时日志；恢复日志。
- 消减建议：手势处理超时监控；事件分发优先级；多模超时检测；超时后恢复机制；手势与事件隔离；稳定性测试。

### AF-34 鸿蒙 APP 语音对话
- 典型原因：按键、小艺等方式唤醒设备后输入语音；语音处理耗时过长；网络延迟。
- 典型影响：反复输入不同垂域语音语料，功能正常，系统无异常。
- 故障注入：语音输入不同垂域语料；网络延迟；语音处理异常；观察系统行为。
- 日志/Trace：语音日志；APR 数据；DevicesTest 检测语料输出结果；功能状态日志；错误日志。
- 消减建议：语音处理超时监控；网络状态检测；语料覆盖测试；功能状态管理；错误处理；稳定性测试。

## K. 南向设备（PC）USB 故障

### AF-35 USB 设备无法识别
- 典型原因：鼠标、摄像头、显示器、音箱、键盘等外设插入 USB 后无法识别；USB 控制器故障；驱动异常；供电不足。
- 典型影响：外设无法使用；业务中断；用户体验劣化。
- 故障注入：插入无法识别的外设；USB 控制器故障；驱动异常；供电不足；观察系统行为。
- 日志/Trace：USB 设备日志；驱动日志；供电日志；错误日志；设备管理日志。
- 消减建议：USB 设备热插拔检测；驱动自动加载；供电监控；设备识别超时；错误提示用户；设备管理器。

### AF-36 USB 协议协商异常
- 典型原因：PC 和外设连接后，构造协议协商异常的情况，比如应该识别为 3.0，实际是 2.0；基于该故障模式验证摄像头通道是否会卡屏、鼠标是否卡顿、键盘是否响应慢、音箱声音是否破音。
- 典型影响：协议协商错误导致设备性能下降；功能异常；用户体验劣化。
- 故障注入：协议协商错误（3.0→2.0）；观察摄像头/鼠标/键盘/音箱行为。
- 日志/Trace：USB 协议日志；协商日志；设备性能日志；错误日志；功能状态日志。
- 消减建议：USB 协议协商校验；协商失败重试；协商超时保护；性能监控；功能降级；错误提示用户；兼容性测试。
