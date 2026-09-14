# 迁移案例与最佳实践

---

## 1. 案例一：FreeRTOS UART驱动 → LiteOS-M UART驱动（L0轻量系统）

### 源代码 (FreeRTOS)
```c
/* freertos_uart.c - FreeRTOS UART Driver */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"
#include "queue.h"
#include "stm32f4xx_hal.h"

static SemaphoreHandle_t uart_tx_mutex;
static QueueHandle_t uart_rx_queue;
static volatile uint8_t rx_byte;

void uart_init(void) {
    uart_tx_mutex = xSemaphoreCreateMutex();
    uart_rx_queue = xQueueCreate(512, sizeof(uint8_t));
    
    UART_HandleTypeDef huart;
    huart.Instance = USART2;
    huart.Init.BaudRate = 115200;
    huart.Init.WordLength = UART_WORDLENGTH_8B;
    huart.Init.StopBits = UART_STOPBITS_1;
    huart.Init.Parity = UART_PARITY_NONE;
    HAL_UART_Init(&huart);
    HAL_UART_Receive_IT(&huart, &rx_byte, 1);
}

int uart_send(const uint8_t *data, uint32_t len, uint32_t timeout_ms) {
    if (xSemaphoreTake(uart_tx_mutex, pdMS_TO_TICKS(timeout_ms)) != pdTRUE) {
        return -1;
    }
    HAL_StatusTypeDef status = HAL_UART_Transmit(&huart, data, len, timeout_ms);
    xSemaphoreGive(uart_tx_mutex);
    return (status == HAL_OK) ? (int)len : -1;
}

int uart_recv(uint8_t *buf, uint32_t len, uint32_t timeout_ms) {
    uint32_t received = 0;
    TickType_t start = xTaskGetTickCount();
    while (received < len) {
        uint8_t byte;
        TickType_t remaining = pdMS_TO_TICKS(timeout_ms) - (xTaskGetTickCount() - start);
        if (xQueueReceive(uart_rx_queue, &byte, remaining) != pdTRUE) {
            break;
        }
        buf[received++] = byte;
    }
    return received;
}

void USART2_IRQHandler(void) {
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    if (__HAL_UART_GET_FLAG(&huart, UART_FLAG_RXNE)) {
        uint8_t byte = huart.Instance->DR;
        xQueueSendFromISR(uart_rx_queue, &byte, &xHigherPriorityTaskWoken);
        HAL_UART_Receive_IT(&huart, &rx_byte, 1);
    }
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}
```

### 转换后 (LiteOS-M，IoT外设子系统方式 — L0)
```c
/* liteos_m_uart.c - OpenHarmony LiteOS-M UART Driver (L0 IoT外设方式) */
#include "los_task.h"         /* ⭐ LiteOS-M内核API，非OSAL */
#include "los_mux.h"
#include "los_queue.h"
#include "los_hwi.h"
#include "uart_if.h"          /* OpenHarmony UART HAL接口 */
#include "hal_uart.h"         /* 芯片厂商UART HAL */

static UINT32 uart_tx_mux;
static UINT32 uart_rx_queue;
static volatile uint8_t rx_byte;

/* 初始化函数 — 通过IoT组件注册机制调用 */
int uart_driver_init(void)
{
    /* 创建互斥锁 (替代xSemaphoreCreateMutex) */
    LOS_MuxCreate(&uart_tx_mux);
    
    /* 创建消息队列 (替代xQueueCreate) — ✅ LiteOS-M原生支持! */
    LOS_QueueCreate("uart_rx", 512, &uart_rx_queue, 0, sizeof(uint8_t));
    
    /* 硬件初始化 */
    hal_uart_init(UART_PORT_2, 115200);
    hal_uart_receive_it(UART_PORT_2, &rx_byte, 1);
    
    printf("UART driver initialized\n");
    return 0;
}

int uart_send(const uint8_t *data, uint32_t len, uint32_t timeout_ms)
{
    /* LOS_MuxPend替代xSemaphoreTake */
    if (LOS_MuxPend(uart_tx_mux, timeout_ms) != LOS_OK) {
        return -1;
    }
    int ret = hal_uart_transmit(UART_PORT_2, data, len, timeout_ms);
    LOS_MuxPost(uart_tx_mux);
    return ret;
}

int uart_recv(uint8_t *buf, uint32_t len, uint32_t timeout_ms)
{
    uint32_t received = 0;
    UINT32 tickStart = LOS_TickCountGet();
    while (received < len) {
        uint8_t byte;
        UINT32 elapsed = LOS_TickCountGet() - tickStart;
        UINT32 remaining = (timeout_ms > elapsed) ? (timeout_ms - elapsed) : 0;
        /* LOS_QueueRead替代xQueueReceive */
        if (LOS_QueueRead(uart_rx_queue, &byte, sizeof(byte), remaining) != LOS_OK) {
            break;
        }
        buf[received++] = byte;
    }
    return received;
}

/* ISR处理 — 使用LiteOS-M中断管理 */
void USART2_IRQHandler(void)
{
    if (hal_uart_get_flag(UART_PORT_2, UART_FLAG_RXNE)) {
        uint8_t byte = hal_uart_read_data(UART_PORT_2);
        /* ISR中使用非阻塞写入 */
        LOS_QueueWrite(uart_rx_queue, &byte, sizeof(byte), 0);
        hal_uart_receive_it(UART_PORT_2, &rx_byte, 1);
    }
}
```

> ⚠️ **关键变化**：
> 1. FreeRTOS API → LiteOS-M内核API（非OSAL）
> 2. `xQueueCreate` → `LOS_QueueCreate`（LiteOS-M原生支持队列！不需要手写RingBuffer）
> 3. 栈大小单位从word变为byte
> 4. 优先级数值含义可能相反
> 5. Tick频率需确认一致

## 2. 案例二：RT-Thread GPIO驱动 → LiteOS-M GPIO驱动（L0轻量系统）

### 源代码 (RT-Thread)
```c
/* rt_gpio.c - RT-Thread GPIO Driver */
#include <rtthread.h>
#include <rtdevice.h>
#include "board.h"
#include "hal_gpio.h"

#define GPIO_PIN_COUNT 32

static rt_err_t rt_gpio_init(rt_device_t dev) {
    hal_gpio_clock_enable();
    for (int i = 0; i < GPIO_PIN_COUNT; i++) {
        hal_gpio_set_direction(i, GPIO_DIR_INPUT);
    }
    rt_kprintf("GPIO driver initialized\n");
    return RT_EOK;
}

static rt_size_t rt_gpio_read(rt_device_t dev, rt_off_t pos, void *buffer, rt_size_t size) {
    if (pos >= GPIO_PIN_COUNT) return 0;
    uint8_t val = hal_gpio_read(pos);
    *((uint8_t *)buffer) = val;
    return 1;
}

static rt_size_t rt_gpio_write(rt_device_t dev, rt_off_t pos, const void *buffer, rt_size_t size) {
    if (pos >= GPIO_PIN_COUNT) return 0;
    hal_gpio_write(pos, *((const uint8_t *)buffer));
    return 1;
}

static rt_err_t rt_gpio_control(rt_device_t dev, int cmd, void *args) {
    switch (cmd) {
        case 0x01: /* SET_DIRECTION */
            hal_gpio_set_direction(((uint32_t *)args)[0], ((uint32_t *)args)[1]);
            break;
        case 0x02: /* SET_PULL */
            hal_gpio_set_pull(((uint32_t *)args)[0], ((uint32_t *)args)[1]);
            break;
        case 0x03: /* ENABLE_IRQ */
            hal_gpio_irq_enable(((uint32_t *)args)[0], ((uint32_t *)args)[1]);
            break;
        default:
            return -RT_ERROR;
    }
    return RT_EOK;
}

static int rt_hw_gpio_init(void) {
    static struct rt_device gpio_device;
    gpio_device.type = RT_Device_Class_Miscellaneous;
    gpio_device.init = rt_gpio_init;
    gpio_device.read = rt_gpio_read;
    gpio_device.write = rt_gpio_write;
    gpio_device.control = rt_gpio_control;
    rt_device_register(&gpio_device, "gpio", RT_DEVICE_FLAG_RDWR);
    return 0;
}
INIT_BOARD_EXPORT(rt_hw_gpio_init);
```

### 转换后 (LiteOS-M，IoT外设子系统方式 — L0)
```c
/* liteos_m_gpio.c - OpenHarmony LiteOS-M GPIO Driver (L0 IoT外设方式) */
#include "los_task.h"         /* ⭐ LiteOS-M内核API */
#include "gpio_if.h"          /* OpenHarmony GPIO HAL接口 */
#include "hal_gpio.h"         /* 芯片厂商HAL */

#define GPIO_PIN_COUNT 32

/* 初始化函数 — 通过IoT组件注册机制调用（替代INIT_BOARD_EXPORT） */
int gpio_driver_init(void)
{
    hal_gpio_clock_enable();
    for (int i = 0; i < GPIO_PIN_COUNT; i++) {
        hal_gpio_set_direction(i, GPIO_DIR_INPUT);
    }
    printf("GPIO driver initialized\n");  /* 替代rt_kprintf */
    return 0;
}

/* 直接函数调用接口（替代rt_device read/write/control模式） */
int gpio_hal_read(uint32_t pin, uint8_t *val)
{
    if (pin >= GPIO_PIN_COUNT) return -1;
    *val = hal_gpio_read(pin);
    return 0;
}

int gpio_hal_write(uint32_t pin, uint8_t val)
{
    if (pin >= GPIO_PIN_COUNT) return -1;
    hal_gpio_write(pin, val);
    return 0;
}

int gpio_hal_set_dir(uint32_t pin, uint8_t dir)
{
    hal_gpio_set_direction(pin, dir);
    return 0;
}

int gpio_hal_set_pull(uint32_t pin, uint8_t pull)
{
    hal_gpio_set_pull(pin, pull);
    return 0;
}

int gpio_hal_enable_irq(uint32_t pin, uint8_t trigger)
{
    hal_gpio_irq_enable(pin, trigger);
    return 0;
}
```

> ⚠️ **关键变化**：
> 1. `rt_device_register` → IoT组件注册（直接函数调用）
> 2. `rt_kprintf` → `printf`
> 3. `INIT_BOARD_EXPORT` → 组件初始化函数列表
> 4. 去掉了rt_device的read/write/control多态模式，改为直接函数接口
> 5. 不再需要rtthread.h和rtdevice.h头文件

## 3. 案例三：Linux Platform驱动 → HDF驱动（仅L1小型系统）

> ⚠️ **注意**：此案例仅适用于L1小型系统（LiteOS-A + 精简版HDF）。L0轻量系统不支持Linux驱动迁移。

### 源代码 (Linux)
```c
/* linux_sensor.c - Linux I2C Sensor Driver */
#include <linux/module.h>
#include <linux/i2c.h>
#include <linux/of.h>
#include <linux/mutex.h>
#include <linux/delay.h>

struct sensor_data {
    struct i2c_client *client;
    struct mutex lock;
    uint16_t chip_id;
    bool powered;
};

static int sensor_read_reg(struct sensor_data *data, uint8_t reg, uint8_t *val) {
    int ret = i2c_smbus_read_byte_data(data->client, reg);
    if (ret < 0) return ret;
    *val = ret;
    return 0;
}

static int sensor_probe(struct i2c_client *client, const struct i2c_device_id *id) {
    struct sensor_data *data = devm_kzalloc(&client->dev, sizeof(*data), GFP_KERNEL);
    if (!data) return -ENOMEM;
    
    data->client = client;
    mutex_init(&data->lock);
    
    uint8_t chip_id;
    int ret = sensor_read_reg(data, 0x00, &chip_id);
    if (ret || chip_id != 0x60) {
        dev_err(&client->dev, "chip id mismatch: 0x%02x\n", chip_id);
        return -ENODEV;
    }
    data->chip_id = chip_id;
    
    i2c_set_clientdata(client, data);
    dev_info(&client->dev, "sensor probed, chip_id=0x%02x\n", chip_id);
    return 0;
}

static const struct of_device_id sensor_of_match[] = {
    { .compatible = "vendor,sensor-x" },
    { }
};
MODULE_DEVICE_TABLE(of, sensor_of_match);

static struct i2c_driver sensor_driver = {
    .driver = {
        .name = "sensor-x",
        .of_match_table = sensor_of_match,
    },
    .probe = sensor_probe,
};
module_i2c_driver(sensor_driver);
```

### 转换后 (HDF)
```c
/* hdf_sensor_driver.c - OpenHarmony HDF Sensor Driver */
#include "hdf_device_desc.h"
#include "hdf_log.h"
#include "osal_mem.h"
#include "osal_mutex.h"
#include "i2c_if.h"

#define HDF_LOG_TAG hdf_sensor
#define SENSOR_CHIP_ID_REG  0x00
#define SENSOR_EXPECTED_ID  0x60

struct SensorDriverData {
    DevHandle i2cHandle;
    OsalMutex lock;
    uint16_t chipId;
    uint16_t i2cAddr;
    uint16_t busNum;
};

static int32_t SensorReadReg(struct SensorDriverData *data, uint8_t reg, uint8_t *val)
{
    uint8_t writeBuf = reg;
    uint8_t readBuf = 0;
    struct I2cMsg msgs[2] = {
        { .addr = data->i2cAddr, .flags = 0, .len = 1, .buf = &writeBuf },
        { .addr = data->i2cAddr, .flags = I2C_FLAG_READ, .len = 1, .buf = &readBuf },
    };
    int32_t ret = I2cTransfer(data->i2cHandle, msgs, 2);
    if (ret != 2) {
        return HDF_FAILURE;
    }
    *val = readBuf;
    return HDF_SUCCESS;
}

static int32_t HdfSensorBind(struct HdfDeviceObject *device)
{
    static struct IDeviceIoService ioService = {
        .Dispatch = HdfSensorDispatch,
    };
    device->service = &ioService;
    return HDF_SUCCESS;
}

static int32_t HdfSensorInit(struct HdfDeviceObject *device)
{
    struct SensorDriverData *data = (struct SensorDriverData *)OsalMemCalloc(1, sizeof(*data));
    if (data == NULL) {
        return HDF_ERR_MALLOC_FAIL;
    }
    
    /* 从HCS读取配置 (替代of_property_read) */
    const struct DeviceResourceNode *node = device->property;
    HdfReadDeviceMatchAttr(node, "i2c_bus_num", &data->busNum);
    HdfReadDeviceMatchAttr(node, "i2c_addr", &data->i2cAddr);
    
    /* 初始化互斥锁 (替代mutex_init) */
    if (OsalMutexInit(&data->lock) != HDF_SUCCESS) {
        OsalMemFree(data);
        return HDF_FAILURE;
    }
    
    /* 打开I2C总线 (替代i2c_client) */
    data->i2cHandle = I2cOpen(data->busNum);
    if (data->i2cHandle == NULL) {
        HDF_LOGE("%s: I2cOpen(%u) failed", __func__, data->busNum);
        OsalMutexDestroy(&data->lock);
        OsalMemFree(data);
        return HDF_FAILURE;
    }
    
    /* 验证芯片ID */
    uint8_t chipId = 0;
    if (SensorReadReg(data, SENSOR_CHIP_ID_REG, &chipId) != HDF_SUCCESS ||
        chipId != SENSOR_EXPECTED_ID) {
        HDF_LOGE("%s: chip id mismatch: 0x%02x", __func__, chipId);
        I2cClose(data->i2cHandle);
        OsalMutexDestroy(&data->lock);
        OsalMemFree(data);
        return HDF_FAILURE;
    }
    data->chipId = chipId;
    
    device->priv = data;
    HDF_LOGI("%s: sensor probed, chip_id=0x%02x", __func__, chipId);
    return HDF_SUCCESS;
}

static void HdfSensorRelease(struct HdfDeviceObject *device)
{
    struct SensorDriverData *data = (struct SensorDriverData *)device->priv;
    if (data) {
        I2cClose(data->i2cHandle);
        OsalMutexDestroy(&data->lock);
        OsalMemFree(data);
    }
}

struct HdfDriverEntry g_sensorDriverEntry = {
    .moduleVersion = 1,
    .moduleName = "SENSOR_X_DRIVER",
    .Bind = HdfSensorBind,
    .Init = HdfSensorInit,
    .Release = HdfSensorRelease,
};
HDF_INIT(g_sensorDriverEntry);
```

## 4. RTOS特有问题处理（L0轻量系统关键）

### 4.1 堆栈溢出检测

RTOS间的堆栈管理机制差异是迁移中最常见的致命问题：

| 特性 | FreeRTOS | RT-Thread | LiteOS-M | 迁移注意事项 |
|------|---------|-----------|----------|------------|
| **栈大小单位** | word (4字节) | byte | byte | FreeRTOS的512 = 2048字节！ |
| **栈增长方向** | 向下 | 向下 | 向下 | 一致，但检查方式不同 |
| **溢出检测** | configCHECK_FOR_STACK_OVERFLOW | RT_USING_OVERFLOW_CHECK | LOSCFG_BASE_CORE_TSK_MONITOR | 需启用对应配置宏 |
| **栈对齐** | portBYTE_ALIGNMENT | RT_ALIGN_SIZE | 8字节(ARM)/16字节(RISC-V) | RISC-V要求更严格对齐 |
| **最小栈** | configMINIMAL_STACK_SIZE | RT_THREAD_PRIORITY_MAX | LOS_TASK_MIN_STACK_SIZE | 确认各平台最小值 |

```c
/* 迁移时的栈大小换算 */
// FreeRTOS原始代码
xTaskCreate(task_func, "name", 512, NULL, 5, &handle);  
// 512 words = 2048 bytes

// LiteOS-M迁移后
TSK_INIT_PARAM_S param = {0};
param.uwStackSize = 2048;  // 直接指定字节数
```

### 4.2 Tick频率差异

不同RTOS的Tick频率配置差异导致时间相关API的行为变化：

| RTOS | 默认Tick频率 | 配置位置 | 典型值范围 |
|------|------------|---------|-----------|
| FreeRTOS | 1000 Hz | `configTICK_RATE_HZ` in FreeRTOSConfig.h | 100~1000 Hz |
| RT-Thread | 1000 Hz | `RT_TICK_PER_SECOND` in rtconfig.h | 100~1000 Hz |
| LiteOS-M | 100 Hz | `LOSCFG_BASE_CORE_TICK_PER_SECOND` in target_config.h | 100~1000 Hz |

⚠️ **常见陷阱**：FreeRTOS中`vTaskDelay(10)`在1000Hz下延时10ms，但在LiteOS-M默认100Hz下仅延时100ms！必须确认Tick频率并做相应换算。

### 4.3 调度策略差异

| 特性 | FreeRTOS | RT-Thread | LiteOS-M |
|------|---------|-----------|----------|
| **优先级数值** | 0(最低)~configMAX_PRIORITIES-1(最高) | 0(最高)~RT_THREAD_PRIORITY_MAX-1(最低) | 0(最高)~LOSCFG_BASE_CORE_TSK_NUM_PRIORITIES-1(最低) |
| **同优先级调度** | 时间片轮转(可选) | 时间片轮转 | 时间片轮转 |
| **优先级继承** | Mutex支持 | Mutex支持 | Mutex支持 |
| **空闲任务钩子** | vApplicationIdleHook | rt_thread_idle_hook | LOS_TaskIdleHook |

⚠️ **严重注意**：FreeRTOS和LiteOS-M的优先级数值含义**相反**！FreeRTOS中数值越大优先级越高，LiteOS-M中数值越小优先级越高。

### 4.4 中断嵌套与ISR安全

| 特性 | FreeRTOS | RT-Thread | LiteOS-M |
|------|---------|-----------|----------|
| **ISR中标识** | `FromISR`后缀API | `rt_interrupt_get_nest()` | `LOS_IntLock/Restore` |
| **上下文切换触发** | `portYIELD_FROM_ISR()` | 自动 | 自动 |
| **嵌套深度** | 取决于Port | 支持 | 支持(Cortex-M NVIC优先级分组) |
| **ISR中可用API** | 仅FromISR系列 | 部分内核API | 仅非阻塞API |

## 5. 常见迁移陷阱清单

| # | 陷阱 | 严重度 | 源平台 | 描述 | 解决方案 |
|---|------|--------|--------|------|---------|
| 1 | **ISR中使用阻塞API** | 🔴 致命 | FreeRTOS | 在非FromISR API中阻塞会导致系统崩溃 | 严格区分ISR/Task上下文，ISR只用OSAL的非阻塞接口 |
| 2 | **Tick频率假设** | 🟡 严重 | FreeRTOS | `configTICK_RATE_HZ`在不同项目中可能不同 | 统一使用毫秒(ms)作为时间单位 |
| 3 | **devm自动释放丢失** | 🟡 严重 | Linux | 迁移后忘记手动释放导致内存泄漏 | 在Release回调中逐一释放所有资源 |
| 4 | **信号量语义差异** | 🟡 严重 | RT-Thread | RT-Thread信号量有PRIO/FCFS模式，OSAL不保证顺序 | 如需优先级继承，使用OsalMutex |
| 5 | **工作队列缺失** | 🟡 严重 | Linux/Zephyr | 底半部机制在OSAL中不存在 | 创建专用工作线程+消息队列(RingBuffer+Sem) |
| 6 | **字节序假设** | 🟡 严重 | All | 不同平台的默认字节序可能不同 | 显式使用htobe/be32toh等转换宏 |
| 7 | **栈大小不足** | 🟡 严重 | FreeRTOS | FreeRTOS以word为单位，OSAL以byte为单位 | 仔细换算：`stack_bytes = words * sizeof(StackType_t)` |
| 8 | **HCS属性名拼写** | 🟢 中等 | All | HCS属性名大小写敏感 | 建立属性名规范文档 |
| 9 | **Dispatch cmdId冲突** | 🟢 中等 | All | 不同驱动的cmdId可能重叠 | 使用统一的cmdId命名空间 |
| 10 | **Platform接口缺失** | 🔴 致命 | All | 某些外设没有对应的HDF Platform接口 | 需先实现Platform驱动或使用MMIO直接访问 |
| 11 | **内存对齐问题** | 🟡 严重 | All | DMA缓冲区需要特殊对齐 | 使用OsalMemAlign分配DMA缓冲 |
| 12 | **日志级别滥用** | 🟢 中等 | All | 高频路径使用HDF_LOGI导致性能下降 | 高频路径使用HDF_LOGD或条件编译 |
| 13 | **中断触发方式不匹配** | 🟡 严重 | Linux | Linux的IRQ flags与OSAL不完全对应 | 仔细对照触发方式映射表 |
| 14 | **竞态条件** | 🔴 致命 | All | 迁移过程中改变了锁的粒度或范围 | 重新审查所有共享数据的保护 |
| 15 | **初始化顺序依赖** | 🟡 严重 | RT-Thread | INIT_BOARD_EXPORT的顺序可能与HDF加载顺序不同 | 通过HCS priority字段控制加载顺序 |

## 6. 最佳实践

1. **先分析再动手**：务必先生成完整的API调用清单和依赖图，再开始转换
2. **增量迁移**：不要一次性转换所有代码，按模块逐步迁移并验证
3. **保留原始注释**：在转换后的代码中保留原始注释，标注修改原因
4. **使用OSAL优先原则**（L1）：所有系统相关操作必须通过OSAL，不使用内核私有API
5. **编写迁移日志**：记录每个文件的修改点、决策依据和遗留问题
6. **自动化测试先行**：在迁移前为源驱动编写接口测试，迁移后用同一套测试验证
7. **代码审查Checklist**：建立专门的迁移代码审查清单
8. **性能基准对比**：迁移前后进行关键路径的性能对比测试

## 7. 质量评估体系

### 7.1 评估维度

| 维度 | 指标 | 权重 | 达标线 |
|------|------|------|--------|
| **功能等价性** | 接口行为一致性测试通过率 | 30% | ≥99% |
| **编译正确性** | 零warning编译通过 | 10% | 100% |
| **代码规范性** | HDF编码规范检查通过率 | 10% | ≥95% |
| **OSAL合规性** | 无内核私有API调用 | 15% | 100% |
| **资源安全性** | 无内存泄漏、无资源泄露 | 15% | 100% |
| **性能保持** | 关键路径延迟退化≤10% | 10% | ≥90% |
| **文档完整性** | 迁移报告、API映射表齐全 | 10% | 100% |

### 7.2 自动化检查项

```yaml
migration_quality_check:
  compile:
    - zero_warning: true
    - target_platforms: ["liteos_m", "liteos_a"]  # ⭐ 仅Lite系统
  
  static_analysis:
    - no_kernel_api: true          # 不允许直接调用内核API（L1适用）
    - osal_coverage: 1.0           # 所有系统调用都通过OSAL（L1适用）
    - null_check: true             # 所有指针使用前检查NULL
    - resource_leak: true          # 资源分配/释放配对
  
  functional:
    - interface_test_pass_rate: 0.99
    - isr_safety: true             # ISR中不使用阻塞API
    - concurrency_review: true     # 并发安全审查
  
  code_style:
    - hdf_naming_convention: true
    - log_tag_defined: true
    - error_handling_complete: true
```
