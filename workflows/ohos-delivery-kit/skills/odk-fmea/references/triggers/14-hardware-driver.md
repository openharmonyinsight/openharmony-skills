# 硬件与驱动故障模式 触发索引

> 两级加载第一级：只读本表做扫描判定；条目触发条件命中后，到 [../14-hardware-driver.md](../14-hardware-driver.md) 读取该 `### ID` 条目详情（大文件可用 Read offset/limit 按锚点局部读）。

| ID | 故障模式 | 触发条件（可判定的代码/设计特征） |
|---|---|---|
| HW-01a | CPU 占用率过高 | 主线程或单线程存在无 sleep 的 while 轮询/计算循环；耗时任务未下沉 FFRT/工作线程；后台任务未用 cgroups 限流 |
| HW-01b | CPU 频率波动 / 下线 | 关键路径依赖 cpufreq 固定频率或 governor 策略；存在 CPU 核心热插拔/离线（cpu offline）场景；DVFS 调频失败无处理 |
| HW-01c | CPU 绑核异常 | 代码调用 sched_setaffinity/pthread_setaffinity_np 设置亲和性；affinity mask 未校验目标核心在线；关键线程绑定单核且无回退 |
| HW-01d | CPU 降频（Thermal Throttling） | 业务未订阅 thermal zone 降频事件做降级；持续高负载渲染/计算场景；实时路径依赖 CPU/GPU 固定频率预算 |
| HW-02a | GPU 频繁上下电 | GPU 电源 runtime PM 策略空闲超时过短且无 hysteresis 防抖；渲染路径频繁挂起/唤醒 GPU；关键渲染路径未保持 GPU 在线 |
| HW-02b | GPU 复位超时（硬复位/软复位/Job Timeout/Fence Timeout） | GPU 驱动含 job/fence timeout 处理路径；命令队列满或硬件无响应需 gpu reset；fence 信号释放依赖对端且无超时兜底 |
| HW-02c | GPU 内存页错误（GPU Page Fault） | GPU 经 ION/dma-buf 访问的内存与 CPU 侧释放生命周期解耦；释放前未等 GPU 空闲；显存分配失败无降级路径 |
| HW-02d | GPU 丢帧 | 渲染管线依赖 VSync/Choreographer 时序且存在丢帧类型（间隔/相同帧/升降序）；GPU 负载过高或管线阻塞；无 dropped frames 统计与动态降质 |
| HW-02e | GPU 绑核 / 降频 | 存在 GPU 多核绑核/调度策略代码；DFS 动态调频未预留性能预算；高负载游戏/视频渲染等高算力场景 |
| HW-03a | TP 未注册 / 重复注册 / 参数非法 | TP 驱动 probe 依赖 i2c/spi 通信成功；dts 中 TP 节点参数非法或重复注册 input 设备；开机流程阻塞于 TP 初始化 |
| HW-04a | 内存不足（Low Memory） | 低内存仅靠 LMK/lowmemorykiller 杀进程恢复；zram/swap 扇入扇出放大 IO；缓存/后台进程内存无上限预算 |
| HW-04b | 内存泄漏（Native / JS / 内核） | new/malloc 与 free 不配对、异常分支跳过释放；JS 闭包/监听器未移除；内核模块持续分配无回收（kmemleak 可检） |
| HW-04c | 内存耗尽（OOM） | 大内存分配前未预检查可用内存；分配失败无分块/压缩降级；依赖连续大内存（/proc/buddyinfo order-N）的路径 |
| HW-04d | 内存越界（Out-of-Bounds） | 数组/缓冲区读写缺下标与长度校验；用 strcpy/memcpy 拷入小缓冲区；递归无出口或大栈帧（栈溢出） |
| HW-04e | 内存碎片（Memory Fragmentation） | 长时间运行后申请连续大内存（buddyinfo 高阶分配失败）；分配/释放模式产生碎片；关键服务未用 CMA/预留内存 |
| HW-04f | 局部/全局引用溢出（JNI Reference Overflow） | Native/JS 互操作循环创建 JNI 或 napi 引用不释放；缺 DeleteLocalRef/napi_delete_reference 调用；全局引用数量无上限监控 |
| HW-05a | 存储初始化失败（EMMC / UFS / SSD） | bootloader/kernel 存储初始化（mmc_init、ufs_init）存在失败路径；eMMC/UFS 供电或总线通信异常场景；无 A/B 双分区恢复机制 |
| HW-05b | 存储读写失败 / 延迟（EMMC / UFS / SSD） | 存储读写路径含坏块/ECC 纠错与重试逻辑；I/O 无超时监控（/sys/block ioerr_cnt 可统计）；高低温或磨损致 eMMC/UFS 性能降级 |
| HW-05c | SCSI / UFS / SSD 协议错误 | UFS/SCSI 命令状态处理含 CHECK_CONDITION、BUSY、QUEUE_FULL 分支；存在 UFSHCD 复位状态机；文件系统转只读后无 fsck 修复 |
| HW-05d | MBR / 分区表读取失败 | 分区表解析依赖 MBR/GPT 单副本、无首尾双备份与校验和；kernel 报 invalid partition table 后无恢复模式；分区表存在被篡改风险 |
| HW-05e | IOWait 高 | 业务发起大量并发 I/O 或 sync 调用可能挂住；后台 IO 风暴未用 ionice 限速；关键路径走同步读写（vmstat iowait 高） |
| HW-06a | 数据库损坏 / 丢失 / 全零 / 事务不一致 | 写库未启用 WAL/事务，存在掉电半写风险；数据库文件无 CRC/校验和验证；损坏后无删除重建或备份恢复路径 |
| HW-06b | 分布式数据库数据不一致 | 分布式同步存在网络分区/时钟偏移场景；并发写同一记录缺版本号冲突解决（LWW/vector clock）；同步中断无完整性校验 |
| DRV-01 | EC hang 死 | 与嵌入式控制器 EC 交互的请求（键盘/鼠标、ACPI 命令）无超时重试；EC 无复位恢复机制；开机关键路径同步等待 EC 响应 |
| DRV-02 | 驱动崩溃 | 内核/HDF 驱动代码含空指针解引用、数组越界、除零；open/ioctl 深层路径缺边界校验；驱动内存/句柄资源耗尽无回收 |
| DRV-03 | 驱动丢失 | /dev 节点未创建或驱动 .ko 未加载、被卸载、文件损坏；上层不探测设备存在性直接调用；无驱动完整性校验与自动加载 |
| DRV-04 | 驱动加载延迟 | 驱动 probe/Init 依赖未就绪的服务或资源而阻塞等待；加载流程无超时保护；上层同步等待设备初始化完成才放行业务 |
| DRV-05 | 驱动管理进程异常 | devmgr/devhost 等 HDF 驱动管理进程可被 kill 或崩溃；无进程保活与状态保存恢复；设备管理消息通道无重连机制 |
| DRV-06 | 驱动模块加载达到上限 | insmod/加载驱动模块数量接近系统上限（如 tty 设备 64 个）；加载前无数量上限校验；超限后新设备 /dev 节点创建失败未处理 |
| DRV-07 | 驱动内存泄漏 | 驱动内 kmalloc/vmalloc 分配后异常分支不释放；设备反复 open/close 路径持续占用内存；无驱动内存水位监控回收 |
| DRV-08 | 加载恶意驱动 | 驱动加载缺签名验证；驱动文件来源无白名单校验；允许运行时 insmod 外部 .ko 模块 |
| DRV-09 | 驱动设备创建超过上限 | 设备节点创建无数量上限校验（如 tty 驱动最多 64 个）；存在批量注册设备的场景；超限创建 /dev 节点失败的分支未处理 |
