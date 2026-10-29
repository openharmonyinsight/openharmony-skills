# 虚拟化故障模式（Virtualization / Container） 触发索引

> 两级加载第一级：只读本表做扫描判定；条目触发条件命中后，到 [../17-virtualization.md](../17-virtualization.md) 读取该 `### ID` 条目详情（大文件可用 Read offset/limit 按锚点局部读）。

| ID | 故障模式 | 触发条件（可判定的代码/设计特征） |
|---|---|---|
| VM-01a | 虚拟机异常销毁（VM Abnormal Destruction） | 业务运行在虚拟机/容器（卓易通、出境易类）内且虚拟机进程可被 kill 或因宿主机资源不足被回收；销毁前无数据持久化与宿主机实时同步、无自动重建 |
| VM-01b | 虚拟机异常挂死（VM Hang） | 虚拟机内部存在死锁/IO 无限延迟形态；宿主机 CPU 可抢占；无虚拟机 watchdog 与挂死检测自动恢复 |
| VM-01c | 虚拟机异常停止（VM Abnormal Stop） | 虚拟机内存在 data abort、非法指令、内存访问错误路径；异常后无数据校验与自动重启 |
| VM-01d | 虚拟机启动或创建失败（VM Start/Create Failure） | 启动依赖镜像完整性、宿主机资源、配置与依赖服务；无镜像校验、资源预检查、就绪检测与启动失败降级（备用镜像/提示） |
| VM-01e | 虚拟机负载过高（VM Overload） | 虚拟机内可运行压测/CPU/内存/IO 密集任务；无 cgroups 资源配额、过载限流与宿主机资源隔离 |
| VM-02a | 容器通讯异常（Container Communication Failure） | 容器内外经 veth/bridge/iptables 交互；网络命名空间隔离或虚拟网卡可故障；无网络健康检查、就绪检测与通讯超时重试 |
| VM-02b | 容器驱动异常（Container Driver Failure） | 容器经虚拟化驱动访问硬件；驱动与内核版本可不兼容、资源可耗尽；无驱动版本校验与崩溃自动恢复 |
| VM-02c | 容器镜像异常（Container Image Failure） | 镜像可损坏/下载中断/校验失败/层缺失；无 SHA256 完整性校验、断点续传、缓存备份与启动失败降级 |
| VM-03a | 多进程/线程并发访问同一段静态共享内存（Shared Memory Concurrent Access） | 跨进程/线程共享内存读写无同步机制（mutex/sem/原子操作）或锁粒度错误 |
| VM-03b | 重复释放静态共享内存（Double Free Shared Memory） | 共享内存可被多进程/线程重复释放；无引用计数、释放后标记与所有权校验 |
| VM-03c | 释放后再次使用静态共享内存（Use-After-Free Shared Memory） | 共享内存释放后其他进程仍持有指针访问；无生命周期引用计数、释放后置空与访问前有效性校验 |
| VM-03d | 创建动态有名共享内存失败（Dynamic Named Shared Memory Creation Failure） | shm_open/mmap 可因物理内存耗尽、名称冲突、权限不足、配额限制失败；无资源预检查、名称唯一性校验与失败降级 |
| VM-04a | vNotify 通道资源耗尽（vNotify Channel Exhaustion） | 循环创建 vNotify 通道且不关闭或配额不足；无通道上限控制、复用与泄漏检测 |
| VM-04b | uapp 进程异常退出后 vNotify 通道未清理（vNotify Channel Leak on uapp Exit） | host 侧 uapp 进程创建多个 vNotify 通道；进程异常退出无自动清理与通道生命周期关联 |
| VM-05a | Host 时钟跳变（Host Clock Jump） | 业务依赖绝对时间且 Host 时钟可因 NTP/手动修改/RTC/迁移跳变；定时器未用 CLOCK_MONOTONIC；无跳变检测告警 |
| VM-06a | Guest 发送到 Host 的中断丢失（Guest-to-Host Interrupt Loss） | 虚拟化层中断注入/路由可失败或被风暴淹没；无中断丢失检测与重发机制 |
| VM-06b | Guest 频繁发送 Host 中断（Guest Interrupt Storm） | Guest 内驱动异常可产生中断风暴；无中断聚合（coalescing）、频率限制与限流 |
| VM-06c | Host 频繁发送 Host/Guest 中断（Host Interrupt Storm） | Host 侧设备驱动异常可产生频繁中断；无中断聚合、限流与 Host/Guest 中断隔离 |
| VM-06d | Guest 不处理 Host 中断（Guest Ignores Host Interrupt） | Guest 侧中断处理程序未注册或被屏蔽、转发可失败；无注册校验、转发监控与超时重发 |
| VM-06e | Guest 处理中断时发生异常（Guest Interrupt Handler Exception） | Guest 中断处理程序内存在空指针/越界/死锁/栈溢出风险；无异常处理、栈深保护与崩溃后自动恢复 |
