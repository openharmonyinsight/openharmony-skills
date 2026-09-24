# 两种内核接入方式详解：厂商内核适配 vs. QEMU 直接编译

> 源码位置（远程）：`/srv/workspace/openharmony_master_default_20260628174411_huawei_f518361fa/code/`
> 面向读者：没有芯片开发背景
> 分析日期：2026-07-02

---

## 第 0 步：先建立四个基本概念

在讲接入方式之前，先用生活化的比喻统一四个词。

### 1. 内核（Kernel）= 设备的"发动机"（一段软件，不是硬件）

内核是一段负责"管任务调度、管内存、管中断、管硬件驱动"的基础**软件代码**。
没有它，芯片只是一坨通电的硅。它就像汽车的发动机——你踩油门（调用 API），它决定怎么喷油、怎么转曲轴。

> ⚠️ 一个关键区分：**内核是软件，不是长在硅片上的硬件。** 它和芯片的关系是"运行/存放"关系，不是"焊接"关系。
> 准确的过程是：内核代码被**烧录进芯片的闪存（Flash）**里持久保存；开机时由一小段启动代码（bootloader）把它从 Flash **搬进 RAM**，然后 CPU 核心开始**执行**它。从这一刻起，内核"常驻" RAM 指挥全局。
>
> 所以"内核装在芯片硬件本体上"这个说法——**大体对，但要修正一点**：内核最终确实物理地落在芯片的 Flash 里，但它是**可擦写、可替换的软件**，不是芯片出厂就烧死的硬件。同一块 hi3861，烧鸿蒙 Mini 镜像它就是鸿蒙设备，烧别的镜像它就是别的东西，硅片本身没变。这也是"芯片适配 OH"能成立的前提。

### 2. OH 接口（KAL）= "标准驾驶座"

OpenHarmony 不希望上层应用（比如软总线 softbus、日志 hiview、安全组件）每换一块芯片就要重写一遍。
所以 OH 定义了一套**标准 API**，要求所有应用只调这套 API：

- `osThreadNew(...)` —— 创建一个任务（线程）
- `osDelay(...)` —— 让任务睡一会儿
- `osMutexAcquire(...)` —— 抢一把锁

这套标准 API 在 Mini 系统里叫 **CMSIS-RTOS2**（再加一套精简 POSIX）。
它就像"标准驾驶座"——油门、刹车、方向盘的位置都规定好了，只要座舱符合这个标准，司机（应用）坐上去就能开，不用管底下是汽油机还是柴油机。

### 3. 适配层（Adapter）= "转接头"

如果厂商的发动机（内核）控制指令不是 `osThreadNew` 而是 `LOS_TaskCreate`，
那"标准驾驶座"就和"发动机"对不上。解决办法：中间加一个**翻译官 / 转接头**，
把 `osThreadNew` 翻译成 `LOS_TaskCreate`。这个转接头就是适配层。

### 4. 闪存（Flash）= 芯片里的"可擦写硬盘"

内核这段软件代码，平时存在哪里？答案是**闪存（Flash）**——一种断电不丢、又可电擦电写的存储颗粒。

> ⚠️ 别被"封在芯片内部"误导成"只读不可改"。要分清两件正交的事：
>
> | | 封装在芯片内部 | 封装在芯片外部（板载颗粒）|
> |---|---|---|
> | **可擦写**（Flash，如 NOR/NAND） | ✅ hi3861 就是这种 | ✅ 手机主板上的 eMMC/UFS |
> | **出厂只读**（Mask ROM / OTP） | ✅ 通常是 bootloader 那一小段 | 较少见 |
>
> - **内部 Flash**＝和 CPU 核心封在同一颗塑料封装里，但本质还是 Flash 颗粒，**可反复擦写**（典型 10 万次量级）。"内部"只意味着体积小、走片内总线更快，**不影响可写性**。
> - **真正不可改的**是 **ROM**（Mask ROM 烧死在硅片制造工艺里，或 OTP 一次性可写）。芯片上电最先跑的那小段 bootloader 常放 ROM，保证出厂固定、不会被写坏；但**内核和应用放在 Flash 里，可改**。
>
> 所以 hi3861 的内部 Flash（约 2 MB，塞下 bootloader + Huawei_LiteOS 内核 + OH 组件 + 应用 + NV 参数）和"硬盘"一样可反复擦写：今天烧鸿蒙 Mini 镜像，明天改了应用代码，重新擦写一次即可，硅片本身没动。
>
> 反直觉的缘由：早期很多低端单片机用 OTP 或 Mask ROM，确实写一次就定型，这种印象被带到了现代 SoC 上。但 hi3861 这类现代 IoT SoC 用的是闪存工艺，天生支持电擦电写（写之前先按块擦，是 Flash 的物理特性）。

> 一句话：**OH 接口是契约，厂商内核是实物，适配层是让实物满足契约的转接头；而内核这段软件最终烧在芯片内部可擦写的 Flash 里，开机进 RAM、由 CPU 执行。**

---

## 方式 A：厂商内核 + 适配 OH 接口（hi3861v100 / ws63v100 的做法）

### 整体形态

```
┌─────────────────────────────────────────────┐
│  上层 OH 应用/组件                            │   ← samgr、hiview、softbus、security…
│  只会调用标准 API：osThreadNew / osDelay…    │   ← 司机只认标准驾驶座
└──────────────────┬──────────────────────────┘
                   │ 调用 osThreadNew()（CMSIS-RTOS2 标准接口）
                   ▼
┌─────────────────────────────────────────────┐
│  适配层 *_adapter/kal/                       │   ← 转接头（源码，OH 侧可编译）
│  把 osThreadNew 翻译成 LOS_TaskCreate        │
└──────────────────┬──────────────────────────┘
                   │ 调用 LOS_TaskCreate()（厂商内核原生 API）
                   ▼
┌─────────────────────────────────────────────┐
│  厂商内核 Huawei_LiteOS（预编译 .a 二进制）  │   ← 发动机（不开放源码参与编译）
│  真正干活：调度任务、管内存、跑中断          │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
                 硬件 (hi3861 芯片)
```

### 这意味着什么——四个关键点

#### ① 内核是"黑盒二进制"，OH 不编译它

`vendor/hisilicon/hispark_pegasus/config.json`：
```json
"kernel_type": "liteos_m",
"kernel_is_prebuilt": true,      // ← 内核是预制品，OH 构建系统不编译它
```
对应的预编译产物放在 `sdk_liteos/ohos/libs/*.a`，比如 `libcmsis.a`、`libposix.a`、`libbase.a`。
`.a` 是静态库（一组编译好的二进制代码），就像买回来的"成品发动机总成"——你不再拆开重造，直接装车。

#### ② OH 仓库里那份开源 `kernel/liteos_m` 内核源码，根本没被编进去

hi3861 全相关目录搜索 `//kernel/liteos_m` 的引用，只命中两类：
```
//kernel/liteos_m/kal                  ← 只是 KAL 接口的头文件声明
//kernel/liteos_m/components/cmsis/2.0 ← 只是 CMSIS-RTOS2 的头文件
```
也就是说：**开源 LiteOS-M 内核的源码（调度器、内存管理…）一行都没编译进 hi3861 镜像**。
被借用的只是"接口头文件"——告诉上层"osThreadNew 长这个签名"，让应用能编译通过。

#### ③ 真正的内核是厂商自带的 Huawei_LiteOS

`config.gni` 的头文件搜索路径暴露真相：
```
.../sdk_liteos/platform/os/Huawei_LiteOS/kernel/base/include
.../sdk_liteos/platform/os/Huawei_LiteOS/arch/risc-v/rv32im
```
这台"发动机"是海思自己长期维护的 Huawei_LiteOS（早于 OH 开源 LiteOS-M 多年，量产验证过），
完整源码树在 `sdk_liteos/platform/os/Huawei_LiteOS/{arch,components,kernel,targets}`，但**作为 SDK 的一部分发行，不参与 OH 主构建**。

#### ④ 适配层是源码、可编译，是"接入"的核心动作

适配层代码长什么样？看 `hi3861_adapter/kal/cmsis/cmsis_liteos2.c`（已简化）：

```c
// 上层应用调用的"标准 API"长这样：
osThreadId_t osThreadNew(osThreadFunc_t func, void *argument,
                         const osThreadAttr_t *attr) {
    TSK_INIT_PARAM_S stTskInitParam = {0};
    stTskInitParam.pfnTaskEntry = (TSK_ENTRY_FUNC)func;
    stTskInitParam.auwArgs[0] = (UINTPTR)argument;
    stTskInitParam.usTaskPrio   = OS_TASK_PRIORITY_LOWEST - attr->priority;
    // ↓↓↓ 这一行就是"翻译"：把 CMSIS 标准调用转成厂商内核调用
    uwRet = LOS_TaskCreate(&uwTid, &stTskInitParam);
    if (LOS_OK != uwRet) return NULL;
    return (osThreadId_t)uwTid;
}
```

**一次完整调用的链路**（以"应用想创建一个任务"为例）：

```
应用代码:  osThreadNew(myTask, NULL, &attr)        // 应用只懂标准 API
              │
              ▼
适配层:    osThreadNew() { ... LOS_TaskCreate(...) } // 翻译官：标准→厂商
              │
              ▼
厂商内核:  LOS_TaskCreate()  →  把任务挂入调度队列、分配栈
              │
              ▼
硬件:      任务真正在 hi3861 上跑起来
```

这就是"适配接入"的全部本质：**上层不变、内核不变，中间加一层翻译**。

### 为什么厂商要走这条路

1. **厂商内核成熟且量产**：Huawei_LiteOS 自带完整 WiFi 协议栈、低功耗管理、烧写工具链、过认证的驱动。换成开源 LiteOS-M 等于推倒重来，风险与成本不可接受。
2. **OH 设计本就允许内核可替换**：只要套上 KAL 适配，上层 OH 组件原样跑。`kernel_is_prebuilt: true` 这条机制就是为这条路准备的。
3. **保护私有资产**：内核以 `.a` 形式发行，核心实现不开放源码。

---

## 方式 B：QEMU 直接编译链接开源 LiteOS-M

### 整体形态

```
┌─────────────────────────────────────────────┐
│  上层 OH 应用/组件                            │   ← 司机
│  调用 osThreadNew / osDelay…                 │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  开源 kernel/liteos_m 内核（源码，参与编译）  │   ← 标准发动机 + 标准座舱一体
│  本身就实现了 CMSIS-RTOS2 和 LOS_* 两套接口  │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
        QEMU 模拟的虚拟开发板（纯软件）
```

### 关键证据：构建脚本直接 import 开源内核

`device/qemu/esp32/liteos_m/board/BUILD.gn`：
```gn
import("//kernel/liteos_m/liteos.gni")     // ← 把开源 LiteOS-M 内核构建体系拉进来

kernel_module("bsp_config") {
  sources = [                               // 板子只提供少量 BSP 代码
    "fs/fs_init.c",
    "hals/driver/hal_watchdog.c",
    "main.c",
  ]
}
```

`import("//kernel/liteos_m/liteos.gni")` 这一行意味着：**开源 LiteOS-M 的全部内核源码（调度器、内存管理、中断管理、CMSIS 实现…）都会被编译进最终镜像**。板子侧只补一点点"启动 + 硬件相关"代码（`main.c`、看门狗 HAL、文件系统初始化）。

### 这意味着什么

- **没有"翻译官"**：开源 LiteOS-M 自己就同时实现了 `osThreadNew`（CMSIS 标准接口）和 `LOS_TaskCreate`（原生接口）——它本身就是按 OH 标准造的发动机，座舱和发动机出厂就配套，不需要转接头。
- **没有预编译 `.a` 黑盒**：内核源码全公开、全参与编译，你能看到每一行调度代码。
- **跑在虚拟板上**：QEMU 是纯软件模拟的开发板，没有真实硬件，所以内核可以直接用源码编译，无需厂商提供 SDK。

---

## 两种方式的对比（核心差异一表看清）

| 维度 | 方式 A：厂商内核适配 | 方式 B：QEMU 直接编译 |
|---|---|---|
| **内核来源** | 厂商自有 Huawei_LiteOS（预编译 `.a`） | 仓库内开源 `kernel/liteos_m`（源码） |
| **OH 是否编译内核** | 否（`kernel_is_prebuilt: true`） | 是（`import("//kernel/liteos_m/liteos.gni")`） |
| **是否需要适配层** | **是**（`*_adapter/kal`，CMSIS→LOS_*） | 否（内核原生提供两套接口） |
| **上层应用调用** | `osThreadNew` → 适配层 → `LOS_TaskCreate` | `osThreadNew` → 内核直接实现 |
| **内核可见性** | 黑盒二进制 | 全源码可见可改 |
| **运行目标** | 真实芯片（hi3861/ws63） | QEMU 虚拟开发板 |
| **典型代表** | hi3861v100、ws63v100 | esp32_qemu、arm_mps2_an386、riscv32_virt |
| **定位** | 量产路线 | 参考实现 / 学习骨架 |

### 一个比喻总结

- **方式 A（厂商适配）**：你买了一台整车（厂商内核 `.a`），但它的方向盘接口和 OH 标准驾照不兼容。于是你装一个方向盘转接头（适配层），让你的标准驾照（上层应用）能开这台车。
- **方式 B（QEMU 直接编译）**：你照着 OH 标准图纸，自己用零件（开源内核源码）造了一台车，方向盘本来就是标准的，不用转接头，直接能开。但这台车是虚拟的（QEMU），上不了真路，只能在模拟器里跑。

---

## 为什么 OH 同时保留两条路

- **没有方式 B**：社区开发者没有真芯片，没法学习、没法验证 OH Mini 系统怎么跑——所以必须有 QEMU 直接编译的参考实现。
- **没有方式 A**：真实量产芯片上不了 OH——因为厂商不可能抛弃成熟内核重写。所以必须有"预编译内核 + 适配层"的机制，让厂商内核能无缝接入。

两条路通过同一个契约（CMSIS-RTOS2 / POSIX Lite KAL）打通：**上层 OH 组件代码完全一致，换的只是底下"发动机 + 是否需要转接头"**。这就是 OpenHarmony "内核可替换"设计的精髓。

---

## 深入：CMSIS 翻译层与换内核的边界

### 5. CMSIS 翻译层 = "标准语→方言"的翻译官

**CMSIS** = ARM 定的 Cortex-M 微控制器软件接口标准。其中 **CMSIS-RTOS2** 规定了一套跨厂商统一的 RTOS API：`osThreadNew` / `osDelay` / `osMutexAcquire`…。但每个 RTOS 内部函数不一样（LiteOS 用 `LOS_TaskCreate`，FreeRTOS 用 `xTaskCreate`），中间需要翻译层把 `os*` 翻译成内核原生 API。

`cmsis_liteos2.c`（文件名 = CMSIS-RTOS2 跑在 LiteOS 上）里 `osThreadNew` 的实现简化后：
```c
osThreadId_t osThreadNew(osThreadFunc_t func, void *argument,
                         const osThreadAttr_t *attr) {
    TSK_INIT_PARAM_S param = {0};
    param.pfnTaskEntry = (TSK_ENTRY_FUNC)func;                          // CMSIS 参数
    param.usTaskPrio   = OS_TASK_PRIORITY_LOWEST - attr->priority;      // 翻译成 LiteOS 参数
    UINT32 ret = LOS_TaskCreate(&tid, &param);                          // 调 LiteOS 原生 API
    ...
}
```
调用链：
```
应用: osThreadNew(...)        ← 只会标准语
      ↓
翻译层: osThreadNew(){ ... LOS_TaskCreate(...) }   ← 翻译官（参数转换+转发）
      ↓
内核: LOS_TaskCreate()  →  真正调度任务            ← 干活的
```
比喻：CMSIS-RTOS2 = 普通话；各 RTOS 原生 API = 方言；翻译层 = 把普通话翻成某方言的翻译官。应用只会普通话，到了 LiteOS 地盘翻译官翻成 `LOS_*`，到了 FreeRTOS 地盘就换一个翻成 `xTask*` 的翻译官——应用不用改。

### 6. "翻译层一字不差，差别在链接到谁"——链接器视角

这句话是说：翻译层这段代码两边源码一样、编出的 `.o` 一样，**差别全在链接器把 `LOS_TaskCreate` 这个符号解析到谁**。

| | 翻译层(cmsis_liteos2.o) | 谁提供了 LOS_TaskCreate 的定义 |
|---|---|---|
| 开源版 | 一模一样 | `liteos_kernel.o`（开源内核源码编出）|
| hi3861 | 一模一样 | `libbase.a`（海思预编译内核）|

翻译层只"喊"了 `LOS_TaskCreate` 这个名字（一个未解析的符号引用），不关心是谁实现的。链接器去各 `.o`/`.a` 里找这个符号的定义：开源版找到 `liteos_kernel.o`，hi3861 找到 `libbase.a`。

比喻：同一个传话筒都喊"找老王"，但"老王"是两个不同的人——开源版的老王是开源内核源码编出的那个人，hi3861 的老王是海思预编译 `.a` 里那个人。两个老王都叫 `LOS_TaskCreate`、都会干活，但内部实现不同。传话筒（翻译层）不关心是哪个老王。

### 7. 换内核时 .a 会换、adapter 恒定吗

- **`.a` 会随内核换**：`.a` 就是内核编译产物，换内核必换 `.a`。✅
- **`cmsis_liteos2.c` 不普遍恒定**：它只在 **LiteOS 家族内**恒定（因为都讲 `LOS_*`）。换非 LiteOS 内核要换 adapter 文件：
  - 换 FreeRTOS → `cmsis_freertos.c`（调 `xTaskCreate`）
  - 换 RT-Thread → `cmsis_rtthread.c`（调 `rt_thread_create`）
  - 换 Linux / LiteOS-A → CMSIS 这层根本不存在（见第 8 节）
- **真正恒定的是两样**：①CMSIS-RTOS2 标准 API（`os*` 签名，是规范，跟内核无关）；②"中间需要一个翻译层"这个机制。**不恒定的是翻译层的具体代码**（调什么原生 API 由底层内核决定）。前文"开源和 hi3861 翻译层一字不差"是两边同属 LiteOS 家族的特例，不是普遍规律。

### 8. 换内核的可换性边界 / CMSIS 适用边界

**不是所有内核都是 RTOS**——Linux 不是 RTOS（是通用操作系统），LiteOS 家族才是 RTOS。CMSIS 只在 **Mini / MCU 层级**作为 KAL 使用。

**能直接换内核**：同系统层级 + 同 API 族 + 同硬件类
- `liteos_m ↔ Huawei_LiteOS`：都 Mini + 都 LiteOS 家族(`LOS_*`) + 都 MCU → ✅ 可换（这就是 OH"内核可替换"承诺的范围）

**不能直接换**：跨其中任一维度
- `liteos_m ↔ Linux`：跨层级(Mini/Standard) + 跨 API 族(CMSIS/POSIX) + 跨硬件类(MCU 无 MMU / 应用处理器有 MMU) → ❌ 本质是换系统层级，hi3861 物理上跑不了 Linux
- `liteos_m ↔ FreeRTOS`：同 Mini + 同 MCU，但跨 API 族 → ⚠️ 需重写 adapter

**CMSIS 何时用不上**：
- 换 Linux（Standard）：KAL 是 POSIX + bionic，**无 CMSIS adapter**
- 换 LiteOS-A（Small）：KAL 是 POSIX-lite + 原生 API，**不用 CMSIS**
- Mini 内换非 LiteOS RTOS：CMSIS 还能用，但 adapter 文件要换

> **OH"内核可替换"是有限度的**：在同一个系统层级内、且满足同一套 KAL 契约的前提下可换。不是任意内核能换任意内核。`liteos_m ↔ Huawei_LiteOS` 之所以能无痛换，是因为层级、API 族、硬件类三者全对齐；`liteos_m ↔ Linux` 三者全错位，所以不能换。

---

## 附：两种方式的代码定位速查

### 方式 A（厂商适配）
- 适配层源码：`device/soc/hisilicon/hi3861v100/hi3861_adapter/kal/cmsis/cmsis_liteos2.c`
- 厂商内核：`device/soc/hisilicon/hi3861v100/sdk_liteos/platform/os/Huawei_LiteOS/`
- 预编译制品：`device/soc/hisilicon/hi3861v100/sdk_liteos/ohos/libs/*.a`
- 内核声明：`vendor/hisilicon/hispark_pegasus/config.json` → `kernel_is_prebuilt: true`
- ws63 同构：`device/soc/hisilicon/ws63v100/sdk/kernel/liteos/{liteos_v208.5.0, ohos_adapt}` + `adapter/kal/`

### 方式 B（直接编译）
- 板级构建：`device/qemu/esp32/liteos_m/board/BUILD.gn` → `import("//kernel/liteos_m/liteos.gni")`
- 开源内核本体：`kernel/liteos_m/`（含 `kal/`、`components/`、`arch/`、`kernel/`）
- QEMU 产品配置：`vendor/ohemu/qemu_*_mini_system_demo/`
