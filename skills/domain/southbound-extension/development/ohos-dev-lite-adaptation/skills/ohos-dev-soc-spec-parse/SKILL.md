---
name: ohos-dev-soc-spec-parse
description: OpenHarmony Lite (L0/L1) 芯片适配的第一步——从芯片型号 + datasheet/SDK/DTS 提取结构化硬件规格（外设基地址/中断号/时钟树/引脚复用/DDR 变体）输出 chip_spec.json。Use when a new chip/SoC is being adapted to OpenHarmony Lite and hardware specs are needed; triggers include 芯片规格提取、解析 datasheet、生成 chip_spec、查外设基地址/中断号/时钟/引脚复用、DDR 变体鉴别、该用哪个 xlsm、reg_info 生成、单点查询某外设 IRQ/基地址。下游设备配置生成/构建装配/内核裁剪消费本 skill 产出。
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: soc
  capability: spec-parse
  version: 0.1.0
  status: trial
---

# OpenHarmony Lite 芯片规格解析

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 完整提取任务 | "提取 XX 芯片规格"、"生成 chip_spec"、"XX 适配要哪些硬件信息"、"全量提取" |
| 单点查询 | "UART0 中断号是多少"、"XX 的基地址"、"DTS 在哪"、"这块板子该用哪个 xlsm" |
| 症状词（隐性需求） | "裸烧 uboot 起不来是不是 xlsm 选错"、"DDR 变体怎么确认"、"reg_info 怎么生成" |
| 下游 skill 链式调用 | ohos-dev-board-config-gen / ohos-dev-build-config / ohos-dev-hal-skeleton-gen / ohos-dev-kernel-trim-config 需要 chip_spec.json 输入 |
| 同义表达 | 芯片画像 / 硬件规格表 / SoC spec / 寄存器中断提取 |

**不触发**（明确排除）：只要 datasheet 原文某段翻译、不涉及结构化提取的问答；已有 chip_spec.json 只是要改某个值的编辑任务（直接改，无需重跑提取）。

## Scope

本 SKILL 是芯片规格提取的**编排层**，支持两种模式：

- **完整提取**：芯片型号 → 7 步工作流 → chip_spec.json
- **单点查询**：具体问题 → MCP 速查（命中则直接回答）→ 未命中调 ohos-dev-kernel-source-query

意图判断详见 Step 0。完整提取模式的输出 `chip_spec.json` 可直接用于设备配置生成、构建装配、内核裁剪等下游流程。

**输入**：芯片型号（必需）；datasheet PDF/文档路径、SDK 源码路径、板级 DTS（可选，有则提取更准）。
**输出**：`chip_spec.json`（结构化芯片规格，按 json-schema-design.md schema）+ 完整性报告（三级 checklist 填充率 + 置信度）。
**不适用**：非 OpenHarmony Lite 目标的芯片评估（如跑 Android/Linux 发行版选型分析）；只改 chip_spec.json 个别值的编辑任务；DDR 颗粒时序调试（走 ohos-issue-lite-diagnose）。

## Initial Checks

收到任务后，按以下顺序先做判断（各步结论决定后续路径）：

1. **意图判断**：完整提取 or 单点查询？（详见 Step 0 决策树）——单点查询不跑完整 8 步，直接查答。
2. **目标系统级别判定**（L0/L1）：有 MMU（Cortex-A / 带 MMU 的 RISC-V）→ L1；无 MMU（Cortex-M / RISC-V E 系）→ L0。这决定 checklist 裁剪（寄存器位域项）。
3. **功能能力判定**：WiFi/BLE 集成？ISP/视频编解码？→ 决定额外 checklist 项。
4. **内置 DDR 变体判定**：该型号是否多变体 SoC（查 `references/ddr-variant-guide.md`）——多变体必须让用户确认丝印后缀，未确认前 DDR 参数标 TODO。
5. **数据源可用性盘点**：quick-ref 已收录？datasheet/SDK/DTS 路径用户给了没？——决定 Step 2 预查起点和 Step 4 联网范围。
6. **用户显式覆盖优先**：用户明确指定系统级别/平台（如"i.MX6ULL 做 L1"）时以用户指定为准，覆盖自动判定。

## Prohibited Practices（禁止操作）

| 禁止 | 正确做法 |
|------|---------|
| 凭记忆填基地址/中断号 | 必须从 DTS/SDK/手册提取，标注来源到 fieldSources |
| **跳过 ohos-dev-kernel-source-query 直接编造缺口数据** | **gap_list 中每个缺口必须调用 ohos-dev-kernel-source-query SKILL 联网查询，禁止凭记忆/推测填写任何硬件参数（基地址、中断号、寄存器地址等）。外部知识源没有的数据 = 必须联网，无例外** |
| 跳过缺口分析直接输出 | 先按系统级别和功能能力裁剪 checklist，再对比产出 gap_list |
| 复制参考文档到本地 | 通过可用知识检索工具按需获取，本地 references/ 是回退源 |
| 生成下游配置文件（HCS/BUILD.gn 等） | chip_spec.json 是终点，下游 SKILL 负责配置文件 |
| 编造无法获取的字段 | 标 null + 在 fieldSources 中说明原因 |
| 跳过交叉验证 | 地址重叠/中断冲突必须发现并报告 |
| **datasheet 查不到时猜颗粒规格（page/OOB/容量/地址）** | **以能跑的 bin 的 runtime print 为权威**——别猜，找该颗粒上能正常跑的 u-boot/内核 bin，烧上去看 runtime 打印（`Page:2KB OOB:128B` / `spi nand id: 0xe5 0xf1`）填规格。datasheet 查不到就别查了，runtime 实测 > datasheet（见下方「颗粒规格 runtime 证据优先」） |

### 颗粒规格 runtime 证据优先于缺 datasheet

> **背景**：板载 SPI Nand / SPI Nor 颗粒常无公开 datasheet（或型号对不上、版本不符），驱动适配时 ID 表/规格参数（page/OOB/容量）没法定。实测 hi3516cv610 板载 DS35Q1GB-IB 颗粒查不到 datasheet，靠 uboot 启动早期 `spi nand id: 0xe5 0xf1` print + 同表同规格条目对照完成适配。详见 `skills/ohos-issue-lite-diagnose/references/fault-knowledge-base.md` §7.3 + `diagnostic-cases.md` §8 案例BG003。

**原则**：datasheet 查不到时，**以能跑的 bin 的 runtime print 为权威**，别猜地址/规格。

**流程**：
```
颗粒规格 datasheet 查不到
  │
  ├── ① 找一个在该颗粒上能正常跑的 bin
  │     厂商 SDK / 参考板 / 同颗粒别的板子的 u-boot / 内核 bin
  │
  ├── ② 烧上去启动，看 runtime 打印的颗粒规格
  │     spi nand id: 0xe5 0xf1                    ← 颗粒 ID（JEDEC）
  │     Page:2KB OOB:128B                          ← page/OOB 规格
  │     pagesize 2048 oobsize 128 chipsize 128MB   ← 驱动实测读寄存器/ID 出来的
  │
  ├── ③ 以 runtime print 的实际值为权威填进 ID 表 / 驱动参数 / chip_spec.json
  │     datasheet 查不到就别查了——runtime 实测 > datasheet
  │     （datasheet 也可能印错/版本不符）
  │
  └── ④ chip_spec.json 的 fieldSources 标 "runtime print from <bin来源>"
        不是 "unavailable"，因为有 runtime 证据
```

**为什么 runtime print 是 ground truth**：
- 驱动的 `Page:2KB OOB:128B` print 是**实测读寄存器/ID 出来的**，比 datasheet 印刷值更可信。
- datasheet 可能版本不符（颗粒改版）、印错、或根本不公开。runtime print 是颗粒在真实硬件上跑出来的。

**适用范围**：SPI Nand / SPI Nor / eMMC 等存储颗粒的 page/OOB/容量/ID 规格。不适用于 DDR 颗粒（DDR 走 xlsm/reg_info，见 `references/ddr-variant-guide.md`）。

**关联**：
- `skills/ohos-issue-lite-diagnose/references/fault-knowledge-base.md` §7.3（颗粒规格 runtime 证据优先）
- `skills/ohos-issue-lite-diagnose/references/diagnostic-cases.md` §8 案例BG003（DS35Q1GB ID 表，颗粒 ID + 2KB page/128B OOB 从 uboot print 抓）

---

## ① 文件路由表

根据用户意图，按需获取参考文档（优先使用可用知识检索工具，回退到本地 references/）。**每次只读一个**，不要一次性加载所有文档。

> **检索方式**: Agent 自动选择最匹配的可用知识检索工具。
> 如有可用的知识检索服务（MCP 等）→ 使用其搜索/读取能力
> 否则 → 直接 `read` 本地 references/ 下的文件
> 本地也没有 → 联网搜索 → 询问用户

| 用户意图 | 信息需求 | 首选本地材料 |
|---------|---------|-------------|
| 判断需要什么信息 | 硬件信息提取 checklist | `references/hardware-info-checklist.md` |
| 确定 JSON 输出格式 | chip_spec.json schema 设计 | `references/json-schema-design.md` |
| 确定输出模板（target_config / HAL / HCS） | 各类输出模板定义 | `references/output-templates.md` |
| 查预提取的芯片数据（9 颗） | 已有芯片规格速查表 | `references/chip-specs-quick-ref.md` |
| **查 SoC 内置 DDR 变体 / 该用哪个 xlsm / reg_info 生成** | **DDR 变体鉴别与 reg_info 流程指南** | **`references/ddr-variant-guide.md`** |
| 解析 DTS 文件 | DTS 语法与提取方法 | `references/dts-parsing-guide.md` |
| 解析 Linux pinctrl/clk 代码 | Linux 内核源码查询方法 | `references/linux-source-guide.md` |
| 解析 SDK 头文件 | SDK 头文件提取案例 | `references/sdk-extraction-cases.md` |
| 理解外设寄存器通用模式 | 寄存器位域通用模式 | `references/peripheral-register-patterns.md` |
| 参照完整提取案例（Linux） | 已有芯片适配完整案例 | `references/adaptation-cases.md` |
| 确定 target_config 骨架 | target_config 模板 | `references/target-config-template.md` |
| 联网查询源码（DTS/SDK/驱动） | 调用 ohos-dev-kernel-source-query SKILL | — |
| 查芯片源码路径规律 | ohos-dev-kernel-source-query SKILL 内的 linux-paths.md / rtos-sources.md | — |
| 查硬件引脚/外设/内存分配（可视化） | Hi3861 官方 Hardware Quick Reference 图 | `references/hi3861_hardware/Hardware_Quick_Reference.png` |

### 硬件信息适用规则

芯片的 checklist 适用范围由两个维度共同决定：

**维度 1：系统级别（L0/L1）→ 决定寄存器位域需求**

| 系统级别 | 判断方法 | checklist 差异 |
|----------|---------|---------------|
| **L0**（无 MMU） | Cortex-M / RISC-V 无 MMU | 需要寄存器定义+位域（HAL 驱动开发必需） |
| **L1**（有 MMU） | Cortex-A / RISC-V 有 MMU | 不需要寄存器位域（HDF 驱动已封装） |

**维度 2：功能能力 → 决定额外字段需求**

| 功能能力 | 判断方法 | 额外 checklist 项 |
|----------|---------|------------------|
| **WiFi/BLE** | 芯片集成无线模块 | RF 校准/天线配置 |
| **视频处理** | 芯片集成 ISP/视频编解码 | ISP/MIPI CSI/视频编解码 |
| **通用** | 无特殊功能模块 | — |

> 一个芯片同时具有系统级别和功能能力。例如：
> - Hi3861 = L0 + WiFi → 需要寄存器位域 + RF/天线
> - Hi3516DV300 = L1 + 视频 → 不需要寄存器位域 + 需要 ISP/MIPI
> - STM32F407 = L0 + 通用 → 需要寄存器位域，无额外项
> - ESP32-C3 = L0 + WiFi → 需要寄存器位域 + RF/天线

---

## ② 工作流

### Step 0: 意图判断

接受用户输入，判断走完整提取还是单点查询：

```
用户输入
  │
  ├── 明确要求完整提取（"提取规格"、"生成 chip_spec"、"全量信息"）
  │   → 进入 Step 1（完整提取模式）
  │
  ├── 询问具体字段/信息（"中断号是多少"、"基地址"、"DTS 在哪"）
  │   → 直接调用 ohos-dev-kernel-source-query SKILL（单点查询模式）
  │   → 返回查询结果，流程结束
  │
  └── 不明确
      → 默认进入 Step 1（完整提取模式）
```

**单点查询模式**：

1. 从用户问题中提取芯片型号和查询目标
2. 先查可用知识检索工具（MCP 等）是否有该芯片的预提取数据覆盖此字段
   - 有 → 直接回答，无需联网
   - 无 → 调用 ohos-dev-kernel-source-query SKILL 联网查询
3. **特殊：SoC 内置 DDR 变体类查询**（"这块板子该用哪个 xlsm"、"DDR 参数是什么"、"reg_info 怎么生成"、"裸烧 uboot 起不来是不是 xlsm 选错"）→ 先查 `references/ddr-variant-guide.md` 和 `references/chip-specs-quick-ref.md` 的 DDR 变体表（如 Hi3516CV610 -10B/-20S/-20G/-00S/-00G），命中则直接回答变体 → DDR 参数 → 对应 xlsm → reg_info 生成命令；**未命中 → 先试联网搜**（不预设搜不到）：① ohos-dev-kernel-source-query 查开源仓库（厂商 SDK / OpenHarmony device_soc_hisilicon 等，找 boot_tools/.xlsm 或产品简介相关文件）② 宿主联网检索能力（WebSearch 或等价物）查厂商产品简介「型号配置差异」表 / 芯片型号 DDR 规格（海思产品简介 PDF 常被第三方文档站收录）；联网搜不到 → 问用户（芯片丝印 / 提供产品简介），在回答中标注数据源边界
4. 返回查询结果

### Step 1: 芯片识别

接受芯片型号，确定四个属性：

| 属性 | 判断方法 |
|------|---------|
| 系统级别（L0/L1） | 有 MMU → L1；无 MMU → L0 |
| CPU 架构 | Cortex-M4F / Cortex-A7 / RV32IMAC / Xtensa 等 |
| 厂商 | STMicroelectronics / HiSilicon / Espressif 等 |
| 功能能力（可多选） | WiFi / 视频处理 / 通用 |
| **内置 DDR 变体**（如适用） | 同型号 SoC 因内置 DDR 颗粒不同分多变体（如 Hi3516CV610 -10B/-20S/-20G/-00S/-00G）。变体决定 DDR 类型/容量/封装/速率 + 对应 xlsm + reg_info。裸烧 bootrom 阶段必须按变体选 xlsm，错配导致 uboot 起不来。查 `references/ddr-variant-guide.md` |

**判断流程**：

```
① 查知识检索工具命中的 chip-specs-quick-ref
   ├── 芯片在列表中 → 直接取已有属性（系统级别 + 架构 + 厂商）
   └── 芯片不在列表 → 走 ohos-dev-kernel-source-query 路由决策树判断系统级别和架构

② 判定系统级别（维度 1）
   ├── 有 MMU（Cortex-A / RISC-V with MMU）→ L1
   └── 无 MMU（Cortex-M / RISC-V E 系列）  → L0

③ 判定功能能力（维度 2，可多选）
   ├── 有 WiFi/BLE 集成 → 标记 WiFi
   ├── 有 ISP/视频编解码 → 标记 视频处理
   └── 均无 → 标记 通用

④ 判定内置 DDR 变体（维度 3，如适用）
   ├── 查 references/ddr-variant-guide.md 变体表
   │   ├── 该型号有多变体 → 需用户/丝印确认变体后缀 → 取 DDR 参数 + xlsm
   │   └── 该型号无变体 → 跳过
   └── 不确定是否有变体 → 先试联网搜厂商产品简介「型号配置差异」表（ohos-dev-kernel-source-query 查开源 SDK/device_soc 仓的 boot_tools / 产品简介文件 + 联网检索查厂商产品简介 PDF/型号差异表）；联网搜不到 → 问用户（芯片丝印/产品简介）

⑤ 用户可显式指定覆盖自动判断
   例："我想适配 NXP i.MX6ULL 做 L1"
```

### Step 2: 预查可用知识源

如有可用的知识检索工具（MCP 等），尝试获取预提取数据：

```
1. 使用可用工具搜索关键词 <芯片名>（如 keyword_search / read_doc 本地 references/）
   → 找到该芯片相关的文档/数据
   → 有? → 进入 Step 3
   → 无? → 继续 Step 3（无预提取数据，全部联网查询）

2. read_doc(chip-spec, "references/chip-specs-quick-ref.md")
   → 提取该芯片的预提取数据（如有）

3. 产出 partial_data：
   {
     "metadata": { vendor, chipName, architecture, ... },
     "cpu": { coreType, fpu, mmu, ... },
     "memoryMap": [...],
     "peripherals": [...],
     "ddrVariant": { variantSuffix, ddrType, ddrCapacity, packageType, xlsmFile, ... },  // 仅内置 DDR 多变体 SoC
     ...
   }
```

> 9 颗已覆盖芯片（STM32F407/Hi3516DV300/全志T507/AT32F437/Hi3861/ESP32-C3/BES2600W/XR806/ASR582X）在 chip-specs-quick-ref 中有详细数据。Hi3516CV610 的 DDR 变体/xlsm 对应表见 `references/ddr-variant-guide.md`。

### Step 3: 缺口分析

根据 Step 1 的系统级别和功能能力裁剪 checklist，对比 partial_data 产出 gap_list：

```
1. read_doc(chip-spec, "references/hardware-info-checklist.md")
   → 获取完整 checklist（三级：必须有/高频使用/按需使用，共 7/4/5 = 16 项）

2. 按两个维度裁剪：
   维度 1（系统级别）：
     L0 → 全部 7 项必须有均适用（含"寄存器定义+位域"）
     L1 → 移除"寄存器定义+位域"（必须有降为 6 项）
   维度 2（功能能力）：
     WiFi  → 必须有增加 RF 校准/天线配置
     视频  → 必须有增加 ISP/MIPI/视频编解码
     通用  → 无额外项
   维度 3（内置 DDR 变体，如适用）：
     多变体 SoC → 必须有增加"SoC 内置 DDR 变体鉴别"（变体→DDR 参数→xlsm→reg_info）
     无变体 SoC → 无额外项

3. 逐项比对 partial_data：
   gap_list = [
     { field: "DMA通道映射", priority: "高频使用", status: "missing" },
     { field: "寄存器位域", priority: "必须有", status: "missing" },  // 仅 L0
     ...
   ]
```

### Step 4: 联网补充（强制）

> **⚠️ 本步骤不可跳过。gap_list 中每个缺口必须调用 ohos-dev-kernel-source-query SKILL 联网查询。禁止凭记忆/推测填写任何硬件参数。**

> **⚠️ 数据源边界说明——SoC 内置 DDR 变体**：DDR 变体鉴别数据（变体后缀→DDR 类型/容量/封装/速率→xlsm→reg_info）多来自厂商产品简介型号配置差异表 + 厂商 SDK boot_tools 的 xlsm 文件名 + Makefile。已结构化收录的 SoC（如 Hi3516CV610）数据在 `references/ddr-variant-guide.md` + `references/chip-specs-quick-ref.md`，**优先直接用，不必每次联网**。未收录的新 SoC：**先试联网搜**（不预设搜不到）——① ohos-dev-kernel-source-query 查开源仓库（厂商 SDK / OpenHarmony device_soc_hisilicon 等，可能查到 boot_tools/.xlsm 文件名或产品简介相关文件；覆盖范围以 ohos-dev-kernel-source-query 实际能查的开源仓库为准，可能查到也可能查不到）② 联网检索查厂商产品简介「型号配置差异」表 / 芯片型号 DDR 规格（海思产品简介 PDF 常被第三方文档站收录）；联网搜不到 → 问用户（芯片丝印/提供产品简介），在 fieldSources 中标 `unavailable — 联网未查到（ohos-dev-kernel-source-query 覆盖开源仓库 + 联网检索查厂商产品简介均无果），需问用户芯片丝印/产品简介`。详见 `references/ddr-variant-guide.md` §数据源边界。

对 gap_list 中每个缺口，调用 ohos-dev-kernel-source-query SKILL 获取数据：

```
对每个 gap：
  1. 确定数据类型 → 选择查询目标
     ├── DTS 数据（reg/interrupts/clocks）→ 查 Linux/RTOS DTS
     ├── 寄存器定义 → 查 SDK 头文件 / pinctrl 驱动
     ├── 时钟树 → 查 clk 驱动 / CCU 头文件
     ├── 引脚复用 → 查 pinctrl 驱动 / GPIO AF 表
     ├── RF/天线 → 查厂商 SDK / OpenHarmony 适配仓库
     └── SoC 内置 DDR 变体 → 先查 references/ddr-variant-guide.md + chip-specs-quick-ref.md（已收录则直接用）
         → 未收录 → 先试联网搜：① ohos-dev-kernel-source-query 查开源 SDK/device_soc 仓（找 boot_tools/.xlsm 文件名或产品简介相关文件，覆盖范围以实际能查的开源仓库为准）② 联网检索（WebSearch 或等价物）查厂商产品简介「型号配置差异」表 / DDR 规格
         → 联网搜不到 → 问用户（芯片丝印/提供产品简介），fieldSources 标 `unavailable — 联网未查到，需问用户`

  2. 调用 ohos-dev-kernel-source-query SKILL（必须执行；DDR 变体项先查已收录表，未收录则按上一步先试联网搜）
     → ohos-dev-kernel-source-query 按芯片→数据源路由找到源码
     → 返回原始代码片段
     → 禁止跳过此步直接用已有知识填充

  3. 按解析指南提取结构化数据
     ├── DTS → read_doc(chip-spec, "references/dts-parsing-guide.md")
     ├── pinctrl/clk → read_doc(chip-spec, "references/linux-source-guide.md")
     ├── SDK 头文件 → read_doc(chip-spec, "references/sdk-extraction-cases.md")
     └── 寄存器 → read_doc(chip-spec, "references/peripheral-register-patterns.md")

  4. 提取的数据补充到 partial_data
```

> ohos-dev-kernel-source-query 查询失败时，字段标 null，在 fieldSources 中记录 "unavailable — <原因>"。**只有联网查询明确失败后才允许标 null，不允许未经查询就标 null。**

### Step 5: 结构化输出

按 JSON Schema 组织数据，生成 chip_spec.json：

```
1. read_doc(chip-spec, "references/json-schema-design.md")
   → 获取完整的 ChipSpecification JSON Schema

2. 组织数据到 Schema 结构：
   {
     "metadata": {
       "vendor": "STMicroelectronics",
       "chipName": "STM32F407VGT6",
       "architecture": "ARM_Cortex_M",
       "targetSystemLevel": "L0",
       "kernelType": "liteos_m",
       ...
     },
     "cpu": { "coreType": "Cortex-M4F", "fpu": true, ... },
     "memoryMap": [...],
     "peripherals": [...],
     "interruptController": { "type": "NVIC", ... },
     "clockSystem": { ... },
     "pinMux": [...],
     "ddrVariant": { "variantSuffix": "-10B", "ddrType": "DDR2", "ddrCapacity": "64MB", "packageType": "QFN9x9", "xlsmFile": "Hi3516CV610-DMEB_4L_DDR2_1333M_64MB_16bit-A7_950M_QFN.xlsm", "regInfoMagic": "2b8c6e1a1a6e8c2b" },  // 仅内置 DDR 多变体 SoC
     "fieldSources": {
       "cpu.coreType": "chip-specs-quick-ref（知识检索命中）",
       "peripherals.0.baseAddress": "Linux mainline arch/arm/boot/dts/st/stm32f429.dtsi",
       "peripherals.0.interrupts.0.irqNumber": "Linux mainline stm32f429.dtsi",
       "peripherals.*.dmaChannels": "unavailable — requires vendor datasheet",
       "ddrVariant": "references/ddr-variant-guide.md (来源: Hi3516CV610 产品简介型号配置差异表 + SDK boot_tools xlsm)"
     }
   }

3. 写到当前工作目录：chip_spec.json
4. 在对话中展示完整 JSON
```

### Step 6: 交叉验证

对提取的数据执行三项检查：

| 检查项 | 方法 | 发现问题 |
|--------|------|---------|
| 寄存器地址不重叠 | 各外设 `[base, base+size)` 无交集 | 报告冲突的外设名和地址范围 |
| 中断号无冲突 | 不同外设的 irqNumber 不重复 | 标注共享 IRQ（如 ADC1/2/3 共享）vs 真冲突 |
| 内存映射合理 | Flash/RAM 地址不重叠，大小在合理范围 | 报告异常值（如 RAM > 物理可能） |

发现问题时，报告给用户确认后再输出。

### Step 7: 完整性报告

按两个维度裁剪后的 checklist 输出填充率：

```
📊 芯片规格提取报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
芯片：STM32F407VGT6
系统级别：L0 | 功能能力：通用
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 必须有      7/7   ← 全有，可进入适配
✅ 高频使用     4/4
⚠️ 按需使用     3/5   ← 低功耗/JTAG 待补充
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
置信度：0.96
输出文件：./chip_spec.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 chip_spec.json 已生成，可用于后续：
   - 设备配置生成（ohos-dev-board-config-gen）
   - 构建装配（ohos-dev-build-config）
   - 内核裁剪（ohos-dev-kernel-trim-config）
```

**置信度计算**：

```
score = (filled_必须 / total_必须) × 0.6
      + (filled_高频 / total_高频) × 0.3
      + (filled_按需 / total_按需) × 0.1

基数来自 hardware-info-checklist.md 最小必要清单：
  通用芯片：必须 7 / 高频 4 / 按需 5（共 16 项）
  L0 芯片：必须 7（含寄存器位域）
  L1 芯片：必须 6（移除寄存器位域）
  WiFi 芯片：必须 +1（RF 校准/天线）
  视频芯片：必须 +1（ISP/MIPI/视频编解码）
  内置 DDR 多变体 SoC：必须 +1（DDR 变体鉴别）

示例（STM32F407 = L0 + 通用）：
  必须 7/7, 高频 4/4, 按需 3/5
  → 1.0×0.6 + 1.0×0.3 + 0.6×0.1 = 0.96
```

---

---

## Exceptions and Fallbacks（异常与兜底）

信息不足、查询失败、数据矛盾时的处理规则（按场景）：

| 场景 | 处理 |
|------|------|
| **联网/源码查询明确失败** | 字段标 null，fieldSources 记录 `unavailable — <原因>`。**只有查询明确失败后才允许标 null，不允许未经查询就标 null** |
| **知识检索服务不可用**（MCP 未配置/连接失败） | 降级链：本地 references/ → 联网搜索 → 询问用户。禁止以"工具不可用"为由跳过提取 |
| **数据源之间矛盾**（如参考资料写单核@950MHz，SDK autoconf/DTS 是双核@1200MHz） | 不盲信任何一方：以**可验证的源码证据**（SDK autoconf.h / DTS）为准，在 `crossValidation.discrepancies` 记录矛盾双方 + 取舍依据 + 建议的运行时复核手段（如烧录后 /proc/cpuinfo） |
| **datasheet 查不到颗粒规格**（page/OOB/容量） | 不猜——走「颗粒规格 runtime 证据优先」流程（见上方专节）：找能跑的 bin 烧上去看 runtime print，fieldSources 标 `runtime print from <bin来源>` |
| **DDR 变体无法确认**（用户不在场/丝印不可读） | variantSuffix 等字段标 TODO + 在 gapList 注明"需用户确认丝印"，不默认取某个变体 |
| **新 SoC 的 DDR 变体未收录** | 先试联网搜（ohos-dev-kernel-source-query 查开源 SDK/device_soc 仓 + 搜厂商产品简介型号差异表）；搜不到 → 问用户（丝印/产品简介），fieldSources 标 `unavailable — 联网未查到，需问用户` |
| **用户输入的芯片型号查无此物** | 先与用户确认拼写/完整型号（SoC 名 vs 板名 vs 家族名常见混淆），不擅自选最近似型号 |
| **交叉验证发现冲突**（地址重叠/中断冲突） | 报告用户确认后再输出；区分共享资源（如同控制器多 devid 共享 IRQ，硬件设计）vs 真冲突 |

---

> 速查: `references/cheatsheet.md`
