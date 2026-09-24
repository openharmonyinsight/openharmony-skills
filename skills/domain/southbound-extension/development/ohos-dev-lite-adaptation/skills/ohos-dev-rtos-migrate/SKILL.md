---
name: ohos-dev-rtos-migrate
description: OpenHarmony Lite RTOS迁移助手——分析 FreeRTOS/RT-Thread/Zephyr/Linux 驱动代码中的RTOS API调用，按 L0/L1 目标系统自动映射为 LiteOS-M 原生API 或 OSAL/HDF 接口，重构驱动架构并生成迁移方案。Use when driver code written for another RTOS/platform (FreeRTOS/RT-Thread/Zephyr/Linux/厂商 OSAL) must be ported to OpenHarmony Lite L0/L1; triggers include 迁移驱动代码、RTOS API 映射、xTaskCreate 换成 LiteOS 什么、FreeRTOS/RT-Thread 驱动移植、Linux 驱动转 HDF、厂商 OSAL 驱动迁到 L1、L1 HdfDriverEntry 改造、迁移后编译报 undeclared / parameter mismatch、ISR 里哪些 API 不能用。同义表达：驱动移植 / RTOS porting / API 转换 / 驱动框架升级。
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: rtos
  capability: migrate
  version: 0.1.0
  status: trial
---

# OpenHarmony Lite RTOS 驱动迁移

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 迁移任务 | "把这段 FreeRTOS 驱动迁到 OpenHarmony"、"厂商 OSAL 驱动改成 L1 HDF 平台驱动"、"Linux platform 驱动怎么转 HDF" |
| API 映射查询 | "xTaskCreate 对应 LiteOS-M 哪个 API"、"xSemaphoreCreateMutex 怎么换"、"这个 osal_* 在 HDF 里等价什么" |
| 迁移后症状 | "WATCHDOG_START undeclared"、"LOS_TaskCreate parameter mismatch"、"HDF_INIT redefined"、迁移代码编译不过 |
| 陷阱咨询 | "ISR 里能不能调这个 API"、"Tick 频率不一样延时怎么换"、"栈大小 word 还是字节"、"L0 能不能用 OSAL" |
| 链式调用 | ohos-dev-hal-skeleton-gen 生成骨架前的存量代码改造、适配工作流存量驱动复用 |
| 同义表达 | 驱动移植 / RTOS porting / API 转换 / 驱动框架升级 |

**不触发**（明确排除）：从零生成新驱动骨架（走 ohos-dev-hal-skeleton-gen）；只查 API 定义不做迁移（查 references/liteos-m-api-reference.md 类文档即可）；迁移后代码的规则审查（走 ohos-dev-driver-review）。

## Scope

本 SKILL 是 OpenHarmony Lite（L0 轻量系统 / L1 小型系统）芯片适配的**RTOS 迁移层**：接收 FreeRTOS/RT-Thread/Zephyr/Linux 等源平台的驱动代码，分析其中的 RTOS API 调用和驱动架构模式，逐 API 映射为 OpenHarmony 等效接口，重构驱动骨架，输出完整的迁移方案。

**本 SKILL 做 API 映射 + 架构重构指导，不修改原始代码文件**（迁移后的代码由用户在 Agent 辅助下写入新文件）。

### 生成文件清单

| 迁移阶段 | 产出物 | 说明 |
|---------|--------|------|
| API 分析 | 源 API 调用清单（Markdown 表格） | 从源码中提取所有 RTOS API 调用点 |
| 映射方案 | API 映射表 + 置信度评分 | 逐条 API 的源→目标映射，标注复杂度（🟢低/🟡中/🔴高） |
| 架构重构 | 驱动骨架重构方案 | L0: IoT 外设组件注册模式; L1: HdfDriverEntry + HCS 绑定 |
| 最终产出 | 迁移后的 .c/.h 源码 | 逐函数转换，保留原注释和业务逻辑 |

**输入**：源 RTOS 类型 + 源驱动源码（.c/.h）+ 目标系统级别（L0/L1）+ 目标芯片型号（可选）。缺失必填项先追问，不猜。
**输出**：源 API 调用清单 + API 映射表（含置信度与来源）+ 驱动骨架重构方案 + 迁移后 .c/.h 新文件 + HCS 配置（L1）+ 编译验证结果。
**不适用**：Linux 驱动直迁 L0（依赖 MMU+完整内核，几乎不可能——如实告知，建议 L1 或重写）；不修改原始代码文件；不做迁移后代码的规则审查（ohos-dev-driver-review 负责）。

## Initial Checks

收到迁移任务后，按以下顺序先做判断（各步结论决定迁移策略和后续路径）：

1. **输入四要素齐不齐**：源 RTOS 类型 / 源驱动源码 / 目标系统级别 / 目标芯片型号——缺必填项（前三）先追问用户，不默认假设。
2. **目标系统级别判定（L0/L1）**：决定 API 目标集——L0 = LiteOS-M 原生 `LOS_*`（禁 OSAL）；L1 = `Osal_*` + HDF 框架（禁直接 `LOS_*`）。用户显式指定优先。
3. **源平台类型判定 → 策略速判**：MCU 级 RTOS（FreeRTOS/RT-Thread）→ 策略 A/B；Zephyr（有 Device Model）→ 策略 D；Linux/厂商 OSAL → 策略 C；**Linux → L0 直接劝退**（见 L0 vs L1 迁移策略速判）。
4. **ISR 上下文 API 识别**：扫描源码中标量上下文调用（`*FromISR()` 系列 / 中断处理函数体内调用）——ISR 安全性是 ERROR 级陷阱检查项，提前标记。
5. **编译验证条件盘点**：目标平台交叉编译器可用？OH 仓 HDF 头路径可达？——决定 Step 7 真编译能否执行；不可达也要诚实声明并给降级方案。
6. **映射命中率预查**：对照 `references/api-mapping-tables.md` 粗扫一遍，无映射的 API 提前进入"先联网查、不凭记忆"流程（见 Prohibited Practices）。

## Prohibited Practices（禁止操作）

| 禁止 | 正确做法 |
|------|---------|
| **L0 迁移使用 OSAL 接口** | L0 = LiteOS-M 原生 API（`LOS_TaskCreate` / `LOS_SemCreate` / `LOS_MuxCreate`），不使用 OSAL |
| **L1 迁移使用 LiteOS-M 原生 API** | L1 = OSAL 封装（`OsalMutexInit` / `OsalSemInit`）+ HDF 框架 |
| 凭记忆映射 API（如"xTaskCreate 大概等于 LOS_TaskCreate"） | 逐条对照 `references/api-mapping-tables.md` 中的映射表，注意参数差异（栈大小单位、优先级方向、超时单位） |
| 不区分 Tick 频率差异直接替换延时函数 | FreeRTOS `configTICK_RATE_HZ` 默认 1000Hz，LiteOS-M `LOSCFG_BASE_CORE_TICK_PER_SECOND` 默认 100Hz，需换算 |
| 忽略 ISR 安全性差异 | FreeRTOS 有 `*FromISR()` 系列专用 API，LiteOS-M ISR 中只能使用 `LOS_SemPost` / `LOS_QueueWrite` 等部分 API |
| 不重构驱动架构只做 API 替换 | FreeRTOS 任务+队列模式 → L0 IoT 外设组件注册（操作函数表，如 GpioOperations）；Linux Platform 驱动 → L1 HDF（HdfDriverEntry） |
| 跳过架构重构的 HCS 配置生成（L1） | L1 迁移后驱动需要配套 `*_config.hcs` + `device_info.hcs` 绑定，match_attr 必须配对 |
| 只做结构自检不真编译就交付 | 结构自检抓不到 include 遗漏/传递包含链断裂，必须做 Step 7 真交叉编译验证 |
| 取不到的 API 映射直接标 TODO 留空 | **先上网查（用宿主联网检索能力，WebSearch 或等价物；坏用备选联网检索 CLI，如 opencode）**，查到填映射并注明来源；确实查不到才标 TODO 并注明来源/查询关键词，禁止凭记忆编造映射 |

---

## ① 文件路由表

根据用户意图，读取对应的参考文件。**每次只读一个**，不要一次性加载所有 reference。

### 本地参考文件

| 用户意图 | Agent 读取 | 预估行数 |
|---------|-----------|:-------:|
| 分析源平台 RTOS API 语义（FreeRTOS/RT-Thread/Zephyr/Linux） | `references/rtos-api-comparison.md` | ~480 |
| 查 LiteOS-M 原生 API 定义 + OSAL 接口（L0/L1） | `references/liteos-m-api-reference.md` | ~375 |
| 执行 API 逐条映射（FreeRTOS/RT-Thread/Zephyr/Linux → LiteOS-M/OSAL） | `references/api-mapping-tables.md` | ~150 |
| 参照已有迁移案例（FreeRTOS UART→L0、RT-Thread GPIO→L0、Linux I2C→L1） | `references/migration-cases.md` | ~540 |
| 排查迁移后的运行时问题（Tick/优先级/栈/ISR） | `references/migration-cases.md` §陷阱清单 | ~80 |

### 本地参考文件续（LiteOS-M API / 迁移案例 / 映射先例 / OSAL）

| 用户意图 | Agent 读取 | 预估行数 |
|---------|-----------|:-------:|
| 查 LiteOS-M 内核 API 最新定义（los_task.h / los_sem.h / los_queue.h 等） | `references/liteos-m-api-reference.md`（LiteOS-M 原生 API + OSAL 接口定义） | ~375 |
| 查已有芯片的迁移案例（BES2600W/ESP32/STM32 的 RTOS→OH 真实迁移） | `references/migration-cases.md`（FreeRTOS UART→L0、RT-Thread GPIO→L0、Linux I2C→L1 真实案例 + 陷阱清单） | ~540 |
| 查特定 API 的映射先例 | `references/api-mapping-tables.md`（80+ 条源→目标映射 + 参数转换 + 注意事项） | ~150 |
| 查 OSAL 接口最新定义（仅 L1 迁移需要） | `references/liteos-m-api-reference.md`（含 OSAL 接口章节）+ `references/rtos-api-comparison.md`（源平台 API 语义对比） | ~375 + ~480 |

### L0 vs L1 迁移策略速判

```
源平台
├── FreeRTOS / RT-Thread / uC-OS / VxWorks (MCU级RTOS)
│   → L0: LiteOS-M 原生 API 直接映射（同是 RTOS，差异最小）
│   → L1: 需要同时做 RTOS→RTOS API 映射 + 驱动框架升级（IoT组件→HDF）
│
├── Zephyr (有 Device Model)
│   → L0: 去除 Zephyr Device Model，回归 IoT 外设组件
│   → L1: Zephyr Device Model 概念可类比 HDF Device/HCS 绑定
│
└── Linux (字符设备/Platform驱动)
    → L0: ❌ 不推荐（Linux 驱动依赖 MMU+完整内核，直迁 MCU 几乎不可能）
    → L1: ✅ Linux Platform 驱动模式 → L1 HDF（HdfDriverEntry + OSAL）
```

---

## ② 工作流

### Step 1: 收集迁移输入

迁移开始前，必须收集以下信息（缺失项需追问用户）：

| 必填项 | 说明 | 示例 |
|-------|------|------|
| 源 RTOS 类型 | FreeRTOS / RT-Thread / Zephyr / Linux / uC-OS / VxWorks | FreeRTOS |
| 源驱动源码 | .c / .h 文件路径或内容 | `freertos_uart.c` |
| 目标系统级别 | L0 (LiteOS-M) / L1 (LiteOS-A + HDF) | L0 |
| 目标芯片型号（可选） | 用于查询芯片特有的 LiteOS-M 配置 | STM32F407 |

### Step 2: 分析源平台 API 依赖

Read `references/rtos-api-comparison.md`（按源 RTOS 类型选择对应章节），从用户提供的源码中提取所有 RTOS API 调用：

```
1. 扫描源码中所有 #include（识别依赖的 RTOS 头文件）
2. 提取所有 RTOS API 调用（任务/队列/信号量/互斥锁/定时器/内存/中断）
3. 标注每个 API 的上下文（任务上下文 vs ISR 上下文）← ISR 安全性关键
4. 输出：源 API 调用清单
   | 行号 | API 调用 | 类别 | 上下文 | 参数列表 |
   |:----:|---------|------|--------|---------|
   |  23  | xSemaphoreCreateMutex() | 互斥锁 | 任务 | 无参数 |
   |  45  | xTaskCreate()           | 任务   | 任务 | 5参数 |
   |  89  | xQueueSendFromISR()     | 队列   | ISR  | 3参数 |
```

### Step 3: 确定迁移策略

根据源 RTOS 类型 + 目标系统级别，确定迁移策略：

```
├── 策略A: RTOS→RTOS (FreeRTOS/RT-Thread → L0)
│   难度: 🟡 中
│   API映射: 直接（同是 RTOS，80+ 条已定义映射）
│   架构重构: 保留任务模型 + 操作函数表注册驱动（GpioOperations 等）
│   关键差异: Tick频率换算、ISR API限制、栈大小单位(word→字节)
│
├── 策略B: RTOS→HDF (FreeRTOS/RT-Thread → L1)
│   难度: 🔴 高
│   API映射: RTOS API → OSAL（OSAL 封装层）
│   架构重构: 任务模型 → HdfDriverEntry + Dispatch + HCS配置
│   额外工作: 生成 device_info.hcs + *_config.hcs
│
├── 策略C: Linux→HDF (Linux Platform驱动 → L1)
│   难度: 🔴 高
│   API映射: Linux内核API → OSAL + HDF API
│   架构重构: Platform驱动模型 → HdfDriverEntry
│   关键: 字符设备→Dispatch、file_operations→IoService命令码
│
└── 策略D: Zephyr→L0/L1
    难度: 🔴 高
    API映射: Zephyr Device Model → IoT外设组件(L0) / HDF(L1)
    架构重构: 去除Zephyr Devicetree绑定，重构为OH配置方式
```

### Step 4: 逐 API 映射 + 生成转换方案

Read `references/api-mapping-tables.md`（按源 RTOS + 目标系统选择对应映射表），逐条 API 生成转换方案：

```
对 Step 2 清单中的每条 API：
  1. 查 api-mapping-tables.md 找对应映射
     ├── 有直接映射（🟢低/🟡中）→ 生成替换代码 + 参数转换逻辑
     ├── 需间接实现（🔴高）  → 生成多API组合方案 + 注意事项
     └── 无映射              → 标注"需手动实现" + 建议替代思路
  
  2. 标注每条的置信度：
     ✅ 高置信度: 有已验证的映射 + 迁移案例
     ⚠️ 中置信度: 有映射但参数差异大，需人工验证
     ❌ 低置信度: 无映射，给出建议替代方案
  
  3. 输出：API 映射表
     | 源API | 目标API | 复杂度 | 参数转换 | 置信度 | 注意事项 |
```

**参数转换的关键差异**（Read `references/api-mapping-tables.md` 中每条映射的"注意事项"列）：

| 差异类型 | 示例 | 转换方法 |
|---------|------|---------|
| **栈大小单位** | FreeRTOS 传 word，LiteOS-M 传字节 | `stackByte = stackWord × 4` (32位) |
| **优先级方向** | FreeRTOS 数值越大优先级越高，部分RTOS相反 | 查 LiteOS-M 确认方向后调整 |
| **超时单位** | FreeRTOS 传 ticks，LiteOS-M 传 ticks（但频率可能不同） | `LOS_ticks = FreeRTOS_ticks × (LOS_TICK / configTICK_RATE_HZ)` |
| **ISR 安全性** | FreeRTOS `*FromISR()` 有独立参数（`pxHigherPriorityTaskWoken`） | L0 ISR 中仅用 `LOS_SemPost`/`LOS_QueueWrite`，唤醒逻辑由内核处理 |

### Step 5: 重构驱动架构

**API 替换只是表面工作，架构重构才是迁移的核心。** Read `references/migration-cases.md` 找到最匹配的迁移案例。

#### L0 架构重构（FreeRTOS/RT-Thread → IoT 外设组件）

```
迁移前 (FreeRTOS 模式)                    迁移后 (L0 IoT 外设模式)
─────────────────────────               ────────────────────────────
任务中直接操作 HAL 寄存器                组件化注册（直接函数调用，非 HDF Dispatch）
static void uart_task(...) {            int32_t uart_send(...) {
  ... HAL_UART_Transmit(...)              ... 寄存器操作 / 厂商HAL ...
}                                       }
                                        int32_t uart_recv(...) { ... }
xTaskCreate(uart_task, ...)             uart_driver_init() 组件注册入口
                                        （非 HdfDriverEntry，非 UartHostMethod）
全局变量 + 互斥锁保护                     LOS_MuxCreate 替代 FreeRTOS 互斥锁
uart_tx_mutex = xSemaphoreCreateMutex()  → LOS_MuxCreate(&uart_mux)
```

#### L1 架构重构（任何源平台 → HDF）

```
迁移前                                      迁移后 (L1 HDF 模式)
─────────────────────────                 ────────────────────────────
源平台驱动初始化函数                         HdfDriverEntry 入口
void uart_init(void) { ... }              struct HdfDriverEntry g_entry = {
                                            .Bind = UartBind,
                                            .Init = UartInit,  ← 原 init()
                                            .Release = UartRelease,
xTaskCreate() / kthread_create()          };
→ Init() 中创建 OsalThreadCreate / 线程   HDF_INIT(g_entry);
                                          配套 *_config.hcs + device_info.hcs
源平台的中断处理                             HDF 中断使用 OSAL 系列 API
request_irq() / hal_irq_register()       → OsalRegisterIrq()
```

### Step 6: 交叉验证 + 常见陷阱检查

生成迁移代码后，对照 `references/migration-cases.md` §陷阱清单逐条检查：

| 检查项 | 方法 | 级别 |
|--------|------|:----:|
| **ISR 中未使用 `*FromISR` 系列 API** | FreeRTOS `xQueueSendFromISR` → L0 ISR 中用 `LOS_QueueWrite`（LiteOS-M ISR 安全） | ERROR |
| **Tick 频率已换算** | `configTICK_RATE_HZ`(FreeRTOS) vs `LOSCFG_BASE_CORE_TICK_PER_SECOND`(LiteOS-M) | ERROR |
| **栈大小单位已转换** | FreeRTOS word → LiteOS-M 字节：`stackByte = stackWord × 4` | ERROR |
| **L0 未使用 OSAL / L1 未使用 LiteOS-M 原生 API** | 检查 `#include`：L0 含 `los_*.h`，L1 含 `osal_*.h` | ERROR |
| **L1 迁移有配套 HCS 配置** | `*_config.hcs` 的 `match_attr` = `device_info.hcs` 的 `deviceMatchAttr` | ERROR |
| **动态内存分配已替换** | `pvPortMalloc`→`LOS_MemAlloc`/`malloc`，`vPortFree`→`LOS_MemFree`/`free` | WARNING |
| **回调签名已调整** | FreeRTOS `void (*)(void*)` → LiteOS-M `void (*)(UINT32)` 等差异 | WARNING |

### Step 7: 真编译验证（迁移代码必做，不只结构自检）

**结构自检（只看代码结构、不真编译）有典型盲区**：符号定义在另一头文件、传递包含链断裂、宏定义遗漏等只有编译器符号解析能抓到。迁移产出代码必须做一次真交叉编译验证，不能只靠 Step 6 的结构自检交付。

#### 真编译验证方法

1. **用目标平台交叉编译器**（L1 用 `arm-linux-gnueabi-gcc` 或产品指定工具链；L0 用 `riscv32-unknown-elf-gcc` 等），**单文件 `-c` 编译**迁移后的 `.c`，至少做 `-fsyntax-only` 或 `-c`：
   ```bash
   # L1 示例（OH 仓内工具链 + HDF 头 + liteos_a 内核头）
   GCC=$OH/prebuilts/gcc/linux-x86/arm/gcc-linaro-7.5.0-arm-linux-gnueabi/bin/arm-linux-gnueabi-gcc
   HDF=$OH/drivers/hdf_core; LA=$OH/kernel/liteos_a
   INC="-I$HDF/interfaces/inner_api/... -I$HDF/framework/include/... -I$LA/kernel/include ..."
   $GCC -c $INC -D__LITEOS__ -Wall -Wextra \
       -Werror=incompatible-pointer-types -Werror=implicit-function-declaration \
       <periph>_driver.c -o <periph>_driver.o
   ```
2. **include 路径复原**：迁移代码 `#include` 的头文件（`hdf_device_desc.h`/`osal_*.h`/`<periph>_core.h`/`<periph>_if.h` 等）全部在 `drivers/hdf_core` 下找；传递依赖链（`osal_atomic_def.h`→`<los_atomic.h>`、`osal_io.h`→`<linux/io.h>` 等）递归补齐。对 LiteOS-A 内核头递归依赖可用最小 stub 隔离迁移代码自身错误（不影响对 `Osal*`/`Hdf*` 公共接口调用正确性的判定）。
3. **编译失败必须修复后重编**，常见遗漏：
   - `'WATCHDOG_START' undeclared` → 遗漏 `#include "<periph>_if.h"`（枚举常量定义在 `_if.h`，`_core.h` 不传递包含）
   - `parameter mismatch` → API 版本差异，对照 `references/liteos-m-api-reference.md` 检查参数
   - `HDF_INIT redefined` → 重复定义 HdfDriverEntry 入口
4. **严格警告模式**（`-Wconversion -Wsign-conversion -Wshadow -Wunused`）建议跑一遍，int→uint32_t 等隐式转换警告虽非致命但应记录。

> **链接期未覆盖（诚实声明）**：单文件 `-c` 编译不解析 `OsalSpinInit`/`WatchdogCntlrAdd` 等符号的实际地址（需完整 GN 构建链接 `.so`），但符号原型已由真实 HDF 头校验，调用参数类型/个数正确。完整链接验证留给 Step 8 全量编译。

### Step 8: 全量编译验证

告知用户运行编译命令验证迁移后的代码（在 OpenHarmony 仓库根目录）：

```bash
./build.sh --product <product_name>
```

常见迁移后编译错误及对应修复：
- `undefined reference to LOS_TaskCreate` → BUILD.gn 缺少 `//kernel/liteos_m` 依赖
- `LOS_SemCreate parameter mismatch` → LiteOS-M API 版本差异，对照 `references/liteos-m-api-reference.md` 检查参数
- `HDF_INIT redefined` → 检查是否重复定义了 HdfDriverEntry 入口

---

## ③ 高频 API 映射速查

快速回忆用。完整 80+ 条映射及参数转换细节见 `references/api-mapping-tables.md`。

### FreeRTOS → LiteOS-M（L0 最常用，20 条核心映射）

| FreeRTOS API | LiteOS-M API | 复杂度 | 关键注意事项 |
|-------------|-------------|:---:|------|
| `xTaskCreate()` | `LOS_TaskCreate()` | 🟡 | **栈大小 word→字节**（×4）；优先级方向可能相反 |
| `vTaskDelete()` | `LOS_TaskDelete()` | 🟢 | 语义等价 |
| `vTaskDelay(ticks)` | `LOS_TaskDelay(ticks)` | 🟢 | **Tick 频率可能不同**（FreeRTOS 默认 1000Hz, LiteOS-M 默认 100Hz） |
| `vTaskDelayUntil()` | ❌ 无直接对应 | 🔴 | 需用 `LOS_SwtmrCreate()` 或手动计算绝对时间 |
| `xSemaphoreCreateMutex()` | `LOS_MuxCreate()` | 🟢 | 语义等价 |
| `xSemaphoreTake(mutex, wait)` | `LOS_MuxPend(mux, timeout)` | 🟡 | 超时转换（确认 Tick 频率一致） |
| `xSemaphoreGive(mutex)` | `LOS_MuxPost()` | 🟢 | 语义等价 |
| `xSemaphoreCreateBinary()` | `LOS_SemCreate(0, &sem)` | 🟢 | 初始值 0 |
| `xSemaphoreCreateCounting(max, init)` | `LOS_SemCreate(init, &sem)` | 🟡 | LiteOS-M 信号量不限制最大值 |
| `xSemaphoreTakeFromISR()` | ❌ ISR 不用信号量 | 🔴 | 改用原子变量 + 任务唤醒模式 |
| `xQueueCreate()` | `LOS_QueueCreate()` | 🟡 | **LiteOS-M 原生支持队列**；参数格式不同 |
| `xQueueSend()` / `xQueueReceive()` | `LOS_QueueWrite()` / `LOS_QueueRead()` | 🟡 | 参数重组，功能等价 |
| `xQueueSendFromISR()` | `LOS_QueueWrite()` | 🟡 | ISR 中可用（LiteOS-M 无特殊 ISR API） |
| `xTimerCreate()` | `LOS_SwtmrCreate()` | 🟡 | 回调签名不同（`void(*)(void*)` → `void(*)(UINT32)`） |
| `pvPortMalloc()` | `LOS_MemAlloc()` 或 `malloc()` | 🟢 | 取决于 `LOSCFG_KERNEL_MEM_BESTFIT` 配置 |
| `vPortFree()` | `LOS_MemFree()` 或 `free()` | 🟢 | 配对使用 |
| `taskENTER_CRITICAL()` | `LOS_IntLock()` | 🟡 | 语义相似（关中断） |
| `taskEXIT_CRITICAL()` | `LOS_IntRestore()` | 🟡 | 配对使用 |
| `xTaskNotifyGive()` | `LOS_SemPost()` | 🟡 | 任务通知 → 信号量近似替代 |
| `eTaskGetState()` | ❌ 无直接对应 | 🔴 | 需自行维护任务状态跟踪 |

### RT-Thread → LiteOS-M（L0 重要，10 条核心映射）

| RT-Thread API | LiteOS-M API | 复杂度 | 关键注意事项 |
|-------------|-------------|:---:|------|
| `rt_thread_create()` | `LOS_TaskCreate()` | 🟡 | 参数重组（栈/优先级/时间片） |
| `rt_sem_create()` | `LOS_SemCreate()` | 🟢 | 参数接近 |
| `rt_mutex_create()` | `LOS_MuxCreate()` | 🟢 | 语义等价 |
| `rt_mq_create()` | `LOS_QueueCreate()` | 🟡 | 消息队列模型不同（RT-Thread 支持紧急消息） |
| `rt_timer_create()` | `LOS_SwtmrCreate()` | 🟡 | 回调参数差异 |
| `rt_device_register()` | IoT 外设组件注册 | 🔴 | **架构级差异**：RT-Thread 设备框架 → OH IoT 外设组件 |
| `rt_device_open()` / `rt_device_read()` | 操作函数表 `Read` / `Write` | 🔴 | 需重构为操作函数表模式（L0: GpioOperations 等，非 GpioMethod） |
| `rt_malloc()` | `LOS_MemAlloc()` 或 `malloc()` | 🟢 | 直接替换 |
| `rt_enter_critical()` | `LOS_IntLock()` | 🟡 | 关中断 |
| `rt_hw_interrupt_install()` | `LOS_HwiCreate()` | 🟡 | 中断注册机制不同 |

> 完整映射表（含 Zephyr→OSAL、Linux→HDF）见 `references/api-mapping-tables.md`。

---

## Exceptions and Fallbacks（异常与兜底）

映射查不到、编译失败、目标不可行时的处理规则（按场景）：

| 场景 | 处理 |
|------|------|
| **映射表无该 API** | 先上网查（用宿主联网检索能力，WebSearch 或等价物；坏用备选联网检索 CLI，如 opencode），查到填映射并注明来源；确实查不到才标 TODO + 注明查询关键词，**禁止凭记忆编造映射**（见 Prohibited Practices） |
| **无直接映射的 API**（如 `vTaskDelayUntil` / `osal_kthread_should_stop` / 带条件回调的超时等待） | 给明确组合替代方案（`LOS_SwtmrCreate` / 自管 `volatile bool` + `OsalSemPost` 唤醒 / `OsalSemWait` + 循环顶重查条件），标 ⚠️ 中置信度 + 注明来源与替代思路，建议人工确认——**不留空 TODO，也不硬凑一个假映射** |
| **Linux 驱动要迁 L0** | 如实告知"依赖 MMU + 完整内核，直迁 MCU 几乎不可能"，建议改 L1（策略 C）或按 IoT 外设组件重写，不硬做映射 |
| **Step 7 真编译失败** | 按常见三类修复后重编：`'XXX' undeclared`（如 `WATCHDOG_START`）→ 补对应 `<periph>_if.h`（枚举常量在 `_if.h`，`_core.h` 不传递包含）；`parameter mismatch` → 对照 `references/liteos-m-api-reference.md` 检查参数；`HDF_INIT redefined` → 去重 HdfDriverEntry 入口。**修不过不交付** |
| **无交叉编译器 / OH 仓不可达** | 至少用可得头做 `-fsyntax-only` 语法校验，并诚实声明"未做真交叉编译，符号原型未经真实 HDF 头校验"，完整验证留给 Step 8 全量编译——**不冒充已真编译** |
| **Tick 频率 / 优先级方向 / 栈单位不确定** | 不默认假设两边一致——换算公式给出但标注"需确认目标配置（`LOSCFG_BASE_CORE_TICK_PER_SECOND` 等）"，列入人工确认项 |
| **真编译能跑但 Step 8 全量编译报链接错**（`undefined reference to LOS_*`） | 检查 BUILD.gn 是否缺 `//kernel/liteos_m`（L0）或 HDF 依赖（L1）；单文件 `-c` 不解析符号地址属正常（见 Step 7 链接期诚实声明），链接验证本就留给 Step 8 |
