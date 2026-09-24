# SoC 内置 DDR 变体鉴别指南

> 一类常见而隐蔽的坑：同型号 SoC 因内置 DDR 颗粒不同存在多个变体（如 Hi3516CV610 分 -10B/-20S/-20G/-00S/-00G），裸烧 bootrom 阶段的 `reg_info.bin` 必须按变体选对应的 `.xlsm`，错配会导致 DDR 初始化表/参数不匹配——**烧到 100% 但 uboot 起不来**（`wait boot running! uboot运行失败`）。
> 本文把散落在厂商 SDK/Makefile/产品简介里的权威数据收归 skill，使 Agent 能在"这块板子该用哪个 xlsm / DDR 参数是什么"这一类问题上直接给出答案，而不必手工翻厂商文档。

## ⚠️ 数据源边界（重要）

**DDR 变体鉴别数据多来自厂商产品简介型号配置差异表 + 厂商 SDK boot_tools 的 xlsm 文件名 + Makefile**，与驱动适配规格（DTS/pinctrl/clk/寄存器定义/中断/compatible——这些在开源内核/SDK 源码里，可由 `ohos-dev-kernel-source-query` 联网抓取）的数据性质不同。DDR 变体数据的来源维度是：

| 数据项 | 来源 | ohos-dev-kernel-source-query / 联网检索（WebSearch 或等价物）覆盖情况 |
|--------|------|----------------------------------------------|
| 变体后缀 → DDR 类型/容量/封装/速率 | 厂商产品简介「型号配置差异」表（PDF/文档） | **先试联网搜**：ohos-dev-kernel-source-query 查开源 SDK/device_soc 仓的产品简介相关文件 + 联网检索查厂商产品简介 PDF（常被第三方文档站收录）；搜不到标 unavailable |
| 变体 → 对应 .xlsm 文件名 | 厂商 SDK boot_tools 目录的 xlsm 文件名 1:1 对应 | **先试联网搜**：ohos-dev-kernel-source-query 查开源 SDK 仓的 boot_tools 目录（若该 SDK 有开源镜像，可列目录找 .xlsm 文件名）；xlsm 工具包本身常闭源，文件名规律可能查到 |
| reg_info 生成流程（magic/脚本/target） | 厂商 SDK Makefile | **先试联网搜**：ohos-dev-kernel-source-query 查开源 SDK 仓的 Makefile；厂商构建脚本未必开源，搜不到标 unavailable |
| 变体后缀本身（板子实际是哪个变体） | 用户芯片丝印/型号后缀 + 板级配置/demo 板使用指南 | 硬件实物事实——联网只能查 demo 板默认变体，实际板子需问用户 |

> **结论**：DDR 变体这一 gap 的数据源优先级是——**① 已收录**（本文变体表 + `chip-specs-quick-ref.md` 对应条目）**直接用**；**② 未收录先试联网搜**（ohos-dev-kernel-source-query 查开源 SDK/device_soc 仓找 boot_tools/xlsm/产品简介相关文件 + 联网检索查厂商产品简介「型号配置差异」表 / DDR 规格）；**③ 联网也搜不到 → 问用户**（芯片丝印/提供产品简介），标 unavailable + 原因。不预设"一定搜不到"——ohos-dev-kernel-source-query 覆盖范围以它实际能查的开源仓库为准（可能查到 xlsm 文件名，也可能查不到），联网检索是补充途径。

---

## 1. 什么场景要做 DDR 变体鉴别

| 触发场景 | 典型问题 |
|---------|---------|
| 裸烧 SoC（bootrom 阶段直接烧 boot 分区） | 选错 `.xlsm` → `reg_info.bin` 的 DDR 表错 → 烧完起不来 |
| 选 `reg_info.bin` / `xlsm_to_bin` 输入 | 要按板子上的 SoC 变体选 xlsm，不能默认 |
| 诊断"烧到 100% 但 uboot 起不来" | 优先怀疑 DDR 变体错配，核对 xlsm 是否对应该变体 |
| 内存映射/容量填 `chip_spec.json` | 内置 DDR SoC 的容量由变体决定，不是芯片型号单独决定 |

> 外置 DDR SoC（如 -00S/-00G 通过 TFBGA 引脚外挂 DDR3）的变体差异不影响 bootrom 阶段 xlsm 选择——但内置 DDR（QFN 封装）变体的容量/类型差异是硬约束。

---

## 2. 鉴别决策路径

```
SoC 型号（如 Hi3516CV610）
  │
  ├── 该型号是否分多个内置 DDR 变体？
  │     否 → 走常规芯片规格提取（见 chip-specs-quick-ref）
  │     是 → 进入变体鉴别 ↓
  │
  ├── 变体标识从何确定？
  │     ① 芯片丝印/型号后缀（-10B / -20S / -20G / -00S / -00G）
  │     ② 板级配置/demo 板使用指南（demo 板默认变体）
  │     ③ 原理图/封装（QFN9×9 = 内置 DDR；TFBGA = 外置 DDR）
  │     ④ 既有 uboot 的 DDR Training 日志（DDR 类型/频率/容量）
  │
  └── 变体 → DDR 参数（类型/容量/封装/速率）→ 对应 .xlsm
        → xlsm_to_bin.py <xlsm> reg_info.bin -magic <magic>
```

---

## 3. Hi3516CV610 变体权威对应表

**权威来源**：Hi3516CV610 产品简介「型号配置差异」表 + 厂商 SDK `boards/dmeb/tools/pc/boot_tools/` 下的 `.xlsm` 文件名。

### 3.1 型号配置差异（SoC 内置 DDR）

| 变体后缀 | DDR 类型 | DDR 速率 | DDR 容量 | 封装 | 备注 |
|---------|---------|---------|---------|------|------|
| **-10B** | DDR2 | 1333 Mbps | 512 Mb (64 MB) | QFN9×9 | 内置 DDR，小容量 |
| **-20S** | DDR3/3L | 2133 Mbps | 1 Gb (128 MB) | QFN9×9 | 内置 DDR |
| **-20G** | DDR3/3L | 2133 Mbps | 1 Gb (128 MB) | QFN9×9 | 内置 DDR（与 -20S 同 DDR 参数，功能差异见产品简介） |
| **-00S** | DDR3/3L | 2133 Mbps | 最大 4 Gb | TFBGA | **外置** DDR |
| **-00G** | DDR3/3L | 2133 Mbps | 最大 4 Gb | TFBGA | **外置** DDR（与 -00S 同 DDR 接口，功能差异见产品简介） |

> 共同点：CPU 均为 ARM Cortex-A7 @ 950 MHz，16-bit DDR 总线。
> -10B 与 -20S/-20G 是**内置 DDR** 变体，xlsm 必须按容量/类型选——这是裸烧最常踩的坑。
> -00S/-00G 是外置 DDR，xlsm 反映的是最大外挂配置（512 MB），实际容量以板载颗粒为准。

### 3.2 xlsm → 变体 → reg_info 对应表（boot_tools 目录）

| .xlsm 文件名 | 对应变体 | DDR 类型 | 容量 | 封装 | 用途 |
|--------------|---------|---------|------|------|------|
| `Hi3516CV610-DMEB_4L_DDR2_1333M_64MB_16bit-A7_950M_QFN.xlsm` | **-10B** | DDR2 | 64 MB | QFN | 标准量产 |
| `Hi3516CV610-DMEB_4L_DDR2_1333M_64MB_16bit-A7_950M_QFN_24M.xlsm` | -10B | DDR2 | 64 MB | QFN | KOL 变体（24 MHz 晶振） |
| `Hi3516CV610-DMEB_4L_DDR3_2133M_128MB_16bit-A7_950M_QFN.xlsm` | **-20S / -20G** | DDR3 | 128 MB | QFN | 标准量产 |
| `Hi3516CV610-DMEB_4L_DDR3_2133M_128MB_16bit-A7_950M_QFN_24M.xlsm` | -20S / -20G | DDR3 | 128 MB | QFN | KOL 变体 |
| `Hi3516CV610-DMEB_4L_DDR3_2133M_512MB_16bit-A7_950M_BGA.xlsm` | **-00S / -00G** | DDR3 | 512 MB | BGA | 外置 DDR（最大配置） |
| `Hi3516CV610-DMEB_4L_DDR3_2133M_512MB_16bit-A7_950M_BGA_24M.xlsm` | -00S / -00G | DDR3 | 512 MB | BGA | KOL 变体 |
| `Hi3516CV608-DMEB_4L_DDR2_1333M_64MB_16bit-A7_950M_QFN.xlsm` | CV608 板专用 | DDR2 | 64 MB | QFN | Hi3516CV608（非 CV610） |
| `Hi3516CV608-DMEB_4L_DDR2_1333M_64MB_16bit-A7_950M_QFN_24M.xlsm` | CV608 板专用 | DDR2 | 64 MB | QFN | CV608 KOL 变体 |

> 命名规律：`<SoC>-<Board>_4L_<DDR类型>_<速率>_<容量>_<位宽>-<CPU>_<主频>_<封装>[_24M].xlsm`
> `_24M` 后缀 = KOL（King-Out-Line，量产物料）变体，用 24 MHz 晶振；无后缀 = 标准版。

### 3.3 快速鉴别问答

| 问题 | 答案 |
|------|------|
| Hi3516CV610 **-10B** 该用哪个 xlsm？ | `Hi3516CV610-DMEB_4L_DDR2_1333M_64MB_16bit-A7_950M_QFN.xlsm`（KOL 用 `_24M` 版） |
| Hi3516CV610 **-20S / -20G** 该用哪个 xlsm？ | `Hi3516CV610-DMEB_4L_DDR3_2133M_128MB_16bit-A7_950M_QFN.xlsm`（KOL 用 `_24M` 版） |
| Hi3516CV610 **-00S / -00G** 该用哪个 xlsm？ | `Hi3516CV610-DMEB_4L_DDR3_2133M_512MB_16bit-A7_950M_BGA.xlsm`（KOL 用 `_24M` 版） |
| -10B 的 DDR 参数？ | DDR2，1333 Mbps，64 MB，16-bit，QFN9×9 |
| -20S/-20G 的 DDR 参数？ | DDR3，2133 Mbps，128 MB，16-bit，QFN9×9 |
| -00S/-00G 的 DDR 参数？ | DDR3，2133 Mbps，最大 4 Gb（xlsm 按 512 MB 配），16-bit，TFBGA（外置） |

---

## 4. reg_info 生成流程（厂商工具链）

> 以下流程抽象自海思 SDK `boards/dmeb/Makefile`，描述从 `.xlsm` 到 `reg_info.bin` 再到 `boot_image.bin` 的标准路径。skill 不依赖特定项目实例路径——只描述流程与关键参数，落到具体项目时按厂商 SDK 实际目录执行。

### 4.1 流程

```
1. 按 SoC 变体选 .xlsm（见上表）
     │  变量：REGBIN_XLSM（按 CHIP + KOL 选）
     │  规则：KOL=1 → 文件名加 _24M 后缀
     │
2. xlsm_to_bin.py 把 .xlsm → reg_info.bin
     │  命令：python xlsm_to_bin.py <TARGET_XLSM> reg_info.bin -magic <MAGIC>
     │  MAGIC = 2b8c6e1a1a6e8c2b（Hi3516CV610 DMEB）
     │  xlsm_to_bin.py 用 openpyxl 读 xlsm，按 sheet 转 bin
     │  header 184B 内嵌 filename（便于回溯用错 xlsm）
     │
3. reg_info.bin + gsl.bin → image_tool → boot_image.bin
     │  把 reg_info.bin 拷到 image_tool/input/reg_info.bin
     │  把 gsl.bin（components/gsl 源码 make CHIP=xxx 出来，~20KB）拷到 image_tool/input/
     │  跑 oem_quick_build.py（厂商打包工具）→ output boot_image.bin
     │  这一步产出的才是烧录工具认的 boot_image
```

### 4.2 关键参数

| 参数 | 值 | 说明 |
|------|-----|------|
| `REGBIN_XLSM` | 按 CHIP 选（见 3.2 表） | Makefile 变量，决定用哪个 xlsm |
| `KOL_REG_BIN_24M` | KOL=1 时 = `_24M`，否则空 | KOL 量产变体后缀 |
| `REGBING_HEAD_MAGIC` | `2b8c6e1a1a6e8c2b` | reg_info.bin header magic，xlsm_to_bin.py 用 |
| `BOOT_REG_BIN` | `reg_info.bin` | 输出文件名 |
| gsl.bin 来源 | `components/gsl/` 源码 `make CHIP=<chip>` | ~20KB，**不是** u-boot.bin |

---

## 5. 错配症状与诊断

### 5.1 典型症状

| 症状 | 根因 | 诊断方向 |
|------|------|---------|
| 烧到 100% 但 `wait boot running! uboot运行失败` | xlsm 选错变体 → DDR 初始化表不匹配 | 核对 xlsm 文件名 vs 板子 SoC 变体后缀 |
| `DDR Training 失败` | DDR 配置参数不匹配（类型/频率/容量） | 换对应变体的 xlsm 重新生成 reg_info.bin |
| bootrom 阶段 `burn gsl code data failed` | gsl.bin 用错（误用 u-boot.bin 当 gsl） | 核对 gsl.bin 来源是 `components/gsl`，非 u-boot |
| 启动到一半卡 / kernel panic | DDR 容量错 → 内存访问越界 | 核对 xlsm 容量 vs 实际板载 DDR 颗粒 |

### 5.2 诊断流程（ohos-issue-lite-diagnose 联动）

```
症状：裸烧后 uboot 起不来
  │
  ├── 1. 核对 boot_image 是否用对 reg_info.bin
  │      → 回溯 xlsm 文件名 → 对应 SoC 变体（见 3.2 表）
  │      → 错配 → 换 xlsm 重生成 reg_info.bin → 重新打包 boot_image
  │
  ├── 2. 核对 gsl.bin 来源
  │      → 应为 components/gsl 出来的 ~20KB 文件，非 u-boot.bin
  │
  ├── 3. 核对 KOL 标志
  │      → 量产板 KOL=1 → xlsm 要带 _24M 后缀
  │
  └── 4. 仍失败 → DDR 颗粒本身问题（焊接/供电），硬件排查
```

> **关键鉴别信号**：非 boot 分区（env/kernel/rootfs）能连上有正常报错 = 串口/连接没问题 → 倾向 boot_image 内部（reg_info/gsl）问题，别只查时序。

---

## 6. 扩展到其他 SoC

本指南以 Hi3516CV610 为实例，但鉴别模式通用。遇到新的内置 DDR SoC 时，按以下数据源优先级补数据：

1. **先查已收录**：本文变体表 + `chip-specs-quick-ref.md` 是否已有该型号（命中直接用，不必联网）
2. **未收录先试联网搜**（不预设搜不到）：
   a. ohos-dev-kernel-source-query 查开源仓库——厂商 SDK / OpenHarmony device_soc_hisilicon（GitCode）等，找 boot_tools/.xlsm 文件名、产品简介相关文件、Makefile
   b. 联网检索查厂商产品简介「型号配置差异」表 / 芯片型号 DDR 规格（海思产品简介 PDF 常被第三方文档站收录）
3. **联网也搜不到 → 问用户**（芯片丝印 / 提供产品简介），标 unavailable + 原因
4. 拿到数据后：列出所有变体后缀 → DDR 类型/容量/封装/速率 → 对应 .xlsm → reg_info 生成命令，补到本文或 chip-specs-quick-ref

> 数据来源必须可追溯（产品简介章节、SDK 文件路径、Makefile target），写入 `chip_spec.json` 的 `fieldSources`。

---

*文档生成日期：2026-07-16*
*来源：Hi3516CV610 产品简介「型号配置差异」表 + 厂商 SDK `boards/dmeb/Makefile` + `boards/dmeb/tools/pc/boot_tools/` xlsm 文件名*
