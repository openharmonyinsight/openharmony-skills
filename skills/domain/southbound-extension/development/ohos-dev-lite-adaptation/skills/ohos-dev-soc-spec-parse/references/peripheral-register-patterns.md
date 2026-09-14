# 外设寄存器通用知识

不同芯片的同类外设有共通的寄存器模式。掌握这些模式，Agent能从任何芯片的寄存器定义中正确提取关键信息。

## GPIO寄存器通用模式

### 共通寄存器组

几乎所有MCU的GPIO控制器都包含以下寄存器：

| 寄存器 | 缩写 | 功能 | 典型位宽 |
|--------|------|------|---------|
| 数据/输出寄存器 | ODR/GPIO_OUT/PTOR | 设置引脚输出电平 | 每pin 1bit |
| 输入寄存器 | IDR/GPIO_IN/PDIR | 读取引脚电平 | 每pin 1bit |
| 方向寄存器 | MODER/GPIO_DIR/PDDR | 输入/输出方向 | 每pin 1-2bit |
| 上拉/下拉寄存器 | PUPDR/GPIO_PUDR | 内部上拉/下拉配置 | 每pin 2bit |
| 复用/功能选择 | AFR/GPIO_AF/IOMUX | 引脚复用功能选择 | 每pin 4bit |
| 中断配置 | EXTI/IMR/EMR | 中断触发方式和使能 | 每pin 2-4bit |

### 各芯片GPIO寄存器对照

```
STM32F4 (寄存器结构体模式):
  GPIOx->MODER    → 模式（输入/输出/复用/模拟） 2bit/pin
  GPIOx->OTYPER   → 输出类型（推挽/开漏） 1bit/pin
  GPIOx->OSPEEDR  → 输出速度 2bit/pin
  GPIOx->PUPDR    → 上下拉 2bit/pin
  GPIOx->IDR      → 输入数据（只读）
  GPIOx->ODR      → 输出数据
  GPIOx->AFR[0/1] → 复用功能选择 4bit/pin
  GPIOx->BSRR     → 位设置/复位（写1置位/清零）

Hi3861 (API函数模式，无直接寄存器访问):
  hi_gpio_set_dir(id, dir)          → 方向设置
  hi_gpio_set_output_val(id, val)   → 输出电平
  hi_gpio_get_input_val(id, &val)   → 读取输入
  hi_io_set_func(id, func)          → 引脚复用（通过hi_mux.h）

ESP32-C3 (SoC宏+寄存器模式):
  GPIO_OUT_REG       → 输出数据
  GPIO_IN_REG        → 输入数据
  GPIO_ENABLE_REG    → 方向使能
  GPIO_FUNCn_OUT_SEL_CFG_REG → 输出信号映射
  GPIO_FUNCn_IN_SEL_CFG_REG  → 输入信号映射

BES2600W (HAL函数模式):
  hal_gpio_pin_set_dir(pin, dir)    → 方向
  hal_gpio_pin_set_output(pin, val) → 输出
  hal_gpio_pin_get_val(pin, &val)   → 输入
  hal_iomux_set_xxx(pin)            → 引脚复用
```

### Agent提取要点

- **寄存器基地址**：GPIO控制器在内存映射中的起始地址
- **每组引脚数量**：通常16个pin一组（PortA/PortB/...）
- **复用功能数**：每个pin可选的AF功能数（STM32: 16个, Hi3861: 4-8个）
- **中断线数**：通常与pin数一致，但可能共享中断向量

---

## UART寄存器通用模式

### IP核复用关系

许多SoC不自己设计UART，而是购买IP核授权：

| IP核 | 使用厂商 | Linux compatible | 寄存器特征 |
|------|---------|-----------------|-----------|
| ARM PL011 | 海思、部分NXP | `"arm,pl011"` | 12个32位寄存器，FIFO深度16/32 |
| Synopsys DW 8250 | 全志、Rockchip、部分海思 | `"snps,dw-apb-uart"` | 兼容16550，额外DMA控制寄存器 |
| STM32 USART | ST全系列 | `"st,stm32-uart"` | CR1/CR2/CR3控制寄存器+BRR波特率 |
| ESP32 UART | 乐鑫全系列 | N/A（无Linux） | FIFO_CONF/INT_RAW/CLKDIV |

### 共通寄存器组

| 寄存器 | 功能 | 说明 |
|--------|------|------|
| TX/RX数据 | 发送/接收FIFO | 通常8位或32位宽 |
| 控制寄存器 | 使能、字长、停止位、奇偶校验 | 配置UART工作模式 |
| 状态寄存器 | TX空、RX满、错误标志 | 轮询或中断触发 |
| 波特率分频 | 时钟分频器 | baud = clk / (divisor × oversampling) |
| 中断寄存器 | 中断使能/状态/清除 | TX完成、RX就绪、错误中断 |

### 波特率计算通用公式

```
divisor = uart_clk / (baud_rate × oversampling)

常见过采样倍数：
- 16x过采样（STM32/16550兼容）: divisor = clk / (baud × 16)
- 8x过采样（STM32高速模式）:   divisor = clk / (baud × 8)
```

---

## I2C寄存器通用模式

### IP核复用关系

| IP核 | 使用厂商 | 特征 |
|------|---------|------|
| Synopsys DW I2C | 海思、Rockchip、全志部分 | 寄存器偏移统一，IC_CON/IC_TAR/IC_DATA_CMD |
| Marvell MV64xxx | 全志（sunxi系列） | 兼容MV64340，SR/CR/DR寄存器 |
| STM32 I2C | ST全系列 | CR1/CR2/OAR/DR/CCR |

### 共通操作序列

```
发送数据：
  1. 设置目标地址 → TAR/DR寄存器
  2. 写数据字节 → DATA/CMD寄存器
  3. 等待TX完成 → 读状态寄存器

接收数据：
  1. 设置目标地址 + 读模式
  2. 触发读操作
  3. 等待RX就绪 → 读数据寄存器
```

---

## SPI寄存器通用模式

### 共通寄存器组

| 寄存器 | 功能 |
|--------|------|
| 控制寄存器 | 使能、主从模式、时钟极性/相位（CPOL/CPHA） |
| 数据寄存器 | TX/RX移位寄存器（通常8/16/32位） |
| 状态寄存器 | TX空、RX满、忙标志 |
| 时钟分频 | SPI_CLK = bus_clk / prescaler |
| 片选控制 | CS极性、CS数量 |

### SPI时钟极性/相位

```
CPOL=0, CPHA=0: 空闲低电平，第一边沿采样
CPOL=0, CPHA=1: 空闲低电平，第二边沿采样
CPOL=1, CPHA=0: 空闲高电平，第一边沿采样
CPOL=1, CPHA=1: 空闲高电平，第二边沿采样

→ 这是所有SPI控制器的共通配置项，提取时需标明支持的CPOL/CPHA组合
```

---

## Timer/计数器通用模式

### 共通寄存器组

| 寄存器 | 功能 |
|--------|------|
| 控制寄存器 | 使能、计数方向、模式（定时/计数/PWM） |
| 计数值寄存器 | 当前计数值（CNT/TCNT） |
| 重载/比较值 | 自动重载值（ARR/PRD）和比较值（CCR/OCR） |
| 预分频器 | 时钟分频（PSC/TCLK） |
| 中断寄存器 | 溢出中断、比较匹配中断 |

### 定时计算

```
定时周期 = (重载值 + 1) × (预分频 + 1) / timer_clk

示例：timer_clk=72MHz, PSC=7199, ARR=9999
→ 周期 = 10000 × 7200 / 72000000 = 1秒
```

---

## ADC通用模式

### 共通寄存器组

| 寄存器 | 功能 |
|--------|------|
| 控制寄存器 | 使能、触发源、扫描模式（单次/连续） |
| 通道选择 | 输入通道号（CH0-CH15） |
| 采样时间 | 采样周期配置 |
| 数据寄存器 | 转换结果（12/16位） |
| 状态寄存器 | 转换完成标志（EOC） |
| 中断寄存器 | 转换完成中断使能 |

### 转换参数

```
转换时间 = 采样时间 + 转换时间（固定，如12.5个ADC时钟周期）
分辨率：通常12位（0-4095），参考电压决定LSB值
LSB = Vref / 2^resolution
```

---

## Agent提取检查清单

对每个外设，提取以下信息：

1. **基地址**：外设控制器在内存映射中的起始地址
2. **寄存器偏移**：各功能寄存器相对基地址的偏移
3. **位域定义**：关键寄存器的位域含义
4. **时钟依赖**：外设工作所需的时钟源和使能位
5. **中断号**：外设对应的中断向量号
6. **DMA通道**：如果支持DMA，哪些通道可用
7. **引脚映射**：哪些GPIO引脚可以复用为该外设的信号线
