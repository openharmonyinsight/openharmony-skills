# 进程故障模式（Process Fault） 触发索引

> 两级加载第一级：只读本表做扫描判定；条目触发条件命中后，到 [../15-process-fault.md](../15-process-fault.md) 读取该 `### ID` 条目详情（大文件可用 Read offset/limit 按锚点局部读）。

| ID | 故障模式 | 触发条件（可判定的代码/设计特征） |
|---|---|---|
| P-01a | 进程崩溃（Crash） | 代码存在空指针解引用、数组越界、除零、无限递归等崩溃形态；JS 层异常无兜底；服务崩溃后无 appspawn/SAMGR 保活与自动重启 |
| P-01b | 进程异常退出（Abnormal Exit） | 进程可被外部 kill（SIGKILL/SIGTERM）或资源耗尽被系统杀死；SIGTERM 无清理处理；关键服务未注册 OnRemoteDied 感知对端死亡 |
| P-01c | 进程启动失败（Start Failure） | 启动依赖其他服务就绪（system_server/servicemanager/surfaceflinger 等）而无依赖图与超时重试；启动路径可死锁或资源不足；关键服务无 fd/内存预算 |
| P-01d | 进程挂死（Hang / Deadlock） | 进程内存在 AB-BA 死锁、条件变量可能永不唤醒、IO 阻塞无超时、主线程死循环等挂死形态；无 watchdog 检测与自动恢复 |
| P-01e | 进程 D 状态（Uninterruptible Sleep） | IO/驱动等待与内核态等待使用不可中断模式（非可中断信号量）；D 状态进程无法 kill -9 且无监控告警 |
| P-01f | 进程 T 状态（Stopped / Traced） | 关键进程未屏蔽 SIGSTOP；可被 ptrace 附加且异常 detach 后无恢复；信号处理不健壮 |
| P-01g | 进程 Z 状态（Zombie） | 父进程创建子进程后不 wait/waitpid 回收；父进程可先崩溃而 init 未接管；无 PID 水位监控 |
| P-02a | 进程内存泄漏（Memory Leak） | malloc/new 与 free/delete 不配对、异常分支跳过释放、循环引用、JNI 全局引用未释放；无 PSS 监控告警 |
| P-02b | 线程泄漏（Thread Leak） | 线程创建后未 join/detach；线程池无上限增长；pthread_create 失败未处理；无线程数监控 |
| P-02c | 进程句柄泄漏（FD / Handle Leak） | open/socket/pipe 后异常分支跳过 close；fd 未 RAII（UniqueFd）封装；无 fd 上限监控与告警 |
| P-02d | 进程资源耗尽（Resource Exhaustion） | fork/PIPE/domain socket/shm/mq/线程可无限创建直至耗尽；无 cgroups/ulimit 配额与资源预留、耗尽降级 |
| P-03a | 线程崩溃（Thread Crash） | 线程内存在空指针/越界/除零/未捕获异常且无统一异常捕获；线程崩溃无隔离（直接终止进程） |
| P-03b | 线程挂死（Thread Hang） | 线程内存在死锁、无限等待、IO 无超时、死循环；无线程级超时与挂死检测恢复 |
| P-03c | 线程 D/T 状态 | 线程内存在不可中断 IO/驱动阻塞；可被 SIGSTOP 停止且无法终止恢复 |
| P-04a | Binder 通信超时 | 同步 Binder 调用无超时（如 5s）；对端挂死/线程池满/服务未启动时本端永久等待；未注册 OnRemoteDied |
| P-04b | Binder 通信延迟 | Binder 传输大数据未走 Ashmem；对端高负载场景无耗时监控与异步替代；高并发线程竞争 |
| P-04c | Binder 通信异常（Parse Error / Transaction Failed） | Binder/Parcel 数据无长度与魔数校验；权限校验可失败无处理；对端崩溃后无降级（system_server 侧可触发 VM/watchdog 整机重启） |
| P-05a | Socket（TCP/UDP）接收超时 | socket 未设置 SO_RCVTIMEO；主线程可阻塞在 recv；对端不响应/弱网场景无重试降级 |
| P-05b | Socket 连接中断 | 长连接无心跳保活与断线重连；NAT 超时/防火墙/对端崩溃场景无状态监控与业务降级 |
| P-05c | Socket 初始化异常 | socket/bind 可因协议栈未就绪、权限不足、端口占用而失败且无重试与降级；端口固定分配 |
| P-05d | Socket 资源耗尽 | socket 可无限创建不关闭（泄漏）；无 RAII 封装、上限控制与 EMFILE 监控 |
