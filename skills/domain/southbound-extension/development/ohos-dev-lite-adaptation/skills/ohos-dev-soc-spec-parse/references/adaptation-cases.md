# 从Linux源码提取芯片规格的案例

> 本文展示如何从Linux内核源码中提取芯片硬件信息，以有Linux主线支持的芯片（STM32F407、全志T507）为详细案例，同时覆盖其他芯片的替代方案。

## 1. STM32F407 — Linux主线支持最完整（ARM Cortex-M4）

### 芯片概况

- ARM Cortex-M4F @ 168MHz（带FPU）
- 192KB SRAM + 1MB Flash
- 外设：GPIO(×9组)、UART(×6)、I2C(×3)、SPI(×3)、PWM(TIM×14)、ADC(×3)、USB OTG
- OpenHarmony L0轻量系统ARM生态代表（Niobe407开发板）

### Linux源码中的信息位置

| 信息类型 | Linux路径 | 提取内容 |
|---------|----------|---------|
| 外设地址/中断 | `arch/arm/boot/dts/stm32f429.dtsi` | 所有外设的reg/interrupts/clocks |
| 引脚复用表 | `drivers/pinctrl/stm32/pinctrl-stm32f429.c` | 每个引脚的AF功能（AF0-AF15） |
| 时钟树 | `drivers/clk/st/clk-stm32f4.c` | PLL/AHB/APB1/APB2分频器 |
| 时钟宏定义 | `include/dt-bindings/clock/stm32f4-clock.h` | 外设时钟编号 |
| 引脚宏定义 | `include/dt-bindings/pinctrl/stm32-pinfunc.h` | PINMUX宏 |
| 内存布局 | `arch/arm/boot/dts/stm32f429.dtsi` | SRAM/Flash地址和大小 |

### 提取示例：USART1

**从DTS提取**（`stm32f429.dtsi`）：

```dts
usart1: serial@40011000 {
    compatible = "st,stm32-usart", "st,stm32-uart";
    reg = <0x40011000 0x400>;           // 基地址: 0x40011000, 大小: 1KB
    interrupts = <37>;                   // NVIC IRQ#37
    clocks = <&rcc 0 STM32F4_APB2_CLOCK(USART1)>;  // 时钟: APB2
    status = "disabled";
};
```

**从pinctrl提取**（`pinctrl-stm32f429.c`）：

```c
// PA9 的复用功能：
STM32_FUNCTION(7, "USART1_TX")   // AF7 = USART1 TX
// PA10 的复用功能：
STM32_FUNCTION(7, "USART1_RX")   // AF7 = USART1 RX
```

**整理输出**：

```json
{
  "peripheral": "USART1",
  "base_address": "0x40011000",
  "size": "0x400",
  "interrupt": 37,
  "clock": "APB2",
  "pins": {
    "TX": {"port": "A", "pin": 9, "af": 7},
    "RX": {"port": "A", "pin": 10, "af": 7}
  }
}
```

### 提取示例：时钟树

**从时钟驱动提取**（`clk-stm32f4.c`）：

```
HSE (8MHz外部晶振)
  └── PLL (×336, /2 = 168MHz SYSCLK)
       ├── AHB_DIV (/1 = 168MHz HCLK)
       │    └── APB1_DIV (/4 = 42MHz) → TIM2/TIM3/...
       │         └── APB1_TIM (*2 = 84MHz) → 定时器时钟
       └── APB2_DIV (/2 = 84MHz) → USART1/SPI1/...
            └── APB2_TIM (*2 = 168MHz) → 定时器时钟
```

## 2. 全志T507 — Linux主线支持好（ARM Cortex-A7, L1）

### 芯片概况

- 四核 ARM Cortex-A53 @ 1.8GHz
- 支持MMU，运行LiteOS-A（L1小型系统）
- 外设：GPIO(×7组)、UART(×6)、I2C(×4)、SPI(×2)、PWM(×8)、USB OTG、LCD、Camera

### Linux源码中的信息位置

| 信息类型 | Linux路径 | 提取内容 |
|---------|----------|---------|
| 外设地址/中断 | `arch/arm64/boot/dts/allwinner/sun50i-h616.dtsi` | 外设节点（T507≈H616） |
| 引脚复用表 | `drivers/pinctrl/sunxi/pinctrl-sun50i-h616.c` | 引脚功能表 |
| 时钟树 | `drivers/clk/sunxi-ng/ccu-sun50i-h616.c` | CCU时钟树 |
| 时钟宏 | `include/dt-bindings/clock/sun50i-h616-ccu.h` | 时钟编号 |
| 复位宏 | `include/dt-bindings/reset/sun50i-h616-ccu.h` | 复位信号编号 |

### 提取示例：UART0

**从DTS提取**（`sun50i-h616.dtsi`）：

```dts
uart0: serial@5000000 {
    compatible = "snps,dw-apb-uart";
    reg = <0x5000000 0x400>;            // 基地址: 0x05000000
    interrupts = <GIC_SPI 0 IRQ_TYPE_LEVEL_HIGH>;  // GIC SPI#0
    clocks = <&ccu CLK_BUS_UART0>;      // 总线时钟
    resets = <&ccu RST_BUS_UART0>;      // 复位信号
    status = "disabled";
};
```

**从pinctrl提取**（`pinctrl-sun50i-h616.c`）：

```c
// PH2/PH3 的复用功能：
SUNXI_FUNCTION(0x0, "gpio_in"),        // GPIO输入
SUNXI_FUNCTION(0x1, "gpio_out"),       // GPIO输出
SUNXI_FUNCTION(0x2, "uart0"),          // UART0 TX/RX
```

## 3. Hi3516DV300 — 需海思SDK（ARM Cortex-A7, L1）

### 芯片概况

- 双核 ARM Cortex-A7 @ 900MHz
- 视频处理芯片，ISP/Camera/显示等丰富外设
- L1小型系统典型代表（HiSpark Taurus开发板）

### Linux源码情况

Hi3516DV300 **不在Linux主线内核**中，需从海思SDK获取定制内核源码。海思SDK中通常包含：

| 信息类型 | SDK路径（推测） | 说明 |
|---------|---------------|------|
| DTS | `arch/arm/boot/dts/hi3516dv300*.dts*` | 外设定义 |
| 引脚 | `drivers/pinctrl/hisilicon/pinctrl-hi3516*.c` | 引脚复用 |
| 时钟 | `drivers/clk/hisilicon/` | 时钟驱动 |

### OpenHarmony仓库中的替代来源

海思SDK公开程度有限，可从OpenHarmony仓库间接获取部分信息：

| 信息 | OpenHarmony路径 |
|------|----------------|
| HCS配置（含regBase/irqStart） | `device/soc/hisilicon/hi3516dv300/` 下的 `.hcs` 文件 |
| 驱动代码（含寄存器操作） | `device/soc/hisilicon/hi3516dv300/` 下的驱动源码 |
| 内核适配配置 | `kernel_liteos_a/arch/arm/` 下的芯片配置 |

## 4. Hi3861 — RISC-V L0代表（需海思SDK）

### 芯片概况

- RISC-V 单核 @ 160MHz
- 352KB SRAM + 2MB Flash
- 外设：GPIO(×14)、UART(×2)、I2C(×1)、SPI(×1)、PWM(×6)、ADC(×7)
- 内置Wi-Fi，OpenHarmony L0标杆平台

### Linux源码情况

Hi3861 **不在Linux主线内核**中。作为RISC-V MCU，主要使用FreeRTOS/LiteOS-M，Linux适配有限。

**替代来源**：

| 信息类型 | 来源路径 |
|---------|---------|
| 寄存器宏定义 | `device/soc/hisilicon/hi3861v100/sdk_liteos/platform/include/` |
| 外设基地址 | SDK头文件中的 `*_REG_BASE` 宏 |
| 中断号 | SDK头文件中的 IRQ 枚举 |
| 引脚定义 | SDK头文件中的 pin mux 定义 |

## 5. ESP32-C3 — RISC-V开源生态（ESP-IDF为主）

### 芯片概况

- RISC-V 单核 @ 160MHz
- 内置Wi-Fi/BLE
- 文档开源在GitHub（Markdown + PDF）

### Linux源码情况

ESP32-C3在Linux主线中支持有限。主要硬件信息在ESP-IDF中：

| 信息类型 | ESP-IDF路径 |
|---------|-----------|
| 寄存器定义 | `components/soc/esp32c3/register/soc/*_reg.h` |
| SoC能力 | `components/soc/esp32c3/include/soc/soc_caps.h` |
| GPIO信号映射 | `components/soc/esp32c3/include/soc/gpio_sig_map.h` |
| 外设基地址 | `components/soc/esp32c3/include/soc/soc.h` |

**特点**：ESP-IDF的头文件组织非常清晰，每个外设一个 `*_reg.h` 文件，宏定义命名规范（`REG_BASE` + `OFFSET`），Agent可以直接读取。

## 6. BES2600W — 需贝斯SDK（Cortex-M33）

### 芯片概况

- ARM Cortex-M33 @ 240MHz（TrustZone安全扩展）
- 带LCD显示、音频编解码、Wi-Fi/BT
- L0带屏方案代表

### Linux源码情况

BES2600W **可能没有Linux适配**。作为MCU芯片，主要运行RTOS。需从贝斯集成SDK获取头文件。

**替代来源**：OpenHarmony BES2600 SoC适配仓库（`device/soc/bestechnic/`）中的头文件和驱动代码。

### 官方移植指南（完整工作流样例）

> ⭐ **OpenHarmony 官方发布的 BES2600W Mini系统带屏移植完整教程**，覆盖环境搭建→源码同步→内核移植→HDF驱动→构建配置→编译烧录全流程，是本工作流设计的重要参考依据。

| 资料 | 链接 | 覆盖阶段 |
|------|------|---------|
| BES2600W Mini系统移植指南（Gitee 官方） | [gitee.com/openharmony/docs → porting-bes2600w-on-minisystem-display-demo.md](https://gitee.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-bes2600w-on-minisystem-display-demo.md) | 01~05 全流程 |
| BES2600W Mini系统移植指南（GitHub 镜像） | [github.com/openharmony/docs → porting-bes2600w-on-minisystem-display-demo.md](https://github.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-bes2600w-on-minisystem-display-demo.md) | 01~05 全流程 |

## 7. XR806 / ASR582X — 需厂商SDK

### XR806（全志RISC-V）

- RISC-V E907 @ 160MHz，内置Wi-Fi
- **不在Linux主线**，需全志SDK
- OpenHarmony XR806适配仓库可能有部分头文件

### ASR582X（翱捷RISC-V）

- Cortex-M33内核，WiFi低功耗芯片
- **不在Linux主线**，需翱捷SDK
- SDK公开程度有限，可能需厂商关系获取

## 8. 案例总结：提取策略选择

| 芯片 | 架构 | Linux主线 | 推荐提取路径 |
|------|------|----------|-------------|
| STM32F407 | Cortex-M4 | ✅ 完整 | **Linux DTS + pinctrl + clk** |
| 全志T507 | Cortex-A53 | ✅ 完整 | **Linux DTS + pinctrl + clk** |
| AT32F437 | Cortex-M4 | ⚠️ 兼容STM32 | Linux DTS（可复用STM32模式） |
| Hi3516DV300 | Cortex-A7 | ❌ 需SDK | 海思SDK内核 + OpenHarmony仓库 |
| Hi3861 | RISC-V | ❌ 无 | **SDK头文件** |
| ESP32-C3 | RISC-V | ⚠️ 有限 | **ESP-IDF头文件** |
| BES2600W | Cortex-M33 | ❌ 无 | 贝斯SDK + OpenHarmony仓库 |
| XR806 | RISC-V | ❌ 无 | 全志SDK + OpenHarmony仓库 |
| ASR582X | Cortex-M33 | ❌ 无 | 翱捷SDK |

**关键发现**：9颗典型芯片中，仅STM32F407和全志T507在Linux主线有完整支持。其余芯片需要从厂商SDK或OpenHarmony适配仓库中提取头文件。SKILL工作流应首先检查Linux主线支持情况，无主线支持时自动切换到SDK头文件路径。
