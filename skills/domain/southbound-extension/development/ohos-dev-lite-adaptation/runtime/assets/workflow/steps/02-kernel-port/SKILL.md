---
name: kernel-port
description: 工作流 Phase 2——执行嵌入式 OS 内核移植：Kconfig 适配链配置、BUILD.gn 编写、内核启动代码适配、C 库适配、linker.ld 链接脚本编写、KAL 内核抽象层映射。触发症状：用户说"内核移植"、"Kconfig 配置"、"启动代码"、"链接脚本"、"内核起不来"、"undefined symbol to main"、"POSIX 适配"、"CMSIS 映射"。
license: MIT
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: lite
  capability: kernel-port
  version: 0.1.0
  status: trial
  category: workflow-step-kernel-port
  references:
    posix_patterns: skills/ohos-dev-kernel-source-query/references/posix_ref_impl.md (~8KB)
    sdk_api_mapping: skills/ohos-dev-board-config-gen/references/hi3861_sdk_api_crossref.md (~12KB)
    compiler_playbook: skills/ohos-dev-build-config/references/compiler_fix_playbook.md
---

## Target profile 路由（强制）

本阶段由内核/profile 驱动，不由 `system_type` 驱动。执行任何内核步骤前，读取 P1 已选定并写入
`workflow_config.yaml` 的 `target.profile` 字段的 target profile（内置在
`{{ASSET_ROOT}}/workflow/target-profiles/` 或用户自定义；**字段缺失 = 回 P1 Step 5 加载**），
选定值记录进 session manifest，消费前校验两者一致。profile 声明 `kernel_family`、
`driver_model`、`device_description`、`build_integration` 和 `source_strategy`。

下方 LiteOS-A/HDF 材料只是参考 profile。不准仅凭 L0/L1 系统级别推断内核或驱动框架。

Profile 优先级：本文档中任何历史 L0/L1 示例或内核专属小节均为非规范性内容，除非加载的
profile 选定了它。profile 可选择 Linux 5.10、LiteOS-A、LiteOS-M 或其他受支持内核，
且必须定义适用的 P2 产出与检查。

# Phase 2: 内核移植（完整）

> **本文件已通过实测验证**。L5 编译 PASS，但 **L2 KAL/POSIX 层仅 0-72% 覆盖率**（Gate Report FAIL）。
> 已产出两份参考文档专门修复此 gap。本 SKILL 已将这些参考文档作为核心输入接入。
>
> **⚠️ Profile 优先级**: 下方历史 L0/L1 材料仅作为那些具名 profile 的证据。L1 目标
> （`system_type = "small"`）不因此选定 LiteOS-A；从 target profile 加载
> `kernel_family` 和 `build_integration`，只用匹配的小节。LiteOS-A 小节仍是条件参考，
> 不是 L1 默认。

## 契约（来自编排器 `skills/ohos-dev-workflow-router/SKILL.md` v0.1.0）

| 属性 | 值 |
|------|-----|
| **输入** | P1 产出的项目骨架 + `chip-basics.yaml` + 芯片内核规格 |
| **产出** | ① Kconfig 4 级适配链 ② BUILD.gn (SoC+Board) ③ 启动代码 (startup/vector/table) ④ C 库适配 (malloc/printf) ⑤ linker.ld ⑥ **KAL 适配层**（仅当选择厂商内核时；直接用开源 LiteOS 则不需要——见 Step 2pre） |
| **门控** | GATE-K: **Step 2pre 可行性报告 `kernel-choice-feasibility.md` 已产出**（含 arch 检查 + SDK 独立性检查 + 方式 A/B 显式选择与理由）+ 内核基线确认（能否链接到 main()? 能否启动到第一个用户任务?）。**缺报告 = GATE-K FAIL，不准进 Step 2a。** |
| **后续** | → P3 驱动开发 / → P4 构建验证 |

## 知识检索（可用时优先知识检索服务如 project-brain MCP；不可用按 skill 知识检索降级链：本地 references → 联网搜索 → 询问用户）

本步骤的本地代码分析，可用时优先使用（可选）project-brain 等知识检索服务 MCP：
- `locate_symbol` — 定位 LOS_*/内核函数定义（方式 B' 桥接时找 Arch* 等价符号）
- `get_call_graph` — 追内核 API 调用链（SDK 预编译库调哪些 LOS_*）
- `get_dependencies` — 看 kernel/SDK 模块依赖结构
- `impact_analysis` — 改内核配置/链接脚本前评估波及面

> MCP 调失败或未装 → 按 skill 知识检索降级链（别的 MCP → skill → 在线搜 → 问用户）。

## 子步骤总览

```
P2: 内核移植
│
├─ 2pre: ★ 内核选择决策（直接用开源 LiteOS vs 厂商内核+KAL 适配）
│        └─ 优先直接用；不可行才退而做 KAL 适配层
│
├─ 2a: Kconfig 适配链 (board → series → soc → defconfig)
│       └─ 可与 2b 并行
│
├─ 2b: BUILD.gn 编译入口 (SoC级 + Board级)
│       └─ 可与 2a 并行
│
├─ 2c: ★ 内核启动代码 (startup_S / 向量表 / SystemInit / 基础时钟)
│       └─ 实测: CSR 指令依赖 zicsr 扩展
│
├─ 2d: ★ C 库适配 (malloc_r --wrap / vprintf / snprintf)
│       └─ L0 必需, L1 可选 (L1 有更完整的 musl)
│
├─ 2e: linker.ld 链接脚本 (Flash/RAM 布局 / 段定义)
│       └─ 实测: ROM_TEXT 预留 +1~3% 余量
│
└─ 2f: KAL 适配层（仅当 Step 2pre 选择厂商内核时）
        ├─ CMSIS-RTOS v2 → {target_kernel} 映射
        ├─ POSIX → {target_kernel} 映射
        └─ 参考文档: posix_ref_impl.md + sdk_api_crossref.md
        ⚠️ 如果 Step 2pre 选了直接用开源 LiteOS，本步跳过（内核原生提供 CMSIS/POSIX）
```

---

## §L1-DIFF: L1 小型系统 (LiteOS-A) 差异说明

> **当目标为 L1 小型系统（`target.system_type = "small"`）时，以下差异适用。**

### 内核差异总览

| 维度 | L0 (LiteOS-M) | L1 (LiteOS-A) |
|------|:-------------:|:-------------:|
| **内核源码** | `kernel/liteos_m/` | `kernel/liteos_a/` |
| **内核大小** | ~6KB 起步 | 数十KB |
| **调度方式** | 硬实时 RTOS | 软实时 |
| **MMU** | ❌ 不支持 | ✅ 支持 |
| **进程模型** | 仅任务(线程) | 进程+线程 |
| **文件系统** | LittleFS/FAT (可选) | VFS |
| **网络协议栈** | 轻量 TCP/IP (可选) | 完整协议栈 |
| **KAL 接口标准** | CMSIS + POSIX 子集 | POSIX + HDF OSAL |

### P2 步骤调整 (L1 模式)

```
P2-L1 变体:
│
├─ 2a: Kconfig 适配链
│   ├── 路径变为: build/liteos/config/board/{series}/soc/{soc}/.config
│   └── defconfig 可能使用 ARCH_ARM / ARMV8_A 而非 RISCV32
│
├─ 2b: BUILD.gn
│   ├── 可能引入 HDF 子系统组件声明
│   └── 编译标志可能包含 -march=armv7-a 等 ARM 特有选项
│
├─ 2c: 启动代码
│   ├── 从 SystemInit() 入口变为 Linux 风格启动
│   ├── 可能有 MMU 初始化步骤 (页表/TLB)
│   └── CSR 指令不再是 zicsr 而是 ARM 系统寄存器
│
├─ 2d: C 库适配
│   ├── L1 通常自带较完整 musl libc, __wrap 可能不需要
│   └── 或使用 uclibc / bionic 替代
│
├─ 2e: linker.ld
│   ├── 需要处理 MMU 内存布局 (虚拟地址空间)
│   └── ROM_TEXT/RAM 分区可能完全不同
│
└─ 2f: KAL 抽象层
    ├── CMSIS 映射目标从 LiteOS-M API 变为 LiteOS-A API
    ├── POSIX 映射可能更完整 (L1 支持更多 POSIX 调用)
    └── ⚠️ 可能额外需要 HDF OSAL 映射层 (非 POSIX, 是 HDF 特有)
```

### 两棵内核关系 + 适配模式（L1-Linux greenfield 必读）

L1-Linux 芯片适配会同时面对**两棵 Linux 内核源码**，必须先厘清二者关系，再选适配模式：

| 内核来源 | OH 集成状态 | 芯片驱动状态 | 用途 |
|----------|:-----------:|:------------:|------|
| **OH code 仓内核**（如 `kernel/linux/linux-5.10/`） | ✅ OH-integrated（能跑 `hb build`，含 OH 框架 config：binder/hilog/MTD 等） | ❌ chip-empty（greenfield，无芯片特定驱动/defconfig/DTS） | **hb build 编这棵，板上跑** |
| **vendor SDK 内核**（如 `third_party/linux/linux-5.10.y/`） | ❌ 非 OH-integrated（不能直接跑 `hb build`，缺 OH 框架 config） | ✅ chip-adapted（含芯片驱动 fmc_ids/watchdog/GPIO/I2C/display + defconfig + DTS） | **参考源**（驱动 port 来源） |

**适配模式 A（OH 仓内核 + vendor 驱动 port）★ greenfield 推荐**：
- 读 vendor SDK 内核的芯片驱动（fmc_ids / watchdog / GPIO / I2C / display）+ defconfig + DTS，**port 进 OH 仓内核**：
  1. 创建 OH defconfig：基于 vendor `{chip}_defconfig` + 追加 OH 必需 config（binder/android/MTD/hilog，见 §BINDER_IPC_32BIT / §binderfs / §Kconfig source uncomment）
  2. DTS port：vendor `boards/{board}/dts/` → OH 仓 `kernel/linux/config/linux-5.10/arch/arm/boot/dts/`（重命名 + include 路径修正，来源声明 patched B 类，见 §DTS 来源完整性）
  3. BUILD.gn 接入：kernel.mk 工具链覆盖 + kernel_module_build.sh 板级分支（见 Step 2b）
- **不重写驱动**——vendor 已写好芯片驱动（懂芯片寄存器），适配者做 integration（port + 配置 + OH 框架胶水），见 §集成边界。

> 与下方"构建路径决策 A/B"的区别：**适配模式 A**（本节）是"用哪棵内核 + 驱动怎么来"的内核选择决策；**构建路径 A/B**（下节）是"OH 组件要不要进 rootfs"的构建系统决策。两者正交，greenfield 芯片通常适配模式 A + 构建路径 B（OH 集成）。

### L1-Linux 变体与构建路径决策

> L1 不只有 LiteOS-A——也可以是 **Linux 内核**（如 hispark_taurus_linux）。Linux 变体有**两条构建路径**，必须问用户选哪条，不能默认走 OH 集成。

#### L1 内核变体

| 变体 | 内核 | 典型板 | 工具链 |
|------|------|--------|--------|
| LiteOS-A | `kernel/liteos_a/` | hispark_taurus | arm-linux-gnueabi |
| Linux | `kernel/linux/linux-5.10/` | hispark_taurus_linux | arm-linux-musleabi（Linux 用户态） |

#### 构建路径决策（L1-Linux 关键，前序锁定优先自决，否则问用户）

L1-Linux 芯片如果厂商 SDK 有**独立 build 系统**（自己的 build.sh + rootfs + 镜像打包），有两条路径：

| 路径 | 做法 | rootfs | OH 组件 | 优缺点 |
|------|------|--------|---------|--------|
| **A. 厂商构建** | 厂商 build.sh 编 uboot+kernel+rootfs + 厂商 mkimg 打包 | busybox（厂商） | 无/叠加 | ✅ 避开 OH 组件依赖（init/begetutil 等），直接产可烧录镜像；❌ 无 OH 组件（samgr/hilog/dsoftbus） |
| **B. OH 集成** | OH `./build.sh` + OH 组件 + make_images | OH rootfs | 全量 | ✅ 完整 OH 小型系统；❌ 可能撞 OH 组件依赖墙（init/begetutil 递归依赖，GCC 下尤其） |

**决策依据（前序锁定优先）**：

先查前序决策（P1 采集的 XTS 要求 / OH 组件需求 / 业务目标）是否已隐式锁定 A 或 B——**锁定则工作流自决并记录理由，不再问用户**；未锁定才问用户。

**前序锁定判定规则**：
- 用户已选 XTS 严标准（要跑 acts）→ **路径 A 跑不了 XTS**（A 无 OH 组件，acts 依赖 samgr/hilog）→ **B 是硬要求 → 工作流自决 B**，记录"Q2 XTS 严标准锁定 B"，不问用户。
- 用户明确"只要可烧录镜像，不要 OH 组件"→ **A 是硬要求 → 工作流自决 A**，记录"用户明确无 OH 组件需求锁定 A"，不问用户。
- 前序未涉及 XTS / OH 组件需求（或需求模糊）→ **未锁定，问用户选 A 还是 B**。

**未锁定时才问用户**：
- 厂商 SDK 有独立 build.sh + rootfs（busybox/mkimg）→ 问用户选 A 还是 B。A 快速产可烧录镜像（无 OH 组件），B 完整但可能撞依赖。
- 厂商 SDK 无独立 build → 只能 B（自决，不问）。
- 用户要完整 OH 小型系统（samgr/hilog/XTS）→ B，但做好框架 patch 准备（init/begetutil GCC 兼容）。

> **不能默认走 B**——L1-Linux + GCC 下 OH 组件（尤其 init/begetutil）可能有递归依赖问题，导致 rootfs 打包阻塞。但前序决策已锁定 B 时（如 XTS 严标准）不必再问，自决 B 并记理由即可，避免碎片化交互（实测教训：Q2 严标准已锁 B，工作流仍要求问用户 = 多余交互）。

### DTS 设备树生成（L1-Linux 必需）

L1-Linux 内核需要 DTS（设备树）描述板级硬件。L0/LiteOS-A 不需要（用 HDF 配置代替）。

- **从芯片 spec 生成**：寄存器地址、中断号、pin mux、时钟、外设连接——**走 `ohos-dev-soc-spec-parse` skill 提取**（单点查询或完整提取，命中 `chip-specs-quick-ref.md` / `ddr-variant-guide.md` 直接用；未命中调 ohos-dev-kernel-source-query 联网查 DTS/SDK 头文件；datasheet 仅作回退，A 类代码，spec 驱动）
- **不抄厂商 DTS**——自己写
- 放到 `boards/{board}/dts/{chip}.dts`，内核编译时编成 DTB
- 参考开源 LiteOS/Linux 的 DTS 结构（`kernel/linux/linux-5.10/arch/arm/boot/dts/`）

#### DTS 来源完整性（W4，GATE-K 检查项）
L1-DIFF §DTS 要求"从芯片 spec 生成，不抄厂商 DTS"。但绿场芯片若用户内核补丁已含 DTS，可接受但**必须声明来源**（A/B/C 分类中属 B 类——补丁带入，非自己生成）。GATE-K 检查：
- [ ] DTS 来源是 `generated`（从 spec 自己写）还是 `patched`（补丁带入）？
- [ ] 若 `patched` → 记录补丁来源 + 评估是否需独立生成（补丁带入的 DTS 可能含厂商特定 quirk，移植到别的板要改）
- [ ] 不准默写"已生成 DTS"而实际依赖补丁——来源必须显式声明（P-显式未验证的同理）

### 源文件来源完整性（GATE-K 检查项，全部源文件通用）

上方 DTS 来源完整性是本检查在 DTS 上的特例。P2 产出的**全部源文件**（启动代码 .c/.S、KAL 适配 .c/.h、linker 脚本、BUILD.gn、defconfig）都要过同一检查：

- [ ] 每个源文件是如何产生的？三选一记录：
  - `generated`（由工作流从规格/模板生成）→ 记录输入 spec + 使用的工具
  - `adapted_from_existing`（基于现有代码修改）→ 记录原始来源 + 改动范围
  - `manual`（手工编写）→ 记录依据
- [ ] ⚠️ 源文件 SHA 与任何现有适配代码一致 → **触发目标漂移警报**（说明是抄现有适配而非按规格生成，"从骨架再生"的验证前提不成立），停下核查
- [ ] 来源记录写入 PROVENANCE，GATE-K 签发前核对本清单齐全

> 本节是编排器 `skills/ohos-dev-workflow-router/SKILL.md` GATE-K「[来源完整性]」确认项在步骤文件的落地——执行者跑 P2 主要读本文件，子项必须在这里可执行，不能只活在编排器清单里。

### L1-Linux 其他 boot/内核环节（实测缺口补全）

#### boot 阶段 DDR/时钟配置（厂商提供，B 类）
boot image（U-Boot/SPL）里含 DDR 初始化 + training 代码/参数 + 时钟 PLL 配置。这些是**芯片厂商提供**的（在 reg_info.bin / U-Boot defconfig / 厂商 DDR 配置工具里），不要自己写。
- 确认 DDR 配置来源：厂商 SDK 的 DDR config 工具 / U-Boot defconfig 里的 DDR 参数 / reg_info.bin 里的寄存器初始化表
- 换芯片/换 DDR 颗粒 → 需厂商提供新的 DDR 参数（B 类，问用户/厂商要），**不要自己调 DDR training**
- 时钟/PLL 同理：boot 阶段时钟树由厂商 U-Boot 配置，内核阶段由 DTS clock 节点描述

#### SMP 多核启动（Cortex-A SMP）
Hi3516 是 Cortex-A7 SMP。多核启动注意：
- **bootargs**：`maxcpus=N` 控制启动核数；`cpuidle.off=1` 调试用
- **DTS**：每个 cpu 节点 + `enable-method`（spin-table / psci）；secondary 核的 release-from-reset 由 boot 阶段处理
- 单核 vs 多核：单核芯片无 secondary 启动流程；SMP 芯片要确认 release-from-reset 机制（厂商 U-Boot 处理，B 类）

#### 内核重编后 uImage 必走 FIT（L1-Linux，实测教训）

L1-Linux 内核任何改动（加驱动/改 CONFIG/改 DTS）重编后，uImage **必须用 `mkimage -f linux_image.its uImage` 重做 FIT**，**不能用 `make uImage`**。

- **为什么不能 `make uImage`**：`make uImage` 产出 **legacy 单 kernel 镜像**——**无 dtb**，load 地址 `0x40020000`。U-Boot `bootm` 拿不到设备树 → 报 `FDT and ATAGS support not compiled in` → 内核**根本没起来**（无 `Starting kernel`）即复位，板子 reboot loop。
- **正确做法（FIT）**：用 `mkimage -f linux_image.its uImage` 打 FIT 镜像，`linux_image.its` 描述 `fdt@0x40000000` + `kernel@0x40018000` 两个组件。FIT 构建目录（如服务器 `/srv/workspace/boot_images/_fit_assemble/`）含三个文件：`linux_image.its` + `devicetree.dtb` + `zImage`。重编流程：拷新 zImage 进 `_fit_assemble/`（改了 DTS 先 `make dtbs` 把 `arch/arm/boot/dts/{board}.dtb` 拷成 `devicetree.dtb`）→ `mkimage -f linux_image.its uImage`。
- **验判（快速判别 FIT vs legacy）**：`mkimage -l uImage`——输出含**两个** `Image `（Image 0 fdt + Image 1 kernel，kernel load `0x40018000`）= FIT；只有**单个** kernel（load `0x40020000`）= legacy，烧了必 reboot loop。
- **症状对应**：烧后板子卡 bootm 跳转、无 `Starting kernel`、reboot loop → 第一时间 `mkimage -l uImage` 验是不是误用了 legacy。FIT 含 dtb（如 16429B 量级），legacy 无 dtb。

> 关联诊断：烧录侧症状处置见 `skills/ohos-ci-lite-deploy-burn/SKILL.md`；改 uImage 属烧录件改动，按 memory `update-changelog-after-burnfile-change` 记 CHANGES（md5+改动+根因）。

#### P2 内核驱动 port：集成边界（不重写驱动，做 integration）

适配模式 A（见 §两棵内核关系）的内核驱动 port 是 **integration 工作，不是写驱动**。以下硬约束界定集成边界：

**vendor 提供（厂家原生，只有厂家能写）**：
- 内核驱动源码（fmc_ids / watchdog / GPIO / I2C / display 等——厂家懂芯片寄存器）
- HAL 层（SDK 的 drv/ + include/ + libs/）
- defconfig（`{chip}_defconfig`，芯片能力基线）
- DTS（`boards/{board}/dts/`，板级硬件描述）
- U-Boot（boot 阶段 DDR/时钟/SPI Nand probe）
- `.xlsm`（DDR 配置工具产出）
- boot 工具（gslboot_build 等）

**适配者做 integration（不重写驱动代码）**：
- port vendor 驱动进 OH 仓内核（拷贝驱动源码 + 修 Makefile.param 相对路径 + build.sh 补编译逻辑）
- 配置：defconfig（基于 vendor + 追加 OH config）/ DTS（port + 重命名 + include 修正）/ BUILD.gn 接入
- OH 框架胶水：HDF wrapper 调 vendor HAL（L1 HDF，见 P3 Step 3c HCS 配置）

**硬阻塞（vendor SDK 缺某驱动 → 适配者写不了）**：
- 若 vendor SDK 缺某驱动（厂家没给）→ 适配者**没有芯片寄存器文档，写不了** → 硬阻塞，**显式声明缺口问用户**（问用户/厂家要驱动，不能自己瞎写）。
- 这与 memory `prefer-driver-adaptation-over-rootfs-bypass` 一致：缺驱动优先找厂家要，不能 rootfs 绕过 / 自己 stub。

**板级 tweak（算 integration，不算写驱动）**：
- 颗粒 ID 不在 vendor fmc_ids 表 → 加 ID 表条目（补数据，不是写逻辑），见 §SPI Nand 颗粒 ID 覆盖。
- DDR 颗粒换型号 → 厂商提供新 .xlsm / DDR 参数（B 类，问厂家要，见 §boot 阶段 DDR/时钟配置）。

> 判据：改的是"数据/配置"（ID 表条目、defconfig CONFIG、DTS 节点、include 路径）= integration；改的是"驱动逻辑"（寄存器读写、初始化序列、中断处理）= 写驱动，适配者不做。

#### SPI Nand 颗粒 ID 覆盖（P2 port 必查项，板子用 SPI Nand 时）

板子用 SPI Nand 介质时，port vendor `fmc_ids` 表后**必须核查板子实际 SPI Nand 颗粒 ID 是否在表里**。vendor demo 板的颗粒和你的实际板子可能不同（实测教训：板载 DS35Q1GB-IB 不在 vendor 默认表 → 烧了 probe 失败 0x81）。

**颗粒 ID 来源**：
1. 板子 SPI Nand 芯片丝印（物理查）
2. 烧录启动日志（getinfo / probe 打印的 ID，如 `0xe5 0xf1`）
3. vendor SDK 文档 / 颗粒 datasheet

**不在表里 → 加条目**（内核 + u-boot 两侧 fmc_ids 都加，否则 uboot 阶段 probe 失败）：
- 条目字段：`id`（manufacturer/device code）/ `page size` / `erase size` / `oob size` / `quad 速率`
- 内核侧：vendor 内核 `drivers/mtd/devices/fmc_ids_hi3516cv610.c`（或对应芯片的 fmc_ids 文件）
- u-boot 侧：vendor u-boot 对应 fmc_ids 文件
- 加完重编 vendor uImage + boot_image（见 §内核重编后 uImage 必走 FIT）

**烧前必查项（不查烧了炸，P-显式未验证）**：
- [ ] 板子实际 SPI Nand 颗粒型号 + ID 采集（丝印 / 启动日志 / 文档）
- [ ] 查 vendor fmc_ids 表是否含该 ID
- [ ] 不在 → 内核 + u-boot 两侧 fmc_ids 加条目
- [ ] 重编 vendor uImage + boot_image，记 CHANGES（md5+改动+根因，按 memory `update-changelog-after-burnfile-change`）

**无硬件 / 无烧录日志时的处理（实测教训）**：

无硬件时无法采集板子实际颗粒 ID，只能查 vendor 表（覆盖的是 vendor demo 板，不是用户实际板子）。**vendor demo 板颗粒和用户实际板子颗粒可能不同**——实测：同一 DMEB demo 板，vendor 表只有 HY035/HY073，但实际板子颗粒是 DS35Q1GB-IB（id `0xe5 0xf1`，不在 vendor 表）。因此：

- **无硬件时**：颗粒 ID 覆盖标 **"待烧录验证"**，**不假设 vendor 表覆盖实际板子**。GATE-B+ / GATE-K 对颗粒 ID 项标 CONDITIONAL（非 PASS），显式声明"未实测验证，烧录时可能 probe 失败"。
- **烧录后验证**：烧录启动日志的 getinfo / probe 打印实际颗粒 ID → 核对是否在 fmc_ids 表。
- **烧录后 probe 失败（0x81 或 fmc_ids 不匹配）→ 加实际颗粒条目**（内核 + u-boot 两侧 fmc_ids，见上方"不在表里 → 加条目"），重编 vendor uImage + boot_image。
- **references 应记录已知板子实测颗粒**（如 hi3516cv610 DMEB 实测 DS35Q1GB-IB，id `0xe5 0xf1`），供后续适配复用——但标注"实测颗粒，换板/换批次需重新采集"。

> 关联：GATE-B+ 消费者验收应含"颗粒 ID 覆盖验证"项（vmlinux/strings 查颗粒名 + uboot fmc_ids 查条目）；无硬件时该项标"待烧录验证"而非 PASS；briefing（Role 2）应把"SPI Nand 颗粒型号 + ID"作为板子规格采集字段（有硬件物理查丝印，无硬件标待烧录采集）。

#### L1-Linux 内核 defconfig 裁剪（P2 L1 专属）
L1-Linux 内核要裁剪（不像 LiteOS 用 Kconfig 组件裁剪）：
- 基于 `{chip}_defconfig`（厂商提供，B 类）+ 按产品裁剪（关掉不需要的子系统：如 IPCamera 关 display/sound）
- `make ARCH=arm {chip}_defconfig` → `make menuconfig` 调整 → `make savedefconfig` 生成精简 defconfig
- 裁剪后内核大小要在 boot 分区容量内（GATE-B 大小检查）

### 32位 OH 小系统内核必开 BINDER_IPC_32BIT（L1-Linux，实测教训）

L1 小系统（32位 ARM，OH 用户空间也是 32 位）内核 binder 必须强制 32 位 IPC 协议，否则与 OH 32 位用户空间结构体大小不一致 → IPC 全瘫。

- **改法**：`include/uapi/linux/android/binder.h` 加一行 `#define BINDER_IPC_32BIT 1`，放在 `B_TYPE_LARGE` 之后。
- **不开的后果**：内核 binder 走 64 位协议（`binder_write_read` 结构体 48B），OH 32 位用户空间按 24B 传 → `binder: ioctl c0186201 returned -22`（EINVAL，`-EINVAL`）刷屏 ×400 → samgr/foundation 等依赖 binder 的服务全起不来 → IPC 瘫痪。
- **来源**：OH 官方 `hispark_taurus_cv610_small.patch`（就这一行改动，patch 第 9 行附近）。
- **前置**：先确认 `drivers/Kconfig` 的 `source "drivers/android/Kconfig"` 已 uncomment（见 §Step 2a "Kconfig source 必须先 uncomment"），否则 `CONFIG_ANDROID_BINDER_IPC=y` 都不进 `.config`，本宏也无处生效。

### OH 小系统禁 binderfs（L1-Linux，实测教训）

OH 小系统 init **不挂 binderfs**——binder 设备靠 `misc_register` + devtmpfs 自动建 `/dev/binder`、`/dev/hwbinder`、`/dev/vndbinder`。defconfig 要**去掉 `CONFIG_ANDROID_BINDERFS=y`**，保留：

```kconfig
CONFIG_ANDROID_BINDER_IPC=y
CONFIG_ANDROID_BINDER_DEVICES="binder,hwbinder,vndbinder"
# CONFIG_ANDROID_BINDERFS is not set   ← 禁掉
```

- **开 binderfs 的后果**：内核期望 init 挂 binderfs（每个 binder 设备在挂载点下），但 OH init 不挂 → `/dev/binder` 不出现或行为异常 → binder IPC 起不来。
- 与 §BINDER_IPC_32BIT 配套：32 位协议 + 禁 binderfs + 三设备字符串，是 OH 小系统 binder 适配的标准组合。

### L1 参考适配 (学习 HDF 结构)

| 参考芯片 | SoC 仓库 | 关键学习点 |
|----------|---------|-----------|
| STM32MP157 (`device_soc_st`) | device_soc_st | L1 HDF 驱动结构、OSAL 映射、HCS 配置 |
| BK7235 (`device_soc_beken`) | device_soc_beken | WiFi/BLE SoC 的 L1 HDF + LiteOS-A 组合 |
| RK2206 (`device_soc_rockchip`) | device_soc_rockchip | 瑞芯微 L1 适配（最完整的社区 L1 参考）|

> **建议**: 如果首次做 L1 适配，先以 STM32MP157 或 BK7235 为参考目标，
> 理解 HDF 驱动结构后再迁移到目标芯片。

---

---

## Step 2pre: 内核选择决策（直接用开源 LiteOS vs 厂商内核+KAL）

> **优先直接使用开源 LiteOS-M（L0）或 LiteOS-A（L1）**，除非实在不可行。
> 开源 LiteOS 原生实现 CMSIS-RTOS2 + LOS_* 双套接口，**不需要 KAL 适配层**。
> 若厂商 SDK 绑定了厂商内核（不能独立链接），优先尝试 **方式 B'（SDK 内核替换）**：用开源 LiteOS 替换 SDK 自带内核，hi_* → LOS_* shim，仍保内核源码可见。
> 详见 本步骤 `references/kernel-access-modes.md`（两种内核接入方式详解）。

> **⚠️ 反短路规则**：repo 里已有的 `kernel_is_prebuilt: true` / `board_adapter_dir` 等配置是**待验证的输入**，不是"已决策"的标志。**禁止**用"repo 说 prebuilt 所以做 prebuilt"作循环论证跳过本步。即使芯片是 OH 已支持板、配置已存在，也必须跑完决策树并产出报告——报告要回答"能否不走 prebuilt"，而不是复读配置。
>
> **硬性产出**：本步必须产出 `kernel-choice-feasibility.md`（无论最终选 A 还是 B）。缺此文件 → GATE-K FAIL → 不准进 Step 2a。报告不是"不可行时才写"，是**每次都写**：可行→选 B，记录 arch✅ + SDK 独立✅；不可行→选 A 或混合，记录阻塞项。

### 决策流程

```
芯片 arch 是什么？
│
├─ kernel/liteos_m/arch/ 支持该 arch？（L0）
│  或 kernel/liteos_a/ 支持？（L1）
│
├─ YES → 检查 SDK 依赖
│  │   厂商 SDK（WiFi/外设）能否作为独立库链接，不依赖厂商内核？
│  │
│  ├─ YES → ★ 直接用开源 LiteOS（方式 B）
│  │        import("//kernel/liteos_m/liteos.gni")
│  │        不需要 KAL 适配层（Step 2f 跳过）
│  │        只需 BSP（启动代码 + 时钟 + UART）+ HAL 驱动
│  │
│  └─ NO → 厂商 SDK 依赖厂商内核
│           → 列报告：哪些功能依赖厂商内核
│           → 检查 SDK 可替换性：hi_* 等厂商内核 API 包装层有源码？或可写 shim？
│           │
│           ├─ 可替换 → ★ 方式 B'（SDK 内核替换）：
│           │     用开源 liteos_m 替换 SDK 自带厂商内核；
│           │     在 liteos_m 上重实现 hi_* → LOS_*（shim）或重编译 SDK 源码。
│           │     内核全源码可见，SDK 驱动复用，无 KAL 层。
│           │
│           → 让用户决定（优先 B' > A）：
│              a. 方式 B'：开源 liteos_m + hi_* shim（内核源码可见）★ 优先
│              b. 方式 A：厂商预编译内核 + KAL 翻译（内核黑盒）
│              c. 混合：部分直接用 + 部分适配
│
└─ NO → arch 不支持
         → 只能走厂商内核 + KAL 适配层（方式 A）
```

### 方式对比

| 维度 | 方式 B：直接用开源 LiteOS ★ | 方式 B'：SDK 内核替换 ★ | 方式 A：厂商内核 + KAL |
|---|---|---|---|
| 内核来源 | 仓库 `kernel/liteos_m`/`liteos_a`（源码） | 仓库 `kernel/liteos_m`（源码） | 厂商预编译 `.a` |
| OH 编译内核 | 是 | 是 | 否（`kernel_is_prebuilt:true`） |
| SDK 处理 | SDK 独立，直接链接 | SDK 绑厂商内核 → hi_* shim 到 LOS_* | SDK 绑厂商内核，直接用 |
| 适配层 | 不需要 | hi_*→LOS_* shim（供 SDK） | CMSIS/POSIX→LOS_* KAL（供 OH 框架） |
| 内核可见性 | 全源码 | 全源码 | 黑盒 |
| 适用条件 | arch✅ + SDK 独立 | arch✅ + SDK 可替换 | arch❌ 或 SDK 不可替换 |
| 典型代表 | rk2206、neptune100、nearlink_dk_3863 | hi3861v100（目标：切 liteos_m） | hi3861v100（现状）、ws63v100 |

### 报告格式（每次必产）

**无论可行与否，产出 `kernel-choice-feasibility.md`（按下述格式）。** 让用户确认选择。

```
## 内核选择可行性报告
- 芯片: {chip_model} / {arch} / L{0|1}
- 开源 LiteOS arch 支持: [✅/❌]  （查 kernel/liteos_m/arch/ 或 kernel/liteos_a/arch/）
- SDK 独立性: [✅/❌]  （厂商 SDK 能否作为独立库链接，不依赖厂商内核？）
- SDK 可替换性: [✅/❌]  （hi_* 厂商内核 API 包装层有源码？或可写 shim 到 LOS_*？）
### 阻塞项（仅当 arch❌ 或 SDK❌ 且不可替换时填）
1. {阻塞项} — {原因/证据}
### 选择（优先 B > B' > A）
- [ ] 方式 B：直接用开源 LiteOS（arch✅ + SDK✅）→ Step 2f 跳过
- [ ] 方式 B'：SDK 内核替换（arch✅ + SDK 可替换：hi_* shim 或源码重编译）→ Step 2f 跳过
- [ ] 方式 A：厂商内核 + KAL（arch❌ 或 SDK 不可替换）
- [ ] 混合：部分直接用 + 部分适配
```

> 用户确认后才进入 Step 2a。选了方式 B → Step 2f 跳过。
>
> **转发给用户时**：把每个选项的**完整描述**说出来（如"直接用开源 LiteOS-M，SDK 独立，无需适配层"），不要只给标签"方式 A/B/B'"——用户记不住标签，按描述确认。

> **编译期证据回填**：P4 编译时若观察到"引入开源 `kernel/liteos_m` 头文件与 SDK 自带内核头文件类型冲突"——这正是 SDK 独立性 ❌ 的实证。回填进本报告"阻塞项"，作为方式 A 的客观依据，而非弃之不顾。

### 方式 B' 执行要点（工作流侧知识，非执行者自行推断）

选了方式 B' 后，以下结构/编译变更由工作流引导：

- **kal/ 层**：方式 A 遗留的 KAL 翻译层不需要。删除 `*_adapter/kal/` 目录，并从上级 `BUILD.gn` 的 deps 中移除（避免引用悬空目标）。
- **config.json**：`kernel_is_prebuilt` 改 `false`（或删除），`kernel_type` 保持 `liteos_m`。
- **构建体系对齐**：厂商 SDK 可能是 SCons 主导（如 hi3861 的 `hm_build.sh`→`SConstruct`），不是纯 GN——OH 的 GN 只编组件库，内核编译/链接被 SDK SCons 管。方式 B' 要让 GN 发现开源 liteos_m：补 GN 侧 BUILD.gn 骨架（board/soc 公司级 + 子级 `module_group`，含 public config 依赖链），让 `//kernel/liteos_m:liteos_m` 能被 GN 编译产出 .a 供链接。参考同架构已支持板（如 hihope）的 BUILD.gn 结构。
- **liteos_m 源码编译触发（关键）**：光改 `kernel_is_prebuilt:false` 不会让开源 liteos_m 源码参与编译。需逐项补齐（参考仓内方式 B 样板板如 rk2206，逐项 diff 补齐）：① vendor `config.json` 声明 `"subsystem":"kernel","component":"liteos_m"`；② `kernel_configs/{debug,release}.config` 存在且非空（含 `LOSCFG_PLATFORM_*` 选对 arch，如 RISC-V 板选 `LOSCFG_PLATFORM_QEMU_RISCV32_VIRT`）；③ board/soc 级 `Kconfig.liteos_m.*` 文件齐全；④ 打断 `soc→sdk→ohos→liteos_m→modules→soc` 依赖循环（soc 级 BUILD.gn `modules=[]`）。缺这些 liteos_m 目标声明了却不编译（.o 不产出）。
- **SDK↔内核接口适配层（核心）**：**不要强行替换预编译内核 .a**。正确做法分四步：
  1. **分析耦合**：SDK 预编译库依赖哪些内核接口——① hi_* 包装层调用 ② 预编译库内部对 LOS_* 的直接调用 ③ 结构体布局/ABI 约定。**区分导出 vs 导入**：`liblitekernel_*.a`/`libbsp_base.o` 是**导出** LOS_*/hi_*（内核/BSP 实现），`libsystem.a`/`libwifi.a` 是**导入**——别把导出当缺失去 stub。**先查 SDK 是否已提供 hi_* 实现**（`build/libs/*.o` 或 SDK .a，如 `libbsp_base.o` 常含 hi_* 全套实现且内部调 LOS_*），有就复用、别重复造 hi_* shim。
  2. **对比开源 liteos_m**：开源 liteos_m 实际提供的 LOS_*/接口，与 SDK 期望的差异在哪（函数签名、缺失函数、结构体布局、调用约定、ABI）。
  3. **写适配层**：差异处写适配层——**对上满足 SDK 的接口要求**，**对下转发/翻译到开源 liteos_m**。注意：hi_* 包装层通常 SDK 已提供实现（复用 `libbsp_base.o` 即可，别重写）；适配层主要补**真正缺失**的厂商扩展 LOS_*（开源 liteos_m + SDK .o 都没有的）。
  4. **链接（两个链接过程，关键）**：厂商 SDK 构建常有两个独立链接——GN 的 `executable("liteos")`（开源 liteos_m 内核 .o）+ SCons 最终固件链接（SDK 预编译库 + OH 组件，产出固件）。**hi_shim 适配层 + 开源 libkernel.a 必须链进 SCons 最终固件链接**（不只 GN liteos executable），否则 SDK 预编译库的 LOS_* 调用解析不到开源内核。hm_build.sh 把 libkernel.a + libhi_shim.a 拷到 ohos/libs/ 作 SCons 链接输入。
- **链接脚本硬编码（关键）**：SDK 的 `link.ld.S` 可能用 `KEEP(SORT(xxx.o)(.text*))` 硬编码引用 SDK 预编译 .o（如 `liblitekernel_base.o`/`libbsp_base.o`）。光从 LIBS 移除 `-llitekernel_flash` 不够，链接脚本仍把它们当输入 → multiple definition。需改链接脚本：移除 SDK 内核 .o（`liblitekernel_base.o`）的段引用、替换为开源 liteos_m 内核 .o；**保留 BSP .o**（`libbsp_base.o`，hi_* 复用）。
- **LOS_*→Arch* 符号桥接（关键，方式 B' 命门）**：开源 liteos_m 把部分 LOS_* 改名为 Arch*（如 `LOS_HwiCreate`→`ArchHwiCreate`、`LOS_IntLock`→`ArchIntLock`），通过 `#define` 宏映射。但**宏只在源码编译时展开，对 SDK 预编译库无效**（预编译库符号表里仍是 `LOS_*`）。桥接方法：在 hi_shim 用**独立 .c**（**不 include** 带宏映射的头，手动 `extern` 声明 Arch* 原型）写**真实包装函数**（`LOS_HwiCreate` 内部调 `ArchHwiCreate`）。不能用宏映射、不宜只靠 `--defsym`（真实包装更稳、能处理签名差异）。**结论：方式 B' 对 SDK 绑内核芯片可行**——需 hi_shim 桥接 LOS_*/Arch* + 让 liteos_m 源码参与编译（见上方"liteos_m 源码编译触发"）。
- **头文件隔离**：开源 `kernel/liteos_m` 头文件与 SDK 自带厂商内核头文件类型定义冲突（实证：`FD_SETSIZE` 等宏重定义）。具体操作：从 board `config.gni` 移除 SDK 自带 musl/libc include 路径（hi3861 移除 10 个 Huawei_LiteOS musl 路径），SDK 侧引厂商头、内核/适配层侧引开源 musl + liteos_m 头。开源 musl 的 `__cplusplus` 等可能触发 `-Werror=undef`，按需加 `-Wno-error=undef`。
- **BSP**：板级提供启动代码 + 时钟 + UART + 中断控制器（开源 liteos_m arch 层提供上下文切换，板级补外设）。
- **Flash 布局适配（开源内核体积远大于厂商精简内核）**：开源 liteos_m（含 posix/vfs/signal，~2.5MB）比厂商精简内核（如 Hi3861 Huawei_LiteOS 278K）大一个数量级。若芯片 `link.ld.S` 把内核映射到小的内嵌 Flash 分区（为厂商精简内核设计），开源内核装不下 → ROM_TEXT 溢出。解法：把内核映射到外挂 SPI flash（XIP，像原生方式 B 芯片 rk2206/STM32F407 那样内核进大 Flash），改 `link.ld.S` 的 ROM_TEXT 到外挂 flash 地址 + 调烧录脚本；内嵌 Flash 留给需高速的核心库（SRAM 加速区）。判据：开源内核精简后仍远超内嵌内核分区 → 走外挂 flash。

---

## Step 2a: Kconfig 适配链

### 4 级链结构

OpenHarmony Lite 的 Kconfig 形成从产品到组件的 4 级依赖链：

```
board Kconfig ──→ series Kconfig ──→ soc Kconfig ──→ defconfig + 组件裁剪
   (产品选择)        (系列选择)          (芯片选择)         (默认配置)
```

| 级别 | 文件位置 | 内容 | 实测状态 |
|------|---------|------|:------------:|
| Board | `device/board/{vendor}/{board}/Kconfig` | 产品型号选项菜单 | ✅ 结构正确 |
| Series | `device/board/{vendor}/Kconfig` | 同一厂商产品系列 | ✅ 继承自 board |
| SoC | `device/soc/{company}/{soc}/Kconfig` | 芯片能力声明 (RAM/外设/特性) | ✅ 结构正确 |
| Defconfig | `device/soc/{company}/{soc}/configs/{board}/defconfig` | 具体配置项默认值 | ✅ 通过编译验证 |

### 关键 CONFIG 项

```kconfig
# SoC Kconfig — 芯片能力声明
config SOC_COMPANY_{COMPANY_UPPER}
    bool
    default y

config CHIP_{SOC_MODEL_UPPER}
    bool "Support {soc_model}"
    default y

# Defconfig — 默认值
CONFIG_ARCH_{ARCH}=y            # riscv32 / arm
CONFIG_KERNEL_{KERNEL_TYPE}=y    # liteos_m / liteos_a
CONFIG_RAM_SIZE={size}           # e.g., 160 for 160KB
CONFIG_FLASH_SIZE={size}         # e.g., 2048 for 2MB
```

### ⚠️ Kconfig source 必须先 uncomment（L1-Linux binder/android 适配链前置，实测教训）

L1-Linux 适配 binder/android 子系统时，`drivers/Kconfig` 里厂商基线常带注释掉的 source 行：

```kconfig
# drivers/Kconfig（厂商基线）
# source "drivers/android/Kconfig"   ← ← 这行被注释掉了
```

**必须先去掉 `#`**，否则后续 `make olddefconfig` **静默丢弃** `CONFIG_ANDROID=y`——不会报错，但 android/binder 子系统的所有 CONFIG 项都不进 `.config`，binder 驱动根本不编。这是适配链最容易被忽略的前置：source 行没开，下游 defconfig 里写的 `CONFIG_ANDROID_BINDER_IPC=y` 等全部无效。

- **判别**：`make olddefconfig` 后 grep `.config` 里 `CONFIG_ANDROID`——若 defconfig 写了 `=y` 但 `.config` 里没有 → 回查 `drivers/Kconfig` 的 `source "drivers/android/Kconfig"` 是否被注释。
- **补法**：去 `#` → 重新 `make olddefconfig` → 确认 `CONFIG_ANDROID=y` 进 `.config`。
- 与下方 §BINDER_IPC_32BIT / §binderfs 配套：先开 source，再调 binder 相关 CONFIG。

### 参考

- 完整 Kconfig 依赖见 本步骤 `references/kernel-trim/`
- 工具: `skills/ohos-dev-kernel-source-query/` (查询已有芯片的 Kconfig)

---

## Step 2b: BUILD.gn 编译入口

### P2 配置与构建证据门控

P2 完成内核配置后，必须归档输入 defconfig SHA256、实际
`make <defconfig>`/`olddefconfig` 命令、最终 `.config` SHA256、内核源
commit、应用 patch 文件及 SHA256、工具链版本和完整构建命令。逐项检查
输入中每个显式 `CONFIG_*` 是否出现在最终 `.config`；若符号因源码缺少
Kconfig 被丢弃，标记 `CONFIG_SOURCE_GAP`，不得在 P4 以“镜像大小接近”
自动通过，必须先修复或明确阻塞。

### 两级构建文件

**Board 级** (`device/board/{vendor}/{board}/BUILD.gn`):
```gn
group("{board}_group") {
  public_configs = [ ":{board}_public_config" ]
  public_deps = [
    "//device/soc/{company}/{soc}:{soc_group}",
  ]
}
```

**SoC 级** (`device/soc/{company}/{soc}/BUILD.gn`):
```gn
group("{soc}_group") {
  public_configs = [ ":{soc}_public_config" ]
  public_deps = [
    # SOC Adapter 子目录
    ":{soc_adapter_hals}",
    ":{soc_adapter_kal",
    # SDK (如有)
    ":sdk_liteos",
  ]
}

# HAL 驱动实现
group("{soc_adapter_hals}") {
  sources = [
    # P3 填充: hal_gpio.c, hal_i2c.c, ...
  ]
  include_dirs = [ "include", "hals/include" ]
}

# KAL 抽象层
group("{soc_adapter_kal}") {
  sources = [
    # 2f 填充: cmsis_liteos.c, pthread.c, time.c, ...
  ]
  include_dirs = [ "kal/include", "kal/posix/include" ]
}
```

**⚠️ 实测经验**: `sources = []` 在 hollowed 状态是正确的。Phase B 填充时必须把实际 `.c` 文件加入。遗漏任何一个 source 都会导致 undefined reference 链接错误。

### GN 语法参考

- `skills/ohos-dev-build-config/references/gn-syntax.md`
- `skills/ohos-dev-build-config/references/error-cheatsheet.md`

---

## Step 2c: 内核启动代码 ★

> **方式 B（直接用开源 LiteOS）**：本步骤大幅简化——开源 LiteOS 在 `kernel/liteos_m/arch/` 自带启动代码（startup_S / 向量表 / 上下文切换），板级**不需要**自己写 `startup_{arch}.S` 或 `system_init.c`。只需生成：
> - `main.c`：`LOS_KernelInit()` → 板级硬件初始化（时钟/UART/中断控制器）→ OH 应用入口
> - 硬件初始化 hooks（时钟/UART/中断配置，作为 `main.c` 内函数或单独文件）
>
> 参考：`skills/ohos-dev-build-config/examples/liteos-m-direct/BUILD.gn` + QEMU esp32 的 `main.c`
>
> 以下文件组成仅适用于**方式 A（厂商内核）**——需要板级自己管启动流程。

### 文件组成（方式 A）

| 文件 | 功能 | 必要性 |
|------|------|:------:|
| `startup_{arch}.S` | 复位向量 + 栈初始化 + BSS 清零 + 跳转入口 | ✅ 必须 |
| `system_init.c` | SystemInit() 时钟/外设基础初始化 | ✅ 必须 |
| `interrupt_vectors.h` | 中断向量表定义 (ISR 函数指针数组) | ✅ 必须 |
| `los_hw.{c/h}` | 底层硬件抽象 (tick/延时/中断控制) | ✅ 必须 |

### 架构差异

| 启动要素 | ARM Cortex-M | RISC-V (Hi3861V100) | x86 |
|---------|-------------|-------------------|-----|
| 入口点符号 | `Reset_Handler` | `_start` | `_start` |
| 栈指针设置 | `MOV SP, #addr` | `la sp, _stack_bottom` | MOV ESP, addr |
| 向量表 | VTABLE 段 (.vectors) | mtvec CSR 写入 | IDT 加载 |
| BSS 清零 | 循环写零 | 循环写零 (同) | REP STOSD |
| 数据拷贝 | Flash→RAM (if RO-data in flash) | 同左 | 同左 |
| SystemInit | 时钟树配置 | PLL + 总线时钟分频 | 同 |

### ⚠️ 实测关键发现 — 启动代码可能依赖非标准指令集

Hi3861V100 的 flashboot 启动代码使用 **CSR (Control Status Register) 指令** (`csrr`/`csrw`) 来读取/写入系统寄存器。这些属于 **zicsr** 扩展，不在基础 `rv32imac` 指令集中。

**如果工具链不暴露 zicsr**:
- 现象: `Error: unknown instruction set extension: zicsr` 或 assembler error
- 修复: Wrapper Script 注入 `-march=rv32imac_zicsr` (见 compiler_fix_playbook §4)
- **这是 P1 工具链问题和 P2 启动代码的交叉点**

### 启动序列 (通用模板)

```c
// system_init.c — 通用启动流程
void SystemInit(void) {
    // 1. 时钟系统初始化 (芯片特定!)
    ClockInit();           // PLL / 分频器 / 总线时钟

    // 2. 基础外设使能 (如果需要 early UART)
    //    EarlyUartInit();   // 可选: 用于早期调试输出

    // 3. 中断控制器初始化
    InterruptControllerInit();  // NVIC / PLIC / APIC

    // 4. 设置 kernel tick 定时器
    HWTickConfig();        // SysTick / MTIME / PIT

    // 5. 不要在这里调用 HAL 驱动函数!
    //    (HAL 可能还没初始化, stub 可以, 调用不行)
}
```

### 用户交互点 — 缺少芯片启动资料时:

> **需要 {chip_model} 的启动代码参考资料。**
> 请提供以下任一来源：
> - [ ] 芯片官方 startup_S 源码 (或 URL)
> - [ ] 参考板 (如 evaluation kit) 的启动代码
> - [ ] 芯片手册的 "Reset Sequence" 章节
> - [ ] 允许我从 GT (如有) 提取启动模式作为参考

---

## Step 2d: C 库适配

### 为什么需要 (L0 vs L1)

| 系统 | C 库情况 | 是否需要此步骤 |
|------|---------|:------------:|
| **L0 (liteos_m)** | musl 子集，功能有限 | ✅ **必须** — malloc/printf/I/O 需要适配 |
| **L1 (liteos_a)** | 接近完整 musl | ⚠️ 可选 — 通常开箱即用 |

### 核心适配项

#### malloc_r / free_r — 内存分配器包装

```c
// libc_adapt/malloc_r.c
#include <sys/types.h>

// 使用 __wrap 让链接器拦截标准 malloc/free 调用
// 将其重定向到内核堆管理器

void *__wrap_malloc(size_t size) {
    return LOS_MemAlloc(OS_SYS_MEM_ADDR, size);
}

void __wrap_free(void *ptr) {
    LOS_MemFree(OS_SYS_MEM_ADDR, ptr);
}

// calloc / realloc 同理...
```

**链接器参数**: `-Wl,--wrap=malloc -Wl,--wrap=free` (在 BUILD.gn 的 ldflags 中添加)

#### vprintf / snprintf — 格式化输出

```c
// libc_adapt/printf_adapt.c
#include <stdarg.h>
#include <stdio.h>

int vprintf(const char *format, va_list ap) {
    // 重定向到 UART 输出 (或 UartPrint 函数)
    char buf[256];
    int len = vsnprintf(buf, sizeof(buf), format, ap);
    UartWrite(buf, len);     // 调用基础 UART HAL
    return len;
}

int snprintf(char *str, size_t size, const char *format, ...) {
    va_list args;
    va_start(args, format);
    int ret = vsnprintf(str, size, format, args);
    va_end(args);
    return ret;
}
```

### ⚠️ 实测发现

- `musl/include/errno.h` 有 `__attribute__((const))` 用于 void 函数 → GCC 13 报 warning → `-Werror` 提升 error → **Patch #001**: 移除 attribute
- 这类问题在 **compiler_fix_playbook.md §2 Decision Tree** 的 Warning 分类中有完整处理流程

---

## Step 2e: linker.ld 链接脚本

### 基本结构

```
MEMORY
{
    VECTORS  (rx)  : ORIGIN = 0x{vector_base}, LENGTH = {vector_size}
    TEXT     (rx)  : ORIGIN = 0x{text_base},   LENGTH = {text_size}    /* ROM_TEXT */
    RODATA   (rx)  : ORIGIN = .,                LENGTH = {rodata_size}
    DATA     (rw)  : ORIGIN = 0x{data_base},   LENGTH = {data_size}    /* RAM */
    BSS      (rw)  : ORIGIN = .,                LENGTH = {bss_size}
}

SECTIONS
{
    .vectors : { *(.vectors*) } > VECTORS
    .text    : { *(.text .text.*) } > TEXT
    .rodata  : { *(.rodata .rodata.*) } > RODATA
    .data    : { *(.data .data.*) } > DATA
    .bss     : {
        __bss_start = .;
        *(.bss .bss.* COMMON)
        __bss_end = .;
    } > BSS

    _heap_start = .;
    _heap_end = ORIGIN(BSS) + LENGTH(BSS);
}
```

### ⚠️ 实测教训 — MEMORY 区域必须预留余量

**不同 GCC 版本的代码密度差 ~0.4%/major version**。同一份源码:
- GCC 7.3.0 编译: `.text` = 278KB
- GCC 13.2.0 编译: `.text` = 279.1KB (+0.4%)

**规则**: 每个 MEMORY 区域预留 **+1~3%** 余量。

**实测案例**:
- Hi3861V100 ROM_TEXT 区域溢出 **1140 bytes** (~0.4% of 278K region)
- 修复: `ROM_TEXT_LEN` 从 `278K` 调整为 `280K` (+1024B margin)
- 这是 **GT Patch #009**, 需要 user approval (修改物理内存布局)

### 链接脚本参考

- `skills/ohos-dev-build-config/references/linker-templates.md` (多架构模板)

---

## Step 2f: KAL 内核抽象层 ★ 实测最大 Gap

> **这是实测表现最差的层 (L2: 0-72%)，也是 重点修复的目标。**
> 已产出两份参考文档，本节将它们作为核心输入。

### 2f-1: CMSIS-RTOS v2 → 目标内核映射

**实测结果**: cmsis_liteos.c PARTIAL, cmsis_liteos2.c PARTIAL (72% CMSIS API 有映射但部分不精确)

**参考文档**: `hi3861_sdk_api_crossref.md` 包含 **55+ CMSIS-RTOS v2 API 映射表**:

| CMSIS-RTOS v2 API | LiteOS-M 对应函数 | 备注 |
|-------------------|-------------------|------|
| `osKernelInitialize()` | `LOS_KernelInit()` | 直接 1:1 |
| `osKernelStart()` | `LOS_Start()` | 直接 1:1 |
| `osThreadNew()` | `LOS_TaskCreate()` | 参数转换: attr→TCB config |
| `osThreadFlagsWait()` | `LOS_EventRead()` | 事件标志位 |
| `osMutexNew()` | `LOS_MuxCreate()` | 互斥量 |
| `osSemaphoreNew()` | `LOS_SemCreate()` | 计数信号量 |
| `osTimerNew()` | `LOS_SwtmrCreate()` | 软件定时器 |
| ... (55+ entries) | | 见完整映射表 |

**优先级反转公式** (实测发现):
```
PriorityInversionRisk = (MutexHoldTime × PreemptibleTaskCount) / TickRateHz
当值 > 阈值时考虑 Priority Inheritance Mutex (PI_Mutex)
```

### 2f-2: POSIX → 目标内核映射

**实测结果**: 这是失败最严重的子集:

| 文件 | 实测得分 | 失败根因 | 实测修复 |
|------|:-----------:|---------|-------------|
| `pthread.c` | **FAIL** | ID 映射模式未知; join 实现方式未知 | ✅ `posix_ref_impl.md` §2-3 |
| `time.c` | **FAIL** | nanosleep/timer 到内核原语映射未知 | ✅ `posix_ref_impl.md` §4 |
| `file.c` | **FAIL** | FD 分区路由规则未知 | ✅ `posix_ref_impl.md` §5 |
| `libc.c` | **FAIL** | stub 不完整 | 部分覆盖 |
| `pthread_attr.c` | **PARTIAL** | 默认值 OK，边界 case 不足 | 小改即可 |
| `cmsis_liteos.c` | **PARTIAL** | 大部分 OK，少数 API 参数有偏差 | 小改即可 |

#### POSIX pthread 关键模式 (来自 `posix_ref_impl.md`)

**模式 1: Thread ID 不是整数序号**
```
❌ 常见误解: pthread_t = 0, 1, 2, 3... (递增整数)
✅ 实际实现: pthread_t = TCB 指针的数值偏移 (或 TCB 地址本身)
   原因: LiteOS-M 的 TCB 是连续数组, 线程 ID = &g_taskCBArray[index]
   操作: ID 比较 = 指针比较, ID 解引用 = 通过偏移查 TCB
```

**模式 2: pthread_join 是轮询式 (非信号量阻塞)**
```
❌ 常见误解: join = sem_wait(&thread->done_sem)  (信号量等待)
✅ 实际实现: while (!thread->exited) { LOS_TaskDelay(1); }  (轮询)
   原因: L0 内存极度受限, 不想为每个 thread 分配一个 semaphore
   性能影响: 1 tick 轮询间隔 ≈ 可接受 (join 本身不是高频操作)
```

**模式 3: nanosleep → TaskDelay**
```
POSIX nanosleep(100ms) → LOS_TaskDelay(10)  (假设 1 tick = 10ms)
POSIX timer_create + timer_settime → LOS_SwtmrCreate + LOS_SwtmrStart
```

**模式 4: FD 分区路由**
```
fd 范围    │  路由到
───────────┼──────────
0 - 3      │  socket (BSD socket 层)
4 - N      │  HiFS (本地文件系统)
N+1 - M    │  random / 其他设备
```

### 2f-3: 生成策略

```
KAL 生成流程:
│
├── 1. 读取 posix_ref_impl.md (实测产出, ~8KB)
│   ├── §2: pthread 完整实现模式 (ID/join/attr/cancel)
│   ├── §3: time 实现模式 (sleep/timer/clock)
│   ├── §4: file FD 路由规则
│   └── §5: libc stub 清单
│
├── 2. 读取 hi3861_sdk_api_crossref.md (实测产出, ~12KB)
│   ├── CMSIS-RTOS v2 → LiteOS 55+ 映射表
│   ├── 9 个 IoT HAL driver SDK API 命名约定
│   └── Common errors Top 5
│
├── 3. 按 target_kernel 类型选择映射目标
│   ├── liteos_m → LOS_* API (如上表)
│   ├── liteos_a → 对应的 LiteOS-A API
│   └── nuttx / freertos → 各自的原语
│
└── 4. 生成以下文件:
    ├── kal/cmsis/cmsis_liteos.c      (CMSIS-RTOS v2 adapter)
    ├── kal/cmsis/cmsis_liteos2.c     (CMSIS-RTOS v2 extended)
    ├── kal/posix/src/pthread.c        (POSIX threads)
    ├── kal/posix/src/pthread_attr.c   (线程属性)
    ├── kal/posix/src/time.c           (时间/定时器)
    ├── kal/posix/src/file.c           (文件 I/O)
    └── kal/posix/src/libc.c           (C 库 stub 补充)
```

---

## 引用的 tools/

| 工具 | 用途 | 路径 |
|------|------|------|
| ohos-dev-kernel-source-query | 查询 Kconfig/BUILD.gn 样本 | `skills/ohos-dev-kernel-source-query/` |
| ohos-dev-soc-spec-parse | 提取寄存器/中断号/时钟定义 | `skills/ohos-dev-soc-spec-parse/` |
| ohos-dev-build-config | GN 语法 / linker 模板 / error cheatsheet | `skills/ohos-dev-build-config/` |
| ohos-dev-kernel-trim-config | 内核组件裁剪方案 / Kconfig 依赖解析 | `skills/ohos-dev-kernel-trim-config/` |
| **compiler_fix_playbook** | **★ 工具链/启动/C库修复知识库** | `skills/ohos-dev-build-config/references/compiler_fix_playbook.md` |

## 语料索引

- **★ POSIX 实现模式**: `skills/ohos-dev-kernel-source-query/references/posix_ref_impl.md` (~8KB) ← **2f 核心输入**
- **★ SDK API 映射**: `skills/ohos-dev-board-config-gen/references/hi3861_sdk_api_crossref.md` (~12KB) ← **2f 核心输入**
- **Kconfig 源码**: 依赖说明见 本步骤 `references/kernel-trim/`
- **构建装配工具**: `skills/ohos-dev-build-config/references/` (GN/linker/error)
- **内核裁剪**: 本步骤 `references/kernel-trim/` (Kconfig 组件清单)

---

## Agent Dispatch Spec

### 分发规格

| 属性 | 值 |
|------|-----|
| **agent_role** | `kernel-expert` |
| **category** | `deep` |
| **load_skills** | `[ohos-dev-kernel-source-query, ohos-dev-soc-spec-parse, ohos-dev-build-config, ohos-dev-kernel-trim-config]` |
| **dispatch_mode** | **部分并行**: G1=[2a‖2b] → G2=串行 [2c→2d→2e→2f] |
| **parallel_groups** | G1: 2a+2b 可并行 (无依赖); G2-G5: 强顺序 |

### Agent Prompt 模板

```
1. TASK:
   为 {chip_model} ({arch}) 执行嵌入式 OS 内核移植 (Phase 2)。
   这是工作流的核心阶段 —— 内核起不来，后面全白搭。
   实测验证: L5 编译 PASS, 但 L2 KAL/POSIX 仅 0-72% (已通过 参考文档修复)。

2. 执行顺序:
   Group 1 (可并行): 2a(Kconfig链) + 2b(BUILD.gn入口)
   Group 2 (顺序): 2c(启动代码) → 2d(C库) → 2e(linker.ld) → 2f(KAL抽象层) ★ 最重要

3. 关键输入文档 (2f 必读):
   A. posix_ref_impl.md — POSIX pthread/time/file 实现模式 (ID映射/join轮询/FD分区)
   B. hi3861_sdk_api_crossref.md — CMSIS 55+ API映射 + 9个HAL命名约定
   → posix_ref_impl.md 在: skills/ohos-dev-kernel-source-query/references/
   → hi3861_sdk_api_crossref.md 在: skills/ohos-dev-board-config-gen/references/

4. 特别注意:
   - 2c 启动代码: 检查是否需要特殊指令集扩展 (如 zicsr), 见 compiler_fix_playbook §4
   - 2e linker.ld: MEMORY 区域预留 +1~3% 余量 (实测教训)
   - 2f KAL: 这是实测中失败最多的地方! 必须严格按参考文档的模式来生成
   - L0 vs L1: 2d(C库) L0必须/L1可选; 2f KAL 映射目标不同

5. EXPECTED OUTCOMES:
   ① Kconfig 4 级链完整 (board→series→soc→defconfig)
   ② BUILD.gn (SoC+Board) 含正确 sources 列表
   ③ 启动代码: startup_S + SystemInit + 向量表 + los_hw
   ④ C 库适配: malloc_r/free_r wrap + printf/snprintf
   ⑤ linker.ld: 正确的 MEMORY 布局 (有余量)
   ⑥ KAL 层: 6-7 个 .c 文件 (cmsis×2 + pthread + attr + time + file + libc)

6. MUST DO:
   - [ ] 2f 必须先读 posix_ref_impl.md 再写代码 (不要凭空想象 POSIX 实现!)
   - [ ] 2e MEMORY 区域留 +1~3% 余量
   - [ ] 2c 启动代码不含未实现的 HAL 函数调用
   - [ ] 2b sources 列表包含所有将要生成的 .c 文件
   - [ ] 区分 L0 (liteos_m) 和 L1 (liteos_a) 的不同路径

7. MUST NOT DO:
   - [ ] 不要跳过 2f 或简化它 (实测证明这是最大 gap)
   - [ ] 不要假设 pthread ID 是整数 (它是 TCB 指针/偏移)
   - [ ] 不要用 semaphore 做 pthread_join (L0 用轮询)
   - [ ] 不要让 linker.ld 区域没有余量
   - [ ] 不要在 2c 中调用未实现的 HAL 函数

8. CONTEXT:
   上游: P1 chip-spec (arch/ram/flash/system_type)
   下游: P3 (driver-dev) 消费 2b 的 BUILD.gn sources 结构
          P4 (build-verify) 消费全部产出做全量编译
```

## MUST DO (实测血泪教训)

- [ ] **2f KAL 必须先读参考文档再生成** — 实测中失败根源就是没有 POSIX 实现模式参考
- [ ] **linker.ld MEMORY 区域预留 +1~3% 余量** — 跨 GCC 版本代码密度差异 (F-009)
- [ ] **启动代码检查指令集依赖** — zicsr/zihintpause 等扩展可能需要 wrapper
- [ ] **BUILD.gn sources 不能漏文件** — 漏一个就 undefined reference
- [ ] **区分 L0/L1 路径** — C库适配和 KAL 映射目标完全不同
- [ ] **malloc 用 __wrap 模式** — 标准 L0 做法
- [ ] **2a/2b 先于 2c-2f** — 编译框架必须在内核代码之前就位

## MUST NOT DO (实测血泪教训)

- ❌ 不要凭空想象 POSIX pthread 实现 (ID/Join/Attr 都有非显而易见的模式)
- ❌ 不要让 linker.ld 区域精确匹配预期大小 (一定要留余量)
- ❌ 不要在启动代码中调用未实现的 HAL 函数
- ❌ 不要混淆 CMSIS-RTOS v1 和 v2 API (映射目标不同)
- ❌ 不要忽略 L0 的内存约束 (KAL 实现必须极简)
