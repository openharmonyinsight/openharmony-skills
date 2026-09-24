# OpenHarmony Lite 术语库

> 本术语库定义了 OpenHarmony Lite（L0轻量系统 + L1小型系统）文档中应使用的标准术语。编写适配文档时必须遵循本术语库，确保用语一致性和准确性。

---

## 1. 核心系统术语

| 术语 | 全称 | 中文释义 | 使用场景 | 备注 |
|------|------|---------|---------|------|
| **LiteOS-M** | LiteOS Microcontroller | 轻量级微控制器内核 | L0系统内核 | 不要写成"LiteOS_M"或"LITEOS-M" |
| **LiteOS-A** | LiteOS Application | 轻量级应用处理器内核 | L1-LiteOS 路线内核 | 不要写成"LiteOS_A" |
| **Linux** | Linux Kernel | Linux 内核（5.10 等） | L1-Linux 路线内核（kernel_family=linux，如 Hi3516CV610） | 属 Lite L1 范畴非 L2；按 target profile 判定，勿按内核名反推系统级别 |
| **L0** | Level 0 | 轻量系统 (Mini System) | 系统级别标注 | MCU级，最小128KB RAM |
| **L1** | Level 1 | 小型系统 (Small System) | 系统级别标注 | MPU级，最小1MB RAM |
| **L2** | Level 2 | 标准系统 (Standard System) | ⚠️ 不在Lite文档中使用 | 标准系统专用；L1-Linux 路线（kernel_family=linux）内核同为 Linux 但属 Lite L1 范畴，勿按内核名判级 |
| **OpenHarmony Lite** | - | OpenHarmony轻量/小型系统统称 | 产品名 | 涵盖L0+L1 |
| **build_lite** | Build Lite | 轻量级编译构建系统 | L0/L1编译构建 | 区别于标准系统的build系统 |

## 2. 接口与框架术语

| 术语 | 全称 | 中文释义 | 使用场景 | 备注 |
|------|------|---------|---------|------|
| **CMSIS** | Cortex Microcontroller Software Interface Standard | ARM MCU软件接口标准 | L0 HAL抽象 | 仅适用于ARM Cortex-M架构 |
| **CMSIS-RTOS2** | CMSIS Real-Time Operating System v2 | RTOS内核抽象接口 | L0任务管理 | 线程/信号量/定时器等 |
| **CMSIS-Driver** | CMSIS Peripheral Driver | 外设驱动抽象接口 | L0外设驱动 | GPIO/SPI/I2C等统一接口 |
| **HAL** | Hardware Abstraction Layer | 硬件抽象层 | 通用硬件操作封装 | gpio_if.h/i2c_if.h等 |
| **IoT外设驱动** | IoT Peripheral Driver Subsystem | IoT外设驱动子系统 | L0推荐驱动方式 | 组件注册模式 |
| **HDF** | Hardware Driver Foundation | 硬件驱动基础框架 | ⚠️ L1精简版可用，L0不使用 | L0用IoT外设驱动替代 |
| **HCS** | HDF Configuration Source | HDF配置描述源码 | L1精简版HDF配置 | L0不使用 |
| **POSIX** | Portable Operating System Interface | 可移植操作系统接口 | L0(部分)/L1系统调用 | 线程/信号量/文件等 |

## 3. 硬件与调试术语

| 术语 | 全称 | 中文释义 | 使用场景 | 备注 |
|------|------|---------|---------|------|
| **MCU** | Microcontroller Unit | 微控制器 | L0目标芯片 | 如Hi3861/STM32F407/BES2600W |
| **MPU** | Microprocessor Unit | 微处理器 | L1目标芯片 | 如Hi3516DV300 |
| **BSP** | Board Support Package | 板级支持包 | 特定开发板的软件适配集合 | |
| **JTAG** | Joint Test Action Group | 联合测试行动组 | MCU在线调试接口 | |
| **SWD** | Serial Wire Debug | 串行线调试 | ARM调试协议 | 比JTAG引脚更少 |
| **ISR** | Interrupt Service Routine | 中断服务程序 | 中断处理函数 | ISR中禁止阻塞调用 |
| **NVIC** | Nested Vectored Interrupt Controller | 嵌套向量中断控制器 | ARM Cortex-M中断管理 | |
| **PLIC** | Platform-Level Interrupt Controller | 平台级中断控制器 | RISC-V中断管理 | Hi3861使用 |
| **DMA** | Direct Memory Access | 直接内存访问 | 高速数据传输 | 需注意缓冲区对齐 |
| **FPU** | Floating Point Unit | 浮点运算单元 | Cortex-M4/M33浮点支持 | 需在Kconfig中启用 |

## 4. 构建与配置术语

| 术语 | 全称 | 中文释义 | 使用场景 | 备注 |
|------|------|---------|---------|------|
| **GN** | Generate Ninja | 构建系统元语言 | BUILD.gn/config.gni | |
| **Ninja** | Ninja Build | 快速构建系统 | 实际执行编译 | 由GN生成 |
| **Kconfig** | Kernel Configuration | 内核配置系统 | LiteOS-M/A内核裁剪 | menuconfig界面 |
| **LTO** | Link-Time Optimization | 链接时优化 | 减小代码体积 | `-flto` 编译选项 |
| **LittleFS** | Little File System | 轻量级文件系统 | L0可选文件系统 | 掉电安全 |
| **map文件** | Linker Map File | 链接器映射文件 | RAM/Flash占用分析 | .map后缀 |

## 5. 芯片相关术语

| 术语 | 说明 | 适用系统 |
|------|------|---------|
| **Hi3861** | 海思RISC-V WiFi SoC | L0 |
| **STM32F407** | ST Cortex-M4 MCU | L0 |
| **BES2600W** | 恒玄Cortex-M33 WiFi/BT SoC | L0 |
| **XR806** | 全志RISC-V WiFi SoC | L0 |
| **Hi3516DV300** | 海思Cortex-A7 MPU | L1 |

## 6. ⚠️ 禁用术语（L2标准系统专属，不应出现在Lite文档中）

以下术语属于L2标准系统，**严禁在Lite适配文档中使用**：

| 禁用术语 | 所属系统 | Lite替代方案 |
|---------|---------|-------------|
| Linux DTS (Device Tree) | L2 | Lite使用Kconfig+config.gni（L1-Linux 路线 kernel_family=linux 时允许 DTS） |
| 完整HDF框架 (HdfDriverEntry/IDeviceIoService/Bind/Init/Release) | L2 | L0使用IoT外设驱动子系统；L1使用精简版HDF |
| hdc (HarmonyOS Device Connector) | L2 | L0使用串口/JTAG；L1有限支持hdc |
| hilog (完整日志系统) | L2 | L0使用printf/串口；L1有限支持hilog |
| Kernel Panic | L2 | Lite使用HardFault/Fault Handler（L1-Linux 路线允许 Kernel Panic） |
| ext4/F2FS | L2 | Lite使用LittleFS/FAT（L1-Linux 路线允许 ext4） |
| gtest (完整版) | L2 | Lite使用HCTest/Unity（L1-Linux 路线允许 gtest/HWTEST_F） |
| HWTEST_F | L2 | Lite使用RUN_TEST宏（L1-Linux 路线允许） |
| XTS完整套件 | L2 | L0使用轻量系统测试框架；L1使用精简版 |
| AAFWK (Ability框架) | L2 | Lite无应用框架 |
| ArkUI/ArkTS | L2 | Lite使用Lite Graphic/C语言UI |
| NAPI | L2 | Lite无JS引擎 |

---

## 7. 常见错误用法纠正

| ❌ 错误写法 | ✅ 正确写法 | 说明 |
|------------|-----------|------|
| LiteOS_M | LiteOS-M | 使用连字符而非下划线 |
| liteos-m | LiteOS-M | 注意大小写 |
| ohos lite | OpenHarmony Lite | 使用完整产品名 |
| HDF驱动 (用于L0) | IoT外设驱动 | L0不使用HDF |
| gtest单元测试 | HCTest/Unity测试 | L0不支持gtest |
| hdc调试 | 串口/JTAG调试 | L0不支持hdc |
| hilog日志 | printf/串口日志 | L0不支持hilog |
| 设备树/DTS | Kconfig/config.gni（L1-Linux 路线除外） | LiteOS 路线不使用 DTS；L1-Linux（kernel_family=linux）用 DTS |
| 标准系统 | L2标准系统 | 明确标注系统级别 |
| 轻量级系统 | L0轻量系统 | 使用官方名称 |
