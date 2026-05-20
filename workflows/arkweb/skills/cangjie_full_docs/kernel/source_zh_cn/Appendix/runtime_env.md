# runtime 环境变量使用手册

本节介绍 `runtime`（运行时）所提供的环境变量。

在 Linux shell 与 macOS shell 中，可以使用以下方式设置仓颉运行时提供的环境变量：

```shell
$ export VARIABLE=value
```

在 Windows cmd 中，可以使用以下方式设置仓颉运行时提供的环境变量：

```shell
> set VARIABLE=value
```

本节后续的示例均为 Linux shell 中的设置方式，若与运行平台不符，请根据运行平台选择合适的环境变量设置方式。

## runtime 初始化可选配置

注意：

1. 所有整型参数为 Int64 类型，浮点型参数为 Float64 类型；
2. 所有参数如果未显式规定最大值，默认隐式最大值为该类型最大值；
3. 所有参数若超出范围则设置无效，自动使用默认值；
4. 所有参数在 OpenHarmony 平台下均无效，OpenHarmony 平台下仓颉运行时使用默认值。

### `cjHeapSize`

指定仓颉堆的最大值，支持单位为 kb（KB）、mb（MB）、gb（GB），支持设置范围为[4MB, 系统物理内存]，超出范围的设置无效，仍旧使用默认值。若物理内存低于 1GB，默认值为 64 MB，否则为 256 MB。

例如：

```shell
export cjHeapSize=4GB
```

### `cjRegionSize`

指定 region 分配器 thread local buffer 的大小，支持单位为 kb（KB）、mb（MB）、gb（GB)，支持设置范围为[4kb, 2048kb]，超出范围的设置无效，仍旧使用默认值。默认值为 64 KB。

例如：

```shell
export cjRegionSize=1024kb
```

### `cjLargeThresholdSize`

需要大量连续内存空间的对象（例如长数组）称为大对象。堆内频繁分配大对象可能导致堆内连续空间不足，从而触发堆溢出问题。通过增加大对象的最大值，可以提升堆内空间的连续性。

在仓颉语言中，大对象的阈值为 `cjLargeThresholdSize` 和 `cjRegionSize` 的较小者。`cjLargeThresholdSize` 支持的单位有 kb（KB）、mb（MB）、gb（GB)，支持的范围是 [4KB, 2048KB]，超出范围的设置无效，仍旧使用默认值。默认值为 32 KB。

> **说明：**
>
> 较大的大对象阈值可能影响程序性能，开发者可根据实际情况设置。

例如：

```shell
export cjLargeThresholdSize=1024kb
```

### `cjExemptionThreshold`

指定存活 region 的水线值，取值 (0,1]，该值与 region 的大小相乘，若 region 中存活对象的大小大于相乘后的值，则该 region 不会被回收（其中死亡对象继续占用内存）。该值指定得越大，region 被回收的概率越大，堆中的碎片空间就越少，但频繁回收 region 也会影响性能。超出范围的设置无效，仍旧使用默认值。默认值为 0.8，即 80%。

例如：

```shell
export cjExemptionThreshold=0.8
```

### `cjHeapUtilization`

指定仓颉堆的利用率，该参数用于 GC 后更新堆水线的参考依据之一，取值 (0, 1]，堆水线是指当堆中对象总大小达到水线值时则进行 GC。该参数指定越小，则更新后的堆水线会越高，则触发 GC 的概率会相对变低。超出范围的设置无效，仍旧使用默认值。默认值为 0.8，即 80%。

例如：

```shell
export cjHeapUtilization=0.8
```

### `cjHeapGrowth`

指定仓颉堆的增长率，该参数用于 GC 后更新堆水线的参考依据之一，取值必须大于 0。增长率的计算方式为 1 + cjHeapGrowth。该参数指定越大，则更新后的堆水线会越高，则触发 GC 的概率会相对变低。默认值为 0.15，表示增长率为 1.15。

例如：

```shell
export cjHeapGrowth=0.15
```

### `cjAlloctionRate`

指定仓颉运行时分配对象的速率，该值必须大于 0，单位为 MB/s，表示每秒可分配对象的数量。默认值为 10240，表示每秒可分配 10240 MB 对象。

例如：

```shell
export cjAlloctionRate=10240
```

### `cjAlloctionWaitTime`

指定仓颉运行时分配对象时的等待时间，该值必须大于 0，支持单位为 s、ms、us、ns，推荐单位为纳秒（ns）。若本次分配对象距离上一次分配对象的时间间隔小于此值，则将等待。默认值为 1000 ns。

例如：

```shell
export cjAlloctionWaitTime=1000ns
```

### `cjGCThreshold`

指定仓颉堆的参考水线值，支持单位为 kb（KB）、mb（MB）、gb（GB）, 取值必须为大于 0 的整数。当仓颉堆大小超过该值时，触发 GC。默认值为堆大小。

例如：

```shell
export cjGCThreshold=20480KB
```

### `cjGarbageThreshold`

当 GC 发生时，如果 region 中死亡对象所占比率大于此环境变量，此 region 会被放入回收候选集中，后续可被回收（如果受到其他策略影响也可能不被回收），默认值为 0.5，无量纲，支持设置的区间为[0.0, 1.0]。

例如：

```shell
export cjGarbageThreshold=0.5
```

### `cjGCInterval`

指定两次 GC 的间隔时间值，取值必须大于 0，支持单位为 s、ms、us、ns，推荐单位为毫秒（ms）。若本次 GC 距离上次 GC 的间隔小于此值，则本次 GC 将被忽略。该参数可以控制 GC 的频率。默认值为 150 ms。

例如：

```shell
export cjGCInterval=150ms
```

### `cjBackupGCInterval`

指定 backup GC 的间隔值，取值必须大于 0，支持单位为 s、ms、us、ns，推荐单位为秒（s），当仓颉运行时在该参数设定时间内未触发 GC，则触发一次 backup GC。默认值为 240 秒，即 4 分钟。

例如：

```shell
export cjBackupGCInterval=240s
```

### `cjProcessorNum`

指定仓颉线程的最大并发数，支持设置范围为 (0, CPU 核数 * 2]，超出范围的设置无效，仍旧使用默认值。调用系统 API 获取 cpu 核数，若成功默认值为 cpu 核数，否则默认值为 8。

例如：

```shell
export cjProcessorNum=2
```

### `cjStackSize`

指定仓颉线程的栈大小，支持单位为 kb（KB）、mb（MB）、gb（GB），支持设置范围为 Linux 平台下[64KB, 1GB]，Windows 平台下[128KB, 1GB]，超出范围的设置无效，仍旧使用默认值。默认值为 128KB。

例如：

```shell
export cjStackSize=100kb
```

### 运维日志可选配置

#### `MRT_LOG_FILE_SIZE`

指定 runtime 运维日志的文件大小，默认值为 10 MB，支持单位为 kb（KB）、mb（MB）、gb（GB），设置值需大于 0。

日志大小超过该值时，会重新回到日志开头进行打印。

最终生成日志大小略大于 MRT_LOG_FILE_SIZE。

例如：

```shell
export MRT_LOG_FILE_SIZE=100kb
```

#### `MRT_LOG_PATH`

指定 runtime 运维日志的输出路径，若该环境变量未设置或路径设置失败，则运维日志默认打印到 stdout（标准输出）或 stderr（标准错误）中。

例如：

```shell
export MRT_LOG_PATH=/home/cangjie/runtime/runtime_log.txt
```

#### `MRT_LOG_LEVEL`

指定 runtime 运维日志的最小输出级别，大于等于这个级别的日志会被打印，默认值为 e，支持设置值为[v|d|i|w|e|f|s]。v（VERBOSE）、d（DEBUGY）、i（INFO）、w（WARNING）、e（ERROR）、f（FATAL）、s（FATAL_WITHOUT_ABORT）。

例如：

```shell
export MRT_LOG_LEVEL=v
```

#### `MRT_REPORT`

指定 runtime GC 日志的输出路径，若该环境变量未设置或路径设置失败，该日志默认不打印。

例如：

```shell
export MRT_REPORT=/home/cangjie/runtime/gc_log.txt
```

#### `MRT_LOG_CJTHREAD`

指定 cjthread 日志的输出路径，若该环境变量未设置或路径设置失败，该日志默认不打印。

例如：

```shell
export MRT_LOG_CJTHREAD=/home/cangjie/runtime/cjthread_log.txt
```

#### `cjHeapDumpOnOOM`

指定是否要在发生堆溢出后输出堆快照文件，默认不开启。支持设置值为[on|off]，设定为 on 时开启功能，设定 off 或者其他值不开启功能。

例如：

```shell
export cjHeapDumpOnOOM=on
```

#### `cjHeapDumpLog`

指定输出堆快照文件的路径。注意指定的路径必须存在，且应用执行者对其具有读写权限。如果不指定，堆快照文件将输出到当前执行目录。

例如：

```shell
export cjHeapDumpLog=/home/cangjie
```

### 运行环境可选配置

#### `MRT_STACK_CHECK`

开启 native stack overflow 检查，默认不开启，支持设置值为 1、true、TRUE 开启功能。

例如：

```shell
export MRT_STACK_CHECK=true
```

#### `CJ_SOF_SIZE`

当 StackOverflowError 发生时，将自动进行异常栈折叠方便用户阅读，折叠后栈帧层数默认值是 32。可以通过配置此环境变量控制折叠栈长度，支持设置为 int 范围内的整数。
CJ_SOF_SIZE = 0，打印所有调用栈；
CJ_SOF_SIZE < 0，从栈底开始打印环境变量配置层数；
CJ_SOF_SIZE > 0，从栈顶开始打印环境变量配置层数；
CJ_SOF_SIZE 未配置，默认打印栈顶开始 32 层调用栈；

例如：

```shell
export CJ_SOF_SIZE=30
```

### 仓颉 GWP-Asan 内存安全检测

在仓颉与 C 代码互操作的过程中，可能出现一些仓颉堆内存安全问题。仓颉 GWP-Asan 提供了一种内存安全检测功能。它可以在仓颉程序运行过程中检测代码是否存在仓颉堆内存安全问题。GWP-Asan 通过对仓颉语言标准库提供的 acquireArrayRawData 和 releaseArrayRawData 接口（参见《仓颉编程语言库 API 文档》std.core 包一节）进行采样，并记录对比采样对象前后内存的 Canary 数据，从而检测仓颉与 C 语言互操作过程中是否出现了仓颉堆内存安全问题。

仓颉 GWP-Asan 是一种基于采样的检测工具，可以通过设置不同的值来调整采样频率，以平衡性能影响和检测覆盖率。在默认或更低采样频率下，CPU 性能损失和额外的内存占用极低。

> **说明：**
>
> 仓颉 GWP-Asan 内存安全检测仅支持 Linux 和 HarmonyOS 操作系统。

#### cjEnableGwpAsan

仓颉 GWP-Asan 内存安全检测功能默认关闭。通过将环境变量 `cjEnableGwpAsan` 设置为 `1`、`true` 或 `TRUE` 可以开启该功能。Linux 下设置参考如下：

```shell
export cjEnableGwpAsan=true
```

#### cjGwpAsanSampleRate

在仓颉 GWP-Asan 内存安全检测功能开启状态下，通过环境变量 `cjGwpAsanSampleRate` 设置采样频率。`cjGwpAsanSampleRate` 支持设置为 32 位整形数值范围内的正整数，即 $(0, 2^{31} - 1]$ 。默认值为 5000，即每 5000 次 acquireArrayRawData 接口调用，进行一次采样。Linux 设置参考如下：

```shell
export cjGwpAsanSampleRate=1000
```

> **说明：**
>
> 仓颉 GWP-Asan 内存安全检测中，采样会影响性能。采样率越高，对性能影响越大，能检出更多的问题；采样率越低，其对性能影响越小，能检出更少的问题。请根据实际情况设置采样率。

#### cjGwpAsanHelp

通过环境变量 `cjGwpAsanHelp` 可以设置是否在控制台输出 GWP-Asan 帮助信息。默认不开启。`cjGwpAsanHelp` 设置为`1`、`true` 或 `TRUE` 时，表示在控制台输出帮助信息。Linux 设置参考如下：

```shell
export cjGwpAsanHelp=true
```

#### 约束限制

- 仓颉 GWP-Asan 是一种基于采样的内存检查工具，内存越界问题可能无法完全检出。
- 仓颉 GWP-Asan 对仓颉堆内存的越界检测范围有限，无法检测内存读越界访问，仅能检测部分写越界访问：向前写越界 8 字节以内；向后写越界到尾部的填充区域（根据数组对象长度的不同，填充区域可能为 0-7 字节）。

#### 异常检测类型

**堆内存写越界**

堆内存写越界指的是，指针实际访问的内存长度超过了数组申请的长度，造成仓颉堆内存写越界。

1. 向前越界

    向前越界数组时，runtime 会报告 Head canary 检测失败，使用 `array[-1]` 表示。例如：

    ```cangjie
    unsafe {
        let array = Array<UInt8>(4, item: 0)
        let cp = acquireArrayRawData(array)
        // array 数组实际可访问的范围是 [0, 4)，而下述写操作访问了第 -2 个字节，导致仓颉堆内存向前溢出 2 个字节。错误报告中使用 array[-1] 表示该向前越界行为。
        cp.pointer.read(-2)
        releaseArrayRawData(array)
    }
    ```

    对应的错误报告如下：

    ```text
    2025-05-22 10:57:13.432786 41217 F Gwp-Asan sanity check failed on raw array addr 0x7f7c887368
    2025-05-22 10:57:13.432863 41217 F Head canary (array[-1]) mismatch: expect: 0x2, actual: 0x200000000000002
    2025-05-22 10:57:13.432878 41217 F Gwp-Asan Aborted.
    ```

2. 向后越界

    向后越界数组时，runtime 会报告 Tail canary 检测失败，并给出相对该数组（`array`）的位置。例如：

    ```cangjie
    unsafe {
        let array = Array<UInt8>(4, item: 0)
        let cp = acquireArrayRawData(array)

        // array 数组实际可访问的范围是 [0, 4)，而下述写操作访问了第 6 个字节，导致仓颉堆内存向前溢出 2 个字节。错误报告中使用 array[size+1] 表示该向后越界行为。
        cp.pointer.read(5)
        releaseArrayRawData(array)
    }
    ```

    对应的错误报告如下：

    ```text
    2025-05-22 10:53:09.564580 37872 F Gwp-Asan sanity check failed on raw array addr 0x7f6278a368
    2025-05-22 10:53:09.564761 37872 F Tail canary (array[size+1]) mismatch: expect: 0x6, actual: 0x2
    2025-05-22 10:53:09.564788 37872 F Gwp-Asan Aborted.
    ```

**仓颉 GC（Garbage Collection）异常**

使用 acquireArrayRawData 获取了数组的指针，但是未配套使用 releaseArrayRawData 释放数组的引用，可能造成仓颉 GC（Garbage Collection）异常。

在 runtime 退出时会检测被采样的数组是否调用了 releaseArrayRawData 释放。未释放时，会报告所有未释放的数组对应的堆地址。例如：

```cangjie
unsafe {
    let array = Array<UInt8>(4, item: 0)
    let cp = acquireArrayRawData(array)
    cp.pointer.read()

    // 未使用 releaseArrayRawData
    return
}
```

对应的错误报告如下：

```text
2025-05-22 10:53:09.564761 1248614 F Unreleased array: 0x7fffd77f92d8
2025-05-22 10:53:09.564788 1248614 F Detect un-released array
```
