# 芯片关键硬件信息速查表

> 预提取各芯片最常用的硬件信息，Agent查表即可使用，无需阅读Linux源码或Datasheet。
> 数据来源：Linux主线内核DTS/驱动、芯片SDK头文件、NuttX BSP、OpenHarmony适配仓库。
> ✅ 以下数据均经过Linux内核查询工作流验证，标注来源路径。

---

## STM32F407 — ARM Cortex-M4F（数据最完整）

**来源**：Linux主线 `arch/arm/boot/dts/st/stm32f429.dtsi`（stm32f429为F407超集，DTS兼容）+ STM32CubeF4 SDK + `drivers/clk/stm32/clk-stm32f4.c`

### 基本信息

| 项目 | 值 |
|------|-----|
| CPU | ARM Cortex-M4F (带FPU) |
| 主频 | 168 MHz |
| Flash | 2MB @ 0x08000000（板级配置，不在.dtsi中） |
| SRAM | 256KB @ 0x20000000（板级配置，不在.dtsi中） |
| CCM RAM | 64KB @ 0x10000000（板级配置，不在.dtsi中） |
| 中断控制器 | ARM NVIC (armv7m-nvic) @ 0xE000E100 |
| EXTI | 0x40013C00 |

> ⚠️ Flash/SRAM容量为板级配置（在board .dts中定义），.dtsi仅描述外设寄存器映射。上述为STM32F429IGT6典型值，F407具体型号可能不同。

### 时钟树（验证自 `drivers/clk/stm32/clk-stm32f4.c`）

```
Root Clocks:
  HSE (板级晶振, 通常8MHz) / HSI (16MHz内部) / LSE (32768Hz) / LSI (32kHz)

PLL:
  VCO = HSE_or_HSI × N (192-432)
  ├── PLL-P (÷2/4/6/8) → SYSCLK
  └── PLL-Q (÷2-15)   → pll48 (USB/SDIO/RNG)

PLLI2S: 用于I2S音频
PLLSAI: 用于LCD-TFT (LTDC)

Bus Divider:
  SYSCLK → AHB_DIV → APB1_DIV (×2 for timers) → APB2_DIV (×2 for timers)

RCC Registers:
  CR       @ offset 0x00    PLLCFGR @ offset 0x04
  CFGR     @ offset 0x08    AHB1ENR @ offset 0x30
  APB1ENR  @ offset 0x40    APB2ENR @ offset 0x44
```

### GPIO控制器

| 端口 | 基地址 | 引脚数 | 备注 |
|------|--------|--------|------|
| GPIOA | 0x40020000 | 16 (PA0-PA15) | |
| GPIOB | 0x40020400 | 16 | |
| GPIOC | 0x40020800 | 16 | |
| GPIOD | 0x40020C00 | 16 | |
| GPIOE | 0x40021000 | 16 | |
| GPIOF | 0x40021400 | 16 | |
| GPIOG | 0x40021800 | 16 | |
| GPIOH | 0x40021C00 | 16 | |
| GPIOI | 0x40022000 | 16 | |
| GPIOJ | 0x40022400 | 16 | |
| GPIOK | 0x40022800 | 8 (PK0-PK7) | F429新增 |

> 共11个端口，168个引脚（GPIOA-GPIOJ各16pin，GPIOK 8pin）。步长 0x400。

### 完整外设基地址和中断号（从 stm32f429.dtsi 提取）

#### APB1 外设

| 外设 | 基地址 | 中断号(NVIC) | 说明 |
|------|--------|-------------|------|
| TIM2 | 0x40000000 | 28 | 通用定时器 |
| TIM3 | 0x40000400 | 29 | 通用定时器 |
| TIM4 | 0x40000800 | 30 | 通用定时器 |
| TIM5 | 0x40000C00 | 50 | 通用定时器 |
| TIM6 | 0x40001000 | 54 | DAC定时器 |
| TIM7 | 0x40001400 | 55 | DAC定时器 |
| TIM12 | 0x40001800 | — | 通用定时器 |
| TIM13 | 0x40001C00 | — | 通用定时器 |
| TIM14 | 0x40002000 | — | 通用定时器 |
| RTC | 0x40002800 | 17 | 实时时钟 |
| IWDG | 0x40003000 | — | 独立看门狗 |
| SPI2 | 0x40003800 | 36 | |
| SPI3 | 0x40003C00 | 51 | |
| USART2 | 0x40004400 | 38 | |
| USART3 | 0x40004800 | 39 | |
| UART4 | 0x40004C00 | 52 | |
| UART5 | 0x40005000 | 53 | |
| I2C1 | 0x40005400 | 31(EV)/32(ER) | |
| I2C3 | 0x40005C00 | 72(EV)/73(ER) | |
| CAN1 | 0x40006400 | 19-22 | TX/RX/SCE/WAKEUP |
| CAN2 | 0x40006800 | 63-66 | TX/RX/SCE/WAKEUP |
| PWR | 0x40007000 | — | 电源控制 |
| DAC | 0x40007400 | — | 数模转换 |
| UART7 | 0x40007800 | 82 | F429新增 |
| UART8 | 0x40007C00 | 83 | F429新增 |

#### APB2 外设

| 外设 | 基地址 | 中断号(NVIC) | 说明 |
|------|--------|-------------|------|
| TIM1 | 0x40010000 | 24-27 | 高级定时器 |
| TIM8 | 0x40010400 | 43-46 | 高级定时器 |
| USART1 | 0x40011000 | 37 | |
| USART6 | 0x40011400 | 71 | |
| ADC | 0x40012000 | 18 | ADC1/2/3共享IRQ，子通道区分 |
| SDIO | 0x40012C00 | 49 | SD卡接口 |
| SPI1 | 0x40013000 | 35 | |
| SPI4 | 0x40013400 | 84 | F429新增 |
| SYSCFG | 0x40013800 | — | 系统配置 |
| EXTI | 0x40013C00 | 5-10/23/40 | 外部中断 |
| TIM9 | 0x40014000 | — | 通用定时器 |
| TIM10 | 0x40014400 | — | 通用定时器 |
| TIM11 | 0x40014800 | — | 通用定时器 |
| SPI5 | 0x40015000 | 85 | F429新增 |
| SPI6 | 0x40015400 | 86 | F429新增 |
| LTDC | 0x40016800 | 88/89 | LCD-TFT控制器(F429新增) |

#### AHB1 外设

| 外设 | 基地址 | 中断号(NVIC) | 说明 |
|------|--------|-------------|------|
| CRC | 0x40023000 | — | CRC计算单元 |
| RCC | 0x40023800 | — | 时钟控制寄存器 |
| DMA1 | 0x40026000 | 11-17/47 | 8流×8通道 |
| DMA2 | 0x40026400 | 56-60/68-70 | 8流×8通道 |
| ETH MAC | 0x40028000 | 61 | 以太网MAC |
| DMA2D | 0x4002B000 | 90 | 2D图形加速器(F429新增) |
| USB OTG HS | 0x40040000 | 77 | USB高速OTG |

#### AHB2 外设

| 外设 | 基地址 | 中断号(NVIC) | 说明 |
|------|--------|-------------|------|
| USB OTG FS | 0x50000000 | 67 | USB全速OTG |
| DCMI | 0x50050000 | 78 | 数字摄像头接口 |
| RNG | 0x50060800 | — | 随机数生成器 |

### 常用引脚复用（参考默认功能）

```
USART1: TX:PA9(AF7), RX:PA10(AF7)
USART2: TX:PA2(AF7), RX:PA3(AF7)
USART3: TX:PB10(AF7), RX:PB11(AF7)
UART4:  TX:PA0(AF8), RX:PA1(AF8)
UART5:  TX:PC12(AF8), RX:PD2(AF8)
USART6: TX:PC6(AF8), RX:PC7(AF8)
I2C1:   SCL:PB6(AF4), SDA:PB7(AF4)
I2C3:   SCL:PA8(AF4), SDA:PC9(AF4)
SPI1:   SCK:PA5(AF5), MISO:PA6(AF5), MOSI:PA7(AF5)
SPI2:   SCK:PB13(AF5), MISO:PB14(AF5), MOSI:PB15(AF5)
SPI3:   SCK:PB3(AF6), MISO:PB4(AF6), MOSI:PB5(AF6)
TIM1:   CH1:PA8(AF1), CH2:PA9(AF1)
TIM2:   CH1:PA0(AF1), CH2:PA1(AF1)
ADC1:   IN0:PA0, IN1:PA1, ...
```

---

## Hi3516CV610 — ARM Cortex-A7 双核 SMP（L1视频SoC，内置 DDR 多变体）

**来源**：Hi3516CV610 产品简介「型号配置差异」表 + 厂商 SDK `boards/dmeb/tools/pc/boot_tools/` xlsm 文件名 + `boards/dmeb/Makefile`；CPU/主频依据服务器 SDK `autoconf.h` CONFIG_SMP=1 + DTS `cpu@0`/`cpu@1` clock-frequency=HI3516CV610_FIXED_1200M

### 基本信息

| 项目 | 值 |
|------|-----|
| CPU | ARM Cortex-A7 双核 SMP |
| 主频 | 1200 MHz |
| MMU | ✅ 有 |
| 中断控制器 | ARM GIC |
| 系统级别 | L1小型系统（LiteOS-A / Linux） |
| DDR 总线位宽 | 16-bit |
| 封装 | QFN9×9（内置 DDR 变体） / TFBGA（外置 DDR 变体） |

### ⚠️ 内置 DDR 变体（同型号 SoC 多变体，裸烧 reg_info 必须按变体选 xlsm）

| 变体后缀 | DDR 类型 | DDR 速率 | DDR 容量 | 封装 | 对应 .xlsm | 备注 |
|---------|---------|---------|---------|------|-----------|------|
| **-10B** | DDR2 | 1333 Mbps | 64 MB (512 Mb) | QFN9×9 | `Hi3516CV610-DMEB_4L_DDR2_1333M_64MB_16bit-A7_950M_QFN.xlsm` | 内置 DDR，KOL 加 `_24M` |
| **-20S** | DDR3 | 2133 Mbps | 128 MB (1 Gb) | QFN9×9 | `Hi3516CV610-DMEB_4L_DDR3_2133M_128MB_16bit-A7_950M_QFN.xlsm` | 内置 DDR，KOL 加 `_24M` |
| **-20G** | DDR3 | 2133 Mbps | 128 MB (1 Gb) | QFN9×9 | 同 -20S | 与 -20S 同 DDR 参数 |
| **-00S** | DDR3 | 2133 Mbps | 最大 4 Gb（xlsm 按 512 MB） | TFBGA | `Hi3516CV610-DMEB_4L_DDR3_2133M_512MB_16bit-A7_950M_BGA.xlsm` | **外置** DDR，KOL 加 `_24M` |
| **-00G** | DDR3 | 2133 Mbps | 最大 4 Gb | TFBGA | 同 -00S | 与 -00S 同 DDR 接口 |

> **裸烧关键**：-10B（DDR2 64MB）与 -20S/-20G（DDR3 128MB）的 xlsm 不可互换，错配会导致 DDR Training 失败 / 烧到 100% 但 uboot 起不来。完整鉴别流程、reg_info 生成命令（magic=`2b8c6e1a1a6e8c2b`）、错配症状诊断见 `references/ddr-variant-guide.md`。

> CV608 板专用 xlsm：`Hi3516CV608-DMEB_4L_DDR2_1333M_64MB_16bit-A7_950M_QFN.xlsm`（非 CV610）。

### reg_info 生成入口

```
变量 REGBIN_XLSM（按 CHIP 选，KOL=1 加 _24M）
  → xlsm_to_bin.py <xlsm> reg_info.bin -magic 2b8c6e1a1a6e8c2b
  → reg_info.bin + gsl.bin(~20KB, components/gsl 源码 make CHIP=xxx) → image_tool/oem_quick_build.py → boot_image.bin
```

> 寄存器基地址/中断号/外设表待从厂商 SDK 头文件补充（视频 SoC，L1 不强制寄存器位域）。

---

## Hi3516DV300 — ARM Cortex-A7 双核（L1视频SoC）

**来源**：HiSilicon vendor kernel fork (Linux 4.9-based)，非Linux主线

### 基本信息

| 项目 | 值 |
|------|-----|
| CPU | ARM Cortex-A7 双核 |
| 主频 | 1000 MHz |
| DDR | 512MB @ 0x82000000 |
| MMU | ✅ 有 |
| 中断控制器 | ARM GIC (arm,cortex-a7-gic) |
| GIC Distributor | 0x10301000 |
| GIC CPU Interface | 0x10302000 |
| 系统级别 | L1小型系统（LiteOS-A） |

### 外设基地址和中断号

| 外设 | 基地址 | 中断号(GIC) | 说明 |
|------|--------|------------|------|
| UART0 | 0x120A0000 | 6 | PL011, 调试串口 |
| UART1 | 0x120A1000 | 7 | PL011 |
| UART2 | 0x120A2000 | 8 | PL011 |
| UART3 | 0x120A3000 | 9 | PL011 |
| UART4 | 0x120A4000 | 10 | PL011 |
| I2C0 | 0x120B0000 | — | hibvt-i2c, 带DMA |
| I2C1 | 0x120B1000 | — | hibvt-i2c, 带DMA |
| I2C2 | 0x120B2000 | — | hibvt-i2c, 带DMA |
| I2C3 | 0x120B3000 | — | hibvt-i2c, 带DMA |
| I2C4 | 0x120B4000 | — | hibvt-i2c, 带DMA |
| I2C5 | 0x120B5000 | — | hibvt-i2c, 带DMA |
| I2C6 | 0x120B6000 | — | hibvt-i2c, 带DMA |
| I2C7 | 0x120B7000 | — | hibvt-i2c, 带DMA |
| SPI0 | 0x120C0000 | — | PL022, max 50MHz |
| SPI1 | 0x120C1000 | — | PL022, max 50MHz |
| SPI2 | 0x120C2000 | — | PL022, max 50MHz |
| GPIO0 | 0x120D0000 | 16 | PL061, 8 pins |
| GPIO1 | 0x120D1000 | 17 | PL061, 8 pins |
| GPIO2 | 0x120D2000 | 18 | PL061, 8 pins |
| GPIO3 | 0x120D3000 | 19 | PL061, 8 pins |
| GPIO4 | 0x120D4000 | 20 | PL061, 8 pins |
| GPIO5 | 0x120D5000 | 21 | PL061, 8 pins |
| GPIO6 | 0x120D6000 | 22 | PL061, 8 pins |
| GPIO7 | 0x120D7000 | 23 | PL061, 8 pins |
| GPIO8 | 0x120D8000 | 24 | PL061, 8 pins |
| GPIO9 | 0x120D9000 | 25 | PL061, 8 pins |
| GPIO10 | 0x120DA000 | 26 | PL061, 8 pins |
| GPIO11 | 0x120DB000 | 80 | PL061, 8 pins |
| ETH (FEMAC) | 0x10010000 | 32 | RMII接口 |
| MMC0 | 0x10100000 | — | max 100MHz |
| MMC1 | 0x100F0000 | — | max 100MHz |
| MMC2 | 0x10020000 | — | max 100MHz |
| USB (XHCI) | 0x100E0000 | 27 | USB 3.0 |
| DMA | 0x10060000 | 28 | 8通道 |
| CRG (时钟) | 0x12010000 | — | 28固定速率振荡器 + MUX/gate树 |

### ISP多媒体管线

| 模块 | 基地址 | 说明 |
|------|--------|------|
| MIPI RX | 0x113A0000 | MIPI CSI接收 |
| VI | 0x11300000 | 视频输入 |
| VPSS | 0x11040000 | 视频处理子系统 |
| NNIE | 0x11100000 | 神经网络推理引擎 |
| VEDU | 0x11500000 | 视频编解码单元 |
| HDMI | 0x11400000 | HDMI输出 |

### GPIO汇总

- 12组 (GPIO0-GPIO11)，每组8引脚，共96个GPIO
- 基地址步进: 0x1000
- 中断号: 16-26, 80
- 控制器: PL061

---

## 全志T507 — ARM Cortex-A53 四核（L1 MPU）

**来源**：Linux主线 `arch/arm64/boot/dts/allwinner/sun50i-h616.dtsi`（T507为H616车规版本，DTS共用）

### 基本信息

| 项目 | 值 |
|------|-----|
| CPU | ARM Cortex-A53 ×4, PSCI enable |
| 主频 | 1.8 GHz |
| RAM | DDR3/LPDDR4 (外置，通常1-2GB) |
| MMU | ✅ 有 |
| 中断控制器 | ARM GIC-400 @ 0x03021000 |
| PMU IRQ | 140-143 (per-core) |
| NMI控制器 | 0x07010320, GIC_SPI 103 |
| 系统级别 | L1小型系统（LiteOS-A） |

### 外设基地址和中断号

| 外设 | 基地址 | 中断号(GIC SPI) | 说明 |
|------|--------|----------------|------|
| MMC0 | 0x04020000 | 35 | max 150MHz |
| MMC1 | 0x04021000 | 36 | max 150MHz |
| MMC2 | 0x04022000 | 37 | max 150MHz |
| NAND | 0x04011000 | 34 | |
| UART0 | 0x05000000 | 0 | DW APB UART, DMA ch 14 |
| UART1 | 0x05000400 | 1 | DW APB UART, DMA ch 15 |
| UART2 | 0x05000800 | 2 | DW APB UART, DMA ch 16 |
| UART3 | 0x05000C00 | 3 | DW APB UART, DMA ch 17 |
| UART4 | 0x05001000 | 4 | DW APB UART, DMA ch 18 |
| UART5 | 0x05001400 | 5 | DW APB UART, DMA ch 19 |
| I2C0 | 0x05002000 | 6 | DMA ch 43 |
| I2C1 | 0x05002400 | 7 | DMA ch 44 |
| I2C2 | 0x05002800 | 8 | DMA ch 45 |
| I2C3 | 0x05002C00 | 9 | DMA ch 46 |
| I2C4 | 0x05003000 | 10 | DMA ch 47 |
| R_I2C | 0x07081400 | 105 | ARISC域I2C |
| SPI0 | 0x05010000 | 12 | DMA ch 22 |
| SPI1 | 0x05011000 | 13 | DMA ch 23 |
| EMAC | 0x05020000 | 14 | RGMII on PI0-PI16 |
| USB OTG (MUSB) | 0x05100000 | 25 | USB 2.0 OTG |
| EHCI0 | — | 26 | USB 2.0 Host Port 0 |
| OHCI0 | — | 27 | USB 2.0 Host Port 0 |
| EHCI1 | — | 28 | USB 2.0 Host Port 1 |
| OHCI1 | — | 29 | USB 2.0 Host Port 1 |
| EHCI2 | — | 30 | USB 2.0 Host Port 2 |
| OHCI2 | — | 31 | USB 2.0 Host Port 2 |
| EHCI3 | — | 32 | USB 2.0 Host Port 3 |
| OHCI3 | — | 33 | USB 2.0 Host Port 3 |
| GPU (Mali Bifrost) | 0x01800000 | 95-97 | |
| Crypto | 0x01904000 | 91 | 加密引擎 |
| CCU (时钟) | 0x03001000 | — | ~90+ clocks from 24MHz oscillator |
| DMA | 0x03002000 | — | 16 channels, 49 requests |
| Pinctrl | 0x0300B000 | 51-57, 43 | 8 interrupt lines, 137 pin function entries |
| RTC | 0x07000000 | 104 | 实时时钟 |
| Thermal | — | — | 4 sensors (CPU/GPU/VE/DDR) |

### 热管理

| 传感器 | 被动降温阈值 | 临界温度 |
|--------|-------------|---------|
| CPU | 60-70°C | 110°C |
| GPU | 60-70°C | 110°C |
| VE | 60-70°C | 110°C |
| DDR | 60-70°C | 110°C |

### 常用引脚复用

```
UART0 default: PH0(TX), PH1(RX)          — pinctrl entry
I2C0:        PH5(SDA), PH6(SCL)          — function mux
SPI0:        PC0(CLK), PC1(MOSI), PC2(MISO), PC3(CS)
EMAC RGMII:  PI0-PI16
```

---

## AT32F437 — ARM Cortex-M4（兼容STM32）

**来源**：Apache NuttX (`boards/arm/at32/at32f437-mini/`)，非Linux主线（无MMU）

### 基本信息

| 项目 | 值 |
|------|-----|
| CPU | ARM Cortex-M4F @ 288MHz |
| Flash | 4032KB @ 0x08000000 |
| SRAM | 384KB @ 0x20000000 |
| 中断控制器 | ARM NVIC |

### Flash分区（来自NuttX linker script）

| 分区 | 大小 | 起始地址 | 用途 |
|------|------|---------|------|
| kflash | 128KB | 0x08000000 | Kernel Flash |
| uflash | 128KB | 0x08020000 | User Flash |
| xflash | 3776KB | 0x08040000 | Extended Flash |

### 引脚映射（验证自NuttX board config）

```
USART1:      TX=PA9,  RX=PA10
USART2:      TX=PD5,  RX=PD6
CAN1:        TX=PD1,  RX=PD0
USB OTG FS1: D+=PA12, D-=PA11
SDIO1:       CMD=PD2, CLK=PC12, D0=PC8, D1=PC9, D2=PC10, D3=PC11
ETH RMII (LAN8720A): REF_CLK=PA1, MDIO=PA2, MDC=PC1, CRS_DV=PA7,
                     RXD0=PC4, RXD1=PC5, TX_EN=PB11, TXD0=PB12, TXD1=PB13
SPI (W25QXX): CLK=PB3, MISO=PB4, MOSI=PB5, CS=PD7
```

### 与STM32F407的兼容性

AT32F437外设基地址与STM32F407 **完全相同**（兼容寄存器布局）：

| 模块 | 基地址 | 与STM32F407 |
|------|--------|------------|
| GPIOA-I | 0x40020000 + port×0x400 | ✅ 相同 |
| USART1 | 0x40011000 | ✅ 相同 |
| I2C1 | 0x40005400 | ✅ 相同 |
| SPI1 | 0x40013000 | ✅ 相同 |
| RCC | 0x40023800 | ✅ 相同 |
| ADC1 | 0x40012000 | ✅ 相同 |

> AT32F437的GPIO、UART、I2C、SPI等外设基地址和中断号与STM32F407相同，可直接参考上方STM32F407完整外设表。差异仅在时钟树（288MHz vs 168MHz）、Flash容量（4032KB vs 2MB）和部分新增外设。

---

## Hi3861 — RISC-V（L0 WiFi SoC）

**来源**：OpenHarmony `device/soc/hisilicon/hi3861v100/` + koendv/hi3861_notes，非Linux（352KB SRAM，无MMU）

### 基本信息

| 项目 | 值 |
|------|-----|
| CPU | RISC-V RV32IMC 单核 |
| 主频 | 160 MHz |
| SRAM | 352KB |
| ROM | 288KB |
| 无线 | Wi-Fi 2.4GHz 802.11b/g/n (集成RF/PA/LNA/balun) |

### 外设信息

| 外设 | 数量 | 说明 |
|------|------|------|
| GPIO | 14个 (GPIO_0 ~ GPIO_13) | 部分引脚复用WiFi |
| UART | 2个 (UART0, UART1) | UART0用于调试(115200) |
| I2C | 1个 | 标准/快速模式 |
| SPI | 1个 | Master模式 |
| PWM | 6通道 | 频率可调 |
| ADC | 7通道 | 12-bit分辨率 |
| SDIO | 2.0 | SD卡接口 |

> ⚠️ 寄存器基地址和中断号需从SDK头文件中提取（`hi_stdlib.h`、`hi_io.h`等），此处未列出具体数值。

---

## ESP32-C3 — RISC-V（开源生态）

**来源**：ESP-IDF `components/soc/esp32c3/include/soc/` + OpenHarmony `device/soc/espressif/`，非Linux（400KB SRAM，无MMU）

### 基本信息

| 项目 | 值 |
|------|-----|
| CPU | RISC-V RV32IMC 单核 |
| 主频 | 160 MHz |
| SRAM | 400KB |
| Flash | 外挂SPI Flash (最大16MB) |
| 中断控制器 | RISC-V标准中断 |
| 无线 | Wi-Fi 802.11b/g/n + BLE 5.0 (内置) |

### 外设基地址（验证自ESP-IDF soc header）

| 外设 | 基地址 | 数量/说明 |
|------|--------|----------|
| UART0 | 0x60000000 | 调试串口 |
| UART1 | 0x60010000 | — |
| GPIO | 0x60004000 | 22个引脚 (GPIO0-GPIO21) |
| I2C | 0x60013000 | 1个 |
| SPI2 | 0x60024000 | 通用SPI |
| LEDC (PWM) | 0x60019000 | 6通道 |
| ADC1 | 0x6000E000 | 5通道, 12-bit |
| TIMG0 | 0x6001F000 | 定时器组0 |
| TIMG1 | 0x60020000 | 定时器组1 |
| TWAI (CAN) | 0x6002B000 | 1个 |

### GPIO信号映射（部分）

```
GPIO0  → 可配置: UART0_TXD, SPI2_CS0, I2C_SDA, LEDC_CH0
GPIO1  → 可配置: UART0_RXD, SPI2_CLK, I2C_SCL, LEDC_CH1
GPIO2  → 可配置: SPI2_MISO, ADC1_CH0
GPIO3  → 可配置: SPI2_MOSI, ADC1_CH1
GPIO4-GPIO21 → 类似可配置，详见 gpio_sig_map.h
```

---

## BES2600W — ARM Cortex-M33（L0带屏SoC）

**来源**：OpenHarmony `device/soc/bestechnic/bes2600/`，非Linux主线

### 基本信息

| 项目 | 值 |
|------|-----|
| CPU | ARM Cortex-M33 (STAR-MC1, TrustZone) |
| Flash | NOR XIP, 最大32MB |
| Filesystem | littlefs @ 0xB60000, 4MB |
| Kernel | LiteOS-M v3.0.0 |
| 无线 | Wi-Fi 802.11b/g/n + BT (内置) |
| 显示 | LCD (RGB/MCU接口) |
| 音频 | 编解码器 (内置) |

### Boot分区布局

| 分区 | 起始地址 | 结束地址 | 说明 |
|------|---------|---------|------|
| BOOT1 | 0x00000000 | 0x00010000 | 一级Bootloader |
| BOOT2 | 0x2C010000 | — | 二级Bootloader |
| OTA | 0x2C020000 | — | OTA升级区 |
| RTOS_MAIN | 0x2C080000 | 0x2C860000 | 主固件 |

### 外设信息

| 外设 | 数量 | 说明 |
|------|------|------|
| GPIO | 多组 | 具体数量需从SDK确认 |
| UART | 多个 | UART0用于调试 |
| I2C | ≥1 | — |
| SPI | ≥1 | — |
| PWM | 多个 | — |
| LCD | 1 | RGB/MCU LCD接口 |
| I2S | 1 | 音频接口 |

> ⚠️ 寄存器基地址和中断号需从贝斯集成SDK获取，公开资料有限。

---

## XR806 — ARM Cortex-M33（全志WiFi MCU）

**来源**：GitCode XR806 Org + docs.aw-ol.com/xr806/，非Linux（独立MCU，非SDIO slave）

### 基本信息

| 项目 | 值 |
|------|-----|
| CPU | ARM Cortex-M33 @ 160MHz |
| SRAM | 320KB |
| ROM | 160KB |
| 封装 | QFN32 4×4mm |
| 无线 | Wi-Fi 2.4GHz b/g/n + BLE 5.0 |

> ⚠️ **重要更正**：XR806文档中标注为RISC-V E907，但实际硬件为ARM Cortex-M33。以实际硬件为准。

### 外设信息

| 外设 | 数量 | 说明 |
|------|------|------|
| GPIO | 2组 | — |
| UART | 3个 | — |
| I2C | 2个 | — |
| SPI | 2个 | — |
| PWM | 8通道 | — |
| ADC | 6通道 | — |

> ⚠️ 寄存器基地址和中断号需从全志SDK获取。

---

## ASR582X — ARM IoT WiFi+BLE MCU（翱捷）

**来源**：OpenHarmony `device/soc/asrmicro/asr582x/`，非Linux（RTOS-class IoT SoC）

### 基本信息

| 项目 | 值 |
|------|-----|
| CPU | ARM Cortex-M4 @ 160MHz |
| 无线 | Wi-Fi 1T1R 802.11b/g/n + BLE 5.1 |
| 封装 | QFN40 (5×5mm) |
| Full OpenHarmony path | device/soc/asrmicro/asr582x/ |

> ⚠️ **注意**：OpenHarmony Kconfig标注为Cortex-M4；ASR官方文档在较新变体中标注为STAR-MC1/Cortex-M33。以具体使用的芯片变体为准。

### 外设信息

| 外设 | 说明 |
|------|------|
| UART | 多路 |
| SPI | 多路 |
| I2C | 多路 |
| PWM | 多通道 |
| I2S | 音频接口 |
| ADC | 8通道 |
| SDIO | SD卡接口 |

> ⚠️ 详细寄存器基地址和中断号需从翱捷SDK获取，公开资料有限。

---

## 速查表使用说明

### 数据来源和可信度

| 芯片 | 数据来源 | 验证方式 | 可信度 | 建议 |
|------|---------|---------|--------|------|
| STM32F407 | Linux主线 `stm32f429.dtsi` + `clk-stm32f4.c` | DTS节点遍历 + 时钟驱动源码 | ✅ 高 | 直接使用，可查Linux源码核对 |
| Hi3516CV610 | 产品简介「型号配置差异」表 + SDK boot_tools xlsm + Makefile | xlsm 文件名 + Makefile target 交叉验证 | ✅ 高 | DDR 变体/xlsm 对应表可直接用，寄存器表待 SDK 补充 |
| Hi3516DV300 | HiSilicon vendor kernel fork (Linux 4.9) | Vendor DTS提取 | ✅ 高 | 非主线但经vendor DTS验证 |
| 全志T507 | Linux主线 `sun50i-h616.dtsi` | DTS节点遍历 | ✅ 高 | 直接使用，可查Linux源码核对 |
| AT32F437 | Apache NuttX BSP (`at32f437-mini/`) | Linker script + board config | ✅ 高 | 外设地址同STM32F407，已验证 |
| ESP32-C3 | ESP-IDF soc headers | 头文件地址宏验证 | ✅ 高 | 直接使用，可查ESP-IDF核对 |
| Hi3861 | OpenHarmony SDK + koendv/hi3861_notes | SDK头文件交叉验证 | ⚠️ 中 | 基地址/中断号需从SDK头文件补充 |
| BES2600W | OpenHarmony `device/soc/bestechnic/bes2600/` | Boot layout + Kconfig验证 | ⚠️ 中 | 外设地址需贝斯SDK补充 |
| XR806 | GitCode XR806 Org + docs.aw-ol.com | 文档验证(CPU类型已更正) | ⚠️ 中 | 需全志SDK补充寄存器地址 |
| ASR582X | OpenHarmony `device/soc/asrmicro/asr582x/` | Kconfig + 目录结构验证 | ⚠️ 中 | CPU型号存在M4/M33分歧，需确认变体 |

### 如何补充不完整的数据

对于标注 ⚠️ 的芯片，按以下方法补充：

1. **有Linux主线支持的**：用 `linux-source-guide.md` 中的方法，在Linux源码中搜索芯片型号
2. **有Vendor Kernel的**：在厂商fork内核的DTS中搜索兼容字符串和reg属性
3. **无Linux支持但有SDK/NuttX的**：在SDK/BSP头文件中搜索 `REG_BASE`、`IRQ`、`_ADDR` 等关键词
4. **仅有OpenHarmony适配的**：从OpenHarmony适配仓库中的驱动代码反推寄存器和中断号
5. **无任何源码的**：联系厂商获取SDK或技术参考手册
