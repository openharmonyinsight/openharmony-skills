---
name: env-prep
description: 工作流 Phase 1——搭建嵌入式 OS 芯片适配开发环境：执行构建工具链安装、源码同步、初始配置文件生成、芯片基础信息收集。触发症状：用户说"环境搭建"、"build 跑不通"、"新项目初始化"、"准备开始移植"、"./build.sh --product-name {product}"、"repo sync"。
license: MIT
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: lite
  capability: env-prep
  version: 0.1.0
  status: trial
  category: workflow-step-env-prep
  downstream: ../04-build-verify/SKILL.md (GATE-0 re-check)
---

# Phase 1: 项目初始化与环境准备

本阶段包含 GATE-0 环境健康检查（hb/gn/ninja/工具链四子门控）、工具链路径冲突全扫、Board/SoC 目录规范。

## 契约（来自编排器 `skills/ohos-dev-workflow-router/SKILL.md` v0.1.0）

| 属性 | 值 |
|------|-----|
| **输入** | `target.name`, `target.arch`, `target.ram_size`, `target.flash_size`, `target.system_type` (mini=L0 轻量 \| small=L1 小型), `vendor`, `board_name` |
| **产出** | ① device 树目录结构 (board + soc) ② `config.json` + `config.gni` 基准 ③ 构建系统可执行 (hb/gn/ninja/toolchain) ④ **GATE-0 环境健康报告** (4 子门控) ⑤ 芯片基础信息清单 (`chip-spec` 或等价物) ⑥ Phase B 输入清单、来源分类和启动链闭合预检 |
| **门控** | **GATE-0**: 项目启动确认（芯片/系统/版本/./build.sh --product-name {product} 基线 + 4 子门控环境健康 + 完整镜像前置闭合预检） |
| **后续** | → P2 内核移植 / → P3 驱动开发 |

> **⚠️ 如果用户未在自然语言中说明 L0 还是 L1，必须询问**：
> - **L0（轻量系统）**：RAM < 1MB，LiteOS-M 内核，IoT HAL 驱动，MCU 级
> - **L1（小型系统）**：1MB < RAM < 16MB，LiteOS-A 内核，精简 HDF 驱动，MPU 级
>
> L0/L1 直接决定 P4 构建行为（单 bin vs 多产物）；P2 内核选型与 P3 驱动框架分别读 target profile 的 `kernel_family` / `driver_model` 字段，不从 L0/L1 标签推断（见编排器 §target profile 加载规则）。一旦选定，全下游分支。

## 知识检索（可用时优先知识检索服务如 project-brain MCP；不可用按 skill 知识检索降级链：本地 references → 联网搜索 → 询问用户）

本步骤的本地代码分析，可用时优先使用（可选）project-brain 等知识检索服务 MCP：
- `get_module_contents` — 看现有 adapter/SDK 模块含哪些函数（规划目录时参考已有结构）
- `locate_symbol` — 定位现有配置/初始化函数
- `get_file_symbols` — 看某文件定义了哪些符号

> MCP 调失败或未装 → 按 skill 知识检索降级链回退。

## 子步骤

```
Step 0: ★ 前置决策采集 — 工作流一开始批量收能提前定的决策（config 或一连串问题）
    │
Step 1: 目录规划 — 创建 Board/SoC 分离的 device 树结构
    │
Step 2: 工具链安装 — hb + gn + ninja + 编译工具链 + 源码同步
    │   ├─ 2a: hb 安装与修复 (pip install-e + __init__.py + import fix)
    │   ├─ 2b: gn / ninja 二进制验证
    │   └─ 2c: 交叉编译工具链 (prebuilt / from-source / wrapper)
    │
Step 3: 配置预适配 — config.json / config.gni / BUILD.gn(board) 初始填充
    │   └─ 3a: ./build.sh --product-name {product} → 自动生成 components.json (实测 F-003)
    │
Step 4: GATE-0 环境健康检查 ★ 实测关键发现
    │   ├─ 0a: hb 模块可导入?
    │   ├─ 0b: gn 二进制可用?
    │   ├─ 0c: components.json 存在?
    │   └─ 0d: 工具链可用? (含指令集扩展)
    │
Step 5: 信息收集 — 芯片规格初版 (供 P2/P3 消费)
```

---

## Step 0: 前置决策采集（P-前置采集原则）

> **为什么有这一步**：避免"推进到每个门控才问一次"的碎片化交互。工作流一开始就把**能提前定的决策**批量采集（config 文件或一连串问题），写入 `workflow_config.yaml` / `chip-basics.yaml`，下游门控消费预录决策、不再重复问。只有**真正晚绑定 / 分支太密**的决策才保留即时问。

### Step 0a: 苏格拉底澄清需求（前置澄清子环节，需求模糊时启用）

> **定位**：Step 0 的前置子环节——先澄清模糊需求，再进入 Step 0b 清单采集。不是独立阶段，不是清单采集的替代。
>
> **与 P-前置采集原则的关系**：苏格拉底澄清是 P-前置采集原则的**前置子环节**。需求模糊先走苏格拉底澄清，澄清后再批量采集清单字段（Step 0b）。需求明确（续作/增量/config 已填）直接跳到 Step 0b。

#### 触发判据（什么时候启用）

| 场景 | 启用苏格拉底澄清？ | 理由 |
|---|:-:|---|
| 首次做新目标 / 新芯片 / 新领域 | ✅ 启用 | 真实目标/成功标准/边界未明，清单会漏 |
| 用户一句话描述需求（如"帮我适配 Hi3516CV610"） | ✅ 启用 | 信息过少，需递进追问揭示隐藏约束 |
| 缺关键约束 / 目标看似矛盾 | ✅ 启用 | 矛盾需追问优先级，约束需追问具体 |
| 续作 / 增量 / config 已填 / 需求明确 | ❌ 跳过，直接 Step 0b 清单采集 | 需求已清晰，追问烦用户 |

> **实测教训**：实测中途才知道"专家说烧出来必须 223k""XTS 要 426 分"——这些成功标准/约束若在 kickoff 苏格拉底追问出来，能少走大量弯路（避免 SDK 不全硬绕标准构建、避免 XTS 分数不达标返工）。模糊需求不澄清直接清单采集，清单字段值会基于错误假设填写。

#### 追问 5 维度（基于回答递进，不是一次抛 5 个问题）

> **苏格拉底式 = 基于用户回答递进追问**，每轮聚焦回答中模糊/矛盾/缺失的点。不是一次列 5 个问题（那又变清单）。

1. **真实目标** — 为什么做？量产 / 学习 / 交付某项目 / 验证可行性？（"适配某芯片"是表面需求，真实目标可能是"交付某客户项目需烧录件可用"）
2. **成功标准** — 什么算"通过"？
   - OH-Lite 举例：能跑就行 / 量产级稳定性 / XTS 多少分 / 烧录件大小精确值（如 223k）/ 交付截止日期
3. **隐藏约束** — 时间 / 资源 / 已有代码 / 必须兼容的东西 / 不能动的部分
   - OH-Lite 举例：SDK 是否完整 / 服务器已有代码 / 必须兼容某版本 uboot / 密钥/DDR 颗粒等厂商资产
4. **矛盾优先级** — 性能 vs 内存 vs 时间 vs 成本，冲突时谁让？
   - OH-Lite 举例：内存紧但又要全功能 / 时间紧但要求 XTS 高分 / SDK 不全但要求标准构建产出
5. **边界** — 做什么不做什么？哪些显式排除？
   - OH-Lite 举例：OTA / 量产工具链 / 功耗调优 / 安全启动签名 / 多板适配 不做

#### 追问方式

- **基于用户回答递进**：每轮追问聚焦上一轮回答中模糊/矛盾/缺失的点，不是预设问题序列
- **模糊词触发追问**：用户回答出现"可能""大概""应该""差不多"等模糊词 → 追问具体（量化 / 时间点 / 具体值）
  - 如"应该要过 XTS" → 追问"过多少分？哪个套件？交付前还是交付后？"
- **矛盾触发追问**：用户目标间看似矛盾 → 追问优先级，让用户显式排序
  - 如"时间紧" + "要标准构建产出"（SDK 不全标准构建跑不了）→ 追问"是补全 SDK 还是接受非标准构建？哪个优先？"
- **缺失触发追问**：5 维度中某维度用户完全没提 → 视情况追问（按对真实目标的影响判断要不要问，不机械补齐）

#### 产出

- **澄清后的需求摘要**：真实目标 + 成功标准（量化）+ 关键约束 + 矛盾优先级排序 + 边界（含显式排除项）
- **落盘（两个文件，职责分工）**：① 结构化配置（`target.*` / `workflow.*` / `intake.*` / `phases.*` / `experience.*`）落 `workflow_config.yaml`，作为运行时机器事实源；② A1-A7 的理由和对账记录落 `DECISIONS.md`，仅供人类审核，不作为运行时配置。两者互补不互替，下游门控必须能从结构化配置读到
- **作为 Step 0b 清单采集输入**：摘要中的目标/约束/优先级 → 派生清单字段值
  - 成功标准（如 XTS 分数 / 烧录件大小）→ `gates.*` 容差 / 验证判据
  - 边界（显式排除项）→ 阶段 `required` 标记 / 裁剪范围
  - 约束（SDK 完整性 / 时间）→ `toolchain.*` / `paths.*` / 迭代策略

#### 禁忌

- ❌ 需求明确时也强行追问——烦用户，违反 P-前置采集"能前置批量问"原则
- ❌ 追问不基于回答递进，变成又一份问题清单——苏格拉底 ≠ 清单，递进追问才是苏格拉底
- ❌ 澄清完不落盘——摘要必须写入 `workflow_config.yaml` 的结构化字段；决策理由再同步到 `DECISIONS.md` 对账，否则下游门控读不到
- ❌ 替代 Step 0b 清单采集——苏格拉底是前置澄清，清单字段采集仍要做（摘要派生字段值，清单补齐剩余字段）

### Step 0b: 前置决策清单采集（P-前置采集原则）

### 能前置采集的决策（工作流开始就问）

> **大白话原则**：每个决策点先说业务内容（用户能看懂的话），再附内部术语括号。向用户提问时用大白话列项，不要直接抛 A1-A6 / partial_reference / greenfield 等内部代号。

| 决策（大白话 + 术语） | 写入字段 | 下游消费 |
|---|---|---|
| 系统类型：L0 IoT 单 bin / L1 小型系统多产物（术语：A2 系统类型 / L0-L1） | `target.system_type` | P2 内核 / P3 驱动框架 / P4 构建 |
| 芯片型号/架构/RAM/Flash | `target.*` | 全流程 |
| vendor/board/product 命名 | `target.vendor/board` | P1 目录 |
| 工具链 mode/path/prefix | `toolchain.*` | P1 Step 2c / GATE-0 4d（调 ohos-dev-cross-toolchain 持久化） |
| 安全模式 secure/non-secure | `intake.security.secure_mode` | P4 Step 4.4 secure build 变体 |
| boot 介质：eMMC / SPI Nor / SPI Nand / SD（术语：boot.medium，值域 `emmc`/`nor`/`spi_nand`/`sd`/`tftp_nfs`——spi_nand 对应 BOOT_MEDIA=spi_nand，与 nor 是两种介质） | `intake.boot.medium` | P4 rootfs 文件系统 + 烧录路由 |
| **SoC 内置 DDR 变体**（如适用，如 Hi3516CV610-10B/-20S/-20G） | 芯片规格（chip-spec；无独立 config 键，走 ohos-dev-soc-spec-parse 提取，烧录链消费见 `burn.package.boot_chain.required_inputs`） | P4 reg_info/xlsm 选择 |
| 外设范围（最小集/全量/带屏） | `intake.peripherals.scope` | P3 驱动范围 + 是否带 display |
| 归档路径 | `intake.paths.archive_dir` | GATE-交付（预录就不必到时才问） |
| 内核变体（LiteOS-A/Linux） | `intake.kernel_variant` | P2 L1-DIFF 分支 |
| **rootfs/烧录件版本号规则** | `burn.version_rule` | P4 Step 4.5 写 `/etc/rootfs_version` + 诊断侧 Step 2.3 核对 |
| **OH 仓里已有这颗芯片的半成品骨架吗？复用补全 / 从零生成**（术语：target profile `source_strategy` 适配模式 / adapted=复用补全 / greenfield=从零生成 / vendor=用厂商参考） | target profile `source_strategy` + profile 路径写入 `target.profile`（`{{ASSET_ROOT}}/workflow/target-profiles/`，选定值随 profile 记录进 session manifest） | 全流程（决定 P1 起点是核对既有骨架还是从零建目录） |
| **经验积累模式**：用完后要不要把本次经验回填进工作流？（术语：experience.accumulation） | `experience.accumulation` | 各阶段收尾时消费（manual / auto / off，见下方"经验积累模式采集"节） |

### 默认交付目标（除非用户明确缩小范围）

工作流默认目标是**完整可烧录镜像**。Phase 1 必须先做完整性预检，不能先生成一个
partial package 再在 P4 才发现缺件。只有用户明确要求“仅验证 kernel/rootfs”时，才将
`intake.deliverable.goal` 改为 `kernel-rootfs-only`，并在验证清单中记录该例外。

可向用户询问烧录形式和是否由工作流执行烧录；用户跳过时仍必须生成完整包，烧录动作
标记为 `USER_EXECUTED` 或 `SKIPPED_USER`，不能降低镜像闭合要求：

- 烧录形式：分区烧录、整包烧录或用户指定格式；
- （可选）烧录工具、版本、连接方式和授权。未提供时记为 `USER_EXECUTED`，不阻断构建。

不要向用户询问内部实现策略（例如 `sdk_linux` 复用/greenfield）或具体 Kconfig 宏名。
这些由工作流根据来源审计和后续阶段结果决定。

### ⚠️ boot.medium 必须确认，不能假设（实测 SPI 重定向教训）
实测案例：假设 boot.medium=SPI Nor，实际板子是 SPI Nand（DMEB demo 板默认 SPI Nand，没贴 SPI Nor 芯片）→ 烧录报 `getinfo spi → no find spi` + `Invalid spi flash block size`，整个 SPI Nor 包白做。`boot.medium` 是烧录包的根基（决定 rootfs 文件系统 ext4/jffs2/ubifs + env + 烧录页签 + defconfig），错了全盘错。**必须确认，不能假设，不能留"未验证"烧时候再炸。**

#### 调查路径（用户不清楚时，按顺序走，不是直接问用户）

> **实测教训**：用户不清楚 boot.medium / DDR 变体时，工作流此前只列"问用户 / 硬件检测 / 查文档"三选一，没给具体可执行的调查路径。执行者在 SDK 里找 .xlsm 撞墙（.xlsm 在参考仓 boards/dmeb 不在 SDK），被迫问用户。先调查再问用户，问的时候带上已查到的线索。

**用户不清楚 boot.medium 时，按顺序调查**：
1. **查芯片丝印 / DMEB demo 板使用指南**：参考仓 `boards/dmeb` 的 demo 指南通常明示默认介质（如 Hi3516CV610-DMEB 默认 SPI Nand Flash）。先查本地参考仓再联网检索（宿主 WebSearch 或等价物）。
2. **上板子跑 `getinfo spi/nand/mmc`**（若板子已上电且有 uboot 串口）：uboot 命令行直接 `getinfo spi` / `getinfo nand` / `getinfo mmc`，能识别的介质就是当前 boot 介质。SSH 上板子或串口连。
3. **查 BOOT_SEL 拨码**：原理图 / 板子丝印 / demo 板使用指南会标拨码位置对应的 boot 介质。
4. **调查后仍不确定才停下问用户**（带上查到的线索，如"参考仓 boards/dmeb 指南写默认 SPI Nand，但 OH 仓 config.gni 写 emmc，需确认用哪个"）。

**确认来源（任一）**：
1. **问用户**：板子 boot 介质是什么（eMMC / SPI Nor / SPI Nand / SD）—— 调查后仍不确定才问，问时带线索
2. **硬件检测**：板上现有 uboot 的 `getinfo spi/nand/mmc` 输出 / BOOT_SEL 拨码 / 原理图
3. **查参考仓/官方文档**：demo 板使用指南通常写明默认介质（如 Hi3516CV610-DMEB 默认 SPI Nand Flash）—— 联网检索查官方文档/社区，或查本地参考仓；联网检索失败则向用户说明失败表现并问有无其他搜法（见 skill 知识检索降级链兜底）

### ⚠️ SDK 环境必须完整（L0 + L1 通用，专家结论）
**专家结论：烧录镜像必须从 SDK 编译生成 + SDK 不全必须问用户提供完整 SDK + 同一 SDK 版本标准编译应一致**——L0（Mini/Hi3861）+ L1（hi3516cv610）都适用。

实测案例（L1）：服务器 SDK 片段不全跑不了标准 `build.sh dmeb all`，被迫 copy image_tool + 手工喂 input 绕过标准 `gslboot_build` → boot_image 与 SDK 标准不一致（~200K vs 223K）→ 烧到 100% `Uncompress Fail! err=0x81`。

实测案例（L1）：P1 Step 0b 自查时只查了服务端裸 SDK 无 osdrv，但没识别"boot_image 构建需 vendor 构建系统（gslboot_build）"这一完整性维度，导致 P4 GATE-V12 才暴露硬阻塞（vendor 构建系统不在 SDK 内）。**实测教训：SDK 完整性核查不能只查 drivers/OSAL/libs，还要核查 boot_image 构建所需部件，不全则显式声明缺口 + 问用户提供完整 vendor 构建系统，别等 P4 才发现。**

#### vendor SDK 组成与两棵内核关系（Step 0 前置认知，适配者必懂）

> **为什么有这一节**：适配者一开始就得懂 vendor SDK 到底给什么、OH 仓内核与 vendor SDK 内核是什么关系——不能靠 brief 喂（brief 只给任务不给 SDK 结构）、不能撞到 P2/P3 才发现"两棵内核"含义。实测教训：曾有执行者到 P2 才搞清"vendor SDK `third_party/linux` 是参考源不是编译目标、OH 仓 `kernel/linux/linux-5.10` 才是 hb build 的对象"，前面对"两棵内核"关系没概念导致 P2 路径选择反复。**Step 0 采集前置决策时就把 vendor SDK 组成 + 两棵内核关系摸清，写入 `chip-basics.yaml` 的 `sdk.composition` 段，下游 P2/P3 直接消费。**

**vendor SDK = 厂家提供的芯片材料包**，组成（L1 Linux 类，如 hi3516cv610）：

| 部件 | 路径 | 用途 |
|---|---|---|
| `soc/` | soc/{config,drivers,include,libs,platform} | HAL/OSAL/libs，P3 port 进 OH userspace |
| `third_party/linux` | third_party/linux/linux-5.10.y | vendor 适配好的 Linux 内核（含芯片内核驱动 + defconfig + DTS）——**参考源，不直接编译** |
| `third_party/u-boot` | third_party/u-boot/u-boot-2022.07 | U-Boot 源（env 分区 + 烧录引导） |
| `boards/dmeb` | boards/dmeb/{Makefile,dts,tools/pc/boot_tools} | boot 构建系统（gslboot_build + image_tool + .xlsm）+ 板级 DTS |
| `kernel-patches/` | kernel-patches/ | 内核 patch |
| `busybox`/`gzip` | third_party/{busybox,gzip} | rootfs 工具链 |

**两棵 Linux 内核（L1-Linux 必懂）**：

| 内核 | 位置 | 集成度 | 芯片驱动 | 角色 |
|---|---|---|---|---|
| ① OH 仓内核 | `kernel/linux/linux-5.10`（OH code 仓） | OH-integrated（有 hilog/HDF/binder 集成） | chip-empty（greenfield，无 cv610 驱动） | **hb build 编这棵，板上跑的** |
| ② vendor SDK 内核 | `third_party/linux/linux-5.10.y`（vendor SDK） | 非 OH-integrated（无 hilog） | chip-adapted（vendor 已适配，芯片驱动都在） | **参考源，port 驱动进 OH 仓内核** |

**适配 = integration，不是 rewrite**：
- **不重写驱动**——vendor 已写好芯片驱动（没芯片文档写不了），适配工作是 **port**（把 vendor SDK 芯片驱动搬进 OH 仓内核 + HAL 集成进 OH userspace）。
- **port 内容**：vendor defconfig → OH 仓 defconfig（追加 OH 必需 config 块）+ vendor DTS → OH 仓 DTS（重命名 + include 修正）+ vendor 内核驱动源码 → OH 仓内核对应目录（或 sdk_linux/drv）。
- **板级 tweak 不算写驱动**：如 SPI Nand 颗粒 ID 不在 vendor fmc_ids 表 → 加 ID 表条目（实测 DS35Q1GB-IB 教训，见 P2/GATE-B+ 的 SPI Nand 颗粒 ID 覆盖核查）。这是配置补充，不是新写驱动。

**按芯片类型分支（不是所有 L1 都有 vendor Linux 内核树）**：

| 芯片类型 | vendor SDK Linux 内核树 | vendor SDK 提供 | 适配做法 |
|---|---|---|---|
| **L1-Linux-greenfield**（如 hi3516cv610） | ✅ 有（`third_party/linux`） | HAL + Linux 内核树 + U-Boot + boot 构建系统 | port vendor 驱动进 OH 仓内核 |
| **L0/LiteOS-A**（如 hi3861） | ❌ 无（内核是 LiteOS-M/A，OH 仓自带） | 只给 HAL（IoT HAL/HDF adapter） | HAL 集成进 OH userspace，内核走 OH 仓 |
| **OH 上游已有 Linux 芯片**（partial_reference） | ✅ 有，但 OH 仓已含 | HAL + 可能已 port 的驱动 | 复用补全 OH 仓既有骨架，不重复 port |

> **与 SDK 完整性核查的关系**：摸清 vendor SDK 组成（有什么），再核查完整性（缺什么）。`sdk.composition` 字段是核查清单的输入——先列出 SDK 应有什么，再逐项核查缺不缺。

#### SDK 完整性核查清单（Step 0 / GATE-0 前置硬步）

**不只查 SDK 有 drivers/OSAL/libs，还要核查 boot_image 构建所需部件是否在 SDK 内或服务端可得。逐项核查，任一缺口显式声明 + 问用户提供**：

| 核查项 | L1（hi3516cv610 类） | L0（Hi3861 类） | 缺口处理 |
|---|---|---|---|
| **基础构建链** | SDK 有 drivers/OSAL/libs + soc/ + third_party/ + build/ + 顶层 Makefile | 完整 OH 源码树（build/ + kernel/liteos_m/ + device/ + vendor/）+ Hi3861 特有工具 | 缺 → 问用户给完整 SDK |
| **osdrv（OS 驱动层）** | SDK 含 osdrv/（U-Boot 源 + 驱动交叉编译） | L0 通常无独立 osdrv（走 OH 源码树） | L1 缺 osdrv → 标缺口，问用户 |
| **U-Boot 源** | SDK 含 U-Boot 源码（或参考仓 boards/dmeb 含 uboot） | L0 走 flashboot（非 U-Boot） | L1 缺 → env 分区也生不了，标硬阻塞 |
| **gslboot_build（boot_image 构建脚本）** | SDK 含 gslboot_build / build.sh dmeb all 能产出 boot_image | L0 不适用（无 boot_image） | L1 缺 → boot_image 构建硬阻塞，问用户给完整 vendor 构建系统 |
| **.xlsm（DDR 配置表）** | 参考仓 `boards/dmeb/tools/pc/boot_tools/` 含 .xlsm 文件（**不在 SDK soc/ 目录**，实测踩坑点） | L0 不适用 | L1 缺 → 走 DDR 变体调查路径；仍缺问用户 |
| **boards/dmeb（板级参考包）** | 参考仓有 boards/dmeb/（demo 板配置 + boot_tools + 使用指南） | L0 对应 boards/ 下板级包 | 缺 → 问用户给板级参考包或换板 |
| **OH 仓自有 sdk_linux** | OH 仓 `device/soc/{vendor}/{soc}/sdk_linux/` 自有完整 sdk_linux（BUILD.gn + build.sh + config） | L0 走 device/soc/{vendor}/{soc}/ 下的 adapter | OH 仓缺 → 标缺口，问用户给完整 SDK 或换路径 |

**核查动作**：
1. **Step 0b 自查时全扫**：SSH 上服务端 / 本地 ls，逐项核查上表。不只查"SDK 有没有"，还要查"boot_image 构建链能不能跑通"。
2. **缺口显式声明**：任一缺口写入 `workflow_config.yaml` 的 `sdk.gaps` 段（列表），不藏着。
3. **缺口处理**：缺口 → 问用户提供完整 vendor 构建系统（osdrv + U-Boot 源 + gslboot_build + .xlsm + boards/dmeb）。**不能手工拼 input 绕过标准构建**（实测教训）。
4. **按交付范围分流**：缺口不必阻塞 `kernel-rootfs-only` 适配，但若目标是
   `full-burnable-image`（默认完整 L1 可烧录镜像），缺口必须在 P1 直接将 image path 标为
   `BLOCKED_VENDOR_SDK`，不得让 P2/P3/P4 继续假定可生成 `boot_image.bin`。
   缺口必须在 Step 0b 显式声明，不能等 P4 才首次发现。

**SDK 环境必须完整到能跑标准 build**：
1. **完整性标准（L1）**：参考仓 + submodule 齐全（顶层 Makefile + soc/ + third_party/ + build/ + osdrv/ + U-Boot 源 + gslboot_build + .xlsm + boards/dmeb），`cd build && ./build.sh dmeb all debug pack`（或 `make ... gslboot_build`）能跑通产出标准 boot_image。
2. **完整性标准（L0）**：完整 OpenHarmony 源码树（build/ + kernel/liteos_m/ + device/ + vendor/）+ Hi3861 特有工具齐全，`hb set`（选 `wifiiot_hispark_pegasus`）→ `hb build -f` 能跑通产出 `Hi3861_wifiiot_app_burn.bin`。
3. **片段不全 → 问用户给完整 SDK**：向用户索取完整 SDK，或 gitcode/gitee 克隆完整参考仓 + `git submodule update --init --recursive`。**不能手工拼 input 绕过标准构建**。
4. **验证（同一 SDK 版本一致性）**：编出的镜像大小/md5 与 SDK 标准一致（L1: Hi3516CV610 debug 标准 227840B；L0: `Hi3861_wifiiot_app_burn.bin` 与同版本标准产出一致）——不一致说明构建流程错了。
5. 详见 `04-build-verify` Step 4.4「烧录镜像构建通用原则」+ `skills/ohos-ci-lite-deploy-burn`「烧录镜像构建通用原则」。

### ⚠️ SoC 内置 DDR 变体必须确认（裸烧 reg_info 前置）
内置 DDR SoC（如 Hi3516CV610）同型号分多变体（-10B=DDR2 64MB / -20S/-20G=DDR3 128MB / -00S/-00G=外置 DDR3），变体决定 bootrom 阶段的 `.xlsm` → `reg_info.bin`。错配 → 烧到 100% 但 uboot 起不来。**DDR 变体属于芯片规格提取，走 `ohos-dev-soc-spec-parse` skill**：
1. **调用 ohos-dev-soc-spec-parse 单点查询**："这块板子的 SoC 变体该用哪个 xlsm / DDR 参数是什么" → 命中 `ddr-variant-guide.md` 变体表直接回答（变体 → DDR 类型/容量/封装/速率 → xlsm → reg_info 生成命令）
2. **变体后缀来源**：芯片丝印/型号后缀（-10B/-20S 等）→ 板级配置/demo 板使用指南 → 原理图/封装（QFN=内置 DDR，TFBGA=外置）
3. ohos-dev-soc-spec-parse 未覆盖该型号 → **先试联网搜**（不预设搜不到）：① ohos-dev-kernel-source-query 查开源 SDK/device_soc 仓（找 boot_tools/.xlsm 文件名或产品简介相关文件，覆盖范围以实际能查的开源仓库为准）② 联网检索（WebSearch 或等价物）查厂商产品简介「型号配置差异」表 / DDR 规格；联网搜不到 → 问用户（芯片丝印/提供产品简介）

#### 调查路径（用户不清楚 DDR 变体时，按顺序走，不是直接问用户）

> **实测教训**：执行者在 SDK 里找 .xlsm 撞墙——.xlsm 在参考仓 `boards/dmeb/tools/pc/boot_tools/` 不在 SDK soc 目录。调查路径要明确指引去哪找，别让执行者在错误位置打转。

**用户不清楚 DDR 变体时，按顺序调查**：
1. **查芯片丝印后缀**：芯片表面丝印的型号后缀（-10B / -20S / -20G / -00S / -00G）直接对应变体。丝印是最权威来源。
2. **搜参考仓 `boards/dmeb/tools/pc/boot_tools/` 找 `.xlsm` 文件名**：.xlsm 文件名通常含变体后缀 + DDR 类型/容量（如 `Hi3516CV610-DMEB_4L_DDR3_2133M_128MB_16bit-A7_950M_QFN.xlsm`）。
   - **注意**：.xlsm 在参考仓 `boards/dmeb` 目录，**不在 SDK 的 soc/ 目录**（实测踩坑点）。SDK soc/ 通常只有 config/drivers/include/libs/platform，不含 boot_tools。
3. **查 demo 板使用指南**：参考仓 `boards/dmeb` 的 demo 指南通常标默认 DDR 变体。
4. **调查后仍不确定才停下问用户**（带上查到的线索，如"参考仓 boards/dmeb 有 `...DDR3_128MB...QFN.xlsm`，推断是 -20S/-20G 变体，需用户确认芯片丝印"）。

> 这条是 GATE-B+ "未验证项必须烧前解决"的典型：boot.medium 不准 → 烧必炸。准了再往下做 rootfs/env/defconfig。

### ⚠️ 版本号规则前置采集（通用，与 P4/诊断侧联动）
rootfs/烧录件版本号规则（如 `{chip}_{date}_{iter}` / `{project}-{iter}-{date}`）在工作流开始就采集，写入 `workflow_config.yaml` 的 `burn.version_rule`。下游 P4 Step 4.5 消费该规则写 `/etc/rootfs_version`（版本号+构建时间+关键改动），诊断侧（`skills/ohos-issue-lite-diagnose` Step 2.3）拿到日志先 grep 版本标记核对。**通用方法**——具体版本号格式由 config 定，不绑特定芯片。多轮迭代调试期才打标记，第一稿一次通过不打。

### 经验积累模式采集（经验积累机制一部分，Step 0b 前置）

> **定位**：经验积累机制的一部分——工作流用完后，把本次适配经验（踩坑、修复、决策依据）回填进工作流的 references / lessons-learned，让工作流越用越个性化。Step 0b 前置采集用户偏好，各阶段收尾时消费。

**问用户**（大白话）：工作流用完后要不要把本次经验回填进工作流？
1. **默认不回填，保持通用**（术语：`manual`）—— 工作流跑完不自动回填，用户觉得有价值的经验手动整理。工作流保持通用，不绑特定项目。
2. **自动回填，越用越个性化**（术语：`auto`）—— 各阶段收尾时自动把踩坑/修复/决策依据写入工作流的 references / lessons-learned，下次跑工作流会带上这些经验。
3. **明确不回填**（术语：`off`）—— 显式声明不回填，跟 manual 的区别是 manual 默认不回填但用户可手动加，off 是显式关闭回填通道（即使阶段收尾有可回填的经验也不写）。

**落盘**：用户选择写入 `workflow_config.yaml` 的 `experience.accumulation` 字段（值：`manual` / `auto` / `off`，默认 `manual`）。

**下游消费**：
- `manual`（默认）：各阶段收尾时不自动回填，仅在用户显式要求时整理经验。
- `auto`：各阶段收尾时自动把本阶段踩坑/修复/决策依据写入工作流 references（如 `references/lessons-learned/{chip}-{phase}.md`），下次跑工作流 load 这些经验。
- `off`：各阶段收尾不回填，即使有可回填的经验也不写。

> **与 GATE-交付 的关系**：经验回填发生在 GATE-交付 之后（工作流跑完、产出件归档后），不是 GATE-交付 的前置。`auto` 模式下 GATE-交付 收尾时触发回填动作。

### 保留即时问的（晚绑定 / 分支太密）
- **L1-Linux 构建路径 A/B**：要试了 B 撞 OH 组件依赖墙才知道走不走 A——保留即时问（撞墙后问用户）
- **内核补丁冲突处理**：扫描后才知道冲不冲突——保留即时
- **DDR 颗粒/密钥等厂商资产**：DDR 变体鉴别走 ohos-dev-soc-spec-parse（见上方 DDR 变体节）；但具体颗粒型号/密钥等需上机或问厂商——保留即时

### 采集方式
- **首选 config**：用户填 `workflow_config.yaml`（或项目根 `{{ASSET_ROOT}}/workflow/workflow_config.template.yaml`），工作流读取即跳过对应询问。`workflow_config.yaml` 是运行时结构化事实源；`DECISIONS.md` 只保存 A1-A7 的人类可读理由和对账记录，不由编排器解析。
- **无 config**：工作流开始时一连串问题批量问（一次问完，不分散到各门控），问完写入 config 持久化
- **信息采集分支太多、实现不合适**的，保留原即时交互式

> 原则（P-前置采集）：能前置采集的决策不留在门控处问。前置采集 ≠ 一次问完所有事——晚绑定的保留即时，但能提前定的别拖到门控。
> **模糊需求先走苏格拉底澄清（Step 0a），再批量采集（Step 0b）**——Step 0a 澄清真实目标/成功标准/约束/优先级/边界，澄清后的需求摘要派生清单字段值，Step 0b 补齐剩余字段。需求明确时跳过 0a 直接 0b。

## P1 可行性核查与 vendor 启动链盘点

创建 device 树之前，先记录目标是否具备：(1) 公开或经授权的板级代码；(2) 可用内核；(3) U-Boot 或等价的 boot 生产者；(4) 镜像构建器和确切的打包命令；(5) 已确认的烧录介质；(6) 硬件或显式的离线验证证据。把用户提供的每个 vendor 件分类为：源码 / 构建输入 / 板级约束 / 工具链 / 二进制 / 仅参考材料。

L1/完整镜像目标必须在盘点中点名 GSL/DDR 训练或寄存器数据、U-Boot、镜像生产者和打包命令。任一私有启动链输入缺失时，设 `burn.package.boot_chain.missing_policy: BLOCKED_VENDOR_SDK`，在 P2/P4 之前停止默认完整镜像路径。内核/rootfs 工作只能作为显式标记的诊断工作继续；不准伪造 `boot_image.bin`，不准把中间包称为完整。

P1 交接（handoff）必须包含 `confirmed`、`unverified`、`blockers`、`artifact_paths`、`completeness` 和 `verification_manifest` 引用。目标无法支撑所请求的验证时，现在就暴露该限制，并询问用户是换目标还是改范围。

## Step 1: 目录规划

### OpenHarmony device 树规范

```
{project_root}/
├── device/
│   ├── board/                           # Board 级 (产品级)
│   │   └── {vendor}/                    #   供应商
│   │       └── {board}/                 #     开发板/产品
│   │           ├── config.json          #     产品配置 (subsystem 清单)
│   │           ├── config.gni           #     板级编译参数
│   │           ├── BUILD.gn             #     板级构建入口
│   │           └── init_configs/        #     初始化配置 (可选)
│   └── soc/                             # SoC 级 (芯片级)
│       └── {company}/                   #   芯片公司
│           └── {soc_model}/             #     芯片型号
│               ├── BUILD.gn             #     SoC 级构建入口
│               ├── {soc_adapter}/       #     SOC Adapter (P2/P3 产出)
│               │   ├── hals/            #       HAL 驱动实现
│               │   ├── kal/             #       KAL 抽象层
│               │   └── hdf_config/      #       HDF 配置 (仅 L1)
│               └── sdk_liteos/          #     SDK (如有, GT 文件)
├── vendor/
│   └── {vendor}/
│       └── {board}/                     # 产品级 vendor 目录 (hals 等)
└── out/                                 # 构建输出 (自动生成)
```

**关键原则**：
- **Board/SoC 分离**：`device/board/{vendor}/{board}/` 是产品视角，`device/soc/{company}/{soc}/` 是芯片视角。同一芯片可以用于多个产品（多个 board 目录）。
- **实测案例**：Hi3861V100 → `device/board/hisilicon/hispark_pegasus/` + `device/soc/hisilicon/hi3861v100/`
- 目录创建后必须能被 `./build.sh --product-name {product}` 发现

### 用户交互点

如果用户未提供 `{vendor}` / `{board_name}`，需询问：

> **请确认以下信息：**
> - 芯片供应商名称（用于目录路径）: `__________`
> - 开发板/产品名称: `__________`
> - 或使用默认值: vendor=`{vendor_from_chip}`, board=`{board_from_chip}`

### Step 1b: 缺失板厂包补齐（上网拉取）

如果芯片的 board/vendor/product config 在本仓不存在（绿场芯片，或本仓只收录了 SoC 层），工作流上 OH 公开仓搜并拉取缺失的板厂包：

1. **判断缺什么**：检查 `device/board/{vendor}/{board}/`、`vendor/{vendor}/{board}/`、productdefine 条目哪些缺失。SoC 层在但 board/vendor 缺 = 典型场景（如本仓有 device/soc/rockchip/rk2206 但无 device/board/rockchip）。
2. **上网搜**：用 `ohos-dev-kernel-source-query` skill 在 GitCode/GitHub 的 OpenHarmony 镜像仓搜板厂包（`device_board_{vendor}`、`vendor_{vendor}` 仓），列目录定位板级文件（config.json/config.gni/BUILD.gn/HCS/BSP）。
3. **拉取**：GitCode API（免认证，见 ohos-dev-kernel-source-query §GitCode获取）或 raw URL 拉缺失的 board/vendor config + BSP + HDF 配置。
4. **接入**：放到本仓对应路径，确保 `./build.sh --product-name {product}` 能发现新产品。

> **不泄漏 GT**：拉的是板厂包（device/board、vendor 级构建依赖），不是 SoC adapter（GT 在 `device/soc/.../adapter`，单独挖空）。板厂包是构建依赖，不是适配答案。
> **搜索 vs 想象（角色原则）**：板名/产品名/板厂包路径等候选**必须来自搜索结果**（公开仓里实际存在的目录/配置），**不要执行者凭知识或想象列候选**。工作流通过 `ohos-dev-kernel-source-query` 确定性搜索，执行者整理"查到了这些选项"→ 转给用户或自行在真实结果中定。工具链等同理（先查仓内 prebuilt + 公开仓，再问）。
> **用户决策点**：若板厂包也不在 OH 公开仓（冷门板），停下来问用户是否提供板厂包路径或换板。

---

## Step 2: 工具链安装

### 2a: hb 安装与修复

```bash
# 标准 OH 安装方式:
cd {oh_root}/build && python3 -m pip install -e ./hb

# 验证:
PYTHONPATH={oh_root}/build python3 -c "import hb; print(hb.__version__)"
```

**实测经验 — hb 常见问题与修复**:

| 问题 | 现象 | 修复方式 | 类别 |
|------|------|---------|------|
| `ModuleNotFoundError: No module named 'hb'` | pip install 未生效或路径错误 | `pip install -e {oh_root}/build/hb` 并确认 PYTHONPATH | 环境 |
| `ModuleNotFoundError: No module named 'util'` 或子模块 | hb 的 util 包缺少 `__init__.py` | 在每个缺失 `__init__.py` 的子目录下创建空 `__init__.py` | **Framework Patch** |
| `ImportError: cannot import name 'X' from 'Y'` | 绝对导入在包内失效 | 将 `from X import Y` 改为 `from .X import Y` (相对导入) | **Framework Patch** (16 files) |

> **实测数据**: hb Python 修复涉及 ~16 个文件的 import 路径修正。这是 **framework patch**（修改构建框架代码），不是 GT 修改。记录但通常不需要用户逐个批准。

### 2b: gn / ninja 验证

```bash
gn --version    # 期望: v2026+ (OH prebuilts)
ninja --version # 期望: v1.10.1+
```

**⚠️ 实测发现**: OH 构建 **必须** 使用 `ninja -w dupbuild=warn`（OH 有重复 NOTICE 文件规则，默认 strict 模式会报错）。此参数由 hb 内部调用时注入，手动调用 ninja 时需注意。

### 2c: 交叉编译工具链

**先读 `workflow_config.yaml` 的 `toolchain` 配置 + 主动问用户用哪种**（不只缺失才问，见 `ohos-dev-cross-toolchain` skill）：

| mode | 做法 |
|---|---|
| `auto` | auto-detect PATH 里的 `{prefix}gcc`（默认） |
| `user` | 用 config 的 `path`/`prefix`，不 auto-detect |
| `wrapper` | 用 config 的 `wrapper` 脚本（注入 flag） |
| `docker` | 用 config 的 `docker_image` 容器 |

config 没填或 mode=auto 时，按下面来源 auto-detect，缺失则交互问用户。

> **⚠️ 强制（GATE-0 前置硬步）**：即使工具链已知（briefing 提供或用户告知），也**必须**调 `ohos-dev-cross-toolchain` skill 走完配置流程：① 问用户确认 mode + path + prefix → ② 写入 `workflow_config.yaml` 的 `toolchain:` 块 → ③ 校验（gcc --version + 测试编译）。**不能因"已知"跳过**——确认 + 持久化记录 + 校验是 GATE-0 4d 的前置，跳过则 GATE-0 不通过。

**三种来源选项**（mode=auto 时）:

| 来源 | 适用场景 | 实测选用 |
|------|---------|------------|
| **Prebuilt 二进制包** | 快速上手，推荐首选 | ✅ GCC 13.2.0 prebuilt |
| **源码编译 (riscv-gnu-toolchain)** | 需要特定版本/patch | 尝试后放弃 (耗时太长) |
| **Vendor SDK 自带** | 芯片厂商提供 | Hi3861V100 有自带 GCC 7.3.0 (不可用) |
| **Wrapper Script** | 注入额外 flag/重定向二进制 | ✅ **最终方案**: wrapper v3 注入 zicsr |

**工具链验证命令**:
```bash
which {toolchain_prefix}gcc 2>/dev/null && echo "FOUND"
{toolchain_prefix}gcc --version 2>/dev/null | head -1
# 测试编译:
echo 'int main(){return 0;}' | {toolchain_prefix}gcc -x c - -o /dev/null
```

**⚠️ 实测关键发现 — 工具链可能缺少指令集扩展**:
- Hi3861V100 flashboot 启动代码使用 CSR 指令 (`csrr`/`csrw`)，需要 `zicsr` 扩展
- Prebuilt GCC 13.2.0 默认不暴露 zicsr 到 march 字符串
- **解法**: Wrapper Script 在编译时动态注入 `-march=rv32imac_zicsr` (见 compiler_fix_playbook §4)

**用户交互点 — 工具链缺失时**:
> **交叉编译工具链未检测到。**
> 目标芯片 **{chip_model}** ({arch}) 需要 **{prefix}gcc** 工具链。
> - [ ] 提供路径: `__________`
> - [ ] 自动安装 (工作流执行安装脚本)
> - [ ] 跳过 L5 (本次仅源码级验证)
> - [ ] 使用 Wrapper 包装现有二进制

### 2d: 源码同步 (如需要)

```bash
# OpenHarmony 标准方式:
repo init -u {manifest_url} -b {branch} -m {default.xml}
repo sync -j$(nproc)
```

> 如果源码已在远程服务器上（如实测场景），此步跳过。

---

## Step 3: 配置预适配

### 3.1 config.json（产品配置）

```json
{
  "product_name": "{board_name}",
  "product_company": "{vendor}",
  "device_company": "{company}",
  "product_device": "{board_name}",
  "version": "3.0",
  "type": "small",            // "mini"(L0 轻量) | "small"(L1 小型) | "standard"(L2 标准)
  "ohos_version": "OpenHarmony 4.0",
  "board": "{board_name}",
  "kernel_type": "{kernel}",   // "liteos_m" | "liteos_a"
  "subsystems": [
    { "name": "kernel", "syscomp": [...] },
    { "name": "hiviewdfx", "syscomp": [...] },
    // ... 基础子系统
  ]
}
```

**关键**: `type` 和 `kernel_type` 决定整条下游路径 (L0 vs L1)。一旦选定，P2/P3/P4 全部行为都会据此分支。

### 3.2 config.gni（板级编译参数）

```gni
board_name = "{board_name}"
product_name = "{board_name}"
device_company = "{company}"
device_company_path = "//device/company/{company}"
target_os = "ohos"
target_cpu = "{arch}"         // "arm" | "riscv32" | "riscv64"
enable_ohos_sdk_ut = false
}
```

### 3.3 BUILD.gn（板级构建入口）

```gn
group("{board_name}_group") {
  public_configs = [ ":{board_name}_config" ]
  if (board_cpu != "") {
    public_deps = [ "//build/oem_config:{board_name}" ]
  }
}

config("{board_name}_config") {
  # 板级通用 defines
  defines = [
    "BOARD_{BOARD_NAME_UPPER}=1",
  ]
}
```

### 3.4 ./build.sh --product-name {product} → components.json 自动生成

```bash
./build.sh --product-name {product} -p {product_path} -t {product_type}
```

**⚠️ 实测关键发现 (F-003)**: `components.json` **不是手动创建的文件**。它是 `./build.sh --product-name {product}` 执行后的**动态生成产物**，位于:
```
{out_dir}/build_configs/parts_info/components.json
```
- 首次构建前该文件不存在是正常的
- `./build.sh --product-name {product}` 会自动生成它
- 如果被删除，重新执行 `./build.sh --product-name {product}` 即可恢复

---

## Step 4: GATE-0 环境健康检查 ★ 实测证明必需

> **实测核心教训**: 编译失败的 **50%+ 是环境问题而非代码问题**。
> P1 结束时的 GATE-0 是首次确认，P4 编译前会复检同样 4 个子门控。

### 4a: hb 模块可导入？

```bash
PYTHONPATH={oh_root}/build python3 -c "import hb; print('hb OK, ver:', hb.__version__)"
```

| 结果 | 含义 | 修复 |
|------|------|------|
| ✅ OK | hb 可用 | 无需操作 |
| ❌ ModuleNotFoundError | 包结构损坏 | `pip install -e` + 补 `__init__.py` (见 Step 2a) |
| ❌ ImportError | import path 错误 | 修复 util 文件的 from/import 为相对导入 |

### 4b: gn / ninja 二进制可用？

```bash
gn --version && ninja --version
```

| 结果 | 含义 | 修复 |
|------|------|------|
| ✅ 两者都有正确版本 | 就绪 | 无需操作 |
| ❌ gn 缺失 | 从 prebuilts 或源码获取 | 见 Step 2b |
| ❌ ninja 缺失 | 通常随 gn 一起安装 | 同上 |

### 4c: components.json 存在？

```bash
ls -la {out_dir}/build_configs/parts_info/components.json 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

| 结果 | 含义 | 修复 |
|------|------|------|
| ✅ EXISTS | 已有产物缓存 (之前 ./build.sh --product-name {product} 过) | 无需操作 |
| ❌ MISSING | 首次构建 / 缓存清理 | 执行 `./build.sh --product-name {product} -p {product} -t {type}` |

### 4d: 工具链可用？

> **前置**：`ohos-dev-cross-toolchain` skill 已运行——`workflow_config.yaml` 的 `toolchain:` 块已填（mode + path/prefix）+ 校验通过。若未运行，回 Step 2c 完成（不能跳过，即使工具链已知）。

```bash
which {toolchain_prefix}gcc 2>/dev/null && echo "FOUND"
{toolchain_prefix}gcc --version 2>/dev/null | head -1
echo 'int main(){return 0;}' | {toolchain_prefix}gcc -x c - -o /dev/null 2>&1 && echo "COMPILES OK"
```

| 结果 | 含义 | 下一步 |
|------|------|--------|
| ✅ FOUND + 可编译 | 工具链就绪 | → **必须进入 4d-TC 全扫**+ 进入 Step 5 |
| ✅ FOUND 但编译失败 | 可能缺 sysroot/库 | 检查 `--sysroot` 参数 |
| ❌ NOT FOUND | 工具链未安装 | → **用户交互点** (见 Step 2c) |

#### ★ 工具链路径一次性全扫（GATE-0 4d 子门控，跨阶段补扫）

> **实测教训（跨阶段补扫）**：P1 GATE-0 只查改了 `config.gni` + `sdk_linux/build.sh` 两处 TC_DIR，P2 接入 `kernel.mk` 时又发现 L38 `ifeq ($(KERNEL_ARCH), arm)` 硬编码 `gcc-linaro-7.5.0-arm-linux-gnueabi`（KERNEL_ARCH 分支 linaro gnueabi，不支持板级覆盖），cv610 需 openeuler musl ARM32。**工具链路径冲突跨阶段漏到 P2 才补**，浪费一轮内核移植。全扫清单不能只扫 P1 阶段的 config.gni/build.sh/kernel.mk，**必须全扫所有含 TC_DIR/工具链路径的文件，且 P2/P3 接入新 build 脚本时也纳入扫（不只 P1/P4）**。

**全扫命令（P1 GATE-0 4d 必跑，不止查 `{toolchain_prefix}gcc` 是否存在）**：

```bash
# 一次性扫所有含 TC_DIR / 工具链路径的 build 脚本（排除 .bak + /out/ 生成产物）
grep -rnE "cv610_tc|TC_DIR|openeuler_gcc_arm32le|linaro.*gnueabi|/opt/[a-z_]+gcc" "$OHROOT" \
  --include="*.sh" --include="*.mk" --include="*.gni" --include="*.gn" \
  --include="*.py" --include="Makefile*" --include="*.mak" \
  | grep -vE "\.bak|/out/"
```

**扫描范围必须覆盖（跨阶段补扫）**：

| 文件 | 接入阶段 | 实测教训点 |
|---|---|---|
| `device/soc/*/sdk_linux/config.gni` + `device/soc/*/sdk_linux/build.sh` | P1 | 基础清单——P1 查改两处 |
| `device/board/*/linux/config.gni` | P1 | 基础清单——板级工具链配置 |
| `kernel/linux/build/kernel.mk` | **P2 接入** | **新增**——L38 KERNEL_ARCH 分支硬编码 linaro gnueabi，不支持板级覆盖（实测漏扫点） |
| `kernel_module_build.sh` | **P2 接入** | **新增**——kernel.mk 覆盖块的环境变量在此设（实测漏扫点） |
| `device/soc/*/sdk_linux/BUILD.gn` | **P2/P3 接入** | **新增**——sdk_linux 构建入口，可能含工具链路径引用 |
| **P2/P3 接入的任何新 build 脚本** | P2/P3 | **跨阶段补扫规则**——P2 内核移植 / P3 驱动开发接入新 build 脚本（sdk_linux/BUILD.gn、driver BUILD.gn、HCS 构建脚本等）时，必须对该新文件跑一次 TC_DIR/工具链路径扫描，不只 P1/P4 扫 |

**扫到路径后的处理（决策分级：技术执行→自决，不转发用户）**：
- 所有 TC_DIR / 工具链路径**必须指向 `workflow_config.yaml.toolchain.path`**（briefing/用户确认的实际工具链路径，如 `/opt/openeuler_gcc_arm32le-musl/bin`）
- 任一文件指向不一致的旧路径或硬编码默认值（如 `gcc-linaro-7.5.0-arm-linux-gnueabi`）→ **技术执行自决修正**：备份 `.bak.{iter}` → 加环境变量覆盖块（最小侵入，不改默认分支，只在板级环境变量设了时覆盖，见 `04-build-verify` Step F 的 kernel.mk 覆盖块模式）→ `bash -n` 语法验证 → 记录到 PROVENANCE
- 修正后重跑全扫命令确认 `0 残留冲突`（闭环验证）
- **跨阶段补扫**：P2 接入 kernel.mk / kernel_module_build.sh / sdk_linux/BUILD.gn 时，P3 接入驱动 build 脚本时，每个新接入的 build 文件都跑一次全扫，确认无新工具链路径冲突。别等 P4 GATE-0 复检才扫——P2/P3 接入时立即扫，冲突立即修。

| 扫描结果 | 含义 | 动作 |
|---------|------|------|
| 0 处路径冲突（全指向 `toolchain.path` 或无硬编码路径） | ✅ PASS | 进 GATE-0 判定 |
| N 处路径冲突（指向旧/错路径或硬编码默认值） | ⚠️ 技术执行自决修正 | 备份→加覆盖块→语法验证→重扫确认 0 残留 |
| 扫到无法判断的路径变量（如 `$(cross_prefix)` 需运行时展开） | 标记待运行时验证 | 进 GATE-0 判定 + P4 编译时验证 |
| P2/P3 接入新 build 脚本未补扫 | ⚠️ 跨阶段补扫缺失 | 回到接入阶段补扫该文件 |

### GATE-0 判定

| 子门控 | 初始状态 | 实测最终 | 修复动作 |
|--------|:-----------:|:-----------:|---------|
| 4a hb 模块 | ❌ BROKEN | ✅ PASS | pip install-e + __init__.py + import fix (16 files) |
| 4b gn/ninja | ✅ FOUND | ✅ PASS | 无需修复 |
| 4c components.json | ❌ MISSING | ✅ PASS | ./build.sh --product-name {product} auto-generate |
| 4d 工具链 | ❌ NOT INSTALLED | ✅ PASS | prebuilt 13.2 + wrapper v3 (zicsr inject) |
| 4d-TC 工具链路径全扫 | N/A | ⚠️ **缺失** | ★ 新增 + 跨阶段补扫：一次性全扫所有 build 脚本 TC_DIR/工具链路径 + P2/P3 接入新 build 脚本跨阶段补扫（实测教训：kernel.mk + kernel_module_build.sh 漏扫） |

> **全部 4 个环境子门控 PASS 后才进入 Step 5。** 启动链闭合预检另行执行：默认完整镜像目标下，
> 任一必需 producer/input 缺失即记录 `BLOCKED_VENDOR_SDK`，不得把 partial package 作为交付物；
> 只有用户明确选择 `kernel-rootfs-only` 才允许跳过该闭合检查。

---

## Step 5: 信息收集

产出芯片规格初版和**阶段输入清单**，供 P2 (内核移植) 和 P3 (驱动开发) 消费；
P4/P5/P6/P7 后续产生的代码、镜像、测试和诊断结果不得伪造为 P1 输入。

### Phase B 输入与完整镜像前置审计

按目标 profile 列出每项前置输入，并记录 `present` / `missing` / `unverified`、来源分类、
SHA256（可获取时）、版本/commit、许可和用途。L1/Linux 完整镜像至少核查：

`OH device/soc target`、vendor kernel/BSP、defconfig/DTS、U-Boot、GSL、DDR/register
输入、boot-image producer、分区 manifest/XML、env 模板、烧录工具说明和交付格式。

每个缺口必须写入 `sdk.gaps` 或等价 manifest，并绑定影响阶段。缺口属于用户私有材料时，
向用户说明所需能力和影响；不得猜测文件名、参数或用历史产物替代。该审计结果和经过审查的
allowlist 一并交给 Phase B。

### 安全模式检测（搜索 + 问用户）

搜 SDK config / docs 是否有 secure boot / 镜像签名 / TEE 相关配置：
```bash
grep -ri "SECURE\|SIGN\|TEE\|TRUST\|secure boot\|安全模式" {sdk_config_dir}
```
- **有 secure boot 迹象**（如 `CONFIG_*_SIGN_SUPPORT` / TEE / secure boot）→ **问用户**："这颗芯片用安全模式还是非安全模式？" → 记录 `intake.security.secure_mode`（secure / non-secure）。
- **无** → `secure_mode: non-secure`（默认）。
- **不确定** → 问用户，不要自己猜。

> 安全模式影响 P4 镜像生成（需签名）+ 烧录流程（安全烧录）。不能跳过检测。

### 输出格式

```yaml
# chip-basics.yaml (或 chip-info.md)
chip:
  model: "{chip_model}"
  arch: "{arch}"                  # riscv32 / arm cortex-m4 / ...
  vendor: "{company}"
  board: "{board_name}"

memory:
  flash:
    size: "{size}"                # e.g., "2MB"
    base_addr: "0x{addr}"
  ram:
    size: "{size}"                # e.g., "160KB SRAM + 2MB PSRAM"
    base_addr: "0x{addr}"

system:
  type: "{L0 or L1}"              # liteos_m / liteos_a
  kernel: "{kernel_name}"
  product_type: "{wifiiot/camera/...}"

peripherals: []                    # P3 时填充，此处留空或初版列表

toolchain:
  prefix: "{toolchain_prefix}"     # e.g., riscv32-unknown-elf-
  path: "{absolute_path_to_bin}"
  version: "{gcc_version}"
  special_flags: []                # e.g., ["-march=rv32imac_zicsr"]
  wrapper: false                   # 是否使用 wrapper script
```

---

## 引用的 tools/

| 工具 | 用途 | 路径 | 新增? |
|------|------|------|:----:|
| ohos-dev-build-config | GN 语法 / config 模板 / error cheatsheet | `skills/ohos-dev-build-config/` | — |
| **compiler_fix_playbook** | **★ 工具链修复完整知识库** (wrapper recipe, toolchain adapt patches) | `skills/ohos-dev-build-config/references/compiler_fix_playbook.md` | ✅ **新增引用** |
| ohos-dev-soc-spec-parse | 芯片规格解析 (P2/P3 也用) | `skills/ohos-dev-soc-spec-parse/` | — |

## 语料索引

- **构建装配工具(通用)**: `skills/ohos-dev-build-config/references/` (GN syntax, error-cheatsheet, linker templates)
- **★ 编译修复知识库**: `skills/ohos-dev-build-config/references/compiler_fix_playbook.md` (实测 9 patches + wrapper + decision tree)

---

## Agent Dispatch Spec

### 分发规格

| 属性 | 值 |
|------|-----|
| **agent_role** | `infra-specialist` |
| **category** | `unspecified-high` |
| **load_skills** | `[ohos-dev-build-config, ohos-dev-cross-toolchain]` |
| **dispatch_mode** | **顺序执行** (Step 1→2→3→4→5 强依赖) |
| **parallel_groups** | 仅 Step 2 内部 2a/2b 可微并行 |

### Agent Prompt 模板

```
1. TASK:
   为 {chip_model} ({arch}) 的嵌入式 OS 适配搭建可执行的基准开发环境。
   这是工作流 Phase 1 —— 所有后续阶段的基础。环境搭不好，后面全白搭。
   已通过实测验证 (Hi3861V100/wifiiot, GATE-0: 4/4 PASS after fixes).

2. 执行步骤 (严格按顺序):
   Step 1: 创建 device/board + device/soc 目录结构 (Board/SoC 分离)
   Step 2: 安装并验证工具链 (hb + gn + ninja + cross-compiler)
     ⚠️ hb 常有 Python import 问题，参考 compiler_fix_playbook §3 (Framework Patch)
     ⚠️ 工具链可能缺指令集扩展，考虑 wrapper 方案 (playbook §4)
   Step 3: 生成 config.json / config.gni / BUILD.gn(board)
     ⚠️ components.json 不手动创建！./build.sh --product-name {product} 自动生成 (F-003)
   Step 4: 执行 GATE-0 环境健康检查 (4 子门控，全部 PASS 才继续)
   Step 5: 产出 chip-basics.yaml (芯片规格初版)

3. EXPECTED OUTCOMES:
   ① device/ 目录树完整 (board + soc)
   ② config.json + config.gni + BUILD.gn(board) 已创建
   ③ ./build.sh --product-name {product} 能发现新产品
   ④ GATE-0: 4/4 sub-gates PASS (hb/gn/components/toolchain)
   ⑤ chip-basics.yaml 已写入 (供 P2/P3 消费)

4. REQUIRED TOOLS:
   - ohos-dev-build-config (GN 语法参考 / config 模板 / error 诊断)

5. MUST DO:
   - [ ] 目录结构遵循 target OS 的 device 树规范 (非 OH 则用对应规范)
   - [ ] config.json 中 type/kernel_type 正确决定 L0/L1 路径
   - [ ] **GATE-0 4 子门控全部检查并记录结果**
   - [ ] hb 导入问题时先查 playbook §3 Framework Patch 模式
   - [ ] 工具链缺扩展时考虑 wrapper (playbook §4) 而非立即从源码编译
   - [ ] components.json 缺失时执行 ./build.sh --product-name {product} 而非手动创建
   - [ ] chip-spec 必须包含 arch/ram/flash/system_type/toolchain 字段
   - [ ] 将 GATE-0 结果写入环境报告

6. MUST NOT DO:
   - [ ] 不要跳过 GATE-0 (实测证明 50%+ 首次编译失败是环境问题)
   - [ ] 不要手动创建 components.json (它是 ./build.sh --product-name {product} 的动态产物)
   - [ ] 不要假设工具链就绪——每次都要验证
   - [ ] 不要混淆 board_name 和 soc_model (前者是产品，后者是芯片)
   - [ ] 不要在未通过 GATE-0 时进入 P2

7. CONTEXT:
   项目参数: {target.name} / {arch} / {vendor} / {board} / {target.system_type}
   上游: 用户提供的芯片规格 (可能不完整，P1 负责补全)
   下游: P2 (kernel-port) 消费 chip-spec + 目录树
          P4 (build-verify) 复检 GATE-0 同样 4 子门控
```

## MUST DO (实测血泪教训)

- [ ] **GATE-0 必做不可跳过** — 50%+ 初次编译失败是环境问题
- [ ] **Board/SoC 目录分离** — 同一芯片可服务多个产品
- [ ] **hb Python 问题先查 Framework Patch 模式** — 不是你的代码问题
- [ ] **components.json 是 ./build.sh --product-name {product} 动态产物** — 不手动创建 (F-003)
- [ ] **ninja 需要 `-w dupbuild=warn`** — OH 专用参数
- [ ] **工具链缺指令集扩展 → Wrapper 优先** — 不急着从源码编译整个 toolchain
- [ ] **chip-spec 必须输出给下游** — P2/P3 依赖这些信息
- [ ] **type/kernel_type 一旦选错影响全流程** — L0/L1 分支在此确定

## MUST NOT DO (实测血泪教训)

- ❌ 不要跳过 GATE-0 "省时间"
- ❌ 不要手动创建 components.json
- ❌ 不要假设 `pip install` 就够了解决 hb 问题 (可能还需要 __init__.py + import fix)
- ❌ 不要把 board_name 和 soc_model 搞混
- ❌ 不要在环境未验证通过时就进入 P2
