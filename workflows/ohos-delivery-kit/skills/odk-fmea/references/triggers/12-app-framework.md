# 应用框架与业务可靠性故障模式（APP 层） 触发索引

> 两级加载第一级：只读本表做扫描判定；条目触发条件命中后，到 [../12-app-framework.md](../12-app-framework.md) 读取该 `### ID` 条目详情（大文件可用 Read offset/limit 按锚点局部读）。

| ID | 故障模式 | 触发条件（可判定的代码/设计特征） |
|---|---|---|
| AF-01 | UIAbility onCreate 超时 | onCreate/onWindowStageCreate 内执行同步 IO（文件/Preferences/数据库读取）或同步 IPC；大对象初始化未用 taskpool 异步化；启动路径无耗时埋点 |
| AF-02 | UIAbility onForeground 前台化超时 | onForeground 中执行大量数据反序列化或复杂 UI 重绘；回调内发起同步网络请求/IO；前后台切换路径未做轻量化 |
| AF-03 | 后台切前台现场恢复超时 | 后台切前台时重建 XComponent/Surface、重连服务或重载数据；处理 onTrimMemory 低内存回收后的全量现场恢复；重建路径无超时保护 |
| AF-04 | UIAbility onBackground 超时 | onBackground 中执行同步数据持久化或同步资源释放；回调内发起同步 IPC 通知；落盘未走异步路径 |
| AF-05 | 退后台资源释放超时 | 退后台路径集中执行大量资源释放与同步写文件（fsync）；同步注销服务；与 onBackground 耗时叠加且前后台路径未解耦 |
| AF-06 | UIAbility onDestroy 超时 | onDestroy 中同步关闭数据库、释放全局对象；阻塞式线程 join 等待线程退出；销毁路径无超时保护或存在循环引用 |
| AF-07 | ServiceExtensionAbility onCreate / onRequest 超时 | ServiceExtensionAbility 的 onCreate/onRequest 主线程执行同步初始化（加载 so、创建线程池、同步网络请求）；onRequest 内处理复杂业务逻辑；启动路径无超时降级 |
| AF-08 | ServiceExtensionAbility onConnect 超时 | onConnect 中创建远程接口对象依赖其他 SA 启动或同步 IPC 等待；对端未就绪时无超时重试；未返回降级 stub |
| AF-09 | ServiceExtensionAbility onDisconnect 超时 | onDisconnect 中同步释放资源或同步通知对端；等待异步任务完成；释放逻辑与销毁路径耦合且无超时保护 |
| AF-10 | ServiceExtensionAbility onDestroy 超时 | ServiceExtensionAbility 的 onDestroy 中同步关闭连接或同步写状态；等待后台线程结束；fd/线程等资源未异步清理 |
| AF-11 | CES 订阅者过载（CES Subscriber Overload） | 通过 commonEvent.subscribe 注册订阅者数量接近上限（>250）；系统公共事件风暴时订阅者全量触发；进程内业务事件未用 emitter 替代 |
| AF-12 | 有序公共事件处理超时（Ordered CES Event Timeout） | 订阅有序（ordered）公共事件；onReceiveEvent 内执行同步耗时操作；业务未移入 taskpool 且未设执行时限 |
| AF-13 | 公共事件订阅泄露（Subscription Leak） | 动态 subscribe 后无 unsubscribe 生命周期配对（onDestroy/onBackground 处未取消）；反复创建销毁 UIAbility 致订阅累积；Native 侧订阅对象未释放 |
| AF-14 | CES 事件异步处理超时（Async CES Event Timeout） | onReceiveEvent 将耗时业务投递 taskpool 异步执行；未在时限内向系统反馈处理完成；无超时兜底机制 |
| AF-15 | 透明窗口（Transparent Window / TWIN） | 窗口 alpha/visibility 设为透明或不可见却覆盖全屏并接收 touch 事件；touchable 属性与业务可见状态不同步；透明层覆盖交互区域 |
| AF-16 | 显示事件丢失 / 丢帧冻屏（Display Event Lost） | 主线程绘制路径存在 sleep/同步 IPC 阻塞；VSync 信号丢失未处理；与 render_service 帧率脱节导致长时间无帧上屏 |
| AF-17 | 多模输入分发超时（Multimodal Input Dispatch Timeout） | 应用窗口接收多模输入分发但主线程阻塞未按时消费；无焦点窗口仍接收输入（焦点配对缺失）；无输入事件优先处理机制 |
| AF-18 | DataShareExtensionAbility 启动超时 | DataShareExtensionAbility 随进程启动；onCreate 中执行打开数据库、加载文件或网络请求等同步初始化；无超时保护 |
| AF-19 | DataShare 数据库操作超时 | 主线程直接调用 DataShareHelper 查询/更新；数据量大或数据库锁竞争场景未走 taskpool 异步；无索引优化与事务粒度控制 |
| AF-20 | Binder 线程池满（Binder Threads Exhausted） | 循环发起异步 IPC 不等待回调结果释放线程；Binder 线程创建后泄漏未释放；并发调用无上限控制 |
| AF-21 | Binder Buffer 满（Binder Buffer Full） | 经 Binder 事务传输接近 1MB 的大数据；未走 Ashmem/共享内存或分片传输；存在 buffer 泄漏/碎片化场景 |
| AF-22 | Binder 对端卡死（Binder Peer Deadlock） | 业务使用同步 IPC 且无超时保护；未注册 OnRemoteDied 感知对端死亡；对端服务死锁/崩溃时本端主线程永久等待 |
| AF-23 | 单事件卡死（Single Event Block） | 主线程 EventRunner 事件处理函数存在死循环/同步 IO/同步 IPC；事件处理无时限监控；耗时任务未移 taskpool/工作线程 |
| AF-24 | 事件积压卡死（Event Accumulation Block） | 高频向主线程投递轻量事件且消费慢于生产；事件队列深度无上限；无过期事件丢弃/合并批处理策略 |
| AF-25 | 频繁 GC（Frequent GC） | 热路径循环快速分配/释放小对象（内存抖动）；频繁分配大对象且无对象池复用；低内存设备上 GC 频率异常升高 |
| AF-26 | GC 卡死 / 全线程暂停冻屏（GC SuspendAll Deadlock / Freeze） | NAPI 长循环不让出线程致不进安全点；终结队列 FinalizationRegistry/WeakRef 回调堆积；SuspendAll 长时间等待业务线程 |
| AF-27 | 通知过载（Notification Overload） | 高频调用通知 publish 发送状态栏/弹窗通知且无速率限制与去重；通知携带大图片/长文本无大小上限；无通知队列深度控制 |
| AF-28 | 多实例 UIAbility 创建失败 | 多实例应用（浏览器/文管类）反复 startAbility 创建同 entry UIAbility；创建路径无内存预检查；无创建失败降级与超时监控 |
| AF-29 | 多 Tab 页创建失败 | 单 UIAbility 内反复创建/销毁 Tab 页（如浏览器 Tab/Web 实例）；内存不足时无预检查；渲染异常无隔离导致创建崩溃 |
| AF-30 | Touch 事件 & HomeKey & RecentKey 事件消费超时 | 窗口子系统侧处理 Touch/HomeKey/RecentKey 事件；未调用或超时调用多模事件消费反馈接口；触发多模超时检测上报 |
| AF-31 | Touch 事件消费超时 | ArkUI 子系统侧 Touch 事件处理耗时过长；未调用多模事件消费反馈接口即返回；多模超时检测上报超时事件 |
| AF-32 | BackKey 事件消费超时 | 窗口子系统侧 BackKey 按键处理耗时过长；未调用或超时调用多模事件消费反馈接口；触发多模超时检测上报 |
| AF-33 | 支持全局手势识别的特殊的触摸屏事件分发超时 | 触摸屏事件分发与全局手势识别处理竞争同一事件流；手势处理耗时过长；Input 事件分发无优先级与超时恢复机制 |
| AF-34 | 鸿蒙 APP 语音对话 | 按键/小艺唤醒后语音输入处理链路含垂域语料识别与网络请求；语音处理耗时过长；无网络状态检测与超时监控 |
| AF-35 | USB 设备无法识别 | 鼠标/摄像头/音箱/键盘等外设 USB 插入后枚举失败场景（控制器/驱动/供电异常）；无热插拔检测与驱动自动加载；无识别超时与用户提示 |
| AF-36 | USB 协议协商异常 | PC 与外设 USB 连接后协议速率协商降级（3.0 被识别为 2.0）场景；无协商校验与失败重试；摄像头卡屏/键鼠卡顿等性能劣化无降级 |
