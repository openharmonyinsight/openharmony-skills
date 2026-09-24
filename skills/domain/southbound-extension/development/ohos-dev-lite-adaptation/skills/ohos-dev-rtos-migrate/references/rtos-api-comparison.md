# 主流RTOS/Linux驱动模型详解

> 来源：需求5分析报告 §2

---

## 1. FreeRTOS

### 1.1 概述
FreeRTOS是Amazon维护的开源微内核RTOS，以极简、可裁剪著称。内核代码量仅约6KB~12KB，支持40+种处理器架构。

### 1.2 核心API清单

**任务管理 (Task Management)**
```c
// 创建任务
BaseType_t xTaskCreate(
    TaskFunction_t pvTaskCode,    // 任务函数
    const char *pcName,           // 任务名称
    configSTACK_DEPTH_TYPE usStackDepth, // 栈大小(word)
    void *pvParameters,           // 参数
    UBaseType_t uxPriority,       // 优先级
    TaskHandle_t *pxCreatedTask   // 任务句柄
);

// 删除任务
void vTaskDelete(TaskHandle_t xTaskToDelete);

// 延时
void vTaskDelay(const TickType_t xTicksToDelay);
void vTaskDelayUntil(TickType_t *pxPreviousWakeTime, const TickType_t xTimeIncrement);

// 任务通知
BaseType_t xTaskNotifyGive(TaskHandle_t xTaskToNotify);
uint32_t ulTaskNotifyTake(BaseType_t xClearCountOnExit, TickType_t xTicksToWait);
BaseType_t xTaskNotify(TaskHandle_t xTaskToNotify, uint32_t ulValue, eNotifyAction eAction);

// 挂起/恢复
void vTaskSuspend(TaskHandle_t xTaskToSuspend);
void vTaskResume(TaskHandle_t xTaskToResume);
```

**队列 (Queue)**
```c
QueueHandle_t xQueueCreate(UBaseType_t uxQueueLength, UBaseType_t uxItemSize);
BaseType_t xQueueSend(QueueHandle_t xQueue, const void *pvItemToQueue, TickType_t xTicksToWait);
BaseType_t xQueueReceive(QueueHandle_t xQueue, void *pvBuffer, TickType_t xTicksToWait);
BaseType_t xQueueSendFromISR(QueueHandle_t xQueue, const void *pvItemToQueue, BaseType_t *pxHigherPriorityTaskWoken);
BaseType_t xQueueReceiveFromISR(QueueHandle_t xQueue, void *pvBuffer, BaseType_t *pxHigherPriorityTaskWoken);
UBaseType_t uxQueueMessagesWaiting(const QueueHandle_t xQueue);
void vQueueDelete(QueueHandle_t xQueue);
```

**信号量与互斥锁 (Semaphore & Mutex)**
```c
// 二值信号量
SemaphoreHandle_t xSemaphoreCreateBinary(void);
// 计数信号量
SemaphoreHandle_t xSemaphoreCreateCounting(UBaseType_t uxMaxCount, UBaseType_t uxInitialCount);
// 互斥锁
SemaphoreHandle_t xSemaphoreCreateMutex(void);
// 递归互斥锁
SemaphoreHandle_t xSemaphoreCreateRecursiveMutex(void);

BaseType_t xSemaphoreTake(SemaphoreHandle_t xSemaphore, TickType_t xBlockTime);
BaseType_t xSemaphoreGive(SemaphoreHandle_t xSemaphore);
BaseType_t xSemaphoreTakeFromISR(SemaphoreHandle_t xSemaphore, BaseType_t *pxHigherPriorityTaskWoken);
BaseType_t xSemaphoreGiveFromISR(SemaphoreHandle_t xSemaphore, BaseType_t *pxHigherPriorityTaskWoken);
```

**软件定时器 (Software Timer)**
```c
TimerHandle_t xTimerCreate(
    const char *pcTimerName,
    const TickType_t xTimerPeriodInTicks,
    const UBaseType_t uxAutoReload,
    void *pvTimerID,
    TimerCallbackFunction_t pxCallbackFunction
);
BaseType_t xTimerStart(TimerHandle_t xTimer, TickType_t xBlockTime);
BaseType_t xTimerStop(TimerHandle_t xTimer, TickType_t xBlockTime);
BaseType_t xTimerReset(TimerHandle_t xTimer, TickType_t xBlockTime);
BaseType_t xTimerChangePeriod(TimerHandle_t xTimer, TickType_t xNewPeriod, TickType_t xBlockTime);
void *pvTimerGetTimerID(TimerHandle_t xTimer);
```

**内存管理**
```c
// heap_1: 只分配不释放
// heap_2: 固定块大小分配
// heap_3: 包装标准C库malloc/free
// heap_4: 首次适配合并算法（最常用）
// heap_5: 非连续RAM区域支持
void *pvPortMalloc(size_t xWantedSize);
void vPortFree(void *pv);
size_t xPortGetFreeHeapSize(void);
size_t xPortGetMinimumEverFreeHeapSize(void);
```

**中断管理**
```c
// FreeRTOS没有统一的中断注册API，由各端口(Port)提供
// 典型模式：
void NVIC_EnableIRQ(IRQn_Type IRQn);           // ARM Cortex-M
void HAL_NVIC_SetPriority(IRQn_Type IRQn, ...); // STM32 HAL

// ISR中使用FromISR后缀的安全API
BaseType_t xSemaphoreGiveFromISR(...);
BaseType_t xQueueSendFromISR(...);
// 并通过pxHigherPriorityTaskWoken参数触发上下文切换
portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
```

### 1.3 驱动开发模式
FreeRTOS **没有内置驱动框架**，驱动通常以以下方式组织：
- **裸机HAL + RTOS封装**：底层用芯片厂商HAL（如STM32 HAL），上层用FreeRTOS原语做线程安全封装
- **回调+ISR模式**：中断中设置标志或发送信号量，任务中轮询或等待
- **无设备模型**：每个驱动自行管理初始化、读写、关闭流程

```c
// 典型的FreeRTOS UART驱动模式
static SemaphoreHandle_t uart_mutex;
static QueueHandle_t uart_rx_queue;

void uart_driver_init(void) {
    uart_mutex = xSemaphoreCreateMutex();
    uart_rx_queue = xQueueCreate(256, sizeof(uint8_t));
    HAL_UART_Init(&huart1);
    HAL_UART_Receive_IT(&huart1, rx_buf, 1);
}

int uart_write(const uint8_t *data, size_t len) {
    if (xSemaphoreTake(uart_mutex, pdMS_TO_TICKS(1000)) != pdTRUE)
        return -1;
    HAL_UART_Transmit(&huart1, data, len, 1000);
    xSemaphoreGive(uart_mutex);
    return len;
}

void USART1_IRQHandler(void) {
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    uint8_t byte = huart1.Instance->RDR;
    xQueueSendFromISR(uart_rx_queue, &byte, &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}
```

## 2. RT-Thread

### 2.1 概述
RT-Thread是国内开源的IoT RTOS，具有完整的组件生态（DFS文件系统、网络协议栈、设备驱动框架、FinSH Shell、OTA等）。分为标准版和Nano版。

### 2.2 核心API清单

**线程管理 (Thread)**
```c
rt_thread_t rt_thread_create(const char *name, void (*entry)(void *param),
                              void *param, rt_uint32_t stack_size,
                              rt_uint8_t priority, rt_uint32_t tick);
rt_err_t rt_thread_startup(rt_thread_t thread);
rt_err_t rt_thread_delete(rt_thread_t thread);
rt_err_t rt_thread_delay(rt_tick_t tick);
rt_err_t rt_thread_mdelay(rt_int32_t ms);
rt_err_t rt_thread_yield(void);
rt_err_t rt_thread_suspend(rt_thread_t thread);
rt_err_t rt_thread_resume(rt_thread_t thread);
rt_thread_t rt_thread_self(void);
rt_err_t rt_thread_control(rt_thread_t thread, int cmd, void *arg);
```

**IPC机制**
```c
// 信号量
rt_err_t rt_sem_init(rt_sem_t sem, const char *name, rt_uint32_t value, rt_uint8_t flag);
rt_err_t rt_sem_take(rt_sem_t sem, rt_int32_t time);
rt_err_t rt_sem_release(rt_sem_t sem);

// 互斥量
rt_err_t rt_mutex_init(rt_mutex_t mutex, const char *name, rt_uint8_t flag);
rt_err_t rt_mutex_take(rt_mutex_t mutex, rt_int32_t time);
rt_err_t rt_mutex_release(rt_mutex_t mutex);

// 消息队列
rt_err_t rt_mq_init(rt_mq_t mq, const char *name, void *msgpool,
                     rt_size_t msg_size, rt_size_t pool_size, rt_uint8_t flag);
rt_err_t rt_mq_send(rt_mq_t mq, const void *buffer, rt_size_t size);
rt_err_t rt_mq_recv(rt_mq_t mq, void *buffer, rt_size_t size, rt_int32_t timeout);

// 邮箱
rt_err_t rt_mb_init(rt_mailbox_t mb, const char *name, void *msgpool,
                     rt_size_t size, rt_uint8_t flag);
rt_err_t rt_mb_send(rt_mailbox_t mb, rt_ubase_t value);
rt_err_t rt_mb_recv(rt_mailbox_t mb, rt_ubase_t *value, rt_int32_t timeout);

// 事件集
rt_err_t rt_event_init(rt_event_t event, const char *name, rt_uint8_t flag);
rt_err_t rt_event_send(rt_event_t event, rt_uint32_t set);
rt_err_t rt_event_recv(rt_event_t event, rt_uint32_t set, rt_uint8_t opt,
                        rt_int32_t timeout, rt_uint32_t *recved);
```

**设备驱动框架 (Device Framework)**
```c
// RT-Thread的设备驱动框架是其核心特色
struct rt_device {
    struct rt_object parent;
    enum rt_device_class_type type;
    const struct rt_device_ops *ops;
    rt_err_t (*init)(rt_device_t dev);
    rt_err_t (*open)(rt_device_t dev, rt_uint16_t oflag);
    rt_err_t (*close)(rt_device_t dev);
    rt_size_t (*read)(rt_device_t dev, rt_off_t pos, void *buffer, rt_size_t size);
    rt_size_t (*write)(rt_device_t dev, rt_off_t pos, const void *buffer, rt_size_t size);
    rt_err_t (*control)(rt_device_t dev, int cmd, void *args);
    // ...
};

rt_err_t rt_device_register(rt_device_t dev, const char *name, rt_uint16_t flags);
rt_device_t rt_device_find(const char *name);
rt_err_t rt_device_init(rt_device_t dev);
rt_err_t rt_device_open(rt_device_t dev, rt_uint16_t oflag);
rt_err_t rt_device_close(rt_device_t dev);
rt_size_t rt_device_read(rt_device_t dev, rt_off_t pos, void *buffer, rt_size_t size);
rt_size_t rt_device_write(rt_device_t dev, rt_off_t pos, const void *buffer, rt_size_t size);
rt_err_t rt_device_control(rt_device_t dev, int cmd, void *arg);
```

**内存管理**
```c
void *rt_malloc(rt_size_t nbytes);
void rt_free(void *ptr);
void *rt_realloc(void *ptr, rt_size_t nbytes);
void *rt_calloc(rt_size_t count, rt_size_t size);
void *rt_page_alloc(rt_size_t npages);  // 页分配器
```

**FinSH Shell**
```c
// FinSH提供交互式命令行调试
MSH_CMD_EXPORT(command_func, description);   // 导出msh命令
FINSH_FUNCTION_EXPORT(func, desc);           // 导出finsh C表达式命令
FINSH_VAR_EXPORT(name, type, desc);          // 导出变量
```

### 2.3 驱动开发模式
RT-Thread有完善的**设备驱动框架**，驱动通过`rt_device`结构体注册：

```c
// RT-Thread GPIO驱动示例
static rt_err_t gpio_init(rt_device_t dev) {
    hal_gpio_init();
    return RT_EOK;
}

static rt_size_t gpio_read(rt_device_t dev, rt_off_t pos, void *buffer, rt_size_t size) {
    uint32_t pin = pos;
    *((uint8_t *)buffer) = hal_gpio_read(pin);
    return 1;
}

static rt_size_t gpio_write(rt_device_t dev, rt_off_t pos, const void *buffer, rt_size_t size) {
    uint32_t pin = pos;
    hal_gpio_write(pin, *((const uint8_t *)buffer));
    return 1;
}

static rt_err_t gpio_control(rt_device_t dev, int cmd, void *args) {
    switch (cmd) {
        case GPIO_CMD_SET_DIR:
            hal_gpio_set_direction(*(uint32_t *)args >> 16, *(uint32_t *)args & 0xFF);
            break;
        default:
            return -RT_ERROR;
    }
    return RT_EOK;
}

int rt_hw_gpio_init(void) {
    static struct rt_device gpio_dev;
    gpio_dev.init = gpio_init;
    gpio_dev.read = gpio_read;
    gpio_dev.write = gpio_write;
    gpio_dev.control = gpio_control;
    rt_device_register(&gpio_dev, "gpio", RT_DEVICE_FLAG_RDWR);
    return 0;
}
INIT_BOARD_EXPORT(rt_hw_gpio_init);
```

## 3. Zephyr

### 3.1 概述
Zephyr由Linux基金会托管，采用Apache 2.0许可证。其最大特点是**深度集成DeviceTree**作为硬件描述机制，驱动与硬件配置完全解耦。

### 3.2 核心API清单

**线程管理**
```c
K_THREAD_DEFINE(name, stack_size, entry, p1, p2, p3, prio, options, delay);
k_tid_t k_thread_create(struct k_thread *new_thread, k_thread_stack_t *stack,
                         size_t stack_size, k_thread_entry_t entry,
                         void *p1, void *p2, void *p3,
                         int prio, uint32_t options, k_timeout_t delay);
void k_thread_abort(k_tid_t thread);
void k_sleep(k_timeout_t timeout);
void k_msleep(int32_t ms);
void k_yield(void);
void k_thread_priority_set(k_tid_t thread, int prio);
```

**同步原语**
```c
// 信号量
K_SEM_DEFINE(name, initial_count, limit);
int k_sem_take(struct k_sem *sem, k_timeout_t timeout);
void k_sem_give(struct k_sem *sem);
void k_sem_reset(struct k_sem *sem);

// 互斥锁
K_MUTEX_DEFINE(name);
int k_mutex_lock(struct k_mutex *mutex, k_timeout_t timeout);
int k_mutex_unlock(struct k_mutex *mutex);

// 消息队列
K_MSGQ_DEFINE(name, msg_sz, max_msgs, align);
int k_msgq_put(struct k_msgq *q, const void *data, k_timeout_t timeout);
int k_msgq_get(struct k_msgq *q, void *data, k_timeout_t timeout);
```

**设备驱动模型 (Device Model)**
```c
// Zephyr的设备模型紧密绑定DeviceTree
#define DEVICE_DT_GET(node_id)      // 从DT节点获取设备
#define DEVICE_DT_INST_GET(inst)    // 从DT实例获取设备

// 驱动API通过api指针实现多态
struct device {
    const char *name;
    const void *config;     // DT-derived静态配置
    const void *api;        // 驱动API函数表
    void *data;             // 运行时数据
};

// 设备声明宏
DEVICE_DT_DEFINE(node_id, init_fn, pm_device, data, config, level, prio, api, ...);
DEVICE_DT_INST_DEFINE(inst, init_fn, pm_device, data, config, level, prio, api, ...);
```

**DeviceTree绑定**
```dts
/* Zephyr DeviceTree overlay示例 */
&i2c0 {
    status = "okay";
    bme280@76 {
        compatible = "bosch,bme280";
        reg = <0x76>;
        label = "BME280";
    };
};
```

## 4. uC/OS-II / uC/OS-III

### 4.1 概述
Micrium开发的商业RTOS（现已开源），以代码质量和文档完善著称。uC/OS-III增加了无限优先级数、时间片轮转、运行时测量等特性。

### 4.2 核心API
```c
// 任务管理
void OSTaskCreate(OS_TCB *p_tcb, CPU_CHAR *p_name, OS_TASK_PTR p_task,
                   void *p_arg, OS_PRIO prio, CPU_STK *p_stk_base,
                   CPU_STK_SIZE stk_limit, CPU_STK_SIZE stk_size,
                   OS_MSG_QTY q_size, OS_TICK time_quanta,
                   void *p_ext, OS_OPT opt, OS_ERR *p_err);
void OSTaskDel(OS_TCB *p_tcb, OS_ERR *p_err);
void OSTimeDly(OS_TICK dly, OS_OPT opt, OS_ERR *p_err);

// 信号量
void OSSemCreate(OS_SEM *p_sem, CPU_CHAR *p_name, OS_SEM_CTR cnt, OS_ERR *p_err);
OS_SEM_CTR OSSemPend(OS_SEM *p_sem, OS_TICK timeout, OS_OPT opt,
                      CPU_TS *p_ts, OS_ERR *p_err);
void OSSemPost(OS_SEM *p_sem, OS_OPT opt, OS_ERR *p_err);

// 互斥锁
void OSMutexCreate(OS_MUTEX *p_mutex, CPU_CHAR *p_name, OS_ERR *p_err);
void OSMutexPend(OS_MUTEX *p_mutex, OS_TICK timeout, OS_OPT opt,
                  CPU_TS *p_ts, OS_ERR *p_err);
void OSMutexPost(OS_MUTEX *p_mutex, OS_OPT opt, OS_ERR *p_err);

// 消息队列
void OSQCreate(OS_Q *p_q, CPU_CHAR *p_name, OS_MSG_QTY max_qty, OS_ERR *p_err);
void OSQPost(OS_Q *p_q, void *p_void, OS_MSG_SIZE msg_size, OS_OPT opt, OS_ERR *p_err);
void *OSQPend(OS_Q *p_q, OS_TICK timeout, OS_OPT opt, OS_MSG_SIZE *p_msg_size,
              CPU_TS *p_ts, OS_ERR *p_err);
```

## 5. VxWorks

### 5.1 概述
Wind River的商业RTOS，是航空航天、国防、医疗、工业自动化领域的标杆。支持POSIX兼容API、实时进程模型、丰富的中间件。

### 5.2 核心API
```c
// 任务管理 (原生API)
TASK_ID taskSpawn(char *name, int priority, int options, int stackSize,
                  FUNCPTR entryPt, int arg1, ..., int arg10);
STATUS taskDelete(TASK_ID tid);
void taskDelay(int ticks);

// POSIX兼容API
int pthread_create(pthread_t *thread, const pthread_attr_t *attr,
                   void *(*start_routine)(void *), void *arg);
int pthread_join(pthread_t thread, void **retval);
int sem_init(sem_t *sem, int pshared, unsigned int value);
int sem_wait(sem_t *sem);
int sem_post(sem_t *sem);
int pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr);
int pthread_mutex_lock(pthread_mutex_t *mutex);
int pthread_mutex_unlock(pthread_mutex_t *mutex);

// 消息队列
MSG_Q_ID msgQCreate(int maxMsgs, int maxMsgLen, int options);
STATUS msgQSend(MSG_Q_ID msgQId, char *buffer, UINT nBytes, int timeout, int priority);
STATUS msgQReceive(MSG_Q_ID msgQId, char *buffer, UINT maxNBytes, int timeout);
```

## 6. Linux驱动模型

### 6.1 字符设备驱动
```c
// Linux字符设备驱动核心结构
static struct file_operations my_fops = {
    .owner   = THIS_MODULE,
    .open    = my_open,
    .release = my_release,
    .read    = my_read,
    .write   = my_write,
    .unlocked_ioctl = my_ioctl,
    .poll    = my_poll,
    .mmap    = my_mmap,
};

static int __init my_init(void) {
    dev_t dev_num;
    alloc_chrdev_region(&dev_num, 0, 1, "mydev");
    cdev_init(&my_cdev, &my_fops);
    cdev_add(&my_cdev, dev_num, 1);
    my_class = class_create(THIS_MODULE, "myclass");
    device_create(my_class, NULL, dev_num, NULL, "mydev");
    return 0;
}

static long my_ioctl(struct file *filp, unsigned int cmd, unsigned long arg) {
    switch (cmd) {
        case MY_CMD_READ_REG:
            // ...
            break;
        case MY_CMD_WRITE_REG:
            // ...
            break;
    }
    return 0;
}
```

### 6.2 Platform设备驱动
```c
// Linux Platform驱动模型
static const struct of_device_id my_of_match[] = {
    { .compatible = "vendor,my-device" },
    { /* sentinel */ }
};
MODULE_DEVICE_TABLE(of, my_of_match);

static int my_probe(struct platform_device *pdev) {
    struct resource *res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
    void __iomem *base = devm_ioremap_resource(&pdev->dev, res);
    int irq = platform_get_irq(pdev, 0);
    devm_request_irq(&pdev->dev, irq, my_isr, IRQF_SHARED, "my-dev", priv);
    // ...
    return 0;
}

static struct platform_driver my_driver = {
    .probe  = my_probe,
    .remove = my_remove,
    .driver = {
        .name = "my-device",
        .of_match_table = my_of_match,
    },
};
module_platform_driver(my_driver);
```

### 6.3 中断处理
```c
// Linux中断处理
static irqreturn_t my_isr(int irq, void *dev_id) {
    struct my_priv *priv = dev_id;
    uint32_t status = ioread32(priv->base + STATUS_REG);
    if (status & INT_FLAG) {
        // 顶半部：快速处理
        iowrite32(status, priv->base + STATUS_CLR_REG);
        schedule_work(&priv->work);  // 底半部：延迟处理
        return IRQ_HANDLED;
    }
    return IRQ_NONE;
}

// 注册
request_irq(irq, my_isr, IRQF_TRIGGER_RISING | IRQF_SHARED, "my-dev", priv);
// 或使用managed版本
devm_request_irq(dev, irq, my_isr, flags, name, priv);
```
