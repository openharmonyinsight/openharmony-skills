# L0/L1驱动代码模板

## L0轻量系统驱动骨架（IoT外设驱动子系统方式）

> ⚠️ L0不使用HDF框架、不使用OSAL、不使用HCS。直接实现LiteOS-M HAL接口。

```c
/*
 * Copyright (c) {{ year }} {{ vendor }}. All rights reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 */

/**
 * @file {{ filename }}
 * @brief {{ periph_type_upper }} driver for {{ chip_name }} (L0 LiteOS-M)
 * @since {{ version }}
 */

/* ======================== Includes ======================== */
#include "{{ header_file }}"
#include "los_gpio.h"      /* LiteOS-M GPIO HAL接口 */
/* #include "cmsis_gcc.h" */ /* CMSIS接口（可选） */

/* ======================== Register Defines ================ */
#define {{ PREFIX }}_BASE_ADDR     {{ regBase }}
#define {{ PREFIX }}_REG_CTRL      0x00
#define {{ PREFIX }}_REG_DATA      0x04
#define {{ PREFIX }}_REG_DIR       0x08
/* ... 其他寄存器偏移 ... */

/* ======================== Private Types =================== */
struct {{ ChipPrefix }}{{ PeriphType }}Device {
    volatile uint32_t *regBase;
    uint32_t pinCount;
    /* {{ periph_specific_fields }} */
};

static struct {{ ChipPrefix }}{{ PeriphType }}Device g_{{ chip_prefix }}{{ periph_type }}Dev;

/* ======================== HAL Interface Implementation ===== */
{% for method in methods %}
static int32_t {{ ChipPrefix }}{{ PeriphType }}{{ method.name }}({{ method.params }})
{
    /* TODO: Implement {{ method.name }} for {{ chip_name }} */
    volatile uint32_t *reg = g_{{ chip_prefix }}{{ periph_type }}Dev.regBase;
    /* 直接寄存器操作示例 */
    return 0;
}
{% endfor %}

/* ======================== Operations Table ================ */
static const struct {{ PeriphOpsType }} g_{{ chip_prefix }}{{ periph_type }}Ops = {
{% for method in methods %}
    .{{ method.field_name }} = {{ ChipPrefix }}{{ PeriphType }}{{ method.name }},
{% endfor %}
};

/* ======================== Driver Init ===================== */
int32_t {{ ChipPrefix }}{{ PeriphType }}DriverInit(void)
{
    g_{{ chip_prefix }}{{ periph_type }}Dev.regBase = 
        (volatile uint32_t *){{ PREFIX }}_BASE_ADDR;
    g_{{ chip_prefix }}{{ periph_type }}Dev.pinCount = {{ pin_count }};
    
    /* 注册到IoT外设驱动子系统 */
    {{ PeriphRegisterFunc }}(&g_{{ chip_prefix }}{{ periph_type }}Ops);
    
    return 0;
}
```

## L1小型系统驱动骨架（精简版HDF方式）

> 以下模板适用于L1小型系统，使用精简版HDF框架和OSAL接口。

```c
/*
 * Copyright (c) {{ year }} {{ vendor }}. All rights reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @file {{ filename }}
 * @brief {{ periph_type_upper }} driver for {{ chip_name }}
 * @since {{ version }}
 */

/* ======================== Includes ======================== */
#include "{{ header_file }}"
#include "hdf_device_desc.h"
#include "hdf_log.h"
#include "osal_mem.h"
#include "osal_mutex.h"
#include "osal_io.h"
#include "osal_irq.h"
#include "{{ periph_type }}_core.h"
#include "device_resource_if.h"

/* ======================== Defines ========================= */
#define {{ PREFIX }}_TAG  "{{ periph_tag }}"

/* ======================== Private Types =================== */
struct {{ ChipPrefix }}{{ PeriphType }}Device {
    struct {{ PeriphCntlrType }} cntlr;       // ★ 核心层控制器（首成员）
    volatile uint32_t *regBase;               // 寄存器基地址（IO映射后）
    uint32_t regSize;                         // 寄存器区域大小
    uint32_t irqNum;                          // 中断号
    OsalMutex mutex;                          // 互斥锁
    /* {{ periph_specific_fields }} */
};

/* ======================== Forward Declarations ============ */
static int32_t {{ ChipPrefix }}{{ PeriphType }}Bind(struct HdfDeviceObject *device);
static int32_t {{ ChipPrefix }}{{ PeriphType }}Init(struct HdfDeviceObject *device);
static void    {{ ChipPrefix }}{{ PeriphType }}Release(struct HdfDeviceObject *device);

/* ======================== Method Implementation ============ */
{% for method in methods %}
static int32_t {{ ChipPrefix }}{{ PeriphType }}{{ method.name }}({{ method.params }})
{
    /* TODO: Implement {{ method.name }} for {{ chip_name }} */
    HDF_LOGD("%s: {{ method.name }} called", {{ PREFIX }}_TAG);
    {% if method.has_default_return %}
    return {{ method.default_return }};
    {% endif %}
}
{% endfor %}

/* ======================== Method Table ===================== */
static struct {{ PeriphMethodType }} g_{{ chip_prefix }}{{ periph_type }}Method = {
{% for method in methods %}
    .{{ method.field_name }} = {{ ChipPrefix }}{{ PeriphType }}{{ method.name }},
{% endfor %}
};

/* ======================== Config Reader ==================== */
static bool {{ ChipPrefix }}{{ PeriphType }}ReadConfig(
    const struct DeviceResourceNode *node,
    struct {{ ChipPrefix }}{{ PeriphType }}Device *dev)
{
    struct DeviceResourceIface *iface = DeviceResourceGetIfaceInstance(HDF_CONFIG_SOURCE);
    if (iface == NULL || iface->GetUint32 == NULL) {
        HDF_LOGE("%s: get resource iface failed", {{ PREFIX }}_TAG);
        return false;
    }
    
    if (iface->GetUint32(node, "regBase", &dev->regBase, 0) != HDF_SUCCESS) {
        HDF_LOGE("%s: get regBase failed", {{ PREFIX }}_TAG);
        return false;
    }
    /* ... 读取其他配置字段 ... */
    return true;
}

/* ======================== Lifecycle Functions =============== */
static int32_t {{ ChipPrefix }}{{ PeriphType }}Bind(struct HdfDeviceObject *device)
{
    struct {{ PeriphCntlrType }} *cntlr = {{ PeriphCntlrFromDevice }}(device);
    if (cntlr == NULL) {
        HDF_LOGE("%s: cntlr is null", {{ PREFIX }}_TAG);
        return HDF_FAILURE;
    }
    cntlr->ops = &g_{{ chip_prefix }}{{ periph_type }}Method;
    return HDF_SUCCESS;
}

static int32_t {{ ChipPrefix }}{{ PeriphType }}Init(struct HdfDeviceObject *device)
{
    struct {{ ChipPrefix }}{{ PeriphType }}Device *dev = NULL;
    
    dev = (struct {{ ChipPrefix }}{{ PeriphType }}Device *)OsalMemCalloc(
        sizeof(struct {{ ChipPrefix }}{{ PeriphType }}Device));
    if (dev == NULL) {
        HDF_LOGE("%s: malloc failed", {{ PREFIX }}_TAG);
        return HDF_ERR_MALLOC_FAIL;
    }
    
    // 读取HCS配置
    if (!{{ ChipPrefix }}{{ PeriphType }}ReadConfig(device->property, dev)) {
        OsalMemFree(dev);
        return HDF_FAILURE;
    }
    
    // IO映射
    dev->regBase = (volatile uint32_t *)OsalIoRemap(dev->regBase, dev->regSize);
    if (dev->regBase == NULL) {
        HDF_LOGE("%s: ioremap failed", {{ PREFIX }}_TAG);
        OsalMemFree(dev);
        return HDF_ERR_IO;
    }
    
    // 互斥锁初始化
    if (OsalMutexInit(&dev->mutex) != HDF_SUCCESS) {
        OsalIoUnmap((void *)dev->regBase);
        OsalMemFree(dev);
        return HDF_FAILURE;
    }
    
    // 注册到核心层
    dev->cntlr.ops = &g_{{ chip_prefix }}{{ periph_type }}Method;
    int32_t ret = {{ PeriphCntlrAdd }}(&dev->cntlr, {{ instance_id }});
    if (ret != HDF_SUCCESS) {
        HDF_LOGE("%s: add cntlr failed, ret=%d", {{ PREFIX }}_TAG, ret);
        OsalMutexDestroy(&dev->mutex);
        OsalIoUnmap((void *)dev->regBase);
        OsalMemFree(dev);
        return ret;
    }
    
    HDF_LOGI("%s: init success, id=%d", {{ PREFIX }}_TAG, {{ instance_id }});
    return HDF_SUCCESS;
}

static void {{ ChipPrefix }}{{ PeriphType }}Release(struct HdfDeviceObject *device)
{
    struct {{ ChipPrefix }}{{ PeriphType }}Device *dev = 
        {{ GetDeviceFromObject }}(device);
    if (dev == NULL) {
        return;
    }
    
    {{ PeriphCntlrRemove }}(&dev->cntlr);
    OsalMutexDestroy(&dev->mutex);
    if (dev->regBase != NULL) {
        OsalIoUnmap((void *)dev->regBase);
    }
    OsalMemFree(dev);
    HDF_LOGI("%s: release done", {{ PREFIX }}_TAG);
}

/* ======================== Driver Entry ===================== */
struct HdfDriverEntry g_{{ chip_prefix }}{{ periph_type }}DriverEntry = {
    .moduleVersion = 1,
    .moduleName = {{ module_name }},
    .Bind = {{ ChipPrefix }}{{ PeriphType }}Bind,
    .Init = {{ ChipPrefix }}{{ PeriphType }}Init,
    .Release = {{ ChipPrefix }}{{ PeriphType }}Release,
};
HDF_INIT(g_{{ chip_prefix }}{{ periph_type }}DriverEntry);
```

## 完整代码示例：L0 Hi3861 GPIO驱动

### gpio_hi3861.h

```c
/*
 * Copyright (c) 2024 HiSilicon Technologies Co., Ltd. All rights reserved.
 * Licensed under the Apache License, Version 2.0
 */

#ifndef GPIO_HI3861_H
#define GPIO_HI3861_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Hi3861 GPIO寄存器定义 */
#define HI3861_GPIO_BASE_ADDR       0x40007000U
#define HI3861_GPIO_DATA_REG        0x00    /* Data Register */
#define HI3861_GPIO_DIR_REG         0x04    /* Direction Register */
#define HI3861_GPIO_IS_REG          0x08    /* Interrupt Sense */
#define HI3861_GPIO_IBE_REG         0x0C    /* Interrupt Both Edges */
#define HI3861_GPIO_IEV_REG         0x10    /* Interrupt Event */
#define HI3861_GPIO_IE_REG          0x14    /* Interrupt Enable */
#define HI3861_GPIO_RIS_REG         0x18    /* Raw Interrupt Status */
#define HI3861_GPIO_MIS_REG         0x1C    /* Masked Interrupt Status */
#define HI3861_GPIO_IC_REG          0x20    /* Interrupt Clear */
#define HI3861_GPIO_AFSEL_REG       0x24    /* Alternate Function Select */

#define HI3861_GPIO_PIN_COUNT       14
#define HI3861_GPIO_IRQ_NUM         30

/* GPIO方向定义 */
#define GPIO_DIR_IN                 0
#define GPIO_DIR_OUT                1

/* GPIO值定义 */
#define GPIO_VAL_LOW                0
#define GPIO_VAL_HIGH               1

/* HAL操作函数表 */
struct GpioOperations {
    int32_t (*setDir)(uint16_t gpio, uint16_t dir);
    int32_t (*getDir)(uint16_t gpio, uint16_t *dir);
    int32_t (*write)(uint16_t gpio, uint16_t val);
    int32_t (*read)(uint16_t gpio, uint16_t *val);
    int32_t (*setIrq)(uint16_t gpio, uint16_t mode);
    int32_t (*unsetIrq)(uint16_t gpio);
};

/* 驱动初始化入口 */
int32_t Hi3861GpioDriverInit(void);

#ifdef __cplusplus
}
#endif

#endif /* GPIO_HI3861_H */
```

### gpio_hi3861.c

```c
/*
 * Copyright (c) 2024 HiSilicon Technologies Co., Ltd. All rights reserved.
 * Licensed under the Apache License, Version 2.0
 */

#include "gpio_hi3861.h"
#include "los_gpio.h"

#define GPIO_TAG "hi3861_gpio"

/* ========== 设备实例 ========== */
static struct {
    volatile uint32_t *regBase;
    uint16_t pinCount;
} g_hi3861GpioDev;

/* ========== 辅助函数 ========== */
static inline bool IsValidPin(uint16_t gpio)
{
    return (gpio < g_hi3861GpioDev.pinCount);
}

/* ========== HAL接口实现 ========== */
static int32_t Hi3861GpioSetDir(uint16_t gpio, uint16_t dir)
{
    if (!IsValidPin(gpio)) {
        return -1;
    }
    
    volatile uint32_t *dirReg = g_hi3861GpioDev.regBase + HI3861_GPIO_DIR_REG;
    uint32_t val = *dirReg;
    if (dir == GPIO_DIR_OUT) {
        val |= (1U << gpio);
    } else {
        val &= ~(1U << gpio);
    }
    *dirReg = val;
    
    return 0;
}

static int32_t Hi3861GpioGetDir(uint16_t gpio, uint16_t *dir)
{
    if (!IsValidPin(gpio) || dir == NULL) {
        return -1;
    }
    
    uint32_t val = *(g_hi3861GpioDev.regBase + HI3861_GPIO_DIR_REG);
    *dir = (val & (1U << gpio)) ? GPIO_DIR_OUT : GPIO_DIR_IN;
    return 0;
}

static int32_t Hi3861GpioWrite(uint16_t gpio, uint16_t val)
{
    if (!IsValidPin(gpio)) {
        return -1;
    }
    
    volatile uint32_t *dataReg = g_hi3861GpioDev.regBase + HI3861_GPIO_DATA_REG;
    uint32_t reg = *dataReg;
    if (val == GPIO_VAL_HIGH) {
        reg |= (1U << gpio);
    } else {
        reg &= ~(1U << gpio);
    }
    *dataReg = reg;
    
    return 0;
}

static int32_t Hi3861GpioRead(uint16_t gpio, uint16_t *val)
{
    if (!IsValidPin(gpio) || val == NULL) {
        return -1;
    }
    
    uint32_t reg = *(g_hi3861GpioDev.regBase + HI3861_GPIO_DATA_REG);
    *val = (reg & (1U << gpio)) ? GPIO_VAL_HIGH : GPIO_VAL_LOW;
    return 0;
}

static int32_t Hi3861GpioSetIrq(uint16_t gpio, uint16_t mode)
{
    if (!IsValidPin(gpio)) {
        return -1;
    }
    /* TODO: 配置中断触发方式 */
    return 0;
}

static int32_t Hi3861GpioUnsetIrq(uint16_t gpio)
{
    if (!IsValidPin(gpio)) {
        return -1;
    }
    volatile uint32_t *ieReg = g_hi3861GpioDev.regBase + HI3861_GPIO_IE_REG;
    *ieReg &= ~(1U << gpio);
    return 0;
}

/* ========== 操作函数表 ========== */
static const struct GpioOperations g_hi3861GpioOps = {
    .setDir   = Hi3861GpioSetDir,
    .getDir   = Hi3861GpioGetDir,
    .write    = Hi3861GpioWrite,
    .read     = Hi3861GpioRead,
    .setIrq   = Hi3861GpioSetIrq,
    .unsetIrq = Hi3861GpioUnsetIrq,
};

/* ========== 驱动初始化（组件注册方式） ========== */
int32_t Hi3861GpioDriverInit(void)
{
    g_hi3861GpioDev.regBase = (volatile uint32_t *)HI3861_GPIO_BASE_ADDR;
    g_hi3861GpioDev.pinCount = HI3861_GPIO_PIN_COUNT;
    
    /* 以组件方式注册到IoT外设驱动子系统 */
    GpioRegisterOps(&g_hi3861GpioOps);
    
    return 0;
}
```

## 完整代码示例：L1 Hi3516 GPIO驱动（精简版HDF）

### gpio_hi3516.h

```c
/*
 * Copyright (c) 2024 HiSilicon Technologies Co., Ltd. All rights reserved.
 * Licensed under the Apache License, Version 2.0
 */

#ifndef GPIO_HI3516_H
#define GPIO_HI3516_H

#include "gpio_core.h"
#include "osal_mutex.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Hi3516DV300 GPIO寄存器偏移定义 */
#define HI3516_GPIO_SWPORT_DR       0x0000  /* Data Register */
#define HI3516_GPIO_SWPORT_DDR      0x0004  /* Data Direction Register */
#define HI3516_GPIO_INTEN           0x0030  /* Interrupt Enable */
#define HI3516_GPIO_INT_STATUS      0x0040  /* Interrupt Status */
#define HI3516_GPIO_EXT_PORT        0x0050  /* External Port */

#define HI3516_GPIO_GROUP_COUNT     12
#define HI3516_GPIO_PINS_PER_GROUP  8

struct Hi3516GpioDevice {
    struct GpioCntlr cntlr;             /* ★ 核心层控制器（首成员） */
    volatile uint32_t *regBase;         /* 寄存器基地址 */
    uint32_t regSize;                   /* 寄存器区域大小 */
    uint32_t irqNum;                    /* 中断号 */
    OsalMutex mutex;                    /* 互斥锁 */
};

#ifdef __cplusplus
}
#endif

#endif /* GPIO_HI3516_H */
```

### gpio_hi3516.c（L1精简版HDF）

```c
/*
 * Copyright (c) 2024 HiSilicon Technologies Co., Ltd. All rights reserved.
 * Licensed under the Apache License, Version 2.0
 */

#include "gpio_hi3516.h"
#include "hdf_device_desc.h"
#include "hdf_log.h"
#include "osal_mem.h"
#include "osal_mutex.h"
#include "osal_io.h"
#include "osal_irq.h"
#include "device_resource_if.h"

#define HDF_LOG_TAG gpio_hi3516

/* ========== 辅助函数 ========== */
static inline struct Hi3516GpioDevice *GetGpioDevice(struct GpioCntlr *cntlr)
{
    return (struct Hi3516GpioDevice *)cntlr;
}

/* ========== GpioMethod 实现 ========== */
static int32_t Hi3516GpioSetDir(struct GpioCntlr *cntlr, uint16_t gpio, uint16_t dir)
{
    struct Hi3516GpioDevice *dev = GetGpioDevice(cntlr);
    
    OsalMutexTimedLock(&dev->mutex, HDF_WAIT_FOREVER);
    uint32_t val = OsalIoRead32(dev->regBase + HI3516_GPIO_SWPORT_DDR);
    if (dir == GPIO_DIR_OUT) {
        val |= (1U << gpio);
    } else {
        val &= ~(1U << gpio);
    }
    OsalIoWrite32(dev->regBase + HI3516_GPIO_SWPORT_DDR, val);
    OsalMutexUnlock(&dev->mutex);
    
    return HDF_SUCCESS;
}

static int32_t Hi3516GpioWrite(struct GpioCntlr *cntlr, uint16_t gpio, uint16_t val)
{
    struct Hi3516GpioDevice *dev = GetGpioDevice(cntlr);
    
    OsalMutexTimedLock(&dev->mutex, HDF_WAIT_FOREVER);
    uint32_t reg = OsalIoRead32(dev->regBase + HI3516_GPIO_SWPORT_DR);
    if (val == GPIO_VAL_HIGH) {
        reg |= (1U << gpio);
    } else {
        reg &= ~(1U << gpio);
    }
    OsalIoWrite32(dev->regBase + HI3516_GPIO_SWPORT_DR, reg);
    OsalMutexUnlock(&dev->mutex);
    
    return HDF_SUCCESS;
}

static int32_t Hi3516GpioRead(struct GpioCntlr *cntlr, uint16_t gpio, uint16_t *val)
{
    struct Hi3516GpioDevice *dev = GetGpioDevice(cntlr);
    if (val == NULL) {
        return HDF_ERR_INVALID_PARAM;
    }
    
    uint32_t reg = OsalIoRead32(dev->regBase + HI3516_GPIO_EXT_PORT);
    *val = (reg & (1U << gpio)) ? GPIO_VAL_HIGH : GPIO_VAL_LOW;
    return HDF_SUCCESS;
}

/* ========== Method 表 ========== */
static struct GpioMethod g_hi3516GpioMethod = {
    .Request = NULL,
    .Release = NULL,
    .SetDir = Hi3516GpioSetDir,
    .GetDir = NULL, /* TODO */
    .Write = Hi3516GpioWrite,
    .Read = Hi3516GpioRead,
    .SetIrq = NULL, /* TODO */
    .UnsetIrq = NULL,
    .EnableIrq = NULL,
    .DisableIrq = NULL,
};

/* ========== HCS配置读取 ========== */
static bool Hi3516GpioReadConfig(const struct DeviceResourceNode *node,
                                  struct Hi3516GpioDevice *dev)
{
    struct DeviceResourceIface *iface = DeviceResourceGetIfaceInstance(HDF_CONFIG_SOURCE);
    if (iface == NULL || iface->GetUint32 == NULL) {
        HDF_LOGE("%s: get resource iface failed", __func__);
        return false;
    }
    
    uint32_t regBase = 0;
    if (iface->GetUint32(node, "regBase", &regBase, 0) != HDF_SUCCESS) {
        HDF_LOGE("%s: get regBase failed", __func__);
        return false;
    }
    dev->regBase = (volatile uint32_t *)(uintptr_t)regBase;
    return true;
}

/* ========== 生命周期函数 ========== */
static int32_t Hi3516GpioBind(struct HdfDeviceObject *device)
{
    struct GpioCntlr *cntlr = GpioCntlrFromDevice(device);
    if (cntlr == NULL) {
        HDF_LOGE("%s: cntlr is null", __func__);
        return HDF_FAILURE;
    }
    cntlr->ops = &g_hi3516GpioMethod;
    return HDF_SUCCESS;
}

static int32_t Hi3516GpioInit(struct HdfDeviceObject *device)
{
    struct Hi3516GpioDevice *dev = NULL;
    
    dev = (struct Hi3516GpioDevice *)OsalMemCalloc(sizeof(struct Hi3516GpioDevice));
    if (dev == NULL) {
        HDF_LOGE("%s: malloc failed", __func__);
        return HDF_ERR_MALLOC_FAIL;
    }
    
    if (!Hi3516GpioReadConfig(device->property, dev)) {
        OsalMemFree(dev);
        return HDF_FAILURE;
    }
    
    if (OsalMutexInit(&dev->mutex) != HDF_SUCCESS) {
        OsalMemFree(dev);
        return HDF_FAILURE;
    }
    
    dev->cntlr.ops = &g_hi3516GpioMethod;
    int32_t ret = GpioCntlrAdd(&dev->cntlr, dev->cntlr.start);
    if (ret != HDF_SUCCESS) {
        OsalMutexDestroy(&dev->mutex);
        OsalMemFree(dev);
        return ret;
    }
    
    HDF_LOGI("%s: init success", __func__);
    return HDF_SUCCESS;
}

static void Hi3516GpioRelease(struct HdfDeviceObject *device)
{
    struct GpioCntlr *cntlr = GpioCntlrFromDevice(device);
    if (cntlr == NULL) { return; }
    
    struct Hi3516GpioDevice *dev = GetGpioDevice(cntlr);
    GpioCntlrRemove(cntlr);
    OsalMutexDestroy(&dev->mutex);
    OsalMemFree(dev);
}

/* ========== 驱动入口（L1精简版HDF） ========== */
struct HdfDriverEntry g_hi3516GpioDriverEntry = {
    .moduleVersion = 1,
    .moduleName = "HDF_PLATFORM_GPIO",
    .Bind = Hi3516GpioBind,
    .Init = Hi3516GpioInit,
    .Release = Hi3516GpioRelease,
};
HDF_INIT(g_hi3516GpioDriverEntry);
```

## UART驱动核心代码片段

```c
/* uart_rk3568.c - 核心Method实现 */

static struct UartHostMethod g_rk3568UartMethod = {
    .Init = Rk3568UartInit,
    .Deinit = Rk3568UartDeinit,
    .Read = Rk3568UartRead,
    .Write = Rk3568UartWrite,
    .GetBaud = Rk3568UartGetBaud,
    .SetBaud = Rk3568UartSetBaud,
    .GetAttribute = Rk3568UartGetAttribute,
    .SetAttribute = Rk3568UartSetAttribute,
    .SetTransMode = Rk3568UartSetTransMode,
};

static int32_t Rk3568UartSetBaud(struct UartHost *host, uint32_t baudRate)
{
    struct Rk3568UartDevice *dev = UartHostToDevice(host);
    if (dev == NULL) {
        return HDF_ERR_INVALID_PARAM;
    }
    
    OsalMutexTimedLock(&dev->mutex, HDF_WAIT_FOREVER);
    /* RK3568 UART波特率计算: DLL = SCLK / (16 * baudRate) */
    uint32_t clk = dev->clkFreq;
    uint32_t divisor = clk / (16 * baudRate);
    
    /* 使能DLAB位以访问分频寄存器 */
    uint32_t lcr = OsalIoRead32(dev->regBase + UART_LCR);
    OsalIoWrite32(dev->regBase + UART_LCR, lcr | UART_LCR_DLAB);
    
    OsalIoWrite32(dev->regBase + UART_DLL, divisor & 0xFF);
    OsalIoWrite32(dev->regBase + UART_DLH, (divisor >> 8) & 0xFF);
    
    /* 恢复LCR */
    OsalIoWrite32(dev->regBase + UART_LCR, lcr);
    
    dev->baudRate = baudRate;
    OsalMutexUnlock(&dev->mutex);
    
    HDF_LOGI("%s: set baud rate to %u", __func__, baudRate);
    return HDF_SUCCESS;
}
```

## 不同Lite系统芯片GPIO驱动对比

| 特性 | Hi3861 (L0) | STM32F407 (L0) | BES2600W (L0) | ESP32-C3 (L0) | Hi3516DV300 (L1) |
|------|-------------|----------------|---------------|---------------|-------------------|
| 系统类型 | L0轻量系统 | L0轻量系统 | L0轻量系统 | L0轻量系统 | L1小型系统 |
| 内核 | LiteOS-M | LiteOS-M | LiteOS-M | LiteOS-M | LiteOS-A |
| 驱动方式 | IoT子系统 | IoT子系统+CMSIS | IoT子系统 | IoT子系统 | 精简版HDF |
| CPU架构 | RISC-V | Cortex-M4F | Cortex-M33 | RISC-V | Cortex-A7 |
| GPIO组数 | 1组(14pin) | 9组(16pin/组) | 多组 | 2组(48/46pin) | 12组(8pin/组) |
| 寄存器布局 | 统一基址 | 分组独立基址 | 分组独立基址 | 统一基址 | 分组独立基址 |
| 中断模型 | PLIC | NVIC | NVIC | PLIC | GIC |
| OSAL使用 | ❌ 不使用 | ❌ 不使用 | ❌ 不使用 | ❌ 不使用 | ✅ 使用 |
| HCS配置 | ❌ 不使用 | ❌ 不使用 | ❌ 不使用 | ❌ 不使用 | ✅ 精简版 |
| BUILD.gn | lite_component | lite_component | lite_component | lite_component | hdf_driver |
| 关键适配点 | PLIC中断映射 | CMSIS兼容、NVIC | TrustZone安全区 | IDF SDK对接 | HDF核心层注册 |
