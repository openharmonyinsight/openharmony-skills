# 跨平台API映射表

> 来源：需求5分析报告 §6

---

## 1. FreeRTOS → LiteOS-M 映射表（L0轻量系统核心映射）

> ⚠️ **这是L0轻量系统最常用的映射**。FreeRTOS和LiteOS-M都是RTOS，API差异相对较小。

| # | FreeRTOS API | LiteOS-M API | 映射复杂度 | 注意事项 |
|---|-------------|-------------|-----------|---------|
| 1 | `xTaskCreate()` | `LOS_TaskCreate()` | 🟡 中 | 参数重组：FreeRTOS传栈大小(word)，LiteOS传字节；优先级数值方向相反 |
| 2 | `vTaskDelete()` | `LOS_TaskDelete()` | 🟢 低 | 语义等价 |
| 3 | `vTaskDelay(ticks)` | `LOS_TaskDelay(ticks)` | 🟢 低 | 注意Tick频率可能不同(configTICK_RATE_HZ vs LOSCFG_BASE_CORE_TICK_PER_SECOND) |
| 4 | `vTaskDelayUntil()` | ❌ 无直接对应 | 🔴 高 | 需用LOS_Swtmr或手动计算绝对时间 |
| 5 | `xSemaphoreCreateMutex()` | `LOS_MuxCreate()` | 🟢 低 | 语义等价 |
| 6 | `xSemaphoreTake(mutex, wait)` | `LOS_MuxPend(mux, timeout)` | 🟡 中 | 超时单位转换：ticks→ticks(需确认tick频率一致) |
| 7 | `xSemaphoreGive(mutex)` | `LOS_MuxPost()` | 🟢 低 | 语义等价 |
| 8 | `xSemaphoreCreateBinary()` | `LOS_SemCreate(0, &sem)` | 🟢 低 | 初始值为0 |
| 9 | `xSemaphoreCreateCounting(max, init)` | `LOS_SemCreate(init, &sem)` | 🟡 中 | LiteOS-M信号量不限制最大值 |
| 10 | `xSemaphoreTakeFromISR()` | ❌ ISR中不使用信号量 | 🔴 高 | 改用原子变量+任务唤醒模式 |
| 11 | `xQueueCreate()` | `LOS_QueueCreate()` | 🟡 中 | ✅ LiteOS-M原生支持消息队列！参数格式不同 |
| 12 | `xQueueSend()` / `xQueueReceive()` | `LOS_QueueWrite()` / `LOS_QueueRead()` | 🟡 中 | 参数重组，但功能等价 |
| 13 | `xTimerCreate()` | `LOS_SwtmrCreate()` | 🟡 中 | 回调签名略有不同 |
| 14 | `pvPortMalloc()` | `LOS_MemAlloc()` 或 `malloc()` | 🟢 低 | 取决于内存管理配置 |
| 15 | `vPortFree()` | `LOS_MemFree()` 或 `free()` | 🟢 低 | 配对使用 |
| 16 | `taskENTER_CRITICAL()` | `LOS_IntLock()` | 🟡 中 | 语义相似 |
| 17 | `taskEXIT_CRITICAL()` | `LOS_IntRestore()` | 🟡 中 | 配对使用 |
| 18 | `*FromISR()`系列 | 对应LiteOS-M接口(部分) | 🔴 高 | ISR上下文中只能使用部分API |
| 19 | `xTaskNotifyGive()` / `ulTaskNotifyTake()` | `LOS_SemPost()` / `LOS_SemPend()` | 🟡 中 | 任务通知→信号量近似替代 |
| 20 | `eTaskGetState()` | ❌ 无直接对应 | 🔴 高 | 需自行维护状态跟踪 |

### FreeRTOS → LiteOS-M 迁移示例

```c
/* ===== 迁移前 (FreeRTOS) ===== */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

static SemaphoreHandle_t uart_mutex;
void uart_init(void) {
    uart_mutex = xSemaphoreCreateMutex();
    xTaskCreate(uart_task, "uart", 512, NULL, 5, NULL);
}
void uart_send(uint8_t *data, uint32_t len) {
    xSemaphoreTake(uart_mutex, portMAX_DELAY);
    HAL_UART_Transmit(&huart, data, len, 1000);
    xSemaphoreGive(uart_mutex);
}

/* ===== 迁移后 (LiteOS-M) ===== */
#include "los_task.h"
#include "los_mutex.h"

static UINT32 uart_mux;
void uart_init(void) {
    LOS_MuxCreate(&uart_mux);
    TSK_INIT_PARAM_S param = {0};
    param.pfnTaskEntry = (TSK_ENTRY_FUNC)uart_task;
    param.uwStackSize = 2048;       /* 注意：字节而非word */
    param.pcName = "uart";
    param.usTaskPrio = 5;           /* 注意：数值含义可能不同 */
    UINT32 taskID;
    LOS_TaskCreate(&taskID, &param);
}
void uart_send(uint8_t *data, uint32_t len) {
    LOS_MuxPend(uart_mux, LOS_WAIT_FOREVER);
    HAL_UART_Transmit(&huart, data, len, 1000);
    LOS_MuxPost(uart_mux);
}
```

## 2. RT-Thread → LiteOS-M 映射表（L0轻量系统重要映射）

> ⚠️ RT-Thread在国内IoT市场占有率高，此映射同样重要。RT-Thread有设备驱动框架，需要重构为IoT外设子系统方式。

| # | RT-Thread API | LiteOS-M API | 映射复杂度 | 注意事项 |
|---|--------------|-------------|-----------|---------|
| 1 | `rt_thread_create()` + `rt_thread_startup()` | `LOS_TaskCreate()` | 🟡 中 | RT-Thread分两步，LiteOS一步完成 |
| 2 | `rt_thread_mdelay()` | `LOS_TaskDelay()` | 🟡 中 | 毫秒→tick转换 |
| 3 | `rt_mutex_init()` | `LOS_MuxCreate()` | 🟢 低 | 去掉flag参数 |
| 4 | `rt_mutex_take()` | `LOS_MuxPend()` | 🟡 中 | RT_TICK_WAIT_FOREVER→LOS_WAIT_FOREVER |
| 5 | `rt_mutex_release()` | `LOS_MuxPost()` | 🟢 低 | 语义等价 |
| 6 | `rt_sem_init()` | `LOS_SemCreate()` | 🟢 低 | 去掉flag参数 |
| 7 | `rt_sem_take()` | `LOS_SemPend()` | 🟡 中 | 超时值转换 |
| 8 | `rt_sem_release()` | `LOS_SemPost()` | 🟢 低 | 语义等价 |
| 9 | `rt_mq_init/send/recv` | `LOS_QueueCreate/Write/Read` | 🟡 中 | ✅ LiteOS-M原生支持队列 |
| 10 | `rt_mb_init/send/recv` | 共享变量 + `LOS_SemCreate` | 🔴 高 | LiteOS-M无邮箱，需组合实现 |
| 11 | `rt_event_init/send/recv` | 原子变量 + `LOS_SemCreate` | 🔴 高 | LiteOS-M无事件集 |
| 12 | `rt_malloc/free()` | `LOS_MemAlloc/Free()` 或 `malloc/free` | 🟢 低 | 语义等价 |
| 13 | `rt_device_register()` | IoT组件注册 | 🔴 高 | **驱动模型重构**：从rt_device改为IoT外设组件 |
| 14 | `rt_kprintf()` | `printf()` / `dprintf()` | 🟢 低 | LiteOS-M直接使用printf |
| 15 | `rt_enter_critical()` | `LOS_IntLock()` | 🟡 中 | 注意嵌套计数差异 |
| 16 | `INIT_BOARD_EXPORT()` | 组件初始化函数注册 | 🔴 高 | 初始化机制完全不同 |
| 17 | `rt_hw_interrupt_install()` | `LOS_HwiCreate()` | 🟡 中 | 参数重组 |
| 18 | `rt_timer_create()` | `LOS_SwtmrCreate()` | 🟡 中 | 参数重组 |
| 19 | FinSH命令导出 | ❌ 无对应 | 🟡 中 | LiteOS-M有自己的Shell组件(可选) |

## 3. Linux → OSAL/HDF 映射表（仅L1小型系统适用）

> ⚠️ **注意**：Linux驱动迁移到OpenHarmony仅限于L1小型系统（LiteOS-A + 精简版HDF）。L0轻量系统不支持Linux驱动迁移。

| # | Linux API | HDF/OSAL API | 映射复杂度 | 注意事项 |
|---|----------|-------------|-----------|---------|
| 1 | `module_init()/module_exit()` | `HdfDriverEntry.Init/Release` | 🔴 高 | 驱动生命周期模型完全不同 |
| 2 | `platform_driver.probe()` | `HdfDriverEntry.Init()` | 🔴 高 | probe的资源获取需改为HCS读取 |
| 3 | `file_operations.open/release` | `IDeviceIoService.Open/Close`(可选) | 🟡 中 | HDF的Open/Close不是必须的 |
| 4 | `file_operations.read/write` | `Dispatch(CMD_READ/CMD_WRITE)` | 🔴 高 | 从文件语义转为消息分发语义 |
| 5 | `file_operations.unlocked_ioctl` | `Dispatch(cmdId)` | 🟡 中 | ioctl命令号映射为cmdId |
| 6 | `copy_to_user/copy_from_user` | `HdfSBufRead/HdfSBufWrite` | 🟡 中 | HDF使用序列化缓冲区 |
| 7 | `devm_kmalloc/kfree` | `OsalMemAlloc/Free` | 🟡 中 | 失去devm自动释放能力 |
| 8 | `ioremap/iounmap` | `OsalIoRemap/OsalIoUnmap`（osal_io.h 提供 static inline 封装） | 🟡 中 | OSAL已抽象，直接替换 |
| 9 | `readl/writel` | 平台相关 | 🟡 中 | MMIO访问通常保持不变 |
| 10 | `request_irq/free_irq` | `OsalRegisterIrq/OsalUnregisterIrq` | 🟡 中 | 参数重组 |
| 11 | `devm_request_irq` | `OsalRegisterIrq` + 手动管理 | 🟡 中 | 失去devm自动注销 |
| 12 | `mutex_init/lock/unlock` | `OsalMutexInit/Lock/Unlock` | 🟢 低 | 语义等价 |
| 13 | `spin_lock_irqsave` | `OsalSpinlockIrqSave` | 🟢 低 | 语义等价 |
| 14 | `kmalloc/kfree` | `OsalMemAlloc/OsalMemFree` | 🟢 低 | 语义等价 |
| 15 | `kzalloc` | `OsalMemCalloc(1, size)` | 🟢 低 | 语义等价 |
| 16 | `msleep/usleep_range` | `OsalSleep(ms)` | 🟡 中 | 微秒级睡眠精度降低 |
| 17 | `printk/dev_info/dev_err` | `HDF_LOGI/HDF_LOGE` | 🟢 低 | 增加TAG定义 |
| 18 | `of_property_read_u32` | `HdfReadDeviceMatchAttr` | 🟡 中 | DT属性→HCS属性 |
| 19 | `platform_get_resource` | HCS配置读取 | 🔴 高 | 资源获取方式完全不同 |
| 20 | `work_struct/schedule_work` | OsalThread + OsalSem | 🔴 高 | 工作队列需手动实现 |
| 21 | `wait_queue_head_t` | `OsalSem` | 🟡 中 | 等待队列→信号量 |
| 22 | `completion` | `OsalSemInit(sem, 0)` + `OsalSemWait/Post` | 🟡 中 | 语义近似 |
| 23 | `atomic_inc/dec/read` | `OsalAtomicInc/Dec/Read` | 🟢 低 | 语义等价 |
| 24 | `timer_setup/mod_timer` | `OsalTimerInit/Start` | 🟡 中 | 参数重组 |
| 25 | `sysfs/class/device_create` | HCS policy配置 | 🔴 高 | 用户空间接口模型完全不同 |

## 4. Zephyr → OSAL 映射表

| # | Zephyr API | OSAL API | 映射复杂度 | 注意事项 |
|---|-----------|----------|-----------|---------|
| 1 | `k_thread_create()` | `OsalThreadCreate()` + `OsalThreadStart()` | 🟡 中 | 栈分配方式不同 |
| 2 | `k_msleep()` | `OsalSleep()` | 🟢 低 | 语义等价 |
| 3 | `k_sem_take/give` | `OsalSemWait/Post` | 🟢 低 | 超时单位转换 |
| 4 | `k_mutex_lock/unlock` | `OsalMutexTimedLock/Unlock` | 🟢 低 | 语义等价 |
| 5 | `k_msgq_put/get` | 共享内存 + 信号量 | 🔴 高 | OSAL无消息队列 |
| 6 | `k_malloc/k_free` | `OsalMemAlloc/OsalMemFree` | 🟢 低 | 语义等价 |
| 7 | `k_timer_init/start` | `OsalTimerInit/Start` | 🟡 中 | 参数重组 |
| 8 | `DEVICE_DT_DEFINE()` | `HDF_INIT()` + HCS | 🔴 高 | **驱动模型重构** |
| 9 | `device_get_binding()` | HDF服务获取 | 🔴 高 | 设备查找机制不同 |
| 10 | `LOG_INF/ERR/WRN` | `HDF_LOGI/E/W` | 🟢 低 | 增加TAG |
| 11 | `IRQ_CONNECT()` | `OsalRegisterIrq()` | 🟡 中 | 从编译时绑定转为运行时注册 |
| 12 | `irq_lock/unlock` | `OsalSaveIrq/RestoreIrq` | 🟢 低 | 语义等价 |
| 13 | `atomic_*()` | `OsalAtomic*()` | 🟢 低 | 语义等价 |
| 14 | DT宏(`DT_PROP`, `DT_REG_ADDR`) | `HdfReadDeviceMatchAttr` | 🔴 高 | DT→HCS完全重构 |
| 15 | `k_work_init/submit` | OsalThread + OsalSem | 🔴 高 | 工作队列需手动实现 |
