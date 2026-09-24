# Hi3861 SDK API 交叉引用表 + CMSIS 映射

> **来源**: Ground Truth `device/soc/hisilicon/hi3861v100/hi3861_adapter/hals/` 全部 HAL 文件
> **用途**: P2 (kernel-port) + P3 (driver-dev) 阶段的 API 命名参考
> **版本**: Iteration 02 提取

---

## 第一部分: IoT HAL → HiSilicon SDK API 映射

### 命名规则总则

```
OH IoT HAL 函数命名:  <Module><Action>() 或 IoT<Module><Action>()
HiSilicon SDK 命名:     hi_<module>_<action>()

转换规则:
  1. Module 名: PascalCase → snake_case (全小写 + 下划线)
  2. Action 名: camelCase → snake_case
  3. 特殊映射需查下表 (非所有都遵循规则)
```

---

### 1.1 Watchdog HAL (`hal_iot_watchdog.c`)

| OH IoT HAL 接口 | HiSilicon SDK 函数 | 头文件 |
|-----------------|-------------------|--------|
| `IoTWatchDogEnable(void)` | `hi_watchdog_enable(void)` | `"hi_watchdog.h"` |
| `IoTWatchDogKick(void)` | `hi_watchdog_feed(void)` | ⚠️ Kick→Feed! |
| `IoTWatchDogDisable(void)` | `hi_watchdog_disable(void)` | |

**OH 头文件**: `"iot_watchdog.h"`, `"iot_errno.h"`

**完整 GT 代码模式**:
```c
#include "iot_errno.h"
#include "iot_watchdog.h"
#include "hi_watchdog.h"

void IoTWatchDogEnable(void)  { return hi_watchdog_enable(); }
void IoTWatchDogKick(void)    { return hi_watchdog_feed(); }
void IoTWatchDogDisable(void) { return hi_watchdog_disable(); }
```

**特点**: 最简单的 HAL — 纯 1:1 委托，无状态，无参数处理。

---

### 1.2 Reset HAL (`hal_reset.c`)

| OH IoT HAL 接口 | HiSilicon SDK 函数 | 头文件 |
|-----------------|-------------------|--------|
| `RebootDevice(unsigned int cause)` | `hi_hard_reboot(cause)` | `"hi_reset.h"` |

**OH 头文件**: `"reset.h"`

```c
#include "reset.h"
#include "hi_reset.h"

void RebootDevice(unsigned int cause) { hi_hard_reboot(cause); }
```

---

### 1.3 Lowpower HAL (`hal_lowpower.c`)

| OH IoT HAL 接口 | HiSilicon SDK 函数 | 头文件 |
|-----------------|-------------------|--------|
| `LpcInit(void)` | `hi_lpc_init(void)` | `"hi_lowpower.h"` |
| `LpcSetType(LpcType type)` | `hi_lpc_set_type(type)` | |

**OH 头文件**: `"lowpower.h"`

**返回值**: `unsigned int` (0 = 成功, 非 0 = 错误码)

---

### 1.4 GPIO HAL (`hal_iot_gpio.c`) — Iteration 01 数据

| OH IoT HAL 接口 | HiSilicon SDK 函数 | 备注 |
|-----------------|-------------------|------|
| `GpioInit(void)` | `hi_gpio_init()` | 初始化 GPIO 模块 |
| `GpioSetDir(WifiIotGpioIdx, WifiIotGpioDir)` | `hi_gpio_set_dir(idx, dir)` | 方向: INPUT/OUTPUT |
| `GpioGetOutputVal(WifiIotGpioIdx)` | `hi_gpio_get_output_val(idx)` | 读取输出寄存器 |
| `GpioSetOutputVal(WifiIotGpioIdx, WifiIotGpioValue)` | `hi_gpio_set_output_val(idx, val)` | 设置高低电平 |
| `GpioRegisterIsrCallback(WifiIotGpioIdx, GpioIntFunc, char*)` | `hi_gpio_register_isr_function(idx, func, arg)` | 中断回调 |
| `GpioUnregisterIsrCallback(WifiIotGpioIdx)` | `hi_gpio_unregister_isr_function(idx)` | 注销中断 |
| `GpioSetIsrMask(WifiIotGpioIdx, uint16_t)` | `hi_gpio_set_isr_mask(idx, mask)` | 中断屏蔽 |
| `GpioSetIsrMode(WifiIotGpioIdx, GpioIntType, GpioIntPolarity)` | `hi_gpio_set_isr_mode(idx, type, polarity)` | 中断触发方式 |

**OH 头文件**: `"iot_gpio.h"`
**SDK 头文件**: `"hi_gpio_io.h"`

**枚举类型映射**:
```
WifiIotGpioIdx    → hi_gpio_idx (GPIO_0 ~ GPIO_15 on Hi3861V100)
WifiIotGpioDir    → hi_gpio_dir (HI_GPIO_DIR_IN / HI_GPIO_DIR_OUT)
WifiIotGpioValue  → HI_GPIO_VALUE0 / HI_GPIO_VALUE1
GpioIntType       → hi_gpio_int_type (INT_TYPE_LEVEL / INT_TYPE_EDGE)
GpioIntPolarity   → hi_gpio_int_polarity
```

---

### 1.5 I2C HAL (`hal_iot_i2c.c`) — Iteration 01 数据

| OH IoT HAL 接口 | HiSilicon SDK 函数 | 备注 |
|-----------------|-------------------|------|
| `I2cInit(WifiIotI2cIdx id, const WifiIotI2cConfig* cfg)` | `hi_i2c_init(id, hi_i2c_cfg*)` | 初始化 I2C 控制器 |
| `I2cDeinit(WifiIotI2cIdx id)` | `hi_i2c_deinit(id)` | 反初始化 |
| `I2cRead(WifiIotI2cIdx, addr, reg, ...)` | `hi_i2c_read(...)` | 读寄存器 |
| `I2cWrite(WifiIotI2cIdx, addr, reg, ...)` | `hi_i2c_write(...)` | 写寄存器 |
| `I2cSetBaudrate(WifiIotI2cIdx, baudrate)` | `hi_i2c_set_baudrate(id, bps)` | 设置波特率 |

**OH 头文件**: `"iot_i2c.h"`
**SDK 头文件**: `"hi_i2c.h"`

---

### 1.6 PWM HAL (`hal_iot_pwm.c`) — Iteration 01 数据 (100% PASS)

| OH IoT HAL 接口 | HiSilicon SDK 函数 |
|-----------------|-------------------|
| `PwmInit(WifiIotPwmPort port)` | `hi_pwm_init(port)` |
| `PwmDeinit(WifiIotPwmPort port)` | `hi_pwm_deinit(port)` |
| `PwmStart(WifiIotPwmPort port, uint16_t*, uint8_t)` | `hi_pwm_start(port, duty, freq, ...)` |
| `PwmStop(WifiIotPwmPort port)` | `hi_pwm_stop(port)` |
| `PwmSetPeriod(WifiIotPwmPort port, uint16_t, uint8_t)` | `hi_pwm_set_port_period(port, period, duty)` |
| `PwmGetCycleTime(WifiIotPwmPort port, uint16_t*)` | `hi_pwm_get_cycle_time(port, time)` |

**OH 头文件**: `"iot_pwm.h"`
**SDK 头文件**: `"hi_pwm.h"`

---

### 1.7 UART HAL (`hal_iot_uart.c`) — Iteration 01 数据 (80% PASS)

| OH IoT HAL 接口 | HiSilicon SDK 函数 | ⚠️ 注意 |
|-----------------|-------------------|---------|
| `UartInit(const WifiIotUartAttr*)` | `hi_uart_init(hi_uart_idx, hi_uart_attr*)` | 属性结构不同 |
| `UartDeinit(WifiIotUwmIdx)` | `hi_uart_deinit(idx)` | |
| `UartRead(WifiIotUartIdx, char*, uint32_t)` | `hi_uart_receive(idx, buf, len)` | Read→Receive |
| `UartWrite(WifiIotUartIdx, const char*, uint32_t)` | `hi_uart_send(idx, buf, len)` | Write→Send |
| `UartSetFlowCtrl(WifiIotUartIdx, WifiIotFlowCtrl)` | `hi_uart_set_flowctrl(idx, ctrl)` | |

**⚠️ UART 特殊之处**:
- OH 使用 `WifiIotUartAttr` 结构体，SDK 使用 `hi_uart_attribute`
- 字段名称不同但含义相同：baud_rate/data_bits/stop_bits/parity/pad
- Read/Write 在 SDK 端叫 Receive/Send（命名不一致！）

---

### 1.8 Flash HAL (`hal_iot_flash.c`) — Iteration 01 数据 (60% PARTIAL)

| OH IoT HAL 接口 | HiSilicon SDK 函数 |
|-----------------|-------------------|
| `FlashWrite(uint32_t, const void*, uint32_t, uint32_t)` | `hi_flash_write(addr, data, len)` |
| `FlashRead(uint32_t, void*, uint32_t, uint32_t)` | `hi_flash_read(addr, data, len)` |
| `FlashInit(void)` | `hi_flash_init()` |

**OH 头文件**: `"iot_flash.h"`
**SDK 头文件**: `"hi_flash.h"`

---

### 1.9 命名不一致汇总表

| OH 名称 | SDK 名称 | 差异类型 |
|---------|---------|---------|
| `IoTWatchDogKick` | `hi_watchdog_feed` | 语义差异 (kick≠feed) |
| `UartRead` | `hi_uart_receive` | Read→Receive |
| `UartWrite` | `hi_uart_send` | Write→Send |
| `GpioGetOutputVal` | `hi_gpio_get_output_val` | 一致 |
| `PwmSetPeriod` | `hi_pwm_set_port_period` | 多了 `port` 前缀 |

> **生成时必须查此表** — 不能简单用正则替换！

---

## 第二部分: CMSIS-RTOS v2 → LiteOS 映射表

> **来源**: `kal/cmsis/cmsis_liteos2.c` (~800+ 行)
> **注意**: `cmsis_liteos.c` 只是版本检查，实际实现在 `cmsis_liteos2.c`

### 2.1 版本关系

```c
// cmsis_liteos.c 内容:
#if (CMSIS_OS_VER == 1)
#error "cmsis version 1.0 is not supported now!"
#elif (CMSIS_OS_VER == 2)
#include "cmsis_liteos2.c"   // ← 所有 v2 实现都在这里
#endif
```

**结论**: 只需支持 CMSIS-RTOS v2，v1 不支持。

---

### 2.2 内核管理 (Kernel Management)

| CMSIS-RTOS v2 API | LiteOS 映射 | 关键细节 |
|-------------------|------------|---------|
| `osKernelInitialize(void)` | `LOS_KernelInit()` + `LOS_TaskLock()` | Init 后锁定调度器 |
| `osKernelStart(void)` | `LOS_TaskUnlock()` | 解锁即启动 |
| `osKernelGetState(void)` | 检查 `g_taskScheduled` | 返回 osKernelRunning/Locked/Inactive |
| `osKernelLock(void)` | `LOS_TaskLock()` | 返回锁深度计数 |
| `osKernelUnlock(void)` | `LOS_TaskUnlock()` | |
| `osKernelRestoreLock(int32_t)` | `LOS_TaskRestoreLock(depth)` | 恢复到指定深度 |
| `osKernelGetTickCount(void)` | `LOS_TickCountGet()` | UINT32 tick 数 |
| `osKernelGetTickFreq(void)` | `LOSCFG_BASE_CORE_TICK_PER_SECOND` | 编译时常量 |
| `osKernelGetSysTimerCount(void)` | `LOS_GetCpuCycle(&hi, &lo)` | 64-bit CPU cycle |
| `osKernelGetSysTimerFreq(void)` | `LOS_GetCpuCycleClk()` | CPU 时钟频率 (Hz) |

---

### 2.3 线程管理 (Thread Management)

| CMSIS-RTOS v2 API | LiteOS 映射 | 类型映射 |
|-------------------|------------|---------|
| `osThreadNew(func, arg, attr)` | `LOS_TaskCreate(&tid, &stTskInitParam, entry, p1..p4)` | attr→TSK_INIT_PARAM_S |
| `osThreadGetName(thread_id)` | `LOS_TaskNameGet(taskID)` | 从 TCB 读取 |
| `osThreadGetId(void)` | `LOS_CurTaskIDGet()` | 返回 osThreadId_t |
| `osThreadGetArgument(void)` | 从 TCB 自定义字段获取 | |
| `osThreadGetState(thread_id)` | 检查 TCB->taskStatus | 映射到 osThreadXxx 枚举 |
| `osThreadGetStackSize(thread_id)` | 检查 TCB->stackSize | |
| `osThreadSetPriority(tid, prio)` | `LOS_TaskPriSet(taskID, losPrio)` | ⚠️ 优先级反转! |
| `osThreadGetPriority(tid)` | `LOS_TaskPriGet(taskID)` | |
| `osThreadYield(void)` | `LOS_TaskYield()` | |
| `osThreadSuspend(tid)` | `LOS_TaskSuspend(taskID)` | |
| `osThreadResume(tid)` | `LOS_TaskResume(taskID)` | |
| `osThreadTerminate(tid)` | `LOS_TaskDelete(taskID)` | |
| `osThreadGetCount(void)` | 自定义遍历任务数组 | |
| `osDelay(ticks)` | `LOS_TaskDelay(ticks)` | |
| `osDelayUntil(tick)` | `LOS_TaskDelay(tick - now)` | 绝对时间延迟 |

#### 优先级映射 (关键!)

```
CMSIS: 高优先级 = 大数字 (osPriorityHigh = 24, osPriorityNormal = 15, osPriorityLow = 7)
LiteOS: 高优先级 = 小数字 (0 = 最高, 31 = 最低)

转换公式:
  los_priority = LOS_PRIO_PROCESS - cmsis_priority;
  // 其中 LOS_PRIO_PROCESS 通常 = 31
  // 例: cmsis=24 → los=7, cmsis=15 → los=16, cmsis=7 → los=24
```

#### osThreadAttr_t → TSK_INIT_PARAM_S 映射

```c
// CMSIS 属性
typedef struct {
    const char *name;        // → taskInitParam.pcName
    uint32_t attr_bits;      // → 未使用 (LiteOS 无概念)
    void *cb_mem;            // → taskInitParam.uwStackSize (自定义栈)
    uint32_t cb_size;        // → 同上
    int priority;            // → taskInitParam.usTaskPrio (需反转!)
    uint32_t stack_size;     // → taskInitParam.uwStackSize
} osThreadAttr_t;

// LiteOS 参数
typedef struct {
    CHAR *pcName;             // 线程名
    UINT32 usTaskPrio;        // 优先级 (0=highest)
    UINT32 uwStackSize;       // 栈大小 (bytes)
    TSK_ENTRY_FUNC pfnTaskEntry; // 入口函数
    UINT32 auwArgs[4];        // 4 个参数
} TSK_INIT_PARAM_S;
```

---

### 2.4 定时器管理 (Timer Management)

| CMSIS-RTOS v2 API | LiteOS 映射 | 说明 |
|-------------------|------------|------|
| `osTimerNew(func, type, arg, attr)` | `LOS_SwtmrCreate(1, mode, (SWTMR_PROC_FUNC)func, &id, (UINT32)arg)` | type→mode 转换 |
| `osTimerStart(timer_id, ticks)` | `LOS_SwtmrStart(swtmrId, ticks)` | |
| `osTimerStop(timer_id)` | `LOS_SwtmrStop(swtmrId)` | |
| `osTimerGetName(timer_id)` | 自定义存储 (attr->name) | |
| `osTimerIsRunning(timer_id)` | `LOS_SwtmrRunningGet(swtmrId)` | |
| `osTimerDelete(timer_id)` | `LOS_SwtmrDelete(swtmrId)` | |

#### 定时器类型映射

```
osTimerOnce      → SWTMR_MODE_ONCE       // 单次触发
osTimerPeriodic  → SWTMR_MODE_PERIODIC   // 周期触发
osTimerOneShot   → SWTMR_MODE_ONCE (同 Once)
```

---

### 2.5 事件标志 (Event Flags)

| CMSIS-RTOS v2 API | LiteOS 映射 |
|-------------------|------------|
| `osEventFlagsNew(attr)` | `LOS_EventInit(&eventHandle)` |
| `osEventFlagsSet(ef_id, flags)` | `LOS_EventWrite(handle, flags)` |
| `osEventFlagsClear(ef_id, flags)` | `LOS_EventClear(handle, flags)` |
| `osEventFlagsWait(ef_id, flags, options, timeout)` | `LOS_EventRead(handle, rflags, mode, timeout)` |
| `osEventFlagsGetName(ef_id)` | 自定义存储 |
| `osEventFlagsDelete(ef_id)` | `LOS_EventDestory(handle)` |

#### Wait Options 映射

```
osFlagsWaitAny     → LOS_WAITMODE_OR
osFlagsWaitAll     → LOS_WAITMODE_AND
osFlagsNoClear     → 不设置 LOS_WAITMODE_CLR (读取后不清除)
osFlagsClearAll    → 默认行为 (读取后清除)
```

---

### 2.6 互斥量 (Mutex)

| CMSIS-RTOS v2 API | LiteOS 映射 |
|-------------------|------------|
| `osMutexNew(attr)` | `LOS_MuxCreate(&muxHandle)` |
| `osMutexAcquire(mutex, timeout)` | `LOS_MuxLock(muxHandle, timeout)` |
| `osMutexRelease(mutex)` | `LOS_MuxUnlock(muxHandle)` |
| `osMutexGetCount(mutex)` | `LOS_MuxGetCount(muxHandle)` |
| `osMutexDelete(mutex)` | `LOS_MuxDelete(muxHandle)` |
| `osMutexGetName(mutex)` | 自定义存储 |

---

### 2.7 信号量 (Semaphore)

| CMSIS-RTOS v2 API | LiteOS 映射 | 说明 |
|-------------------|------------|------|
| `osSemaphoreNew(max_count, initial, attr)` | `LOS_SemCreate(initCount)` | max_count 在 LiteOS 中忽略 |
| `osSemaphoreAcquire(sem, timeout)` | `LOS_SemPend(semHandle, timeout)` | |
| `osSemaphoreRelease(sem)` | `LOS_SemPost(semHandle)` | |
| `osSemaphoreGetCount(sem)` | `LOS_SemGetCount(semHandle)` | |
| `osSemaphoreDelete(sem)` | `LOS_SemDelete(semHandle)` | |
| `osSemaphoreGetName(sem)` | 自定义存储 | |

> **注意**: CMSIS 的 counting semaphore (max_count > 1) 在 LiteOS 中降级为 binary semaphore。如需真正的 counting semaphore，需要使用 Event Flags 替代。

---

### 2.8 内存池 (Memory Pool) — 可选

| CMSIS-RTOS v2 API | LiteOS 映射 |
|-------------------|------------|
| `osMemoryPoolNew(block_count, block_size, attr)` | `LOS_MemboxCreate(pool, blkSz, blkCnt)` |
| `osMemoryPoolAlloc(mp, timeout)` | `LOS_MboxAlloc(pool, timeout)` |
| `osMemoryPoolFree(mp, block)` | `LOS_MboxFree(pool, block)` |
| `osMemoryPoolDelete(mp)` | `LOS_MboxDelete(pool)` |

---

### 2.9 类型映射速查

| CMSIS 类型 | LiteOS 实际类型 | 说明 |
|-----------|---------------|------|
| `osThreadId_t` | `UINT32` | 任务 ID (可能偏移) |
| `osTimerId_t` | `UINT32` | 软件 Timer ID |
| `osEventFlagsId_t` | `EVENT_HANDLE_S` (= UINT32) | 事件标志句柄 |
| `osMutexId_t` | `UINT32` | Mux 句柄 |
| `osSemaphoreId_t` | `UINT32` | Sem 句柄 |
| `osMemoryPoolId_t` | `VOID*` | 内存池指针 |
| `osStatus_t` | `int` / 枚举 | osOK=0, osError=-1, etc. |
| `osPriority_t` | `int` | 与 LiteOS 优先级**反向** |
| `uint32_t` | `UINT32` | 兼容 |
| `uint64_t` | `UINT64_T` | 仅用于 SysTimer |

---

## 第三部分: 头文件包含矩阵

### 3.1 每个 HAL 文件的标准头文件组合

| HAL 文件 | OH 公共头文件 | SDK 私有头文件 | 其他依赖 |
|----------|-------------|--------------|---------|
| hal_iot_watchdog.c | iot_errno.h, iot_watchdog.h | hi_watchdog.h | — |
| hal_reset.c | reset.h | hi_reset.h | — |
| hal_lowpower.c | lowpower.h | hi_lowpower.h | — |
| hal_iot_gpio.c | iot_gpio.h | hi_gpio_io.h | — |
| hal_iot_i2c.c | iot_i2c.h | hi_i2c.h | — |
| hal_iot_pwm.c | iot_pwm.h | hi_pwm.h | — |
| hal_iot_uart.c | iot_uart.h | hi_uart.h | — |
| hal_iot_flash.c | iot_flash.h | hi_flash.h | — |
| pthread.c | pthread.h, unistd.h, errno.h | — | los_task.h, los_task_pri.h, securec.h |
| time.c | time.h, errno.h | — | los_tick.h, los_swtmr.h |
| file.c | fcntl.h, unistd.h, errno.h | hi_fs.h, hks_client.h | lwip/sockets.h, securec.h |
| cmsis_liteos2.c | cmsis_os2.h | — | los_task.h, los_swtmr.h, los_mux.h, los_sem.h, los_event.h |

---

## 第四部分: 生成时常见错误与修正

### 错误 1: 直接使用正则替换命名
```
❌ 错误: s/GpioSetOutput/hi_gpio_set_output/g
✅ 正确: 必须查表 — UartRead→hi_uart_receive (不是 uart_read)
```

### 错误 2: CMSIS 优先级未反转
```
❌ 错误: LOS_TaskPriSet(tid, cmsis_prio)  // 直接传入
✅ 正确: LOS_TaskPriSet(tid, 31 - cmsis_prio)  // 反转
```

### 错误 3: pthread_t == raw taskID
```
❌ 错误: pthread_create 返回 LOS_CurTaskIDGet()
✅ 正确: 返回 T2P(taskID) = taskID + g_taskMaxNum
```

### 错误 4: FD 空间未分区
```
❌ 错误: open() 返回 hi_fs_open() 的原始 FD
✅ 正确: 返回 HI_FS_FD_OFFSET + internal_fd (避免与 socket 冲突)
```

### 错误 5: Timer ID 与 Task ID 冲突
```
❌ 错误: timer ID 从 0 开始分配
✅ 正确: timer ID 也需要偏移 (类似 pthread_t)，或使用独立命名空间
```
