---
name: driver-device
description: 工作流 Phase 3——开发嵌入式外设驱动：生成 HAL/IoT HAL/HDF 驱动代码、编写设备树配置（HCS/devicetree）、执行 RTOS→目标 OS 驱动迁移。触发症状：用户说"写驱动"、"GPIO/UART/I2C/SPI/PWM 驱动"、"HDF 驱动"、"HCS 配置"、"WiFi 驱动"、"从 FreeRTOS 迁移驱动"。
license: MIT
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: lite
  capability: driver-device
  version: 0.1.0
  status: trial
  category: workflow-step-driver-device
  references:
    wifi_arch: skills/ohos-dev-board-config-gen/references/wifi_hal_architecture.md (~10KB)
    sdk_api_mapping: skills/ohos-dev-board-config-gen/references/hi3861_sdk_api_crossref.md (~12KB)
    iot_hal_model: skills/ohos-dev-board-config-gen/references/l0-iot-hal-driver-model.md
    compiler_playbook: skills/ohos-dev-build-config/references/compiler_fix_playbook.md
---

## Target profile 路由（强制）

读取 `workflow_config.yaml` 的 `target.profile` 字段指定的同一份 target profile（P1 选定、P2/P3/P4 共用；与 session manifest 记录不一致时停下问）。驱动框架、注册方式和设备描述格式都是 profile 值；`L0`/`L1` 标签**本身不决定** HDF、HCS、IoT HAL、DTS 或 Linux userspace 集成的取舍。只跑 profile 适用的子步骤，其余机制在 manifest 里标 `NOT_APPLICABLE`。

Profile 优先级：下方示例和框架专属章节只是模板。选定 profile 决定实现用 Linux 内核驱动、HDF/HCS、IoT HAL、DTS 还是其他机制。`source_strategy: greenfield` 时，只生成已记录公开规格支持的能力，不支持的能力标 `UNVERIFIED`。

# Phase 3: 驱动开发与设备配置

> **本文件已通过实测验证**。L3 整体覆盖率 25%，但呈现明显的**两极分化**：
> **简单驱动 (GPIO/I2C/PWM/UART) → PASS/PARTIAL** | **复杂驱动 (WiFi) + 系统驱动 (watchdog/reset/lowpower) → FAIL**。
> 已产出两份参考文档专门修复复杂驱动 gap。本 SKILL 已接入。

## 契约（来自编排器 `skills/ohos-dev-workflow-router/SKILL.md` v0.1.0）

| 属性 | 值 |
|------|-----|
| **输入** | P2 产出的内核基线 + P1 的 chip-spec + 外设需求列表 |
| **产出** | ① 外设驱动源码 ② 设备配置 (L0: config structs / L1: HCS device tree) ③ BUILD.gn 集成 (sources 更新) ④ (可选) RTOS→OS 映射表 |
| **门控** | GATE-D: 驱动适配确认——① 驱动范围（所有需求外设都有对应驱动?）② 驱动框架与 target profile 的 `driver_model` 一致（不从 L0/L1 标签推断）③ 设备配置（HCS/DTS/config 结构体，按 profile 的 `device_description`）与驱动匹配 ④ 来源完整性 ⑤ 工具链就绪 |
| **后续** | → P4 构建验证 (全量编译含驱动) |

## 知识检索（可用时优先知识检索服务如 project-brain MCP；不可用按 skill 知识检索降级链：本地 references → 联网搜索 → 询问用户）

本步骤的本地代码分析，可用时优先使用（可选）project-brain 等知识检索服务 MCP：
- `get_call_graph` — 追 HAL→KAL→内核 调用链（驱动调 hi_*→LOS_*）
- `get_module_contents` — 看 adapter 模块含哪些函数
- `locate_symbol` — 定位 HAL API / SDK 驱动函数定义
- `get_dependencies` — 看 SDK 驱动依赖结构

> MCP 调失败或未装 → 按 skill 知识检索降级链回退。

## 子步骤总览

```
P3: 驱动开发与设备配置
│
├─ 3a: 芯片规格提取 (使能活动, 按需触发)
│       └─ 走 ohos-dev-soc-spec-parse skill → DTS / SDK header / datasheet → 寄存器/中断/时钟/引脚（datasheet 仅作回退）
│
├─ 3b: ★ 外设驱动代码生成 (核心)
│       ├─ 简单驱动: GPIO / I2C / SPI / PWM / UART (模板化)
│       └─ 复杂驱动: WiFi / Ethernet / Display (架构优先, MVP 策略)
│
├─ 3c: 设备配置 (L0 vs L1 分支)
│       ├─ L0: 配置结构体 / 直接注册 (无 HCS)
│       └─ L1: HCS 设备树 (.hcs 文件 + device_info.hcs)
│
└─ 3d: RTOS 驱动迁移 (可选, 有现有 RTOS 代码时触发)
```

---

## Step 3a: 芯片规格提取（使能活动）

> **注意**: 3a 已从独立阶段降格为使能活动——不再按固定顺序执行，而是在 3b 需要时按需触发。

### 输入来源 (按优先级)

> **芯片信息提取统一走 `ohos-dev-soc-spec-parse` skill**（单点查询/完整提取）——命中 `chip-specs-quick-ref.md` / `ddr-variant-guide.md` 直接用，未命中调 ohos-dev-kernel-source-query 联网查；下列原始来源是 ohos-dev-soc-spec-parse 的数据源，手工翻 datasheet 仅作回退。

| 来源 | 可靠性 | 典型内容 |
|------|:------:|---------|
| **ohos-dev-soc-spec-parse skill**（首选路由） | ✅ 高 | 预提取芯片规格 + DDR 变体/xlsm + 单点查询 |
| **SDK header files** | ✅ 高 | 寄存器地址宏定义、结构体声明 |
| **Datasheet PDF**（回退） | ✅ 高 | 内存映射表、外设基地址、时序参数 |
| **DTS (Device Tree Source)** | 🟡 中 | 节点拓扑、中断号、引脚复用 |
| **现有参考板代码** | ✅ 高 | 完整的寄存器操作序列 |

### 提取输出格式

```yaml
# peripheral_list.yaml (或 chip-spec 扩展)
peripherals:
  - name: gpio
    base_addr: "0x11000000"
    interrupt: 44
    clock_gate: "CG_PERI_GPIO"
    pins: [12]           # GPIO 组数
    registers:
      - { name: "DATA_OFFSET", offset: "0x000", width: 32 }
      - { name: "DIR_OFFSET",  offset: "0x004", width: 32 }
      # ...

  - name: uart0
    base_addr:0x40000000"
    interrupt: 19
    baud_base: 40MHz
    fifo_depth: 32
    # ...
```

### 工具

- `skills/ohos-dev-soc-spec-parse/` — 自动解析 SDK headers / DTS
- `skills/ohos-dev-soc-spec-parse/references/hi3861v100-adapter-structure.md` — Hi3861V100 实际文件位置参考

---

## Step 3b: 外设驱动代码生成 ★ 核心

### ⚠️ 驱动适配集成边界（驱动适配 = integration，不重写驱动）

> **核心原则**：P3 驱动适配是 **integration（集成）**，不是从零写芯片驱动。适配者把 vendor 提供的 HAL/OSAL 集成进 OH userspace，并生成 OH 框架胶水（HDF driver wrapper）调 vendor HAL 接口——**不重写 vendor HAL/OSAL 驱动代码**。本节是 P3 所有驱动适配活动的前置边界声明，与 02-kernel-port 的集成边界小节（内核侧：不重写内核驱动，只 defconfig+DTS port）呼应——P3 是 HAL/userspace 侧的集成边界。

**职责划分**：

| 层 | 谁写 | 内容 | 缺失怎么办 |
|---|---|---|---|
| **vendor HAL/OSAL**（soc/drivers + soc/OSAL + soc/libs） | **厂家**（只有厂家能写） | 厂家原生 userspace 芯片 API（寄存器操作/中断/时钟/DMA 等底层驱动） | vendor SDK 缺该 HAL 驱动 → 适配者**写不了**（没芯片文档/寄存器规格）→ **硬阻塞问用户**，不瞎编 |
| **OH-HDF driver wrapper**（vendor/ + hals/ 下的 HdfDriverEntry 实现） | **适配者** | OH 框架胶水：HdfDriverEntry(Bind/Init/Release/Dispatch) → 调 vendor HAL 接口 + HCS 设备树配置（device_info.hcs + {peripheral}_config.hcs） | 这是 integration 层，不是芯片驱动——适配者按 OH HDF 框架规范写 |
| **HCS 设备树配置** | **适配者** | device_info.hcs（host→device→deviceNode 拓扑）+ {peripheral}_config.hcs（外设属性：base_addr/irq/clock/pins） | 从 3a 规格提取填 HCS，不凭空编 |

**适配者做 integration 的具体动作**：
1. 把 vendor HAL/OSAL（soc/drivers + soc/OSAL + soc/libs）集成进 OH userspace 目录结构（vendor/{chip}/ + hals/）——port 不改内容（B 类来源，见 P2 §来源声明）。
2. 生成 OH-HDF driver wrapper（OH 框架胶水，调 vendor HAL 接口）——这是 integration 层代码，不是芯片驱动重写。
3. 生成 HCS 设备树配置（device_info.hcs + {peripheral}_config.hcs），属性从 3a 规格提取。
4. 更新 BUILD.gn sources（把 wrapper .c + vendor HAL .so/.a 接入构建图）。

**适配者不做的事**（硬边界）：
- ❌ **不重写 vendor HAL/OSAL 驱动代码**——那是厂家原生芯片 API，只有厂家有寄存器规格/上电序列/复位拓扑能写。适配者只 port + 调用。
- ❌ **不瞎编 vendor SDK 缺的 HAL 驱动**——缺某 HAL 驱动 → 没芯片文档写不了 → 报硬阻塞问用户（P-硬阻塞转发），不准凭空生成占位驱动冒充已适配。
- ❌ **不混淆 wrapper 与芯片驱动**——OH-HDF wrapper 是 OH 框架胶水（HdfDriverEntry 调 vendor HAL），不是芯片驱动本身。芯片驱动在 vendor HAL/OSAL 里。

**外设范围按用户定的 scope**（关联）：
外设集成范围按用户在 P1 前置决策定的 scope（标准集 / 全量等）执行。**不在 scope 的组件不集成**——如 graphic 不在标准集 → 从 BUILD.gn/subsystem_config.json 移除依赖（候选：OH 上游代码 bug 遇到不在 scope 的组件，走 B 移除依赖绕过，不修 OH 共享代码）。scope 内的组件按本节 integration 边界执行。

> **GATE-D 检查**：驱动适配集成边界声明——若某外设用了"预编译库占位"（vendor .so 直接放 rootfs + copy 规则，无 HDF wrapper），必须**显式声明**"驱动未真实适配，用预编译库占位 + 占位理由（缺厂商 build scripts / 快速产可烧录镜像）"，不准默写"驱动已适配"。完整 L1 适配应逐步把占位换成真实 HDF wrapper（调 vendor HAL）。实测 hi3516cv610 因 SDK 驱动编译依赖厂商 build scripts 采用了预编译库占位模式（见下方 §L1 真实 HDF 驱动适配 vs 预编译库占位），是权宜不是完整适配。

**GATE-D 来源完整性检查（驱动源码三分类）**：本阶段每个驱动源文件的产生方式三选一记录——
- `generated`（由 ohos-dev-soc-spec-parse + ohos-dev-board-config-gen 从规格生成）→ 记录输入 datasheet + 使用的工具
- `adapted_from_existing`（基于现有驱动修改）→ 记录原始来源 + 改动范围
- `manual`（手工编写）→ 记录依据
- ⚠️ 驱动代码 SHA 与任何现有适配一致 → **触发目标漂移警报**（抄现有适配而非按规格生成，验证前提不成立），停下核查；来源记录写入 PROVENANCE

> 与编排器 `skills/ohos-dev-workflow-router/SKILL.md` GATE-D「[来源完整性]」确认项对应——执行者跑 P3 主要读本文件，子项在这里可执行。

### ⚠️ 关键分类：简单 vs 复杂驱动

实测证明：**不是所有驱动都能用同一种方式生成**。

```
驱动复杂度判断:
│
├─ 【简单驱动】— 寄存器直接读写模式
│   │   特征: 单个基地址 + 少量寄存器 + 无内部状态机
│   │   代表: GPIO, I2C Master, PWM, 基础 UART (仅收发)
│   │   方法: 模板填充 (见下方模板)
│   │   实测结果: ✅ PASS (GPIO/I2C/PWM/UART)
│   │
└─ 【复杂驱动】— 多层架构 / 状态机 / 异步事件
    │   特征: 多模块协作 / 内部状态机 / 中断+轮询混合 / 协议栈
    │   代表: WiFi, Ethernet, USB, Filesystem, Display
    │   方法: 架构设计先行 → MVP 实现 → 迭代扩展
    │   实测结果: ❌ FAIL (WiFi 0%, watchdog/reset/lowpower 0%)
    │
        └─ 【系统驱动】— 芯片级子系统 (介于简单和复杂之间)
            特征: 影响全局状态 (电源域/复位/看门狗)
            方法: 需要芯片级系统知识 (上电序列/复位拓扑)
            实测结果: ❌ FAIL (需要芯片系统手册)
```

### ⚠️⚠️⚠️ 关键前置决策：target profile 的 driver_model → 驱动框架映射

> **纠正**: 早期验证轮全程只验证了 **L0 (wifiiot/LiteOS-M)**。不同 driver_model 的
> 驱动框架、注册方式、配置文件格式**完全不同**，必须在 3b 之前确认。
> **数据源是 target profile（见顶部 Target profile routing）**：驱动框架读 profile 的
> `driver_model` 字段，**不从 L0/L1 标签或 mini/small 值域推断**——L0/L1 标签是推导结论
> 不是判定依据（config 值域映射：mini=L0 轻量 / small=L1 小型）。

```
驱动框架判断流程:
│
├─ Step A: 读 target profile 的 driver_model 字段 ({{ASSET_ROOT}}/workflow/target-profiles/,
│          P2 已选定并记录到 session manifest)
│   │
│   ├─ driver_model: iot_hal (典型 L0 轻量: system_type=mini / kernel_type=liteos_m)
│   │   └─ → IoT 外设驱动子系统 (⚠️ 不是 HDF!)
│   │       注册方式: 组件化直接注册 (无 HdfDriverEntry)
│   │       配置文件: C 结构体 / 宏定义 (无 .hcs)
│   │       HAL 接口: LiteOS-M HAL (hals/iot_hardware/)
│   │       典型芯片: Hi3861V100, STM32F407, ESP32, GR551x,
│   │                CST85, W800, TLSR9/B91, GD32F4xx
│   │
│   ├─ driver_model: hdf (典型 L1 小型: system_type=small / kernel_type=liteos_a)
│   │   └─ → 精简版 HDF + HCS 配置
│   │       注册方式: HdfDriverEntry (Bind/Init/Release)
│   │       配置文件: .hcs 设备树 + device_info.hcs
│   │       HAL 接口: HDF OSAL (os_adapter/)
│   │       内核: LiteOS-A (非 LiteOS-M!)
│   │       典型芯片: RK2206, BK7235, ASR582x, BES2600,
│   │                HPM6750, Hi3518EV300, STM32MP1xx
│   │
│   ├─ driver_model: linux_kernel / linux_kernel_plus_oh_integration
│   │   └─ → Linux 内核驱动 + vendor HAL/OSAL 集成进 OH userspace
│   │       注册方式: 内核 platform driver probe + userspace 集成 (无 HdfDriverEntry)
│   │       配置文件: DTS 设备树 (非 .hcs——设备描述按 profile 的 device_description)
│   │       内核: Linux (典型 L1 小型 system_type=small, 如 hi3516cv610)
│   │
│   └─ driver_model: 完整 HDF (L2 标准系统, 高性能 SoC, >16MB RAM)
│       └─ → 完整 HDF + 完整 HCS
│           注册方式: HdfDriverEntry + IDeviceIoService
│           配置文件: 完整 .hcs 设备树体系
│           HAL 接口: HDF OSAL (Linux 用户态)
│           内核: Linux
│           典型芯片: RK3568/RK3588, Hi3516DV300, Hi3751V350
│
├─ Step B: driver_model=iot_hal → 继续使用本 SKILL 的现有流程 (IoT HAL 模板)
│
├─ Step C: driver_model=hdf → 切换到 HDF 驱动模式:
│   ├── 驱动代码结构变为:
│   │   {chip}_adapter/
│   │   ├── driver/           # HdfDriverEntry 实现
│   │   ├── hal/              # HDF OSAL 映射层
│   │   └── hcs/              # .hcs 配置文件
│   ├── BUILD.gn 使用 hdf 模块声明
│   └── 参考: device_soc_st/ (STM32MP1) 或 device_soc_beken/ (BK7235)
│
├─ Step C': driver_model=linux_kernel / linux_kernel_plus_oh_integration
│   └─ → 内核侧驱动适配 (defconfig + DTS, 见下方 watchdog/SPI Nand 节)
│      + vendor HAL/OSAL 集成 (见 §驱动适配集成边界), 不生成 HCS
│
└─ Step D: driver_model=完整 HDF (L2) → 本 SKILL 不适用 → 转向标准系统 HDF 文档
```

> **⚠️ 常见错误**: 对 driver_model=iot_hal 的目标使用 `HdfDriverEntry` / `IDeviceIoService` / `.hcs`。
> 这些是 HDF 模型专属 API。IoT HAL 模型（如 wifiiot 产品类型）**不加载 HDF 子系统**。

---

### 3b-1: 简单驱动模板 (实测验证有效, 仅适用于 L0 IoT HAL)

以下模板在实测中对 GPIO/I2C/PWM/UART 全部通过或接近通过：

```c
// hal_{peripheral}.c — 通用简单驱动模板
#include "{peripheral}_if.h"          // OH HAL 接口头文件
#include "hdf_log.h"                  // 日志 (可选, L0 可能没有)

/* ====== 芯片特定: 从 3a 规格提取 ====== */
#define {PERIPH_UPPER}_BASE_ADDR    0x{base_addr}    // 寄存器基址
#define {PERIPH_UPPER}_DATA_OFFSET  0x{data_off}     // 数据寄存器偏移
#define {PERIPH_UPPER}_DIR_OFFSET   0x{dir_off}      // 方向寄存器偏移
#define BIT_SET(n)                 (1UL << (n))

/* ====== 私有资源结构体 ====== */
struct {PeriphName}Resource {
    uint16_t pin;         // 通道号 / 实例 ID
    void *priv;           // 私有数据 (扩展用)
};

/* ====== Init: 时钟使能 + GPIO 引脚复用 + 默认配置 ====== */
static int32_t {PeriphName}Init(struct {PeriphName}Resource *resource)
{
    // 1. 时钟使能 (芯片特定!)
    // CLOCK gating: {clock_gate_name}
    // {ClockEnableFunction}({PERIPH_UPPER}_CLOCK_GATE);

    // 2. GPIO 引脚复用 (如果需要)
    // {GpioSetFunc}(resource->pin, {FUNC_{PERIPH}});

    // 3. 寄存器默认值
    // HWREG({PERIPH_UPPER}_BASE_ADDR + {PERIPH_UPPER}_DIR_OFFSET) = 0;

    HDF_LOGI("{PeriphName}: init pin=%u", resource->pin);
    return HDF_SUCCESS;
}

/* ====== Read: 读寄存器 + 位掩码 ====== */
static int32_t {PeriphName}Read(struct {PeriphName}Resource *resource, uint16_t *val)
{
    uint32_t raw = HWREG({PERIPH_UPPER}_BASE_ADDR + {PERIPH_UPPER}_DATA_OFFSET);
    *val = (raw >> resource->pin) & 0x1;  // 或多 bit 掩码
    return HDF_SUCCESS;
}

/* ====== Write: 写寄存器 + 位掩码 ====== */
static int32_t {PeriphName}Write(struct {PeriphName}Resource *resource, uint16_t val)
{
    uint32_t reg = HWREG({PERIPH_UPPER}_BASE_ADDR + {PERIPH_UPPER}_DATA_OFFSET);
    if (val != 0)
        reg |= BIT_SET(resource->pin);
    else
        reg &= ~BIT_SET(resource->pin);
    HWREG({PERIPH_UPPER}_BASE_ADDR + {PERIPH_UPPER}_DATA_OFFSET) = reg;
    return HDF_SUCCESS;
}

/* ====== Release: 时钟禁用 + GPIO 恢复 ====== */
static int32_t {PeriphName}Release(struct {PeriphName}Resource *resource)
{
    // {ClockDisableFunction}({PERIPH_UPPER}_CLOCK_GATE);
    // {GpioRestoreFunc}(resource->pin);
    HDF_LOGI("{PeriphName}: release");
    return HDF_SUCCESS;
}

/* ====== OH HAL 接口绑定 ====== */
struct {IHalInterfaceName} g_{periphName}Methods = {
    .Init = {PeriphName}Init,
    .Read = {PeriphName}Read,
    .Write = {PeriphName}Write,
    .Release = {PeriphName}Release,
};
```

**模板变量替换规则**:

| 变量 | 替换为 | 来源 |
|------|--------|------|
| `{PeriphName}` | 驼峰命名 (GpioWrite, I2cTransfer) | HAL 接口头文件 |
| `{peripheral}` | 小写 (gpio, i2c, pwm) | 目录名/文件名 |
| `{PERIPH_UPPER}` | 大写下划线 (GPIO, I2C, PWM) | 宏定义前缀 |
| `0x{base_addr}` | 实际寄存器基址 | 3a 规格提取 |
| `{IHalInterfaceName}` | OH 定义的接口 struct 名 | HAL 接口头文件 |

### 3b-2: 复杂驱动策略 — WiFi 为例

**实测最大 L3 Gap**: WiFi HAL (`wifi_device.c`) 在 GT 中有 **993 行**，7 层架构，30+ API。工作流生成了空壳 → Gate Report 0%。

**参考文档**: `wifi_hal_architecture.md` (~10KB) 包含完整分析。

#### WiFi 驱动的 7 层架构

```
┌─────────────────────────────────────────────┐
│ Layer 1: OH WiFi HAL API (wifi_if.h)        │ ← 公开接口, 30+ 函数
├─────────────────────────────────────────────┤
│ Layer 2: Event Dispatch (同步+异步双通道)    │ ← 事件分发器
├─────────────────────────────────────────────┤
│ Layer 3: State Machine (7 个全局状态变量)    │ ← 连接/扫描/断开/DHCP...
├─────────────────────────────────────────────┤
│ Layer 4: Protocol Parser (帧解析/组装)       │ ← 802.11 帧处理
├─────────────────────────────────────────────┤
│ Layer 5: NetIF Adapter (LwIP 集成)          │ ← 网络协议栈对接
├─────────────────────────────────────────────┤
│ Layer 6: Low-level TX/RW (DMA/中断)         │ ← 硬件操作
├─────────────────────────────────────────────┤
│ Layer 7: Chip IOCTL (厂商私有命令)           │ ← SDK 封装
└─────────────────────────────────────────────┘
```

#### 复杂驱动生成策略: MVP First

```
不要试图一次生成全部 7 层!

MVP (Minimum Viable Product, ~400 行):
  ├─ Layer 1: Init/DeInit/GetMacAddr/SetMode (5 个核心 API)
  ├─ Layer 2: 简单同步 dispatch (无异步)
  ├─ Layer 3: 最小状态 (Idle ↔ Init ↔ Scan)
  ├─ Layer 6: 基础 TX/RX (调用 SDK 函数)
  └─ Layer 7: SDK 初始化 + 基础 ioctl

Full (~700 行):
  └─ 在 MVP 基础上逐层添加 Layer 4/5 和完整异步支持
```

**关键参考**: `wifi_hal_architecture.md` §7 Generation Strategy 有完整的 MVP→Full 路线图。

### 3b-3: SDK API 命名约定

**实测发现**: 每个 IoT HAL 驱动底层都调用 SDK 函数，而 SDK 函数命名遵循特定约定。

`hi3861_sdk_api_crossref.md` 记录了 **9 个 IoT HAL 驱动**的完整映射:

| HAL Driver | 底层 SDK 函数命名模式 | 示例 |
|-----------|-------------------|------|
| GPIO | `HalGpio{Op}` | HalGpioSetDir, HalGpioWrite |
| I2C | `HalI2c{Op}` | HalI2cInit, HalI2cReadWrite |
| UART | `Uart{Dev}_{Op}` | Uart0_Init, Uart0_Send |
| SPI | `Spi{Op}` | SpiInit, SpiTransfer |
| PWM | `Pwm{Ch}_{Op}` | Pwm0_Init, Pwm0_Start |
| WiFi | `wifi_{subsys}_{op}` | wifi_init, wifi_connect |
| Watchdog | `{Chip}Wdg{Op}` | Hi3861WdgFeed |
| ... | ... | ... |

**生成驱动时必须先查此映射表**，确保底层 SDK 函数名正确。

---

## Step 3c: 设备配置

### 驱动模型决策树（按 target profile 的 driver_model 分支，不从 L0/L1 标签分支）

```
target.profile.driver_model?
├── iot_hal (典型 L0 轻量, system_type=mini / liteos_m):
│   ├── 驱动模型: IoT HAL (直接函数指针, 无 HDF)
│   ├── 设备配置: C 结构体数组 / 简单 config.h
│   ├── 注册方式: 直接函数调用 / module init list
│   └── HCS 文件: ❌ 不使用 (跳过 3c 的 HCS 部分)
│
├── hdf (典型 L1 小型, system_type=small / liteos_a):
│   ├── 驱动模型: HDF (Bind/Init/Release/Dispatch)
│   ├── 设备配置: HCS 设备树 (.hcs 文件)
│   ├── 注册方式: HDF DriverEntry + HdfDriverBind/Init/Release
│   └── HCS 文件: ✅ 必须生成
│       ├── device_info.hcs (host → device → deviceNode)
│       └── {peripheral}_config.hcs (每个外设一个)
│
└── linux_kernel / linux_kernel_plus_oh_integration (L1-Linux, 如 hi3516cv610):
    ├── 驱动模型: Linux 内核驱动 (platform driver, defconfig + DTS)
    ├── 设备配置: DTS 设备树 (board.dts——设备描述按 profile 的 device_description)
    ├── 注册方式: 内核驱动 probe (非 HdfDriverEntry)
    └── HCS 文件: ❌ 不适用 (设备描述是 DTS 不是 HCS)
```

> **⚠️ 实测经验**: Hi3861V100 (wifiiot/L0) 的 `hdf_config/` 目录虽然存在于代码仓中，但 **不被纳入构建图**。L0 不走 HDF。对 L0 目标，3c 只需生成简单的配置头文件即可。

### L1 HDF 驱动注册模式 (L1 专用)

> **当 target profile 的 driver_model = hdf（典型 L1 小型系统；config 值域 `target.system_type = "small"`，映射：mini=L0 轻量 / small=L1 小型）时，以下内容替代 3b-1 的简单模板**

```c
// {chip}_adapter/driver/{peripheral}/{peripheral}.c — L1 HDF 驱动模板
#include "hdf_log.h"
#include "device/device_service_manager.h"
#include "hdf_device_object.h"
#include "osal/hdf_osal_{peripheral}.h"    // ← HDF OSAL 接口, 非 IoT HAL!

// 1. Bind: 框架创建驱动服务时调用
static int32_t {PeriphName}Bind(struct HdfDeviceObject *deviceObject)
{
    // 从 deviceObject->property 获取 HCS 配置属性
    // 初始化硬件资源 (时钟/引脚复用/中断)
    return HDF_SUCCESS;
}

// 2. Init: 驱动初始化
static int32_t {PeriphName}Init(struct HdfDeviceObject *deviceObject)
{
    // 外设初始化序列 (与 L0 简单驱动的 Init 类似)
    // 但通过 HDF DeviceObject 获取配置, 而非硬编码
    return HDF_SUCCESS;
}

// 3. Release: 资源释放
static int32_t {PeriphName}Release(struct HdfDeviceObject *deviceObject)
{
    // 反初始化、释放资源
    return HDF_SUCCESS;
}

// 4. Dispatch: 服务分发 (可选, 有 IO 服务时需要)
static int32_t {PeriphNameDispatch(struct HdfDeviceObject *object,
    int cmdId, struct HdfSBuf *data, struct HdfSBuf *reply)
{
    // 处理自定义 IOCTL 命令
    return HDF_SUCCESS;
}
```

**L1 HDF 驱动的关键差异 vs L0 IoT HAL**:

| 维度 | L0 IoT HAL | L1 HDF |
|------|-----------|---------|
| 头文件 | `hal_{periph}.h` | `hdf_{periph}_driver.h` |
| 入口宏 | 无 | `HDF_DRIVER_ENTRY({PeriphName})` |
| 初始化参数 | 自定义 Resource 结构体 | `HdfDeviceObject*` (框架传入) |
| 配置来源 | C 结构体 / 宏定义 | `.hcs` 文件 → `property` 字段 |
| 日志接口 | 可选 `hdf_log.h` | 必须 `HDF_LOG{}/HDF_LOGE{}` |
| 服务发布 | 无 | `IoServiceAdd()` + `IDeviceIoService` |

### L1 真实 HDF 驱动适配 vs 预编译库占位（实测教训）

Hi3516CV610因 SDK 驱动编译依赖厂商 build scripts（不在 SDK 中），采用了**预编译 .so + BUILD.gn copy 规则占位**模式。这是**权宜**，不是完整的 L1 适配：

| 模式 | 做法 | 何时可接受 | 局限 |
|---|---|---|---|
| **预编译库占位** | SDK .so 直接放 rootfs/lib + copy 规则 | SDK 驱动源码不可编译（缺厂商 build scripts）/ 快速产可烧录镜像 | 驱动黑盒、不可裁剪、不可移植、HDF 绑定缺失 |
| **真实 HDF 适配** | 写 HdfDriverEntry 驱动 + HCS 绑定 + 调 SDK/寄存器 | 完整 L1 适配 / 需 HDF 设备节点 / 需可维护 | 需驱动源码或寄存器规格 |

> **GATE-D 检查**：若用预编译库占位，必须**显式声明**"驱动未真实适配，用预编译库占位 + 占位理由（缺厂商 build scripts）"，不准默写"驱动已适配"。这是 P-显式未验证在驱动层的落地。完整 L1 适配应逐步把占位换成真实 HDF 驱动。

### SPI Nand 驱动适配：板载颗粒 ID 表补条目两侧（uboot + 内核，实测教训）

板载 SPI Nand 颗粒若不在 SoC 厂商的 SPI Nand ID 表（如 hi3516cv610 的 `fmc_spi_nand_flash_table[]`），uboot 侧报 `pagesize 8192` BUG、内核侧 `bsp_spi_nand_probe error -19`(-ENODEV)，UBI/rootfs 起不来。**这是驱动适配层的活**——补 ID 表条目：

- ⚠️ **uboot 与内核是两份独立的 ID 表源文件**：uboot `drivers/mtd/nand/raw/fmc100/fmc_ids_hi3516cv610.c` + 内核 `drivers/mtd/nand/fmc100/fmc_ids_hi3516cv610.c`（路径差一层 `raw/` vs 无，但独立）。补颗粒**两侧都要补**，否则一侧识别另一侧 probe 失败（uboot 报 `pagesize 8192` BUG / 内核 `bsp_spi_nand_probe error -19`）。**DS35Q1GB-IB 类颗粒即此情况**——两侧都补才能两侧通。
- **补法**：抓颗粒 ID（JEDEC ID，如 `0xe5,0xf1`）→ grep 确认不在表 → 照抄同表同厂商前缀（`0xe5`）、同规格（pagesize/OOB）的现有条目（如 HY035），只改 id + name，参数按颗粒规格书核对。别从零写条目。
- 补完重编 uboot + 内核，重烧。完整诊断见 `skills/ohos-issue-lite-diagnose/references/diagnostic-cases.md` BG003；烧录症状处置见 `skills/ohos-ci-lite-deploy-burn/SKILL.md`「板载 SPI Nand 颗粒不在 ID 表」。

> **内核侧驱动适配的完整 playbook 见 `skills/ohos-dev-kernel-node-adapt/` skill**（SPI Nand ID 表两侧补见该 skill `skills/ohos-dev-kernel-node-adapt/references/spi-nand-id-table-playbook.md`；watchdog/hilog/binder 适配 + CONFIG→/dev 节点映射同在此 skill）。本节是方法论引路，落地操作回该 skill。

### watchdog 驱动适配标准操作 + 驱动适配审计清单（实测教训）

板子 bring-up 缺 `/dev/watchdog`（OH `watchdog_service` open 失败退出 → init `ReapService` 见 IMPORTANT 进程退出 → `reboot(RB_AUTOBOOT)` 软重启 loop）时，**优先做内核侧 watchdog 驱动适配**，不要只靠 rootfs 侧绕过（删 watchdog_service）。

**标准操作（按序）**：
1. **查 defconfig**：`CONFIG_WATCHDOG=y` + `CONFIG_DW_WATCHDOG=y`（Synopsys DesignWare WDT，hi3516cv610 用的是 dw wdt）。没开就开。
2. **查 DTS**：watchdog 节点（hi3516cv610 实例 `wdg@0x11030000`）要含 `compatible = "snps,dw-wdt"` + `clocks` + `status = "okay"`。缺节点或 `status="disabled"` → 加/改。
3. **重编 zImage + dtbs**（DTS 改了必走 `make dtbs`），uImage 按上方 §02-kernel-port「内核重编后 uImage 必走 FIT」重做 FIT。
4. 烧后 `ls /dev/watchdog` 确认节点出现。

**驱动适配审计清单（不只查当前报错那个）**：缺 `/dev` 节点导致 OH init/service 起不来时，把 init.cfg pre-init 的 chmod/chown 路径 + service 依赖的 `/dev` 节点列出来，逐个对内核配置找缺口。常见要审计的节点：

| `/dev` 节点 | 依赖的内核驱动/配置 | 缺失后果 |
|---|---|---|
| `/dev/watchdog` | `CONFIG_WATCHDOG`+`CONFIG_DW_WATCHDOG` + DTS wdt 节点 | watchdog_service open 失败 → init reboot loop（典型 bring-up 卡点） |
| `/dev/binder`、`/dev/hwbinder`、`/dev/vndbinder` | `CONFIG_ANDROID_BINDER_IPC` + 禁 binderfs（见 02 §binderfs） | samgr/foundation 起不来 |
| `/dev/hilog` | hilog 驱动（见下方 §hilog 驱动适配） + mknod | hilog/hiview 起不来 |
| `/dev/ttyS*` | UART 驱动 + DTS uart 节点 | 串口 console/getty 起不来 |
| `/dev/cgroup` 相关 | 内核 cgroup 配置 | 部分 service 依赖 |

> **原则**：rootfs 侧绕过（init.cfg 删 service、mknod 假节点）只在驱动适配短期不可行时作权宜，并标注技术债；驱动适配才是 bring-up 正路。驱动基地址/时钟查 SoC TRM（HiSilicon NDA），查不到**别猜地址**，报 blocker。

### hilog 驱动适配 + mknod 陷阱（实测教训）

OH hilog 驱动（`drivers/staging/hilog`）注册字符设备但**不调 `device_create`** → devtmpfs 不会自动建 `/dev/hilog`，必须在 init.cfg pre-init 手动 `mknod`。

- **mknod 陷阱**：OH init **不支持原生 `mknod` 命令**（init.cfg 的 `exec` 走的是 OH init 内置命令集，无 mknod）。必须 `exec /bin/busybox mknod`：
  ```json
  // init.cfg pre-init jobs
  "exec /bin/busybox mknod /dev/hilog c 245 0",
  "chmod 0666 /dev/hilog"
  ```
- **major 245** = `drivers/staging/hilog/hilog.c` 的 `HILOGDEV_MAJOR`（核对源码确认，别猜主设备号）。
- **chmod 0666**：hilog 需要用户态进程（apphilogcat 等）读写，不放开权限起不来。
- 与上方审计清单配套：hilog 是"驱动有但节点不自动建"的典型——驱动适配（开 `CONFIG_HILOG`）+ pre-init mknod 缺一不可。

> **内核侧驱动适配的完整 playbook 见 `skills/ohos-dev-kernel-node-adapt/` skill**（watchdog 适配见 `skills/ohos-dev-kernel-node-adapt/references/watchdog-adapter-playbook.md`，hilog 适配见 `skills/ohos-dev-kernel-node-adapt/references/hilog-adapter-playbook.md`，binder 32 位协议位宽适配见 `skills/ohos-dev-kernel-node-adapt/references/binder-adapter-playbook.md`，CONFIG→/dev 节点→OH service 依赖映射见 `skills/ohos-dev-kernel-node-adapt/references/config-devnode-map.md`）。本节是方法论引路，落地操作回该 skill。

### 带屏 L1：Display / Touch 驱动（实测未覆盖）

实测是 IPCamera（无屏），没遇到 display。带屏 L1（如带屏智能面板）额外需要：

| 驱动 | 框架 | 关键点 |
|---|---|---|
| **Display** | HDF Display 驱动（L1 精简版） | framebuffer/DRM 接入、屏参（分辨率/时序/背光）从 DTS display 节点读、厂商 GFX 适配 |
| **Touch** | HDF Input 驱动 | I2C 触控 + 中断 + 事件上报（HDF Input 模型） |
| **GPU（可选）** | HDF GPU 驱动或厂商闭源 .so | 2D/3D 加速，多数 L1 用软件渲染即可 |

带屏 L1 的 DTS 必须含 display/touch 节点（bootargs + framebuffer 配置）。参考带屏 L1 适配案例（display/touch 节点 + framebuffer 配置）。

### L0 配置示例

```c
// hals/include/{periph}_config.h
#ifndef {PERIPH_UPPER}_CONFIG_H
#define {PERIPH_UPPER}_CONFIG_H

#define {PERIPH_UPPER}_INSTANCE_COUNT  {count}

typedef struct {
    uint32_t base_addr;
    uint32_t irq_number;
    uint16_t default_pin;
} {PeriphName}Config;

extern const {PeriphName}Config g_{periphName}Configs[{PERIPH_UPPER}_INSTANCE_COUNT];

#endif
```

### L1 HCS 配置示例 (如适用)

```hcs
root {
    platform {
        {peripheral}_controller_0x{addr} {
            match_attr = "{peripheral}_controller_0";
            num = {count};
            /* ... 属性从 3a 规格提取 */
        }
    }
}
```

参考工具: `skills/ohos-dev-board-config-gen/references/hcs-syntax-and-config.md`

---

## Step 3d: RTOS 驱动迁移（可选）

当用户有现有 FreeRTOS / RT-Thread / Zephyr 驱动代码时触发。

### 映射关系

| FreeRTOS | 目标 OS (OH LiteOS-M) | 变更点 |
|----------|----------------------|--------|
| `xTaskCreate()` | `LOS_TaskCreate()` | 参数结构不同 (TcbTaskConfig) |
| `xQueueCreate/Send/Receive` | `LOS_Queue*` | API 名称不同，语义相同 |
| `xSemaphoreCreate/Mutex` | `LOS_Mux/Sem*` | Mutex 和 Semaphore 分开 |
| `xTimerCreate/Start/Stop` | `LOS_Swtmr*` | 回调签名略有不同 |
| `vTaskDelay()` | `LOS_TaskDelay()` | 参数单位可能不同 (tick vs ms) |
| `portENTER_CRITICAL()` | `LOS_IntLock()` | 同 |
| `taskYIELD()` | `LOS_Schedule()` | 同 |

### 迁移步骤

1. **识别 RTOS 原语调用** — grep 所有 `xTask`/`xQueue`/`xSemaphore`/`xTimer`/`vTask`
2. **逐个替换为 OH 对等 API** — 用上表映射
3. **调整参数结构** — TcbTaskConfig 替代 TaskParameters
4. **处理 include 路径** — `FreeRTOS.h` → `los_task.h`/`los_queue.h` 等
5. **编译验证** — 替换后立即编译，不积累错误

参考: 本步骤 `references/rtos-migration/api-mapping-tables.md`

---

## 引用的 tools/

| 工具 | 用途 | 路径 |
|------|------|------|
| ohos-dev-soc-spec-parse | 外设寄存器/中断/时钟/引脚规格提取 | `skills/ohos-dev-soc-spec-parse/` |
| ohos-dev-board-config-gen | HCS 配置生成 / linker 片段 / IoT HAL 模型 | `skills/ohos-dev-board-config-gen/` |
| ohos-dev-build-config | GN 语法 / error cheatsheet | `skills/ohos-dev-build-config/` |
| ohos-dev-hal-skeleton-gen | HAL 驱动骨架生成（GPIO/UART/I2C/PWM/...） | `skills/ohos-dev-hal-skeleton-gen/` |
| ohos-dev-rtos-migrate | RTOS→LiteOS API 映射（可选 Step 3d） | `skills/ohos-dev-rtos-migrate/` |

## 语料索引

- **★ WiFi 架构分析**: `skills/ohos-dev-board-config-gen/references/wifi_hal_architecture.md` (~10KB) ← **复杂驱动核心输入**
- **★ SDK API 映射**: `skills/ohos-dev-board-config-gen/references/hi3861_sdk_api_crossref.md` (~12KB) ← **命名约定**
- **IoT HAL 驱动模型**: `skills/ohos-dev-board-config-gen/references/l0-iot-hal-driver-model.md` (9 个 HAL API 清单)
- **Hi3861V100 adapter 结构**: `skills/ohos-dev-soc-spec-parse/references/hi3861v100-adapter-structure.md`
- **HCS 语法**: `skills/ohos-dev-board-config-gen/references/hcs-syntax-and-config.md`
- **RTOS 迁移**: 本步骤 `references/rtos-migration/api-mapping-tables.md`

---

## Agent Dispatch Spec

### 分发规格

| 属性 | 值 |
|------|-----|
| **agent_role** | `driver-expert` |
| **category** | `deep` |
| **load_skills** | `[ohos-dev-soc-spec-parse, ohos-dev-board-config-gen, ohos-dev-build-config, ohos-dev-hal-skeleton-gen, ohos-dev-rtos-migrate]` |
| **dispatch_mode** | **部分并行**: G1=[3a(按需)] → G2=[3b(可按外设并行)] → G3=串行[3c→3d(可选)] |
| **parallel_groups** | 3b 内部: 简单驱动可并行生成; 复杂驱动(WiFi) 串行 |

### Agent Prompt 模板

```
1. TASK:
   为 {chip_model} ({arch}) 生成外设驱动代码和设备配置 (Phase 3)。
   实测验证: L3 simple drivers 0-73%, complex/WiFi 0%.
   已产出修复文档: wifi_hal_architecture.md + sdk_api_crossref.md。

2. 核心决策:
   A. 读 target profile 的 driver_model 字段决定驱动框架 ({{ASSET_ROOT}}/workflow/target-profiles/,
      P2 已选定; 不从 L0/L1 标签推断):
      driver_model = iot_hal → IoT HAL 模型, 无 HCS, 简单配置
      driver_model = hdf → HDF 模型, 需要 HCS device tree
      driver_model = linux_kernel / linux_kernel_plus_oh_integration → Linux 内核驱动
        (defconfig + DTS) + vendor HAL 集成, 无 HCS
   B. 每个外设 → 判断简单还是复杂 → 选择生成策略

3. 简单驱动 (GPIO/I2C/SPI/PWM/UART):
   使用 3b-1 模板 (寄存器直接读写模式)。
   必须读 sdk_api_crossref.md 获取底层 SDK 函数命名约定。

4. 复杂驱动 (WiFi/Ethernet/Display):
   ★ 必须先读 wifi_hal_architecture.md 了解 7 层架构!
   使用 MVP First 策略: 先生成 ~400 行核心功能, 不要试图一步到位。

5. 系统驱动 (watchdog/reset/lowpower):
   需要芯片系统级知识 (上电序列/复位拓扑/电源域)。
   如果 datasheet 信息不足 → 标记为 TODO 并记录缺失信息。

6. EXPECTED OUTCOMES:
   ① hals/{peripheral}/hal_{name}.c (每个外设一个)
   ② 设备配置 (L0: config.h / L1: *.hcs)
   ③ P2 的 BUILD.gn sources 列表更新 (加入新 .c 文件)
   ④ (可选) RTOS migration mapping table

7. MUST DO:
   - [ ] 先读 target profile 的 driver_model (决定驱动模型, 不从 L0/L1 标签推断)
   - [ ] 简单驱动用模板 (3b-1), 复杂驱动用 MVP 策略
   - [ ] 复杂驱动必须先读 wifi_hal_architecture.md
   - [ ] 所有驱动必须查 sdk_api_crossref.md 确认 SDK 函数名
   - [ ] 更新 P2 BUILD.gn 的 sources 列表
   - [ ] driver_model 非 hdf 不生成 HCS (如 iot_hal / linux_kernel, 跳过 HCS 相关部分)

8. MUST NOT DO:
   - [ ] 不要对所有驱动用同一策略 (简单≠复杂)
   - [ ] 不要试图一次性生成 WiFi 全部 7 层 (MVP first!)
   - [ ] 不要猜 SDK 函数名 (查 sdk_api_crossref.md)
   - [ ] 不要对 L0 目标生成 HCS 文件
   - [ ] 不要忽略系统驱动的特殊需求 (它们不是模板化的)

9. CONTEXT:
   上游: P2 (BUILD.gn sources 结构待填充) + P1 (chip-spec)
   下游: P4 (build-verify) 编译包含这些驱动
   参考: posix_ref_impl.md (P2 KAL) 与本阶段的驱动是独立但互补的
```

## MUST DO (实测血泪教训)

- [ ] **区分简单/复杂/系统三类驱动** — 不同策略 (实测证明一刀切失败)
- [ ] **简单驱动用寄存器读写模板** — 实测验证 GPIO/I2C/PWM/UART 全部 PASS
- [ ] **复杂驱动 MVP First** — 不要试图一次写完 WiFi 993 行
- [ ] **必须查 SDK API 映射表再写底层调用** — 函数名猜错 = 编译错误
- [ ] **L0 不生成 HCS** — wifiiot 不使用 HDF 设备树
- [ ] **更新 P2 BUILD.gn sources** — 漏加 .c = undefined reference
- [ ] **系统驱动标记信息缺口** — 缺 datasheet 就标 TODO, 不要瞎编

## MUST NOT DO (实测血泪教训)

- ❌ 不要把 GPIO 的模板套到 WiFi 上 (复杂度差 10 倍)
- ❌ 不要忽略 L0/L1 驱动模型差异 (IoT HAL ≠ HDF)
- ❌ 不要猜 SDK 函数名 (Hi3861 是 `HalGpioWrite` 不是 `GPIO_Write`)
- ❌ 不要对 L0 生成 HCS (编译不报错但不纳入构建, 浪费时间)
- ❌ 不要认为 watchdog/reset/simple 一样 (它们依赖芯片系统知识)

---

## L1 子系统适配 checklist

> **范围声明**：本节针对 **L1（LiteOS-A / Linux，本仓 hi3516cv610）** 的子系统适配。L1 的子系统组成与 L0（LiteOS-M / wifiiot，IoT 外设驱动子系统）**不同**——L0 不走 HDF、子系统更精简，本节不适用 L0（L0/L1 分流见 `ohos-dev-soc-spec-parse` skill）。
>
> 本节是**引路汇总**，不重复 P3/P4 既有内容，只把散落在 P3/P4 的子系统适配点显性化 + 给出官方 subsys 文档 URL。各项展开回 P3/P4 对应章节查。

| 子系统 | L1 适配关键 | 官方文档 URL | 本仓既有内容 |
|---|---|---|---|
| **启动** | `OHOS_SystemInit`（bootstrap）注册顺序、`samgr_lite` A 核模式、init/begetutil 启动参数与配置 | `https://gitee.com/openharmony/docs/raw/master/zh-cn/device-dev/porting/porting-minichip-subsys-startup.md` | P2 启动代码 / P4 构建产物（boot_image+env+uImage+rootfs+xml） |
| **文件** | vfs HAL（`HalFileOpen`/`HalFileRead`/`HalFileWrite`）、文件系统挂载（ubifs/jffs2，rootfstype↔rootfs↔xml 一致性） | `https://gitee.com/openharmony/docs/raw/master/zh-cn/device-dev/porting/porting-minichip-subsys-filesystem.md` | P3 §SPI Nand 驱动适配（颗粒 ID 表两侧补）、P4 烧录包消费者验收 |
| **安全** | huks（密钥存储）、device_auth（设备认证）组件接入与 HAL 实现 | `https://gitee.com/openharmony/docs/raw/master/zh-cn/device-dev/porting/porting-minichip-subsys-security.md` | P3 §M4 安全模式维度（secure boot / TEE / image 签名显式声明） |
| **通信** | dsoftbus（软总线）、wifi_lite（轻量 WiFi）组件适配与网络协议栈对接 | `https://gitee.com/openharmony/docs/raw/master/zh-cn/device-dev/porting/porting-minichip-subsys-communication.md` | P3 §3b-2 复杂驱动策略（WiFi 7 层架构 MVP） |

### 使用方式

1. **先判 L0/L1**：系统级别判断见本 SKILL §Step 3b 前置决策（L0/L1 标签由 target profile 的 system_type 推导，config 值域映射：mini=L0 轻量 / small=L1 小型）。L1 才进本 checklist。
2. **逐子系统对照**：按上表"适配关键"列出的点逐项检查实现是否覆盖；缺失项回 P3/P4 对应章节补。
3. **查官方文档**：URL 指向 OpenHarmony 官方 porting-minichip-subsys-* 系列，作为权威适配参考（L1 小型系统子系统移植指南）。
4. **跨产物一致性**：文件子系统的 rootfstype ↔ rootfs ↔ xml、启动子系统的 bootargs ↔ 实际产物，是 P4 §交付物消费者验收的跨产物一致性检查项，本节不重复。

> **L0 不适用**：L0（LiteOS-M）子系统组成不同（IoT 外设驱动子系统、无 HDF、无 samgr_lite A 核模式），本 checklist 不适用 L0 适配。

## L1 子系统选配 + init 配置步骤 ★ 必做（实测教训）

> **为什么有这一步**：Hi3516CV610裸烧进 OH shell 后 `ps -A` 只有 busybox `init`（PID 1）+ `/bin/sh`（PID 705），**缺所有 OH 系统服务**——samgr/foundation/hilog/dsoftbus/wifi/huks 一个都没起。根因：rootfs 的 init 脚本（`=== Hi3516CV610 SPI Nor boot OK ===` / `=== rootfs=jffs2 from /dev/mtdblock3 ===`）是过时 busybox-only 脚本，**只起 sh，没把 OH 子系统组件和 init 配置打进 rootfs**。OH 在 L1 不是"装了就全起"——子系统按需选配，init 配置（`init_linux_openharmony.cfg`）定义起哪些进程/jobs/services，**没有 init 配置 + 没有子系统组件 = 起的进程少**。

### 步骤要点（执行者按序）

1. **问用户需要哪些 OH 子系统**（P-前置采集，不准替用户决定）：
   按上方 L1 checklist 表（启动/文件/安全/通信）+ 媒体/显示等，让用户勾选。典型组合：
   - 最小启动：samgr_lite + init + hilog（hiview/apphilogcat）+ foundation
   - 通信：dsoftbus（softbus_server）+ wifi_lite（wifi_manager_service/wifi_hal_service）
   - 安全：huks（huks_server）+ device_auth（deviceauth_service）
   - 媒体/显示：media_server + wms_server（带屏 L1）
   - 应用框架：appspawn + bundle_daemon
   用户选配结果写入 `workflow_config.yaml`（如 `subsystems.selected: [startup, hilog, dsoftbus, wifi_lite, huks, ...]`）。

2. **让用户提供对应 init 配置**（`init_linux_openharmony.cfg` 或等价）：
   - **参考标准**：OpenHarmony 官方 hi3516 linux L1 init 配置——上游 `openharmony/vendor_hisilicon/hispark_taurus_linux/init_configs/init_linux_3516dv300_openharmony_{debug,release}.cfg`（gitcode `HiSpark/ohos_aiot_solution` 仓 `patch/vendor/hisilicon/hispark_hi3516cv610_linux/init_configs/init_linux_openharmony.cfg` 为同源 cv610 版本，gitcode raw 常被 HTML 拦截，降级走 gitee 上游同构 cfg）。
   - 该 cfg 定义 `jobs`（pre-init/init/post-init 的 mkdir/chmod/chown/start 序列）+ `services`（每个进程的 path/uid/gid/caps/socket）。
   - 执行者**不凭空编造 cfg**——要么用用户提供的，要么基于上游标准 cfg 按用户选配的子系统裁剪（删未选子系统的 service + 对应 job 行）。裁剪后显式声明"基于上游 X cfg 裁剪，删了 Y/Z"。

3. **工作流据此配置 rootfs**（P4 §Step 4.5 rootfs 构建的输入）：
   - **子系统组件**：用户选的子系统对应的可执行文件（samgr/foundation/softbus_server/huks_server/...）+ 依赖 .so 打进 rootfs `/bin` + `/lib`（B 类：从用户 SDK/OH 编译产物取，不手工编）。
   - **init 配置**：裁剪后的 `init_linux_openharmony.cfg` 放 rootfs `/etc/init.cfg`（或 init 读的路径）。
   - **init 脚本**：rootfs 的 `/sbin/init`（或 `/etc/inittab`/`/etc/init.d/rcS`）必须是 OH init（begetutil），不是 busybox init。实测症结就是 rootfs 用 busybox init + 过时脚本，没接 OH init。把 busybox init 换成 OH init（或让 OH init 作为 `/sbin/init`），由 init.cfg 驱动起子系统进程。
   - **目录/权限**：cfg `pre-init` job 里的 mkdir/chmod/chown（`/storage/data/dsoftbus`、`/storage/maindata/hks_client`、`/dev/binder`、`/dev/hilog` 等）必须在 rootfs 预建或由 init job 创建，否则子系统起不来（如 dsoftbus 找不到 `/storage/data/dsoftbus`、hilog 找不到 `/dev/hilog`）。

4. **验证 OH 启动后起对应子系统进程**（不只 busybox sh）：
   烧录启动后串口 `ps -A`，对照用户选配 + cfg services 列表核对：
   - ✅ 通过：每个选配子系统对应进程在 ps 列表（samgr/foundation/hiview/softbus_server/wifi_manager_service/huks_server/...）
   - ❌ 失败（实测症结复现）：只有 `init` + `/bin/sh`，无 OH 服务 → 回步骤 3 检查 rootfs 是否打了子系统组件 + init.cfg + 用的是 OH init 而非 busybox init
   - 部分起：起了 samgr 但 dsoftbus 没起 → 查该 service 的 path 文件是否在 rootfs、依赖 .so 是否齐、pre-init 目录是否建

### 标准该起的进程（上游 init_linux_3516dv300_openharmony.cfg 参考）

> 以下是 hi3516 linux L1 标准配置定义的 services，作为用户选配 + 裁剪的基线。实测 log.txt 起的（busybox init + sh）对比此基线**全缺**。

| 子系统 | 标准进程（service name → path） | 实测 log.txt 状态 |
|---|---|---|
| 启动/系统 | `foundation` → `/bin/foundation` | ❌ 缺 |
| 启动/应用 | `appspawn` → `/bin/appspawn`、`bundle_daemon` → `/bin/bundle_daemon` | ❌ 缺 |
| 日志 | `hiview` → `/bin/hiview`、`apphilogcat` → `/bin/apphilogcat`、`faultloggerd` → `/bin/faultloggerd` | ❌ 缺 |
| 安全 | `huks_server` → `/bin/huks_server`、`deviceauth_service` → `/bin/deviceauth_service` | ❌ 缺 |
| 通信/dsoftbus | `softbus_server` → `/bin/softbus_server`、`devicemanagerservice` → `/bin/devicemanagerservice` | ❌ 缺 |
| 通信/wifi | `wifi_manager_service` → `/bin/wifi_manager_service`、`wifi_hal_service` → `/bin/wifi_hal_service` | ❌ 缺 |
| 媒体/显示 | `media_server` → `/bin/media_server`、`wms_server` → `/bin/wms_server` | ❌ 缺 |
| 设备认证 | `devattest_service` → `/bin/devattest_service` | ❌ 缺 |
| 内核事件 | `ueventd` → `/bin/ueventd_linux`、`watchdog_service` → `/bin/watchdog_service` | ❌ 缺 |
| shell | `shell` → `/sbin/getty -n -l /bin/sh -L 115200 ttyS000 vt100` | ✅ 仅此（但实测是 busybox sh，非 getty） |

> **init job 关键前置**（pre-init 必须先做，否则 service 起不来）：`chmod 0666 /dev/binder`、`chown 4 4 /dev/hilog`、`mkdir /storage/data/dsoftbus`、`mkdir /storage/maindata/hks_client/{info,key}`、`mkdir /storage/deviceauth`、`chmod 0666 /dev/hdf/hdfwifi`、`export LD_LIBRARY_PATH /storage/app/libs`、`export LD_PRELOAD /usr/lib/libdfx_signalhandler.so`。

> **参考 URL**：
> - 上游标准 cfg（可直接用/裁剪）：`https://gitee.com/openharmony/vendor_hisilicon/raw/master/hispark_taurus_linux/init_configs/init_linux_3516dv300_openharmony_debug.cfg`
> - gitcode cv610 同源 cfg（raw 常被 HTML 拦截，降级用上面 gitee）：`https://gitcode.com/HiSpark/ohos_aiot_solution/blob/main/patch/vendor/hisilicon/hispark_hi3516cv610_linux/init_configs/init_linux_openharmony.cfg`
> - L1 子系统移植官方文档：见本节上方 checklist 表"官方文档 URL"列
