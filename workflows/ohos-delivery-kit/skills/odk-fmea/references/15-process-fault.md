# 进程故障模式（Process Fault）

本类覆盖 **进程生命周期、线程状态、资源泄漏、Binder/Socket 通信、进程间交互** 等进程层故障，适用于涉及进程管理、服务保活、IPC 通信的模块分析。

---

## P-01 进程生命周期故障

### P-01a 进程崩溃（Crash）
- 典型原因：空指针解引用、数组越界、除零、栈溢出、非法指令；Native 层 SIGSEGV/SIGABRT；JS 层未捕获异常。
- 典型影响：服务退出（critical 服务由 appspawn/SAMGR 重新拉起）；应用闪退；虚拟机重新启动；黑屏/不亮屏/不灭屏/桌面无法滑动。
- 故障注入：构造空指针解引用；数组越界写；栈溢出（无限递归）；除零；kill -11 发送 SIGSEGV。
- 日志/Trace：faultlog 崩溃栈（SIGSEGV/SIGABRT）；tombstone；HiAppEvent 崩溃事件；appspawn 重启日志；watchdog 超时日志。
- 消减建议：空指针/边界检查；异常分支兜底；critical 服务由 appspawn 保活；崩溃后自动重启；崩溃信息上报与聚类。

### P-01b 进程异常退出（Abnormal Exit）
- 典型原因：被其他进程 kill（SIGKILL/SIGTERM）；遭遇严重错误主动 exit；资源耗尽（OOM）被系统杀死；信号处理不当。
- 典型影响：服务退出（critical 服务重新拉起）；应用崩溃；虚拟机重新启动；业务中断。
- 故障注入：kill -9 发送 SIGKILL；kill -15 发送 SIGTERM；构造资源耗尽场景；注入信号处理异常。
- 日志/Trace：进程退出信号日志（`WIFSIGNALED`、`WIFEXITED`）；appspawn 重启日志；OOM killer 日志；HiAppEvent 退出事件。
- 消减建议：关键服务注册 OnRemoteDied 感知对端死亡；退出前清理资源（SIGTERM 处理）；critical 服务保活；退出原因审计与上报。

### P-01c 进程启动失败（Start Failure）
- 典型原因：关键服务依赖未就绪（system_server、servicemanager、surfaceflinger、systemui）；启动路径死锁；资源不足（内存/句柄）；配置错误。
- 典型影响：开机后无法进入桌面；应用启动 ANR；系统服务不可用；级联故障。
- 故障注入：延迟/阻止依赖服务启动；构造资源不足场景（耗尽 fd/内存）；篡改启动配置；启动路径注入死锁。
- 日志/Trace：服务启动超时日志（`SystemAbility start timeout`）；启动依赖图日志；资源不足日志（`ENOMEM`、`EMFILE`）；ANR trace。
- 消减建议：服务启动依赖图管理（拓扑排序）；启动超时监控与重试；资源预留（关键服务 fd/内存预算）；启动路径异常降级。

### P-01d 进程挂死（Hang / Deadlock）
- 典型原因：死锁（mutex/semaphore 顺序错误）；无限等待（条件变量未唤醒）；IO 阻塞无超时；主线程死循环。
- 典型影响：应用无响应；黑屏/不亮屏/不灭屏/桌面无法滑动；虚拟机重新启动；只能长按电源键恢复。
- 故障注入：构造 AB-BA 死锁；条件变量永不唤醒；IO 操作注入无限延迟；主线程注入死循环。
- 日志/Trace：ANR trace（主线程阻塞栈）；watchdog 超时事件；线程 dump（`SIGUSR1` 触发）；HiAppEvent 冻屏事件。
- 消减建议：锁顺序一致性（全局锁层级）；超时等待（`pthread_cond_timedwait`）；IO 异步化与超时；watchdog 检测与自动恢复。

### P-01e 进程 D 状态（Uninterruptible Sleep）
- 典型原因：IO 操作阻塞（磁盘/网络）；驱动等待；信号量/互斥锁不可中断等待；内核态阻塞。
- 典型影响：应用无响应；无法被 kill -9 终止；系统资源被占用；watchdog 超时重启。
- 故障注入：构造不可中断 IO 阻塞；驱动注入阻塞；内核态信号量死锁。
- 日志/Trace：进程状态统计（`ps aux` 中 D 状态）；内核 IO 栈 trace；watchdog 超时日志；sysrq-t 线程 dump。
- 消减建议：IO 操作使用可中断模式；驱动超时保护；内核态使用可中断信号量；D 状态进程监控与告警。

### P-01f 进程 T 状态（Stopped / Traced）
- 典型原因：被 SIGSTOP 信号停止；被 ptrace 调试器附加；信号处理异常。
- 典型影响：应用无响应；进程被挂起；业务中断；调试器异常detach后可能无法恢复。
- 故障注入：发送 SIGSTOP；构造 ptrace 附加后异常退出；信号处理异常。
- 日志/Trace：进程状态统计（T 状态）；信号日志；ptrace 事件日志。
- 消减建议：关键进程屏蔽 SIGSTOP；ptrace 使用监控；信号处理健壮性；T 状态检测与恢复。

### P-01g 进程 Z 状态（Zombie）
- 典型原因：父进程未调用 wait/waitpid 回收子进程；父进程崩溃或挂死；init 进程未接管孤儿进程。
- 典型影响：PID 资源耗尽；进程表膨胀；系统无法创建新进程；fork 失败。
- 故障注入：创建大量子进程后父进程不 wait；父进程崩溃；观察僵尸进程积累。
- 日志/Trace：僵尸进程统计（`ps aux | grep Z`）；PID 耗尽日志（`fork failed`）；进程表监控。
- 消减建议：父进程注册 SIGCHLD 信号处理及时回收；使用 double-fork 避免僵尸；PID 监控与告警；init 进程接管机制。

---

## P-02 资源泄漏故障

### P-02a 进程内存泄漏（Memory Leak）
- 典型原因：malloc/new 后未 free/delete；异常分支跳过释放；循环引用；JNI 全局引用未释放；内核模块内存泄漏。
- 典型影响：服务导致低内存卡顿甚至重启；应用被 LMK 杀死闪退；系统可用内存持续下降。
- 故障注入：循环触发可疑分配路径；长时间运行后对比 PSS；构造内核模块泄漏。
- 日志/Trace：HiAppEvent 资源泄漏事件（pss 超限）；hidumper 内存采样；kmemleak 报告；faultlog。
- 消减建议：RAII/智能指针；异常分支兜底释放；内存泄漏检测工具（ASan/LeakWatcher）；kmemleak 内核检测；PSS 监控告警。

### P-02b 线程泄漏（Thread Leak）
- 典型原因：线程创建后未 join/detach；线程池无限增长；线程异常退出未清理；pthread_create 失败未处理。
- 典型影响：系统 PID 资源被消耗；线程上下文切换开销增加；线程内部逻辑对系统影响更大（如死锁）。
- 故障注入：循环创建线程不 join/detach；线程池任务队列无限增长；构造线程异常退出。
- 日志/Trace：线程数量统计（`/proc/pid/status` 中 Threads）；pthread_create 失败日志；线程 dump。
- 消减建议：线程池上限控制；线程生命周期管理（join/detach）；线程数量监控；线程异常退出处理。

### P-02c 进程句柄泄漏（FD / Handle Leak）
- 典型原因：open/socket/pipe 后未 close；异常分支跳过关闭；重复打开同一资源；文件描述符表无上限。
- 典型影响：服务重启甚至系统重启；应用 ANR（fd 耗尽导致 IO 失败）；EMFILE 错误；级联故障。
- 故障注入：循环 open 不 close；socket 创建不关闭；构造 fd 耗尽场景（`ulimit -n` 上限）。
- 日志/Trace：fd 数量统计（`/proc/pid/fd`）；EMFILE 错误日志；ANR trace；服务重启日志。
- 消减建议：fd 使用 RAII 封装（UniqueFd）；异常分支兜底 close；fd 上限监控与告警；fd 泄漏检测工具。

### P-02d 进程资源耗尽（Resource Exhaustion）
- 典型原因：fork 创建进程数直至上限；PIPE/domain socket/shm/mq 耗尽；线程数耗尽；内存耗尽。
- 典型影响：系统无法创建新进程/线程；IPC 失败；业务中断；级联故障。
- 故障注入：循环 fork 至上限；创建大量 PIPE/socket/shm；构造资源耗尽场景。
- 日志/Trace：资源耗尽错误（`EAGAIN`、`ENOMEM`、`EMFILE`）；系统资源统计（`/proc/sys/kernel`）；fork 失败日志。
- 消减建议：资源配额管理（cgroups/ulimit）；资源使用监控与告警；关键服务资源预留；资源耗尽降级。

---

## P-03 线程状态故障

### P-03a 线程崩溃（Thread Crash）
- 典型原因：线程内空指针、越界、除零、非法指令；未捕获异常；栈溢出。
- 典型影响：线程业务逻辑无法正常进行；应用/上层业务失败；进程可能崩溃。
- 故障注入：构造线程内空指针解引用；数组越界；栈溢出；未捕获异常。
- 日志/Trace：faultlog 崩溃栈（SIGSEGV）；线程崩溃日志；HiAppEvent 崩溃事件。
- 消减建议：线程内异常捕获；边界检查；线程崩溃监控与重启；线程隔离（线程崩溃不导致进程崩溃）。

### P-03b 线程挂死（Thread Hang）
- 典型原因：线程内死锁；无限等待；IO 阻塞；死循环。
- 典型影响：线程业务逻辑无法正常进行；所有应用 ANR（若为主线程）；资源占用。
- 故障注入：线程内注入死锁；条件变量永不唤醒；IO 无限延迟；死循环。
- 日志/Trace：线程 dump（`SIGUSR1`）；ANR trace；watchdog 超时日志。
- 消减建议：线程内超时机制；锁顺序一致性；IO 异步化；线程挂死检测与恢复。

### P-03c 线程 D/T 状态
- 典型原因：同进程 D/T 状态原因，但在线程层面；驱动阻塞；信号停止。
- 典型影响：线程业务逻辑无法正常进行；应用/上层业务失败；线程无法被终止。
- 故障注入：构造线程内不可中断 IO；发送 SIGSTOP 到线程。
- 日志/Trace：线程状态统计；内核 IO 栈 trace；信号日志。
- 消减建议：同进程 D/T 状态消减建议；线程级超时与恢复。

---

## P-04 Binder 通信故障（进程间）

### P-04a Binder 通信超时
- 典型原因：对端进程挂死/死锁/主线程阻塞；同步调用无超时；Binder 线程池满；对端服务未启动。
- 典型影响：物理按键/虚拟按键/UI 界面不响应；SystemUI 通知栏无响应；x 秒后整机重启恢复。
- 故障注入：对端进程注入死循环/睡眠；构造 Binder 线程池满；断开对端服务后触发同步 IPC。
- 日志/Trace：Binder 调用超时日志（`transaction timeout`）；对端进程堆栈 dump；watchdog 超时日志；ANR trace。
- 消减建议：同步 Binder 调用设超时（如 5s）；超时后转异步或降级；注册 OnRemoteDied 感知对端死亡；Binder 线程池监控。

### P-04b Binder 通信延迟
- 典型原因：对端进程负载高/处理慢；Binder 传输大数据；Binder 线程竞争；系统负载高。
- 典型影响：界面操作不响应；xx 秒后弹出应用 ANR 对话框；系统恢复正常。
- 故障注入：对端进程注入高负载；构造大数据传输；Binder 线程竞争。
- 日志/Trace：Binder 调用耗时统计；ANR 检测日志；系统负载统计。
- 消减建议：Binder 调用耗时监控；大数据走 Ashmem；异步调用替代同步；ANR 检测后恢复。

### P-04c Binder 通信异常（Parse Error / Transaction Failed）
- 典型原因：Binder 数据序列化/反序列化错误；Parcel 数据损坏；权限校验失败；对端进程崩溃。
- 典型影响：若为 system_server 发起，则 Binder 解析失败导致 VM 重启或 watchdog 整机重启；若为应用发起，则应用崩溃。
- 故障注入：篡改 Binder 数据；构造非法 Parcel；权限注入；kill 对端进程后触发 IPC。
- 日志/Trace：Binder 解析错误日志（`FAILED BINDER TRANSACTION`）；权限拒绝日志；VM 重启日志；watchdog 日志。
- 消减建议：Binder 数据校验（长度、魔数）；权限最小化；OnRemoteDied 注册；关键路径降级；VM 重启保护。

---

## P-05 Socket 通信故障

### P-05a Socket（TCP/UDP）接收超时
- 典型原因：网络延迟/丢包/断开；对端未响应；socket 未设置 SO_RCVTIMEO；主线程阻塞在 recv。
- 典型影响：业务线程阻塞；若为主线程则黑屏/系统复位；数据传输失败。
- 故障注入：断开网络；模拟高延迟；对端不响应；构造 socket 超时场景。
- 日志/Trace：socket 超时日志（`ETIMEDOUT`）；网络错误日志；ANR trace（主线程阻塞）；系统复位日志。
- 消减建议：socket 设置接收超时（SO_RCVTIMEO）；超时后重试或降级；主线程不阻塞网络 IO；网络状态监控。

### P-05b Socket 连接中断
- 典型原因：网络断开、对端崩溃、防火墙阻断、NAT 超时、心跳丢失。
- 典型影响：业务中断；数据丢失；连接状态不一致；系统黑屏/复位（若主线程阻塞）。
- 故障注入：断开网络；kill 对端进程；防火墙阻断；NAT 超时模拟。
- 日志/Trace：socket 断开日志（`ECONNRESET`、`EPIPE`）；心跳超时日志；网络状态日志。
- 消减建议：心跳机制保活；断线重连；连接状态监控；业务层断线降级；主线程不依赖网络状态。

### P-05c Socket 初始化异常
- 典型原因：网络协议栈未就绪、权限不足、端口被占用、地址绑定失败、资源耗尽。
- 典型影响：业务异常（如指纹功能异常、WiFi 热点切换不可用）；功能初始化失败。
- 故障注入：网络协议栈未启动时创建 socket；权限注入；端口占用；资源耗尽。
- 日志/Trace：socket 创建失败日志（`socket failed`、`bind failed`）；权限拒绝日志；资源耗尽日志。
- 消减建议：socket 创建失败重试；权限预校验；端口动态分配；资源预留；初始化失败降级。

### P-05d Socket 资源耗尽
- 典型原因：无限创建 socket 直至资源耗尽；socket 泄漏不关闭；重复释放不存在的 socket。
- 典型影响：无法创建新连接；业务失败；系统资源耗尽；级联故障。
- 故障注入：循环创建 socket 不关闭；释放已关闭/不存在的 socket；构造资源耗尽。
- 日志/Trace：socket 数量统计（`/proc/pid/fd` 中 socket）；EMFILE 错误；资源耗尽日志。
- 消减建议：socket 使用 RAII 封装；上限控制；泄漏检测；资源监控与告警。
