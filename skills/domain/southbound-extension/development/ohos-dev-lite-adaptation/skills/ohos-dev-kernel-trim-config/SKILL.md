---
name: ohos-dev-kernel-trim-config
description: OpenHarmony Lite 内核裁剪配置器——根据芯片 RAM/Flash 资源推荐 LiteOS-M / LiteOS-A 组件裁剪方案，解析 Kconfig 与旧式 LOSCFG 宏的 #error 守卫依赖，生成无冲突的 .config 或 target_config.h 片段。Use when the kernel footprint must fit the chip's RAM/Flash budget; triggers include 内核裁剪、省 RAM/Flash、组件裁剪、LOSCFG 宏取舍、target_config.h 裁剪、Kconfig depends on/select、#error 守卫不触发、实例上限下调（TSK/SEM/MUX/QUEUE/SWTMR LIMIT）、RAM 分级方案、make menuconfig 能不能用、注释掉宏反而编译不过、裁剪后编译报 undefined reference / section overflowed。
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: kernel
  capability: trim-config
  version: 0.1.0
  status: trial
---

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 完整裁剪任务 | "帮我看这块板子要裁哪些内核组件"、"RAM 不够了出个裁剪方案"、"LiteOS-M 极致裁剪" |
| 单点查询 | "这个宏能不能关"、"关了 CPUP 会不会编译错"、"SWTMR 和 QUEUE 什么依赖"、"LOSCFG_XXX_LIMIT 能下调到多少" |
| 症状词（隐性需求） | "裁剪后编译报 #error"、"注释掉宏反而编译不过"、"LOS_SemCreate 返回 LOS_ERRNO_SEM_ALL_BUSY"、"section .text overflowed"、"undefined reference to LOS_SemCreate"、"关了宏怎么 ROM 一点没省" |
| 下游 skill 链式调用 | ohos-dev-board-config-gen 生成 target_config.h 骨架后，组件级 LOSCFG 裁剪由本 skill 负责 |
| 同义表达 | 内核瘦身 / 组件裁剪 / 配置裁剪 / footprint 优化 |

**不触发**（明确排除）：target_config.h 中设备硬件字段生成（内存地址/外设基地址 → ohos-dev-board-config-gen）；构建装配与编译入口（→ ohos-dev-build-config）；链接段溢出的在线诊断（→ ohos-issue-lite-diagnose，本 skill 只做事前裁剪预防）。

## Scope

本 SKILL 是 OpenHarmony Lite（L0 轻量系统 / L1 小型系统）芯片适配的**内核裁剪层**：根据芯片 RAM/Flash 资源和产品功能需求，从 LiteOS-M（50+ Kconfig 选项）或 LiteOS-A（100+ Kconfig 选项）中选出最优组件组合，解析依赖关系（depends on / select / imply），生成不冲突的内核配置。

**本 SKILL 做组件级裁剪决策 + 依赖完整性保证，不修改内核源码**（仅生成 .config / target_config.h / Kconfig 片段）。

### 生成文件清单

| 内核类型 | 本 SKILL 生成的配置 | 说明 |
|---------|-------------------|------|
| **LiteOS-M** (L0) | `target_config.h` 裁剪宏定义 + Kconfig `.config` 片段 | GN+Kconfig 方式，**不使用 make menuconfig** |
| **LiteOS-A** (L1) | Kconfig `.config` 片段 | GN+Kconfig 方式 |

> `target_config.h` 中与芯片硬件相关的字段（如内存地址、外设基地址）由 ohos-dev-board-config-gen 生成，本 SKILL 只生成内核组件裁剪相关的宏（`LOSCFG_*`）。

**输入**：芯片型号 + RAM/Flash 大小 + CPU 架构 + 产品功能需求 + 认证需求（必需）；现有 `target_config.h`（改造场景，可选）。
**输出**：裁剪方案（trim-plan：逐项决策表 + 资源节省汇总 + RAM 预算检查 + 交叉验证）+ 可替换的 `target_config.h` 片段 / `.config` 片段。

## Initial Checks

收到任务后，按以下顺序先做判断（各步结论决定后续路径）：

1. **输入形态判断**：已有 `target_config.h` 改造（先读现状摘要，逐宏决策）vs 从零按芯片资源推荐（走 RAM 分级方案）——两者 Step 3 起点不同。
2. **配置体系判定**（最易判错，判错则依赖验证全错）：OH 上游 Kconfig（`KERNEL_*` 命名空间，`code/kernel/liteos_m/Kconfig`）vs 厂商 SDK 旧式 `LOSCFG_*` 宏 + 源码 `#ifdef` 守卫 + `los_config.h` 的 `#error`（如 Hi3861 SDK `Huawei_LiteOS/` 目录下无任何 Kconfig 文件）。实测翻车根因：执行者拿 Kconfig 规则自报"依赖完整"，与实际旧式宏体系不是同一套。
3. **内核类型判定**：按 RAM 映射规则（Step 2）确定 LiteOS-M / LiteOS-A。
4. **RAM 预算判定**：总 SRAM 扣厂商组件占用（如 WiFi/BLE 协议栈 100~150KB）得内核可用预算，再归入分级——不拿总 SRAM 直接分级。
5. **认证需求确认**：L1 安全认证要求必选组件保留（`LOSCFG_SECURITY_*`）。
6. **编译环境可用性**：决定 Step 7 真跑编译还是静态核实（守卫 grep + RAM 预算）+ 标"待实跑"。

## Prohibited Practices（内核裁剪禁止操作）

| 禁止 | 正确做法 |
|------|---------|
| **关闭最小功能集组件（任务管理/调度器/内存管理/中断/异常管理/系统时钟）** | 这 6 个组件不可裁剪——它们是内核运行的最小依赖，关闭后系统无法启动 |
| 忽略 `select` 级联效应直接关组件 | 关闭 A 前检查是否有其他组件 `select A`——被 select 的组件无法关闭 |
| 凭经验估算组件资源占用 | 对照 `references/trimming-recipes.md` §1-2 的组件资源占用表，不同架构（ARM Cortex-M0/M3/M4/M7, RISC-V）数值不同 |
| 不区分 LiteOS-M 和 LiteOS-A 的 Kconfig 体系 | LiteOS-M 用 `LOSCFG_*` 宏 + GN 集成；LiteOS-A 有额外的 MMU/Virtual Memory 必选组件 |
| 为 L0 MCU 启用完整 lwIP + FAT + HDF | 128KB RAM 的设备无法同时承载多个扩展组件，按 RAM 分级方案裁剪 |
| 忽略产品兼容性认证的必选组件 | 认证要求某些组件必须保留（如 `LOSCFG_SECURITY_CAPABILITY` L1 安全认证必选） |
| 取不到的组件资源占用/依赖关系直接标 TODO 留空 | **先上网查（用宿主联网检索能力，WebSearch 或等价物；坏用备选联网检索 CLI，如 opencode）**，查到填值并注明来源；确实查不到才标 TODO 并注明来源/查询关键词，禁止凭记忆编造或留空 |

---

## ① 文件路由表

根据用户意图，读取对应的参考文件。**每次只读一个**，不要一次性加载所有 reference。

| 用户意图 | Agent 读取 | 预估行数 |
|---------|-----------|:-------:|
| 了解 LiteOS-M/A 组件体系（每个组件的功能/ROM/RAM/Kconfig宏） | `references/liteos-ma-components.md` | ~180 |
| 理解 Kconfig 依赖规则（depends on / select / imply / choice） | `references/kconfig-reference.md` | ~160 |
| 查组件资源占用数据 + 分级裁剪方案（64K/128K/256K/512K RAM） | `references/trimming-recipes.md` §1-3 | ~130 |
| 查主流 MCU/MPU 芯片规格与推荐内核 | `references/trimming-recipes.md` §4 | ~80 |
| 查芯片→内核→配置映射规则（IF RAM < 128KB...） | `references/trimming-recipes.md` §4.3 | ~30 |
| 参照已有裁剪案例（STM32F407 极致裁剪 / Hi3516DV300 功能裁剪 / ESP32-C3 RISC-V） | `references/trimming-recipes.md` §5 | ~120 |
| 查常见裁剪错误与规避方法 | `references/trimming-recipes.md` §6 | ~50 |
| 查 Kconfig 语法细节（bool/int/hex/string/default/range） | `references/kconfig-reference.md` §1 | ~60 |
| 查看真实的 target_config.h / los_config.h / config.json（了解 LOSCFG_* 宏和子系统裁剪的标准格式） | `examples/l0/hi3861/`（L0 宏级裁剪）+ `examples/l1/hi3516dv300/`（L1 子系统级裁剪） | ~100/套 |

---

## ② 工作流

### Step 1: 收集芯片资源与功能需求

生成裁剪方案前，必须收集以下信息（缺失项需追问用户）：

| 必填项 | 说明 | 示例 |
|-------|------|------|
| 芯片型号 | 用于查 trimming-recipes.md §4 的芯片规格表 | STM32F407ZG |
| RAM 大小 | 决定内核类型和裁剪级别 | 192 KB |
| Flash 大小 | 影响文件系统和网络协议栈选择 | 1 MB |
| CPU 架构 | 影响组件资源占用估算（ARM vs RISC-V） | Cortex-M4F |
| 产品功能需求 | 需要哪些子系统（MQTT/OTA/文件系统/WiFi/BLE/显示等） | MQTT + OTA + LittleFS |
| 是否需认证 | 产品兼容性认证要求额外的必选组件 | 否 |

### Step 2: 确定内核类型

Read `references/trimming-recipes.md` §4.3（芯片→内核→配置映射规则）：

```
IF RAM < 128 KB:
    → ❌ 不支持 OpenHarmony（低于最低要求）
    
ELIF RAM >= 128 KB AND RAM < 1 MB:
    → 内核 = LiteOS-M, 系统 = L0
    → 按 RAM 分级: 128KB / 256KB / 512KB 方案
    
ELIF RAM >= 1 MB AND RAM < 128 MB:
    IF CPU == Cortex-A:
        → 内核 = LiteOS-A, 系统 = L1
    ELSE:
        → 内核 = LiteOS-M（高配 MCU 模式）
        
ELIF RAM >= 128 MB:
    → ⚠️ 超出本工具范围（标准系统 L2/Linux）
```

### Step 3: 查组件资源占用 + 匹配 RAM 分级方案

Read `references/liteos-ma-components.md`（组件清单）和 `references/trimming-recipes.md` §1-3（资源占用 + 分级方案）。

**LiteOS-M RAM 分级速判**：

| RAM 级别 | 可启用组件范围 | 裁剪策略 |
|---------|--------------|---------|
| **128~256 KB** | 最小功能集 + 信号量 + 互斥锁 + 队列 | 可选 LittleFS 或精简 lwIP（二选一），禁用调试/HDF |
| **256~512 KB** | 核心 + 全 IPC + FS 或 NET（二选一） | 可启用一个扩展组件组 |
| **512 KB~1 MB** | 核心 + 全 IPC + FS + NET（精简） | 接近完整功能集 |

**LiteOS-A（L1）**：trimming-recipes.md 未提供独立的 RAM 分级表。L1 裁剪从 LiteOS-A 组件资源占用表（trimming-recipes.md §2）出发，按 RAM 约束逐组件决策——LiteOS-A 最小核心（进程/线程/调度/MMU/中断/时钟）合计约 32KB ROM，剩余空间按功能需求优先级分配 FS → NET → HDF → ELF/Shell。

### Step 4: 逐功能需求匹配组件 + 依赖解析

Read `references/kconfig-reference.md`（依赖规则），按功能需求逐项反查所需组件：

```
功能需求              必需组件（Kconfig 宏）              级联依赖
─────────            ────────────────────               ──────
MQTT 上报            LOSCFG_NET_LWIP (lwIP)             → 需要 LOSCFG_BASE_IPC_QUEUE（队列）
                     LOSCFG_NET_SOCKETS (Socket API)    → 需要 lwIP

OTA 升级             LOSCFG_FS_LITTLEFS (LittleFS)      → 需要 LOSCFG_FS_VFS（VFS 层）
                                                         → 需要 Flash 驱动

WiFi 连接            LOSCFG_NET_LWIP (lwIP)             → 同 MQTT
                     (WiFi 驱动由 vendor SDK 提供)

多任务并发            LOSCFG_BASE_IPC_SEM (信号量)        → 最小功能集已含任务管理
                     LOSCFG_BASE_IPC_MUX (互斥锁)

Cortex-M 架构        LOSCFG_CMSIS_RTOS2 (CMSIS-RTOS2)   → 可选用以兼容 CMSIS 生态
```

**依赖解析规则**：

```
1. MUST_ENABLE:  被其他已选组件 "select" 的组件 → 强制开启，不可关闭
2. FORCE_SELECT: 开启组件 A 时自动 "select" 组件 B → 自动加入配置
3. SUGGEST:      被 "imply" 的组件 → 建议开启但可关闭
4. CONFLICT:     两个组件互斥（choice 结构）→ 只能选一个
```

### Step 5: 生成配置

对每个 Kconfig 选项，按以下优先级决策：

```
对每个组件 C：
  1. C 属于最小功能集？         → y（不可裁剪）
  2. C 被其他已选组件 select？   → y（级联强制）
  3. C 满足功能需求？           → y（业务需要）
  4. C 的内存占用超出芯片能力？  → n（资源约束跳过）
  5. 其他                       → n（默认关闭）
```

**LiteOS-M 输出**：`target_config.h` 片段（`#define LOSCFG_*` 宏）+ Kconfig `.config` 片段
**LiteOS-A 输出**：Kconfig `.config` 片段

> **关闭宏的方式**：显式 `#define LOSCFG_XXX NO`（保留定义、值改 NO），**不能注释掉 `#define`**——注释掉后符号未定义，`#if` 里的未定义标识符按 0 求值（C99 §6.10.1，标准工具链**不报编译错**）：`#if (LOSCFG_XXX == 1)` 静默判假，`#if (LOSCFG_XXX == NO)` 更会反向判真，配置错误被掩盖；宏若被普通 C 表达式引用才真正报 undeclared identifier。显式 `NO`（=0）语义干净、意图明确（compile-verification 实测建议）。

### Step 6: 交叉验证

对照 `references/trimming-recipes.md` §6（常见裁剪错误）逐条检查：

| 检查项 | 方法 | 级别 |
|--------|------|:----:|
| **最小功能集完整性** | 任务管理/调度器/内存管理/中断管理/异常管理/系统时钟 = y | ERROR |
| **无依赖断裂（Kconfig 体系）** | 每个开启组件的 `depends on` 条件均满足 | ERROR |
| **无 select 冲突（Kconfig 体系）** | 未被任何组件 select 的组件允许关闭；被 select 的组件必须开启 | ERROR |
| **#error 守卫检查（旧式 LOSCFG 宏体系）** | **不止看 Kconfig select/depends**——Hi3861 SDK 等用旧式 `LOSCFG_*` 宏，依赖关系由源码 `#ifdef` 守卫 + `los_config.h` 里的 `#error` 表达。必须 Grep `los_config.h`/`los_task.h` 等核心头的 `#error` 守卫，确认关闭组合不触发。且**以实读源码的 #error 清单为准**，不凭文档/记忆引用守卫文本（compile-verification 实测：文档所述 `#error "cpup need support task monitor"` 在当前 los_config.h 中不存在，真实依赖方向相反——CPUP 包在 TSK_MONITOR==YES 守卫内） | ERROR |
| **choice 互斥满足** | 内存管理算法（bestfit/membox）至少选一个，且互斥项只有一个 y | ERROR |
| **不为无效宏报节省** | 宏关闭若 boot asm/底层**无条件启用**则 ROM/RAM 节省为**虚报**，必须注明并从合计扣除。典型：Hi3861 `LOSCFG_BASE_CORE_PMP` 宏在 C 代码里无 `#ifdef` 引用，但 boot 汇编（`riscv_init_*.S` 的 `pmp_init:` 块）无条件写 PMP CSR——关宏不省 ROM（无 C 实现）、不省 RAM（PMP 区是硬件 CSR）、不改运行时 PMP 行为。Track/FPB 同类：全代码树无实现无调用，关闭实际省 0。这类宏关闭须标注"无实际收益"，**禁止计入 §ROM/RAM 节省合计** | ERROR |
| **RAM 预算不超标** | 总 ROM = Σ(开启组件 ROM) < Flash 容量；总 RAM = Σ(开启组件 RAM) + 应用需求 < RAM 容量 | ERROR |
| **认证必选组件保留** | L1 安全认证: `LOSCFG_SECURITY_CAPABILITY` / `LOSCFG_SECURITY_DAC` = y | WARNING |
| **LiteOS-M 不使用 make menuconfig** | 配置通过 GN+Kconfig 集成，不执行 `make menuconfig` | WARNING |

### Step 7: 编译验证

```bash
# 在 OpenHarmony 仓库根目录
./build.sh --product <product_name>
```

常见裁剪导致的编译错误：
- `undefined reference to LOS_SemCreate` → 信号量组件被关闭但其他组件引用了它 → 检查 Kconfig `select` 链
- `section .text overflowed` → ROM 预算超标 → 关闭非必要扩展组件
- `LOSCFG_XXX undeclared` → Kconfig 未生成对应的 `#define` → 检查 GN 集成是否正确

---

## ③ 内核裁剪速查

快速回忆用。详细组件数据和依赖规则见 references/。

### LiteOS-M 最小功能集（不可裁剪）

| 组件 | 功能 | 预估ROM | 预估RAM | 关掉会怎样 |
|------|------|:------:|:------:|----------|
| 任务管理(Task) | 任务创建/删除/挂起/恢复、TCB管理 | ~2.5 KB | ~0.5 KB + N×400B | ❌ 无法创建任何任务 |
| 调度器(Sched) | 优先级位图、上下文切换、时间片 | ~1.5 KB | ~200 B | ❌ 系统无法调度 |
| 内存管理(Mem) | 动态内存分配(bestfit/buddy/membox) | ~1.5 KB | 堆大小可配 | ❌ 无动态内存 |
| 中断管理(Int) | 中断注册/注销、嵌套处理 | ~1.0 KB | ~100 B | ❌ 外设无法响应 |
| 异常管理(Fault) | HardFault/SVC/NMI 处理 | ~0.8 KB | ~200 B | ❌ 异常后无法定位 |
| 系统时钟(Tick) | SysTick 配置、tick 计数 | ~0.5 KB | ~50 B | ❌ 延时/超时不可用 |
| **最小功能集合计** | | **~7.8 KB** | **~1.1 KB+** | |

### LiteOS-M 常用可选组件

| 组件 | Kconfig 宏 | ROM | RAM | 何时开启 |
|------|-----------|:---:|:---:|---------|
| 信号量 | `LOSCFG_BASE_IPC_SEM` | ~0.8 KB | 32B×N | 任务间同步（几乎所有应用都需要） |
| 互斥锁 | `LOSCFG_BASE_IPC_MUX` | ~1.0 KB | 48B×N | 共享资源保护（几乎所有应用都需要） |
| 消息队列 | `LOSCFG_BASE_IPC_QUEUE` | ~1.2 KB | 64B×N+缓冲 | 任务间数据传递 |
| 软件定时器 | `LOSCFG_BASE_CORE_SWTMR` | ~1.0 KB | 40B×N | 需要周期性任务 |
| LittleFS | `LOSCFG_FS_LITTLEFS` | ~6.0 KB | ~2.0 KB | OTA / 数据存储（推荐——Flash 友好） |
| lwIP | `LOSCFG_NET_LWIP` | ~40.0 KB | ~30.0 KB | MQTT / HTTP / WiFi（⚠️ RAM 大户） |
| CMSIS-RTOS2 | `LOSCFG_CMSIS_RTOS2` | ~3.0 KB | ~0.5 KB | 需要 CMSIS 生态兼容（Cortex-M 推荐） |
| HDF 框架 | `LOSCFG_DRIVERS_HDF` | ~10.0 KB | ~4.0 KB | L1 必选 / L0 通常不需要 |

### LiteOS-M RAM 分级裁剪方案

| RAM 级别 | 推荐开启 | 推荐关闭 | 典型芯片 |
|---------|---------|---------|---------|
| **128~256 KB** | 最小集 + SEM + MUX + QUEUE | FS 和 NET 二选一；关 CMSIS/HDF/调试 | Hi3861(352K), STM32F407(192K), XR806(288K) |
| **256~512 KB** | 最小集 + 全 IPC + FS 或 NET | 关调试/CPUP；HDF按需 | BES2600W(512K), ESP32-C3(400K) |
| **512 KB~1 MB** | 最小集 + 全 IPC + FS + NET | 接近完整集 | STM32H743(1M), ESP32-S3(512K+PSRAM) |

> ⚠️ **RAM 级别含义**：上表"RAM 级别"指**内核可用的 RAM 预算**（扣除 WiFi/BLE 协议栈等厂商组件占用后的剩余空间），括号内为芯片**总 SRAM**。例如 Hi3861 总 SRAM 352KB，但 WiFi 协议栈占用约 100~150KB，内核可用约 200~250KB，归入 128~256KB 级别。详见 `references/trimming-recipes.md` §3。

### Kconfig 依赖陷阱速记

| 关键字 | 含义 | Agent 操作 |
|--------|------|-----------|
| `depends on A` | 只有 A=y 时本选项才可见 | 开启前检查前置条件是否满足 |
| `select B` | 本选项=y 时强制 B=y | 开启后自动将 B 加入配置（级联） |
| `imply C` | 本选项=y 时建议 C=y | 可手动关闭 C |
| `choice` | 多个选项中只能选一个 | 检查是否恰好有一个 y |

### LiteOS-M vs LiteOS-A 配置体系差异

| 维度 | LiteOS-M (L0) | LiteOS-A (L1) |
|------|:---:|:---:|
| Kconfig 选项数 | ~50+ | ~100+ |
| 内核最小体积 | < 10 KB ROM（最小功能集） | 未明确给出（核心组件合计参考值 ~32 KB ROM，见 liteos-ma-components.md §2.3） |
| 配置方式 | GN + Kconfig（**无 make menuconfig**） | GN + Kconfig |
| 特有必选组件 | 无 MMU | MMU/Virtual Memory（~10KB ROM） |
| 目标芯片 | MCU (Cortex-M/RISC-V) | MPU (Cortex-A) |

---

## Exceptions and Fallbacks（异常与兜底）

数据不可得、依赖矛盾、环境不可用时的处理规则（按场景）：

| 场景 | 处理 |
|------|------|
| **组件资源占用/依赖关系查不到** | 先联网查询，查到填值并注明来源；确实查不到才标 TODO + 注明查询关键词，禁止编造或留空 |
| **惰性宏（宏无 C 引用 / 底层无条件启用）** | 关闭不省 ROM/RAM，禁止计入节省合计（防虚报）：Hi3861 PMP——C 代码无 `#ifdef` 引用但 boot 汇编无条件写 PMP CSR，关宏三项皆不省；Track/FPB——全代码树无实现无调用，关闭实际省 0。处置：保持 YES 或关闭均可，但节省标 0/TODO 并注明"无实际收益" |
| **关闭宏的方式错误（注释掉 #define）** | 注释掉 `#define` 后 `#if` 中的未定义标识符按 0 求值（C99 §6.10.1，不报编译错），`#if (CPUP==1)` 静默判假、`#if (CPUP==NO)` 反向判真，配置错误被掩盖；宏被普通 C 表达式引用处才报 undeclared。处置：显式 `#define LOSCFG_BASE_CORE_CPUP NO`（NO=0 走排除分支，干净无残留符号），CPUP_HWI 同理 |
| **文档/记忆中的 #error 守卫与源码不符** | 以实读源码为准：先 Grep 实际 `los_config.h` 的全量 `#error` 清单再下结论。实测案例：文档所述 `#error "cpup need support task monitor"` 在当前 los_config.h 不存在，真实依赖方向相反（CPUP 定义包在 `#if (TSK_MONITOR == YES)` 守卫内，TSK_MONITOR=NO 连带不定义 CPUP）；引用守卫文本必须来自源码实读 |
| **限额下调 vs 组件关闭混淆** | `LOSCFG_XXX_LIMIT` 下调 ≠ 组件关闭：QUEUE_LIMIT 64→16 只缩池，不触发 `los_config.h:421` 的 SWTMR→QUEUE 依赖 `#error`（那条只约束 QUEUE 组件被关闭）。下调方向上保持组件 YES 即安全，但需另评运行期耗尽风险 |
| **实例上限下调偏激进** | 编译期安全（无 STATIC_ASSERT 下限断言 / 无静态池 / 建议值 > 内核默认下限 TSK5/SEM6/MUX6/QUEUE6/SWTMR5）≠ 运行期安全：SEM 砍 68%/QUEUE 砍 75% 时厂商 WiFi 协议栈并发可能运行期耗尽（`LOS_ERRNO_SEM_ALL_BUSY`）。处置：标注风险等级 + 建议保守值（如 SEM 48/QUEUE 24）先跑通冒烟再压 |
| **RAM/ROM 预算超标** | 关非必要扩展组件（lwIP/FS 二选一等）+ 下调实例上限，保留 20% 安全裕量；仍超 → 报告用户升级硬件或砍功能需求，不硬塞 |
| **编译环境不可用 / GN gen 损坏** | 降级为静态核实：`#error` 守卫全量 grep + 源码 `#ifdef` 守卫核对 + RAM 预算复算，结论标注"静态验证通过，待用户环境实跑"，不声称实测通过 |
| **裁剪后编译报错** | 按关键词路由：`undefined reference to LOS_*` → 关了被引用组件，查 select 链补回；`section .text overflowed` → ROM 超标，关扩展组件；`LOSCFG_XXX undeclared` → 宏被注释掉或 GN 集成缺 #define，恢复显式定义 |
