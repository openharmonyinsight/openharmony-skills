# 适配文档模板集

> 本文件包含 OpenHarmony Lite 芯片适配所需的全部文档模板。模板使用 `${变量名}` 标记需要填充的内容，Agent应根据用户提供的MCU规格书、适配源码和build_lite配置进行替换。

---

## 1. L0轻量系统适配手册模板

```markdown
# ${CHIP_NAME} OpenHarmony Lite ${OHOS_VERSION} 适配手册

> **文档版本**: ${DOC_VERSION}  
> **适配版本**: OpenHarmony Lite ${OHOS_VERSION}  
> **系统级别**: L0 轻量系统 (Mini System)  
> **内核**: LiteOS-M  
> **芯片架构**: ${CPU_ARCH} (Cortex-M / RISC-V)  
> **芯片厂商**: ${VENDOR_NAME}  
> **最后更新**: ${LAST_UPDATE_DATE}  

---

## 1. 概述

### 1.1 芯片简介

${CHIP_NAME} 是 ${VENDOR_NAME} 推出的 ${CHIP_CATEGORY} MCU，基于 ${CPU_ARCH} 架构，
主频 ${CPU_FREQ}，内置 ${RAM_SIZE} RAM 和 ${FLASH_SIZE} Flash，
适用于 ${TARGET_SCENARIOS} 等IoT应用场景。

**核心规格：**

| 特性 | 规格 |
|------|------|
| CPU | ${CPU_SPEC} |
| RAM | ${RAM_SIZE} |
| Flash | ${FLASH_SIZE} |
| GPIO | ${GPIO_COUNT} 个 |
| UART | ${UART_COUNT} 路 |
| I2C | ${I2C_COUNT} 路 |
| SPI | ${SPI_COUNT} 路 |
| ADC | ${ADC_SPEC} |
| PWM | ${PWM_COUNT} 路 |
| 无线 | ${WIRELESS_SPEC} |
| 工作电压 | ${VOLTAGE_RANGE} |
| 低功耗模式 | ${LOW_POWER_MODES} |

### 1.2 适配范围

本适配基于 OpenHarmony Lite ${OHOS_VERSION} L0轻量系统（LiteOS-M内核），已验证以下功能：

| 功能模块 | 状态 | RAM占用 | 备注 |
|---------|------|---------|------|
| LiteOS-M内核 | ✅ 已验证 | ~6KB | 最小配置 |
| GPIO | ✅ 已验证 | ~0.5KB | |
| UART | ✅ 已验证 | ~1KB | 含调试输出 |
| I2C | ✅ 已验证 | ~0.8KB | |
| SPI | ✅ 已验证 | ~0.8KB | |
| PWM | ✅ 已验证 | ~0.5KB | |
| ADC | ✅ 已验证 | ~0.5KB | |
| WiFi | ✅ 已验证 | ~30KB | ${WIFI_CHIP} |
| BLE | ⚠️ 部分支持 | ~15KB | ${BLE_LIMITATIONS} |
| 文件系统 | ❌ 未启用 | - | RAM不足 |

**总RAM占用**: ${TOTAL_RAM_USAGE} / ${RAM_SIZE} (${RAM_USAGE_PERCENT})

### 1.3 已知限制

| # | 限制描述 | 影响范围 | 规避方案 |
|---|---------|---------|---------|
| 1 | ${LIMITATION_1} | ${IMPACT_1} | ${WORKAROUND_1} |

### 1.4 开发环境要求

| 项目 | 要求 |
|------|------|
| 主机操作系统 | Ubuntu 20.04/22.04 LTS 64-bit |
| 编译器 | ${TOOLCHAIN} (arm-none-eabi-gcc / riscv-gcc) |
| Python | 3.8+ |
| 烧录工具 | ${FLASH_TOOL} |
| 调试器 | ${DEBUGGER} (J-Link / ST-Link / DAPLink) |
| 串口工具 | 任意串口终端（minicom/PuTTY/DevEco Terminal） |

---

## 2. 硬件资源映射

### 2.1 内存布局

| 区域 | 起始地址 | 大小 | 用途 |
|------|---------|------|------|
| FLASH | ${FLASH_BASE} | ${FLASH_SIZE} | 代码+只读数据 |
| RAM | ${RAM_BASE} | ${RAM_SIZE} | 数据+堆+栈 |
| 栈空间 | ${STACK_BASE} | ${STACK_SIZE} | 主任务栈 |
| 堆空间 | ${HEAP_BASE} | ${HEAP_SIZE} | 动态内存分配 |

### 2.2 引脚复用表

| 功能 | 引脚 | 复用模式 | 备注 |
|------|------|---------|------|
| UART_TX | ${UART_TX_PIN} | AF${UART_AF} | 调试串口 |
| UART_RX | ${UART_RX_PIN} | AF${UART_AF} | 调试串口 |
| I2C_SDA | ${I2C_SDA_PIN} | AF${I2C_AF} | |
| I2C_SCL | ${I2C_SCL_PIN} | AF${I2C_AF} | |

---

## 3. 驱动适配概览

### 3.1 IoT外设驱动架构（L0）

```
${CHIP_NAME} IoT外设驱动架构:

应用层
  ↓ (CMSIS/POSIX接口)
IoT外设驱动子系统
  ├── gpio_component    ← 组件注册
  ├── uart_component
  ├── i2c_component
  ├── spi_component
  ├── pwm_component
  └── adc_component
  ↓ (HAL接口)
芯片HAL层 (${CHIP_NAME}_hal)
  ↓ (寄存器操作)
硬件
```

> ⚠️ **注意**：L0轻量系统使用 **IoT外设驱动子系统**，不使用完整HDF框架。驱动以组件方式注册，通过CMSIS/POSIX接口向上暴露能力。

---

## 4. 配套工具与资源

### 4.1 开发工具

| 工具 | 版本 | 用途 |
|------|------|------|
| DevEco Device Tool | ${DEVTOOL_VERSION} | IDE + 烧录 + 串口调试 |
| ${FLASH_TOOL} | ${FLASH_VER} | 固件烧录 |
| ${DEBUGGER} | ${DEBUG_VER} | JTAG/SWD在线调试 |
| 串口终端 | - | 日志查看和交互 |

### 4.2 参考文档

| 文档 | 链接 |
|------|------|
| ${CHIP_NAME} 数据手册 | [链接] |
| ${CHIP_NAME} 参考手册 | [链接] |
| OpenHarmony Lite移植指导 | [docs.openharmony.cn](https://docs.openharmony.cn/) |
| LiteOS-M内核文档 | [GitCode](https://gitcode.com/openharmony/kernel_liteos_m) |

---

## 附录

### A. 术语表

| 术语 | 全称 | 说明 |
|------|------|------|
| LiteOS-M | LiteOS Microcontroller | L0轻量系统内核 |
| CMSIS | Cortex Microcontroller Software Interface Standard | ARM MCU接口标准 |
| HAL | Hardware Abstraction Layer | 硬件抽象层 |
| IoT外设驱动 | IoT Peripheral Driver Subsystem | L0推荐驱动方式 |

### B. 变更记录

| 版本 | 日期 | 作者 | 变更说明 |
|------|------|------|---------|
| ${DOC_VERSION} | ${LAST_UPDATE_DATE} | ${AUTHOR} | 初始版本 |
```

---

## 2. L0移植指南模板（关键章节）

```markdown
## 4. LiteOS-M内核移植

### 4.1 启动代码适配

将芯片厂商提供的启动代码（startup_${CHIP}.s）适配到OpenHarmony Lite：

```asm
/* startup_${CHIP}.s - 适配要点 */
/* 1. 设置向量表基地址 */
    LDR     R0, =__vector_table
    MSR     VTOR, R0

/* 2. 初始化堆栈指针 */
    LDR     SP, =__stack_top

/* 3. 跳转到LiteOS-M入口 */
    BL      main
```

### 4.2 时钟配置

```c
/* ${CHIP}_clock.c */
void SystemClock_Config(void) {
    /* 配置系统时钟到 ${SYS_CLOCK_FREQ} */
    ${CLOCK_CONFIG_CODE}
    
    /* 更新SystemCoreClock变量 */
    SystemCoreClockUpdate();
}
```

### 4.3 Kconfig内核裁剪

```kconfig
# kernel/liteos_m/targets/${CHIP}/Kconfig
config LOSCFG_PLATFORM_${CHIP_UPPER}
    bool "Enable ${CHIP_NAME} platform"
    default y
    
config LOSCFG_KERNEL_HEAP_SIZE
    hex "Heap size"
    default 0x4000  # 16KB for ${CHIP_NAME}
    
config LOSCFG_TASK_DEFAULT_STACK_SIZE
    hex "Default task stack size"
    default 0x800   # 2KB
```

### 4.4 验证内核启动

编译并烧录后，通过串口观察输出：
```
************* Hello OpenHarmony Lite *************
[INFO] LiteOS-M kernel start
[INFO] System clock: ${SYS_CLOCK_FREQ} Hz
[INFO] Heap: ${HEAP_SIZE} bytes
[INFO] Kernel init success
OHOS $
```
```

---

## 3. 移植指南标准章节结构

```
Lite系统移植指南标准结构
│
├── 1. 概述
│   ├── 1.1 目标MCU/MPU简介
│   ├── 1.2 适配范围与已验证功能
│   ├── 1.3 软硬件环境要求（含RAM/Flash最低要求）
│   └── 1.4 文档约定与术语
│
├── 2. 环境搭建
│   ├── 2.1 主机环境要求
│   ├── 2.2 arm-none-eabi-gcc/riscv-gcc工具链安装
│   ├── 2.3 OpenHarmony Lite源码获取
│   ├── 2.4 芯片厂商SDK/BSP获取
│   └── 2.5 烧录/调试工具安装（ST-Link/J-Link/HiBurn等）
│
├── 3. build_lite编译配置
│   ├── 3.1 创建产品和单板目录
│   ├── 3.2 config.gni配置
│   ├── 3.3 product.json配置
│   ├── 3.4 链接脚本适配（.ld/.sct）
│   └── 3.5 首次编译验证
│
├── 4. LiteOS-M/A内核移植
│   ├── 4.1 启动代码适配（startup.s）
│   ├── 4.2 时钟配置（SystemClock）
│   ├── 4.3 中断管理（NVIC/PLIC配置）
│   ├── 4.4 内存管理（堆大小、栈大小配置）
│   ├── 4.5 Kconfig内核裁剪
│   └── 4.6 内核启动验证（串口输出）
│
├── 5. HAL层适配
│   ├── 5.1 GPIO HAL实现
│   ├── 5.2 UART HAL实现（用于调试输出）
│   ├── 5.3 I2C HAL实现
│   ├── 5.4 SPI HAL实现
│   ├── 5.5 PWM HAL实现
│   ├── 5.6 ADC HAL实现
│   └── 5.7 其他外设HAL
│
├── 6. IoT外设驱动开发（L0）/ 精简版HDF驱动（L1）
│   ├── 6.1 驱动组件注册方式
│   ├── 6.2 各外设驱动实现
│   └── 6.3 驱动验证方法
│
├── 7. 子系统集成（可选）
│   ├── 7.1 WiFi/BLE子系统
│   ├── 7.2 文件系统（LittleFS/FAT）
│   ├── 7.3 图形UI（Lite Graphic）
│   └── 7.4 网络协议栈
│
├── 8. 编译烧录与验证
│   ├── 8.1 完整编译命令
│   ├── 8.2 镜像说明和烧录步骤
│   ├── 8.3 串口调试验证
│   ├── 8.4 功能验证清单
│   └── 8.5 RAM/Flash使用统计
│
└── 9. 附录
    ├── A. 已知问题与限制
    ├── B. 常见问题FAQ
    ├── C. 参考资源链接
    └── D. 变更记录
```

---

## 4. FAQ模板（Lite系统特有）

```markdown
# ${CHIP_NAME} OpenHarmony Lite 适配常见问题 (FAQ)

> **适用版本**: OpenHarmony Lite ${OHOS_VERSION}  
> **系统级别**: L0 轻量系统 / L1 小型系统

---

## 编译构建

### Q1: build_lite编译报错 "undefined reference to `xxx`"

**现象：**
执行 `python build/lite/build.py` 时出现链接错误。

**原因：**
通常是BUILD.gn中deps缺少必要的库依赖。

**解决方案：**
```gn
# 在对应的BUILD.gn中添加缺失的依赖
deps += [
    "//kernel/liteos_m:liteos_m",
    "//drivers/lite/gpio:gpio_hal",
]
```

### Q2: RAM段溢出 "region 'RAM' overflowed by N bytes"

**解决方案：**
1. 分析.map文件找出RAM占用最大的模块
2. 在Kconfig中裁剪非必要组件
3. 启用LTO优化（`-flto`）
4. 减小堆栈大小
5. 将只读数据移至Flash

---

## 内核启动

### Q3: 烧录后串口无输出

**排查步骤：**
1. 确认串口波特率配置正确（通常115200）
2. 检查TX/RX引脚是否正确连接
3. 确认启动代码中向量表和堆栈指针设置正确
4. 使用JTAG/SWD调试器确认CPU是否正常运行
5. 检查时钟配置是否正确

### Q4: LiteOS-M启动后立即HardFault

**常见原因：**
- 堆栈空间不足（增大LOSCFG_TASK_DEFAULT_STACK_SIZE）
- 内存区域配置与实际硬件不匹配
- 启动代码中未正确初始化FPU（Cortex-M4/M33）
- 向量表偏移地址不正确

---

## 驱动适配

### Q5: GPIO操作无效

**排查步骤：**
1. 确认引脚号在有效范围内
2. 检查引脚复用配置（AF模式）
3. 确认GPIO时钟已使能
4. 用万用表/示波器验证引脚电平

### Q6: I2C通信失败

**排查步骤：**
1. 确认上拉电阻已安装（4.7KΩ~10KΩ）
2. 检查设备地址是否正确（7-bit vs 10-bit）
3. 用逻辑分析仪抓取SDA/SCL波形
4. 确认I2C时钟频率在设备支持范围内
```

---

## 5. API文档注释规范（Doxygen风格）

```c
/**
 * @brief 打开指定GPIO引脚
 * @note  Hi3861支持GPIO0-GPIO21，STM32F407支持PA0-PE15
 * @param pin 引脚编号（有效范围取决于具体芯片）
 * @return int32_t 成功返回0，失败返回负数错误码
 * @retval 0       打开成功
 * @retval -1      参数无效（引脚号超出范围）
 * @retval -2      GPIO未初始化
 * @retval -3      引脚已被占用
 *
 * @code
 * // 打开GPIO5
 * int32_t ret = GpioOpen(5);
 * if (ret != 0) {
 *     printf("GpioOpen failed, ret=%d\n", ret);
 * }
 * @endcode
 *
 * @see GpioClose
 * @see GpioSetDir
 */
int32_t GpioOpen(uint16_t pin);
```

---

## 6. Lite系统API文档重点接口体系

| 接口体系 | 适用系统 | 说明 |
|---------|---------|------|
| **CMSIS-RTOS2** | L0 | RTOS内核抽象接口 |
| **CMSIS-Driver** | L0 | 外设驱动抽象接口 |
| **HAL接口** | L0/L1 | GPIO/I2C/SPI/UART/PWM/ADC等 |
| **POSIX接口** | L0(部分)/L1 | 线程/信号量/文件等 |
| **IoT子系统API** | L0 | WiFi/BLE/传感器等IoT组件 |
| **精简版HDF** | L1 | HdfDriverEntry + 精简HCS |

---

## 7. 文档生成工具链推荐

### 方案A：轻量快速方案（推荐）

```
源码注释 ──→ Doxygen ──→ XML ──→ mkdoxy ──→ MkDocs Material ──→ HTML
                                                      ↓
Markdown 文档 ──────────────────────────────────────→ Pandoc ──→ PDF
```

- **优势**：学习成本低，适合MCU项目的小团队
- **适合**：中小芯片厂商、社区贡献者

### 方案B：OpenHarmony社区兼容方案

```
源码注释 ──→ Doxygen ──→ Markdown API文档 ──→ OpenHarmony docs仓库格式
                                                    ↓
Markdown 移植指南 ──────────────────────────→ OpenHarmony 官方文档站
```

- **优势**：直接兼容OpenHarmony文档体系
- **适合**：希望文档合入主线的厂商

---

## 8. 核心写作原则

OpenHarmony Lite文档遵循以下原则：

1. **面向MCU开发者**：假设读者熟悉嵌入式C开发，但不了解OpenHarmony Lite架构
2. **步骤精确**：每步操作都包含具体的命令、配置文件路径、预期输出
3. **资源意识**：始终关注RAM/Flash占用，标注每个组件的资源开销
4. **真机验证**：所有步骤均需在实际MCU开发板上验证，注明使用的开发板型号
5. **清晰区分L0/L1**：明确标注哪些内容适用于L0、哪些适用于L1
