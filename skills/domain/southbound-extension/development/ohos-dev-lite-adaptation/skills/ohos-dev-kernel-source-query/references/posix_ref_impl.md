# POSIX KAL 参考实现模式 (Hi3861V100 / OH Lite)

> **来源**: Ground Truth `device/soc/hisilicon/hi3861v100/hi3861_adapter/kal/posix/src/`
> **用途**: P2 kernel-port 阶段生成 POSIX 适配层时的参考模板
> **版本**: Iteration 02 提取 | 目标覆盖率: L2 POSIX ≥ 80%

---

## 1. 架构总览

OH Lite 的 POSIX KAL 不是简单的一对一映射，而是一个**多层适配层**：

```
应用代码 (POSIX API)
    ↓
┌─────────────────────────────────────┐
│  POSIX Wrapper Layer (本文件描述)     │  ← pthread.h / unistd.h / time.h / fcntl.h
│  - ID 转换 (pthread_t ↔ taskID)      │
│  - FD 分区路由 (socket vs filesystem) │
│  - 回调封装                          │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  LiteOS Kernel API                  │  ← los_task.h / los_swtmr.h / los_mux.h
│  LOS_TaskCreate / LOS_MuxLock / ... │
└─────────────────────────────────────┘
```

**关键设计决策（必须在生成时遵守）：**
1. `pthread_t` ≠ `UINT32 taskID` — 必须偏移以防止混淆
2. `PthreadData` 复用 TCB 的 `taskName` 字段存储（不额外分配内存）
3. `pthread_join` 使用**轮询**而非阻塞信号量
4. 文件描述符空间**分区管理**：socket / random / HiFS 各占一段

---

## 2. pthread.c 实现模式

### 2.1 核心数据结构

```c
#define POLLING_INTERVAL_FOR_JOIN 1000   /* join 轮询间隔 (ticks) */
#define PTHREAD_NAMELEN 16              /* 线程名最大长度 */

/* PthreadData: 存储在 TCB->taskName 字段中 */
struct PthreadData {
    CHAR name[PTHREAD_NAMELEN];    /* 线程名称 */
    BOOL detached;                 /* 是否 detached */
    BOOL exited;                   /* 是否已退出 */
    VOID *exitCode;                /* 退出码 */
};
```

### 2.2 ID 转换机制（关键！）

```c
/*
 * pthread_t 与原生 taskID 的转换:
 *   pthread_t = taskID + g_taskMaxNum (偏移)
 *   taskID   = pthread_t - g_taskMaxNum
 *
 * 原因: 防止误将 pthread_t 传给 LOS_TaskXXX 作为原生 taskID
 */
static inline UINT32 P2T(pthread_t id) { return (UINT32)id - g_taskMaxNum; }
static inline pthread_t T2P(UINT32 id) { return (pthread_t)(id + g_taskMaxNum); }

/* 从 TCB 获取 PthreadData (复用 taskName 字段) */
static inline struct PthreadData *GetPthreadData(UINT32 taskID) {
    return IsPthread(taskID)
        ? (struct PthreadData *)(UINTPTR)(OS_TCB_FROM_TID(taskID)->taskName)
        : NULL;
}
```

### 2.3 pthread_create 模式

```
输入: pthread_t *thread, const pthread_attr_t *attr, void *(*start)(void*), void *arg

步骤:
1. 验证参数 (thread != NULL, startRoutine != NULL)
2. malloc(sizeof(PthreadData)) → memset(0)
3. 设置默认值:
   - priority = LOSCFG_BASE_CORE_TSK_DEFAULT_PRIO
   - stacksize = LOSCFG_BASE_CORE_TSK_DEFAULT_STACK_SIZE
4. 如果 attr != NULL:
   - detachstate == PTHREAD_CREATE_DETACHED → pthreadData->detached = TRUE
   - stacksize → 从 attr->stacksize 取
   - priority → 从 attr->schedparam.sched_priority 取
5. 将 startRoutine 和 arg 编码为 UINT32 参数:
   - param1 = (UINT32)(UINTPTR)startRoutine
   - param2 = (UINT32)(UINTPTR)arg
   - param3, param4 = 0 (未使用)
6. LOS_TaskCreate(&tid, &taskInitParam, PthreadEntry, param1..4)
7. *thread = T2P(tid)
8. 返回 0 (成功)
```

### 2.4 PthreadEntry 包装函数

```c
static void *PthreadEntry(UINT32 param1, UINT32 param2, UINT32 param3, UINT32 param4)
{
    // 1. 解码参数
    void *(*startRoutine)(void *) = (void *)(UINTPTR)param1;
    void *param = (void *)(UINTPTR)param2;
    void *retVal = NULL;
    UINT32 taskID = LOS_CurTaskIDGet();
    struct PthreadData *pthreadData = GetPthreadData(taskID);

    // 2. 执行用户函数
    retVal = startRoutine(param);

    // 3. 退出处理
    pthreadData = GetPthreadData(taskID);
    if (pthreadData->detached) {
        free(pthreadData);           // detached 线程自动释放
        pthreadData = NULL;
    } else {
        pthreadData->exited = TRUE;  // joinable 线程标记退出
        pthreadData->exitCode = retVal;
    }
    return retVal;
}
```

### 2.5 pthread_join 模式（轮询！非阻塞！）

```c
int pthread_join(pthread_t thread, void **retval)
{
    UINT32 taskID = P2T(thread);
    struct PthreadData *pData;

    // 1. 验证是合法 pthread (非 native task)
    if (!IsPthread(taskID)) return ESRCH;

    // 2. 轮询等待退出 (不是阻塞信号量!)
    while (TRUE) {
        pData = GetPthreadData(taskID);
        if (pData && pData->exited) break;

        LOS_TaskDelay(POLLING_INTERVAL_FOR_JOIN);  // 休眠 1000 ticks 后重试
    }

    // 3. 收集退出码 + 清理
    if (retval) *retval = pData->exitCode;
    free(pdata);  // join 后释放 PthreadData
    // 标记为 non-pthread 以防重复 join
    return 0;
}
```

> **⚠️ 关键差异点**: 大多数 POSIX 实现用信号量做 join 阻塞。OH Lite 用轮询+TaskDelay，因为 LiteOS 的 Mux/Sem 不支持从 ISR 或外部唤醒。

### 2.6 其他函数速查

| 函数 | LiteOS 映射 | 备注 |
|------|------------|------|
| pthread_setschedparam | LOS_TaskPriSet | policy 参数忽略 |
| pthread_getschedparam | LOS_TaskPriGet | |
| pthread_self | T2P(LOS_CurTaskIDGet()) | |
| pthread_cancel | 设置 cancel flag + LOS_TaskSuspend | 非立即取消 |
| pthread_detach | 设置 PthreadData->detached=TRUE | |
| pthread_exit | 设置 exited+exitCode, LOS_TaskSuspend(self) | |
| pthread_setname_np | LOS_TaskSetName (截断到16字符) | |
| pthread_getname_np | LOS_TaskGetName | |

### 2.7 头文件依赖

```c
#include <errno.h>
#include <pthread.h>
#include <unistd.h>
#include <securec.h>          // Huawei 安全函数 (memset_s 等)
#include "los_task.h"
#include "los_task_pri.h"     // OS_TCB_FROM_TID 等内部 API
```

---

## 3. pthread_attr.c 模式

### 数据结构

```c
// OH Lite 的 pthread_attr_t 是一个简化的结构体:
typedef struct {
    int detachstate;            // PTHREAD_CREATE_DETACHED / JOINABLE
    int schedpolicy;            // SCHED_OTHER (唯一支持)
    struct sched_param schedparam; // .sched_priority
    size_t stacksize;           // 默认 = LOSCFG_BASE_CORE_TSK_DEFAULT_STACK_SIZE
    int stackaddr_set;          // 不支持自定义栈地址!
    void *stackaddr;
    // 注意: 没有 inheritsched, scope, guardsize 等高级属性
} pthread_attr_t;
```

### 默认值表

| 属性 | 默认值 | 可设置范围 |
|------|--------|-----------|
| detachstate | PTHREAD_CREATE_JOINABLE | DETACHED / JOINABLE |
| schedpolicy | SCHED_OTHER | 仅 SCHED_OTHER |
| sched_priority | LOSCFG_BASE_CORE_TSK_DEFAULT_PRIO | 1-31 |
| stacksize | LOSCFG_BASE_CORE_TSK_DEFAULT_STACK_SIZE | ≥ PTHREAD_STACK_MIN |
| stackaddr_set | 0 (不支持) | N/A |

---

## 4. time.c 实现模式

### 4.1 时间基础

```c
const UINT32 nsPerTick = OS_SYS_NS_PER_SECOND / LOSCFG_BASE_CORE_TICK_PER_SECOND;
// 例: 1000000000ns / 1000Hz = 1000000ns/tick (1ms per tick)
```

### 4.2 nanosleep → LOS_TaskDelay

```c
int nanosleep(const struct timespec *rqtp, struct timespec *rmtp)
{
    UINT64 nseconds = (UINT64)rqtp->tv_sec * OS_SYS_NS_PER_SECOND + rqtp->tv_nsec;
    UINT64 tick = (nseconds + nsPerTick - 1) / nsPerTick;  // 向上取整
    LOS_TaskDelay((UINT32)tick);
    return 0;
}
```

### 4.3 sleep → nanosleep 封装

```c
unsigned int sleep(unsigned int seconds) {
    struct timespec req = { .tv_sec = seconds, .tv_nsec = 0 };
    nanosleep(&req, NULL);
    return 0;
}
```

### 4.4 Timer API 映射 (CMSIS-RTOS v2 timer wrapper)

| POSIX Timer | LiteOS SWTimer | 说明 |
|-------------|---------------|------|
| timer_create | LOS_SwtmrCreate | timerID 偏移存储 |
| timer_settime | LOS_SwtmrStart | 支持 RELATIVE/ABSOLUTE |
| timer_gettime | LOS_SwtmrTimeGet | |
| timer_delete | LOS_SwtmrDelete | |
| timer_getoverrun | 直接返回 0 | LiteOS 不支持 overrun 计数 |

### 4.5 clock_gettime

```c
int clock_gettime(clockid_t clk_id, struct timespec *ts)
{
    switch (clk_id) {
    case CLOCK_MONOTONIC: {
        UINT64 tick = LOS_TickCountGet();
        ts->tv_sec = tick / LOSCFG_BASE_CORE_TICK_PER_SECOND;
        ts->tv_nsec = (tick % LOSCFG_BASE_CORE_TICK_PER_SECOND) * nsPerTick;
        break;
    }
    case CLOCK_REALTIME: {
        // 读取 RTC 系统时间 (具体实现因芯片而异)
        // 通常调用 LOS_GetSystemTime() 或 hi_get_rtc_time()
        break;
    }
    default:
        errno = EINVAL;
        return -1;
    }
    return 0;
}
```

### 4.6 头文件依赖

```c
#include <errno.h>
#include <time.h>
#include <unistd.h>
#include "los_tick.h"       // OS_SYS_NS_PER_SECOND, LOSCFG_BASE_CORE_TICK_PER_SECOND
#include "los_swtmr.h"      // Software Timer APIs
```

---

## 5. file.c 实现模式

### 5.1 FD 分区架构（核心设计）

```
FD 空间布局 (32-bit int):
┌─────────────────────────┬──────────────┬───────────────────┬──────────┐
│ Standard I/O (0-2)      │ LWIP Sockets │ Random Device     │ HiFS FS  │
│ stdin/stdout/stderr     │ [offset,N)   │ [RANDOM_FD]       │ [HI_FS,) │
└─────────────────────────┴──────────────┴───────────────────┴──────────┘

宏定义:
  LWIP_SOCKET_OFFSET      = 基础偏移 (通常 >= 3)
  RANDOM_DEV_FD           = LWIP_SOCKET_OFFSET + LWIP_CONFIG_NUM_SOCKETS
  HI_FS_FD_OFFSET         = RANDOM_DEV_FD + 1
  HI_FS_MAX_OPEN_FILES    = 33 (32个文件 + 1 slot)

判断宏:
  IS_SOCKET_FD(fd)  → (fd >= LWIP_OFFSET && fd < LWIP_OFFSET + NUM_SOCKETS)
  IS_HI_FS_FD(fd)   → (fd >= HI_FS_FD_OFFSET && fd < HI_FS_FD_OFFSET + MAX_FILES)
  HI_FS_FD(fd)      → (fd - HI_FS_FD_OFFSET)  // 转换为内部 FD
```

### 5.2 open() 路由逻辑

```c
int open(const char *path, int oflag, ...)
{
    // 1. Socket 路径? (如 "/dev/socket/xxx")
    //    → lwip_socket(AF_INET, ...)
    // 2. Random 设备? ("/dev/random")
    //    → 返回 RANDOM_DEV_FD (特殊处理)
    // 3. 普通 HiFS 文件?
    //    → hi_fs_open(path, oflag) → 返回 HI_FS_FD_OFFSET + internal_fd
    // 4. 特殊路径处理 (/proc/, /sys/)
    //    → 各自的处理函数
}
```

### 5.3 read/write/ioctl/close 路由

```c
ssize_t read(int fd, void *buf, size_t count) {
    if IS_SOCKET_FD(fd)  → lwip_read(HI_FS_FD(fd), buf, count);
    if IS_HI_FS_FD(fd)   → hi_fs_read(HI_FS_FD(fd), buf, count);
    if fd == RANDOM_DEV_FD → hi_rng_read(buf, count);  // 硬件随机数
}

// write/close/ioctl 类似，按 fd 路由到对应后端
```

### 5.4 头文件依赖

```c
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <securec.h>
#include "lwip/sockets.h"      // Socket API
#include "hks_client.h"        // HUKS (密钥服务, 用于加密 FS)
#include "hi_fs.h"             // HiSilicon 文件系统 API
```

---

## 6. libc.c 模式

最小化包装 (~50 行)，主要包含：
- 非 ANSI C 扩展函数的 stub
- 编译器内置函数的替代实现
- 与 musl libc 的桥接函数

通常不需要复杂实现，大部分返回 0 或 ENOTSUP。

---

## 7. 生成时检查清单

生成 POSIX KAL 代码时，必须验证：

- [ ] `pthread_t` 使用偏移 ID（不等于 raw taskID）
- [ ] `PthreadEntry` 正确编码/解码函数指针和参数
- [ ] `pthread_join` 使用轮询模式（非信号量）
- [ ] `PthreadData` 通过 `OS_TCB_FROM_TID->taskName` 存储
- [ ] FD 空间分区正确（socket / random / HiFS 不重叠）
- [ ] `nanosleep` 向上取整到 tick
- [ ] Timer ID 使用独立偏移（不与 taskID 冲突）
- [ ] 所有 `#include` 包含 `<securec.h>` 和对应的 `los_*.h`
- [ ] 错误码使用 `errno` + 返回 `-1`（POSIX 惯例），而非 LiteOS 的 `UINT32` 返回值
