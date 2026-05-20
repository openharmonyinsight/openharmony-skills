# std.runtime

## 功能介绍

runtime 包的作用是与程序的运行时环境进行交互，提供了一系列函数和变量，用于控制、管理和监视程序的执行。

Cangjie 语言使用自动垃圾回收机制来管理内存，runtime 包提供了手动触发垃圾回收、设置垃圾回收的阈值、获取内存统计信息等功能，用于对垃圾回收进行调控和监测。

## API 列表

### 函数

|              函数名          |           功能           |
| --------------------------- | ------------------------ |
| [blackBox\<T>(T)](./runtime_package_api/runtime_package_funcs.md#func-blackboxtt) | 指示编译器传入的变量进入优化黑盒，无法进行死代码消除等优化。 |
| [dumpHeapData(Path)](./runtime_package_api/runtime_package_funcs.md#func-dumpheapdatapath) | 生成堆内存快照信息，写入指定路径的文件。 |
| [GC(Bool) <sup>(deprecated)</sup>](./runtime_package_api/runtime_package_funcs.md#func-gcbool-deprecated) | 执行 GC。 |
| [gc(Bool)](./runtime_package_api/runtime_package_funcs.md#func-gcbool) | 执行 GC。 |
| [getAllocatedHeapSize](./runtime_package_api/runtime_package_funcs.md#func-getallocatedheapsize) | 获取仓颉堆已被使用的大小，单位为 byte。 |
| [getBlockingThreadCount](./runtime_package_api/runtime_package_funcs.md#func-getblockingthreadcount) | 获取阻塞的仓颉线程数。 |
| [getGCCount](./runtime_package_api/runtime_package_funcs.md#func-getgccount) | 获取触发 GC 的次数。 |
| [getGCFreedSize](./runtime_package_api/runtime_package_funcs.md#func-getgcfreedsize) | 获取触发 GC 后，成功回收的内存，单位为 byte。 |
| [getGCTime](./runtime_package_api/runtime_package_funcs.md#func-getgctime) | 获取触发的 GC 总耗时，单位为 us。 |
| [getMaxHeapSize](./runtime_package_api/runtime_package_funcs.md#func-getmaxheapsize) | 获取仓颉堆可以使用的最大值，单位为 byte。 |
| [getNativeThreadCount](./runtime_package_api/runtime_package_funcs.md#func-getnativethreadcount) | 获取物理线程数。 |
| [getProcessorCount](./runtime_package_api/runtime_package_funcs.md#func-getprocessorcount) | 获取处理器数量。 |
| [getThreadCount](./runtime_package_api/runtime_package_funcs.md#func-getthreadcount) | 获取仓颉当前的线程数量。 |
| [getUsedHeapSize](./runtime_package_api/runtime_package_funcs.md#func-getusedheapsize) | 在 Linux 平台下获取仓颉堆实际占用的物理内存大小，单位为 byte。在 Windows 及 macOs 平台下获取仓颉进程实际占用的物理内存大小，单位为 byte。 |
| [SetGCThreshold(UInt64) <sup>(deprecated)</sup>](./runtime_package_api/runtime_package_funcs.md#func-setgcthresholduint64-deprecated) | 修改用户期望触发 GC 的内存阈值，当仓颉堆大小超过该值时，触发 GC，单位为 KB。 |
| [setGCThreshold(UInt64)](./runtime_package_api/runtime_package_funcs.md#func-setgcthresholduint64) | 修改用户期望触发 GC 的内存阈值，当仓颉堆大小超过该值时，触发 GC，单位为 KB。 |
| [startCPUProfiling](./runtime_package_api/runtime_package_funcs.md#func-startcpuprofiling) | 启动 CPU profiler 跟踪。 |
| [stopCPUProfiling(Path)](./runtime_package_api/runtime_package_funcs.md#func-stopcpuprofilingpath) | 停止 CPU profiler 跟踪，并将记录写入指定路径的文件。 |

### 结构体

|              结构体名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [MemoryInfo <sup>(deprecated)</sup>](./runtime_package_api/runtime_package_structs.md#struct-memoryinfo-deprecated) | 提供获取一些堆内存统计数据的接口。 |
| [ProcessorInfo <sup>(deprecated)</sup>](./runtime_package_api/runtime_package_structs.md#struct-processorinfo-deprecated) | 提供获取一些处理器信息的接口。 |
| [ThreadInfo <sup>(deprecated)</sup>](./runtime_package_api/runtime_package_structs.md#struct-threadinfo-deprecated) | 提供获取一些仓颉线程统计数据的接口。 |
