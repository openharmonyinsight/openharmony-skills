# HDF/IoT驱动框架详解

> 来源：需求分析报告 §1

## L0与L1架构对比

> ⚠️ **关键区别**：L0轻量系统和L1小型系统的HAL实现方式完全不同：
> - **L0轻量系统**：使用 **IoT外设驱动子系统**（非HDF），通过LiteOS-M HAL接口 + CMSIS/POSIX API暴露能力
> - **L1小型系统**：使用 **精简版HDF框架**，通过HDI直通模式暴露能力

```
┌─────────────────────────────────────────────────────────────┐
│              L0 轻量系统架构 (LiteOS-M)                       │
├─────────────────────────────────────────────────────────────┤
│                  应用层 (Application)                         │
├─────────────────────────────────────────────────────────────┤
│            CMSIS / POSIX 接口层                               │
├─────────────────────────────────────────────────────────────┤
│         ★ IoT外设驱动子系统 ★（非HDF）                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                    │
│  │GPIO驱动   │ │UART驱动   │ │I2C/SPI   │ ← 组件化注册       │
│  │(寄存器操作)│ │(寄存器操作)│ │PWM/ADC   │ ← LiteOS-M HAL    │
│  └──────────┘ └──────────┘ └──────────┘                    │
├─────────────────────────────────────────────────────────────┤
│             LiteOS-M 内核 (RTOS)                              │
├─────────────────────────────────────────────────────────────┤
│                   硬件层 (MCU SoC / Board)                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              L1 小型系统架构 (LiteOS-A/Linux)                  │
├─────────────────────────────────────────────────────────────┤
│                  应用框架层                                    │
├─────────────────────────────────────────────────────────────┤
│         ★ HDI (Hardware Device Interface) ★ 直通模式          │
├─────────────────────────────────────────────────────────────┤
│           精简版 HDF 驱动框架                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                    │
│  │平台驱动   │ │ 器件驱动  │ │ HdfDriver│ ← HdfDriverEntry  │
│  │(GPIO/I2C │ │(LCD/TP/  │ │ Entry    │ ← 精简版HCS配置    │
│  │/SPI/UART)│ │ Sensor)  │ │ Bind/Init│                    │
│  └──────────┘ └──────────┘ └──────────┘                    │
├─────────────────────────────────────────────────────────────┤
│      OSAL (OS Abstraction Layer)                             │
├─────────────────────────────────────────────────────────────┤
│             LiteOS-A 内核                                     │
├─────────────────────────────────────────────────────────────┤
│                   硬件层 (MPU SoC / Board)                     │
└─────────────────────────────────────────────────────────────┘
```

## HAL层的三大作用

| 作用 | 说明 |
|------|------|
| **硬件解耦** | 将上层系统服务与具体芯片/板卡硬件分离，更换芯片只需替换HAL层实现 |
| **接口标准化** | 定义统一的外设操作接口（读/写/配置/中断等），保证跨平台一致性 |
| **跨设备部署** | 同一套系统服务可运行在不同硬件平台上，支持从百K级到G级的弹性部署 |

## L0轻量系统：IoT外设驱动子系统（非HDF）

L0轻量系统**不使用HDF框架**，因为MCU资源受限（最小128KB内存），无法承载HDF的运行时开销。L0驱动开发方式为：

1. **直接实现LiteOS-M HAL接口**：操作寄存器或使用厂商SDK的HAL库
2. **组件化注册**：通过函数调用将驱动注册到系统
3. **CMSIS/POSIX API暴露**：向上层提供标准化接口
4. **无需OSAL**：直接使用LiteOS-M内核API和CMSIS接口

```c
/* L0 GPIO驱动示例 — IoT外设驱动子系统方式 */
#include "gpio_if.h"
#include "los_gpio.h"

/* 实现LiteOS-M HAL接口 */
static int32_t Hi3861GpioSetDir(uint16_t gpio, uint16_t dir)
{
    /* 直接操作寄存器 */
    volatile uint32_t *gpio_base = (volatile uint32_t *)GPIO_BASE_ADDR;
    if (dir == GPIO_DIR_OUT) {
        gpio_base[GPIO_DIR_REG] |= (1U << gpio);
    } else {
        gpio_base[GPIO_DIR_REG] &= ~(1U << gpio);
    }
    return 0;
}

/* 以组件方式注册 */
void GpioDriverRegister(void)
{
    static const struct GpioOperations ops = {
        .setDir = Hi3861GpioSetDir,
        .write  = Hi3861GpioWrite,
        .read   = Hi3861GpioRead,
        /* ... */
    };
    GpioRegisterOps(&ops);
}
```

## L1小型系统：精简版HDF框架

L1小型系统可使用**精简版HDF框架**，保留了HdfDriverEntry/Bind/Init/Release生命周期，但相比标准系统有以下简化：

- HCS配置更简洁
- 不支持完整的设备管理器
- HDI仅支持直通模式（不支持IPC模式）
- OSAL接口完整可用

### HdfDriverEntry — 驱动入口（仅L1适用）

> ⚠️ 以下内容仅适用于 **L1小型系统**。L0轻量系统不使用此机制。

每个L1 HDF驱动都必须定义一个 `struct HdfDriverEntry` 结构体作为驱动入口，并通过 `HDF_INIT()` 宏注册到框架中：

```c
#include "hdf_device_desc.h"

// 驱动入口结构体
struct HdfDriverEntry g_sampleDriverEntry = {
    .moduleVersion = 1,                    // 驱动模块版本号
    .moduleName = "SAMPLE_DRIVER",         // 驱动模块名称（必须与HCS中moduleName一致）
    .Bind = SampleDriverBind,              // 绑定函数指针
    .Init = SampleDriverInit,              // 初始化函数指针
    .Release = SampleDriverRelease,        // 释放函数指针
};

// 将驱动入口注册到HDF框架
HDF_INIT(g_sampleDriverEntry);
```

### Bind / Init / Release — 三大生命周期函数

| 函数 | 调用时机 | 职责 | 注意事项 |
|------|---------|------|---------|
| **Bind** | 驱动加载时最先调用 | 实例化驱动服务对象，将 `IDeviceIoService` 与 `DeviceObject` 绑定；如需对外发布服务接口，在此完成 | 只做接口绑定，不做硬件初始化 |
| **Init** | Bind成功后调用 | 执行硬件初始化、资源申请、读取HCS配置等实际初始化逻辑 | 若Init失败，框架会自动调用Release |
| **Release** | Init失败或驱动卸载时调用 | 释放所有已分配的资源（内存、中断、IO映射等） | 必须保证幂等性，多次调用不崩溃 |

```c
// ===== Bind 示例 =====
static int32_t SampleDriverBind(struct HdfDeviceObject *device)
{
    if (device == NULL) {
        HDF_LOGE("%s: device is null", __func__);
        return HDF_ERR_INVALID_PARAM;
    }
    
    // 创建并绑定设备服务接口
    struct IDeviceIoService *service = &g_sampleService.ioService;
    service->Dispatch = SampleDriverDispatch;  // 设置消息分发函数
    
    int32_t ret = HdfDeviceRegisterEvent(device, service);
    if (ret != HDF_SUCCESS) {
        HDF_LOGE("%s: register event failed, ret=%d", __func__, ret);
        return ret;
    }
    
    HDF_LOGI("%s: bind success", __func__);
    return HDF_SUCCESS;
}

// ===== Init 示例 =====
static int32_t SampleDriverInit(struct HdfDeviceObject *device)
{
    if (device == NULL) {
        return HDF_ERR_INVALID_PARAM;
    }
    
    // 1. 读取HCS配置
    const struct DeviceResourceNode *node = device->property;
    struct SampleConfig config;
    if (!SampleReadConfig(node, &config)) {
        HDF_LOGE("%s: read config failed", __func__);
        return HDF_FAILURE;
    }
    
    // 2. 硬件寄存器映射
    g_sampleBase = OsalIoRemap(config.regBase, config.regSize);
    if (g_sampleBase == NULL) {
        HDF_LOGE("%s: ioremap failed", __func__);
        return HDF_ERR_IO;
    }
    
    // 3. 中断注册
    if (config.irqNum > 0) {
        int32_t ret = OsalRegisterIrq(config.irqNum, 0, SampleIrqHandler, 
                                       "sample_irq", NULL);
        if (ret != HDF_SUCCESS) {
            HDF_LOGE("%s: register irq failed", __func__);
            OsalIoUnmap(g_sampleBase);
            g_sampleBase = NULL;
            return ret;
        }
    }
    
    HDF_LOGI("%s: init success", __func__);
    return HDF_SUCCESS;
}

// ===== Release 示例 =====
static void SampleDriverRelease(struct HdfDeviceObject *device)
{
    (void)device;
    
    // 释放中断
    if (g_config.irqNum > 0) {
        OsalUnregisterIrq(g_config.irqNum, NULL);
    }
    
    // 解除IO映射
    if (g_sampleBase != NULL) {
        OsalIoUnmap(g_sampleBase);
        g_sampleBase = NULL;
    }
    
    HDF_LOGI("%s: release done", __func__);
}
```

### IDeviceIoService — 设备IO服务接口

`IDeviceIoService` 是HDF驱动对外提供服务的基础接口，采用C语言面向对象编程模式。**驱动服务结构体的第一个成员必须是 `IDeviceIoService`**：

```c
// 驱动服务结构体定义（首成员必须是 IDeviceIoService）
struct SampleDriverService {
    struct IDeviceIoService ioService;   // ★ 必须放在第一个成员
    // 以下为自定义的成员
    struct SampleConfig config;
    volatile uint32_t *regBase;
    OsalMutex mutex;
};

// Dispatch 消息分发函数 —— 处理用户态/其他驱动的调用请求
static int32_t SampleDriverDispatch(struct HdfDeviceIoClient *client, 
                                     int32_t cmdId,
                                     struct HdfSBuf *data, 
                                     struct HdfSBuf *reply)
{
    if (client == NULL || client->device == NULL) {
        return HDF_ERR_INVALID_PARAM;
    }
    
    switch (cmdId) {
        case SAMPLE_CMD_READ:
            return SampleHandleRead(client, data, reply);
        case SAMPLE_CMD_WRITE:
            return SampleHandleWrite(client, data, reply);
        case SAMPLE_CMD_GET_CONFIG:
            return SampleHandleGetConfig(client, data, reply);
        default:
            HDF_LOGW("%s: unknown cmd %d", __func__, cmdId);
            return HDF_ERR_NOT_SUPPORT;
    }
}
```

## HDI（Hardware Device Interface）与HAL的关系

**HDI 是 OpenHarmony 对传统 HAL 概念的标准化实现**。两者关系如下：

| 维度 | 传统HAL | OpenHarmony HDI |
|------|---------|-----------------|
| 接口定义方式 | 头文件 + 函数指针 | **IDL（Interface Description Language）** 描述 |
| 代码生成 | 手工编写 | IDL编译器自动生成Stub/Proxy代码 |
| 通信机制 | 直接函数调用 | **IPC（进程间通信）** 模式，支持跨进程 |
| 跨平台能力 | 依赖手动适配 | 框架级支持，驱动与平台/内核解耦 |
| 版本管理 | 无标准 | IDL自带版本控制 |

HDI使用IDL定义接口示例：

```idl
// IGpioInterface.idl
package ohos.hdi.gpio.v1_0;

interface IGpioInterface {
    SetDir([in] unsigned short gpio, [in] enum GpioDir dir);
    GetDir([in] unsigned short gpio, [out] enum GpioDir dir);
    Write([in] unsigned short gpio, [in] enum GpioValue val);
    Read([in] unsigned short gpio, [out] enum GpioValue val);
    SetIrq([in] unsigned short gpio, [in] enum GpioIrqType type,
           [in] object callback);
    UnsetIrq([in] unsigned short gpio);
    EnableIrq([in] unsigned short gpio);
    DisableIrq([in] unsigned short gpio);
}
```

HDI分为两种工作模式：
- **IPC模式**：系统服务和驱动运行在不同进程，通过Binder IPC通信（标准系统）
- **直通模式**：系统服务和驱动在同一进程，直接函数调用（小型/轻量系统）

## OSAL（OS Abstraction Layer）

> ⚠️ **关键区别**：
> - **L0轻量系统不使用OSAL**：直接使用LiteOS-M内核API + CMSIS接口
> - **L1小型系统使用OSAL**：通过OSAL屏蔽LiteOS-A与其他内核的差异

### OSAL提供的统一接口清单

| 类别 | 主要接口 | 说明 |
|------|---------|------|
| **内存管理** | `OsalMemAlloc()`, `OsalMemCalloc()`, `OsalMemRealloc()`, `OsalMemFree()` | 统一内存分配/释放 |
| **互斥锁** | `OsalMutexInit()`, `OsalMutexTimedLock()`, `OsalMutexUnlock()`, `OsalMutexDestroy()` | 互斥同步原语 |
| **自旋锁** | `OsalSpinInit()`, `OsalSpinLock()`, `OsalSpinUnlock()`, `OsalSpinDestroy()` | 中断上下文同步 |
| **信号量** | `OsalSemInit()`, `OsalSemWait()`, `OsalSemPost()`, `OsalSemDestroy()` | 计数信号量 |
| **线程** | `OsalThreadCreate()`, `OsalThreadStart()`, `OsalThreadJoin()`, `OsalThreadSleep()` | 线程管理 |
| **定时器** | `OsalTimerCreate()`, `OsalTimerStart()`, `OsalTimerStop()`, `OsalTimerDelete()` | 软件定时器 |
| **IO映射** | `OsalIoRemap()`, `OsalIoUnmap()`, `OsalIoRead8/16/32()`, `OsalIoWrite8/16/32()` | 寄存器访问 |
| **中断管理** | `OsalRegisterIrq()`, `OsalUnregisterIrq()` | 中断注册/注销 |
| **时间** | `OsalGetTime()`, `OsalGetSysTimeMs()`, `OsalUDelay()`, `OsalMDelay()` | 时间和延时 |
| **日志** | `HDF_LOGD/I/W/E/F()` | 分级日志宏 |
| **原子操作** | `OsalAtomicInc()`, `OsalAtomicDec()`, `OsalAtomicRead()`, `OsalAtomicSet()` | 原子变量 |

> **重要原则**：HDF驱动中**禁止直接使用内核原生API**（如Linux的`kmalloc`/`mutex_lock`或LiteOS的`LOS_MemAlloc`），必须使用OSAL封装接口，以保证跨平台兼容性。

## 当前驱动开发的痛点

| 痛点 | 详细描述 | 影响 | 适用系统 |
|------|---------|------|---------|
| **L0驱动模板缺失** | L0轻量系统没有统一的驱动框架，各厂商实现方式各异，缺乏标准化模板 | 每个L0芯片的驱动结构完全不同，难以复用 | L0 |
| **CMSIS接口适配繁琐** | 需要将厂商SDK的HAL接口转换为CMSIS/POSIX标准接口 | 手动编写转换层耗时且易出错 | L0 |
| **重复劳动严重(L1)** | 每种外设的HDF驱动骨架高度相似，但每个芯片平台都要手写一遍 | 适配一个新芯片需重复编写数千行样板代码 | L1 |
| **易出错(L1)** | HCS配置的字段名、serviceName、deviceMatchAttr必须严格匹配 | 新手调试HCS配置问题平均耗时2-3天 | L1 |
| **学习成本高** | HDF框架涉及HCS语法、OSAL/PAL接口等多个新概念 | 有经验的Linux驱动开发者也需要1-2周才能上手 | L0/L1 |
| **多系统适配复杂** | 同一驱动需同时支持L0(IoT子系统)和L1(精简HDF)，API差异大 | 维护成本倍增 | L0/L1 |
| **BUILD.gn格式混淆** | L0使用build_lite格式，L1也使用build_lite但与标准系统不同 | 编译配置频繁出错 | L0/L1 |
| **文档分散** | Lite系统驱动开发信息比标准系统更分散 | 开发者反复搜索和验证信息 | L0/L1 |
