# SDK头文件提取案例

当芯片没有Linux适配时，需要从厂商SDK头文件中提取硬件规格。本文展示两个完整案例。

## 案例1：Hi3861（海思LiteOS SDK风格）

### SDK特征

- 头文件位于 `hi3861v100/sdk_liteos/include/`
- 以`hi_`前缀命名（hi_gpio.h, hi_uart.h, hi_io.h等）
- **API函数封装**，不直接暴露寄存器地址
- 使用typedef enum定义参数类型（hi_gpio_dir, hi_gpio_value等）
- 引脚复用通过独立的`hi_io.h` + `hi_mux.h`管理

### 提取流程

#### Step 1: GPIO能力（从hi_gpio.h提取）

```c
// 读取 hi_gpio.h，提取以下信息：

// 1. GPIO引脚定义（枚举）
typedef enum {
    HI_GPIO_IDX_0,   // GPIO0
    HI_GPIO_IDX_1,   // GPIO1
    ...
    HI_GPIO_IDX_14,  // GPIO14
    HI_GPIO_IDX_MAX, // = 15，共15个GPIO
} hi_gpio_idx;

// → 提取: total_pins = 15 (GPIO_0 ~ GPIO_14)

// 2. GPIO方向
typedef enum {
    HI_GPIO_DIR_IN = 0,  // 输入
    HI_GPIO_DIR_OUT      // 输出
} hi_gpio_dir;

// 3. GPIO电平
typedef enum {
    HI_GPIO_VALUE0 = 0,  // 低电平
    HI_GPIO_VALUE1       // 高电平
} hi_gpio_value;

// 4. 中断触发类型
typedef enum {
    HI_INT_TYPE_LEVEL = 0,  // 电平触发
    HI_INT_TYPE_EDGE        // 边沿触发
} hi_gpio_int_type;

// 5. API函数清单
hi_u32 hi_gpio_init(void);
hi_u32 hi_gpio_deinit(void);
hi_u32 hi_gpio_set_dir(hi_gpio_idx id, hi_gpio_dir dir);
hi_u32 hi_gpio_get_dir(hi_gpio_idx id, hi_gpio_dir *dir);
hi_u32 hi_gpio_set_output_val(hi_gpio_idx id, hi_gpio_value val);
hi_u32 hi_gpio_get_output_val(hi_gpio_idx id, hi_gpio_value *val);
hi_u32 hi_gpio_get_input_val(hi_gpio_idx id, hi_gpio_value *val);
hi_u32 hi_gpio_register_isr_function(hi_gpio_idx id, hi_gpio_int_type int_type,
    hi_gpio_int_polarity int_polarity, gpio_isr_callback func, hi_void *arg);
```

**提取结论**：Hi3861有15个GPIO，支持输入/输出/中断，SDK封装了所有寄存器操作。

#### Step 2: 引脚复用（从hi_io.h + hi_mux.h提取）

```c
// 读取 hi_io.h，提取引脚复用功能

// hi_io_set_func: 设置IO复用功能
hi_u32 hi_io_set_func(hi_io_name id, hi_io_func func);

// hi_io_name: IO名称枚举（与GPIO编号对应）
typedef enum {
    HI_IO_NAME_GPIO_0,  // IO0
    HI_IO_NAME_GPIO_1,  // IO1
    ...
    HI_IO_NAME_GPIO_14, // IO14
    HI_IO_NAME_MAX,
} hi_io_name;

// hi_io_func: 复用功能枚举
typedef enum {
    HI_IO_FUNC_GPIO_0_GPIO,     // GPIO_0 → GPIO功能
    HI_IO_FUNC_GPIO_0_UART0_TXD, // GPIO_0 → UART0 TX
    HI_IO_FUNC_GPIO_0_SPI0_CS,  // GPIO_0 → SPI0 片选
    HI_IO_FUNC_GPIO_0_JTAG_TMS, // GPIO_0 → JTAG TMS
    // ... 每个GPIO有4-8个复用功能
} hi_io_func;
```

**提取结论**：每个GPIO引脚有多个复用功能，通过`hi_io_set_func()`切换。需要逐个枚举提取每个引脚的所有可选功能。

#### Step 3: UART能力（从hi_uart.h提取）

```c
// 读取 hi_uart.h

// UART属性结构体
typedef struct {
    hi_u32 baud_rate;   // 波特率
    hi_u8  data_bits;   // 数据位 (5-8)
    hi_u8  stop_bits;   // 停止位 (1-2)
    hi_u8  parity;      // 校验 (0=无, 1=奇, 2=偶)
    hi_u8  rx_block;    // 接收阻塞模式
    hi_u8  tx_block;    // 发送阻塞模式
} hi_uart_attribute;

// API
hi_s32 hi_uart_init(hi_uart_idx id, const hi_uart_attribute *attr, const hi_void *param);
hi_s32 hi_uart_deinit(hi_uart_idx id);
hi_s32 hi_uart_write(hi_uart_idx id, const hi_u8 *data, hi_u32 len);
hi_s32 hi_uart_read(hi_uart_idx id, hi_u8 *data, hi_u32 len);

// UART索引
typedef enum {
    HI_UART_IDX_0,  // UART0
    HI_UART_IDX_1,  // UART1
    HI_UART_IDX_2,  // UART2 (可能)
    HI_UART_IDX_MAX,
} hi_uart_idx;
```

**提取结论**：Hi3861有2-3个UART，SDK通过函数封装（无直接寄存器访问），波特率/数据位/停止位/校验位可配。

#### Step 4: 生成JSON输出

```json
{
  "chip_name": "Hi3861",
  "vendor": "HiSilicon",
  "architecture": "RISC-V",
  "cpu_core": "RV32",
  "system_clock_hz": 160000000,
  "gpio": {
    "total_pins": 15,
    "api_style": "function_wrapper",
    "pin_functions": {
      "GPIO_0": ["GPIO", "UART0_TXD", "SPI0_CS", "JTAG_TMS"],
      "GPIO_1": ["GPIO", "UART0_RXD", "SPI0_CLK", "JTAG_TCK"],
      "GPIO_2": ["GPIO", "UART1_TXD", "SPI0_MOSI", "JTAG_TDO"],
      "GPIO_3": ["GPIO", "UART1_RXD", "SPI0_MISO", "JTAG_TDI"]
    }
  },
  "uart": {
    "controllers": [
      {"id": 0, "max_baud": 1500000, "configurable": ["baud_rate","data_bits","stop_bits","parity"]},
      {"id": 1, "max_baud": 1500000, "configurable": ["baud_rate","data_bits","stop_bits","parity"]}
    ],
    "api_style": "function_wrapper"
  },
  "notes": "Hi3861 SDK封装了寄存器访问，base_address和irq无法从头文件直接获取"
}
```

---

## 案例2：ESP32-C3（ESP-IDF风格）

### SDK特征

- 头文件位于 `components/soc/esp32c3/include/soc/`
- 使用`SOC_`前缀宏定义（soc_caps.h, soc.h）
- **宏定义模式**，直接暴露寄存器地址和数量
- 外设数量和能力在`soc_caps.h`中集中定义
- 外设基地址在`soc.h`中定义

### 提取流程

#### Step 1: SoC能力概览（从soc_caps.h提取）

```c
// 读取 soc_caps.h — 这个文件包含ESP32-C3的所有能力定义

// GPIO能力
#define SOC_GPIO_PIN_COUNT                  22   // 22个GPIO引脚
#define SOC_GPIO_SUPPORT_PIN_GLITCH_FILTER  1    // 支持毛刺滤波
#define SOC_GPIO_VALID_GPIO_MASK            0x3FFFFF  // 有效GPIO掩码

// UART能力
#define SOC_UART_NUM                        2    // 2个UART
#define SOC_UART_FIFO_LEN                   128  // FIFO深度128字节
#define SOC_UART_SUPPORT_RTC_CLK            1    // 支持RTC时钟源
#define SOC_UART_SUPPORT_XTAL_CLK           1    // 支持XTAL时钟源

// I2C能力
#define SOC_I2C_NUM                         1    // 1个I2C
#define SOC_I2C_FIFO_LEN                    32   // FIFO深度

// SPI能力
#define SOC_SPI_PERIPH_NUM                  2    // 2个SPI
#define SOC_SPI_MAX_CS_NUM                  6    // 最多6个片选

// ADC能力
#define SOC_ADC_MAX_CHANNEL_NUM             5    // 最多5个ADC通道
#define SOC_ADC_DIGI_MAX_BITWIDTH           12   // 12位分辨率

// Timer能力
#define SOC_TIMER_GROUP_TIMERS_PER_GROUP    1
#define SOC_TIMER_GROUP_TOTAL_TIMERS        2

// 中断
#define SOC_CPU_CORES_NUM                   1    // 单核
#define SOC_CPU_INTERRUPTS_NUM              31   // 31个中断
```

**提取结论**：soc_caps.h是最关键的入口文件，包含了ESP32-C3的所有外设数量和能力的集中定义。

#### Step 2: 外设基地址（从soc.h提取）

```c
// 读取 soc.h — 外设寄存器基地址

#define DR_REG_UART_BASE         0x60000000  // UART0基地址
#define DR_REG_UART1_BASE        0x60010000  // UART1基地址
#define DR_REG_SPI1_BASE         0x60002000  // SPI1基地址
#define DR_REG_SPI0_BASE         0x60003000  // SPI0基地址
#define DR_REG_GPIO_BASE         0x60004000  // GPIO基地址
#define DR_REG_FE2_BASE          0x60005000  // FE2基地址
#define DR_REG_I2C_BASE          0x60013000  // I2C基地址
#define DR_REG_I2S_BASE          0x6000F000  // I2S基地址
#define DR_REG_TIMERGROUP0_BASE  0x6001F000  // Timer Group 0基地址
#define DR_REG_TIMERGROUP1_BASE  0x60020000  // Timer Group 1基地址
```

**提取结论**：soc.h定义了所有外设的寄存器基地址，是硬件映射的核心信息。

#### Step 3: 生成JSON输出

```json
{
  "chip_name": "ESP32-C3",
  "vendor": "Espressif",
  "architecture": "RISC-V",
  "cpu_core": "RV32IMC",
  "system_clock_hz": 160000000,
  "memory": {
    "sram_size_bytes": "0x64000"
  },
  "gpio": {
    "total_pins": 22,
    "base_address": "0x60004000",
    "api_style": "macro_register",
    "features": ["glitch_filter"]
  },
  "uart": {
    "controllers": [
      {"id": 0, "base_address": "0x60000000", "fifo_depth": 128},
      {"id": 1, "base_address": "0x60010000", "fifo_depth": 128}
    ],
    "api_style": "macro_register"
  },
  "i2c": {
    "controllers": [
      {"id": 0, "base_address": "0x60013000", "fifo_depth": 32}
    ]
  },
  "spi": {
    "controllers": [
      {"id": 0, "base_address": "0x60003000"},
      {"id": 1, "base_address": "0x60002000"}
    ]
  },
  "adc": {
    "channels": 5,
    "resolution_bits": 12
  },
  "interrupts": {
    "total": 31,
    "cpu_cores": 1
  }
}
```

---

## SDK风格对比总结

| 特征 | Hi3861 (LiteOS) | ESP32-C3 (ESP-IDF) | STM32 (CMSIS) | BES2600W (Bestechnic) |
|------|----------------|---------------------|---------------|----------------------|
| 命名前缀 | `hi_` | `SOC_` / `DR_REG_` | `GPIO_` / `HAL_` | `hal_` |
| 寄存器访问 | 函数封装 | 宏定义+直接地址 | 结构体+位域 | 函数封装 |
| 外设数量定义 | 需从枚举推断 | `soc_caps.h`集中定义 | 手册/设备头文件 | 需从头文件推断 |
| 基地址 | SDK隐藏 | `soc.h`明确定义 | 设备头文件定义 | `plat_addr_map.h` |
| 引脚复用 | `hi_io_set_func()` | `gpio_sig_map.h` | `GPIO_AF`寄存器 | `hal_iomux_set_xxx()` |
| 信息密度 | 中（分散多文件） | 高（集中两文件） | 高（单文件大） | 中（分散多文件） |

### Agent识别策略

1. **看命名前缀**：`hi_` → HiSilicon风格, `SOC_` → ESP-IDF风格, `HAL_`/`TypeDef` → STM32 CMSIS风格
2. **找入口文件**：soc_caps.h（ESP-IDF）/ include目录所有hi_*.h（Hi3861）/ 设备头文件（STM32）
3. **确定寄存器访问方式**：函数封装 or 宏定义 or 结构体
4. **按外设逐一提取**：GPIO → UART → I2C → SPI → ADC → Timer
