# 输出模板

从芯片规格提取后，Agent需要按标准格式生成以下文件。每个模板展示了文件结构和关键字段。

## 1. L0 target_config.h 模板

适用于LiteOS-M轻量系统（Cortex-M / RISC-V MCU），定义芯片的内核参数和外设能力。

```c
/*
 * Copyright (c) 2024 OpenHarmony Contributors
 * target_config.h - 芯片目标配置
 */

#ifndef TARGET_CONFIG_H
#define TARGET_CONFIG_H

/* ====== 内核配置 ====== */
#define LOSCFG_KERNEL_TICK_FACTOR              1      /* Tick精度因子 */
#define LOSCFG_BASE_CORE_TSK_LIMIT             16     /* 最大任务数 */
#define LOSCFG_BASE_CORE_TSK_IDLE_STACK_SIZE   0x500  /* 空闲任务栈大小 */
#define LOSCFG_BASE_CORE_TSK_DEFAULT_STACK_SIZE 0x800 /* 默认任务栈大小 */
#define LOSCFG_BASE_IPC_QUEUE_LIMIT            32     /* 最大队列数 */
#define LOSCFG_BASE_IPC_SEM_LIMIT              20     /* 最大信号量数 */
#define LOSCFG_BASE_IPC_MUX_LIMIT              20     /* 最大互斥锁数 */
#define LOSCFG_BASE_MEM_NODE_INTEGRAL_SIZE     32     /* 内存对齐粒度 */
#define LOSCFG_SYS_HEAP_SIZE                   0x8000 /* 堆内存大小 */

/* ====== CPU配置 ====== */
#define CHIP_INT_RAM_SIZE       0x40000   /* 内部RAM大小 (256KB) */
#define CHIP_FLASH_START        0x08000000 /* Flash起始地址 */
#define CHIP_FLASH_SIZE         0x80000   /* Flash大小 (512KB) */

/* ====== 外设能力声明 ====== */
/* GPIO控制器数量及每组引脚数 */
#define HAL_GPIO_PORT_NUM       9         /* GPIOA-GPIOI */
#define HAL_GPIO_PIN_PER_PORT   16        /* 每组16个引脚 */

/* UART控制器数量 */
#define HAL_UART_NUM            6         /* USART1-6 */

/* I2C控制器数量 */
#define HAL_I2C_NUM             3         /* I2C1-3 */

/* SPI控制器数量 */
#define HAL_SPI_NUM             3         /* SPI1-3 */

/* ADC通道数 */
#define HAL_ADC_CHANNEL_NUM     16        /* ADC1通道0-15 */

/* PWM/定时器通道数 */
#define HAL_PWM_NUM             14        /* TIM1-14 */

/* ====== 时钟配置 ====== */
#define CHIP_SYS_CLOCK          168000000 /* 系统主频 168MHz */
#define CHIP_EXTERNAL_OSC_FREQ  8000000   /* 外部晶振频率 8MHz */
#define CHIP_LOSC_CLOCK         32768     /* 低速外部时钟 */

/* ====== 中断配置 ====== */
#define CHIP_IRQ_MAX_NUM        82        /* 最大中断号 */
#define CHIP_INT_PEND_ARRAY_SIZE ((CHIP_IRQ_MAX_NUM >> 5) + 1)

#endif /* TARGET_CONFIG_H */
```

### 字段说明

| 字段 | 来源 | 说明 |
|------|------|------|
| LOSCFG_KERNEL_TICK_FACTOR | 芯片定时器精度 | 1=1ms tick, 需SysTick支持 |
| LOSCFG_BASE_CORE_TSK_LIMIT | RAM大小决定 | 64KB RAM建议≤10, 256KB+可16 |
| LOSCFG_SYS_HEAP_SIZE | 可用RAM - 内核开销 | 通常为总RAM的40-60% |
| CHIP_SYS_CLOCK | 时钟树配置 | 从时钟驱动/手册获取 |
| CHIP_IRQ_MAX_NUM | 芯片中断控制器 | Cortex-M NVIC最大中断数 |
| 外设能力声明 | DTS/SDK头文件 | 统计各外设控制器数量 |

---

## 2. L0 HAL实现模板（hal_iot_xxx.c）

适用于OpenHarmony L0 IoT子系统，将芯片SDK API映射为OpenHarmony标准HAL接口。

### GPIO HAL模板

```c
/*
 * hal_iot_gpio.c - OpenHarmony L0 GPIO HAL实现
 * 映射: IoT GPIO API → 芯片SDK GPIO API
 */

#include "iot_gpio.h"
#include "hi_gpio.h"     /* 芯片SDK头文件 */
#include "hi_io.h"        /* 芯片IO复用头文件 */

unsigned int IoTGpioInit(void)
{
    /* 映射: IoT GPIO初始化 → SDK GPIO初始化 */
    return hi_gpio_init();
}

unsigned int IoTGpioDeinit(void)
{
    return hi_gpio_deinit();
}

unsigned int IoTGpioSetDir(unsigned int id, IotGpioDir dir)
{
    /* 映射: IoT方向枚举 → SDK方向枚举 */
    hi_gpio_dir sdk_dir = (dir == IOT_GPIO_DIR_IN) ?
                          HI_GPIO_DIR_IN : HI_GPIO_DIR_OUT;
    return hi_gpio_set_dir((hi_gpio_idx)id, sdk_dir);
}

unsigned int IoTGpioGetDir(unsigned int id, IotGpioDir *dir)
{
    hi_gpio_dir sdk_dir;
    unsigned int ret = hi_gpio_get_dir((hi_gpio_idx)id, &sdk_dir);
    if (ret == 0) {
        *dir = (sdk_dir == HI_GPIO_DIR_IN) ?
               IOT_GPIO_DIR_IN : IOT_GPIO_DIR_OUT;
    }
    return ret;
}

unsigned int IoTGpioSetOutputValue(unsigned int id, IotGpioValue val)
{
    return hi_gpio_set_output_val((hi_gpio_idx)id, (hi_gpio_value)val);
}

unsigned int IoTGpioGetInputValue(unsigned int id, IotGpioValue *val)
{
    return hi_gpio_get_input_val((hi_gpio_idx)id, (hi_gpio_value *)val);
}

unsigned int IoTGpioRegisterIsrFunc(unsigned int id, IotGpioIntType intType,
    IotGpioIntPolarity intPolarity, GpioIsrCallbackFunc func, void *arg)
{
    /* 映射: IoT中断类型/极性 → SDK中断类型/极性 */
    hi_gpio_int_type sdk_type = (intType == IOT_INT_TYPE_EDGE) ?
                                HI_INT_TYPE_EDGE : HI_INT_TYPE_LEVEL;
    hi_gpio_int_polarity sdk_pol = (intPolarity == IOT_GPIO_EDGE_RISE_LEVEL_HIGH) ?
                                   HI_GPIO_EDGE_RISE_LEVEL_HIGH :
                                   HI_GPIO_EDGE_FALL_LEVEL_LOW;
    return hi_gpio_register_isr_function((hi_gpio_idx)id, sdk_type, sdk_pol,
                                           (gpio_isr_callback)func, arg);
}
```

### UART HAL模板

```c
/*
 * hal_iot_uart.c - OpenHarmony L0 UART HAL实现
 */

#include "iot_uart.h"
#include "hi_uart.h"

unsigned int IoTUartInit(int id, const IotUartAttribute *param)
{
    hi_uart_attribute attr;
    attr.baud_rate = param->baudRate;
    attr.data_bits = param->dataBits;
    attr.stop_bits = param->stopBits;
    attr.parity    = param->parity;
    attr.rx_block  = param->rxBlock;
    attr.tx_block  = param->txBlock;
    return hi_uart_init(id, &attr, HI_NULL);
}

int IoTUartWrite(int id, const unsigned char *data, unsigned int dataLen)
{
    return hi_uart_write(id, data, dataLen);
}

int IoTUartRead(int id, unsigned char *data, unsigned int dataLen)
{
    return hi_uart_read(id, data, dataLen);
}

unsigned int IoTUartDeinit(int id)
{
    return hi_uart_deinit(id);
}
```

---

## 3. L1 HCS配置模板

适用于LiteOS-A小型系统（HDF驱动框架），通过HCS文件描述硬件设备信息。

### GPIO HCS配置模板

```hcs
/*
 * gpio_config.hcs - GPIO设备HCS配置
 * L1小型系统使用，由HDF GPIO驱动解析
 */
root {
    platform {
        gpio_config {
            /* 每个GPIO控制器一个节点 */
            controller_0x{BASE_ADDR_HEX} {
                match_attr = "{vendor}_{chip}_gpio{N}";
                group_num = {PORT_COUNT};      /* GPIO组数(如A/B/C/D/E) */
                bit_num = {PIN_PER_PORT};      /* 每组引脚数(通常16) */
                regBase = 0x{BASE_ADDR_HEX};  /* 寄存器基地址 */
            }
        }
    }
}
```

### UART HCS配置模板

```hcs
/*
 * uart_config.hcs - UART设备HCS配置
 */
root {
    platform {
        uart_config {
            /* 模板说明：
             * 每个UART控制器一个节点，节点名包含基地址
             */
            uart_{N} {
                match_attr = "hisilicon_hi35xx_uart{N}";
                num = {N};                    /* UART端口号 */
                fifo_tx_en = 1;               /* TX FIFO使能 */
                fifo_rx_en = 1;               /* RX FIFO使能 */
                fifo_tx_depth = 32;           /* TX FIFO深度 */
                fifo_rx_depth = 32;           /* RX FIFO深度 */
                regBase = 0x{BASE_ADDR_HEX}; /* 寄存器基地址 */
                irq = {IRQ_NUM};              /* 中断号 */
                baud_rate = 115200;           /* 默认波特率 */
                wlen = 8;                     /* 数据位宽 */
                parity = 0;                   /* 校验: 0=无 */
                stop = 1;                     /* 停止位 */
                rts = 0;                      /* RTS流控 */
                cts = 0;                      /* CTS流控 */
            }
        }
    }
}
```

### I2C HCS配置模板

```hcs
root {
    platform {
        i2c_config {
            i2c_{N} {
                match_attr = "{vendor}_{chip}_i2c{N}";
                regBase = 0x{BASE_ADDR_HEX};
                irq = {IRQ_NUM};
                freq = 100000;       /* I2C频率: 100kHz标准 / 400kHz快速 */
            }
        }
    }
}
```

---

## 4. JSON Schema输出模板

芯片规格解析器的标准输出格式（完整定义见json-schema-design.md），此处展示关键片段。

```json
{
  "chip_name": "Hi3861",
  "vendor": "HiSilicon",
  "architecture": "RISC-V",
  "cpu_core": "RV32",
  "system_clock_hz": 160000000,
  "memory": {
    "flash_size_bytes": "0x200000",
    "sram_size_bytes": "0x60000"
  },
  "gpio": {
    "total_pins": 15,
    "groups": [{"name": "GPIO0", "pin_count": 15, "base_address": null}],
    "pin_functions": {
      "GPIO_0": ["GPIO", "UART0_TX", "SPI0_CS"],
      "GPIO_1": ["GPIO", "UART0_RX", "SPI0_CLK"]
    }
  },
  "uart": {
    "controllers": [
      {"id": 0, "base_address": null, "irq": null, "max_baud": 1500000},
      {"id": 1, "base_address": null, "irq": null, "max_baud": 1500000}
    ]
  },
  "i2c": {
    "controllers": [
      {"id": 0, "base_address": null, "irq": null, "max_freq_hz": 400000}
    ]
  }
}
```

> **注**：Hi3861的LiteOS SDK封装了寄存器访问，部分`base_address`和`irq`字段为null（无法从SDK头文件直接获取）。这些信息需要从芯片手册或寄存器参考文档补充。
