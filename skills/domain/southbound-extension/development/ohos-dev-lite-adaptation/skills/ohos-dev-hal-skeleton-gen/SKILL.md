---
name: ohos-dev-hal-skeleton-gen
description: OpenHarmony Lite HAL 驱动骨架生成器——基于芯片规格生成 L0 IoT 外设驱动子系统 / L1 精简版 HDF 驱动骨架代码（GPIO/I2C/SPI/UART/ADC/PWM/RTC/Watchdog 等），含配套 BUILD.gn 和 HCS 设备绑定。Use when peripheral driver skeleton code is needed for an OpenHarmony Lite (L0/L1) adaptation; triggers include 生成 GPIO/I2C/SPI/UART/ADC/PWM 驱动、HdfDriverEntry、Bind/Init/Release/Dispatch、GpioMethod、驱动 .ko 加载了但 Bind/Init 不被调用、match_attr 无对端、device_info.hcs deviceNode 片段、irqStart / OsalRegisterIrq 中断号换算、IoTGpioInit 类 L0 HAL 接口、GpioOperations 组件化注册、厂商 SDK API 映射（hi_*/lz_*/osal_*/ot_*）。
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: hal
  capability: skeleton-gen
  version: 0.1.0
  status: trial
---

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 完整生成任务 | "给 XX 生成 GPIO 驱动"、"写一个 UART 的 HDF 驱动骨架"、"生成 I2C 驱动 + HCS + BUILD.gn" |
| 单点问题 | "match_attr 报错怎么配"、"IRQ 该填 23 还是 55"、"厂商 SDK 没有 GPIO API 怎么办"、"moduleName 和 BUILD.gn module_name 什么关系" |
| 症状词（隐性需求） | ".ko 加载了但驱动不工作"、"HDF 找不到 deviceNode"、"Bind/Init 没被调用"、"中断注册到错误 IRQ"、"setIrq/enableIrq 不生效" |
| 下游 skill 链式调用 | ohos-dev-board-config-gen 产出 HCS 后驱动侧配套；ohos-test-lite-ut-gen 需要驱动接口做被测对象 |
| 同义表达 | 外设驱动适配 / HAL 层 / 驱动骨架 / 平台驱动 |

**不触发**（明确排除）：HCS 主文件与 device_info.hcs 全量生成（→ ohos-dev-board-config-gen，本 SKILL 只生成驱动的 `*_config.hcs` 与 device_info.hcs 对端片段）；测试用例生成（→ ohos-test-lite-ut-gen）；RTOS 迁移重构（→ ohos-dev-rtos-migrate）；芯片规格提取（→ ohos-dev-soc-spec-parse）。

## Scope

本 SKILL 是 OpenHarmony Lite（L0 轻量系统 / L1 小型系统）新芯片适配的**HAL 驱动层**：基于上游 ohos-dev-soc-spec-parse 输出的 `chip_spec.json`，生成外设驱动的骨架代码（.c/.h）、编译配置（BUILD.gn）和 HCS 设备绑定（L1），让驱动框架能正确加载并调用硬件操作。

**本 SKILL 生成驱动骨架（函数框架 + 寄存器操作位 + Method/HdfDriverEntry 注册）**，不填充芯片特有的业务逻辑（如 DMA 配置、电源管理、厂商私有协议）。

### 生成文件清单

| 系统级别 | 本 SKILL 生成的文件 | 说明 |
|---------|-------------------|------|
| **L0** | `hal_iot_<periph>.c`、`hal_iot_<periph>.h`、`BUILD.gn` | IoT 外设驱动子系统方式，直接寄存器操作，Method 结构体注册 |
| **L1** | `<periph>_driver.c`、`<periph>_driver.h`、`<periph>_config.hcs`、`BUILD.gn`、**`device_info.hcs` 对端片段** | 精简版 HDF 方式，HdfDriverEntry + Bind/Init/Release/Dispatch |

> 文件已存在时检查内容正确性而非覆盖。L1 的 `device_info.hcs` 主文件和 `hdf.hcs` 入口由 ohos-dev-board-config-gen 生成；本 SKILL 生成各外设的 `*_config.hcs`，**并一并生成 `device_info.hcs` 中该外设的 deviceNode 对端片段**（见 Step 3 L1 第 4 步）——只写 `*_config.hcs` 一侧而不改 device_info.hcs 是实测翻车根因，HDF 框架找不到 deviceNode 则驱动 .ko 加载了但 Bind/Init 不被调用。

**输入**：上游 `chip_spec.json`（必需，寄存器/中断/位域来源）+ 目标外设清单 + L1 额外的 moduleName/serviceName + 厂商 SDK 头文件（调 SDK 函数路线时必需）。
**不适用**：完整业务驱动开发；HCS 配置体系全量生成；非 OpenHarmony Lite 目标。

## Initial Checks

收到任务后，按以下顺序先做判断（各步结论决定后续路径）：

1. **上游输入判断**：有 `chip_spec.json`？→ 取 `peripherals[].baseAddress` / `registers[]` / `interrupts[]`；无 → 追问用户或回 ohos-dev-soc-spec-parse，**禁止凭记忆填寄存器/中断**。
2. **系统级别 L0/L1 判定**：决定驱动框架路线（L0 = IoT 外设驱动子系统 + 组件化注册；L1 = 精简版 HDF + HdfDriverEntry + OSAL + HCS），两条路线代码形态完全不同，不混用。
3. **驱动实现路线选择**（Step 1b）：扫描厂商 SDK 头文件有无该外设 API → 调 SDK 函数路线 vs 寄存器直写路线（如 Hi3516CV610 无 GPIO 外设 API，走 PL061 寄存器直写）。
4. **SDK API 命名族识别**：读 SDK `include/` 顶层头文件名判断命名族（`hi_*.h`/`lz_*.h`/`osal_*.h`/`ot_*.h`），别按芯片名猜全叫 `hi_*`。
5. **L1 对端文件现状**：产品 `device_info.hcs` 是否已存在 + 该外设当前是否在用 `linux_*_adapter` → 决定对端片段形式（并入片段 + 位置说明 vs 完整文件）与替换/并存策略。
6. **目标外设清单与 moduleName/serviceName**：L1 必填，用户指定或按 HDF 命名约定推断。

## Prohibited Practices（HAL驱动禁止操作）

| 禁止 | 正确做法 |
|------|---------|
| L0 生成 HDF 框架代码（HdfDriverEntry/Bind/Init/GpioMethod/GpioCntlrAdd） | L0 = IoT 外设驱动子系统 + 组件化注册（GpioOperations/GpioRegisterOps 等，非 HDF）；L1 = HDF（GpioMethod/GpioCntlrAdd） |
| L1 不生成 HCS 配置文件或 BUILD.gn | L1 驱动 = .c/.h + *_config.hcs + BUILD.gn，三者必须配套 |
| 凭记忆填寄存器基地址/位域 | 从 ohos-dev-soc-spec-parse 输出的 chip_spec.json 取 `peripherals[].baseAddress` 和 `registers[]` |
| match_attr 与 device_info.hcs 不一致 | `*_config.hcs` 的 `match_attr` 必须与 `device_info.hcs` 的 `deviceMatchAttr` **严格相等** |
| L0 使用 OSAL 接口 / L1 直接操作寄存器 | L0 = 直接寄存器操作 + CMSIS / 厂商 SDK API（hi_*/lz_*）；L1 = OSAL 封装（OsalIoRead32/OsalIoWrite32） |
| L1 只写 `*_config.hcs` 不生成 `device_info.hcs` 对端 | **必须一并生成 `device_info.hcs` 的 deviceNode 片段**（含 `moduleName`/`serviceName`/`deviceMatchAttr`），否则 HDF 框架找不到 deviceNode，驱动 .ko 加载了但 Bind/Init 不被调用（实测翻车根因） |
| 只认 `hi_*` SDK API 命名 | 厂商 SDK API 命名多样：Hi3861 用 `hi_*`（hi_gpio_set_dir）、RK2206 用 `lz_*`/`Lz*`（LzGpioInit）、Hi3516cv610 SDK 用 `osal_*`+`ot_*`（无 GPIO 外设 API，走寄存器直写）。读 SDK 头提取实际命名，别假设全叫 `hi_*` |
| 跳过 BUILD.gn 只生成 .c/.h | 驱动必须声明编译依赖，L0 用 `lite_component`，L1 用 `hdf_driver` |
| 在驱动的 .c 文件中编造未从 chip_spec.json 提取的硬件参数 | 取不到的字段**先上网查（用宿主联网检索能力，WebSearch 或等价物；坏用备选联网检索 CLI，如 opencode）**，查到填值并注明来源；确实查不到才标 `/* TODO: extract from datasheet §<section> */` 并注明来源/查询关键词，禁止凭记忆编造 |

---

## ① 文件路由表

根据用户意图，读取对应的参考文件。**每次只读一个**，不要一次性加载所有 reference。

| 用户意图 | Agent 读取 | 预估行数 |
|---------|-----------|:-------:|
| 理解 L0/L1 驱动框架差异（架构/API/注册方式） | `references/hdf-iot-driver-framework.md` | ~330 |
| 查外设 Method 接口定义（GPIO/I2C/SPI/UART/ADC/PWM/RTC/Watchdog） | `references/peripheral-api-specs.md` | ~150 |
| 生成 L0 驱动 .c/.h（IoT 外设驱动子系统骨架） | `references/driver-code-templates.md` §L0 | ~350 |
| 生成 L1 驱动 .c/.h（HDF 骨架：HdfDriverEntry + Bind/Init/Release） | `references/driver-code-templates.md` §L1 | ~350 |
| 生成 L1 *_config.hcs（外设 HCS 配置） | `references/hcs-config-templates.md` | ~315 |
| 生成 BUILD.gn（L0 lite_component / L1 hdf_driver） | `references/hcs-config-templates.md` §BUILD.gn | ~80 |
| 查已有芯片驱动实现（Hi3861/BES2600W/Hi3516DV300/ESP32） | `examples/<level>/<chip>/` 目录（Hi3861 L0 / STM32MP1 L1 真实样本）+ `references/field-patterns.md`（实测生成模式） | ~80/套 + ~350 |
| 查 OSAL 接口用法（L1 寄存器读写封装） | `references/hdf-iot-driver-framework.md` §OSAL | ~80 |
| 查厂商 SDK API 命名与映射套路（hi_*/lz_*/osal_*/ot_*） | `references/field-patterns.md` §API 映射套路 | ~200 |
| 查实测生成模式（L0 IoT HAL / L1 HDF / HCS 配对 / BUILD.gn） | `references/field-patterns.md` | ~350 |
| 需要参照已有芯片驱动实现 | `examples/<level>/<chip>/` 目录 | ~80/套 |

### 系统级别 → 样本目录映射

| 系统级别 | 代表芯片 | 样本目录 | 展示内容 |
|---------|---------|---------|---------|
| L0 轻量系统（MCU） | Hi3861 | `examples/l0/hi3861/` | IoT 外设驱动子系统：IoT API 适配 + 寄存器操作 |
| L1 小型系统（MPU） | STM32MP1 | `examples/l1/stm32mp1/` | 精简版 HDF：HdfDriverEntry + OSAL + HCS 绑定 |

---

## ② 工作流

### Step 1: 收集上游输入

生成驱动前，必须收集以下信息。优先从 ohos-dev-soc-spec-parse 输出的 `chip_spec.json` 读取，缺失项需追问用户：

| 必填项 | 来源 | 示例 |
|-------|------|------|
| 芯片名称 | chip_spec.json `metadata.chipName` | STM32F407ZG |
| 系统级别（L0/L1） | chip_spec.json `metadata.targetSystemLevel` | L0 |
| CPU 架构 | chip_spec.json `cpu.coreType` | cortex-m4 |
| 目标外设列表 | 用户输入 | GPIO, UART0, I2C0, SPI1 |
| 各外设寄存器基地址 | chip_spec.json `peripherals[].baseAddress` | 0x40020000 |
| 各外设中断号 | chip_spec.json `peripherals[].interrupts[]` | 37 (USART1) |
| 各外设时钟门控 | chip_spec.json `clockSystem.peripheralClockGates[]` | APB2, bit 14 (USART1) |

**L1 额外必填**：

| 必填项 | 来源 |
|-------|------|
| moduleName（驱动模块名） | 用户指定或从 HDF 命名约定推断 |
| serviceName（对外服务名） | 用户指定或从 moduleName 推导 |

### Step 1b: 驱动实现路线选择（寄存器直写 vs 调 SDK 函数）★ C7 增强

驱动底层实现有两条路线，生成前必须选定（影响 .c 里 Init/Read/Write 的函数体）：

| 路线 | 输入 | 函数体做法 | 适用 |
|---|---|---|---|
| **寄存器直写** | `chip_spec.json` 的 `peripherals[].registers[]` | 直接 `OsalIoRead32/Write32` 操作寄存器偏移 | SDK 不提供外设驱动 API / 学习型芯片 / 简单外设 |
| **调 SDK 函数** | **SDK 头文件**（B 类，厂商提供 `.h`） | 驱动 Method 函数体调 SDK API（如 `hi_gpio_write`/`hi_i2c_write`），映射逻辑自己写 | SDK 提供外设驱动 API / 复杂外设（省得自己写时序） |

**调 SDK 函数路线的生成步骤（C7）**：
1. **读 SDK 头**：扫描厂商 SDK 的外设头文件（`hi_gpio.h`/`hi_i2c.h`/`hi_uart.h` 等），提取 API 函数签名（`hi_gpio_set_dir`/`hi_gpio_write`/`hi_i2c_write`...）。可用 `ohos-dev-soc-spec-parse` 解析 SDK headers，或 grep `hi_*`/`Hal*`/`lz_*`/`Lz*`/`osal_*`/`ot_*` 函数声明
2. **建映射**：OH HAL Method 接口（`GpioMethod.Write` 等）→ SDK API（`hi_gpio_write`）映射表。**映射逻辑自己写，不抄厂商驱动源码**（A 类：需 SDK 头做输入，但映射是自己的）
3. **生成驱动**：Method 函数体调映射好的 SDK API，不是裸寄存器操作
4. **查命名约定**：参考 `hi3861_sdk_api_crossref.md`（9 个 HAL 驱动的 SDK 函数命名模式）+ `references/field-patterns.md` §API 映射套路（hi_*/lz_*/osal_*/ot_* 各厂映射模式），别猜 SDK 函数名

> **厂商 SDK API 命名多样，别假设全叫 `hi_*`**（实测经验）：
> - **Hi3861 SDK**：`hi_*` 小写（`hi_gpio_set_dir`/`hi_i2c_write`），枚举 1:1 兼容直接强转，返回值透传
> - **RK2206 Lockzhiner SDK**：`lz_*`/`Lz*`（`LzGpioInit`/`LzGpioSetDir`），返回值需 `LZ_HARDWARE_SUCCESS → IOT_SUCCESS` 转换，中断类型+极性双参数需合并成单枚举
> - **Hi3516cv610 SDK**：`osal_*`（OSAL 抽象层）+ `ot_*`（媒体/安全接口），**GPIO/UART 等基础外设无厂商 API**，走寄存器直写路线（PL061/PL011）；`ot_*` 仅媒体子系统用，HAL 驱动不直接调
> - **其他厂商**：读 SDK `include/` 顶层头文件名判断命名族（`hi_*.h`/`lz_*.h`/`osal_*.h`/`ot_*.h`/`hal_*.h`），别凭芯片名猜

> **禁止**：凭记忆/想象编造 SDK 函数名——必须从 SDK 头文件实际提取。无法获取 SDK 头时，标 `/* TODO: extract SDK API from <header> */` 并退回寄存器直写路线，不准瞎编 SDK 调用。
> **A/B/C 分类落地**：驱动代码属 A 类（自己写映射，但需 SDK 头做输入）；SDK 头本身是 B 类（厂商提供，include 用）；SDK 预编译库是 B 类（链接用）。不抄厂商驱动源码。

### Step 2: 判定系统级别与驱动框架

```
系统级别判定：
├── L0（MCU, LiteOS-M, 无 MMU）
│   └── 框架：IoT 外设驱动子系统（非 HDF）
│       注册方式：组件化注册（GpioOperations + GpioRegisterOps 等，非 HdfDriverEntry）
│       硬件操作：直接寄存器读写 + CMSIS 接口
│       编译配置：lite_component 模板
│       配置文件：无 HCS（编译时常量在 board_config.h）
│
└── L1（MPU, LiteOS-A / L1-Linux, 有 MMU）
    └── 框架：精简版 HDF
        注册方式：HdfDriverEntry（Bind / Init / Release）+ IDeviceIoService.Dispatch
        硬件操作：OSAL 封装（OsalIoRead32 / OsalIoWrite32）
        编译配置：hdf_driver 模板
        配置文件：*_config.hcs + device_info.hcs 绑定
```

### Step 3: 生成驱动骨架

对每个目标外设，按顺序生成文件。

#### L0 生成顺序

```
hal_iot_<periph>.h → hal_iot_<periph>.c → BUILD.gn
```

1. **头文件 .h**：Read `references/driver-code-templates.md` §L0 头文件模板，参照 `examples/l0/hi3861/`
   - 包含：寄存器偏移宏定义（从 chip_spec.json 的 `registers[]` 提取）、Device 结构体、HAL 函数声明
2. **源文件 .c**：Read `references/driver-code-templates.md` §L0 源文件模板
   - 包含：操作函数表实例化（GpioOperations 等，非 GpioMethod）、Init/Deinit/Read/Write 实现骨架、组件化注册函数（GpioRegisterOps 等）
3. **BUILD.gn**：Read `references/hcs-config-templates.md` §L0 BUILD.gn
   - 使用 `lite_component("hal_iot_<periph>")` 模板

#### L1 生成顺序

```
<periph>_driver.h → <periph>_driver.c → <periph>_config.hcs → device_info.hcs 对端片段 → BUILD.gn
```

1. **头文件 .h**：Read `references/driver-code-templates.md` §L1 头文件模板
   - 包含：Device 结构体（含 OsalIo 句柄）、Dispatch 命令码枚举
2. **源文件 .c**：Read `references/driver-code-templates.md` §L1 源文件模板，参照 `examples/l1/stm32mp1/`
   - 包含：HdfDriverEntry 实例（`.Bind` / `.Init` / `.Release`）、Bind 返回 `HdfDeviceObject` 的 service、Init 中注册 Method 接口、Dispatch 中实现 IoService 命令码、`HDF_INIT(g_<periph>DriverEntry)`
3. **\*\_config.hcs**：Read `references/hcs-config-templates.md` §外设 HCS
   - 包含：`root { <periph>_config { match_attr = "..."; ... } }`
   - **关键约束**：此处的 `match_attr` 值与 `device_info.hcs` 中的 `deviceMatchAttr` **必须严格相等**
4. **`device_info.hcs` 对端片段**：Read `references/hcs-config-templates.md` §device_info.hcs + `references/field-patterns.md` §HCS 配对写法
   - **必须生成**该外设在 `device_info.hcs` 的 `platform` host 下的 `device_<periph>` deviceNode 片段（含 `moduleName`/`serviceName`/`deviceMatchAttr`），与第 3 步的 `*_config.hcs` 配对
   - 生成形式：若产品 `device_info.hcs` 已存在，输出**待并入的 deviceNode 片段 + 并入位置说明**（如 `device_gpio :: device { device1 :: deviceNode { ... } }`）；若不存在，输出完整 `device_info.hcs`
   - **实测翻车根因**：只写 `*_config.hcs` 一侧、不改 `device_info.hcs` 另一侧 → HDF 框架找不到 deviceNode → .ko 加载了但 Bind/Init 不被调用。两侧必须一起生成
   - **L1 Linux 体系特殊情形**：部分外设产品侧已用 `linux_*_adapter`（走 Linux 内核 gpiolib/i2c-dev，非自研 HDF 驱动）。若自研驱动要替换它，需在 `device_info.hcs` 片段里把原 `linux_*_adapter` 的 deviceNode 改为本驱动 `moduleName`+`deviceMatchAttr`，或并存（见实测 device_info.hcs 的 device_gpio.device1 = linux_gpio_adapter 模式）
5. **BUILD.gn**：Read `references/hcs-config-templates.md` §L1 BUILD.gn
   - 使用 `hdf_driver("<periph>_driver")` 模板，声明 `moduleName` 与 .c 中 `HDF_INIT` 对应

### Step 4: 交叉验证

生成所有外设的驱动文件后，逐项检查：

| 检查项 | 方法 | 级别 |
|--------|------|:----:|
| **match_attr 配对** | 每个 `*_config.hcs` 的 `match_attr` 在 `device_info.hcs` 中有 `deviceMatchAttr` 精确对应，**字符串严格相等** | ERROR |
| **device_info.hcs 对端已生成** | L1 驱动生成时**必须一并输出 `device_info.hcs` 的 deviceNode 片段**（含 `moduleName`/`serviceName`/`deviceMatchAttr`），不能只写 `*_config.hcs` 一侧。只写一侧是实测翻车根因——HDF 框架找不到 deviceNode，驱动 .ko 加载了但 Bind/Init 不被调用 | ERROR |
| **HCS match_attr 运行时配对** | 上面只验两侧字符串相等还不够——必须确认产品 `device_info.hcs` 里**实际有**某个 `deviceNode` 的 `moduleName` == .c `HDF_INIT` 的 `moduleName`，且该 deviceNode 的 `deviceMatchAttr` == `*_config.hcs` 的 `match_attr`。否则 HCS 节点找不到对端 deviceNode，HDF 框架不调 Bind/Init，驱动 .ko 加载了但不工作（编译器查不出，是运行时框架行为）。若 device_info.hcs 当前在用别的驱动（如 `linux_gpio_adapter`），必须改 device_info.hcs 或并存配置，不能只写 `*_config.hcs` 一侧 | ERROR |
| **moduleName 一致** | .c 中 `HDF_INIT(g_xxxDriverEntry)` 的模块名 = `device_info.hcs` 某 deviceNode 的 `moduleName`（注意：BUILD.gn 的 `module_name` 是 .ko 文件名，与 HDF 注册名不同维度，**无需相等**） | ERROR |
| **IRQ +32 GIC 换算（L1 Linux/HDF）** | Linux/GIC 体系下 `OsalRegisterIrq(irq, …)` 的 `irq` 参数是 **Linux IRQ 号（virq）**，不是 DTS `interrupts` 三元组里的原始 SPI 号。GIC SPI 的 xlate 做 `hwirq = spi_param + 32`，所以 DTS `<0 23 4>`（SPI 23）→ 驱动 `irqStart=55`。**禁止把 DTS SPI 号原样填入 irqStart/irqNum**——会注册到错误中断（SPI 23+32=55 才是 GPIO0，23 是 PPI/SPI 7 区，根本不是 GPIO）。PPI（三元组首字段=1）换算不同（`hwirq = ppi_param + 16`），别套 +32。核对方法：查同族已验证芯片（如 hi3516dv300 `gpio_config.hcs` irqStart=48 对应 DTS SPI 16→16+32=48）佐证 +32 约定 | ERROR |
| **寄存器地址来源可追溯** | .c 中每个硬编码的寄存器地址在 chip_spec.json `fieldSources` 中有对应记录 | ERROR |
| **Method 结构体完整** | 所有 Method 函数指针已填充（不允许 NULL 函数指针） | ERROR |
| **L0/L1 框架不混用** | L0 不出现 HdfDriverEntry / OSAL / HCS；L1 不出现裸 CMSIS 寄存器操作 | ERROR |
| **BUILD.gn 依赖完整** | `deps` 中包含芯片 SDK 路径和框架头文件路径 | ERROR |
| **中断号/时钟无冲突** | 不同外设的 irqNum 不重复，时钟门控位不冲突 | WARNING |

### Step 5: 编译验证

告知用户运行编译命令。

#### L0 编译验证

```bash
# 在 OpenHarmony 仓库根目录
./build.sh --product <product_name>
```

#### L1 HCS 编译验证（先于全量编译）

```bash
# 编译 HCS 为 HCB 二进制
hc-gen -o /dev/null vendor/<dc>/<board>/hdf_config/uhdf/hdf.hcs
```

如果 hc-gen 报错，引导用户粘贴错误信息，常见错误：
- `match_attr` 拼写不一致 → 对照 device_info.hcs 逐字符检查
- template 实例缺少属性 → 对照 `references/hcs-config-templates.md` 补全必填属性

---

## ③ 外设 Method 接口速查

快速回忆用。详细结构体定义和参数说明见 `references/peripheral-api-specs.md`。

### L1 精简版 HDF — Method 结构体（核心层接口）

> ⚠️ 以下 Method 结构体（`GpioMethod` / `GpioCntlrAdd` / `*_core.h`）属于 **L1 HDF 核心层**，L1 驱动在 `Init` 中填充并调用 `GpioCntlrAdd` 注册。
> **L0 不使用 HDF**，驱动通过 `GpioOperations` + `GpioRegisterOps` 等组件化方式注册（详见 `references/driver-code-templates.md` §L0）。
> 每个 Method 结构体由一组函数指针组成，Agent 生成 L1 驱动时必须为**所有函数指针**提供实现（不允许 NULL）。完整定义见 `references/peripheral-api-specs.md`。

| 外设 | Method 结构体 | 必须实现的函数 | 注册函数 | 头文件 |
|------|-------------|--------------|----------|--------|
| GPIO | `GpioMethod` | `Request` / `Release` / `SetDir` / `GetDir` / `Write` / `Read` / `SetIrq` / `UnsetIrq` / `EnableIrq` / `DisableIrq` | `GpioCntlrAdd()` | `gpio_core.h` |
| I2C | `I2cMethod` | `Read` / `Write` / `SetConfig` / `GetConfig` | `I2cCntlrAdd()` | `i2c_core.h` |
| SPI | `SpiMethod` | `Transfer` / `SetCfg` / `GetCfg` | `SpiCntlrAdd()` | `spi_core.h` |
| UART | `UartHostMethod` | `Init` / `Deinit` / `Read` / `Write` / `GetBaud` / `SetBaud` / `GetAttribute` / `SetAttribute` / `SetTransMode` | `UartHostCreate()` | `uart_core.h` |
| ADC | `AdcMethod` | `Read` / `Start` / `Stop` | `AdcDeviceAdd()` | `adc_core.h` |
| PWM | `PwmMethod` | `SetConfig` / `GetConfig` / `Enable` / `Disable` | `PwmCntlrAdd()` | `pwm_core.h` |
| RTC | `RtcMethod` | `ReadTime` / `WriteTime` / `ReadAlarm` / `WriteAlarm` / `RegisterAlarmInterrupt` / `UnregisterAlarmInterrupt` / `AlarmInterruptEnable` | `RtcHostCreate()` | `rtc_core.h` |
| Watchdog | `WatchdogMethod` | `GetStatus` / `Start` / `Stop` / `SetTimeout` / `GetTimeout` / `Feed` | `WatchdogCntlrAdd()` | `watchdog_core.h` |

### L1 HdfDriverEntry 模板

```c
struct HdfDriverEntry g_<periph>DriverEntry = {
    .moduleVersion = 1,
    .moduleName    = "HDF_PLATFORM_<PERIPH>",  // 与 *_config.hcs / device_info.hcs 一致
    .Bind          = <Periph>Bind,               // 返回 HdfDeviceObject service，设置 IDeviceIoService.Dispatch
    .Init          = <Periph>Init,               // 注册 Method 接口（GpioCntlrAdd 等）
    .Release       = <Periph>Release,            // 释放资源
};
HDF_INIT(g_<periph>DriverEntry);
```

> Dispatch 不在 HdfDriverEntry 中，而是在 Bind 中通过 `IDeviceIoService.Dispatch` 设置（详见 `references/hdf-iot-driver-framework.md` §IDeviceIoService）。

### L1 HCS match_attr 配对速记

```
device_info.hcs                              *_config.hcs
─────────────────────────────────────       ─────────────────────────
deviceMatchAttr = "hdf_platform_gpio0"  ←→  match_attr = "hdf_platform_gpio0"
deviceMatchAttr = "hdf_platform_uart1"  ←→  match_attr = "hdf_platform_uart1"
deviceMatchAttr = "hdf_platform_i2c0"   ←→  match_attr = "hdf_platform_i2c0"
```

> 两侧拼写、大小写、下划线、数字后缀必须**逐字符相等**，否则驱动**静默加载失败**。注意：字符串相等只是第一步——还须确认 `device_info.hcs` 里确实有 deviceNode 用了这个 `moduleName`/`deviceMatchAttr`（运行时配对），否则 `*_config.hcs` 写了也无人绑定。

---

## 真实示例参考

完整的芯片驱动真实样本见 `examples/`：

- L0 样本：`examples/l0/hi3861/` — Hi3861 GPIO/UART 驱动（IoT API 适配层 + 厂商 HAL 封装）
- L1 样本：`examples/l1/stm32mp1/` — STM32MP1 GPIO 驱动（精简版 HDF + OSAL + HCS 绑定）

更多芯片驱动样本可参照 `references/field-patterns.md`（实测生成模式，含 BES2600W display/flash、Hi3861 HAL、Hi3516DV300 HDF 等案例模式）。

---

## Exceptions and Fallbacks（异常与兜底）

信息不足、SDK 缺失、集成失败时的处理规则（按场景）：

| 场景 | 处理 |
|------|------|
| **厂商 SDK 头文件拿不到**（调 SDK 函数路线无法建映射） | 标 `/* TODO: extract SDK API from <header> */` 并**退回寄存器直写路线**（L1 经 OSAL OsalIoRead32/Write32），禁止编造 SDK 函数名 |
| **厂商 SDK 无该外设 API**（如 Hi3516CV610 无 GPIO/UART 外设 API，仅 osal_*/ot_*） | 正确回退寄存器直写路线（PL061/PL011），不瞎编 hi_* 类调用（实测的正确行为） |
| **chip_spec.json 缺寄存器/中断字段** | 先联网查询（查到注明来源）；仍缺 → 追问用户或标 `/* TODO: extract from datasheet §<section> */`，禁止凭记忆填 |
| **IRQ +32 换算不确定** | 查同族已验证芯片 HCS 佐证（如 hi3516dv300 `gpio_config.hcs` irqStart=48 ↔ DTS SPI 16 → 16+32=48）；注意 PPI 是 +16 不是 +32，别套错 |
| **产品 device_info.hcs 在用 `linux_*_adapter`** | 改该 deviceNode 的 `moduleName`/`deviceMatchAttr` 为本驱动，或并存配置；**不能只写 `*_config.hcs` 一侧**（写了也无设备节点绑定） |
| **match_attr 无对端（编译过、hc-gen 过，但驱动不绑定）** | 这是运行时框架行为，编译器查不出——必须真产出 `device_info.hcs` 对端 deviceNode 片段（非仅文档说明"应改"），三段链（.c HDF_INIT moduleName ↔ deviceNode moduleName ↔ *_config.hcs match_attr/deviceMatchAttr）全部对齐后才算修复（实测：只文档化不改文件 = 未修复） |
| **hc-gen 报错** | 两大常见：match_attr 拼写不一致 → 对照 device_info.hcs 逐字符检查；template 实例缺属性 → 对照 `references/hcs-config-templates.md` 补全 |
| **编译环境不可用** | 给 hc-gen / build.sh 完整命令 + 常见报错路由，明确标注"待编译验证"，不谎称编译通过 |
| **文件已存在** | 检查内容正确性而非覆盖 |
