# LiteOS-M/A内核组件详解

---

## 1. LiteOS-M内核（轻量系统）

### 1.1 定位与特点
- **面向MCU设备**: ARM Cortex-M系列、RISC-V MCU
- **最小RAM要求**: 128 KB
- **内核最小体积**: < 10 KB ROM（最小功能集）
- **标准配置体积**: < 20 KB ROM（含IPC组件）
- **源码规模**: 约17,000行C代码
- **调度方式**: 优先级抢占式 + 同优先级时间片轮转
- **优先级数量**: 32级（可配置）

### 1.2 架构分层

```
┌─────────────────────────────────────┐
│         应用层 (Application)          │
├─────────────────────────────────────┤
│    POSIX / CMSIS-RTOS2 接口层        │
├─────────────────────────────────────┤
│      内核抽象层 (KAL)                │
├──────────┬──────────────────────────┤
│ 扩展组件  │     最小功能集            │
│ ·信号量   │  ·任务管理               │
│ ·互斥锁   │  ·内存管理               │
│ ·消息队列  │  ·中断/异常管理           │
│ ·事件标志  │  ·调度器                 │
│ ·软件定时器│  ·系统时钟               │
├──────────┴──────────────────────────┤
│       BSP / HAL 硬件抽象层           │
├─────────────────────────────────────┤
│          硬件 (MCU)                  │
└─────────────────────────────────────┘
```

### 1.3 组件详细清单

**最小功能集（不可裁剪核心）**：

| 组件 | 功能描述 | 预估ROM | 预估RAM | 备注 |
|------|---------|---------|---------|------|
| 任务管理(Task) | 任务创建/删除/挂起/恢复、TCB管理、就绪队列 | ~2.5 KB | ~0.5 KB + N×TCB | TCB大小约400B/任务 |
| 调度器(Sched) | 优先级位图、上下文切换、时间片管理 | ~1.5 KB | ~200 B | 含PendSV处理 |
| 内存管理(Mem) | 动态内存分配(best-fit/buddy)、MemBox固定块 | ~1.5 KB | 堆大小可配 | 支持bestfit/little/membox三种算法 |
| 中断管理(Int) | 中断注册/注销、嵌套处理、向量表 | ~1.0 KB | ~100 B | 架构相关 |
| 异常管理(Fault) | HardFault/SVC/NMI处理、异常信息记录 | ~0.8 KB | ~200 B | 调试关键 |
| 系统时钟(Tick) | SysTick配置、tick计数、时间转换 | ~0.5 KB | ~50 B | 通常1ms tick |
| **小计** | | **~7.8 KB** | **~1.1 KB+** | 不含应用任务栈 |

**可选IPC组件（可按需裁剪）**：

| 组件 | 功能描述 | 预估ROM | 预估RAM | Kconfig宏 |
|------|---------|---------|---------|-----------|
| 信号量(Sem) | 计数信号量、PV操作、超时等待 | ~0.8 KB | N×SemCB | LOSCFG_BASE_IPC_SEM |
| 互斥锁(Mutex) | 互斥访问、优先级继承、死锁检测 | ~1.0 KB | N×MuxCB | LOSCFG_BASE_IPC_MUX |
| 消息队列(Queue) | FIFO消息传递、阻塞/非阻塞读写 | ~1.2 KB | N×QueueCB+缓冲 | LOSCFG_BASE_IPC_QUEUE |
| 事件标志(Event) | 事件组、AND/OR组合等待 | ~0.6 KB | N×EventCB | LOSCFG_BASE_IPC_EVENT |
| 软件定时器(Swtmr) | 单次/周期定时、回调执行 | ~1.0 KB | N×SwtmrCB+队列 | LOSCFG_BASE_CORE_SWTMR |
| **IPC小计** | | **~4.6 KB** | **取决于实例数** | 全部启用时 |

**扩展组件（按需启用）**：

| 组件 | 功能描述 | 预估ROM | 预估RAM | 备注 |
|------|---------|---------|---------|------|
| VFS文件系统 | 虚拟文件系统层、FAT/LittleFS支持 | ~5-15 KB | ~2-8 KB | 含底层FS驱动 |
| 网络协议栈(lwIP) | TCP/IP、UDP、DHCP、DNS | ~30-60 KB | ~20-50 KB | lwIP裁剪后 |
| HDF驱动框架 | 统一驱动模型、设备管理 | ~8-15 KB | ~3-5 KB | 轻量版HDF |
| POSIX接口适配 | pthread/socket/mqueue等 | ~3-8 KB | ~0.5-2 KB | 部分API |
| CMSIS-RTOS2 | ARM标准RTOS接口 | ~2-5 KB | ~0.3-1 KB | Cortex-M专用 |
| CPUP(CPU占用率) | 任务级CPU使用率统计 | ~0.5 KB | N×8B | 调测用 |
| 内核调测(Kernel Debug) | 日志、断言、backtrace | ~2-5 KB | ~1-3 KB | 发布版可裁 |

### 1.4 构建系统（GN配置方式）
- **构建工具**: GN + Ninja（非make menuconfig）
- **配置入口**: `kernel/liteos_m/Kconfig`
- **单板配置**: `device/<vendor>/<board>/Kconfig`
- **特性开关**: `target_config.h`中的`LOSCFG_*`宏
- **组件化构建**: 每个组件有独立的`BUILD.gn`文件
- **配置方式**: 修改`target_config.h`或通过GN args传递

> ⚠️ **注意**：LiteOS-M不使用`make menuconfig`。裁剪通过直接编辑Kconfig默认值或`target_config.h`完成，由GN构建系统读取并生成编译配置。

### 1.5 RISC-V架构特殊裁剪考虑

RISC-V架构的LiteOS-M有一些特殊的裁剪注意事项：

| 考虑维度 | ARM Cortex-M | RISC-V | 说明 |
|---------|-------------|--------|------|
| **中断控制器** | NVIC（固定） | PLIC/CLINT/ECLIC（可变） | RISC-V中断控制器实现因芯片而异 |
| **栈对齐** | 8字节 | 16字节 | RISC-V要求更严格的栈对齐 |
| **FPU** | 可选(VFP) | 可选(F/D扩展) | 无FPU时需裁剪浮点相关代码 |
| **原子操作** | LDREX/STREX | A扩展(AMO) | 无A扩展时需用软件模拟 |
| **指令集变体** | Thumb/Thumb-2 | RV32I/M/A/C/F/D组合 | ISA字符串影响编译选项 |
| **启动代码** | 向量表+Reset_Handler | _start+trap_entry | 完全不同的启动流程 |
| **上下文切换** | PendSV | 软中断(ecall) | 切换机制不同 |
| **内存模型** | 哈佛/统一 | 统一 | 链接脚本格式差异 |

## 2. LiteOS-A内核（小型系统）

### 2.1 定位与特点
- **面向MPU/AP设备**: ARM Cortex-A系列
- **最小RAM要求**: 1 MB（实际推荐≥8 MB）
- **支持虚拟内存**: 每进程独立4GB地址空间
- **支持多进程**: 进程+线程两级调度模型
- **支持SMP**: 多核对称处理
- **支持用户态/内核态分离**: 系统调用机制

### 2.2 架构分层

```
┌─────────────────────────────────────────┐
│           应用层 (User Space)             │
├─────────────────────────────────────────┤
│         系统调用接口 (Syscall)            │
├─────────────────────────────────────────┤
│  ┌──────────┬──────────┬──────────────┐ │
│  │进程/线程  │虚拟内存   │   IPC机制    │ │
│  │管理      │管理      │(队列/信号量/  │ │
│  │          │          │ 互斥/事件)    │ │
│  ├──────────┼──────────┼──────────────┤ │
│  │VFS文件   │网络协议栈 │   安全能力    │ │
│  │系统      │(lwIP)    │ (DAC/Cap)   │ │
│  ├──────────┴──────────┴──────────────┤ │
│  │         内核基础 (调度/中断/时钟)     │ │
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│         HDF 驱动框架                      │
├─────────────────────────────────────────┤
│          硬件 (SoC)                       │
└─────────────────────────────────────────┘
```

### 2.3 组件详细清单

| 组件类别 | 组件名称 | 功能描述 | 预估ROM | 预估RAM | Kconfig控制 |
|---------|---------|---------|---------|---------|------------|
| **核心** | 进程管理 | 进程创建(fork)/退出、PCB管理、ELF加载 | ~8 KB | ~2 KB + N×PCB | 必选 |
| **核心** | 线程管理 | 线程创建/调度、TCB、上下文切换 | ~5 KB | ~1 KB + N×TCB | 必选 |
| **核心** | 调度器 | CFS/RR/FIFO策略、SMP负载均衡 | ~4 KB | ~1 KB | 必选 |
| **核心** | 虚拟内存 | MMU页表管理、mmap、缺页处理、内存保护 | ~10 KB | ~4 KB + 页表 | LOSCFG_KERNEL_MMU |
| **核心** | 中断管理 | GIC配置、中断分发、软中断 | ~3 KB | ~0.5 KB | 必选 |
| **核心** | 系统时钟 | Tick管理、高精度定时器、睡眠 | ~2 KB | ~0.3 KB | 必选 |
| **IPC** | 消息队列 | 进程间消息传递 | ~1.5 KB | 队列缓冲 | LOSCFG_BASE_IPC_QUEUE |
| **IPC** | 信号量 | 进程/线程同步 | ~1 KB | N×SemCB | LOSCFG_BASE_IPC_SEM |
| **IPC** | 互斥锁 | 资源互斥、优先级继承 | ~1.2 KB | N×MuxCB | LOSCFG_BASE_IPC_MUX |
| **IPC** | 事件标志 | 事件组同步 | ~0.8 KB | N×EventCB | LOSCFG_BASE_IPC_EVENT |
| **IPC** | 信号(Signal) | POSIX信号机制 | ~1.5 KB | ~0.3 KB | LOSCFG_KERNEL_SIGNAL |
| **IPC** | 共享内存 | 进程间共享内存区域 | ~2 KB | 共享区大小 | LOSCFG_KERNEL_SHM |
| **文件系统** | VFS | 虚拟文件系统层 | ~5 KB | ~2 KB | LOSCFG_FS_VFS |
| **文件系统** | FAT | FAT12/16/32文件系统 | ~10 KB | ~4 KB | LOSCFG_FS_FAT |
| **文件系统** | JFFS2 | Flash日志文件系统 | ~12 KB | ~6 KB | LOSCFG_FS_JFFS2 |
| **文件系统** | LittleFS | 轻量级Flash文件系统 | ~8 KB | ~3 KB | LOSCFG_FS_LITTLEFS |
| **文件系统** | procfs | 进程信息伪文件系统 | ~3 KB | ~1 KB | LOSCFG_FS_PROC |
| **文件系统** | devfs | 设备文件伪文件系统 | ~2 KB | ~0.5 KB | LOSCFG_FS_DEVFS |
| **网络** | lwIP协议栈 | TCP/UDP/IP/ICMP/ARP | ~40-60 KB | ~30-50 KB | LOSCFG_NET_LWIP |
| **网络** | Socket接口 | BSD Socket API | ~5 KB | ~2 KB | LOSCFG_NET_SOCKETS |
| **网络** | DHCP客户端 | 动态IP获取 | ~3 KB | ~1 KB | LOSCFG_NET_DHCP |
| **网络** | DNS解析 | 域名解析 | ~2 KB | ~0.5 KB | LOSCFG_NET_DNS |
| **安全** | DAC权限 | 自主访问控制、UID/GID | ~3 KB | ~1 KB | LOSCFG_SECURITY_DAC |
| **安全** | Capability | 能力安全模型 | ~2 KB | ~0.5 KB | LOSCFG_SECURITY_CAPABILITY |
| **加载** | ELF加载器 | 动态链接、符号解析 | ~5 KB | ~2 KB | LOSCFG_KERNEL_DYNLOAD |
| **Shell** | 内核Shell | 命令行调试接口 | ~4 KB | ~2 KB | LOSCFG_SHELL |
| **驱动** | HDF框架 | 统一驱动模型 | ~10 KB | ~4 KB | LOSCFG_DRIVERS_HDF |

### 2.4 构建系统（GN + Kconfig）
- **构建工具**: GN + Ninja + Kconfig
- **配置入口**: `kernel/liteos_a/Kconfig`
- **输出文件**: `.config` → `autoconf.h`
- **组件化构建**: 每个组件有独立的`BUILD.gn`文件

> ⚠️ **注意**：LiteOS-A的Kconfig不使用标准Linux的`make menuconfig`交互界面，而是通过GN构建系统集成。
