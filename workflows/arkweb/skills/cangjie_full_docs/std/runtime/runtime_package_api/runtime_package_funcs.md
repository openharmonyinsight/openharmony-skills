# 函数

## func blackBox\<T>(T)

```cangjie
public func blackBox<T>(input: T): T
```

功能：指示编译器传入的变量进入优化黑盒，无法进行死代码消除等优化。

参数：

- input: T - 进入优化黑洞的变量。

返回值：

- T - 若变量仍需被使用，则可使用该返回值进行调用。

## func dumpHeapData(Path)

```cangjie
public func dumpHeapData(path: Path): Unit
```

功能：生成堆内存快照信息，写入指定路径的文件。

参数：

- path: [Path](../../fs/fs_package_api/fs_package_structs.md#struct-path) - 生成堆内存快照文件的文件路径。

异常：

- MemoryInfoException - 生成堆内存快照失败时，抛出此异常。

## func gc(Bool)

```cangjie
public func gc(heavy!: Bool = false): Unit
```

功能：执行 [gc](runtime_package_funcs.md#func-gcbool)。

参数：

- heavy!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - [gc](runtime_package_funcs.md#func-gcbool) 执行程度，如果为 true，执行会慢，内存收集的多一些，默认值为 false。

## func GC(Bool) <sup>(deprecated)</sup>

```cangjie
public func GC(heavy!: Bool = false): Unit
```

功能：执行 [GC](runtime_package_funcs.md#func-gcbool-deprecated)。

> **注意：**
>
> 未来版本即将废弃，使用 [gc](runtime_package_funcs.md#func-gcbool) 替代。

参数：

- heavy!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - [GC](runtime_package_funcs.md#func-gcbool-deprecated) 执行程度，如果为 true，执行会慢，内存收集的多一些，默认值为 false。

## func getAllocatedHeapSize()

```cangjie
public func getAllocatedHeapSize(): Int64
```

功能：获取仓颉堆已被使用的大小，单位为 byte。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 仓颉堆已被使用的大小，单位为 byte。

## func getBlockingThreadCount()

```cangjie
public func getBlockingThreadCount(): Int64
```

功能：获取阻塞的仓颉线程数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 阻塞的仓颉线程数。

## func getGCCount()

```cangjie
public func getGCCount(): Int64
```

功能：获取触发 GC 的次数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 触发 GC 的次数。

## func getGCFreedSize()

```cangjie
public func getGCFreedSize(): Int64
```

功能：获取触发 GC 后，成功回收的内存，单位为 byte。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 触发 GC 后，成功回收的内存，单位为 byte。

## func getGCTime()

```cangjie
public func getGCTime(): Int64
```

功能：获取触发的 GC 总耗时，单位为 us。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 触发的 GC 总耗时，单位为 us。

## func getMaxHeapSize()

```cangjie
public func getMaxHeapSize(): Int64
```

功能：获取仓颉堆可以使用的最大值，单位为 byte。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 仓颉堆可以使用的最大值，单位为 byte。

## func getNativeThreadCount()

```cangjie
public func getNativeThreadCount(): Int64
```

功能：获取物理线程数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 物理线程数。

## func getProcessorCount()

```cangjie
public func getProcessorCount(): Int64
```

功能：获取处理器数量。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 处理器数量。

## func getThreadCount()

```cangjie
public func getThreadCount(): Int64
```

功能：获取仓颉当前的线程数量。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 仓颉当前的线程数量。

## func getUsedHeapSize()

```cangjie
public func getUsedHeapSize(): Int64
```

功能：在 Linux 平台下获取仓颉堆实际占用的物理内存大小，单位为 byte。在 Windows 及 macOs 平台下获取仓颉进程实际占用的物理内存大小，单位为 byte。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 仓颉堆或仓颉进程实际占用的物理内存大小，单位为 byte。

## func setGCThreshold(UInt64)

```cangjie
public func setGCThreshold(value: UInt64): Unit
```

功能：修改用户期望触发 [gc](runtime_package_funcs.md#func-gcbool) 的内存阈值，当仓颉堆大小超过该值时，触发 [gc](runtime_package_funcs.md#func-gcbool)，单位为 KB。

参数：

- value: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 用户期望触发 [gc](runtime_package_funcs.md#func-gcbool) 的内存阈值。

示例：
设置用户期望的 [gc](runtime_package_funcs.md#func-gcbool) 的内存阈值为 2MB。

<!-- run -->

```cangjie
import std.runtime.*
main() {
  setGCThreshold(2048)
}
```

## func SetGCThreshold(UInt64) <sup>(deprecated)</sup>

```cangjie
public func SetGCThreshold(value: UInt64): Unit
```

功能：修改用户期望触发 [GC](runtime_package_funcs.md#func-gcbool-deprecated) 的内存阈值，当仓颉堆大小超过该值时，触发 [GC](runtime_package_funcs.md#func-gcbool-deprecated)，单位为 KB。

> **注意：**
>
> 未来版本即将废弃，使用 [setGCThreshold(UInt64)](./runtime_package_funcs.md#func-setgcthresholduint64) 替代。

参数：

- value: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 用户期望触发 [GC](runtime_package_funcs.md#func-gcbool-deprecated) 的内存阈值。

示例：
设置用户期望的 [GC](runtime_package_funcs.md#func-gcbool-deprecated) 的内存阈值为 2MB。

<!-- run -->

```cangjie
import std.runtime.*
main() {
  SetGCThreshold(2048)
}
```

## func startCPUProfiling()

```cangjie
public func startCPUProfiling(): Unit
```

功能：启动 CPU profiler 跟踪。

> **注意：**
>
> [startCPUProfiling](./runtime_package_funcs.md#func-startcpuprofiling) 与 [stopCPUProfiling(Path)](./runtime_package_funcs.md#func-stopcpuprofilingpath) 两个函数必须一一对应。

异常：

- ProfilingInfoException - 若调用了 [startCPUProfiling](./runtime_package_funcs.md#func-startcpuprofiling) 后，没有调用 [stopCPUProfiling(Path)](./runtime_package_funcs.md#func-stopcpuprofilingpath)，而是又调用了 [startCPUProfiling](./runtime_package_funcs.md#func-startcpuprofiling) 则抛出异常。

## func stopCPUProfiling(Path)

```cangjie
public func stopCPUProfiling(path: Path): Unit
```

功能：停止 CPU profiler 跟踪，并将记录写入指定路径的文件。

> **注意：**
>
> [startCPUProfiling](./runtime_package_funcs.md#func-startcpuprofiling) 与 [stopCPUProfiling(Path)](./runtime_package_funcs.md#func-stopcpuprofilingpath) 两个函数必须一一对应。

参数：

- path: [Path](../../fs/fs_package_api/fs_package_structs.md#struct-path) - 生成记录文件的文件路径。

异常：

- ProfilingInfoException - 若没有调用了 [startCPUProfiling](./runtime_package_funcs.md#func-startcpuprofiling)，直接调用 [stopCPUProfiling(Path)](./runtime_package_funcs.md#func-stopcpuprofilingpath) 则抛出异常。
