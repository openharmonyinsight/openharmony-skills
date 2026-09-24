/*
 * target_config.h — STM32F407ZG (Uniproton) 最小可用内核配置骨架
 * 芯片: STM32F407ZG, ARM Cortex-M4, 168MHz
 * 来源：ohos-lite-helper MCP 域 device-config（kernel-config-samples）
 *
 * ⚠️ 此文件为最小可用骨架。深度特性裁剪由内核裁剪能力（06）完成。
 */

#ifndef _TARGET_CONFIG_H
#define _TARGET_CONFIG_H

/* ==================== 内核版本 ==================== */
#define LITEOS_VER                        "1.0"

/* ==================== 系统时钟 ==================== */
/* STM32F407 主频 168MHz */
#define OS_SYS_CLOCK                      168000000

/* ==================== Tick 配置 ==================== */
#define LOSCFG_BASE_CORE_TICK_PER_SECOND  100

/* ==================== 任务配置 ==================== */
#define LOSCFG_BASE_CORE_TSK_LIMIT        16
#define LOSCFG_BASE_CORE_TSK_DEFAULT_STACK_SIZE  (0x1000UL)  /* 4KB */
#define LOSCFG_BASE_CORE_TSK_IDLE_STACK_SIZE     (0x400UL)   /* 1KB */
#define LOSCFG_BASE_CORE_TSK_MIN_STACK_SIZE      (0x180UL)   /* 384B */

/* ==================== IPC 配置 ==================== */
#define LOSCFG_BASE_IPC_SEM_LIMIT         16
#define LOSCFG_BASE_IPC_MUX_LIMIT         16
#define LOSCFG_BASE_IPC_QUEUE_LIMIT       16

/* ==================== 软件定时器 ==================== */
#define LOSCFG_BASE_CORE_SWTMR_LIMIT      16

/* ==================== 内存配置 ==================== */
#define LOSCFG_MEM_POOL_SIZE              0x2000

#endif /* _TARGET_CONFIG_H */
