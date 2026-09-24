# 芯片适配硬件信息需求清单

> 从适配流程的每个阶段倒推，梳理工程师（或AI）在每一步需要从芯片datasheet中获取的硬件信息。

---

## 适配全链路 × 所需硬件信息

### 阶段0：环境准备（构建配置）

写linker script、配GCC编译选项、建产品目录时需要：

| 信息项 | 用途 | datasheet位置 |
|--------|------|--------------|
| CPU架构 + 内核型号 | GCC `-mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16` 或 `-march=rv32imac` | 首页/概述 |
| Flash大小 + 起始地址 | linker script的ROM段 | Memory Map章节 |
| SRAM大小 + 起始地址 | linker script的RAM段 | Memory Map章节 |
| 是否有FPU | 编译选项要不要加`-mfpu` | CPU Features |
| 字节序（Little/Big Endian） | 一般ARM/RISC-V都是Little，但要确认 | CPU Features |

### 阶段1：启动引导（Bootloader + 系统时钟）

芯片上电后第一件事是配时钟、初始化内存：

| 信息项 | 用途 | datasheet位置 |
|--------|------|--------------|
| 启动地址 / Boot入口 | 中断向量表放哪里、Reset_Handler跳转地址 | Memory Map / Boot |
| 时钟源类型 | HSI/HSE/LSE/PLL有哪些可用 | RCC / Clock章节 |
| 系统时钟配置方法 | PLL倍频分频参数、时钟切换步骤 | RCC / Clock |
| 外设总线结构 | AHB/APB1/APB2各挂哪些外设 | Bus Matrix / Memory Map |
| Flash等待周期 | 不同主频下Flash访问要插几个Wait State | Flash Controller |
| **SoC 内置 DDR 变体鉴别** | **内置 DDR SoC 同型号多变体（如 Hi3516CV610 -10B/-20S/-20G/-00S/-00G），裸烧 bootrom 阶段的 reg_info/xlsm 必须按变体选。错配 → DDR 初始化表不匹配 → 烧到 100% 但 uboot 起不来。鉴别路径：型号 → DDR 类型(DDR2/DDR3)/容量/封装(QFN/BGA)/速率 → 对应 .xlsm → reg_info。详见 `references/ddr-variant-guide.md`** | **产品简介「型号配置差异」表 + 厂商 SDK boot_tools 目录** |

### 阶段2：内核移植（LiteOS-M / LiteOS-A）

内核需要调度、中断、内存保护：

| 信息项 | 用途 | datasheet位置 |
|--------|------|--------------|
| SysTick定时器 | 内核Tick时钟源，周期中断 | SysTick / Timer |
| 中断控制器类型 | NVIC（ARM）/ PLIC/CLIC（RISC-V），决定中断管理代码 | Interrupt Controller |
| 中断优先级位数 | NVIC的优先级分组配置（2bit还是4bit） | NVIC章节 |
| 中断向量表 | 每个IRQn对应的handler名，异常向量排列 | Interrupt Vector Table |
| MPU（内存保护单元） | 可选，用于内存区域权限保护 | MPU章节 |
| PendSV / SVC（ARM） | 上下文切换和系统调用用的异常 | 内核架构文档 |

### 阶段3：外设驱动开发

这是工作量最大的一块，每个外设都要写驱动：

| 信息项 | 用途 | datasheet位置 |
|--------|------|--------------|
| **外设基地址** | 所有寄存器操作的起点 | Memory Map |
| **寄存器列表** | 每个外设有哪些寄存器、偏移地址、读写属性 | 各外设章节 |
| **寄存器位域定义** | 每个bit/bit group的含义，驱动的核心操作对象 | 各外设章节（占篇幅最大） |
| **时钟使能位** | 每个外设在RCC的哪个寄存器的哪个bit开时钟 | RCC章节 |
| **外设中断号** | UART的接收中断是IRQn几、触发方式是什么 | Interrupt章节 |
| **引脚复用表** | 某个pin能复用为UART_TX还是SPI_MOSI，AF编号 | GPIO / Pin Mux |
| **DMA通道映射** | 哪个DMA通道能服务哪个外设 | DMA章节 |

### 阶段4：板级配置（HCS / board_config.h）

把上面的信息填进OpenHarmony的配置系统：

| 信息项 | 用途 |
|--------|------|
| 外设实例数量 | 有几个UART、几个SPI、几个I2C |
| 各实例的基地址 + 中断号 | board_config.h / HCS配置 |
| 默认引脚分配 | 调试串口用哪两个pin、I2C用哪两个pin |
| 开发板特有资源 | LED接哪个GPIO、按键接哪个GPIO、外部晶振频率 |

### 阶段5：调试

| 信息项 | 用途 |
|--------|------|
| JTAG/SWD接口引脚 | 连接调试器 |
| 调试串口默认引脚 | 打印启动日志 |
| Fault寄存器定义（ARM） | CFSR/HFSR/BFAR位域解析 |

---

## 汇总：最小必要清单

按重要性分三级：

### 必须有（没有就适配不了）

1. CPU架构 + 内核型号
2. Flash/SRAM 大小和起始地址
3. 系统时钟配置方法（时钟源、PLL参数）
4. 中断控制器类型 + 中断向量表
5. SysTick/系统定时器
6. 各外设的基地址
7. 各外设的寄存器定义 + 位域
8. **SoC 内置 DDR 变体鉴别**（仅内置 DDR SoC 需要，但一旦适用即为必须）——型号后缀 → DDR 类型/容量/封装/速率 → 对应 .xlsm → reg_info。错配导致裸烧 uboot 起不来。见 `references/ddr-variant-guide.md`

### 高频使用（驱动开发必查）

8. 引脚复用表（Pin Mux / AF映射）
9. 外设时钟使能位（RCC寄存器）
10. 外设中断号
11. DMA通道映射

### 按需使用

12. FPU信息
13. MPU配置
14. 低功耗模式
15. JTAG/SWD接口
16. 启动模式/Boot配置

---

## 关键发现

**外设寄存器定义 + 位域**这一块占了datasheet 60-80%的篇幅，也是适配工作量最大的部分。这也是为什么"芯片规格解析"这个需求被列为P1——它主要解决的就是这块信息的提取和结构化问题。

---

*文档生成日期：2026-06-08*
*来源：OpenHarmony Lite适配流程分析*
