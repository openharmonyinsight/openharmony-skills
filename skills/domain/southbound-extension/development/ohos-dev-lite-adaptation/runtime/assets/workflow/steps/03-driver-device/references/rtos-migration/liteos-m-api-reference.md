# HDF框架与OSAL/LiteOS-M接口文档

---

## 1. L0轻量系统：IoT外设驱动子系统（非HDF）

### 1.1 核心概念

L0轻量系统**不使用完整HDF框架**，而是采用**IoT外设驱动子系统**方式组织驱动。这是因为MCU级设备资源有限（128KB~256KB RAM），无法承载完整HDF的开销。

```
┌──────────────────────────────────────────────────────────┐
│              L0 IoT外设驱动模型                            │
│                                                          │
│  ┌─────────────────────────────────────────────────────┐ │
│  │            应用层 / 业务逻辑                          │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │     CMSIS-RTOS2 / POSIX 接口 (可选)                  │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │     LiteOS-M 内核API (LOS_TaskCreate等)              │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │     IoT外设HAL接口 (GPIO/UART/I2C/SPI/PWM/ADC)      │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │     厂商SDK HAL层                                    │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │     硬件寄存器                                       │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                          │
│  驱动注册方式：组件化注册（非HdfDriverEntry）               │
│  配置方式：编译时宏定义/Kconfig（非HCS）                    │
└──────────────────────────────────────────────────────────┘
```

### 1.2 L0驱动开发模式

```c
/* L0轻量系统 GPIO驱动示例 — IoT外设子系统方式 */
#include "los_task.h"       /* LiteOS-M内核API */
#include "los_sem.h"
#include "gpio_if.h"        /* OpenHarmony GPIO HAL接口 */
#include "hal_gpio.h"       /* 芯片厂商HAL */

/* 初始化函数 — 通过组件注册机制调用 */
int gpio_driver_init(void)
{
    /* 直接调用厂商HAL初始化 */
    hal_gpio_clock_enable();
    
    /* 使用LiteOS-M内核API创建同步原语 */
    UINT32 semHandle;
    LOS_SemCreate(1, &semHandle);  /* 注意：不是OSAL */
    
    printf("GPIO driver initialized\n");
    return 0;
}

/* 读写操作 — 直接函数调用，非Dispatch模式 */
int gpio_read(uint32_t pin, uint8_t *val)
{
    *val = hal_gpio_read(pin);
    return 0;
}

int gpio_write(uint32_t pin, uint8_t val)
{
    hal_gpio_write(pin, val);
    return 0;
}
```

## 2. L1小型系统：精简版HDF驱动框架

### 2.1 核心概念

L1小型系统使用**精简版HDF**，支持HdfDriverEntry和HCS配置，但相比标准系统的完整HDF有所简化：

```
┌──────────────────────────────────────────────────────────┐
│              L1 精简版HDF驱动模型                          │
│                                                          │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────────┐  │
│  │HdfDriverEntry│──▶│ IDeviceIoService│──▶│ Dispatch Method│
│  │  .Bind()     │   │  .Dispatch    │   │  .Read()      │
│  │  .Init()     │   │  .Open        │   │  .Write()     │
│  │  .Release()  │   │  .Close       │   │  .Ioctl()     │
│  └─────────────┘   └──────────────┘   └──────────────┘  │
│                                                          │
│  ┌─────────────┐   ┌──────────────┐                      │
│  │ 精简版HCS    │   │ Device Host  │ ← 精简版             │
│  │ (.hcs文件)  │   │  Manager     │                      │
│  └─────────────┘   └──────────────┘                      │
│                                                          │
│  ⚠️ L1的HDF是精简版，部分高级特性不可用                     │
└──────────────────────────────────────────────────────────┘
```

### 2.2 驱动入口定义

```c
// HDF驱动入口 — 所有HDF驱动的标准模板
#include "hdf_device_desc.h"
#include "hdf_log.h"

#define HDF_LOG_TAG my_driver

// Dispatch方法实现
static int32_t MyDriverRead(struct HdfDeviceIoClient *client, int cmdId,
                             struct HdfSBuf *data, struct HdfSBuf *reply) {
    // 读取操作实现
    return HDF_SUCCESS;
}

static int32_t MyDriverWrite(struct HdfDeviceIoClient *client, int cmdId,
                              struct HdfSBuf *data, struct HdfSBuf *reply) {
    // 写入操作实现
    return HDF_SUCCESS;
}

static int32_t MyDriverDispatch(struct HdfDeviceIoClient *client, int cmdId,
                                 struct HdfSBuf *data, struct HdfSBuf *reply) {
    switch (cmdId) {
        case CMD_READ:
            return MyDriverRead(client, cmdId, data, reply);
        case CMD_WRITE:
            return MyDriverWrite(client, cmdId, data, reply);
        default:
            HDF_LOGE("%s: unsupported cmd %d", __func__, cmdId);
            return HDF_ERR_NOT_SUPPORT;
    }
}

// Bind: 将Dispatch绑定到设备服务对象
static int32_t MyDriverBind(struct HdfDeviceObject *deviceObject) {
    static struct IDeviceIoService ioService = {
        .Dispatch = MyDriverDispatch,
    };
    deviceObject->service = &ioService;
    return HDF_SUCCESS;
}

// Init: 从HCS读取配置并初始化硬件
static int32_t MyDriverInit(struct HdfDeviceObject *deviceObject) {
    const struct DeviceResourceNode *node = deviceObject->property;
    uint32_t regBase = 0;
    if (HdfReadDeviceMatchAttr(node, "regBase", &regBase) != HDF_SUCCESS) {
        HDF_LOGE("%s: read regBase failed", __func__);
        return HDF_FAILURE;
    }
    // 硬件初始化...
    HDF_LOGI("%s: init success, regBase=0x%x", __func__, regBase);
    return HDF_SUCCESS;
}

// Release: 释放资源
static void MyDriverRelease(struct HdfDeviceObject *deviceObject) {
    HDF_LOGI("%s: release", __func__);
    // 清理资源...
}

// 驱动入口
struct HdfDriverEntry g_myDriverEntry = {
    .moduleVersion = 1,
    .moduleName = "MY_DRIVER",
    .Bind = MyDriverBind,
    .Init = MyDriverInit,
    .Release = MyDriverRelease,
};
HDF_INIT(g_myDriverEntry);
```

### 2.3 HCS配置文件（仅L1小型系统使用）

```hcs
// my_driver_config.hcs — L1精简版HCS配置
root {
    platform {
        my_driver_config :: host {
            serviceName = "my_device_service";
            deviceMatchAttr = "my_device_001";
            
            device_0 :: device {
                device0 :: deviceNode {
                    policy = 2;          // 对用户态可见
                    priority = 100;
                    preload = 0;         // 按需加载
                    permission = 0644;
                    moduleName = "MY_DRIVER";
                    serviceName = "my_device_service";
                    
                    deviceMatchAttr = "my_device_001";
                    regBase = 0x40020000;
                    irq_num = 37;
                    bus_width = 8;
                }
            }
        }
    }
}
```

> ⚠️ **注意**：L0轻量系统不使用HCS配置，驱动参数通过编译时宏定义或Kconfig传递。

## 3. LiteOS-M原生API清单（L0迁移核心目标）

> ⚠️ **关键**：L0轻量系统的RTOS迁移目标是LiteOS-M原生API，而非OSAL。以下是FreeRTOS/RT-Thread代码迁移时的主要映射目标。

### 3.1 任务管理 (`los_task.h`)

| API | 原型 | 说明 |
|-----|------|------|
| `LOS_TaskCreate` | `UINT32 LOS_TaskCreate(UINT32 *taskID, TSK_INIT_PARAM_S *initParam)` | 创建并启动任务 |
| `LOS_TaskDelete` | `UINT32 LOS_TaskDelete(UINT32 taskID)` | 删除任务 |
| `LOS_TaskDelay` | `UINT32 LOS_TaskDelay(UINT32 tick)` | 延时指定tick数 |
| `LOS_TaskSuspend` | `UINT32 LOS_TaskSuspend(UINT32 taskID)` | 挂起任务 |
| `LOS_TaskResume` | `UINT32 LOS_TaskResume(UINT32 taskID)` | 恢复任务 |
| `LOS_TaskYield` | `UINT32 LOS_TaskYield(void)` | 让出CPU |
| `LOS_CurTaskIDGet` | `UINT32 LOS_CurTaskIDGet(void)` | 获取当前任务ID |

### 3.2 信号量 (`los_sem.h`)

| API | 原型 | 说明 |
|-----|------|------|
| `LOS_SemCreate` | `UINT32 LOS_SemCreate(UINT32 count, UINT32 *semHandle)` | 创建信号量 |
| `LOS_SemDelete` | `UINT32 LOS_SemDelete(UINT32 semHandle)` | 删除信号量 |
| `LOS_SemPend` | `UINT32 LOS_SemPend(UINT32 semHandle, UINT32 timeout)` | 等待信号量 |
| `LOS_SemPost` | `UINT32 LOS_SemPost(UINT32 semHandle)` | 释放信号量 |

### 3.3 互斥锁 (`los_mutex.h`)

| API | 原型 | 说明 |
|-----|------|------|
| `LOS_MuxCreate` | `UINT32 LOS_MuxCreate(UINT32 *muxHandle)` | 创建互斥锁 |
| `LOS_MuxDelete` | `UINT32 LOS_MuxDelete(UINT32 muxHandle)` | 删除互斥锁 |
| `LOS_MuxPend` | `UINT32 LOS_MuxPend(UINT32 muxHandle, UINT32 timeout)` | 获取互斥锁 |
| `LOS_MuxPost` | `UINT32 LOS_MuxPost(UINT32 muxHandle)` | 释放互斥锁 |

### 3.4 消息队列 (`los_queue.h`)

| API | 原型 | 说明 |
|-----|------|------|
| `LOS_QueueCreate` | `UINT32 LOS_QueueCreate(char *queueName, UINT16 maxMsg, ...)` | 创建消息队列 |
| `LOS_QueueDelete` | `UINT32 LOS_QueueDelete(UINT32 queueHandle)` | 删除消息队列 |
| `LOS_QueueWrite` | `UINT32 LOS_QueueWrite(UINT32 queueHandle, void *buffer, ...)` | 写入消息 |
| `LOS_QueueRead` | `UINT32 LOS_QueueRead(UINT32 queueHandle, void *buffer, ...)` | 读取消息 |

### 3.5 软件定时器 (`los_swtmr.h`)

| API | 原型 | 说明 |
|-----|------|------|
| `LOS_SwtmrCreate` | `UINT32 LOS_SwtmrCreate(UINT32 interval, UINT8 mode, SWTMR_PROC_FUNC handler, ...)` | 创建定时器 |
| `LOS_SwtmrStart` | `UINT32 LOS_SwtmrStart(UINT16 swtmrID)` | 启动定时器 |
| `LOS_SwtmrStop` | `UINT32 LOS_SwtmrStop(UINT16 swtmrID)` | 停止定时器 |
| `LOS_SwtmrDelete` | `UINT32 LOS_SwtmrDelete(UINT16 swtmrID)` | 删除定时器 |

### 3.6 内存管理 (`los_memory.h`)

| API | 原型 | 说明 |
|-----|------|------|
| `LOS_MemAlloc` | `void *LOS_MemAlloc(void *pool, UINT32 size)` | 分配内存 |
| `LOS_MemFree` | `UINT32 LOS_MemFree(void *pool, void *mem)` | 释放内存 |
| `LOS_MemRealloc` | `void *LOS_MemRealloc(void *pool, void *mem, UINT32 size)` | 重新分配 |

## 4. CMSIS-RTOS2接口映射（L0重要补充）

> ⚠️ **重要**：很多FreeRTOS/RT-Thread项目中使用CMSIS接口编写跨平台代码。LiteOS-M的KAL层提供了CMSIS-RTOS2兼容实现，如果源代码使用了CMSIS接口，可以直接链接到LiteOS-M的CMSIS实现而无需修改。

| CMSIS-RTOS2 API | FreeRTOS等价 | RT-Thread等价 | LiteOS-M KAL实现 |
|----------------|-------------|--------------|-----------------|
| `osThreadNew()` | `xTaskCreate()` | `rt_thread_create()` + `rt_thread_startup()` | ✅ 已支持 |
| `osDelay()` | `vTaskDelay()` | `rt_thread_mdelay()` | ✅ 已支持 |
| `osMutexNew()` | `xSemaphoreCreateMutex()` | `rt_mutex_init()` | ✅ 已支持 |
| `osSemaphoreNew()` | `xSemaphoreCreateBinary()` | `rt_sem_init()` | ✅ 已支持 |
| `osMessageQueueNew()` | `xQueueCreate()` | `rt_mq_init()` | ✅ 已支持 |
| `osTimerNew()` | `xTimerCreate()` | `rt_timer_create()` | ✅ 已支持 |
| `osKernelGetTickCount()` | `xTaskGetTickCount()` | `rt_tick_get()` | ✅ 已支持 |

## 5. OSAL接口完整清单（仅L1小型系统使用）

### 5.1 内存管理 (`osal_mem.h`)

| API | 原型 | 说明 |
|-----|------|------|
| `OsalMemAlloc` | `void *OsalMemAlloc(size_t size)` | 分配指定大小内存 |
| `OsalMemCalloc` | `void *OsalMemCalloc(size_t nmemb, size_t size)` | 分配并清零内存 |
| `OsalMemRealloc` | `void *OsalMemRealloc(void *ptr, size_t size)` | 重新分配内存 |
| `OsalMemFree` | `void OsalMemFree(void *mem)` | 释放内存 |
| `OsalMemAlign` | `void *OsalMemAlign(unsigned int boundary, size_t size)` | 对齐分配内存 |
| `OsalMemFreeAlign` | `void OsalMemFreeAlign(void *mem)` | 释放对齐内存 |

### 5.2 互斥锁 (`osal_mutex.h`)

| API | 原型 | 说明 |
|-----|------|------|
| `OsalMutexInit` | `int32_t OsalMutexInit(OsalMutex *mutex)` | 初始化互斥锁 |
| `OsalMutexDestroy` | `int32_t OsalMutexDestroy(OsalMutex *mutex)` | 销毁互斥锁 |
| `OsalMutexLock` | `int32_t OsalMutexLock(OsalMutex *mutex)` | 加锁（阻塞） |
| `OsalMutexUnlock` | `int32_t OsalMutexUnlock(OsalMutex *mutex)` | 解锁 |
| `OsalMutexTimedLock` | `int32_t OsalMutexTimedLock(OsalMutex *mutex, uint32_t ms)` | 超时加锁 |

### 5.3 信号量 (`osal_sem.h`)

| API | 原型 | 说明 |
|-----|------|------|
| `OsalSemInit` | `int32_t OsalSemInit(OsalSem *sem, uint32_t value)` | 初始化信号量 |
| `OsalSemDestroy` | `int32_t OsalSemDestroy(OsalSem *sem)` | 销毁信号量 |
| `OsalSemWait` | `int32_t OsalSemWait(OsalSem *sem, uint32_t ms)` | 等待信号量 |
| `OsalSemPost` | `int32_t OsalSemPost(OsalSem *sem)` | 释放信号量 |

### 5.4 自旋锁 (`osal_spinlock.h`)

| API | 原型 | 说明 |
|-----|------|------|
| `OsalSpinlockInit` | `int32_t OsalSpinlockInit(OsalSpinlock *lock)` | 初始化自旋锁 |
| `OsalSpinlockDestroy` | `int32_t OsalSpinlockDestroy(OsalSpinlock *lock)` | 销毁自旋锁 |
| `OsalSpinlockLock` | `int32_t OsalSpinlockLock(OsalSpinlock *lock)` | 获取自旋锁 |
| `OsalSpinlockUnlock` | `int32_t OsalSpinlockUnlock(OsalSpinlock *lock)` | 释放自旋锁 |
| `OsalSpinlockIrqSave` | `int32_t OsalSpinlockIrqSave(OsalSpinlock *lock, unsigned long *flags)` | 关中断并获取锁 |
| `OsalSpinlockIrqRestore` | `int32_t OsalSpinlockIrqRestore(OsalSpinlock *lock, unsigned long flags)` | 恢复中断并释放锁 |

### 5.5 线程管理 (`osal_thread.h`)

| API | 原型 | 说明 |
|-----|------|------|
| `OsalThreadCreate` | `OsalThread *OsalThreadCreate(const char *name, OsalThreadFunc func, void *param)` | 创建线程 |
| `OsalThreadStart` | `int32_t OsalThreadStart(OsalThread *thread, const OsalThreadParam *param)` | 启动线程 |
| `OsalThreadDestroy` | `int32_t OsalThreadDestroy(OsalThread *thread)` | 销毁线程 |
| `OsalThreadJoin` | `int32_t OsalThreadJoin(OsalThread *thread)` | 等待线程结束 |
| `OsalThreadDetach` | `int32_t OsalThreadDetach(OsalThread *thread)` | 分离线程 |
| `OsalThreadKill` | `int32_t OsalThreadKill(OsalThread *thread)` | 终止线程 |
| `OsalThreadSetSchedParam` | `int32_t OsalThreadSetSchedParam(OsalThread *thread, const OsalThreadParam *param)` | 设置调度参数 |
| `OsalSleep` | `int32_t OsalSleep(uint32_t ms)` | 休眠指定毫秒 |

### 5.6 定时器 (`osal_timer.h`)

| API | 原型 | 说明 |
|-----|------|------|
| `OsalTimerInit` | `int32_t OsalTimerInit(OsalTimer *timer, uint32_t ms, OsalTimerFunc func, void *arg, OsalTimerType type)` | 初始化定时器 |
| `OsalTimerStart` | `int32_t OsalTimerStart(OsalTimer *timer)` | 启动定时器 |
| `OsalTimerStop` | `int32_t OsalTimerStop(OsalTimer *timer)` | 停止定时器 |
| `OsalTimerDelete` | `int32_t OsalTimerDelete(OsalTimer *timer)` | 删除定时器 |

### 5.7 中断管理 (`osal_irq.h`)

| API | 原型 | 说明 |
|-----|------|------|
| `OsalRegisterIrq` | `int32_t OsalRegisterIrq(uint32_t irq, uint32_t flags, OsalIrqHandler handler, const char *name, void *dev)` | 注册中断处理函数 |
| `OsalUnregisterIrq` | `int32_t OsalUnregisterIrq(uint32_t irq, void *dev)` | 注销中断处理函数 |
| `OsalEnableIrq` | `int32_t OsalEnableIrq(uint32_t irq)` | 使能中断 |
| `OsalDisableIrq` | `int32_t OsalDisableIrq(uint32_t irq)` | 禁止中断 |
| `OsalSaveIrq` | `unsigned long OsalSaveIrq(void)` | 保存中断状态并关中断 |
| `OsalRestoreIrq` | `void OsalRestoreIrq(unsigned long flags)` | 恢复中断状态 |

### 5.8 原子操作 (`osal_atomic.h`)

| API | 原型 | 说明 |
|-----|------|------|
| `OsalAtomicRead` | `int32_t OsalAtomicRead(OsalAtomic *v)` | 读取原子变量 |
| `OsalAtomicSet` | `void OsalAtomicSet(OsalAtomic *v, int32_t counter)` | 设置原子变量 |
| `OsalAtomicInc` | `void OsalAtomicInc(OsalAtomic *v)` | 原子递增 |
| `OsalAtomicDec` | `void OsalAtomicDec(OsalAtomic *v)` | 原子递减 |
| `OsalAtomicIncReturn` | `int32_t OsalAtomicIncReturn(OsalAtomic *v)` | 原子递增并返回 |
| `OsalAtomicDecReturn` | `int32_t OsalAtomicDecReturn(OsalAtomic *v)` | 原子递减并返回 |

### 5.9 日志 (`hdf_log.h`)

| API | 说明 |
|-----|------|
| `HDF_LOGF(fmt, ...)` | Fatal级别日志 |
| `HDF_LOGE(fmt, ...)` | Error级别日志 |
| `HDF_LOGW(fmt, ...)` | Warning级别日志 |
| `HDF_LOGI(fmt, ...)` | Info级别日志 |
| `HDF_LOGD(fmt, ...)` | Debug级别日志 |
