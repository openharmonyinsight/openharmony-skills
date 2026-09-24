# DTS语法解读指南

> 本文教Agent如何阅读Device Tree Source（DTS）文件，从中提取芯片硬件信息。DTS是Linux内核描述硬件拓扑的标准格式，包含了外设的寄存器地址、中断号、时钟源、引脚配置等关键信息。

## 1. DTS基本语法

### 1.1 节点结构

DTS用树形结构描述硬件，每个节点代表一个硬件设备或子系统：

```dts
/ {
    /* 根节点 */
    model = "STMicroelectronics STM32F429i-Discovery board";
    compatible = "st,stm32f429i-disco", "st,stm32f429";

    soc {
        /* SoC节点，包含所有片内外设 */
        usart1: serial@40011000 {
            compatible = "st,stm32-usart";
            reg = <0x40011000 0x400>;
            interrupts = <37>;
            clocks = <&rcc 0 STM32F4_APB2_CLOCK(USART1)>;
            status = "disabled";
        };
    };
};
```

**关键概念**：
- **标签**（`usart1:`）：节点引用名，其他节点可通过 `&usart1` 引用
- **节点名**（`serial@40011000`）：格式为 `设备类型@基地址`
- **属性**（`compatible`, `reg` 等）：键值对，描述设备特征

### 1.2 `.dtsi` vs `.dts`

```
stm32f429.dtsi    ← SoC级：定义芯片所有外设（这是芯片规格来源）
  └── stm32f429i-disco.dts  ← 板级：选择启用哪些外设、配置引脚
```

- **`.dtsi`** 是芯片级的硬件描述，包含所有外设节点的完整定义
- **`.dts`** 是板级的，通过 `&usart1 { status = "okay"; }` 启用外设

**提取芯片规格时，主要读 `.dtsi` 文件。**

## 2. 核心属性详解

### 2.1 `compatible` — 设备类型标识

格式：`"vendor,device-model"` 或 `"generic-name"`

```dts
compatible = "st,stm32f429-usart", "st,stm32-usart";
```

- 第一个值是最精确的匹配（芯片型号+外设）
- 后面的值是通用兼容（系列级别）
- **对适配的启示**：Agent可通过 `compatible` 判断该外设属于哪个驱动框架

### 2.2 `reg` — 寄存器地址

格式：`<基地址 大小>` 或 `<基地址 大小 基地址2 大小2 ...>`（多段）

```dts
/* 单段：USART1在0x40011000，占用0x400字节 */
reg = <0x40011000 0x400>;

/* 多段：I2C有控制寄存器和数据寄存器两个区域 */
reg = <0x40005400 0x400>, <0x40005800 0x400>;
reg-names = "ctrl", "data";
```

**提取目标**：每个外设的物理基地址和寄存器区域大小。

### 2.3 `interrupts` — 中断配置

中断格式因中断控制器而异：

**ARM Cortex-M（NVIC）**：

```dts
/* 格式：<中断号> */
interrupts = <37>;           /* USART1 = NVIC IRQ#37 */
interrupts = <38>;           /* USART2 = NVIC IRQ#38 */
```

**ARM Cortex-A（GIC）**：

```dts
/* 格式：<类型 中断号 触发方式> */
interrupts = <GIC_SPI 34 IRQ_TYPE_LEVEL_HIGH>;
/* GIC_SPI = 0 (共享中断), GIC_PPI = 1 (私有中断) */
/* IRQ_TYPE_LEVEL_HIGH=4, IRQ_TYPE_EDGE_RISING=1 */
```

**RISC-V（PLIC/CLINT）**：

```dts
/* 格式：<中断号>（PLIC）*/
interrupts = <5>;            /* UART0 = PLIC IRQ#5 */

/* 或使用中断父节点的扩展格式 */
interrupt-parent = <&plic>;
interrupts = <5 1>;          /* IRQ#5, 优先级1 */
```

**提取目标**：每个外设的中断号和触发方式，映射到中断向量表。

### 2.4 `clocks` — 时钟源

格式：`<&时钟控制器节点 参数1 参数2 ...>`

```dts
/* STM32F4：引用rcc时钟控制器，参数为总线类型+外设编号 */
clocks = <&rcc 0 STM32F4_APB2_CLOCK(USART1)>;

/* 全志sunxi：引用ccu时钟控制器，参数为时钟ID */
clocks = <&ccu CLK_BUS_UART0>;
clock-names = "ahb", "apb";  /* 多时钟时有名字 */

/* 通用：引用固定频率时钟 */
clocks = <&hse_clk>;
clock-frequency = <8000000>;  /* 8MHz */
```

**提取目标**：每个外设依赖哪些时钟源，时钟控制器的寄存器地址。

### 2.5 `pinctrl` — 引脚配置

DTS中通过 `pinctrl-N` 属性引用引脚配置节点：

```dts
/* 在pinctrl控制器节点下定义引脚配置 */
pinctrl: pin-controller@40020000 {
    usart1_pins_a: usart1-0 {
        pins1 {
            pinmux = <STM32_PINMUX('A', 9, AF7)>;   /* PA9 = USART1_TX */
            bias-disable;
            drive-push-pull;
            slew-rate = <0>;
        };
        pins2 {
            pinmux = <STM32_PINMUX('A', 10, AF7)>;  /* PA10 = USART1_RX */
            bias-disable;
        };
    };
};

/* 在外设节点中引用 */
&usart1 {
    pinctrl-names = "default";
    pinctrl-0 = <&usart1_pins_a>;   /* 引用上面的引脚配置 */
    status = "okay";
};
```

**全志sunxi的pinctrl写法**：

```dts
uart0_pins: uart0-pins {
    pins = "PB8", "PB9";           /* 引脚名 */
    function = "uart0";             /* 复用功能 */
    drive-strength = <40>;          /* 驱动强度 */
    bias-pull-up;                   /* 上拉 */
};

&uart0 {
    pinctrl-names = "default";
    pinctrl-0 = <&uart0_pins>;
    status = "okay";
};
```

**提取目标**：每个外设的默认引脚分配、复用功能号（AF编号）、引脚电气配置。

### 2.6 `status` — 设备状态

| 值 | 含义 |
|----|------|
| `"okay"` | 启用（板级DTS中显式启用） |
| `"disabled"` | 禁用（SoC级默认状态） |
| `"reserved"` | 保留（其他系统使用） |

## 3. 常见外设节点示例

### 3.1 GPIO控制器

```dts
gpioa: gpio@40020000 {
    compatible = "st,stm32f429-gpio", "st,stm32-gpio";
    reg = <0x40020000 0x400>;
    clocks = <&rcc 0 STM32F4_AHB1_CLOCK(GPIOA)>;
    gpio-controller;                    /* 标记为GPIO控制器 */
    #gpio-cells = <2>;                  /* GPIO引用需要2个参数 */
    ngpios = <16>;                      /* 该端口16个引脚 */
    st,bank-name = "GPIOA";             /* 端口名 */
    st,bank-ioport = <0>;              /* 端口编号 */
};
```

**提取目标**：GPIO控制器基地址、端口数、每端口引脚数、时钟依赖。

### 3.2 UART

```dts
usart1: serial@40011000 {
    compatible = "st,stm32-usart", "st,stm32-uart";
    reg = <0x40011000 0x400>;
    interrupts = <37>;
    clocks = <&rcc 0 STM32F4_APB2_CLOCK(USART1)>;
    status = "disabled";
};
```

**提取目标**：基地址、中断号、时钟源。

### 3.3 I2C

```dts
i2c1: i2c@40005400 {
    compatible = "st,stm32f4-i2c";
    reg = <0x40005400 0x400>;
    interrupts = <31>, <32>;           /* 事件中断 + 错误中断 */
    clocks = <&rcc 0 STM32F4_APB1_CLOCK(I2C1)>;
    #address-cells = <1>;              /* I2C设备地址1字节 */
    #size-cells = <0>;
    status = "disabled";

    /* 板级DTS中挂接I2C设备 */
    eeprom@50 {
        compatible = "atmel,24c256";
        reg = <0x50>;                  /* I2C地址0x50 */
    };
};
```

**提取目标**：基地址、中断号（可能有多个）、时钟源、I2C总线上的设备地址。

### 3.4 SPI

```dts
spi1: spi@40013000 {
    compatible = "st,stm32f4-spi";
    reg = <0x40013000 0x400>;
    interrupts = <35>;
    clocks = <&rcc 0 STM32F4_APB2_CLOCK(SPI1)>;
    #address-cells = <1>;
    #size-cells = <0>;
    status = "disabled";

    /* 板级DTS中挂接SPI设备 */
    flash@0 {
        compatible = "jedec,spi-nor";
        reg = <0>;                     /* CS0 */
        spi-max-frequency = <50000000>; /* 最大50MHz */
    };
};
```

**提取目标**：基地址、中断号、时钟源、SPI设备片选号。

### 3.5 ADC

```dts
adc1: adc@40012000 {
    compatible = "st,stm32f4-adc";
    reg = <0x40012000 0x400>;
    interrupts = <18>;
    clocks = <&rcc 0 STM32F4_APB2_CLOCK(ADC1)>;
    #address-cells = <1>;
    #size-cells = <0>;

    channel@0 {
        reg = <0>;                     /* ADC通道0 */
    };
    channel@1 {
        reg = <1>;                     /* ADC通道1 */
    };
};
```

**提取目标**：基地址、中断号、通道数、时钟源。

### 3.6 PWM / Timer

```dts
tim2: timer@40000000 {
    compatible = "st,stm32-timer";
    reg = <0x40000000 0x400>;
    interrupts = <28>;
    clocks = <&rcc 0 STM32F4_APB1_CLOCK(TIM2)>;
    status = "disabled";
};
```

**提取目标**：基地址、中断号、时钟源、PWM通道数（从pinctrl AF功能推断）。

### 3.7 DMA控制器

```dts
dma1: dma-controller@40026000 {
    compatible = "st,stm32f4-dma";
    reg = <0x40026000 0x400>;
    interrupts = <11>, <12>, <13>, <14>,  /* Stream 0-3 */
                 <15>, <16>, <17>, <18>;  /* Stream 4-7 */
    clocks = <&rcc 0 STM32F4_AHB1_CLOCK(DMA1)>;
    #dma-cells = <4>;                    /* DMA引用需要4个参数 */
};

/* 外设请求DMA通道 */
&usart1 {
    dmas = <&dma1 2 4 0x414 0x3>,        /* TX: stream2, channel4 */
           <&dma1 5 4 0x414 0x3>;        /* RX: stream5, channel4 */
    dma-names = "tx", "rx";
};
```

**提取目标**：DMA控制器基地址、Stream数量、每个外设可用的DMA Stream/Channel组合。

## 4. 中断控制器节点

### 4.1 ARM NVIC（Cortex-M）

```dts
nvic: interrupt-controller@e000e100 {
    compatible = "arm,v7m-nvic";
    reg = <0xe000e100 0x400>;
    interrupt-controller;
    #interrupt-cells = <1>;              /* 只需中断号 */
    arm,num-irq-priority-bits = <4>;     /* 优先级位宽 */
};
```

### 4.2 ARM GIC（Cortex-A）

```dts
gic: interrupt-controller@10300000 {
    compatible = "arm,gic-400";
    reg = <0x10300000 0x2000>,           /* GICD */
          <0x10302000 0x2000>;           /* GICC */
    interrupt-controller;
    #interrupt-cells = <3>;              /* 类型+中断号+触发方式 */
};
```

### 4.3 RISC-V PLIC

```dts
plic: interrupt-controller@c000000 {
    compatible = "riscv,plic0";
    reg = <0xc000000 0x4000000>;
    interrupt-controller;
    #interrupt-cells = <1>;
    riscv,ndev = <52>;                   /* 52个外部中断源 */
};
```

## 5. 内存和Flash节点

```dts
memory@20000000 {
    device_type = "memory";
    reg = <0x20000000 0x30000>;         /* SRAM: 0x20000000, 192KB */
};

flash@08000000 {
    reg = <0x08000000 0x100000>;        /* Flash: 0x08000000, 1MB */
};
```

**提取目标**：SRAM/Flash的物理地址和大小——这是链接脚本和内核配置的关键输入。

## 6. 从DTS提取信息的标准流程

```
1. 找到目标芯片的 .dtsi 文件（SoC级定义）
2. 列出所有外设节点（搜索 reg = 、interrupts = 等属性）
3. 逐个外设提取：基地址、中断号、时钟源、引脚配置
4. 找到中断控制器节点，确认中断格式（NVIC/GIC/PLIC）
5. 找到内存节点，确认SRAM/Flash地址和大小
6. 交叉校验：对比DTS中的地址与dt-bindings头文件中的宏定义
```
