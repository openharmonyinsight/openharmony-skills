# Linux内核源码解读指南

> 本文教Agent**找到源码后怎么读懂它**——如何解读DTS节点、pinctrl定义、时钟树和DT bindings宏。
> 路径查找（文件在哪个目录）→ 见 ohos-dev-kernel-source-query SKILL 的 `linux-paths.md`。
> DTS语法详解 → 见 `dts-parsing-guide.md`。

---

## 1. pinctrl驱动代码解读

pinctrl驱动文件中包含引脚的完整复用信息。不同厂商格式不同，但核心数据相同：每个引脚有哪些可选功能。

### STM32格式：`stm32_desc_pin` 结构体

```c
// drivers/pinctrl/stm32/pinctrl-stm32f429.c
static const struct stm32_desc_pin stm32f429_pins[] = {
    PIN(STM32_PIN(0),       // PA0
        STM32_FUNCTION(0, "GPIOA0"),      // 功能0: GPIO
        STM32_FUNCTION(1, "TIM2_CH1"),    // 功能1: 定时器2通道1
        STM32_FUNCTION(2, "TIM5_CH1"),    // 功能2: 定时器5通道1
        STM32_FUNCTION(7, "USART2_CTS"),  // 功能7: UART2 CTS
        STM32_FUNCTION(14, "ADC123_IN0"), // 功能14: ADC输入
    ),
    // ...
};
```

**Agent提取要点**：
- 每个`PIN()`定义一个引脚，`STM32_FUNCTION(编号, "名称")`列出所有复用功能
- 编号即AF（Alternate Function）编号，对应DTS中PINMUX宏的func参数
- 特殊功能映射：关注UART TX/RX、I2C SDA/SCL、SPI MOSI/MISO等

> 实际代码样本 → `resources/pinctrl-code-samples/stm32-pinctrl-stm32f429.c`

### DTS中的pinctrl节点

DTS通过pinctrl子节点引用驱动中定义的功能：

```dts
/* arch/arm/boot/dts/st/stm32f429-pinctrl.dtsi */
pinctrl: pin-controller@40020000 {
    usart1_pins_a: usart1-0 {
        pins1 {
            pinmux = <STM32_PINMUX('A', 9, AF7)>;  /* TX: PA9, AF7 */
        };
        pins2 {
            pinmux = <STM32_PINMUX('A', 10, AF7)>; /* RX: PA10, AF7 */
        };
    };
};
```

**Agent提取要点**：
- `STM32_PINMUX('A', 9, AF7)` → 端口A、引脚9、复用功能7
- 外设节点通过 `pinctrl-0 = <&usart1_pins_a>` 引用这些引脚配置
- 一个外设可能有多个pinctrl配置（如`usart1_pins_a`和`usart1_pins_b`是不同引脚方案）

> 实际DTS样本 → `resources/dts-samples/stm32f429-pinctrl.dtsi`

---

## 2. 时钟驱动代码解读

Linux使用Common Clock Framework（CCF）描述时钟树。核心概念：

```
时钟源（HSE/LSE/HSI/LSI）→ PLL（倍频）→ 分频器（AHB/APB）→ 门控（外设时钟开关）
```

### 时钟注册模式

```c
// 时钟门控：控制外设时钟的开关
static struct clk_gate usart1_clk = {
    .reg = base + 0x44,       // 时钟门控寄存器地址
    .bit_idx = 4,             // 控制位（写1开启时钟）
    .hw.init = CLK_HW_INIT_PARENTS("usart1", usart1_parents, ...),
};

// 时钟分频器：总线分频
static struct clk_divider apb1_div = {
    .reg = base + 0x08,       // 分频寄存器
    .shift = 10, .width = 3,  // 位域位置
    .hw.init = CLK_HW_INIT("apb1", "ahb", ...),
};

// PLL：倍频
static struct clk_pll stm32f4_pll = {
    .reg = base + 0x00,       // PLL控制寄存器
    .hw.init = CLK_HW_INIT("pll", "hse", ...),
};
```

**Agent提取要点**：
- 时钟源（HSI=内部16MHz、HSE=外部晶振、LSE=32.768kHz）
- 时钟树层次：PLL → AHB → APB1/APB2 → 各外设
- 各外设的时钟门控寄存器地址和位号（写驱动时需要开启时钟）
- 分频系数（AHB/APB1/APB2的分频值，影响外设实际时钟频率）

> 实际代码样本 → `resources/clk-code-samples/`

### DT bindings时钟宏解读

这些宏定义了DTS中引用的时钟编号：

```c
// include/dt-bindings/clock/stm32f4-clock.h
#define STM32F4_AHB1_CLOCK(x)  (x)          // AHB1总线外设编号
#define STM32F4_APB1_CLOCK(x)  (38 + (x))   // APB1总线外设（从38开始）
#define STM32F4_APB2_CLOCK(x)  (96 + (x))   // APB2总线外设（从96开始）

// DTS中使用：clocks = <&rcc 0 STM32F4_APB2_CLOCK(USART1)>;
// 含义：USART1的时钟来自APB2总线
```

```c
// include/dt-bindings/pinctrl/stm32-pinfunc.h
#define STM32_PINMUX(port, pin, func)  \
    (((port - 'A') << 8) | (pin << 4) | (func))
// STM32_PINMUX('A', 9, AF7) → PA9引脚使用复用功能7
```

**Agent提取要点**：
- 时钟宏把外设名映射到编号，编号对应驱动中的时钟注册顺序
- PINMUX宏把端口+引脚+功能编码成一个整数，供DTS引用

> 实际文件 → `resources/clk-code-samples/st-stm32fx-clock.h`、`resources/pinctrl-code-samples/stm32-pinfunc.h`

---

## 3. 各厂商代码特点

路径规律见 `linux-paths.md`，这里记录各厂商的**代码风格和注意事项**：

| 厂商 | 特点 | 注意 |
|------|------|------|
| **ST STM32** | 代码最规范，DTS+驱动分离清晰。CCF标准时钟注册。 | 适合初学者学习 |
| **全志 sunxi** | CCU（Clock Control Unit）统一管理时钟和复位，代码量大但结构一致。pinctrl用`SUNXI_FUNCTION`宏。 | 时钟和复位信号在同一CCU模块 |
| **海思 HiSilicon** | 部分芯片不在Linux主线。UART常用ARM PL011 IP核。 | 需从海思SDK获取定制内核 |
| **Espressif ESP32** | 没有DTS（FreeRTOS不用设备树）。信息在头文件宏定义中。`soc_caps.h`集中定义外设数量。 | 走SDK头文件提取路径 |

---

## 4. 无Linux适配的芯片怎么办

部分MCU芯片（BES2600W、XR806、ASR582X等）没有Linux适配代码。退回到：

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | 芯片SDK头文件 | 寄存器宏定义、基地址、中断号——与Linux头文件等价 |
| 2 | CMSIS-SVD（仅ARM Cortex-M） | 标准化的寄存器XML描述 |
| 3 | PDF Datasheet/Reference Manual | 最后手段 |

**判断方法**：在Linux源码中搜索芯片型号，如果无结果说明该芯片不在Linux主线中。

> SDK头文件提取案例 → `sdk-extraction-cases.md`
