# KAL (Kernel Abstraction Layer) 适配参考

> **来源**：步骤 20-21 + `session_kal.json`(HAL) + `session_hal.json`(KAL补全)
> **适用场景**：P2 内核移植阶段，target_system = **L0** 时需要实现的内核抽象层
> **位置**：`hi3861_adapter/kal/` 目录下

## 什么是 KAL？

KAL = Kernel Abstraction Layer（内核抽象层）。它的作用是**将标准 OS API 映射到 LiteOS-M 的原生 API**，
使原本为其他 RTOS 或标准 POSIX/CMSIS 编写的代码能在 LiteOS-M 上运行。

```
┌──────────────────────────────┐
│   应用代码 / 第三方库         │  调用标准 API
│   osThreadNew()               │ ──┐
│   pthread_create()             │ ──┤
│   open() / read()              │ ──┘
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│        KAL 层（你需要写的）      │  API 翻译
│   cmsis/cmsis_liteos2.c       │  CMSIS-OS2 → LiteOS-M
│   posix/src/pthread.c          │  POSIX → LiteOS-M
│   posix/src/file.c             │  POSIX FS → LiteOS FS
│   posix/src/time.c             │  POSIX time → LiteOS
└──────────────┬───────────────┘
               │ 调用原生 API
┌──────────────▼───────────────┐
│     LiteOS-M 内核              │
│   LOS_TaskCreate / LOS_MuxCreate │
│   LOS_Open / LOS_Read / LOS_Write │
└──────────────────────────────┘
```

## KAL 的两个子模块

### 模块 A: CMSIS-OS2 适配 (`kal/cmsis/`)

**头文件**: `#include "cmsis_os.h"` （CMSIS 标准 OS 抽象接口）
**目标文件**: `cmsis_liteos2.c`
**规模**: ~1386 行（Hi3861V100 实际案例）

#### 核心 API 映射表

| CMSIS-OS2 API | LiteOS-M 原生 API | 参数转换说明 |
|:-------------|:------------------|:------------|
| `osKernelInitialize(void)` | 无需调用 | LiteOS 在 main() 前自动初始化 |
| `osKernelStart(void)` | 无需调用 | main() 返回后自动启动调度 |
| `osKernelGetState(void)` | 直接返回 `osKernelRunning` | |
| `osKernelLock(void)` | `LOS_TaskLock()` | |
| `osKernelUnlock(void)` | `LOS_TaskUnlock()` | |
| **线程** | | |
| `osThreadNew(func, arg, attr)` | `LOS_TaskCreate(&taskID, &taskAttr, func, attr)` | osThreadAttr_t → LOS_TaskAttr_t（栈大小/优先级/名称）|
| `osThreadGetName(thread_id)` | `LOS_TaskInfoGet(taskId, &taskInfo); return taskInfo.pcName` | |
| `osThreadExit()` | `LOS_Exit(0)` | |
| `osThreadTerminate(thread_id)` | `LOS_TaskDelete(taskId)` | |
| `osThreadYield()` | `LOS_Yield()` | |
| **延时** | | |
| `osDelay(ticks)` | `LOS_TaskDelay(ticks)` | 直接映射 |
| `osDelayUntil(tick)` | 自行计算差值 + LOS_TaskDelay | |
| **互斥量** | | |
| `osMutexNew(attr)` | `LOS_MuxCreate(&muxId)` | |
| `osMutexDelete(mutex_id)` | `LOS_MuxDelete(mutex_id)` | |
| `osMutexAcquire(mutex_id, timeout)` | `LOS_MuxPend(muxId, timeout)` | |
| `osMutexRelease(mutex_id)` | `LOS_MuxPost(muxId)` | |
| **信号量** | | |
| `osSemaphoreNew(max, init, attr)` | `LOS_SemCreate(&semId, ...)` | |
| `osSemaphoreDelete(semaphore_id)` | `LOS_SemDelete(semId)` | |
| `osSemaphoreAcquire(sem_id, timeout)` | `LOS_SemPend(semId, timeout)` | |
| `osSemaphoreRelease(sem_id)` | `LOS_SemPost(semId)` | |
| **定时器** | | |
| `osTimerNew(name, func, type, attr)` | `LOS_SwtCreate(&swtimerId, ...)` | osTimerType → SwtFuncType |
| `osTimerStart(timer_id)` | `LOS_SwtStart(swtimerId)` | |
| `osTimerStop(timer_id)` | `LOS_SwtStop(swtimerId)` | |
| `osTimerDelete(timer_id)` | `LOS_SwtDelete(swtimerId)` | |

### 模块 B: POSIX 适配 (`kal/posix/src/`)

**头文件**: 标准 POSIX 头文件 (`pthread.h`, `fcntl.h`, `unistd.h` 等)
**目标文件**: `pthread.c`, `file.c`, `time.c` 等
**规模**: pthread(~285行) + file(~200行) + time(~50行)

#### 核心 API 映射表

| POSIX API | LiteOS-M 原生 API | 说明 |
|:----------|:------------------|:-----|
| **线程 (pthread)** | | |
| `pthread_create(thread, attr, func, arg)` | `LOS_TaskCreate(&taskId, &losAttr, (TS_ENTRY_FUNC)func, (void *)arg)` | attr → LOS_TaskAttr_t 映射 |
| `pthread_join(thread, retval)` | `LOS_TaskJoin(taskId, retval)` | |
| `pthread_detach(thread)` | `LOS_TaskDetach(taskId)` | |
| `pthread_exit(retval)` | `LOS_Exit((UINTPTR)retval)` | |
| `pthread_self()` | `LOS_CurTaskIDGet(&taskId); return (pthread_t)taskId` | |
| **文件操作** | | |
| `open(path, flags, mode)` | `LOS_Open(path, flags)` | mode 参数在 LiteOS 中忽略 |
| `close(fd)` | `LOS_Close(fd)` | |
| `read(fd, buf, size)` | `LOS_Read(fd, buf, size)` | |
| `write(fd, buf, size)` | `LOS_Write(fd, buf, size)` | |
| `lseek(fd, offset, whence)` | `LOS_Seek(fd, offset, whence)` | |
| **时间** | | |
| `clock_gettime(clk_id, tp)` | `tp->tv_sec = LOS_TickCountGet() / LOSCFG_BASE_CORE_TICK_PER_SECOND` | 仅支持 CLOCK_REALTIME 近似 |
| **其他** | | |
| `gettimeofday(tv, tz)` | 类似 clock_gettime 实现 | |

### KAL BUILD.gn 模板

```gn
import("//build/lite/config/component/LiteComponent.gni")

# CMSIS-OS2 适配
static_library("cmsis") {
    sources = [ "cmsis_liteos2.c" ]
    include_dirs = [
        "//kernel/liteos_m/kal/cmsis",
        "//kernel/liteos_m/kal/posix/include",
    ]
}

# POSIX 适配
static_library("posix") {
    sources = [
        "src/pthread.c",
        "src/file.c",
        "src/time.c",
    ]
    include_dirs = [
        "//kernel/liteos_m/kal/posix/include",
        "//kernel/liteos_m/kal/cmsis",
    ]
}
```

## KAL 与 P2 其他子步骤的关系

```
P2 内核移植的完整子步骤（L0 场景）:

  2a: Kconfig 适配链 ──────────────── 内核组件选择（含 KAL 组件使能）
  2b: BUILD.gn 编译入口 ──────────── 含 KAL 的 BUILD.gn 引用
  2c: 启动代码 ──────────────────── 与 KAL 无直接关系
  2d: C 库适配 ──────────────────── malloc/printf 等（KAL 不涉及）
  2e: linker.ld ──────────────────── 需包含 KAL 符号
  ★2f: KAL 适配 (CMSIS+POSIX) ──── ★ 新增：本参考文档覆盖的内容
```

**关键点**：
- KAL 是 P2 的一部分（内核适配层），不是独立的阶段
- KAL 在 **config.gni 的 board_include_dirs 中必须包含 KAL 头文件路径**
- KAL 的 `BUILD.gn` 需要被 SoC 级 `BUILD.gn` 通过 `deps` 引用
- 对于 L1 系统，**不需要 KAL**（L1 使用 Linux 内核或完整 LiteOS-A，原生支持 POSIX）

## 何时需要实现 KAL？

| 条件 | 需要 KAL？ |
|------|:--------:|
| target_system = L0 且有第三方 CMSIS 代码 | ✅ 需要 (`cmsis_liteos2.c`) |
| target_system = L0 且有 POSIX 依赖(pthread/open等) | ✅ 需要 (`posix/*.c`) |
| target_system = L0 但仅写裸机驱动 | ❌ 可跳过 |
| target_system = L1 | ❌ 不需要（内核已提供） |
