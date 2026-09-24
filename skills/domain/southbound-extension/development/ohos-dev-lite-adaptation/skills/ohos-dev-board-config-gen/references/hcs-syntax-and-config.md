# HCS语法规范与L0/L1配置体系

## L0 vs L1 vs L2 设备配置对比

| 系统级别 | 设备描述方式 | 配置文件格式 | 工具链 |
|---------|------------|-------------|--------|
| **L0 轻量系统** | **代码宏定义 + 极简头文件** | `.h` 头文件 / `config.json` | build_lite |
| **L1 小型系统** | **精简版HCS** | `.hcs` 文件（精简） | hc-gen (精简) |
| L2 标准系统 | Linux DTS + 完整HCS | `.dts/.dtsi` + `.hcs` | dtc + hc-gen |

> ⚠️ **重要说明**：
> - **L0轻量系统不使用DTS也不使用完整HCS**。设备配置通过代码宏定义或极简头文件完成。
> - **L1小型系统使用精简版HCS**，相比标准系统的完整HCS更加简洁。

### L0 vs L1 详细对比

| 对比维度 | L0 轻量系统 | L1 小型系统 |
|----------|-----------|-----------|
| **设备描述格式** | C头文件宏定义 / config.json | 精简版HCS |
| **编译工具** | build_lite (GN+Ninja) | hc-gen (精简) |
| **运行时解析** | ❌ 无（编译时常量） | 精简版HCS Parser |
| **配置范围** | MCU外设引脚映射、寄存器地址 | HDF驱动相关配置 |
| **模板/继承** | ❌ 不支持 | 精简支持 |
| **产品配置目录** | `vendor/<vendor>/<board>/config.json` | `vendor/<vendor>/<product>/hdf_config/` |

### L1精简版HCS与标准系统完整HCS的区别

| 特性 | L1精简版HCS | L2完整HCS |
|------|-----------|----------|
| template模板 | ✅ 基础支持 | ✅ 完整支持 |
| 节点复制(`:`) | 基本不使用 | ✅ 广泛使用 |
| delete删除 | 基本不使用 | ✅ 支持 |
| 属性引用(`&`) | 基本不使用 | ✅ 支持 |
| 条件编译 | ✅ 支持 | ✅ 支持 |
| match_attr | ✅ 核心机制 | ✅ 核心机制 |
| deviceNode层次 | host→device→deviceNode | 相同但更复杂 |

## L0轻量系统的设备配置方式

L0轻量系统运行在MCU上（最小128KB内存），资源极度受限，**不使用任何运行时设备树解析机制**。设备配置以编译时常量的形式存在：

```c
/* L0 设备配置示例 — 通过头文件宏定义 */
#ifndef BOARD_CONFIG_H
#define BOARD_CONFIG_H

/* UART引脚映射 */
#define BOARD_UART0_TX_PIN      GPIO_PIN(0, 9)   /* PA9 */
#define BOARD_UART0_RX_PIN      GPIO_PIN(0, 10)  /* PA10 */
#define BOARD_UART0_BAUDRATE    115200

/* I2C引脚映射 */
#define BOARD_I2C0_SDA_PIN      GPIO_PIN(1, 7)   /* PB7 */
#define BOARD_I2C0_SCL_PIN      GPIO_PIN(1, 6)   /* PB6 */
#define BOARD_I2C0_SPEED        400000

/* SPI引脚映射 */
#define BOARD_SPI0_SCK_PIN      GPIO_PIN(0, 5)   /* PA5 */
#define BOARD_SPI0_MOSI_PIN     GPIO_PIN(0, 7)   /* PA7 */
#define BOARD_SPI0_MISO_PIN     GPIO_PIN(0, 6)   /* PA6 */
#define BOARD_SPI0_CS_PIN       GPIO_PIN(0, 4)   /* PA4 */

/* ADC通道映射 */
#define BOARD_ADC_TEMP_CHANNEL  16               /* 内部温度传感器 */
#define BOARD_ADC_VREF_CHANNEL  17               /* 内部参考电压 */

/* LED/按键引脚 */
#define BOARD_LED1_PIN          GPIO_PIN(2, 13)  /* PC13 */
#define BOARD_KEY1_PIN          GPIO_PIN(0, 0)   /* PA0 */

#endif /* BOARD_CONFIG_H */
```

产品级配置则通过 `vendor/<vendor>/<board>/config.json` 管理：

```json
{
    "boardName": "HiSpark_WiFi_IoT",
    "socName": "hi3861v100",
    "kernelType": "liteos_m",
    "peripherals": {
        "uart": [{"id": 0, "enable": true, "baudRate": 115200}],
        "i2c": [{"id": 0, "enable": true, "speed": 400000}],
        "spi": [{"id": 0, "enable": false}],
        "pwm": [{"id": 0, "enable": true}]
    }
}
```

## HCS完整语法规范

### 基本数据类型

| 类型 | 语法示例 | 说明 |
|------|---------|------|
| 整数 | `value = 100;` | 十进制整数 |
| 十六进制 | `addr = 0xFE650000;` | 以0x开头 |
| 八进制 | `perm = 0644;` | 以0开头 |
| 字符串 | `name = "uart1";` | 双引号包裹 |
| 布尔 | `enable = true;` | true/false |
| uint8数组 | `data = [0x01, 0x02, 0xFF];` | 方括号包裹 |
| 字符串数组 | `names = ["tx", "rx"];` | 字符串列表 |

### 节点定义

```hcs
root {
    // 一级节点
    platform {
        // 属性键值对
        attr1 = 100;
        attr2 = "hello";

        // 二级子节点
        child_node {
            attr3 = 0x1000;
        }
    }
}
```

**规则**：
- 必须有且仅有一个`root`根节点
- 节点名只能包含字母、数字和下划线
- 节点用花括号`{}`包裹其内容
- 属性以分号`;`结尾

### Include文件包含

```hcs
#include "device_info/device_info.hcs"
#include "gpio/gpio_config.hcs"
#include "uart/uart_config.hcs"
```

### Template模板与继承

```hcs
root {
    device_info {
        // 定义模板
        template host {
            hostName = "";
            priority = 100;

            template device {
                template deviceNode {
                    policy = 0;
                    priority = 100;
                    preload = 0;
                    permission = 0664;
                    moduleName = "";
                    serviceName = "";
                    deviceMatchAttr = "";
                }
            }
        }

        // 使用模板（通过 :: 继承）
        my_host :: host {
            hostName = "platform_host";
            priority = 200;

            my_device :: device {
                uart_node :: deviceNode {
                    policy = 2;
                    priority = 100;
                    preload = 0;
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_UART";
                    serviceName = "HDF_PLATFORM_UART_1";
                    deviceMatchAttr = "hdf_uart_config";
                }
            }
        }
    }
}
```

**模板继承规则**：
- 使用`::`操作符声明继承关系：`子节点名 :: 模板名 { ... }`
- 子节点**可以修改**模板中已定义的属性值
- 子节点**不能新增**模板中未定义的属性
- 子节点**不能删除**模板中已定义的属性
- 模板支持多级嵌套（host → device → deviceNode）

### 节点复制

```hcs
root {
    config {
        uart_base {
            baudRate = 115200;
            fifoSize = 128;
            flags = 0;
        }

        // uart_debug复制uart_base的全部内容
        uart_debug : uart_base {
            // 可以在复制基础上修改
            baudRate = 9600;
        }
    }
}
```

**注意**：节点复制使用单冒号`:`，区别于模板继承的双冒号`::`。

### 属性引用

```hcs
root {
    config {
        common {
            base_addr = 0xFE650000;
            clock_freq = 24000000;
        }

        uart1 {
            iomemBase = &config.common.base_addr;
            clkFreq = &config.common.clock_freq;
        }
    }
}
```

### Delete删除

```hcs
#include "base_config.hcs"

root {
    config {
        delete unused_peripheral;

        some_node {
            delete deprecated_attr;
        }
    }
}
```

**重要限制**：`delete`只能删除通过`#include`引入的内容，不能删除当前文件中直接定义的节点或属性。

### 条件编译

```hcs
#if defined(SOC_RK3568)
    #include "rk3568_platform.hcs"
#elif defined(SOC_HI3516)
    #include "hi3516_platform.hcs"
#endif

root {
    config {
#if defined(ENABLE_WIFI)
        wifi_config {
            chipType = "rtl8822";
            busType = 1;  // SDIO
        }
#endif
    }
}
```

### match_attr匹配属性

```hcs
// device_info.hcs 中
uart_node :: deviceNode {
    deviceMatchAttr = "hdf_uart_1_config";  // 匹配标识
}

// uart_config.hcs 中
root {
    uart_1_config {
        match_attr = "hdf_uart_1_config";  // 必须与上面一致
        baudRate = 115200;
        iomemBase = 0xFE650000;
    }
}
```

## hc-gen工具详解

### 命令行参数

```
用法: hc-gen [选项] <输入文件>

选项:
  -o <output>     指定输出文件路径
  -b              生成HCB二进制文件（默认模式）
  -c              生成配置树C源码（.c/.h）
  -m              生成配置宏头文件
  -d              反编译HCB文件为可读文本
  -t              生成配置树数据结构头文件
  -I <path>       添加include搜索路径
  -D <macro>      定义预处理宏（配合条件编译）
  -v              显示版本信息
  -h              显示帮助信息
```

### 典型使用示例

```bash
# 1. 编译HCS为HCB（最常用的场景）
hc-gen -o vendor/hihope/rk3568/hdf_config.hcb \
       -I vendor/hihope/rk3568/hdf_config/uhdf \
       vendor/hihope/rk3568/hdf_config/uhdf/hdf.hcs

# 2. 带条件编译宏的编译
hc-gen -o output.hcb \
       -DSOC_RK3568 \
       -DENABLE_CAMERA \
       -I include_path \
       input.hcs

# 3. 生成C源码（适用于LiteOS-M等弱性能环境）
hc-gen -o config_tree.c -c input.hcs

# 4. 反编译HCB查看配置内容（调试用途）
hc-gen -d system.hcb > config_dump.txt
```

## HCS在HDF驱动框架中的角色

```
┌─────────────────────────────────────────────────────┐
│                  HDF 驱动框架架构                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────┐    ┌──────────────┐    ┌───────────┐  │
│  │ 驱动开发者 │──→│ .hcs配置文件  │──→│  hc-gen   │  │
│  │          │    │ (源码级配置)   │    │ (编译器)   │  │
│  └──────────┘    └──────────────┘    └─────┬─────┘  │
│                                            │        │
│                                      ┌─────▼─────┐  │
│                                      │  .hcb文件  │  │
│                                      │(二进制配置) │  │
│                                      └─────┬─────┘  │
│                                            │        │
│  ┌──────────┐    ┌──────────────┐    ┌─────▼─────┐  │
│  │ 驱动模块  │←──│  HCS Parser  │←──│ HDF框架    │  │
│  │(读取配置) │    │ (解析配置树)  │    │ (加载驱动) │  │
│  └──────────┘    └──────────────┘    └───────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### HCS编译流程

```
.hcs源文件 ──→ hc-gen编译 ──→ .hcb二进制 ──→ 打包进系统镜像
                                         │
                                    系统启动时
                                         │
                              HDF框架加载.hcb文件
                                         │
                              HCS Parser重建配置树
                                         │
                              驱动模块通过API读取配置
```

### 运行时API

| API函数 | 功能 |
|---------|------|
| `HdfGetDeviceResourceNode()` | 获取当前设备的配置节点 |
| `HdfReadU32()` | 读取uint32类型属性 |
| `HdfReadString()` | 读取字符串类型属性 |
| `HdfReadU8Array()` | 读取uint8数组属性 |
| `HdfGetChildByName()` | 按名称获取子节点 |
| `HdfTraverseDeviceResource()` | 遍历配置节点的所有属性 |
| `HdfGetDeviceMatchAttr()` | 获取设备匹配属性 |

## Lite系统设备配置目录结构

### L0轻量系统

```
vendor/<vendor>/<board>/
├── config.json                       # ★ 产品编译配置（核心）
├── include/
│   └── board_config.h                # ★ 板级外设引脚映射头文件
├── src/
│   └── board_init.c                  # 板级初始化代码
└── BUILD.gn                          # build_lite编译入口

device/board/<vendor>/<board>/
├── config.gni                        # 单板编译配置
└── <board>.mk                        # Makefile配置（可选）

device/soc/<vendor>/<chip>/
├── sdk_liteos/
│   └── include/                      # 芯片SDK头文件
│       ├── soc_regs.h               # SoC寄存器定义
│       └── hal_gpio.h                # HAL GPIO接口
└── common/
    └── soc.mk                        # SoC通用配置
```

> ⚠️ **L0关键特点**：没有`hdf_config/`目录，没有`.hcs`文件。所有设备配置通过`config.json`和`board_config.h`完成。

### L1小型系统

```
vendor/<vendor_name>/<product_name>/
├── config.json                           # 产品编译配置
├── hdf_config/
│   └── uhdf/                             # 精简版HDF配置根目录
│       ├── hdf.hcs                       # 主入口
│       ├── device_info/
│       │   └── device_info.hcs           # 设备信息配置（精简版）
│       ├── gpio/
│       │   └── gpio_config.hcs           # GPIO配置
│       ├── uart/
│       │   └── uart_config.hcs           # UART配置
│       ├── i2c/
│       │   └── i2c_config.hcs            # I2C配置
│       └── spi/
│           └── spi_config.hcs            # SPI配置
```

## 附录：HCS语法速查表

```
┌──────────────────────────────────────────────────────────┐
│                    HCS 语法速查表                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  基本结构:                                                │
│    root { node_name { key = value; } }                   │
│                                                          │
│  数据类型:                                                │
│    整数: 100  |  十六进制: 0xFF  |  八进制: 0644          │
│    字符串: "text"  |  布尔: true/false                    │
│    数组: [0x01, 0x02]  |  字符串数组: ["a", "b"]          │
│                                                          │
│  文件包含:                                                │
│    #include "path/to/file.hcs"                           │
│                                                          │
│  模板定义:                                                │
│    template node_name { key = default_value; }           │
│                                                          │
│  模板继承:                                                │
│    child_name :: template_name { key = new_value; }      │
│                                                          │
│  节点复制:                                                │
│    new_name : source_name { key = override_value; }      │
│                                                          │
│  属性引用:                                                │
│    key = &root.node.other_key;                           │
│                                                          │
│  删除(仅限include引入):                                    │
│    delete node_or_attr_name;                             │
│                                                          │
│  条件编译:                                                │
│    #if defined(MACRO) ... #elif ... #endif               │
│                                                          │
│  匹配属性:                                                │
│    match_attr = "unique_identifier";                     │
│                                                          │
│  注释:                                                    │
│    /* 块注释 */  // 行注释                                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## 附录：deviceNode属性速查表

```
┌──────────────────────────────────────────────────────────┐
│              deviceNode 标准属性速查表                      │
├──────────────┬────────┬──────────────────────────────────┤
│ 属性名        │ 类型   │ 说明                              │
├──────────────┼────────┼──────────────────────────────────┤
│ policy       │ int    │ 0=不发布,1=内核态,2=用户态          │
│ priority     │ int    │ 加载优先级(越大越高)                 │
│ preload      │ int    │ 0=正常,1=延迟,2=按需               │
│ permission   │ octal  │ 设备节点权限(如0644)                │
│ moduleName   │ string │ 驱动模块名(对应HdfDriverEntry)      │
│ serviceName  │ string │ 对外服务名(用户态获取服务的标识)      │
│ deviceMatchAttr│string│ 关联资源配置的匹配标识               │
└──────────────┴────────┴──────────────────────────────────┘
```

---

## 真实示例参考

完整真实芯片配置样本见本 SKILL 的 `examples/` 目录：
- L0: `examples/l0/`（Hi3861 / STM32F407 等）
- L1: `examples/l1/`（Hi3516DV300 全套 HCS）
