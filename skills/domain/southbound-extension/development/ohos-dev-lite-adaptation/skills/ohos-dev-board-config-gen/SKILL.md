---
name: ohos-dev-board-config-gen
description: >-
  OpenHarmony Lite 芯片适配的设备配置层——生成描述芯片硬件外设/引脚/内存映射的配置文件（L0: config.gni/board_config.h/linker.ld/target_config.h；L1: config.gni/soc.gni/defconfig/DTS/hdf.hcs/device_info.hcs/各外设 *_config.hcs）。Use when hardware-description config files are needed for an OpenHarmony Lite (L0/L1) adaptation; triggers include 设备配置生成、board_config 宏、HCS 文件、device_info.hcs、match_attr 配对、*_config.hcs 怎么写、defconfig 生成、CONFIG_XXX depends on 依赖断裂、对照官方 defconfig 金标准、hc-gen 编译报错、0x3516CV610 非法 hex、target_config.h、L1 漏 HCS 导致驱动加载失败、引脚/寄存器/中断号配置。
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: board
  capability: config-gen
  version: 0.1.0
  status: trial
---

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 完整生成任务 | "给 XX 板生成设备配置"、"生成 HCS 配置"、"写 defconfig / DTS"、"生成 board_config.h" |
| 单点配置问题 | "match_attr 怎么配"、"uart_config.hcs 怎么写"、"这个 CONFIG 依赖什么"、"寄存器基地址填多少" |
| 症状词（隐性需求） | "驱动加载失败是不是 match_attr 没配对"、"hc-gen 报错"、"0x3516CV610 编译不过"、"SPI Nand 编译不进"、"HDF 没有设备节点树"、"L1 驱动全加载失败"、"启动找不到 DTB"、"无法 reboot" |
| 下游 skill 链式调用 | ohos-dev-build-config 装配前需要设备配置；ohos-dev-hal-skeleton-gen 需要 HCS 对端/硬件参数 |
| 同义表达 | 板级配置 / 设备树配置 / 硬件描述文件 / Kconfig 配置 / 内核 defconfig |

**不触发**（明确排除）：驱动 .c/.h 代码生成（→ ohos-dev-hal-skeleton-gen）；构建注册文件 config.json/ohos.build/hals（→ ohos-dev-build-config）；内核组件级 LOSCFG 裁剪（→ ohos-dev-kernel-trim-config）；芯片规格提取（→ ohos-dev-soc-spec-parse）。

## Scope

本 SKILL 是 OpenHarmony Lite（L0 轻量系统 / L1 小型系统）新芯片适配的**设备配置层**：生成描述芯片硬件外设、引脚、内存映射的配置文件，让 HDF 驱动框架（L1）或板级代码（L0）能正确发现并初始化硬件。

### 生成文件清单

| 系统级别 | 本 SKILL 生成的文件 | 说明 |
|---------|-------------------|------|
| **L0** | `config.gni`、`board_config.h`、`linker.ld`、`target_config.h` | 编译时常量，无运行时解析 |
| **L1** | `config.gni`、`hdf.hcs`、`device_info.hcs`、各外设 `*_config.hcs` | 运行时 HCS Parser 解析 |

> 文件已存在时检查内容正确性而非覆盖。`target_config.h` 只生成最小可用骨架。

**输入**：结构化芯片规格（首选上游 ohos-dev-soc-spec-parse 的 `chip_spec.json`）+ 硬件连接描述（引脚分配/原理图，可选）+ 厂商 SDK（寄存器地址/CRG 偏移/autoconf.h CONFIG 值核实来源，如有）。
**不适用**：驱动实现代码；构建装配；已验证通过配置的单值编辑任务。

## Initial Checks

收到任务后，按以下顺序先做判断（各步结论决定后续路径）：

1. **系统级别 L0/L1 判定**：决定两套完全不同的文件清单（L0 = 4 文件编译时 C 宏；L1 = 12-18 文件含 11 个 HCS 必生成）。判错级别 = 产出方向全错。
2. **输入齐全度盘点**：芯片名/架构/Flash/RAM/外设清单为基本必填；L1 额外必填各外设寄存器基地址、中断号、驱动 moduleName——缺失先追问用户或回 ohos-dev-soc-spec-parse，不猜。
3. **defconfig 任务的金标准定位**：先找到官方 `arch/arm/configs/<chip>_defconfig` + 对应 Kconfig 源（SDK/内核源码树/联网查询）——依赖链核对必须有金标准作对照，无金标准先声明再补。
4. **文件已存在 or 新建**：已存在 → 检查内容正确性而非覆盖。
5. **hc-gen 可用性**：决定 L1 语法验证用工具编译还是人工三层验证 + 留命令给用户。
6. **RISC-V vs ARM 判定**：march/mabi 规则不同（RISC-V 不用 `-mcpu`，board_cpu 留空），影响 config.gni 生成。

## Prohibited Practices（设备配置禁止操作）

| 禁止 | 正确做法 |
|------|---------|
| 凭经验填 march/mabi/-mcpu | 从厂商 SDK/工具链提取实际值；RISC-V 不用 `-mcpu`（见 config-gni-guide） |
| 生成 `peripherals.json` 虚构文件 | 外设使能/波特率信息并入 `board_config.h` 宏 |
| 在 target_config.h 做深度特性裁剪 | 本 SKILL 只生成最小可用骨架 |
| match_attr 两侧拼写不一致 | device_info.hcs 的 deviceMatchAttr 必须与 *_config.hcs 的 match_attr **严格相等** |
| L0 用 HCS / L1 用 board_config.h | L0 = 编译时 C 宏；L1 = 运行时 HCS |
| L1 只生成 config.gni/defconfig/DTS，漏 HCS | L1 产出**必须含** `device_info.hcs` + `hdf.hcs` + 各外设 `*_config.hcs`（gpio/uart/i2c/spi/pwm/adc/watchdog/rtc 等）。实测翻车根因：device-config 只生成 config.gni/soc.gni/defconfig/dts/target_config.h，完全漏了 HCS 文件——L1 无 HCS 则 HDF 驱动框架无设备节点树，所有 HDF 驱动加载失败 |
| 只核 CONFIG 名存在于 Kconfig，不核 `depends on` 链 | **必须对照官方 `arch/arm/configs/<chip>_defconfig` 金标准**逐条核对：每个 `CONFIG_XXX=y` 的 `depends on` 链全部满足（如 `MTD_SPI_NAND_FMC100 depends on MFD_BSP_FMC && MTD_SPI_NAND_BSP`——只开 FMC100 不开 MFD_BSP_FMC 则依赖断裂；`BSP_TIMER depends on PM`——无 PM 则不生效）。漏开依赖项编译器不报错但走不到编译分支，必须人工查 Kconfig `depends on` + 对照官方 defconfig 补齐 |
| 跳过 Step 4 三层验证直接交付 | 语法→语义→交叉三层逐条过，match_attr 不过则驱动静默加载失败 |
| 取不到的配置值直接标 TODO 留空 | **先上网查（用宿主联网检索能力，WebSearch 或等价物；坏用备选联网检索 CLI，如 opencode）**，查到填值并注明来源；确实查不到才标 TODO 并注明来源/查询关键词，禁止凭记忆编造或留空 |
| 修改 `build/` 或 `build/lite/` 平台模板 | 平台模板只读；本 SKILL 只生成 vendor/device 侧文件 |

---

## ① 文件路由表

根据用户意图，读取对应的参考文件。**每次只读一个**，不要一次性加载所有 reference。

| 用户意图 | Agent 读取 | 预估行数 |
|---------|-----------|:-------:|
| 生成 config.gni（设备硬件字段） | `references/config-gni-guide.md` | ~150 |
| 生成 board_config.h（L0 引脚/外设宏） | `references/config-templates.md` | ~230 |
| 生成 linker.ld（链接脚本） | `references/linker-templates.md` | ~200 |
| 生成 target_config.h（最小骨架） | `references/target-config-guide.md` | ~120 |
| HCS 语法 / hc-gen / 目录结构 | `references/hcs-syntax-and-config.md` | ~490 |
| 生成 L1 各外设 *_config.hcs（gpio/uart/i2c/spi/pwm/adc） | `references/config-templates.md` | ~230 |
| 查 L0/L1 文件清单 + 参考来源 | `references/config-file-checklist.md` | ~180 |
| 查外设配置项知识库 / 常见错误 | `references/product-config-examples.md` | ~210 |
| 查 L1 实战模式（config.gni/soc.gni/defconfig/DTS/HCS） | `references/l1-config-patterns.md` | ~300 |
| 查询真实芯片配置样本 | 查 `examples/<level>/<chip>/` 目录或搜索 `target_config.h` / `board_config.h` | — |
| 需要参照已有芯片配置 | `examples/<level>/<chip>/` 目录 | ~50/套 |
| 参照官方 BUILD.gn 结构（含 WiFi 头文件） | Hi3861 课程 4 个 GN 样本 + Makefile | `references/hi3861_build_gn_samples/` (5 files) |

### 系统级别 → 样本目录映射

| 系统级别 | 代表芯片 | 样本目录 |
|---------|---------|---------|
| L0 轻量系统（MCU） | Hi3861 | `examples/l0/hi3861/` |
| L0 轻量系统（MCU） | STM32F407 | `examples/l0/stm32f407/` |
| L1 小型系统（MPU） | Hi3516DV300 | `examples/l1/hi3516dv300/` |

---

## ② 工作流

### Step 1: 收集芯片规格

生成任何配置文件前，必须收集以下信息（缺失项需追问用户）：

| 必填项 | 说明 | 示例 |
|-------|------|------|
| 芯片名称 | 芯片型号 | Hi3861V100 / STM32F407ZG |
| CPU 架构 | 核心类型 | rv32imac / cortex-m4 / cortex-a7 |
| Flash 基地址 + 大小 | 十六进制地址和容量 | 0x00000000, 2MB |
| RAM 基地址 + 大小 | 十六进制地址和容量 | 0x40000000, 352KB |
| 系统级别 | L0 (Mini) / L1 (Small) | L0 |
| device_company / board | 厂商名 / 板名 | hisilicon / hispark_pegasus |
| 外设清单 | 需要配置的外设及引脚 | UART0: TX=GPIO9, RX=GPIO10 |
| 厂商 SDK 是否就绪 | 决定 config.gni include_dirs 写法 | 已有 SDK / 暂无 |

**L1 额外必填**：

| 必填项 | 说明 |
|-------|------|
| 各外设寄存器基地址 | 从 Datasheet Memory Map 章节获取 |
| 各外设中断号 | 从 Datasheet 中断向量表获取 |
| 驱动模块名（moduleName） | 从厂商驱动或 HDF 框架获取 |

### Step 2: 判定系统级别

根据用户输入确定 L0 或 L1：

```
系统级别判定：
├── L0（MCU, LiteOS-M, <128KB RAM）
│   └── 生成：config.gni + board_config.h + linker.ld + target_config.h
│       （4 个文件，编译时常量，无运行时解析）
│
└── L1（MPU, LiteOS-A / L1-Linux, >1MB RAM）
    └── 生成：config.gni + soc.gni + defconfig + DTS + hdf.hcs + device_info.hcs + 各外设 *_config.hcs
        （12-18 个文件，运行时 HCS Parser 解析）
        ★ HCS 文件（hdf.hcs + device_info.hcs + *_config.hcs）必生成，漏了则 HDF 驱动框架无设备节点树
```

> **实测翻车根因**：ohos-dev-board-config-gen 在 L1 场景只生成 config.gni/soc.gni/defconfig/dts/target_config.h，**完全漏了 HCS 文件**——L1 无 HCS 则 HDF 驱动框架无设备节点树，所有 HDF 驱动加载失败。L1 产出清单必须含 `hdf.hcs` + `device_info.hcs` + 各外设 `*_config.hcs`。

### Step 3: 按顺序生成文件

对每个文件，先 Read 对应的参考文件，再生成内容。

#### L0 生成顺序

```
config.gni → board_config.h → linker.ld → target_config.h
```

1. **config.gni**：Read `references/config-gni-guide.md`，参照 `examples/l0/<chip>/config.gni`
2. **board_config.h**：Read `references/config-templates.md`，参照 `examples/l0/<chip>/board_config.h`。外设使能/波特率信息写入此文件的宏定义
3. **linker.ld**：Read `references/linker-templates.md`，参照 `examples/l0/<chip>/linker.ld`
4. **target_config.h**：Read `references/target-config-guide.md`，参照 `examples/l0/<chip>/target_config.h`。只生成最小可用骨架

#### L1 生成顺序

```
config.gni → soc.gni → defconfig → DTS → hdf.hcs → device_info.hcs → 各外设 *_config.hcs（gpio → uart → i2c → spi → pwm → adc → watchdog → rtc → mmc）
```

1. **config.gni**：Read `references/config-gni-guide.md`，参照 `references/l1-config-patterns.md` §config.gni
2. **soc.gni**：Read `references/config-gni-guide.md`，参照 `references/l1-config-patterns.md` §soc.gni（SoC 标识/工具链/SDK 路径/媒体开关）
3. **defconfig**：Read `references/l1-config-patterns.md` §defconfig（核心依赖链 + 对照官方金标准）
   - **必检**：每个 `CONFIG_XXX=y` 的 `depends on` 链全部满足（查 Kconfig），对照官方 `arch/arm/configs/<chip>_defconfig` 逐条核对
   - 常见依赖断裂：`MTD_SPI_NAND_FMC100 depends on MFD_BSP_FMC`、`BSP_TIMER depends on PM`、`UBIFS_FS depends on MTD_UBI`
   - 常见漏项：`POWER_RESET_BSP`（无法 reboot）、`ARM_APPENDED_DTB`/`ARM_ATAG_DTB_COMPAT`（启动找不到 DTB）、`VFP`/`NEON`（FPU）、`MTD_UBI`（有 UBIFS 无 UBI）
4. **DTS**：Read `references/l1-config-patterns.md` §DTS（设备节点 + compatible + interrupts + reg）
5. **hdf.hcs**：Read `references/hcs-syntax-and-config.md`（HCS 语法 + include 入口）
6. **device_info.hcs**：同上（设备节点树 + template/::/match_attr 语法），参照 `examples/l1/<chip>/device_info.hcs` + `references/l1-config-patterns.md` §device_info.hcs
7. **各外设 *_config.hcs**：Read `references/config-templates.md`（各外设 HCS 模板），参照 `references/product-config-examples.md`（外设配置项知识库）+ `references/l1-config-patterns.md` §*_config.hcs

**关键约束**：
- device_info.hcs 的每个 `deviceMatchAttr` 值必须与对应 `*_config.hcs` 的 `match_attr` 值**严格相等**，否则驱动静默加载失败
- **HCS 文件必生成**：L1 产出清单必须含 `hdf.hcs` + `device_info.hcs` + 各外设 `*_config.hcs`，漏了则 HDF 驱动框架无设备节点树（实测翻车根因）
- **defconfig 核依赖链必检**：不只核 CONFIG 名存在于 Kconfig，还要核 `depends on` 链 + 对照官方 defconfig 金标准（实测翻车根因：缺 `MFD_BSP_FMC` 致 `MTD_SPI_NAND_FMC100` 依赖断裂）

### Step 4: 三层验证

生成所有文件后，逐层检查。任一层有 ERROR 项未通过则必须修正后重新验证。

#### 层 1：语法验证

| 检查项 | 方法 | 级别 |
|--------|------|------|
| HCS 括号配对 | 检查 `{}` 配对完整 | ERROR |
| HCS 分号完整 | 每个属性以 `;` 结尾 | ERROR |
| HCS template 合规 | template 实例未新增/删除属性 | ERROR |
| C 头文件语法 | `#ifndef`/`#define`/`#endif` 配对 | ERROR |
| config.gni GN 语法 | 变量赋值、列表语法正确 | ERROR |
| linker.ld 语法 | MEMORY/SECTIONS 语法正确 | ERROR |

L1 额外：用 hc-gen 编译验证：
```bash
hc-gen -o /dev/null hdf.hcs
```

#### 层 2：语义验证

| 检查项 | 方法 | 级别 |
|--------|------|------|
| 寄存器地址冲突 | 各外设 [regBase, regBase+regSize) 无重叠 | ERROR |
| 中断号冲突 | 各外设 irqNum 无重复 | ERROR |
| 引脚复用冲突 | 同一物理引脚未被分配给多个外设 | ERROR |
| match_attr 唯一性 | 所有 match_attr 值全局唯一 | ERROR |
| march/mabi 三处一致 | config.gni 的 board_arch + board_cflags(-march/-mabi/-mcpu) == 厂商 SDK/工具链实际值；RISC-V 不用 -mcpu | ERROR |
| MEMORY 地址一致 | linker.ld MEMORY 地址与 config.gni / 用户提供参数一致 | ERROR |
| 数值范围合法 | 波特率、频率等在合理范围 | WARNING |

#### 层 3：交叉验证

| 检查项 | 方法 | 级别 |
|--------|------|------|
| **L1 HCS 文件生成完整性** | L1 产出清单必须含 `hdf.hcs` + `device_info.hcs` + 各外设 `*_config.hcs`（gpio/uart/i2c/spi/pwm/adc 等）。漏任一类 = ERROR（实测翻车根因：完全漏了 HCS） | ERROR |
| **match_attr 配对** | device_info.hcs 的每个 deviceMatchAttr 在 *_config.hcs 中有对应 match_attr，**两侧字符串严格相等** | ERROR |
| **match_attr 运行时配对** | 两侧字符串相等之外，确认 `device_info.hcs` 里实际有 deviceNode 用了该 `moduleName`+`deviceMatchAttr`（不只配对字符串，要配对到 deviceNode 实例） | ERROR |
| 设备节点↔资源配置对应 | 每个 deviceNode 都有对应的资源配置节点 | ERROR |
| include 链完整 | hdf.hcs 包含了所有必要的子配置文件 | ERROR |
| config.gni 字段交叉 | config.gni 的 kernel_type 与系统级别一致（L0: liteos_m / L1: liteos_a / linux） | ERROR |
| **defconfig 核依赖链完整性**（必检） | 对照官方 `arch/arm/configs/<chip>_defconfig`（金标准）逐条核对：每个开启的 `CONFIG_XXX=y` 的 `depends on` 链全部满足（如 `MTD_SPI_NAND_FMC100 depends on MFD_BSP_FMC && MTD_SPI_NAND_BSP`——只开 FMC100 不开 MFD_BSP_FMC 则依赖断裂，SPI Nand 编译不进；`BSP_TIMER depends on PM`——无 PM 则 BSP_TIMER 不生效）。漏开依赖项编译器不报错但走不到编译分支，必须人工查 Kconfig `depends on`。**实测翻车根因**：缺 `MFD_BSP_FMC` 致 FMC100 依赖断裂 + 缺 `PM` 致 BSP_TIMER 不生效 + 缺 `POWER_RESET_BSP` 致无法 reboot | ERROR |
| **CONFIG 值合法性** | 所有 `CONFIG_XXX` 值合法：bool 只能 `y`/`n`/`m`（或 `# CONFIG_XXX is not set`）；hex 值是合法十六进制（**大写 `V` 非法**——如 `0x3516CV610` 里 `V` 不是十六进制字符，C 编译错误，应为 `0x3516c610` 全小写或合法 hex）；string 值加引号；int 值在 `range` 范围内。**实测翻车点**：`0x3516CV610` 非法十六进制致 C 编译错误 | ERROR |
| **官方 defconfig 偏离核对** | 生成的 defconfig 与官方 `<chip>_defconfig` 偏离项逐条标注原因（如 `VFP/NEON`/`THUMB2_KERNEL`/`ARM_APPENDED_DTB`/`POWER_RESET_BSP` 等关键启动/重启项是否遗漏），不凭"厂商接管"等臆断跳过。**实测翻车点**：多项偏离官方 defconfig（缺 POWER_RESET_BSP/ARM_APPENDED_DTB/MTD_UBI，EDMAC vs EDMACV310 选错） | WARNING |
| 引脚号与原理图一致 | board_config.h / *_config.hcs 的引脚号与用户提供的原理图一致 | WARNING |

### Step 5: 编译验证

告知用户运行编译命令。

#### L1 HCS 编译验证

```bash
# 编译 HCS 为 HCB 二进制
hc-gen -o vendor/<dc>/<board>/hdf_config/uhdf/hdf_config.hcb \
       -I vendor/<dc>/<board>/hdf_config/uhdf \
       vendor/<dc>/<board>/hdf_config/uhdf/hdf.hcs
```

如果 hc-gen 报错，引导用户粘贴错误信息，然后 **Grep** `references/product-config-examples.md` 查找修复方案（"常见 HCS 配置错误及修复方案"章节）。

#### 完整编译验证

```bash
./build.sh --product <product_name>
```

> 本 Step 只做配置生成后的本地编译验证。

---

## ③ 外设配置项速查

快速回忆用。详细含义和填法见 `references/product-config-examples.md`。

### L0 board_config.h 宏命名约定

| 外设 | 宏名模式 | 示例 |
|------|---------|------|
| UART TX | `BOARD_UART<n>_TX_PIN` | `BOARD_UART0_TX_PIN` |
| UART RX | `BOARD_UART<n>_RX_PIN` | `BOARD_UART0_RX_PIN` |
| UART 波特率 | `BOARD_UART<n>_BAUDRATE` | `BOARD_UART0_BAUDRATE` |
| UART 使能 | `BOARD_UART<n>_ENABLE` | `BOARD_UART0_ENABLE` |
| I2C SDA | `BOARD_I2C<n>_SDA_PIN` | `BOARD_I2C0_SDA_PIN` |
| I2C SCL | `BOARD_I2C<n>_SCL_PIN` | `BOARD_I2C0_SCL_PIN` |
| I2C 速率 | `BOARD_I2C<n>_SPEED` | `BOARD_I2C0_SPEED` |
| SPI SCK | `BOARD_SPI<n>_SCK_PIN` | `BOARD_SPI0_SCK_PIN` |
| SPI MOSI | `BOARD_SPI<n>_MOSI_PIN` | `BOARD_SPI0_MOSI_PIN` |
| SPI MISO | `BOARD_SPI<n>_MISO_PIN` | `BOARD_SPI0_MISO_PIN` |
| SPI CS | `BOARD_SPI<n>_CS_PIN` | `BOARD_SPI0_CS_PIN` |
| PWM | `BOARD_PWM<n>_PIN` / `_CHANNEL` | `BOARD_PWM0_PIN` |
| ADC | `BOARD_ADC_<NAME>_CHANNEL` | `BOARD_ADC_TEMP_CHANNEL` |
| LED | `BOARD_LED<n>_PIN` | `BOARD_LED1_PIN` |
| 按键 | `BOARD_KEY<n>_PIN` | `BOARD_KEY1_PIN` |

### L1 HCS 各外设核心字段

| 外设 | 核心配置项 | 必填 |
|------|----------|------|
| GPIO | match_attr, groupNum, bitNum, regBase, irqStart | ✅ |
| UART | match_attr, num, baudRate, iomemBase, irqNum | ✅ |
| I2C | match_attr, id, regBase, irqNum, freq | ✅ |
| SPI | match_attr, busNum, regBase, irqNum, maxFreq | ✅ |
| PWM | match_attr, channel 数, 引脚映射 | ✅ |
| ADC | match_attr, 通道数, 引脚映射 | 按需 |

---

## 真实示例参考

完整真实芯片配置样本见本 SKILL 的 `examples/` 目录（L0: Hi3861/STM32F407，L1: Hi3516DV300）。
如需更多芯片样本，可在项目中搜索 `target_config.h` / `board_config.h` / `config.gni` 等文件名，或联网搜索对应芯片的 OpenHarmony 适配仓库。

- L0 样本：`examples/l0/`（Hi3861 / STM32F407）
- L1 样本：`examples/l1/`（Hi3516DV300）；L1 实战配置模式（config.gni/soc.gni/HCS/defconfig）见 `references/l1-config-patterns.md`
- 配置格式规范：`references/` 内各格式指南（`hcs-syntax-and-config.md` / `target-config-guide.md` / `config-gni-guide.md`）
- **GT 芯片官方 BUILD.gn 样本**：`references/hi3861_build_gn_samples/`（5 files — 来自 [Hi3861 官方课程](https://gitee.com/hihopeorg/HarmonyOS-IoT-Application-Development)，含 board_name 条件编译 + WiFi lwip 头文件模式）
- 内核配置样本：`references/config-templates.md`（board_config.h / target_config.h 模板库）

---

## Exceptions and Fallbacks（异常与兜底）

信息不足、工具不可用、数据矛盾时的处理规则（按场景）：

| 场景 | 处理 |
|------|------|
| **配置值取不到**（寄存器地址/依赖关系/配置参数） | 先联网搜索，查到填值并注明来源；确实查不到才标 TODO + 注明查询关键词，禁止凭记忆编造或留空 |
| **match_attr 配对失败 / hc-gen 报 match 相关错** | 逐字符比对两侧（拼写/大小写/下划线/数字后缀），修正后重跑三层验证；注意只配字符串相等还不够，必须配到 device_info.hcs 的 deviceNode 实例 |
| **defconfig 依赖链断裂**（缺 MFD_BSP_FMC/PM 等） | 对照官方 `arch/arm/configs/<chip>_defconfig` 金标准补齐依赖项（实测案例：`MFD_BSP_FMC`+`MFD_SYSCON` 补齐 FMC100 链、`PM=y` 补齐 BSP_TIMER、`POWER_RESET`+`POWER_RESET_HISI` 修 reboot）；编译器不报错但功能走不到，必须人工核 Kconfig |
| **hex 值非法**（如 `0x3516CV610`） | 大写 `V` 不是十六进制字符 → 全小写 `0x3516c610`；交付前全量 grep 产出中的非法 hex（`0x` 后出现 `[G-Zg-z]`） |
| **官方 defconfig 金标准拿不到** | 先联网查内核源码（官方 defconfig/Kconfig）；仍拿不到 → 声明缺失 + 给出依赖链人工核对方法，不凭"厂商接管"臆断跳过偏离项 |
| **hc-gen 工具不可用** | 人工跑层 1 语法验证（括号配对/分号/template 合规），并把 hc-gen 命令留给用户在可用环境执行；不因工具缺失跳过验证 |
| **编译环境不可用** | 给 hc-gen / build.sh 完整命令 + 常见 HCS 错误修复方案（Grep `references/product-config-examples.md`），明确标注"待编译验证"，不谎称编译通过 |
| **数据源矛盾**（手册 vs DTS/SDK 源码） | 以可验证的 DTS/SDK 源码证据为准，在产出中注明矛盾双方与取舍依据 |
| **文件已存在** | 检查内容正确性而非覆盖 |
