# OpenHarmony Lite 芯片接入配置文件清单

> 新芯片适配OpenHarmony Lite时需要创建哪些配置文件，以及每份文件的参考来源。

---

## L0 轻量系统（MCU, LiteOS-M, <128KB RAM）

L0不使用HDF框架和设备树，所有设备配置以**C头文件宏定义 + 构建脚本**形式存在，编译时确定，运行时不解析任何配置文件。

### 需要创建的配置文件

```
device/soc/<厂商>/<芯片>/
├── config.gni                    # SoC级构建参数
└── ld/
    └── linker.ld                 # MCU链接脚本

device/board/<厂商>/<开发板>/
└── liteos_m/
    ├── config.gni                # 板级构建参数
    └── board_config.h            # 板级引脚/外设分配（C宏定义）

vendor/<厂商>/<产品>/
└── config.json                   # 产品定义（子系统+组件列表）
```

| 文件 | 内容 | 参考来源 |
|------|------|---------|
| `device/soc/.../config.gni` | CPU架构、主频、Flash/RAM大小和基地址、中断数量、外设基地址 | 芯片Datasheet的Memory Map章节 |
| `device/soc/.../ld/linker.ld` | MEMORY区域定义（FLASH/RAM起始地址和大小）、SECTIONS段分配（向量表/代码/数据/堆栈）、栈大小 | 芯片Datasheet的Memory Map + 内核要求 |
| `device/board/.../liteos_m/config.gni` | 开发板名称、SoC引用、外设使能开关、调试串口选择 | 开发板原理图 |
| `device/board/.../liteos_m/board_config.h` | 各外设使用的引脚号、引脚复用配置（AF映射） | 芯片Datasheet的GPIO/Pin Mux章节 + 开发板原理图 |
| `vendor/.../config.json` | 产品名、内核类型（liteos_m）、启用的子系统和组件列表 | 产品功能需求 |

### L0配置示例

**config.gni（SoC级）：**
```gn
board_cpu = "cortex-m4"
board_fpu = "dp"
board_flash_size = 0x100000      # 1MB
board_flash_base = 0x08000000
board_ram_size = 0x20000         # 128KB
board_ram_base = 0x20000000
board_tick_irq_num = 15          # SysTick中断号
```

**board_config.h：**
```c
#define BOARD_UART0_TX_PIN    GPIO_PIN(0, 9)    // PA9
#define BOARD_UART0_RX_PIN    GPIO_PIN(0, 10)   // PA10
#define BOARD_I2C0_SCL_PIN    GPIO_PIN(1, 6)    // PB6
#define BOARD_I2C0_SDA_PIN    GPIO_PIN(1, 7)    // PB7
```

---

## L1 小型系统（MPU, LiteOS-A / L1-Linux, >1MB RAM）

L1-LiteOS 路线使用**精简版HDF框架**，设备配置以HCS文件形式存在，运行时由HCS Parser解析加载驱动；L1-Linux 路线（kernel_family=linux，如 Hi3516CV610）设备描述用 DTS，按 target profile 的 device_description 决定，不按 L1 标签一刀切。

### 需要创建的配置文件

```
device/soc/<厂商>/<芯片>/
└── config.gni                    # SoC级构建参数

device/board/<厂商>/<开发板>/
└── config.gni                    # 板级构建参数

vendor/<厂商>/<产品>/
├── config.json                   # 产品定义
└── hdf_config/uhdf/
    ├── hdf.hcs                   # HCS主入口（#include所有子配置）
    ├── device_info/
    │   └── device_info.hcs       # 设备节点树（host→device→deviceNode）
    ├── gpio/
    │   └── gpio_config.hcs       # GPIO控制器寄存器配置
    ├── uart/
    │   └── uart_config.hcs       # UART端口配置（端口号、波特率、引脚）
    ├── i2c/
    │   └── i2c_config.hcs        # I2C总线配置
    ├── spi/
    │   └── spi_config.hcs        # SPI总线配置
    ├── pwm/
    │   └── pwm_config.hcs        # PWM配置
    ├── adc/
    │   └── adc_config.hcs        # ADC配置
    └── platform/
        └── platform_config.hcs   # 平台级配置
```

| 文件 | 内容 | 参考来源 |
|------|------|---------|
| `device/soc/.../config.gni` | 同L0的SoC参数 | 芯片Datasheet |
| `device/board/.../config.gni` | 开发板名称、SoC引用 | 开发板原理图 |
| `vendor/.../config.json` | 产品名、内核类型（liteos_a）、子系统列表 | 产品功能需求 |
| `hdf.hcs` | HCS主入口，#include所有子配置文件 | 框架规范 |
| `device_info.hcs` | 设备节点树：每个驱动加载为一个deviceNode，通过match_attr与配置文件关联 | 芯片Datasheet + 驱动框架文档 |
| `gpio_config.hcs` | GPIO控制器数量、寄存器基地址、引脚数 | 芯片Datasheet的GPIO章节 |
| `uart_config.hcs` | 每个UART端口：基地址、中断号、波特率、TX/RX引脚 | 芯片Datasheet的UART章节 + 开发板原理图 |
| `i2c_config.hcs` | 每个I2C总线：基地址、中断号、时钟频率、SCL/SDA引脚 | 芯片Datasheet的I2C章节 + 开发板原理图 |
| `spi_config.hcs` | 每个SPI总线：基地址、中断号、引脚映射 | 芯片Datasheet的SPI章节 + 开发板原理图 |
| `pwm_config.hcs` | PWM通道数量和引脚映射 | 芯片Datasheet的PWM章节 |
| `adc_config.hcs` | ADC通道数量和引脚映射 | 芯片Datasheet的ADC章节 |
| `platform_config.hcs` | 平台级参数（系统时钟、电源管理） | 芯片Datasheet的RCC/Clock章节 |

### L1配置示例

**device_info.hcs：**
```hcs
root {
    platform {
        gpio_config :: host {
            device_gpio :: device {
                device0 :: deviceNode {
                    match_attr = "gpio_config";    // 必须与gpio_config.hcs中的match_attr完全一致
                }
            }
        }
    }
}
```

**uart_config.hcs：**
```hcs
root {
    platform {
        uart_config :: host {
            uart_1 {
                match_attr = "uart_config";
                template uart_device {
                    num = 1;
                    fifoTxIrqNum = 37;
                    fifoRxIrqNum = 38;
                    baudrate = 115200;
                    txPin = 9;       // PA9
                    rxPin = 10;      // PA10
                }
            }
        }
    }
}
```

---

## L0与L1配置差异对比

| 维度 | L0 轻量系统 | L1 小型系统 |
|------|------------|------------|
| 设备描述方式 | C头文件宏定义（编译时常量） | HCS配置文件（运行时解析） |
| 运行时配置解析 | 无 | Lite HCS Parser |
| 驱动框架 | IoT外设驱动子系统（static_library） | 精简版HDF（HdfDriverEntry） |
| 配置文件格式 | .h + .gni + .json + .ld | .hcs + .gni + .json |
| 配置文件数量 | 约5个 | 约10-15个 |
| 引脚配置方式 | board_config.h 宏定义 | xxx_config.hcs 文件 |
| 匹配机制 | 无（编译时确定） | match_attr 必须严格匹配 |
| 易错点 | 链接脚本地址写错导致HardFault | match_attr拼写错误导致驱动加载失败且难排查 |

---

## 参考来源汇总

新芯片适配时，配置文件的内容来自以下几个源头：

| 参考来源 | 提供什么信息 | 喂给哪些配置文件 |
|---------|------------|----------------|
| **芯片Datasheet** — Memory Map章节 | Flash/RAM大小和基地址、外设寄存器基地址 | config.gni、linker.ld、*_config.hcs |
| **芯片Datasheet** — GPIO/Pin Mux章节 | 引脚功能复用表、AF编号映射 | board_config.h(L0)、*_config.hcs(L1) |
| **芯片Datasheet** — 各外设章节 | 中断号、DMA通道、外设能力参数 | *_config.hcs(L1) |
| **芯片Datasheet** — RCC/Clock章节 | 时钟源、PLL参数、外设时钟使能位 | platform_config.hcs(L1)、board_init.c(L0) |
| **开发板原理图** | 各外设实际使用的引脚号、外部晶振频率 | board_config.h(L0)、*_config.hcs(L1) |
| **内核文档** | Tick中断号、堆大小、IPC组件选择 | linker.ld、target_config.h |
| **产品功能需求** | 需要哪些子系统、哪些外设驱动 | config.json |
| **已有芯片的配置文件** | 作为模板参照，复制后修改芯片特有参数 | 所有配置文件 |

---

*文档生成日期：2026-06-08*
*来源：OpenHarmony Lite适配代码结构分析*

---

## 真实示例参考

完整真实芯片配置样本见本 SKILL 的 `examples/` 目录：
- L0: `examples/l0/`（Hi3861 / STM32F407 等）
- L1: `examples/l1/`（Hi3516DV300 等）
