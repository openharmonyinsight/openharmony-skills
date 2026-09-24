# target_config.h 参考模板

target_config.h是LiteOS-M轻量系统（L0）的核心配置文件，定义芯片的内核参数、内存布局和外设能力。

## 文件位置

通常在产品仓库的 `target/{board_name}/GCC/target_config.h`，或SOC适配包中。

## 参考样本

以下基于OpenHarmony已适配芯片的格式编写，适用于新芯片适配时作为起点。

### 通用target_config.h

```c
/*
 * target_config.h - {CHIP_NAME} 目标配置
 * 基于OpenHarmony LiteOS-M轻量系统
 */
#ifndef TARGET_CONFIG_H
#define TARGET_CONFIG_H

#ifdef __cplusplus
#if __cplusplus
extern "C" {
#endif
#endif

/* ====== 内核基础配置 ====== */
#define LOSCFG_PLATFORM_HWI                    1    /* 硬件中断支持 */
#define LOSCFG_BASE_CORE_TSK_LIMIT             {TASK_LIMIT}  /* 最大任务数 */
#define LOSCFG_BASE_CORE_TSK_IDLE_STACK_SIZE   0x500  /* IDLE任务栈 */
#define LOSCFG_BASE_CORE_TSK_DEFAULT_STACK_SIZE 0x800 /* 默认任务栈 */
#define LOSCFG_BASE_CORE_TSK_MIN_STACK_SIZE    0x380  /* 最小任务栈 */
#define LOSCFG_BASE_CORE_TIMESLICE             1    /* 时间片轮转 */
#define LOSCFG_BASE_CORE_TICK_HW_TIME          0    /* tick时间 */
#define LOSCFG_BASE_CORE_TICK_FACTOR           1    /* tick精度(1ms) */

/* ====== IPC配置 ====== */
#define LOSCFG_BASE_IPC_QUEUE                  1    /* 队列支持 */
#define LOSCFG_BASE_IPC_QUEUE_LIMIT            {QUEUE_LIMIT}  /* 最大队列数 */
#define LOSCFG_BASE_IPC_SEM                    1    /* 信号量支持 */
#define LOSCFG_BASE_IPC_SEM_LIMIT              {SEM_LIMIT}    /* 最大信号量数 */
#define LOSCFG_BASE_IPC_MUX                    1    /* 互斥锁支持 */
#define LOSCFG_BASE_IPC_MUX_LIMIT              {MUX_LIMIT}    /* 最大互斥锁数 */
#define LOSCFG_BASE_IPC_EVENT                  1    /* 事件支持 */
#define LOSCFG_BASE_IPC_EVENT_LIMIT            {EVENT_LIMIT}  /* 最大事件数 */

/* ====== 内存配置 ====== */
#define LOSCFG_BASE_MEM_NODE_INTEGRAL_SIZE     32   /* 内存对齐粒度 */
#define LOSCFG_MEM_MUL_MEMPOOL                 0    /* 多内存池 */
#define LOSCFG_SYS_HEAP_SIZE                   {HEAP_SIZE}    /* 堆大小 */
#define LOSCFG_SYS_MEM_SIZE_MAX                {MEM_SIZE}     /* 最大可用内存 */

/* ====== 软件定时器 ====== */
#define LOSCFG_BASE_SWTMR                      1    /* 软件定时器 */
#define LOSCFG_BASE_SWTMR_LIMIT                {SWTMR_LIMIT}  /* 最大软定时器数 */

/* ====== 调试配置 ====== */
#define LOSCFG_SHELL                           1    /* Shell支持 */
#define LOSCFG_SHELL_SERIAL                    0    /* 串口Shell */
#define PRINT_LEVEL                            4    /* 打印级别(0-4) */

/* ====== 芯片硬件参数 ====== */
/* 时钟 */
#define CHIP_SYS_CLOCK                         {SYS_CLOCK}    /* 系统主频Hz */
#define CHIP_EXTERNAL_OSC_FREQ                 {OSC_FREQ}     /* 外部晶振Hz */
#define CHIP_LOSC_CLOCK                        32768          /* 低速时钟Hz */

/* 内存映射 */
#define CHIP_INT_RAM_START                     {RAM_START}     /* RAM起始地址 */
#define CHIP_INT_RAM_SIZE                      {RAM_SIZE}      /* RAM大小 */
#define CHIP_FLASH_START                       {FLASH_START}   /* Flash起始 */
#define CHIP_FLASH_SIZE                        {FLASH_SIZE}    /* Flash大小 */

/* 中断 */
#define CHIP_IRQ_MAX_NUM                       {IRQ_MAX}       /* 最大中断号 */
#define CHIP_INT_PEND_ARRAY_SIZE               ((CHIP_IRQ_MAX_NUM >> 5) + 1)

/* ====== 外设能力 ====== */
#define HAL_GPIO_PORT_NUM                      {GPIO_PORTS}    /* GPIO端口数 */
#define HAL_GPIO_PIN_PER_PORT                  {PIN_PER_PORT}  /* 每端口引脚数 */
#define HAL_UART_NUM                           {UART_NUM}      /* UART数量 */
#define HAL_I2C_NUM                            {I2C_NUM}       /* I2C数量 */
#define HAL_SPI_NUM                            {SPI_NUM}       /* SPI数量 */
#define HAL_ADC_CHANNEL_NUM                    {ADC_CH}        /* ADC通道数 */
#define HAL_PWM_NUM                            {PWM_NUM}       /* PWM通道数 */

#ifdef __cplusplus
#if __cplusplus
}
#endif
#endif

#endif /* TARGET_CONFIG_H */
```

## 典型芯片参数参考

| 参数 | STM32F407 | Hi3861 | ESP32-C3 |
|------|-----------|--------|----------|
| TASK_LIMIT | 16 | 10 | 16 |
| HEAP_SIZE | 0x8000 (32KB) | 0x8000 | 0x10000 (64KB) |
| RAM_SIZE | 0x20000 (128KB) | 0x60000 (384KB) | 0x64000 (400KB) |
| FLASH_START | 0x08000000 | 0x100000 | 0x42000000 |
| FLASH_SIZE | 0x100000 (1MB) | 0x200000 (2MB) | 0x400000 (4MB) |
| SYS_CLOCK | 168000000 | 160000000 | 160000000 |
| IRQ_MAX | 82 | 64 | 31 |
| GPIO_PORTS | 9 (A-I) | 1 | 1 |
| PIN_PER_PORT | 16 | 15 | 22 |
| UART_NUM | 6 | 2 | 2 |
| I2C_NUM | 3 | 1 | 1 |
| SPI_NUM | 3 | 1 | 2 |
| ADC_CH | 16 | 2 | 5 |
| PWM_NUM | 14 | 5 | 0 |

## 参数选取指导

| 参数 | 选取规则 |
|------|---------|
| TASK_LIMIT | RAM ≤ 64KB: 8-10, 128KB: 12-16, 256KB+: 16-32 |
| HEAP_SIZE | 总RAM × 40-60%，扣除内核开销(约8-16KB) |
| QUEUE/SEM/MUX_LIMIT | 与TASK_LIMIT相当或略多 |
| IRQ_MAX | 从芯片手册的中断向量表获取 |
| SYS_CLOCK | 从时钟树配置或PLL设置获取 |
