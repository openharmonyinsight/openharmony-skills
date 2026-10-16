# 系统稳定性故障模式 触发索引

> 两级加载第一级：只读本表做扫描判定；条目触发条件命中后，到 [../18-system-stability.md](../18-system-stability.md) 读取该 `### ID` 条目详情（大文件可用 Read offset/limit 按锚点局部读）。

| ID | 故障模式 | 触发条件（可判定的代码/设计特征） |
|---|---|---|
| S-01a | 内核态死锁（Kernel Deadlock） | 内核态多处 spinlock/mutex/信号量以相反顺序获取构成 AB-BA；中断上下文与进程上下文竞争同一锁；lockdep 可报锁序不一致 |
| S-01b | 用户态死锁（User-space Deadlock） | 多线程以相反顺序加 mutex/semaphore；条件变量 wait 后存在永不 signal 的分支；跨进程锁未用 pthread_mutex_timedlock 设超时 |
| S-01c | 内核态死循环（Kernel Infinite Loop） | 内核线程或软中断路径存在条件恒真的 while/for；循环体内无 cond_resched 调度点；高优先级内核线程长循环无超时退出 |
| S-01d | 用户态死循环（User-space Infinite Loop） | 主线程或工作线程存在无超时退出的轮询/消息循环；循环内无 sleep/yield 让出 CPU；压测下 ANR trace 停在同一循环 |
| S-01e | 调度时间过长（Scheduling Latency） | 批量创建 CPU 密集线程无数量上限；实时任务 SCHED_FIFO 优先级配置过高；CPU 隔离/cgroup 亲和配置错误致 sched_latency 升高 |
| S-01f | 内核态线程泛滥（Kernel Thread Flooding） | 内核模块循环创建 kthread 无上限；workqueue 深度无限增长；线程数涨至 PID 耗尽且无配额监控 |
| S-01g | 原子上下文发生调度（Atomic Context Scheduling） | spinlock 持有区或原子上下文调用 msleep/kmalloc(GFP_KERNEL) 等可睡眠函数；panic 报 scheduling while atomic |
| S-01h | 中断上下文发生调度（Interrupt Context Scheduling） | 硬中断处理函数内调用 mutex/msleep 等可睡眠或阻塞函数；top-half 内触发调度切换；中断嵌套路径含睡眠调用 |
| S-02a | 中断处理超时（Interrupt Handler Timeout） | 中断 top-half 内执行 IO/复杂运算等耗时操作未移 tasklet/workqueue；高频中断风暴致处理积压；无中断耗时监控 |
| S-02b | 中断处理死循环（Interrupt Handler Infinite Loop） | 中断处理程序内循环条件恒真；中断状态寄存器清除遗漏致重复进入同一处理函数；中断计数陡增且单核 CPU 占满 |
| S-02c | 中断处理时异常（Interrupt Handler Exception） | 中断处理函数内空指针/越界/除零访问或引用已释放资源；hardirq 上下文大局部数组可致栈溢出；oops 栈顶落在中断处理 |
| S-02d | 软中断中任务切换（Softirq Context Scheduling） | softirq 处理函数内调用 msleep/mutex 等可睡眠函数；软中断上下文触发任务切换；panic 栈显示 softirq 上下文 |
| S-02e | 中断嵌套（Interrupt Nesting） | 中断优先级配置允许高优先级嵌套低优先级处理；处理程序入口未屏蔽同级中断；高频注入下嵌套深度与中断栈深无上限 |
| S-02f | 频繁软中断（Frequent Softirq） | 高频网络包/定时器/块设备事件触发 softirq；未启用 ksoftirqd 线程化分发；/proc/softirqs 计数陡增且 CPU 被占满 |
| S-03a | 挂载超出上限（Mount Limit Exceeded） | 循环执行 mount 挂载 tmpfs/fatfs/ext2fs 无次数上限；容器/虚拟机内批量挂载；/proc/mounts 条目逼近系统挂载上限 |
| S-03b | 强制卸载文件系统（Forced Unmount） | 文件读写未完成时调用 umount 强制卸载；目标含根目录、/dev、/sys、/proc 等关键挂载；卸载前未用 fuser/lsof 查占用 |
| S-03c | 格式化过程中异常终止（Format Abort） | mkfs/格式化执行路径可被 kill、ctrl+c 或掉电中断；格式化无事务化与进度保存；中断后无 fsck 校验与恢复 |
| S-03d | 反复格式化（Repeated Format） | 多线程或脚本循环对同一分区反复 format/mkfs；格式化无频率限制与审计；闪存写入磨损（SMART 计数）快速累积 |
| S-03e | 权限修改（Permission Modification） | 对业务目录或 /dev、/sys、/proc 执行 chmod 000 或非常规权限；依赖路径权限可被外部篡改；访问报 EACCES 无恢复机制 |
| S-03f | 系统重启后文件系统初始化（Post-Reboot FS Initialization） | 重启流程依赖 fsck/mount 自动修复而超级块或元数据已损坏；文件系统未启用 journal/checkpoint；失败无恢复模式兜底 |
| S-03g | 空间占满（Disk Full） | 自行挂载 tmpfs/fatfs/ext4 等文件系统后循环写入至满；日志膨胀、临时文件无轮转清理；写入侧未处理 ENOSPC 降级 |
| S-03h | 最大目录深度（Max Directory Depth） | 递归/循环 mkdir 创建超深层目录（ext4 上千层）；创建前无路径长度校验；目录遍历递归无栈深保护，报 ENAMETOOLONG |
| S-03i | inode 资源耗尽（Inode Exhaustion） | 批量创建海量小文件且临时文件不清理；df -i 显示 inode 耗尽而容量未满；文件创建报 No space left on device |
| S-03j | 软/硬链接超出上限（Link Limit Exceeded） | 循环创建硬/软链接无上限（超 ext4 65000 限制）；构造符号链接互指循环；路径解析无 max_symlinks 保护 |
| S-03k | 文件句柄耗尽（FD Exhaustion） | 循环 open 不 close 直至 fd 上限报 EMFILE/ENFILE；rlimit NOFILE 与系统文件句柄上限配置过低；/proc/pid/fd 持续增长 |
| S-03l | 超大文件（Oversized File） | dd/写入方式生成 1000M 以上超大文件；日志、数据库文件无大小上限与分片归档；大文件传输/备份路径无超时处理 |
| S-03m | 同名文件/目录（Name Collision） | 并发创建同名文件/目录未用 O_EXCL 原子创建；跨大小写敏感差异文件系统操作同名异大小写文件；未处理 EEXIST 即覆盖 |
| S-03n | 文件内容丢失（File Content Loss） | 文件写入过程中进程被 kill、文件被删或掉电；写后未 fsync 刷盘；未采用临时文件+rename 原子写与进度保存 |
| S-03o | 文件句柄泄露（FD Leak） | open 后的异常/提前返回分支跳过 close；fd 未用 RAII/UniqueFd 封装；长稳运行中 /proc/pid/fd 数量单调增长 |
| S-03p | IO 时延高（High IO Latency） | 大量并发 IO 或后台 IO 风暴（批量下载/备份/扫描）；无 IO 限速、异步化与优先级调度；iostat 时延陡增引发主线程 ANR |
| S-03q | 文件内容破坏（File Content Corruption） | 文件写入/传输后无 CRC/SHA256 校验即使用；存在掉电半写、篡改或位翻转可能；checksum failed 无拒绝与恢复流程 |
| S-03r | 元数据破坏（Metadata Corruption） | 直接写 ftl/a1/mtd0 等块设备破坏超级块或 inode 表；元数据无校验和与备份；损坏后 mount 失败且 fsck 不能自动修复 |
| S-03s | F2FS 特定故障 | 使用 f2fs 且 superblock/checkpoint/NAT/SIT/SSA 元数据区可被篡改或损坏；无 checkpoint 备份与 fsck.f2fs 自动修复 |
| S-03t | 分区故障（Partition Fault） | 分区出现挂载失败、umount busy、只读（read-only）、损坏或满等状态；挂载前无校验；异常状态无检测与恢复路径 |
| S-03u | 镜像故障（Image Fault） | HOTA/OTA 升级中掉电或中断致镜像写半；镜像加载无签名+哈希完整性校验；无 A/B 分区与恢复模式回滚，bootloader 引导失败 |
| S-03v | 磁盘满（Disk Full） | 循环写入致用户可见磁盘分区满；日志膨胀与大文件不清理；无磁盘配额、预留空间与 No space 优雅降级 |
| S-04a | 频繁进行数据库操作（Frequent DB Operations） | 高频循环执行数据库（SQLite/RDB）增删改查；无连接池、事务粒度过细；查询缺索引全表扫描；日志现 deadlock detected |
| S-05a | 权限类签名证书故障 | 签名证书过期、证书链不完整或被撤销仍调用受保护接口；URI 无权限；报 certificate expired/SecurityException；无 OCSP 检查 |
| S-06a | 反复进行视频播放（Repeated Video Playback） | 循环播放不同类型/大小视频文件的压测或业务；播放结束未调用 release/reset 释放解码器与句柄；无播放资源预检查 |
| S-06b | 反复进行分辨率切换（Repeated Resolution Switch） | 播放/投播过程中反复调用分辨率切换接口；切换无防抖节流与超时监控；资源不足时仍并发切换 |
| S-06c | 反复进行刷新率切换（Repeated Refresh Rate Switch） | 显示/播放过程中高频调用刷新率切换接口；切换与 VSync 无同步保护；无切换频率限制与失败降级 |
| S-06d | 媒体多实例并行（Media Multi-Instance Parallel） | 并发创建多个媒体播放/录制实例且无实例上限控制；超上限无优雅拒绝；实例间无资源隔离引发竞争 |
| S-06e | 媒体进程 crash（Media Process Crash） | 对媒体进程执行 kill 注入或进程异常退出后保活重启；崩溃后无资源清理、播放状态保存与自动恢复 |
| S-06f | 长时间运行（Long-time Running） | 媒体播放/录制 7x24 小时长稳或老化运行；PSS/句柄/IO 资源随时长累积泄漏；无定期清理与内存碎片整理 |
| S-06g | 资源不足（Resource Insufficient） | 低内存（内存水位紧张）、CPU/IO 高负载或存储空间不足下调用媒体功能；无资源预检查与低画质低帧率降级 |
| S-06h | 网络故障（Network Fault） | 流媒体路径遭遇断网/弱网/丢包/高延迟；网络服务进程被 kill；无缓存播放、断点续播与自动重连 |
| S-06i | 操作系统故障（OS Fault） | 注入内核 panic/系统挂死/异常重启后恢复媒体功能；重启后无播放状态保存与功能自检校验 |
| S-06j | 电源故障（Power Fault） | 播放/录制过程中掉电或电池耗尽；重新上电后无播放进度恢复；低电量时未主动保存状态 |
| S-06k | 媒体文件故障（Media File Fault） | 播放器直接打开损坏/不存在/不支持编码封装格式的文件；文件系统服务被 kill 或 fd 耗尽时调用媒体接口；无格式校验降级 |
| S-06l | 磁盘故障（Disk Fault） | 媒体读写路径遭遇磁盘不可读、写保护（read-only）或坏块（I/O error）；无磁盘错误检测与只读降级 |
| S-06m | 下游故障（Downstream Fault） | 媒体服务面对下游高并发或异常数据请求；解码器/渲染器注入故障；无请求限流、输入校验与服务熔断 |
| S-07a | 全屏 AOD 折叠开合状态组合切换 | 折叠屏设备开启全屏 AOD 长时挂机；反复折叠态/展开态组合切换；AOD 状态与折叠状态无同步和刷新保护 |
| S-08a | 硬件压力_反复掉电重启压测 | 设备运行业务中被反复掉电、重启、插拔的压测循环；不同器件断电次数无差异化标准；数据无定期保存与重启自检 |
| S-08b | 硬件压力_反复断电重启压测 | 高负载业务中循环执行整机/器件级断电重启压测；重启后无数据一致性校验与恢复机制 |
| S-08c | 软件老化可靠可用（Software Aging） | 设备 7x24 小时挂机运行业务的软件老化测试；内存/句柄/内存碎片随时长累积泄漏；无老化监控与老化后自动重启 |
| S-09a | 负向改进-休眠状态下折叠开合 | 设备休眠（suspend）状态下反复执行展开/悬停/折叠状态切换；唤醒后无状态恢复；休眠唤醒无超时监控 |
| S-09b | 负向改进-休眠状态下按住电源键同时折叠开合 | 休眠状态下按住电源键同时执行折叠/展开组合操作；电源键事件与折叠处理无互斥与按键队列管理；唤醒流程无优先级 |
| S-10a | 前台窗口负载（Foreground Window Load） | 前台创建 20 个以上窗口（含全遮挡/半遮挡）负载运行业务；无窗口数量上限与资源预检查；窗口泄漏无检测 |
| S-10b | 后台窗口负载（Background Window Load） | 后台创建 20 个以上窗口负载运行；后台窗口无冻结（不渲染）与内存/CPU 限制；无后台窗口清理策略 |
| S-11a | 反复调用功能入口/出口 | 循环调用功能/服务入口与出口（enable/disable、start/stop）；多实例并发与跨进程调用无锁与超时保护；无状态机管理 |
| S-11b | 反复进行横竖屏切换 | 功能使用中反复触发横竖屏切换；切换无防抖与资源预检查；低内存时切换无降级与状态保存恢复 |
| S-11c | 频繁休眠唤醒 | 功能使用中高频执行休眠唤醒与解锁亮灭屏循环；无休眠唤醒防抖与超时监控；唤醒后功能状态无恢复 |
| S-11d | 语音唤醒 | 开启语音唤醒功能并高频语音唤醒设备；高负载下唤醒无降级；唤醒后无功能状态恢复与功耗监控 |
| S-11e | 多用户切换 | 多用户场景频繁切换机主/隐私/子用户后即时发短信、拨打电话；切换无资源与数据隔离；切换后无状态恢复 |
| S-11f | 用户冻屏（User Freeze） | 第三方管家类应用（腾讯管家/360 等）高频触发 FWK 框架操作；FWK 模块存在死锁或主线程耗时操作；无死锁检测与冻屏恢复 |
| S-11g | 低存储空间（Low Storage） | 构造剩余存储低于 1G/3G 场景执行 monkey 与高负载测试；应用无存储预检查、缓存清理与低存储降级 |
| S-11h | 高 IO 读写操作（High IO） | OTG 高频读写 U 盘或应用商店批量下载更新构造高 IO 负载；无 IO 限速/异步化/优先级管理；高 IO 时无降级 |
| S-11i | AOD 模式 | 反复进入/退出 AOD 模式循环；进退出无资源管理与防抖；AOD 显示刷新与功耗无监控 |
| S-11j | GlobalAction 模式 | 遍历全部 GlobalAction 系统操作场景做压力测试；各场景无功能状态管理；高频连续触发无节流 |
| S-11k | 频繁多种解锁方式使用 | 设置指纹/人脸/数字多种解锁方式并交替组合压测；解锁失败无降级与超时监控；解锁资源无管理 |
| S-11l | 频繁视频通话和电话 | 视频通话中并发语音通话（或反向）多次并发；无并发通话限制与通话状态机管理；资源不足无降级与超时 |
| S-12a | 界面 UI | 长时间反复操作界面控件并进入/退出不同层级；无 UI 防抖与层级管理；长时操作无 ANR/Crash/黑白屏监控与泄漏检测 |
| S-12b | 多 APP 终端管理 | 10 台手机同时登入 APP 管理同一路由并并发操作界面；无并发连接上限与操作隔离；界面状态无同步 |
| S-12c | 多设备接入，APP 访问性能测试 | 路由接入 128 台以上有线/无线设备满载后反复操作 APP 界面；无设备接入上限；满载下界面无性能优化与资源监控 |
| S-13a | 发现连接（Discovery & Connection） | 设备发现覆盖主动/被动、首次/非首次、BLE/COAP 单一与混合协议；典型及最大组网规模下长时间测发现成功率 |
| S-13b | 数据传输（Data Transfer） | 双端长时间传输不同类型/大小/超大文件；反复本地/远端与虚拟设备切换；无分片、CRC/MD5 校验与超时重传 |
| S-13c | 数据同步（Data Synchronization） | 全量与实时数据同步并发大数据量；同步过程中反复断网、丢包；系统高负载下同步；无冲突解决、重传与高负载限速 |
| S-13d | 文件同步（File Synchronization） | 双端设备长时间添加/删除/修改不同类型文件并同步；大容量存储空间不足时仍同步；无空间预检查与暂停策略 |
| S-13e | 设备组网（Device Networking） | 组网反复连接/断开、最大规模单混组网、设备与进程多次重启后重新组网；双端反复亮灭屏；无组网上限与恢复机制 |
