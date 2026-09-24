# L0 Mini 系统：IoT HAL 驱动模型参考

> **来源**：步骤 8-16 + `session_kal.json` 实际执行记录
> **适用场景**：target_system = **L0 轻量系统** 时，P3 阶段的驱动开发模式
> **不适用于**：L1 小型系统（L1 使用 HDF Platform Driver 模型，见 `hcs-syntax-and-config.md`）

## 核心概念

L0 Mini 系统的驱动模型是 **IoT HAL 接口**——OpenHarmony 定义的一套标准外设 API，
驱动开发者的工作是**将 OH IoT HAL API 包装为芯片 SDK 的底层调用**。

```
┌─────────────────────────────────────┐
│         应用层 / 测试用例           │  调用
│    IoTGpioInit() / IoTUartRead()   │ ──────┐
└─────────────────┬───────────────────┘      │
                  │                          │
┌─────────────────▼───────────────────┐      │
│     IoT HAL 驱动层（你需要写的）       │      │
│   hal_iot_gpio.c                    │      │
│   hal_iot_uart.c                    │ ◄───┘
│   hal_iot_i2c.c / pwm / flash ...   │  实现 OH API → 调用 SDK API
└─────────────────┬───────────────────┘
                  │ 调用
┌─────────────────▼───────────────────┐
│        芯片 SDK 层（厂商提供）         │
│   hi_gpio.h / hi_uart.h / hi_i2c.h  │  不修改
│   hi_gpio_init() / hi_uart_read()   │
└─────────────────────────────────────┘
```

## 与 L1 HDF 模式的关键区别

| 维度 | L0 IoT HAL 模式 | L1 HDF 模式 |
|:----:|:---------------:|:-----------:|
| **头文件** | `#include "iot_gpio.h"` (OH 标准) | `#include "hdf_device_desc.h"` (HDF) |
| **入口函数** | 直接导出 `IoTGpioInit` 等 | `Bind/Init/Release/Dispatch` 回调 |
| **配置文件** | 无 HCS，纯 C 代码 | 需要 `.hcs` 设备树配置 |
| **注册方式** | 编译进 static_library 即可 | `HDF_DEVICE_DEFINE()` + HCS match_attr |
| **枚举转换** | IotGpioDir → hi_gpio_dir_e（必须） | HDF 配置自动处理 |
| **代码量/驱动** | 22-113 行（薄包装） | 通常更厚（含状态机/协议栈）|
| **位置** | `hi3861_adapter/hals/iot_hardware/wifiiot_lite/` | `hdf/models/` |

## 9 个标准 IoT HAL 驱动的完整 API 清单

### 1. GPIO (`hal_iot_gpio.c`)

**OH 头文件**: `#include "iot_gpio.h"`
**SDK 头文件**: `#include "hi_gpio.h"`

```c
// 必须实现的 API（7 个）:
unsigned int IoTGpioInit(unsigned int id);
unsigned int IoTGpioSetDir(unsigned int id, IotGpioDir dir);
unsigned int IoTGpioGetDir(unsigned int id, IotGpioDir *dir);
unsigned int IoTGpioSetOutputVal(unsigned int id, IotGpioVal val);
unsigned int IoTGpioGetOutputVal(unsigned int id, IotGpioVal *val);
unsigned int IoTGpioRegisterIsrFunc(unsigned int id, IotGpioIntType intType,
                                     IotGpioIntPolarity intPolarity,
                                     GpioIsrCallbackFunc func, char *arg);
unsigned int IoTGpioUnregisterIsrFunc(unsigned int id);

// 枚举映射表:
IotGpioDir::IOT_GPIO_DIR_IN  → hi_gpio_dir_e::HI_GPIO_DIR_IN
IotGpioDir::IOT_GPIO_DIR_OUT → hi_gpio_dir_e::HI_GPIO_DIR_OUT
IotGpioVal::IOT_GPIO_VAL_LOW  → 0
IotGpioVal::IOT_GPIO_VAL_HIGH → 1
// 中断类型和极性也有对应映射
```

### 2. UART (`hal_iot_uart.c`)

**OH**: `iot_uart.h` → **SDK**: `hi_uart.h`

```c
unsigned int IoTUartInit(unsigned int id, const IotUartAttribute *param);
unsigned int IoTUartRead(unsigned int id, unsigned char *data, unsigned int dataLen);
unsigned int IoTUartWrite(unsigned int id, const unsigned char *data, unsigned int dataLen);
unsigned int IoTUartDeinit(unsigned int id);
// 可选: IoTUartSetBaud / GetBaud

// IotUartAttribute → hi_uart_attribute 映射:
// .baudRate → .baud_rate
// .dataBits → .data_bits (枚举映射)
// .stopBits → .stop_bits (枚举映射)
// .parity → .parity (枚举映射)
```

### 3. I2C (`hal_iot_i2c.c`)

**OH**: `iot_i2c.h` → **SDK**: `hi_i2c.h`

```c
unsigned int IoTI2cInit(unsigned int id, const IotI2cAttr *attr);
unsigned int IoTI2cDeinit(unsigned int id);
unsigned int IoTI2cWrite(unsigned int id, unsigned short deviceAddr,
                     const unsigned char *data, unsigned int dataLen);
unsigned int IoTI2cRead(unsigned int id, unsigned short deviceAddr,
                    unsigned char *data, unsigned int dataLen);
```

### 4. PWM (`hal_iot_pwm.c`)

**OH**: `iot_pwm.h` → **SDK**: `hi_pwm.h`

```c
unsigned int IoTPwmInit(unsigned int port);
unsigned int IoTPwmStart(unsigned int port, unsigned int duty, unsigned int freq);
unsigned int IoTPwmStop(unsigned int port);
// 注意: freq 和 duty 需要根据芯片时钟计算实际寄存器值
```

### 5-9. Flash / Watchdog / LowPower / Reset

遵循相同模式。每个驱动的实现模板：

```c
#include "iot_xxx.h"      // OH 标准 API
#include "hi_xxx.h"      // 芯片 SDK API

unsigned int IoTXxxFunction(params) {
    // 1. 参数校验（id 范围检查等）
    if (id >= MAX_PORT_NUM) { return IOT_FAILURE; }

    // 2. 枚举/参数类型转换（如需要）
    xxx_sdk_type sdk_param = convert_to_sdk(params);

    // 3. 调用 SDK 函数
    int ret = hi_xxx_function(id, sdk_param, ...);

    // 4. 返回值映射
    return (ret == 0) ? IOT_SUCCESS : IOT_FAILURE;
}
```

## IoT HAL BUILD.gn 模板

```gn
import("//build/lite/config/component/LiteComponent.gni")

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
        "//utils/native/lite/include",
        "//base/hiviewdfx/hilog_lite/interfaces/native/kits/hilog_lite",
        "//device/soc/{company}/{soc}/sdk_liteos/platform/include",    # SDK 头文件
        "//device/soc/{company}/{soc}/{adapter}/hals/iot_hardware/wifiiot_lite", # 自身目录
    ]
}

lite_component("iot_hardware_adapter") {
    target_type = "static"
    deps = [ ":hal_iothardware" ]
    features = []
}
```

## 判断使用哪种模式的决策规则

在 P3 阶段开始时，根据 `target_system` 选择驱动模型：

```
if target_system == "L0":
    驱动模型 = IoT_HAL
    输出目录 = hi3861_adapter/hals/iot_hardware/wifiiot_lite/
    配置方式 = 纯 C 代码（无 HCS）
    参考文件 = 本文档 + ohos-dev-soc-spec-parse/references/hi3861v100-adapter-structure.md
    
elif target_system == "L1":
    驱动模型 = HDF_Platform_Driver
    输出目录 = hdf/models/
    配置方式 = HCS (.hcs) + HDF Device 定义
    参考文件 = hcs-syntax-and-config.md
```
