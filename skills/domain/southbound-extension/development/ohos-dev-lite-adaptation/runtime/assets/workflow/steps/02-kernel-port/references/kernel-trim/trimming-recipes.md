# 组件资源占用数据 + 裁剪方案 + 案例

---

## 1. LiteOS-M组件资源占用估算表

> **注**: 以下数据基于ARM Cortex-M4架构、GCC -Os优化级别的典型估算值。实际值因架构、编译器、配置参数而异。

| 组件 | Kconfig宏 | ROM(代码+只读数据) | RAM(静态+动态) | 启动时间影响 | 裁剪等级 |
|------|-----------|-------------------|---------------|-------------|---------|
| **核心-任务管理** | 必选 | 2,500 B | 500 B + 400B×N_task | +2 ms | 不可裁 |
| **核心-调度器** | 必选 | 1,500 B | 200 B | +1 ms | 不可裁 |
| **核心-内存管理(bestfit)** | LOSCFG_KERNEL_MEM_BESTFIT | 1,500 B | 堆大小+256B元数据 | +1 ms | 算法可选 |
| **核心-内存管理(membox)** | LOSCFG_KERNEL_MEM_MEMBOX | 800 B | 池大小+128B元数据 | +0.5 ms | 算法可选 |
| **核心-中断管理** | 必选 | 1,000 B | 100 B + 向量表 | 0 | 不可裁 |
| **核心-异常处理** | 必选 | 800 B | 200 B | 0 | 不可裁 |
| **核心-系统时钟** | 必选 | 500 B | 50 B | +0.5 ms | 不可裁 |
| **IPC-信号量** | LOSCFG_BASE_IPC_SEM | 800 B | 32B×N_sem | 0 | 推荐保留 |
| **IPC-互斥锁** | LOSCFG_BASE_IPC_MUX | 1,000 B | 48B×N_mux | 0 | 推荐保留 |
| **IPC-消息队列** | LOSCFG_BASE_IPC_QUEUE | 1,200 B | 64B×N_q + 缓冲 | 0 | 按需 |
| **IPC-事件标志** | LOSCFG_BASE_IPC_EVENT | 600 B | 24B×N_evt | 0 | 按需 |
| **扩展-软件定时器** | LOSCFG_BASE_CORE_SWTMR | 1,000 B | 40B×N_tmr + 队列 | +1 ms | 按需 |
| **扩展-CPUP** | LOSCFG_BASE_CORE_CPUP | 500 B | 8B×N_task | 0 | 调测用 |
| **扩展-内核调试** | LOSCFG_KERNEL_DEBUG | 3,000 B | 1,000 B | +2 ms | 发布版裁 |
| **扩展-VFS** | LOSCFG_FS_VFS | 3,000 B | 1,000 B | +3 ms | 按需 |
| **扩展-FAT** | LOSCFG_FS_FAT | 8,000 B | 4,000 B | +5 ms | 按需 |
| **扩展-LittleFS** | LOSCFG_FS_LITTLEFS | 6,000 B | 2,000 B | +3 ms | 按需 |
| **扩展-lwIP** | LOSCFG_NET_LWIP | 40,000 B | 30,000 B | +20 ms | 按需 |
| **扩展-HDF** | LOSCFG_DRIVERS_HDF | 10,000 B | 4,000 B | +10 ms | 按需 |
| **接口-POSIX** | LOSCFG_POSIX_API | 5,000 B | 1,000 B | +2 ms | 按需 |
| **接口-CMSIS** | LOSCFG_CMSIS_RTOS2 | 3,000 B | 500 B | +1 ms | Cortex-M |

## 2. LiteOS-A组件资源占用估算表

| 组件 | Kconfig宏 | ROM估算 | RAM估算 | 启动时间影响 | 裁剪等级 |
|------|-----------|---------|---------|-------------|---------|
| **核心-进程管理** | 必选 | 8,000 B | 2,000 B + PCB | +5 ms | 不可裁 |
| **核心-线程管理** | 必选 | 5,000 B | 1,000 B + TCB | +3 ms | 不可裁 |
| **核心-调度器** | 必选 | 4,000 B | 1,000 B | +2 ms | 不可裁 |
| **核心-MMU/虚拟内存** | LOSCFG_KERNEL_MMU | 10,000 B | 4,000 B + 页表 | +10 ms | 小型系统必选 |
| **核心-中断(GIC)** | 必选 | 3,000 B | 500 B | +1 ms | 不可裁 |
| **核心-系统时钟** | 必选 | 2,000 B | 300 B | +1 ms | 不可裁 |
| **IPC-全量** | LOSCFG_BASE_IPC_* | 6,000 B | 3,000 B | +2 ms | 推荐保留 |
| **IPC-Signal** | LOSCFG_KERNEL_SIGNAL | 1,500 B | 300 B | 0 | 按需 |
| **IPC-共享内存** | LOSCFG_KERNEL_SHM | 2,000 B | 共享区大小 | 0 | 按需 |
| **FS-VFS** | LOSCFG_FS_VFS | 5,000 B | 2,000 B | +3 ms | 推荐保留 |
| **FS-FAT** | LOSCFG_FS_FAT | 10,000 B | 4,000 B | +5 ms | 按需 |
| **FS-JFFS2** | LOSCFG_FS_JFFS2 | 12,000 B | 6,000 B | +8 ms | NOR Flash |
| **FS-LittleFS** | LOSCFG_FS_LITTLEFS | 8,000 B | 3,000 B | +3 ms | NAND/NOR |
| **FS-procfs** | LOSCFG_FS_PROC | 3,000 B | 1,000 B | +2 ms | 调测用 |
| **FS-devfs** | LOSCFG_FS_DEVFS | 2,000 B | 500 B | +1 ms | 推荐保留 |
| **NET-lwIP** | LOSCFG_NET_LWIP | 50,000 B | 40,000 B | +25 ms | 按需 |
| **NET-Socket** | LOSCFG_NET_SOCKETS | 5,000 B | 2,000 B | +3 ms | 随lwIP |
| **NET-DHCP** | LOSCFG_NET_DHCP | 3,000 B | 1,000 B | +5 ms | 按需 |
| **NET-DNS** | LOSCFG_NET_DNS | 2,000 B | 500 B | +2 ms | 按需 |
| **SEC-DAC** | LOSCFG_SECURITY_DAC | 3,000 B | 1,000 B | +2 ms | 推荐 |
| **SEC-Capability** | LOSCFG_SECURITY_CAPABILITY | 2,000 B | 500 B | +1 ms | 推荐 |
| **ELF加载器** | LOSCFG_KERNEL_DYNLOAD | 5,000 B | 2,000 B | +5 ms | 按需 |
| **Shell** | LOSCFG_SHELL | 4,000 B | 2,000 B | +3 ms | 调测用 |
| **HDF框架** | LOSCFG_DRIVERS_HDF | 10,000 B | 4,000 B | +10 ms | 推荐 |

## 3. Lite系统分级资源约束参考（L0轻量系统）

> ⚠️ **核心**：L0轻量系统面向MCU级设备，RAM极其有限。以下是针对不同RAM级别的裁剪方案建议。

| RAM级别 | 可用组件 | 推荐裁剪策略 | 典型芯片 |
|---------|---------|------------|---------|
| **64KB~128KB** | 最小功能集(任务+调度+内存+中断) + 信号量 | 仅保留核心IPC，禁用FS/NET/CMSIS/调试 | STM32F103, ESP32-C3(部分) |
| **128KB~256KB** | 核心 + 信号量 + 互斥锁 + 队列 | 可选LittleFS或lwIP(精简)，禁用调试 | Hi3861, STM32F407, XR806 |
| **256KB~512KB** | 核心 + 全IPC + FS或NET(二选一) | 可启用一个扩展组件 | BES2600W, STM32H743, ESP32-S3 |
| **512KB~1MB** | 核心 + 全IPC + FS + NET(精简) | 接近完整功能集 | STM32H743(高配), ESP32-S3(+PSRAM) |

## 4. 主流MCU/MPU芯片规格与适配矩阵

### 4.1 MCU级芯片（LiteOS-M目标，L0轻量系统）

| 芯片 | 厂商 | CPU | 主频 | RAM | Flash | 外设 | 推荐内核 | OH适配状态 |
|------|------|-----|------|-----|-------|------|---------|-----------|
| STM32F103 | ST | Cortex-M3 | 72 MHz | 20-96 KB | 64-512 KB | UART/SPI/I2C/ADC | LiteOS-M | ✅ 社区已适配 |
| STM32F407 | ST | Cortex-M4F | 168 MHz | 192 KB | 512 KB-1 MB | USB/Ethernet/DCMI | LiteOS-M | ✅ 官方参考 |
| STM32L476 | ST | Cortex-M4F | 80 MHz | 128 KB | 512 KB-1 MB | LP UART/SPI/QSPI | LiteOS-M | ✅ 低功耗场景 |
| STM32H743 | ST | Cortex-M7 | 480 MHz | 1 MB | 2 MB | 双USB/Ethernet/LTDC | LiteOS-M | ✅ 高性能MCU |
| ESP32 | Espressif | Xtensa LX6 双核 | 240 MHz | 520 KB SRAM | External 4-16 MB | WiFi/BLE/SPI/I2C | LiteOS-M | ✅ 官方支持 |
| ESP32-S3 | Espressif | Xtensa LX7 双核 | 240 MHz | 512 KB SRAM + PSRAM | External | WiFi/BLE/USB/LCD | LiteOS-M | ✅ 新一代 |
| ESP32-C3 | Espressif | RISC-V 单核 | 160 MHz | 400 KB SRAM | 4 MB Flash | WiFi/BLE | LiteOS-M | ✅ RISC-V生态 |
| Hi3861 | HiSilicon | RISC-V | 160 MHz | 352 KB | 2 MB | WiFi/BLE/UART/SPI | LiteOS-M | ✅ OH官方 |
| BES2600W | Bestechnic | ARM CM33 + DSP | 260 MHz | 512 KB | 4 MB | WiFi/BT/Audio | LiteOS-M | ✅ OH参考 |
| XR806 | Allwinner | RISC-V | 160 MHz | 288 KB | 2 MB | WiFi/BLE | LiteOS-M | ✅ OH社区 |
| W806 | WinnerMicro | XT804(C-Sky) | 240 MHz | 288 KB | 2 MB | WiFi/BLE | LiteOS-M | ✅ OH社区 |

### 4.2 MPU级芯片（LiteOS-A目标，L1小型系统）

| 芯片 | 厂商 | CPU | 主频 | RAM | 存储 | GPU/NPU | 推荐内核 | OH适配状态 |
|------|------|-----|------|-----|------|---------|---------|-----------|
| Hi3516DV300 | HiSilicon | Cortex-A7 双核 | 950 MHz | DDR3/4 256MB-1GB | eMMC/SPI NAND | Mali-T720 | LiteOS-A | ✅ OH IPC参考 |
| Hi3516EV200 | HiSilicon | Cortex-A7 | 950 MHz | DDR3 64-256 MB | SPI NAND | ISP | LiteOS-A | ✅ 低端IPC |
| Hi3518 | HiSilicon | Cortex-A7 | 800 MHz | DDR2 64-128 MB | SPI NAND | ISP | LiteOS-A | ✅ IPC方案 |
| SSC8625V | SigmaStar | Cortex-A7 | 950 MHz | DDR3 128-512 MB | eMMC/SPI NAND | ISP+IVE | LiteOS-A | ✅ IPC方案 |
| STM32MP1 | ST | Cortex-A7 | 650 MHz | DDR3/4 ≤1GB | eMMC/SD | GPU 2D | LiteOS-A | ⚠️ 社区适配中 |
| 全志T507 | Allwinner | Cortex-A53 四核 | 1.5 GHz | DDR3/4 ≤2GB | eMMC/NAND | Mali-400 | LiteOS-A/Linux | ⚠️ 社区适配中 |

> ⚠️ **注意**：RK3568/RK3588/JH7110等高性能SoC属于标准系统(L2/Linux)范畴，不在本工具范围内。

### 4.3 芯片-内核-配置映射规则（仅Lite系统）

```
IF RAM < 128 KB:
    → ❌ 不支持OpenHarmony（低于最低要求）
    
ELIF RAM >= 128 KB AND RAM < 1 MB:
    → 内核 = LiteOS-M
    → 系统 = L0轻量系统
    → 裁剪重点: 最小化IPC组件，谨慎启用文件系统和网络
    → 参考分级: 64KB/128KB/256KB/512KB方案
    
ELIF RAM >= 1 MB AND RAM < 128 MB:
    IF CPU == Cortex-A:
        → 内核 = LiteOS-A
        → 系统 = L1小型系统
        → 裁剪重点: 文件系统选择、网络协议栈裁剪、驱动精简
    ELSE:
        → 内核 = LiteOS-M (高配MCU模式)
        
ELIF RAM >= 128 MB:
    → ⚠️ 超出本工具范围（标准系统L2/Linux）
```

## 5. 已有裁剪案例

### 5.1 案例1：STM32F407 智能传感器（LiteOS-M 极致裁剪）

**芯片规格**: Cortex-M4F, 168MHz, 192KB RAM, 1MB Flash  
**功能需求**: 温湿度采集 + MQTT上报 + OTA升级  
**裁剪目标**: 尽可能多的RAM留给MQTT和应用

| 配置项 | 默认值 | 裁剪后 | 节省 | 理由 |
|-------|-------|--------|------|------|
| LOSCFG_BASE_IPC_EVENT | y | n | ~600B ROM + RAM | 仅需信号量和队列 |
| LOSCFG_BASE_CORE_SWTMR | y | n | ~1,000B ROM + RAM | 使用硬件定时器替代 |
| LOSCFG_BASE_CORE_CPUP | y | n | ~500B ROM | 发布版不需要 |
| LOSCFG_KERNEL_DEBUG | y | n | ~3,000B ROM + 1KB RAM | 发布版关闭 |
| LOSCFG_FS_FAT | y | n | ~8,000B ROM + 4KB RAM | 使用LittleFS |
| LOSCFG_FS_LITTLEFS | n | y | +6,000B ROM + 2KB RAM | Flash友好型FS |
| LOSCFG_CMSIS_RTOS2 | y | n | ~3,000B ROM | 直接使用LiteOS API |
| LOSCFG_NET_LWIP | y | y(精简) | ~10,000B ROM | 关闭IPv6/TCP高级特性 |

**裁剪结果**: ROM从~85KB降至~58KB（节省32%），RAM从~65KB降至~42KB（节省35%）

### 5.2 案例2：Hi3516DV300 IPC摄像头（LiteOS-A 功能裁剪）

**芯片规格**: Cortex-A7 双核, 950MHz, 512MB DDR3  
**功能需求**: H.264/H.265编码 + RTSP推流 + OSD叠加  
**裁剪目标**: 最大化ISP和视频编码性能

| 配置项 | 默认值 | 裁剪后 | 理由 |
|-------|-------|--------|------|
| LOSCFG_FS_JFFS2 | y | n | 使用SPI NAND + LittleFS |
| LOSCFG_FS_FAT | y | n | 无需FAT分区 |
| LOSCFG_SHELL | y | n | 发布版关闭Shell |
| LOSCFG_KERNEL_DYNLOAD | y | n | 静态链接所有模块 |
| LOSCFG_NET_DHCP | y | n | 使用静态IP |
| LOSCFG_NET_DNS | y | n | 直连RTSP服务端 |
| LOSCFG_SECURITY_CAPABILITY | y | y | IPC需要安全隔离 |
| LOSCFG_DRIVERS_HDF | y | y | ISP/Video Codec通过HDF |

**裁剪结果**: 内核启动时间从3.2s降至2.1s，可用RAM增加约15MB

### 5.3 案例3：ESP32-C3 RISC-V传感器节点（LiteOS-M RISC-V裁剪）

**芯片规格**: RISC-V RV32IMC, 160MHz, 400KB SRAM, 4MB Flash  
**功能需求**: BLE通信 + 温湿度采集 + 低功耗休眠  
**裁剪目标**: 最小化RAM占用以支持BLE协议栈

| 配置项 | 默认值 | 裁剪后 | 节省 | 理由 |
|-------|-------|--------|------|------|
| LOSCFG_BASE_IPC_EVENT | y | n | ~600B ROM + RAM | 仅需信号量 |
| LOSCFG_BASE_CORE_SWTMR | y | y(精简) | ~400B ROM | 减少定时器数量至4个 |
| LOSCFG_BASE_CORE_CPUP | y | n | ~500B ROM | 发布版不需要 |
| LOSCFG_KERNEL_DEBUG | y | n | ~3,000B ROM + 1KB RAM | 发布版关闭 |
| LOSCFG_FS_VFS | n | n | - | 不使用文件系统 |
| LOSCFG_NET_LWIP | n | n | - | 使用轻量BLE协议栈替代 |
| LOSCFG_CMSIS_RTOS2 | n | n | - | 直接使用LiteOS API |
| LOSCFG_POSIX_API | n | n | - | 不需要POSIX接口 |

**RISC-V特殊考虑**:
- 栈对齐必须16字节（ARM为8字节）
- 无FPU，浮点运算需软件模拟（避免使用）
- ISA为RV32IMC（含压缩指令），代码密度优于RV32IM
- 中断控制器为ECLIC（非PLIC），需确认向量表格式

**裁剪结果**: ROM从~45KB降至~28KB（节省38%），RAM从~35KB降至~22KB（节省37%），剩余空间满足BLE协议栈需求

## 6. 常见裁剪错误与规避

| 错误类型 | 具体表现 | 根因 | 规避方法 |
|---------|---------|------|---------|
| **依赖遗漏** | 启用A但忘记启用其depends on的B，编译报错 | 未理解Kconfig依赖链 | 工具自动解析依赖并补全 |
| **过度裁剪** | 裁掉了被隐式依赖的组件，运行时crash | select/imply关系未被注意 | 建立完整依赖图+运行时验证 |
| **内存不足** | 裁剪后RAM够用但运行时OOM | 未考虑动态分配的峰值 | 预留安全裕量(建议20%) |
| **启动失败** | 初始化顺序依赖被破坏 | 组件初始化有隐含时序要求 | 保持核心组件初始化链完整 |
| **功能缺失** | 裁掉的功能被上层框架默认调用 | 不了解OH框架层的隐式依赖 | 维护框架-内核功能映射表 |
| **安全降级** | 关闭安全模块导致系统易受攻击 | 安全组件被视为可选 | 标记安全组件为"强烈建议保留" |
| **认证失败** | 裁剪后不满足兼容性测评要求 | 不了解认证的必选组件清单 | 内置认证组件检查规则 |
| **Flash溢出** | 裁剪不够导致固件超出Flash容量 | 低估了某些组件的实际大小 | 精确度量+分级预警 |

## 7. 内核裁剪最佳实践

1. **渐进式裁剪原则**: 从全功能配置出发，逐步禁用不需要的组件，而非从最小配置逐步添加
2. **先测量再裁剪**: 每次裁剪前后都要测量ROM/RAM变化，确认裁剪效果
3. **保持安全裕量**: RAM预留至少20%裕量，Flash预留至少10%裕量
4. **分层裁剪策略**: 先裁大组件(网络/FS/驱动)，再裁小组件(IPC/调试)
5. **回归测试**: 每次裁剪后执行冒烟测试，确保基本功能正常
6. **版本化配置**: 使用defconfig保存每轮裁剪的配置，便于回溯
7. **文档化决策**: 记录每个裁剪决策的理由，便于后续维护
8. **区分发布/调试**: 维护两套配置——调试版(含调测组件)和发布版(极致裁剪)

## 8. 资源占用度量方法（Lite系统适用）

| 度量维度 | 工具/方法 | 说明 |
|---------|----------|------|
| **代码大小(ROM)** | `arm-none-eabi-size -A` / `riscv-none-elf-size` | 按段统计代码+只读数据大小 |
| **RAM占用** | 链接脚本map文件分析(`--print-memory-usage`) | .data + .bss + 堆栈 + 动态分配池 |
| **增量大小** | 对比两次编译的size输出 | 手动或使用脚本对比 |
| **启动时间** | GPIO翻转 + 示波器/逻辑分析仪 | MCU级启动时间测量 |
| **运行时内存** | LOS_MemInfoGet() / LOS_ShowMem() | LiteOS-M内置内存统计API |
| **功耗影响** | 电流探针 + 功耗分析仪 | 硬件测量 |
