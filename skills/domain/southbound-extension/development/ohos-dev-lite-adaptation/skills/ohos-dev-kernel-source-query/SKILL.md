---
name: ohos-dev-kernel-source-query
description: >
  芯片硬件信息多内核查询：覆盖Linux、LiteOS-M、NuttX、FreeRTOS等内核的驱动/适配代码，无需clone仓库。
  按芯片类型自动选择数据源，通过raw URL/Sourcegraph API快速读取源码文件。
  Use when chip hardware info must be looked up in kernel/RTOS source trees without cloning;
  triggers include 查内核源码、查芯片DTS、查HCS、查Kconfig、查寄存器定义、读驱动实现、查引脚/时钟配置、
  搜compatible字符串反查驱动、这块芯片在哪个开源仓库有支持、boot_tools/.xlsm/产品简介文件在哪。
  同义表达：多内核源码检索 / kernel source lookup / 芯片开源支持查询。
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: kernel
  capability: source-query
  version: 0.1.0
  status: trial
---

# 芯片硬件信息多内核查询

查询多种内核生态中的芯片硬件信息，无需clone仓库。根据芯片类型自动选择最佳数据源，快速定位并获取代码片段。

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 源码查询任务 | "查 XX 芯片的 DTS"、"找 esp32c3 的 HCS 配置"、"Kconfig 里有没有 XXX"、"这个 compatible 对应哪个驱动文件" |
| 寄存器/引脚/时钟查询 | "UART0 基地址在哪个头文件"、"XX 的 pinctrl 定义在哪"、"clk 驱动源码" |
| 仓库/支持性查询 | "这块芯片哪个开源仓库有支持"、"Linux 主线收了吗"、"NuttX 有没有这个 BSP" |
| 链式调用 | ohos-dev-soc-spec-parse 的 gap_list 联网补充、DDR 变体查开源 SDK boot_tools / .xlsm 文件名、其他 skill 需要源码证据时 |
| 同义表达 | 查内核源码 / 搜源码片段 / sourcegraph 搜代码 / raw 读文件 |

**不触发**（明确排除）：本地 references/ 已有预提取数据可直答的查询（如 chip-specs-quick-ref 已收录芯片的规格速查，直接查本地即可）；需要 clone 整仓做大规模改动开发（本 skill 只做免 clone 的只读查询）；datasheet PDF 解析（走 ohos-dev-soc-spec-parse）。

## Scope

本 SKILL 是芯片硬件信息的**多内核源码只读查询层**：给定芯片型号 + 查询目标（DTS/HCS/Kconfig/寄存器定义/驱动实现/compatible 反查/boot_tools 等），路由到正确的开源数据源（Linux 主线/厂商树、NuttX、RT-Thread、ESP-IDF、OpenHarmony GitCode 仓），用 raw URL / Sourcegraph / GitCode API 免 clone 拿到代码片段。

**输入**：芯片型号（必需）+ 查询目标（文件类型/关键字/compatible 字符串/符号名）。
**输出**：命中的源码文件路径 + 代码片段（原始内容，不做结构化提取——结构化提取归 ohos-dev-soc-spec-parse）；查不到时明确返回"未查到 + 已查渠道"，供调用方转宿主联网检索能力（WebSearch 或等价物）或问用户。
**不适用**：预提取芯片规格的结构化输出（ohos-dev-soc-spec-parse 的 chip_spec.json）；对仓库做修改/提交（本 skill 只读）；闭源 NDA 材料获取（本 skill 只覆盖公开开源镜像，覆盖范围以实际能查的开源仓库为准）。

## Initial Checks

收到查询后，按以下顺序先做判断（各步结论决定数据源和路径策略）：

1. **芯片在不在映射表**：命中（如 Hi3861 / ESP32-C3 / AT32F437 等）→ 直接取 Primary Source，Fallback 备用；未命中 → 走决策树（① 有无 MMU 定 Linux/RTOS 方向 ② 按优先级逐一搜索）。
2. **芯片类型判定（有/无 MMU）**：Cortex-A / RISC-V with MMU → 优先 Linux（主线→厂商树）；Cortex-M / RISC-V E 系 → 优先 RTOS（RT-Thread→NuttX→厂商 SDK）。近似型号映射也要判（STM32F407 在主线按 F429 查、全志 T507 按 H616 查）。
3. **仓库托管平台判定**：GitHub 仓（Linux/RT-Thread/NuttX/ESP-IDF）→ Sourcegraph/raw URL；GitCode 仓（OpenHarmony device_soc_*）→ GitCode API（**raw URL 格式不可用**）。
4. **查询意图分类**：找文件路径（type:path 搜索）/ 找代码内容（content 搜索，compatible 反查用 literal）/ 读文件内容（raw 优先）/ 列目录（GitCode contents API）——决定阶段 2-3 用哪条工具链。
5. **LiteOS arch 支持类查询**（如可行性别判定）：直接查 `kernel/liteos_m/arch/`（arm/csky/risc-v/xtensa）或 `kernel/liteos_a/arch/`（arm）目录列表。
6. **不预设搜不到**：SoC 变体/.xlsm/boot_tools 等冷门需求也先试本 skill 的联网机制（GitCode API 列目录 + Sourcegraph 搜 Makefile），查不到才标 unavailable——不写"闭源所以一定搜不到"。

## Prohibited Practices（禁止操作）

| 禁止 | 正确做法 |
|------|---------|
| 凭记忆回答硬件参数（基地址/中断号/寄存器偏移） | 必须真查源码拿代码片段作答，并给出来源文件路径；查不到就明说未查到 |
| 未试联网就断言"闭源/查不到" | 先试本 skill 的查询机制（Sourcegraph/GitCode API），覆盖范围以实际能查的开源仓库为准，试过才下结论 |
| clone 整个仓库来查一个文件 | 免 clone：raw URL / Sourcegraph / GitCode API 只取目标文件片段 |
| GitCode 仓用 raw URL（`gitcode.com/{owner}/{repo}/raw/master/{path}`） | 该格式返回 HTML 不是文件内容；必须走 GitCode contents API + blobs/{sha} 两步 |
| 对 GitCode 仓用 Sourcegraph | Sourcegraph 未索引 GitCode 上的 OpenHarmony 仓；用 GitCode API 列目录/读文件 |
| GitHub API 硬刷（限速 10 次/分钟） | 优先 Sourcegraph（不限速）；GitHub API 仅最终兜底 |
| 把查到的代码片段改写/总结后当原文返回 | 返回原始代码片段 + 文件路径，摘要与原文分开标注 |

## ① 文件路由表

### 芯片→数据源映射表

| Chip | Primary Source | Fallback |
|------|---------------|----------|
| STM32F407 | Linux mainline (as F429) | CMSIS-SVD |
| 全志T507 | Linux mainline (as H616) | — |
| Hi3516DV300 | HiSilicon vendor kernel | OpenHarmony HCS |
| Hi3516CV610 | OpenHarmony device_soc_hisilicon（GitCode，查 SoC 目录 / boot_tools / 产品简介相关文件） | 联网检索查厂商产品简介 |
| AT32F437 | NuttX BSP | Artery SDK |
| Hi3861 | OpenHarmony device_soc_hisilicon | koendv/hi3861_notes |
| BES2600W | OpenHarmony device_soc_bestechnic | Bestechnic SDK |
| ESP32-C3 | ESP-IDF | OpenHarmony device_soc_esp |
| XR806 | AW-OL docs | OpenHarmony GitCode |
| ASR582X | OpenHarmony device_soc_asrmicro | ASR IoT SDK |

### 参考文件索引

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| [linux-paths.md](references/linux-paths.md) | Linux路径规律（DTS/pinctrl/clk/DT bindings/Kconfig × 各厂商） | 查询Linux芯片的路径时 |
| [linux-driver-lookup.md](references/linux-driver-lookup.md) | 外设驱动查找表（UART/I2C/SPI/GPIO/PWM/ADC/WDT/Ethernet/DMA × 5+厂商） | 需要从DTS compatible反查驱动文件时 |
| [rtos-sources.md](references/rtos-sources.md) | RTOS路径规律表（LiteOS-M/RT-Thread/NuttX/FreeRTOS/厂商SDK） | 查询RTOS芯片的路径时 |
| [chip-specs-quick-ref.md](../ohos-dev-soc-spec-parse/references/chip-specs-quick-ref.md) | 9颗典型芯片的预提取硬件规格（维护在 ohos-dev-soc-spec-parse skill） | 需要芯片基地址/中断号/时钟等数据时 |
| [examples.md](references/examples.md) | 15个完整查询示例 | 不确定方法怎么用时 |

## ② 工作流

### 阶段1：路由 — 查哪个仓库

根据芯片型号，查①文件路由表的映射表确定目标仓库。

**表中没有的芯片**，按以下决策树路由：

```
① 判断芯片类型
   ├── 有MMU（Cortex-A / RISC-V with MMU）→ 优先查Linux（主线 → 厂商树）
   └── 无MMU（Cortex-M / RISC-V E系列）  → 优先查RTOS（RT-Thread → NuttX → 厂商SDK）
② 按优先级逐一搜索（用Sourcegraph）
   1. Linux主线：repo:github.com/torvalds/linux + 芯片型号
   2. Linux厂商树：查 linux-paths.md §厂商内核树
   3. RTOS BSP：repo:github.com/RT-Thread/rt-thread 或 repo:github.com/apache/nuttx
   4. 厂商SDK：ESP-IDF / 其他
   5. OpenHarmony仓库（GitCode）
③ 第一个有结果的就是主数据源，其余作为交叉校验
```

**⚠️ 关于 SoC 内置 DDR 变体 / boot_tools / .xlsm 查询**：不预设"搜不到"。遇到查 SoC 变体→xlsm 对应、boot_tools 目录、reg_info 生成 Makefile 等 DDR 变体类需求时，**先试本 skill 的联网机制**：
- 用 GitCode API 列 `openharmony/device_soc_hisilicon` 等开源 SDK 仓的 SoC 目录 / boot_tools 目录，看是否有 `.xlsm` 文件名或产品简介相关文件
- 用 Sourcegraph 搜开源厂商 SDK 仓的 Makefile / boot_tools 路径
- 覆盖范围以本 skill 实际能查的开源仓库为准——**可能查到 xlsm 文件名/Makefile target，也可能该 SDK 无开源镜像查不到**
- 查到 → 返回结果；查不到 → 标 unavailable 并说明"ohos-dev-kernel-source-query 对该芯片未查到开源镜像"，由调用方（ohos-dev-soc-spec-parse）转联网检索查厂商产品简介，再不行问用户。不要写"闭源所以一定搜不到"——先试。

### 阶段2：定位 — 文件在哪

1. **查路径规律表**（按需读取）：
   - Linux芯片 → [linux-paths.md](references/linux-paths.md)（DTS/pinctrl/clk/driver路径规律，含厂商内核树和Kconfig/Makefile）
   - RTOS芯片 → [rtos-sources.md](references/rtos-sources.md)（LiteOS-M/RT-Thread/NuttX/FreeRTOS路径）
   - **开源 LiteOS arch 支持检查**（Step 2pre 可行性分析用）：
     - LiteOS-M：查 `kernel/liteos_m/arch/`，支持 **arm / csky / risc-v / xtensa**
     - LiteOS-A：查 `kernel/liteos_a/arch/`，支持 **arm**
     - 如果芯片 arch 在列表中 → 方式 B（直接用开源内核）可行；否则只能走方式 A（厂商内核+KAL）
2. **路径不确定时**：
   - **GitHub仓库**（Linux/RT-Thread/NuttX/ESP-IDF）→ Sourcegraph搜索（~200ms，不限速）：
     ```bash
     curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/{owner}/{repo}+{keyword}+type:path"
     ```
     从返回JSON中提取 `"path"` 字段即为完整路径。
   - **GitCode仓库**（OpenHarmony）→ GitCode API列目录（免认证）：
     ```bash
     curl -s "https://api.gitcode.com/api/v5/repos/{owner}/{repo}/contents/{dir_path}?ref=master"
     ```
     返回JSON数组，每项含`name`（文件名）、`sha`（blob SHA）、`type`（file/dir）。
3. **仍找不到** → Linux主线无结果时，用Sourcegraph搜厂商内核树（见linux-paths.md §厂商内核树）；其他仓库用GitHub API搜索（限速10次/分钟）

### 阶段3：获取 — 拿到代码内容

| 优先级 | 方法 | 速度 | 适用 |
|--------|------|------|------|
| 1 | `curl -sL "https://raw.githubusercontent.com/{owner}/{repo}/master/{path}"` | 最快 | 所有GitHub仓库 |
| 2 | GitCode API读文件（见下方§GitCode获取） | 快 | OpenHarmony仓库（免认证） |
| 3 | Sourcegraph内容搜索（见下方§查询工具） | 中 | 404时的兜底 |
| 4 | GitHub API Contents | 慢（限速） | 最终兜底 |

### GitCode获取（OpenHarmony仓库，免认证）

GitCode公开仓库API**不需要token**，直接curl即可。

```bash
# 列目录（获取文件列表和SHA）
curl -s "https://api.gitcode.com/api/v5/repos/{owner}/{repo}/contents/{dir_path}?ref=master"

# 读文件（返回JSON含base64编码的content字段）
curl -s "https://api.gitcode.com/api/v5/repos/{owner}/{repo}/contents/{file_path}?ref=master"
# 提取内容：返回的JSON中 "content" 字段是base64编码的文件内容

# 下载原始文件（需要先通过列目录获取SHA）
curl -s "https://raw.gitcode.com/{owner}/{repo}/blobs/{sha}/{path}"
```

**两步获取文件的标准流程**：
1. `contents/{dir}` 列目录 → 拿到目标文件的`sha`
2. `raw.gitcode.com/.../blobs/{sha}/{path}` 下载原始内容

> **注意**：`gitcode.com/{owner}/{repo}/raw/master/{path}` 这种raw URL格式**不可用**（返回HTML页面而非文件内容）。

### 阶段4：提取 — 根据用户诉求分析代码

代码已获取，根据用户的具体需求分析代码内容。如需预提取的芯片硬件数据，查 chip-spec 的 `chip-specs-quick-ref.md`。

### 查询工具

**Sourcegraph（首选，不限速，不需要token）：**

```bash
# 路径搜索 — 找文件在哪
curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/{owner}/{repo}+{keyword}+type:path"

# 内容搜索 — 找代码内容（compatible反查驱动、函数定义、寄存器宏等）
curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/{owner}/{repo}+%22exact-string%22+lang:c&patternType=literal"
```

适用仓库：`github.com/torvalds/linux`、`github.com/RT-Thread/rt-thread`、`github.com/apache/nuttx`、`github.com/espressif/esp-idf` 等GitHub公开仓库。**不适用**：GitCode上的OpenHarmony仓库（未索引）。

**Elixir Bootlin（仅Linux，符号交叉引用）：**

```
宿主网页抓取（WebFetch 或等价物）：抓 https://elixir.bootlin.com/linux/latest/ident/{symbol}，取「定义和引用」
```

---

## Exceptions and Fallbacks（异常与兜底）

查询失败、路径不对、仓库未索引时的处理规则：

### 工具级失败兜底

| 失败场景 | 兜底方案 |
|---------|---------|
| raw URL 404（路径不对） | Sourcegraph `type:path` 搜索正确路径 |
| GitHub API 403（限速） | Sourcegraph 替代（不限速） |
| raw.githubusercontent.com 超时 | Sourcegraph 内容搜索 / 宿主网页抓取（WebFetch 或等价物） |
| Sourcegraph 无结果（小众仓库） | GitHub API / 网页抓取（WebFetch 或等价物）读页面 |
| OpenHarmony GitHub镜像过期 | GitCode API（免认证，见§GitCode获取） |
| Sourcegraph 未索引的仓库（如GitCode） | GitCode API 列目录 + 下载文件 |
| GitCode raw URL返回HTML | 改用GitCode API（contents端点），不要用raw URL |

### 结果级兜底

| 场景 | 处理 |
|------|------|
| **映射表+决策树全链路无结果**（该芯片无开源支持） | 明确返回"未查到"，列出已查渠道（主线/厂商树/RTOS BSP/厂商 SDK/OpenHarmony 仓），供调用方转联网检索或问用户——不凭记忆填，不硬选最近似型号当结论 |
| **近似型号映射不命中**（如 STM32F407 按 F429 查到但节点缺失） | 如实报告差异（F429.dtsi 有而 F407 目标侧需裁剪），标注"近似来源"，让调用方决定取舍 |
| **冷门需求（.xlsm/boot_tools/产品简介）** | 先试联网机制（Initial Checks #6），试过才标 unavailable；说明"ohos-dev-kernel-source-query 对该芯片未查到开源镜像"，不写"闭源一定搜不到" |
| **网络工具全部不可用** | 报告失败原因 + 建议替代（本地 references/ 已收录数据 / 联网检索 / 问用户提供源码路径），不以"工具不可用"为由凭记忆作答 |
| **多数据源内容矛盾** | 同时返回两侧片段 + 各自文件路径供调用方交叉验证，不擅自择优隐藏另一方 |

## 常见路径速记

- DTS: `arch/{arm,arm64}/boot/dts/{vendor}/{chip}.dtsi`
- pinctrl: `drivers/pinctrl/{vendor}/pinctrl-{chip}.c`
- 时钟: `drivers/clk/clk-{chip}.c`（注意：STM32没有st/子目录）
- UART: `drivers/tty/serial/` — IP核复用常见（全志/RK用DW 8250，海思用PL011）
- I2C: `drivers/i2c/busses/` — 全志用MV64xxx，海思用DW I2C
- 完整驱动路径表 → [linux-driver-lookup.md](references/linux-driver-lookup.md)
