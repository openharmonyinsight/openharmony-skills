# Hi3861V100 适配层目录结构（来自真实 AI Agent 执行记录）

> **来源**：`session_kal.json`(HAL适配) + `session_hal.json`(KAL补全)
> **芯片**：Hi3861V100 (Hisilicon, RISC-V rv32imac, LiteOS-M Mini系统)
> **价值**：展示 L0 Mini 系统的完整适配层文件组织——IoT HAL / KAL / WiFi / OTA / Utils 各模块的实际位置

## 完整目录树

```
device/soc/hisilicon/hi3861v100/
├── BUILD.gn                              # SoC 编译入口（5行）
├── README.md / README_zh.md
├── NOTICE
├── doc/
│   └── figures/
│
├── hi3861_adapter/                      # ★ 核心适配层（所有新增代码在此）
│   │
│   ├── BUILD.gn                          # 适配层总编译入口
│   │
│   ├── hals/                             # HAL 层（OH API → SDK API 包装）
│   │   ├── iot_hardware/wifiiot_lite/    # ★ IoT HAL 驱动（L0 核心驱动模型）
│   │   │   ├── hal_iot_gpio.c           # GPIO (IoTGpioInit/SetDir/Write/Read/RegisterIsrFunc)
│   │   │   ├── hal_iot_uart.c           # UART (IoTUartInit/Read/Write/Deinit)
│   │   │   ├── hal_iot_i2c.c            # I2C (IoTI2cInit/Write/Read/Deinit)
│   │   │   ├── hal_iot_pwm.c            # PWM (IoTPwmInit/Start/Stop)
│   │   │   ├── hal_iot_flash.c          # Flash (IoTFlashRead/Write/Erase/Init)
│   │   │   ├── hal_iot_watchdog.c       # Watchdog (IoTWatchDogEnable/Kick/Disable)
│   │   │   ├── hal_lowpower.c            # LowPower (LpcInit/LpcSetType)
│   │   │   ├── hal_reset.c              # Reset (RebootDevice)
│   │   │   └── BUILD.gn                 # static_library("hal_iothardware")
│   │   │
│   │   ├── communication/wifi_lite/     # WiFi 通信 HAL
│   │   │   ├── wifiservice/source/
│   │   │   │   ├── wifi_device.c        # STA: Connect/Disconnect/Scan/GetLinkedInfo
│   │   │   │   ├── wifi_device_util.c/h  # WiFi 工具函数
│   │   │   │   └── wifi_hotspot.c       # AP: EnableHotspot/DisableHotspot/SetConfig
│   │   │   ├── wifiservice/BUILD.gn
│   │   │   ├── wifiaware/source/
│   │   │   │   └── hal_wifiaware.c      # WiFi Aware
│   │   │   ├── wifiaware/BUILD.gn
│   │   │   └── BUILD.gn                  # wifi_lite 总入口
│   │   │
│   │   ├── update/                       # OTA 升级 HAL
│   │   │   ├── hal_hota_board.c          # HotaHalInit/WriteFragment/ReadFragment/PatchFirmware
│   │   │   └── BUILD.gn
│   │   │
│   │   └── utils/                        # 工具类 HAL
│   │       ├── sys_param/
│   │       │   ├── hal_sys_param.c       # HalGetSerial/ProductType/Manufacture/Brand
│   │       │   └── BUILD.gn
│   │       ├── token/
│   │       │   ├── hal_token.c           # HalReadToken/WriteToken/GetAcKey/SetAcKey
│   │       │   └── BUILD.gn
│   │       └── file/src/
│   │           ├── hal_file.c            # HalFileOpen/Close/Read/Write/Lseek
│   │           └── BUILD.gn
│   │
│   └── kal/                              # KAL 内核抽象层（OS API 适配）
│       ├── BUILD.gn                        # KAL 总编译入口
│       │
│       ├── cmsis/                         # CMSIS-OS2 → LiteOS-M 映射
│       │   ├── cmsis_liteos2.c            # osKernelInitialize/Start, osThreadNew, osDelay,
│       │   │                               # osMutexNew, osSemaphoreNew 等 (~1386行)
│       │   ├── kal.h                      # KAL 头文件
│       │   └── BUILD.gn
│       │
│       └── posix/                         # POSIX → LiteOS-M 映射
│           ├── src/
│           │   ├── pthread.c               # pthread_create/join → LOS_TaskCreate
│           │   ├── file.c                  # open/close/read/write/lseek → LiteOS FS
│           │   └── time.c                  # clock_gettime
│           └── BUILD.gn
│
└── sdk_liteos/                           # 芯片 SDK 原始代码（不修改，仅引用）
    ├── BUILD.gn                           # SDK 构建编排（build_ext_component + lite_component）
    ├── platform/
    │   ├── os/Huawei_LiteOS/targets/hi3861v100/include/
    │   │   └── target_config.h           # 内核裁剪配置（堆/任务/信号量等宏）
    │   └── include/                        # SDK 公开头文件
    └── third_party/                        # SDK 第三方库
```

## vendor 层（板级，非 SoC 级）

```
vendor/hisilicon/hispark_pegasus/           # 产品级（板级）适配
├── config.json                            # 产品定义（116行）
├── BUILD.gn                               # 产品编译入口
├── ohos.build                              # 子系统注册
└── hals/                                   # 板级 HAL（产品特定参数）
    ├── audio/product.gni
    ├── utils/sys_param/
    │   ├── BUILD.gn
    │   ├── hal_sys_param.c                # 产品序列号/型号/厂商实现
    │   └── vendor.para                    # 产品参数定义
    └── utils/token/
        ├── BUILD.gn
        └── hal_token.c                     # 安全 Token 读写实现

device/board/hisilicon/hispark_pegasus/     # 板级目录
├── liteos_m/config.gni                     # 板级构建配置（124行核心）
├── ohos.build                              # 板级子系统注册
└── README_zh.md
```

## L0 vs L1 适配层对比

| 维度 | L0 Mini 系统（Hi3861V100 模式） | L1 小型系统 |
|------|:-------------------------------:|:----------:|
| **驱动框架** | **IoT HAL 接口模型** (`iot_gpio.h`, `iot_uart.h` 等) | **HDF Platform Driver** (`HdfDriverEntry`, HCS 配置) |
| **配置系统** | config.json + config.gni + ohos.build | HDF HCS (.hcs) + Kconfig |
| **内核适配** | KAL (CMSIS-OS2 + POSIX) | 直接 syscall / 标准 Linux 接口 |
| **适配目录** | `hi3861_adapter/hals/` + `hi3861_adapter/kal/` | `hdf/` + 平台驱动目录 |
| **WiFi** | `hals/communication/wifi_lite/` | HDF WiFi 驱动 |
| **关键头文件** | `iot_xxx.h` (IoT HAL API) | `hdf_xxx.h` (HDF API) |

## IoT HAL API 映射模式

L0 驱动的核心模式是 **OH IoT HAL API → 芯片 SDK API 的薄包装**：

```c
// 以 GPIO 为例（hal_iot_gpio.c 模式）
#include "iot_gpio.h"         // OH 定义的标准接口
#include "hi_gpio.h"         // Hi3861 SDK 底层 API

unsigned int IoTGpioSetDir(unsigned int id, IotGpioDir dir) {
    // 1. 枚举转换：OH IotGpioDir → SDK hi_gpio_dir_e
    hi_gpio_dir_e sdk_dir = (dir == IOT_GPIO_DIR_IN) ? HI_GPIO_DIR_IN : HI_GPIO_DIR_OUT;
    // 2. 调用 SDK API
    return hi_gpio_setdir(id, sdk_dir);
}
```

**每个 IoT HAL 驱动都遵循相同的三步模式**：
1. **枚举类型转换**：OH 枚举 → SDK 枚举
2. **调用 SDK 函数**：直接委托给底层 SDK 实现
3. **返回值映射**：SDK 返回值 → OH 标准返回值 (`IOT_SUCCESS` / `IOT_FAILURE`)

### 9 个 IoT HAL 驱动的完整 API 清单

| 文件 | OH API（需实现） | SDK API（被调用） | 行数(约) |
|------|-------------------|------------------|:-------:|
| `hal_iot_gpio.c` | IoTGpioInit/SetDir/GetDir/OutputVal/RegisterIsrFunc | hi_gpio_init/setdir/getdir/outputval/register_isr_function | 113 |
| `hal_iot_uart.c` | IoTUartInit/Read/Write/Deinit | hi_uart_init/read/write/deinit | 68 |
| `hal_iot_i2c.c` | IoTI2cInit/Deinit/Write/Read | hi_i2c_init/write/read | 55 |
| `hal_iot_pwm.c` | IoTPwmInit/Start/Stop | hi_pwm_set_duty/freq/start/stop | 63 |
| `hal_iot_flash.c` | IoTFlashRead/Write/Erase/Init | hi_flash_read/write/erase | 44 |
| `hal_iot_watchdog.c` | IoTWatchDogEnable/Kick/Disable | hi_watchdog_enable/kick/disable | 34 |
| `hal_lowpower.c` | LpcInit/LpcSetType | hi_lpc_init/set_type | 28 |
| `hal_reset.c` | RebootDevice | hi_hard_reboot | 22 |
| **BUILD.gn** | static_library("hal_iothardware") | — | 30 |

## KAL (Kernel Abstraction Layer) 映射模式

### CMSIS-OS2 → LiteOS-M

| CMSIS-OS2 API | LiteOS-M 对应 | 说明 |
|:--------------|:---------------|:-----|
| `osKernelInitialize()` | （无需映射，LiteOS 自动初始化） | 内核已预初始化 |
| `osKernelStart()` | （无需映射，main() 后自动启动） | |
| `osThreadNew(func, arg, attr)` | `LOS_TaskCreate(&taskID, attr, func, arg)` | 参数：attr→LOS_TaskAttr_t |
| `osDelay(ticks)` | `LOS_TaskDelay(ticks)` | 直接映射 |
| `osMutexNew(attr)` | `LOS_MuxCreate(&muxId)` | |
| `osSemaphoreNew(max, init, attr)` | `LOS_SemCreate(&semId, ...)` | |

### POSIX → LiteOS-M

| POSIX API | LiteOS-M 对应 | 说明 |
|:----------|:-------------|:-----|
| `open(path, flags)` | `LOS_Open(path, flags)` | |
| `close(fd)` | `LOS_Close(fd)` | |
| `read(fd, buf, size)` | `LOS_Read(fd, buf, size)` | |
| `write(fd, buf, size)` | `LOS_Write(fd, buf, size)` | |
| `lseek(fd, offset, whence)` | `LOS_Seek(fd, offset, whence)` | |
| `pthread_create(thread, attr, func, arg)` | `LOS_TaskCreate(&taskID, ..., func, arg)` | |
| `pthread_join(thread, retval)` | `LOS_TaskJoin(taskId, retval)` | |
| `clock_gettime(clk_id, tp)` | `LOS_TickCountGet()` 或自定义实现 | |

## 测试集评估方法（挖空映射表）

> 来自 `Mini系统测试集设计.md` 的核心方法论：
>
> 以已适配芯片为基准，将 agent 需要生成的部分**挖空**，agent 填回后与 ground truth 对比。
>
> 三元组：**Input（输入）+ Template（挖空骨架）+ Ground Truth（正确答案）**

### 难度分级

| 难度 | 步骤 | 特征 |
|:----:|:-----|:-----|
| 入门 | 目录规划、config.json、ohos.build | 纯配置，无逻辑 |
| 简单 | config.gni、target_config.h、sys_param | 参数填充 |
| 中等 | Watchdog/LowPower/Reset/Flash/file HAL | 简单 API 包装（22-53行）|
| 中等偏难 | GPIO/UART/I2C/PWM | 枚举转换 + SDK 映射（55-113行）|
| 困难 | WiFi STA/AP | 大量状态管理 + 复杂 SDK API（438-993行）|
| 极难 | OTA/CMSIS-OS2/POSIX/token | 深度内核适配（210-1386行）|
