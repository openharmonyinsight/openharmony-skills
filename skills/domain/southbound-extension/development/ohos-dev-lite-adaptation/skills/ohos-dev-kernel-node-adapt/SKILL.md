---
name: ohos-dev-kernel-node-adapt
description: 内核侧驱动适配器（L1-Linux 路线，kernel_family=linux）——defconfig 开 CONFIG + DTS 加节点 + 设备 ID 表两侧补条目，让 Linux 内核产出 OH init/service 依赖的 /dev 节点（watchdog/binder/hilog/cgroup 等）。L1-LiteOS 路线的内核侧配置走 ohos-dev-kernel-trim-config（LOSCFG/Kconfig），L0 驱动走 ohos-dev-hal-skeleton-gen（IoT 外设子系统）。Use during board bring-up when OH init/services fail due to missing /dev nodes or storage probe failures; triggers include 缺 /dev 节点、init reboot loop、watchdog_service 起不来、apphilogcat fd failed、samgr boot step 卡死、binder ioctl EINVAL、SPI Nand/Nor 颗粒 probe 失败、pagesize BUG、开内核驱动 CONFIG、DTS 加节点、设备 ID 表补条目、内核驱动使能。同义表达：bring-up 卡点、设备树节点适配、驱动适配（内核侧）。
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: kernel
  capability: node-adapt
  version: 0.1.0
  status: trial
---

# OpenHarmony Lite 内核驱动节点适配

> **适用路线**：本 skill 面向 **L1-Linux 路线**（target profile `kernel_family=linux`，如 Hi3516CV610）——defconfig / DTS / 设备 ID 表 / 内核 CONFIG 均为 Linux 内核机制。
> 其他路线：**L1-LiteOS** 的内核侧配置/裁剪走 `ohos-dev-kernel-trim-config`（LOSCFG / Kconfig / target_config.h）；**L0** 驱动走 `ohos-dev-hal-skeleton-gen`（IoT 外设子系统）。
> 收到上述路线的请求时改调对应 skill，不用本 skill 的 Linux 内核机制硬套。

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 缺 /dev 节点症状 | "init 起不来 reboot loop"、"watchdog_service open 失败"、"apphilogcat fd failed No such file"、"chmod /dev/xxx 文件不存在" |
| binder 协议症状 | "binder ioctl c0186201 returned -22 EINVAL"、"samgr boot step -9"、"/dev/binder 不存在" |
| 颗粒 probe 失败 | "spi nand id: 0xe5 0xf1 识别不了"、"bsp_spi_nand_probe error -19"、uboot "pagesize 8192" BUG |
| 驱动使能任务 | "把 XX 内核驱动打开"、"defconfig 加 CONFIG"、"DTS 加 wdt/uart 节点"、"SPI Nand ID 表补条目" |
| 链式调用 | ohos-issue-lite-diagnose 定位到 BG003（SPI Nand ID 表）/ OH001（binder 协议位宽）类根因后转来做修复；03-driver-device B4/B5/SPI Nand 段路由过来 |
| 同义表达 | 内核驱动使能 / 设备树节点适配 / bring-up 卡点 / 驱动适配（内核侧） |

**不触发**（明确排除）：生成用户态 HAL/HDF 驱动骨架代码（走 ohos-dev-hal-skeleton-gen）；提取芯片寄存器/中断/时钟规格做结构化画像（走 ohos-dev-soc-spec-parse）；用户明确只要 rootfs 侧绕过且不要驱动适配（仍应提醒绕过是技术债）。

## Scope

本 SKILL 是 OpenHarmony Lite 芯片适配的**内核侧驱动适配**：通过改内核 defconfig（开 `CONFIG_*`）+ DTS（加/改设备节点）+ 设备 ID 表（SPI Nand/Nor/USB vendor ID 表**uboot 与内核两侧**补条目），让内核产出 OH init/service 依赖的 `/dev` 节点（`/dev/watchdog`、`/dev/binder`、`/dev/hilog`、`/dev/ttyS*`、cgroup 等），打通 bring-up 最常卡的一关。

**本 SKILL 管内核侧（CONFIG/DTS/ID 表）**，区别于 `ohos-dev-hal-skeleton-gen`（生成**用户态** HAL/HDF 驱动骨架代码）。两者互补：ohos-dev-hal-skeleton-gen 产出 `.c/.h/HCS` 驱动骨架，本 SKILL 产出内核 defconfig/DTS/ID 表改动让驱动真正起来并出现 `/dev` 节点。

### 何时用

- 板子 bring-up 缺 `/dev` 节点（watchdog/binder/hilog/ttyS 等）→ OH init/service 起不来或 reboot loop。
- SPI Nand / SPI Nor 颗粒 probe 失败（uboot `pagesize 8192` BUG / 内核 `bsp_spi_nand_probe error -19`）。
- 新内核驱动使能（开 CONFIG + 加 DTS 节点 + 可能补 ID 表）。

> **原则（关联 memory `prefer-driver-adaptation-over-rootfs-bypass`）**：缺 `/dev` 节点优先做内核侧驱动适配，不要只靠 rootfs 侧绕过（init.cfg 删 service、mknod 假节点）。绕过是权宜，驱动适配才是 bring-up 正路；且要**全量审计**缺口，不只修当前报错那个。

**输入**：目标内核源码路径（defconfig/DTS/ID 表所在树）、缺什么 /dev 节点或哪个颗粒 probe 失败（症状/日志）、颗粒 ID（ID 表类任务，uboot 打印或 JEDEC ID）。
**输出**：内核侧改动集（defconfig CONFIG 增开 + DTS 节点增改 + ID 表两侧补条目）+ 重编/重烧/验证步骤说明。**不产出**用户态驱动代码（ohos-dev-hal-skeleton-gen 负责）、不做问题根因诊断（ohos-issue-lite-diagnose 负责，诊断完路由到本 SKILL 修复）。

## Initial Checks

收到任务后，按以下顺序先做判断（各步结论决定后续路径）：

1. **症状归类**：缺 /dev 节点（init/service 起不来）→ Step 1 缺口审计；颗粒 probe 失败 → Step 4 ID 表；新驱动使能 → Step 2-3 CONFIG+DTS。
2. **缺口全量盘点**（不只当前报错那个）：把 init.cfg pre-init 的 chmod/chown 路径 + 各 service 依赖的 /dev 节点列全，逐个对 defconfig + DTS 找缺口。
3. **CONFIG 可达性确认**：defconfig 里要开的 CONFIG 在内核 Kconfig 中是否存在；`drivers/Kconfig` 对应 `source` 行是否被注释（注释则驱动不编入）。
4. **32 位小系统判定**：32 位 ARM OH 小系统的 binder 需额外 `BINDER_IPC_32BIT`（见 Step 4 / binder playbook），且关 BINDERFS。
5. **颗粒信息来源盘点**：ID 表类任务先抓颗粒 ID（uboot 启动打印 / JEDEC ID）；datasheet 是否可得——查不到时以能跑的 bin 的 runtime print 为权威，不猜。
6. **绕过 vs 适配判定**：用户只要 rootfs 绕过时，按 Scope 原则提醒"驱动适配才是正路 + 绕过标注技术债"，不默默配合绕过。

## Prohibited Practices（禁止操作）

| 禁止 | 正确做法 |
|------|---------|
| 缺 `/dev/watchdog` 只在 rootfs 删 `watchdog_service` 绕过 | defconfig 开 `CONFIG_WATCHDOG`+`CONFIG_DW_WATCHDOG` + DTS 加 wdt 节点 + 重编；rootfs 绕过仅短期权宜并标注技术债 |
| 凭记忆猜驱动基地址/时钟/中断号 | 查 SoC TRM（HiSilicon NDA）→ TRM 拿不到先用宿主联网检索能力（WebSearch 或等价物；坏用备选联网检索 CLI，如 opencode）→ 仍查不到别猜地址，报 blocker 标注信息来源与已查渠道 |
| SPI Nand/Nor ID 表只补一侧 | uboot 与内核是**两份独立的源文件**（`raw/fmc100/` vs `fmc100/`），两侧都补，否则一侧识别另一侧 probe 失败 |
| 从零写 ID 表条目（字段多易错） | 照抄同表同厂商前缀、同规格（pagesize/OOB）的现有条目，只改 id + name，参数按颗粒规格书核对 |
| 颗粒无 datasheet 就猜 page/OOB/容量 | 以**能跑的 bin 的 runtime print** 为权威（`Page:2KB OOB:128B` / `spi nand id: 0xe5 0xf1`），runtime 实测 > datasheet |
| `/dev/hilog` 缺失靠 OH init 原生 `mknod` | OH init **无 mknod 命令**，要 `exec /bin/busybox mknod /dev/hilog c 245 0`；major 号从 `/proc/devices` 查实际分配值，别猜 |
| 32 位 OH 小系统 binder 不开 `BINDER_IPC_32BIT` | 32 位 ARM 必须在内核 binder.h 加 `#define BINDER_IPC_32BIT 1` 对齐 user 态 24B 结构体，否则 `ioctl -22 EINVAL` ×400 |
| DTS 改了不走 `make dtbs` | DTS 改动必走 `make dtbs` 重编设备树；uImage 按内核重编后必走 FIT 重做 |
| 只查当前报错那一个节点 | 把 init.cfg pre-init 的 chmod/chown 路径 + service 依赖的 `/dev` 节点列出来，逐个对内核配置全量审计缺口 |

---

## ① 文件路由表

根据适配对象，读取对应的 playbook。**每次只读一个**，不要一次性加载所有 reference。

| 适配对象 / 症状 | Agent 读取 | 预估行数 |
|---------|-----------|:-------:|
| 缺 `/dev/watchdog` → watchdog_service open 失败 → init reboot loop | `references/watchdog-adapter-playbook.md` | ~80 |
| 缺 `/dev/hilog` → apphilogcat `fd failed No such file` | `references/hilog-adapter-playbook.md` | ~70 |
| binder `ioctl c0186201 returned -22 EINVAL` ×400 → samgr `boot step -9` | `references/binder-adapter-playbook.md` | ~110 |
| SPI Nand 颗粒 probe 失败（uboot `pagesize 8192` BUG / 内核 `-19`） | `references/spi-nand-id-table-playbook.md` | ~120 |
| 查 CONFIG → /dev 节点 → OH service 依赖映射（哪个 CONFIG 出哪个节点） | `references/config-devnode-map.md` | ~120 |
| 查驱动框架差异 / L0 vs L1 驱动模型 | 调 `ohos-dev-hal-skeleton-gen` skill | — |
| 查芯片寄存器基地址/中断/时钟规格 | 调 `ohos-dev-soc-spec-parse` skill | — |
| 查完整诊断案例（BG003 DS35Q1GB / OH001 binder -22） | `../ohos-issue-lite-diagnose/references/diagnostic-cases.md` §8 BG003 / §9 OH001 | — |

---

## ② 工作流

### Step 1: 审计 /dev 节点缺口（不只查当前报错那个）

缺 `/dev` 节点导致 OH init/service 起不来时，先做全量审计：

1. **列需求**：把 OH `init.cfg` pre-init 的 `chmod`/`chown` 路径 + 各 service 依赖的 `/dev` 节点列出来（如 `chmod 0666 /dev/binder`、`chown 4 4 /dev/hilog`、`watchdog_service` 依赖 `/dev/watchdog`）。
2. **逐个对内核配置找缺口**：每个 `/dev` 节点对应内核一个 `CONFIG_*` + DTS 节点，查 defconfig（CONFIG 开没开）+ DTS（节点在不在、`status` 是不是 `"okay"`）。
3. **全量列出缺口**：不只修当前报错那个——把全部缺的驱动一次性列出来（避免一个个报错才发现，实测教训）。

常见要审计的节点见 `references/config-devnode-map.md`（watchdog/binder/hilog/ttyS/cgroup 等，含缺失症状）。

### Step 2: defconfig 开 CONFIG

逐个缺口开对应的 `CONFIG_*`（在芯片 defconfig，如 `arch/arm/configs/hi3516cv610_defconfig`）：

| /dev 节点 | 要开的 CONFIG | 备注 |
|---|---|---|
| `/dev/watchdog` | `CONFIG_WATCHDOG=y` + `CONFIG_DW_WATCHDOG=y` | Synopsys DesignWare WDT（hi3516cv610 用 dw wdt） |
| `/dev/binder`、`/dev/hwbinder`、`/dev/vndbinder` | `CONFIG_ANDROID=y` + `CONFIG_ANDROID_BINDER_IPC=y` | 32 位 OH 小系统额外加 `BINDER_IPC_32BIT`（见 Step 4 / binder playbook），**关 BINDERFS** 用 misc_register/devtmpfs |
| `/dev/hilog` | `CONFIG_HILOG=y` + `CONFIG_STAGING=y` | hilog 驱动在 `drivers/staging/hilog` |
| cgroup 相关 | `CONFIG_CGROUPS=y` + `CONFIG_CGROUP_FREEZER=y` | 部分 service 依赖 |
| `/dev/ttyS*` | 对应 UART 驱动 CONFIG（如 `CONFIG_SERIAL_8250`） | + DTS uart 节点 |

完整 CONFIG → /dev 节点 → OH service 依赖 → 缺失症状映射表见 `references/config-devnode-map.md`。

> 开 CONFIG 后注意 `drivers/Kconfig` 里对应 `source` 行是否 uncomment（如 binder 驱动要在 `drivers/Kconfig` 有 `source "drivers/android/Kconfig"`，被注释掉则驱动不编入）。

### Step 3: DTS 节点适配

defconfig 开了 CONFIG 仍不够，DTS 要有对应节点且 `status = "okay"`：

1. **查/加节点**：在芯片 DTS（如 `arch/arm/boot/dts/hi3516cv610.dtsi`）加或改节点，含 `compatible` + `clocks` + `status = "okay"` + `interrupts` + `reg`。
2. **子系统节点规范**：
   - wdt：`compatible = "snps,dw-wdt"`（Synopsys DesignWare）+ `clocks` + `reg`（基地址，如 hi3516cv610 `wdg@0x11030000`）
   - uart：`compatible` 按厂商（如 `arm,pl011`）+ `interrupts` + `clocks` + `status`
   - mmc / display / touch：按各子系统规范，参考芯片参考板 DTS
3. **重编 dtbs**：DTS 改了必走 `make dtbs` 重编设备树，再重编 zImage；uImage 按内核重编后必走 FIT 重做（见 02-kernel-port「内核重编后 uImage 必走 FIT」）。

各子系统 DTS 节点规范细节见对应 playbook（watchdog 见 `references/watchdog-adapter-playbook.md`）。

### Step 4: 设备 ID 表两侧补条目

SPI Nand / SPI Nor / USB 等 vendor ID 表，uboot 侧与内核侧是**两份独立的源文件**，两侧都要补：

1. **抓颗粒 ID**：uboot 启动早期打印（如 `spi nand id: 0xe5 0xf1`）或读 JEDEC ID。`0xe5`=厂商前缀，`0xf1`=颗粒型号。
2. **grep 确认不在表**：两侧 ID 表源文件都 grep（如 hi3516cv610：uboot `drivers/mtd/nand/raw/fmc100/fmc_ids_hi3516cv610.c` + 内核 `drivers/mtd/nand/fmc100/fmc_ids_hi3516cv610.c`，路径差一层 `raw/` 但独立）。
3. **照抄同规格条目改 id**：找同表同厂商前缀（如 `0xe5`）、同 pagesize/OOB 的现有条目复制，只改 id + name，参数按颗粒规格书核对。别从零写条目。
4. **两侧都补**：uboot 侧 + 内核侧都补条目，重编 uboot + 内核，重烧。

> 颗粒无 datasheet 时，以**能跑的 bin 的 runtime print** 为权威填规格（`Page:2KB OOB:128B`），别猜。完整 ID 表适配流程 + DS35Q1GB-IB 实例见 `references/spi-nand-id-table-playbook.md`。

### Step 5: 验证

1. **重编**：defconfig 改了重编 zImage；DTS 改了走 `make dtbs` + 重编 zImage；uImage 按 02-kernel-port 重做 FIT；ID 表改了重编对应侧（uboot / 内核）。
2. **烧后验证节点出现**：`ls /dev/watchdog`（或对应节点）确认出现；`cat /proc/devices` 查驱动注册的主设备号（hilog major 245 等）。
3. **验证 OH service 起来**：`ps -A` 对照 init.cfg services 列表核对（watchdog_service / samgr / foundation / hiview 等起来，不再 reboot loop / boot step 卡死）。
4. **改烧录件记 changelog**：改 uImage/rootfs 等烧录件后立即更新 `CHANGES_*.md`（md5 + 改动 + 根因），关联 memory `update-changelog-after-burnfile-change`。

---

## ③ 与其他 skill / 工作流的关系

| 关系 | 说明 |
|------|------|
| **互补 `ohos-dev-hal-skeleton-gen`** | ohos-dev-hal-skeleton-gen 生成**用户态** HAL/HDF 驱动骨架（.c/.h/HCS）；本 SKILL 管**内核侧** CONFIG/DTS/ID 表让驱动起来。缺 `/dev` 节点属本 SKILL 范畴。 |
| **P3 `{{ASSET_ROOT}}/workflow/steps/03-driver-device`** | 03-driver-device 是方法论（含 B4 watchdog / B5 hilog / SPI Nand ID 表段），本 SKILL 把这些内核侧适配独立成可发现 skill。03-driver-device B4/B5/SPI Nand 段有指针指向本 SKILL。 |
| **P7 `ohos-issue-lite-diagnose`** | BG003（DS35Q1GB ID 表）/ OH001（binder -22）案例路由到本 SKILL 做适配修复。本 SKILL 是 P7 这类 bring-up 卡点的修复侧。 |
| **`ohos-dev-soc-spec-parse`** | 驱动基地址/中断/时钟规格查 ohos-dev-soc-spec-parse（命中知识库直接用，未命中联网查）。 |
| **memory `prefer-driver-adaptation-over-rootfs-bypass`** | 缺 /dev 节点优先驱动适配不靠 rootfs 绕过的原则依据。 |

### P3 / P7 路由复用

- **P3（驱动开发）**：bring-up 缺 `/dev` 节点 / 颗粒 probe 失败 → 从 03-driver-device B4/B5/SPI Nand 段路由到本 SKILL 做内核侧适配。
- **P7（问题诊断）**：ohos-issue-lite-diagnose 诊断到 BG003（SPI Nand ID 表）/ OH001（binder 协议位宽）/ §7.1（mknod 陷阱）类根因 → 路由到本 SKILL 做 defconfig/DTS/ID 表修复。

---

## Exceptions and Fallbacks（异常与兜底）

信息不足、查询失败、改了不生效时的处理规则（按场景）：

| 场景 | 处理 |
|------|------|
| **SoC TRM 拿不到**（基地址/时钟/中断号未知） | 降级链：查 SoC TRM（HiSilicon NDA）→ TRM 拿不到先用联网检索（WebSearch 或等价物；坏用备选 CLI 如 opencode）→ 仍查不到**别猜地址**，报 blocker 标注信息来源与已查渠道；可联动 ohos-dev-soc-spec-parse 查开源 DTS/SDK 中的同 SoC 节点 |
| **颗粒无 datasheet**（page/OOB/容量定不了） | 以能跑的 bin 的 runtime print 为权威（`Page:2KB OOB:128B` / `spi nand id: 0xe5 0xf1`），runtime 实测 > datasheet，不猜规格（见 Prohibited Practices） |
| **defconfig 开了 CONFIG 但 /dev 节点仍不出现** | 逐层排查：`drivers/Kconfig` 对应 source 行是否被注释 → DTS 节点是否存在且 `status = "okay"` → 是否走了 `make dtbs` 重编 → 烧的镜像是否是重编后的（md5 核对） |
| **ID 表补了一侧仍 probe 失败** | 检查另一侧——uboot 与内核是两份独立源文件（路径差一层 `raw/`），两侧都补齐再重编重烧 |
| **`/dev/hilog` 缺失且 OH init 原生 mknod 无效** | OH init 无 mknod 命令，需 `exec /bin/busybox mknod /dev/hilog c 245 0`；major 号从 `/proc/devices` 查实际分配值，不猜 |
| **binder 开了 CONFIG 仍 `ioctl -22 EINVAL`** | 检查 32 位系统是否在内核 binder.h 加 `#define BINDER_IPC_32BIT 1` 对齐 user 态 24B 结构体；BINDERFS 是否误开（应用 misc_register/devtmpfs） |
| **重编后启动行为不变** | 确认烧录件真更新了（md5）+ uImage 是否按 FIT 重做（legacy 无 dtb 会 bootm 复位）+ dtbs 是否重编 |
| **改完烧录件** | 立即更新 `CHANGES_*.md`（md5 + 改动 + 根因），关联 memory `update-changelog-after-burnfile-change` |
