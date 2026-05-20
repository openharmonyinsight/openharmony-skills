# 枚举

## enum ExplicitGcType

```cangjie
public enum ExplicitGcType <: ToString {
    | Disabled
    | Heavy
    | Light
}
```

功能：用于指定 `@Configure` 宏的 `explicitGC` 配置参数。表示 [GC](../../runtime/runtime_package_api/runtime_package_funcs.md#func-gcbool) 执行的三种不同方式。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### Disabled

```cangjie
Disabled
```

功能：[GC](../../runtime/runtime_package_api/runtime_package_funcs.md#func-gcbool) 不会被框架显式调用。

### Heavy

```cangjie
Heavy
```

功能：[std.runtime.GC](../../runtime/runtime_package_api/runtime_package_funcs.md#func-gcbool)(heavy: true) 将在性能测试执行期间由框架显式调用。

### Light

```cangjie
Light
```

功能：[std.runtime.GC](../../runtime/runtime_package_api/runtime_package_funcs.md#func-gcbool)(heavy: false) 将在 Benchmark 函数执行期间由框架显式调用。这是默认设置。

### func toString()

```cangjie
public func toString(): String
```

功能：[GC](../../runtime/runtime_package_api/runtime_package_funcs.md#func-gcbool) 执行的三种不同方式字符串。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - [GC](../../runtime/runtime_package_api/runtime_package_funcs.md#func-gcbool) 执行的三种不同方式字符串。

## enum TimeUnit

```cangjie
public enum TimeUnit <: ToString {
    | Micros
    | Millis
    | Nanos
    | Seconds
}
```

功能：可以在 [TimeNow](./unittest_package_structs.md#struct-timenow) 构造函数中使用的时间单位。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### Micros

```cangjie
Micros
```

功能：单位为微秒。

### Millis

```cangjie
Millis
```

功能：单位为毫秒。

### Nanos

```cangjie
Nanos
```

功能：单位为纳秒。

### Seconds

```cangjie
Seconds
```

功能：单位为秒。

### func toString()

```cangjie
public func toString(): String
```

功能： 将时间转换为字符串。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 由四个不同的时间表示组成的字符串。

## enum PerfCounter

```cangjie
public enum PerfCounter <: ToString {
    | HW_CPU_CYCLES
    | HW_INSTRUCTIONS
    | HW_CACHE_REFERENCES
    | HW_CACHE_MISSES
    | HW_BRANCH_INSTRUCTIONS
    | HW_BRANCH_MISSES
    | HW_BUS_CYCLES
    | HW_STALLED_CYCLES_FRONTEND
    | HW_STALLED_CYCLES_BACKEND
    | HW_REF_CPU_CYCLES
    | SW_CPU_CLOCK
    | SW_TASK_CLOCK
    | SW_PAGE_FAULTS
    | SW_CONTEXT_SWITCHES
    | SW_CPU_MIGRATIONS
    | SW_PAGE_FAULTS_MIN
    | SW_PAGE_FAULTS_MAJ
    | SW_EMULATION_FAULTS
}
```

功能：枚举 [Perf](./unittest_package_structs.md#struct-perf) 构造器支持的 CPU 计数器。

有关特定 cpu 计数器的详细信息，请参阅 Linux 内核中 [perf_event_open](https://man7.org/linux/man-pages/man2/perf_event_open.2.html) 系统调用的文档。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### HW_CPU_CYCLES

```cangjie
HW_CPU_CYCLES
```

功能：原始 CPU 周期数。

### HW_INSTRUCTIONS

```cangjie
HW_INSTRUCTIONS
```

功能：退役的 CPU 指令数量。

### HW_CACHE_REFERENCES

```cangjie
HW_CACHE_REFERENCES
```

功能：缓存访问量。

### HW_CACHE_MISSES

```cangjie
HW_CACHE_MISSES
```

功能：缓存未命中数量。

### HW_BRANCH_INSTRUCTIONS

```cangjie
HW_BRANCH_INSTRUCTIONS
```

功能：退役的分支 CPU 指令数量。

### HW_BRANCH_MISSES

```cangjie
HW_BRANCH_MISSES
```

功能：分支预测失败的数量。

### HW_BUS_CYCLES

```cangjie
HW_BUS_CYCLES
```

功能：总线周期数。

### HW_STALLED_CYCLES_FRONTEND

```cangjie
HW_STALLED_CYCLES_FRONTEND
```

功能：CPU 周期被浪费在 CPU 管道前端阶段的等待上的数量。

### HW_STALLED_CYCLES_BACKEND

```cangjie
HW_STALLED_CYCLES_BACKEND
```

功能：CPU 周期被浪费在 CPU 管道后端阶段的等待上的数量。

### HW_REF_CPU_CYCLES

```cangjie
HW_REF_CPU_CYCLES
```

功能：与频率无关的 CPU 周期数。

### SW_CPU_CLOCK

```cangjie
SW_CPU_CLOCK
```

功能：每个 CPU 时钟时间量。

### SW_TASK_CLOCK

```cangjie
SW_TASK_CLOCK
```

功能：每个任务的 CPU 时钟时间量。

### SW_PAGE_FAULTS

```cangjie
SW_PAGE_FAULTS
```

功能：页错误数量。

### SW_CONTEXT_SWITCHES

```cangjie
SW_CONTEXT_SWITCHES
```

功能：操作系统上下文切换的数量。

### SW_CPU_MIGRATIONS

```cangjie
SW_CPU_MIGRATIONS
```

功能：CPU 之间的任务迁移量。

### SW_PAGE_FAULTS_MIN

```cangjie
SW_PAGE_FAULTS_MIN
```

功能：次要页错误数量。

### SW_PAGE_FAULTS_MAJ

```cangjie
SW_PAGE_FAULTS_MAJ
```

功能：主要页错误数量。

### SW_EMULATION_FAULTS

```cangjie
SW_EMULATION_FAULTS
```

功能：需要内核模拟的不受支持的指令数量。

### func toString()

```cangjie
public func toString(): String
```

功能： 将计数器转换为字符串。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 处理器计数器的字符串表示。
