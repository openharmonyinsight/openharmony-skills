# 实测生成模式（手工产物提炼）

> 来源：L0 IoT HAL（hi3861v100）/ L0（rk2206）/ L1 HDF（hi3516cv610）手工适配产物
> 用途：给 ohos-dev-hal-skeleton-gen 单点调用提供实战验证的 API 映射套路、BUILD.gn 模板、HCS 配对写法

---

## 一、API 映射套路（L0 调 SDK 函数路线）

不同厂商 SDK API 命名差异大，生成 L0 驱动前必须读 SDK 头确认命名族。以下模式来自实测案例。

### 1.1 Hi3861 SDK — `hi_*` 小写命名（实测）

**映射模式**：直接类型转换 + 返回值透传（枚举 1:1 兼容）

```c
#include "iot_errno.h"
#include "iot_gpio.h"
#include "hi_gpio.h"   /* SDK 头 */

/* 参数类型强制转换，返回值直接透传（HI API 与 OH API 返回值兼容） */
unsigned int IoTGpioSetDir(unsigned int id, IotGpioDir dir)
{
    return hi_gpio_set_dir((hi_gpio_idx)id, (hi_gpio_dir)dir);
}

unsigned int IoTGpioSetOutputVal(unsigned int id, IotGpioValue val)
{
    return hi_gpio_set_ouput_val((hi_gpio_idx)id, (hi_gpio_value)val);
}

/* 中断注册：枚举强转，回调函数签名兼容 */
unsigned int IoTGpioRegisterIsrFunc(unsigned int id, IotGpioIntType intType,
                                    IotGpioIntPolarity intPolarity,
                                    GpioIsrCallbackFunc func, char *arg)
{
    return hi_gpio_register_isr_function((hi_gpio_idx)id,
                                         (hi_gpio_int_type)intType,
                                         (hi_gpio_int_polarity)intPolarity,
                                         (gpio_isr_callback)func, arg);
}
```

**特点**：
- 枚举 1:1 数值兼容，直接强转无需中间转换函数
- 返回值透传（`hi_u32` → `unsigned int`，`HI_ERR_*` 与 `IOT_*` 数值兼容）
- 全局状态管理用静态数组（如 `g_gpioMap[HI_GPIO_IDX_MAX]` 跟踪 pin 初始化状态）
- **注意**：`hi_gpio_set_ouput_val` 是 SDK 的拼写（output 拼成 ouput），别"纠正"成 output

### 1.2 RK2206 Lockzhiner SDK — `lz_*`/`Lz*` 命名（实测）

**映射模式**：返回值规范化 + 中间转换层（枚举不兼容需转换函数）

```c
#include "iot_errno.h"
#include "iot_gpio.h"
#include "lz_hardware.h"   /* SDK 头 */

/* 返回值转换：LZ_HARDWARE_SUCCESS → IOT_SUCCESS */
unsigned int IoTGpioInit(unsigned int id)
{
    unsigned int ret = LzGpioInit((GpioID)id);
    return (ret == LZ_HARDWARE_SUCCESS) ? IOT_SUCCESS : IOT_FAILURE;
}

/* Get 类需先读 SDK 枚举再转 OH 枚举 */
unsigned int IoTGpioGetDir(unsigned int id, IotGpioDir *dir)
{
    LzGpioDir lzDir;
    unsigned int ret = LzGpioGetDir((GpioID)id, &lzDir);
    if (ret != LZ_HARDWARE_SUCCESS) {
        return IOT_FAILURE;
    }
    *dir = (IotGpioDir)lzDir;   /* 枚举数值兼容可直接转 */
    return IOT_SUCCESS;
}

/* OH 双参数（intType + intPolarity）→ LZ 单枚举，需转换函数 */
static LzGpioIntType HalGpioIntTypeToLz(IotGpioIntType intType, IotGpioIntPolarity intPolarity)
{
    if (intType == IOT_INT_TYPE_LEVEL) {
        return (intPolarity == IOT_GPIO_EDGE_FALL_LEVEL_LOW)
               ? LZGPIO_INT_LEVEL_LOW : LZGPIO_INT_LEVEL_HIGH;
    }
    return (intPolarity == IOT_GPIO_EDGE_FALL_LEVEL_LOW)
           ? LZGPIO_INT_EDGE_FALLING : LZGPIO_INT_EDGE_RISING;
}

/* SetIsrMask：OH mask(0/1) → LZ Enable/Disable 两个函数 */
unsigned int IoTGpioSetIsrMask(unsigned int id, unsigned char mask)
{
    unsigned int ret;
    if (mask) {
        ret = LzGpioDisableIsr((GpioID)id);
    } else {
        ret = LzGpioEnableIsr((GpioID)id);
    }
    return (ret == LZ_HARDWARE_SUCCESS) ? IOT_SUCCESS : IOT_FAILURE;
}
```

**特点**：
- 返回值统一转换（`LZ_HARDWARE_SUCCESS → IOT_SUCCESS`，非成功一律 `IOT_FAILURE`）
- 中断类型+极性双参数合并成单枚举（4 种组合：LEVEL_LOW/LEVEL_HIGH/EDGE_FALLING/EDGE_RISING）
- `SetIsrMask` 在 LZ SDK 里是 `EnableIsr`/`DisableIsr` 两个函数，需按 mask 值分派
- `SetIsrMode` LZ SDK 无对应，标 no-op 返回 SUCCESS（注释说明限制）

### 1.3 Hi3516cv610 SDK — `osal_*`+`ot_*`，无 GPIO 外设 API（实测）

**映射模式**：SDK 不提供通用 GPIO/UART 外设 API → 走寄存器直写路线

实测案例探查结论：Hi3516cv610 SDK `/srv/workspace/Hi3516CV610/soc/` 下：
- `include/` 顶层无 `ot_gpio.h`/`hi_gpio.h`（只有 `ot_*` 媒体接口和 `osal_*` 接口）
- `drivers/interdrv/` 下无 `gpio` 目录（只有 `ot_adc`/`wtdg`/`mipi_rx`/`sysconfig`）
- `ot_user.h` 是 `#include <linux/gpio.h>`（走 Linux 内核 gpiolib，非厂商外设 API）
- GPIO IP 为 ARM PrimeCell PL061（dtsi `compatible="arm,pl061"`），寄存器操作用 OSAL 封装

**L1 HDF 驱动寄存器直写模式**（PL061）：
```c
/* 读 HCS 配置（DeviceResourceIface，非 HdfRead*） */
static bool ReadDrs(const struct DeviceResourceNode *node, struct GpioInfo *info)
{
    struct DeviceResourceIface *iface = DeviceResourceGetIfaceInstance(HDF_CONFIG_SOURCE);
    if (iface == NULL || iface->GetUint32 == NULL) { return false; }
    if (iface->GetUint32(node, "regBase", &info->phyBase, 0) != HDF_SUCCESS) { return false; }
    if (iface->GetUint32(node, "groupNum", &info->groupNum, 0) != HDF_SUCCESS) { return false; }
    /* ... */
    return true;
}

/* 寄存器读写用 OSAL 封装（OsalIoRemap + OSAL_READL/OSAL_WRITEL） */
dev->regBase = (volatile void *)OsalIoRemap(dev->phyBase, dev->groupNum * dev->regStep);
uint32_t val = OSAL_READL(dev->regBase + PL061_GPIO_DIR);
OSAL_WRITEL(val, dev->regBase + PL061_GPIO_DIR);
```

> **关键**：`ot_*` 是媒体/安全子系统接口（vi/vpss/venc/cipher/km/otp），HAL 驱动不直接调。`osal_*` 是 OSAL 抽象层（OsalIoRemap/OsalMemCalloc/OsalMutex 等），L1 HDF 驱动必须用。

### 1.4 API 命名族识别速查

| SDK 头文件命名 | 厂商 | API 前缀 | 映射模式 |
|--------------|------|---------|---------|
| `hi_gpio.h`/`hi_i2c.h`/`hi_uart.h` | HiSilicon Hi3861 | `hi_*` 小写 | 直接强转 + 透传 |
| `lz_hardware.h` | Lockzhiner RK2206 | `lz_*`/`Lz*` | 返回值转换 + 中间转换函数 |
| `osal_io.h`/`osal_mem.h` | OpenHarmony OSAL | `osal_*`/`Osal*` | L1 HDF 必用（寄存器/内存/锁） |
| `ot_*_api.h` | HiSilicon Hi3516cv610 | `ot_*` | 媒体/安全接口，HAL 不直接调 |
| `hal_gpio.h`/`HalGpio*` | 通用 HAL | `Hal*` 大写 | 按实际签名映射 |

**识别方法**：grep SDK `include/` 顶层 `*.h` 文件名前缀，判断命名族，别凭芯片名猜。

---

## 二、BUILD.gn 模板

### 2.1 L0 IoT HAL BUILD.gn（实测 hi3861v100）

```gn
# device/soc/hisilicon/hi3861v100/hi3861_adapter/hals/iot_hardware/wifiiot_lite/BUILD.gn
static_library("hal_iothardware") {
  sources = [
    "hal_iot_gpio.c",
    "hal_iot_uart.c",
    "hal_iot_i2c.c",
    "hal_iot_pwm.c",
    "hal_iot_flash.c",
    "hal_iot_watchdog.c",
    "hal_lowpower.c",
    "hal_reset.c",
  ]
  include_dirs = [
    "//commonlibrary/utils_lite/include",
    "//base/iot_hardware/peripheral/interfaces/inner_api",
    "//device/soc/hisilicon/hi3861v100/sdk_liteos/include",   # SDK 头
  ]
}
```

**特点**：
- `static_library` 聚合所有 hal_iot_*.c 成一个库
- `include_dirs` 必含 SDK 头路径（`sdk_liteos/include`）+ OH IoT HAL 接口路径
- L0 无 HCS、无 hdf_driver 模板

### 2.2 L0 WiFi HAL BUILD.gn（实测 hi3861v100）

```gn
import("//build/lite/ndk/ndk.gni")

static_library("wifiservice") {
  sources = [
    "source/wifi_device.c",
    "source/wifi_device_util.c",
    "source/wifi_hotspot.c",
  ]
  include_dirs = [
    "//device/soc/hisilicon/hi3861v100/sdk_liteos/include",
    "//foundation/communication/wifi_lite/interfaces/wifiservice",
    "//kernel/liteos_m/kal",
  ]
}

if (ohos_kernel_type == "liteos_m") {
  ndk_lib("wifiservice_ndk") {
    deps = [ ":wifiservice" ]
    head_files = [ "//foundation/communication/wifi_lite/interfaces/wifiservice" ]
  }
}
```

**特点**：
- WiFi 驱动独立 `static_library`，不与 hal_iot_* 混编
- `ndk_lib` 声明 NDK 暴露（条件：`ohos_kernel_type == "liteos_m"`）
- `head_files` 指向 OH WiFi 服务接口头

### 2.3 L1 HDF BUILD.gn（实测 hi3516cv610）

```gn
import("//build/lite/config/component/lite_component.gni")
import("//drivers/hdf_core/adapter/khdf/khdf.gni")

hdf_driver("hdf_gpio_hi3516cv610") {
  sources = [ "gpio_hi3516cv610.c" ]
  include_dirs = [
    ".",
    "//drivers/hdf_core/framework/include/core",
    "//drivers/hdf_core/framework/include/utils",
    "//drivers/hdf_core/framework/include/osal",
    "//drivers/hdf_core/framework/include/platform",
    "//drivers/hdf_core/framework/include/platform/gpio",
  ]
  cflags = [ "-Wall", "-Wextra", "-Wno-unused-parameter" ]
}
```

**特点**：
- `hdf_driver` 模板（L1 专用），`module_name`（此处 `hdf_gpio_hi3516cv610`）决定 .ko 文件名
- `include_dirs` 必含 HDF 核心层头路径（core/utils/osal/platform）
- 注意：BUILD.gn 的 `module_name` 与 .c `HDF_INIT` 的 `moduleName` 是不同维度，无需相等

---

## 三、HCS 配对写法（L1）

### 3.1 device_info.hcs ↔ *_config.hcs 严格配对（实测案例）

**device_info.hcs（声明侧）**：
```hcs
root {
    device_info {
        platform :: host {
            hostName = "platform_host";
            priority = 50;

            device_watchdog :: device {
                device0 :: deviceNode {
                    policy = 2;
                    priority = 20;
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_WATCHDOG";
                    serviceName = "HDF_PLATFORM_WATCHDOG_0";
                    deviceMatchAttr = "hisilicon_hi35xx_watchdog_0";  /* ← 对端 */
                }
            }

            device_uart :: device {
                device0 :: deviceNode {
                    policy = 1;
                    priority = 40;
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_UART";
                    serviceName = "HDF_PLATFORM_UART_0";
                    deviceMatchAttr = "hisilicon_hi35xx_uart_0";     /* ← 对端 */
                }
            }
        }
    }
}
```

**watchdog_config.hcs（资源侧）**：
```hcs
root {
    platform {
        template watchdog_controller {
            id = 0;
            match_attr = "";
            regBase = 0x12050000;
            regStep = 0x1000;
        }
        controller_0x12050000 :: watchdog_controller {
            match_attr = "hisilicon_hi35xx_watchdog_0";  /* ← 与 deviceMatchAttr 严格相等 */
        }
    }
}
```

**uart_config.hcs（多实例 + template 继承）**：
```hcs
root {
    platform {
        template uart_controller {
            match_attr = "";
            num = 0;
            baudrate = 115200;
            regPbase = 0x120a0000;
            interrupt = 38;
        }
        controller_0x120a0000 :: uart_controller {
            match_attr = "hisilicon_hi35xx_uart_0";   /* ← 与 device_info.hcs device0 配对 */
        }
        controller_0x120a1000 :: uart_controller {
            num = 1;
            baudrate = 9600;
            regPbase = 0x120a1000;
            interrupt = 39;
            match_attr = "hisilicon_hi35xx_uart_1";   /* ← 与 device_info.hcs device1 配对 */
        }
    }
}
```

### 3.2 L1 Linux 体系 `linux_*_adapter` 并存模式（实测案例）

Hi3516cv610 产品 `device_info.hcs` 里部分外设走 Linux 内核适配器（非自研 HDF 驱动）：

```hcs
device_gpio :: device {
    device0 :: deviceNode {
        policy = 2;
        moduleName = "HDF_PLATFORM_GPIO_MANAGER";  /* GPIO 管理器 */
        serviceName = "HDF_PLATFORM_GPIO_MANAGER";
    }
    device1 :: deviceNode {
        policy = 0;
        moduleName = "linux_gpio_adapter";          /* ← 走 Linux gpiolib，非自研 */
        deviceMatchAttr = "linux_gpio_adapter";
    }
}

device_i2c :: device {
    device0 :: deviceNode {
        policy = 2;
        moduleName = "HDF_PLATFORM_I2C_MANAGER";
        serviceName = "HDF_PLATFORM_I2C_MANAGER";
        deviceMatchAttr = "hdf_platform_i2c_manager";
    }
    device1 :: deviceNode {
        policy = 0;
        moduleName = "linux_i2c_adapter";           /* ← 走 Linux i2c-dev，非自研 */
        deviceMatchAttr = "linux_i2c_adapter";
    }
}
```

**对应的 gpio_config.hcs**（资源侧也用 `linux_gpio_adapter`）：
```hcs
root {
    platform {
        gpio_config {
            controller_0x120d0000 {
                match_attr = "linux_gpio_adapter";   /* ← 与 device_info.hcs device1 配对 */
                groupNum = 12;
                bitNum = 8;
                regBase = 0x120d0000;
                regStep = 0x1000;
                irqStart = 48;
                irqShare = 0;
            }
        }
    }
}
```

**生成自研驱动替换 `linux_*_adapter` 时的做法**：
1. 生成自研 `*_config.hcs`（如 `match_attr = "hisilicon_hi3516cv610_gpio"`）
2. **一并生成 device_info.hcs 对端片段**：把 `device1` 的 `moduleName` 改为自研驱动名（如 `hisi_hi3516cv610_gpio_driver`）、`deviceMatchAttr` 改为 `hisilicon_hi3516cv610_gpio`
3. 或并存（device1 保留 linux_adapter，device2 加自研驱动）——但同一外设两套驱动会冲突，通常替换

> **实测翻车根因**：只生成 `*_config.hcs`（match_attr=hisilicon_hi3516cv610_gpio），没改 device_info.hcs 的 device1（仍是 linux_gpio_adapter）→ HDF 框架找不到 moduleName=hisi_hi3516cv610_gpio_driver 的 deviceNode → .ko 加载了但 Bind/Init 不被调用。

### 3.3 IRQ +32 GIC 换算（L1 Linux/HDF，实测翻车点）

DTS `interrupts = <0 23 4>` 三元组：`0`=GIC_SPI，`23`=SPI 编号，`4`=触发类型。

GIC IRQ domain xlate 对 SPI 做 `hwirq = spi_param + 32`（`drivers/irqchip/irq-gic.c`）：
- DTS SPI 23 → Linux IRQ 55（23+32）
- `OsalRegisterIrq(irq, …)` 的 `irq` 参数是 Linux IRQ 号（virq），直接调 `request_threaded_irq(irq, …)` 不做 +32
- **HCS `irqStart` 必须填 +32 后的值**（55），不是原始 SPI 号（23）

**同族佐证**：hi3516dv300 `gpio_config.hcs` `irqStart=48` 对应 DTS SPI 16（16+32=48）。

**PPI 换算不同**：三元组首字段=1（PPI），`hwirq = ppi_param + 16`，别套 +32。

---

## 四、L0 驱动文件清单（实测案例）

### 4.1 Hi3861v100 L0 IoT HAL（实测，8 驱动 + WiFi）

| 文件 | 外设 | SDK API 族 |
|----|------|-----------|
| `hal_iot_gpio.c` | GPIO | `hi_gpio_*` |
| `hal_iot_uart.c` | UART | `hi_uart_*` |
| `hal_iot_i2c.c` | I2C | `hi_i2c_*` |
| `hal_iot_pwm.c` | PWM | `hi_pwm_*` |
| `hal_iot_flash.c` | Flash | `hi_flash_*` |
| `hal_iot_watchdog.c` | Watchdog | `hi_watchdog_*` |
| `hal_lowpower.c` | 低功耗 | `hi_lpc_*` |
| `hal_reset.c` | 复位 | `hi_sys_*` |
| `wifi_device.c` | WiFi STA | `hi_wifi_*` |
| `wifi_hotspot.c` | WiFi AP | `hi_wifi_*` |
| `wifi_device_util.c` | WiFi 工具 | `hi_wifi_*` |

### 4.2 RK2206 L0（实测，12 驱动）

| 文件 | 外设 | SDK API 族 |
|----|------|-----------|
| `hal_iot_gpio.c` | GPIO | `LzGpio*` |
| `hal_iot_uart.c` | UART | `LzUart*` |
| `hal_iot_i2c.c` | I2C | `LzI2c*` |
| `hal_iot_pwm.c` | PWM | `LzPwm*` |
| `hal_iot_flash.c` | Flash | `LzFlash*` |
| `hal_iot_watchdog.c` | Watchdog | `LzWatchdog*` |
| `hal_lowpower.c` | 低功耗 | `LzLpc*` |
| `hal_reset.c` | 复位 | `LzReset*` |
| `hal_file.c` | 文件 | `LzFile*` |
| `wifi_device.c` | WiFi STA | `LzWifi*` |
| `wifi_hotspot.c` | WiFi AP | `LzWifi*` |
| `wifi_device_util.c` | WiFi 工具 | `LzWifi*` |

---

## 五、实测翻车根因（skill 正确性缺口）

### 5.1 ohos-dev-hal-skeleton-gen 翻车点

| 翻车点 | 根因 | 修正 |
|--------|------|------|
| IRQ+32 换算 | `irqStart=23` 是 GIC 原始 SPI 号，Linux 上应为 55（SPI 23+32） | HCS `irqStart` 填 Linux IRQ 号（+32），非 DTS SPI 号 |
| HCS 集成断裂 | 只写 `*_config.hcs`（match_attr=hisilicon_hi3516cv610_gpio），没改 device_info.hcs（仍是 linux_gpio_adapter） | **一并生成 device_info.hcs 对端 deviceNode 片段**，两侧 match_attr 严格相等 |
| 编译过≠正确 | .ko 编译通过 + HCS 聚合编译通过，但运行时 HDF 框架找不到 deviceNode，Bind/Init 不被调用 | Step 4 加运行时配对检查（不只验字符串相等，验 deviceNode 实例存在） |

### 5.2 共性教训

- **编译器查不出的运行时错误**：IRQ 号是合法 uint32、HCS 配对是运行时框架行为——只有核 IRQ 换算规则 + 核 HCS 双侧配对才能抓到
- **只写一侧=没写**：HCS 配对必须两侧（device_info.hcs + *_config.hcs）一起生成，只写 *_config.hcs 等于只接了插头一半
- **SDK API 命名别假设**：Hi3516cv610 SDK 无 GPIO 外设 API（走寄存器直写），Hi3861 用 hi_*，RK2206 用 Lz*——必须读 SDK 头确认
