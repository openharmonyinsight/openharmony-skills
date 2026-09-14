---
name: ohos-ci-lite-deploy-burn
description: >
  OpenHarmony Lite (L0/L1) 通用构建部署流水线：环境检测 → 编译 → 产物下载 → 烧录 → 测试运行 → MAP 分析。
  多连接方式（SSH 推荐 / Local / Custom），芯片无关，设备配置在 references/devices/。
  Use when the user asks to execute a concrete pipeline step or the whole pipeline for an OpenHarmony Lite target（跑编译、拉产物、烧板子、跑测试抓串口、看 MAP）。
  Do not use for: 适配工作流编排与阶段门控（走 ohos-dev-workflow-router）；验证策略编排（走 ohos-test-lite-adapt-verify，本 skill 是其底层执行工具）；测试用例生成（走 ohos-test-lite-ut-gen）；故障根因诊断闭环（走 ohos-issue-lite-diagnose）。
metadata:
  author: openharmony
  scope: domain
  stage: cicd
  domain: lite
  capability: deploy-burn
  version: 0.1.0
  status: trial
---

# OH Lite Build-Deploy — 通用构建部署流水线

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 完整流水线 | "一键全流程"、"编译部署全流程"、"从头到尾跑一遍" |
| 单阶段任务 | "编译" / "build"、"下载/拉取产物"、"烧录" / "burn" / "部署" / "flash"、"测试运行" / "run test"、"map分析" / "结果分析" |
| 组合任务 | "编译并烧录"、"烧录并测试"、"连接远程 + 环境检测" |
| 症状词（隐性需求） | "HiBurn 报 0xC35A69A6"、"烧到 100% Uncompress Fail"、"串口没输出"、"XTS 跑完怎么统计"、"固件太大想看内存布局"、"gn internal error" |
| 上游 skill 链式调用 | ohos-test-lite-adapt-verify 的 init/explore/verify 阶段调用本 skill 编译/烧录/串口捕获；ohos-test-lite-ut-gen 产出的用例需编进镜像烧板验证 |

**不触发**（明确排除）：测试用例代码生成（走 ohos-test-lite-ut-gen）；验证策略编排/优化提案（走 ohos-test-lite-adapt-verify，本 skill 是其底层工具）；芯片规格提取（ohos-dev-soc-spec-parse）。

## 概述（Scope）

本 skill 是 OpenHarmony **L0 (LiteOS-M) / L1 (LiteOS-A/Linux)** 芯片适配的**通用构建部署流水线**。

**设计原则**：
- **芯片无关**：不绑定任何具体芯片型号或开发板
- **连接方式可插拔**：支持 SSH（推荐）、Local、Custom，用户自选
- **设备配置外置**：Hi3861 / STM32 / ESP32 等各有自己的设备配置文件（`references/devices/*.json`）
- **阶段解耦**：每个阶段可独立执行，也可组合串联

**输入**：`config.json`（连接 + 编译 + 产物 + 设备参数）或 `references/devices/<chip>.json` 设备配置；编译产物（远端或本地）。
**输出**：编译产物（.bin/.map）下载到 `local.artifacts_dir`；烧录到板；测试运行日志（含 PASS/FAIL 统计）；MAP 分析报告。
**不适用**：测试用例生成（ohos-test-lite-ut-gen）；芯片验证工作流编排（ohos-test-lite-adapt-verify）；问题根因诊断的完整闭环（ohos-issue-lite-diagnose，本 skill 提供烧录失败症状→处置速查但不替代诊断）。

### 流水线阶段

| Phase | 名称 | 说明 | 依赖连接方式 |
|-------|------|------|:------------:|
| **0** | 环境检测 | 连接验证 + 本地工具 + 远程工具链 | 全部 |
| **1** | 编译 | 远程执行 `build.sh` 或本地编译 | SSH / Local |
| **2** | 产物下载 | SCP 拉取 .bin/.map 到本地 | SSH（Local 跳过） |
| **3** | 烧录 | 通过设备烧录工具写入固件（烧后自动 WAKE_MAGIC 唤醒 AT，保证可反复烧录） | 全部 |
| **4** | 测试运行 | 自动复位 + 捕获串口输出 (XTS/ACTS) + 统计 PASSED/FAILED | 全部 |
| **5** | MAP 分析 | 解析 .map 文件的内存布局 | 全部 |

---

## Initial Checks

收到任务后，按以下顺序先做判断（各步结论决定后续路径）：

1. **config.json 存在且必填齐全？** 不存在 → 走"第一步：配置"从模板创建；存在 → 对照必填项清单核缺（connection / build / artifacts / device）。
2. **系统级别判定（L0/L1）**：L0（HiBurn + 串口 + 单 bin）与 L1（ToolPlatform/HiTool + eMMC/NAND/NOR 多分区包）烧录机制完全不同——烧录类任务先判级别再路由（见 L1 烧录路由节）。
3. **连接方式可用性**：`connection.method` 是 ssh / local / custom？SSH 先做免密连通测试；Local 确认 code_dir 可达。连接不通 → 先修连接再跑流水线，不带病执行。
4. **boot 介质确认（L1 烧录前必做）**：`intake.boot.medium` 不能假设，必须从硬件确认（板上 uboot `getinfo` / 拨码 / 原理图）。实测：介质假设错 → `no find spi` + `Invalid spi flash block size!`。
5. **产物是否标准构建产出**：烧到板上的镜像必须由 SDK 标准编译产出（大小/md5 与同 SDK 版本标准产出一致）；非标准大小 = 构建流程错信号，先回溯构建再烧。
6. **硬件操作授权**：烧录是硬件操作，执行前**必须停下问用户**用哪种模式（协助/手动），获准后执行。
7. **L0 烧录外部依赖（HiBurn.exe）**：不随 plugin 分发（华为工具，用户自备）——首次烧录前确认已放到 `${SKILL_DIR}/tools/`（`burn_one.py` 默认查找位置），或用 `--hiburn` / `device.burn_tool_path` 指定路径；缺失时 `burn_one.py` 报错并附修复指引。

## Prohibited Practices（禁止操作）

| 禁止 | 正确做法 |
|------|---------|
| **手工拼烧录镜像绕过标准构建** | 烧到板上的镜像必须由 SDK/hb 标准编译产出（L1: `./build.sh ... gslboot_build`；L0: `hb build -f`）。手工拼 → 0x81（实测） |
| **SDK 不全时手工拼片段绕过** | 必须向用户索取/补齐完整 SDK（gitcode 克隆 + submodule），不 copy 片段 + 手工拼 input |
| **boot 介质凭假设烧录** | 烧录前从硬件确认实际介质（getinfo / 拨码 / 原理图），按实际介质做包 |
| **L1 裸烧用非 debug defconfig** | 裸烧/下载模式必用 debug defconfig（`DEBUG=1`）；量产 defconfig 含 `CONFIG_BSP_DISABLE_DOWNLOAD=y` 不适合裸烧 |
| **误用 gsl/uboot 文件**（`gsl.bin` ≠ `u-boot-hi3516cv610.bin`；`u-boot-original.bin` 要 hw_comp stub ≠ `u-boot.bin`） | 严格按 `boards/dmeb/Makefile` gslboot_build 的 input 来源映射取文件 |
| **烧 L0 raw 件**（无 0xBEEFADDF 头的 `OHOS_Image`） | L0 烧 `Hi3861_wifiiot_app_burn.bin`（0xBEEFADDF 头可烧件，packet_bin 打包） |
| **0xC35A69A6 当校验失败处理** | 它是握手重试码（板子没及时进下载模式），重试 LINK+RESET 时序；校验 fail 是签名/格式问题，两类别混淆 |
| **把中间态当验证终点**（编译过 / raw 件有符号 / 能烧进去） | 验证终点 = 可烧录件烧进板子 + 板上 test 执行 PASS；差一步继续推进，不停在中间态反复问用户 |
| **改烧录件不记 changelog** | 每次改 boot_image/uImage/env/rootfs/burn_table 后立即更新 `partitions/CHANGES_*.md`（md5 + 改动 + 根因） |
| **L0 全链 acts 测试** | L0 RAM 装不下全部 acts，只链要跑的那个 target（如 `ActsWifiIotTest`） |
| **不确定的错误码闷头试错** | 遇不确定的错误码/报错先联网查（联网检索，WebSearch 或等价物；坏用备选检索 CLI 如 opencode/curl）错误码含义，据查到的事实定方案 |
| **遇 GN internal error 在脏仓上 debug** | 先 `hb clean` + 确认仓完整性（build/lite 注册齐全、vendor 完整、无半恢复残留），干净仓不复现 |

---

## 自动上板跑 test + PASS/FAIL 统计（学 DeepRust pipeline）

> 来源：参考仓 `ohos-mini-harness` 的 `ohos_lite_pipeline.py` + `burn_3861_auto.py`。
> 本 skill 的 `tools/burn_one.py` 已集成以下能力，无需额外脚本即可自动上板跑 test。

### 能力 1：WAKE_MAGIC 唤醒（保证可反复烧录/重跑）

HiBurn 烧完芯片重启后 AT 可能静默（bootrom/download 态退出），下一轮 `AT+RST` 发不出。`burn_one.py` 在烧录成功后（`reset_mode=at` 时）自动发 `WAKE_MAGIC`（`bytes([0xEF,0xBE,0xAD,0xDE,0x0C,0x00,0x87,0x78,0x00,0x00,0x61,0x94])`，DEADBEEF 魔法字）唤醒 AT app，保证下一轮 `AT+RST` 能发出。

### 能力 2：AT 探测 + 唤醒 + 降级（运行前健壮性）

`burn_one.py` 发 `AT+RST` 前先 `at_probe`（发 `AT` 期望 `OK`）：
- AT 在线 → 直接发 `AT+RST` 软复位重跑 XTS（免按键）。
- AT 静默 → 自动发 `WAKE_MAGIC` 唤醒，唤醒成功再发 `AT+RST`。
- 唤醒仍失败 → **降级为仅监听串口 + 提示用户手按板子 RST 跑 XTS**（监听已在抓不会遗漏），避免 AT 不可用时静默超时白等。

### 能力 3：PASS/FAIL 统计

`burn_one.py` 的 `run_and_read` / `run_only` / `_monitor_only` 在抓 XTS 输出时累计 `PASSED` / `FAILED` 标记出现次数，退出时打印统计行：

```
[统计] 40 Tests, 0 Failures, 通过率 100.0%
```

XTS 结束标志：`All the test suites finished`（通用，收到即视为完成）。

### 能力 4：一键全流程（编译→下载→烧录→抓 test 统计）

串联现有工具即可一键跑通，无需额外 pipeline 脚本：

```powershell
# 1. 编译（SSH 模式，远程跑 build.sh，产物在 out/hispark_pegasus/...）
# 2. 下载（SCP 拉产物到本地 LOCAL_ARTIFACTS）
# 3. 烧录 + 自动抓 XTS + 统计 PASS/FAIL
python "${SKILL_DIR}\tools\burn_one.py" "${LOCAL_ARTIFACTS}\Hi3861_wifiiot_app_burn.bin" `
  -com ${COM_PORT} -baud ${BAUD_RATE} `
  --hiburn "${HIBURN_EXE}" `
  --reset-mode at --retries 5 --timeout 600 `
  --log "${LOCAL_ARTIFACTS}\test_run_<timestamp>.log"
```

烧录并测试（组合触发词）= Phase 3 → 4 一气呵成：`burn_one.py` 烧完自动发复位魔字节启动新固件 + 抓 XTS + 统计。

镜像已烧好只想重跑 XTS：`--run-only`（AT+RST 软复位重跑，免按键，AT 静默自动唤醒降级）。

### config 多板 profiles（可选，参考 DeepRust config.example.json）

单板场景用现有 `references/devices/*.json` 即可。多板场景可参考参考仓 `config.example.json` 的 `boards` 字典结构，在项目 `config.json` 里按板名组织多套 profile：

```json
{
  "active_board": "hi3861_hispark_pegasus",
  "boards": {
    "hi3861_hispark_pegasus": {
      "remote": { "host": "", "port": 22, "user": "", "code_dir": "" },
      "local": { "artifacts_dir": "", "acts_dir": "" },
      "burn": {
        "tool": "HiBurn",
        "hiburn_exe": "<HiBurn.exe 绝对路径>",
        "reset_mode": "auto",
        "burn_timeout": 90,
        "xts_timeout": 600,
        "retries": 5
      },
      "board": { "com_port": "<COMx>", "baud_rate": 115200, "usb_chip": "CH340" },
      "build_modes": {
        "<mode>": { "command": "<构建命令>", "artifacts": ["<烧录产物>"] }
      },
      "remote_artifacts": { "map_path": "<map 路径>" }
    }
  }
}
```

> 注：现有 `references/devices/hi3861_hispark_pegasus.json` 保持单板扁平结构不变（不破坏向后兼容）。多板 profiles 是可选增强，需要时在项目 `config.json` 里用 `boards` 字典。

---


## 第一步：配置

### 1.1 创建 config.json

```powershell
# 从模板复制
Copy-Item config.example.json config.json

# 编辑填写实际值（必填项见下方）
```

### 1.2 必填项清单

```
config.json
├── connection                    ← ★ 必填：怎么连到编译环境
│   ├── method: "ssh" | "local" | "custom"
│   ├── ssh: { host, port, user, identity_file }   ← SSH 时必填
│   └── local: { code_dir }                        ← Local 时必填
│
├── build                         ← ★ 必填：编译参数
│   ├── code_dir                                           ← OH 源码路径
│   ├── product_name                                       ← hb set 的产品名
│   ├── build_command                                     ← 完整编译命令
│   └── toolchain_prefix                                  ← 工具链前缀
│
├── artifacts                     ← 产物路径
│   ├── remote_map_path                                   ← .map 文件在远端的相对路径
│   ├── remote_bin_files                                  ← .bin 文件列表（可选，留空则自动发现）
│   ├── local.artifacts_dir                               ← 本地存放产物目录
│   └── local.acts_dir                                    ← ACTS 目录
│
└── device                        ← 设备相关（无烧录功能可省略）
    ├── burn_tool / com_port / reset_mode / usb_chip       ← 烧录参数
    └── hardware.flash_total_kb / ram_total_kb            ← 信息性字段
```

### 1.3 （推荐）选用设备配置文件

`references/devices/` 目录下有预置的设备配置文件。选择与你匹配的：

```powershell
# 查看可用设备配置
Get-ChildItem references\devices\*.json | Select-Object Name

# 将设备配置合并到 config.json（覆盖 build/device/artifacts 字段）
# 或直接参考其中的值手动填写 config.json
```

| 设备配置文件 | 适用场景 |
|-------------|---------|
| `hi3861_hispark_pegasus.json` | Hi3861V100 / HiSpark Pegasus (wifiiot) |
| *(待添加)* | STM32F407 / ESP32-C3 / BES2600W / ... |

> **添加新设备**: 复制任一 `.json` 为模板，修改 `build` 和 `device` 字段即可。

### 1.4 连接方式选择

| 方式 | 推荐度 | 何时用 | 配置复杂度 |
|------|:------:|--------|:----------:|
| **SSH** | ⭐⭐⭐⭐⭐ | 源码在远程 Linux 服务器 | 低（填 host/port/user） |
| **Local** | ⭐⭐⭐⭐ | 源码就在本机（WSL2 / Git Bash） | 极低（只填路径） |
| **Custom** | ⭐⭐ | 特殊环境（Docker / VPN / 代理跳板） | 中（写命令模板） |

详细说明见 `references/connection-methods/` 下各文档。

---

## 📋 关键词触发说明

### Skill 加载触发词

以下关键词出现时加载本 skill：
> `编译`、`build`、`deploy`、`部署`、`烧录`、`burn`、`map分析`、`连接远程`、`XTS`、`acts`、`flash`、`固件`

### 功能触发词 → 执行动作

| 用户说的 | 触发动作 | 备注 |
|---------|---------|------|
| **连接远程** / **环境检测** | **Phase 0** | 自动根据 connection.method 选择检测流程 |
| **编译** / **build** | **Phase 1** | 弹出构建模式选择（如果有多个） |
| **下载** / **拉取产物** | **Phase 2** | SSH 模式执行；Local 模式跳过 |
| **烧录** / **burn** / **部署** | **Phase 3** | 使用 device.burn_tool 对应的工具 |
| **测试运行** / **run test** | **Phase 4** | 复位 + 串口捕获 |
| **map分析** / **结果分析** | **MAP 分析** | 单个分析 or 对比分析 |
| **一键** / **全流程** / **从头到尾** | Phase 0→1→2(→)3→4 | 按连接方式自动裁剪 |

### 组合触发词

| 用户说的 | 触发动作 |
|---------|---------|
| **编译并烧录** | Phase 1 → 2 → 3 |
| **烧录并测试** | Phase 3 → 4 |
| **编译部署全流程** | Phase 0 → 1 → 2 → 3 → 4 |

---

## 全局配置与变量

### 变量替换规则

SKILL.md 命令中的 `${VAR_NAME}` 占位符由代理在执行前从 `config.json` 替换为实际值。

**优先级**：CLI 参数 > config.json > 代码默认值 > 设备配置文件默认值

### 核心变量映射

```
# ===== 连接（来自 connection.*）=====
CONNECTION_METHOD = connection.method              # ssh | local | custom
SSH_HOST         = connection.ssh.host
SSH_PORT         = connection.ssh.port
SSH_USER         = connection.ssh.user
SSH_IDENTITY     = connection.ssh.identity_file
LOCAL_CODE_DIR   = connection.local.code_dir          # 仅 local 模式

# ===== 构建（来自 build.*）===========
CODE_DIR         = build.code_dir                   # 远程: 绝对路径; 本地: connection.local.code_dir
PRODUCT_NAME     = build.product_name               # hb set 产品名
BUILD_COMMAND     = build.build_command             # 完整编译命令
TOOLCHAIN_PREFIX = build.toolchain_prefix          # riscv32-unknown-elf- 等

# ===== 产物（来自 artifacts.*）==========
REMOTE_MAP_PATH  = artifacts.remote_map_path        # 相对 code_dir
REMOTE_BIN_FILES = artifacts.remote_bin_files      # .bin 路径列表
LOCAL_ARTIFACTS = local.artifacts_dir    # 本地产物目录
LOCAL_ACTS      = local.acts_dir          # ACTS 目录

# ===== 设备（来自 device.*）=============
BURN_TOOL        = device.burn_tool                 # hiburn | openocd | jlink | none
COM_PORT         = device.com_port
BAUD_RATE        = device.baud_rate
RESET_MODE       = device.reset_mode               # at | dtr | none
USB_CHIP         = device.usb_chip
HIBURN_EXE       = device.burn_tool_path               # HiBurn 路径（传给 burn_one.py --hiburn）
BURN_SCRIPT      = ${SKILL_DIR}/tools/burn_one.py # 固定派生路径，不读配置

# ===== 硬件（来自 hardware.*）===========
FLASH_TOTAL_KB   = hardware.flash_total_kb
RAM_TOTAL_KB     = hardware.ram_total_kb

# ===== 派生路径 ========================
# SSH 目标（SSH 模式）
SSH_TARGET       = ${SSH_USER}@${SSH_HOST}

# SKILL_DIR        = <本 SKILL.md 所在目录>
```

---

> Details: `references/phases-detail.md`

## ① 文件路由表

根据当前阶段/意图，按需读取对应参考文件。**每次只读一个**，不要一次性加载所有 reference。

| 阶段/意图 | Agent 读取 |
|---------|-----------|
| 各 Phase（0-5）的详细执行步骤 | `references/phases-detail.md` |
| 连接方式选择与配置（SSH/Local/Custom） | `references/connection-methods/ssh.md` / `local.md` |
| 已适配设备的预置配置（Hi3861 等） | `references/devices/<chip>.json` |
| L1 init.cfg 完整模板（18 services + 目录权限 + /dev 节点） | `references/l1-init-cfg-reference.md` |
| 烧录/测试执行工具 | `tools/burn_one.py`（烧录 + AT 唤醒 + XTS 抓取统计）；HiBurn.exe 用户自备（不随 plugin 分发） |
| MAP 内存布局分析 | `tools/map_analyzer.py`（analyze / compare）——analyze：段汇总 + RAM/Flash 口径 + Top 段/Top 符号（按相邻地址差估算）；compare：RAM/Flash 变化 delta + 段级/符号级变化 Top（按 \|变化\| 排序）。命令：`python tools/map_analyzer.py analyze <map_file> [-o report.md]` / `compare <map1> <map2> [-o report.md]`（位置参数，MAP 文件来自编译产物 out 目录） |

> Details: `references/phases-detail.md`

## L1 烧录路由（多介质，C5/W6）

> 本 skill 的 Phase 3 烧录默认面向 **L0**（HiBurn + 串口 + COM 口 + reset）。**L1（Linux/LiteOS-A）烧录机制完全不同**：L1 用 eMMC/NAND 大容量介质 + U-Boot 引导，烧录工具是厂商 ToolPlatform / HiTool，不是 HiBurn。Hi3516CV610实证：L1 烧录包是 boot_image+env+uImage+rootfs+xml，用 HiTool 按 xml 分区烧到 eMMC。

### L0 vs L1 烧录差异

| 维度 | L0（HiBurn） | L1（ToolPlatform/HiTool） |
|---|---|---|
| 介质 | 内嵌 SPI Flash（小容量） | eMMC / NAND / NOR（大容量） |
| 工具 | HiBurn（串口）+ burn_one.py | 厂商 ToolPlatform / HiTool（USB/网口） |
| 包格式 | 单 .bin | boot_image + env + uImage + rootfs + 分区 xml |
| 烧录方式 | 串口按地址写 | 按 xml 分区表逐区烧 |
| reset | at/dtr | 一般不需要（U-Boot 引导） |

### L1 烧录路由（按 boot 介质分支）

| 介质 | 烧录工具 | 包内容 | 备注 |
|---|---|---|---|
| **eMMC** | HiTool / 厂商 ToolPlatform | boot_image+env+uImage+rootfs.ext4+eMMC xml | xml 分区布局匹配 env blkdevparts（见 P4 Step 4.6） |
| **NOR** | HiTool / SPI 烧录器 | boot_image+env+uImage+rootfs.jffs2+flash xml | rootfs 用 jffs2（NOR 适配） |
| **NAND** | HiTool / UBI 工具 | boot_image+env+uImage+rootfs.ubifs+ubi img | rootfs 用 ubifs |
| **SD** | dd / 厂商 SD 烧录工具 | 直接写 SD 卡（含分区表） | boot_mode=SD 时 U-Boot 从 SD 启动 |
| **TFTP/NFS** | U-Boot tftpboot/nfs 命令 | 网络拉镜像到 RAM 运行 | 调试用，不固化 |

### L1 烧录的 GATE-HW 交互（与 L0 一致）
烧录是硬件操作。L1 烧录同样**必须停下问用户**用哪种模式（协助/手动），获准后执行。L1 烧录失败常见：xml 分区不匹配、boot_image 格式不被工具接受（→ GATE-B+ 该抓住）、介质容量不够。

> **L1 烧录包的完整性由 P4 GATE-B+ 把关**（消费者验收：xml↔blkdevparts 一致、boot_image 有厂商工具产出证据等）。本 skill 只负责"按用户选的介质路由到对应工具执行烧录"。

## 烧录失败症状 → 原因 → 处置（L1/SPI/NAND，P-失败回填）

> **遇不确定的错误码/报错根因主动联网查**：烧录报错码（如 HiBurn `0xC35A69A6`）、编译/链接错误、工具行为不明时，先用宿主联网检索能力（WebSearch 或等价物；坏用备选检索 CLI 如 opencode，或 curl 抓 URL）查错误码含义/已知案例，据查到的事实定方案。别闷头试错或直接问用户——自己不确定就该先查。
> 来源：厂商 BurnTool FAQ 与实测案例沉淀。烧录失败时按此表分类，回溯 GATE-B+ 哪步本该抓住，补检查。看 `#####` 走到哪停 + `getinfo` 输出是关键判断。

### 阶段 1：bootrom 阶段（烧 boot/fastboot 分区，串口传输）

| 控制台日志 | 含义 | 原因 | 处置 |
|---|---|---|---|
| `Failed to send start frame` | bootrom 没收到起始帧 | 点击烧写后 15 秒内没重新上电 / 串口接触不良 / COM 口错 | 查上电时序、串口线、COM 号 |
| 只打印 `#####` 一段后停 + `Failed to send head frame` | bootrom 起来了但卡住 | ① boot_image 与单板型号不匹配 ② DDR 初始化失败 | 核对芯片型号/镜像；查 DDR。**若烧到 100% 但 uboot 起不来，优先怀疑 SoC 内置 DDR 变体错配**——走 `ohos-dev-soc-spec-parse` skill 查该变体该用哪个 xlsm（如 Hi3516CV610 -10B 不能用 -20S 的 DDR3 xlsm） |
| `Failed to send data frame` | 数据传输中断 | 串口连接松动 | 查串口接触 |
| `burn gsl code data failed` / `failed to download boot file` / `U-Boot is faulty` / `timeout` / 烧 boot 无响应 | bootrom 没握手成功 | 两类：①**模式/时序**——bootrom_sel 没置 1 / 没做 update+复位时序 / 15s 内没重新上电 / 串口松动；②**GSL 文件用错**——把别的产物（如 `u-boot-hi3516cv610.bin`）当 `input/gsl.bin` 喂给 image_tool。**关键鉴别**：非 boot 分区（env/kernel/rootfs）能连上有正常报错 = 串口/连接没问题 → 倾向 ②镜像 GSL 问题，别只查时序 | ①查模式时序：bootrom_sel=1、长按 update+复位 ≥50ms 松复位进 update 模式（或 15s 内重新上电）、串口接触/COM；②**核对 gsl.bin 来源**：必须是 `components/gsl/pub/gsl.bin`（从 `boards/dmeb/components/gsl` 源码 `make CHIP=xxx` 出来，通常 ~20KB），见参考仓 `boards/dmeb/Makefile` 的 `gslboot_build`。实测：误用 148KB 的 `u-boot-hi3516cv610.bin` 当 gsl → boot_image 虚胖（u-boot 被推到 0x28e00、0x824 gsl-size=0x24600）→ `burn gsl code data failed`；换成正确 20KB gsl 后结构恢复正常（u-boot@0x9800、0x824=0x5000） |
| `Failed to execute command` | 命令执行失败 | **Flash 类型选错**（如实际 NAND 却走 SPI 分区烧） | 重启看串口 Flash 属性，换对应页签/介质 |
| 打印 **DDR Training 失败** | DDR 训练失败 | DDR 配置参数不匹配（型号/频率/容量）/ 焊接 / 供电 | reg_info.bin 的 DDR 配置要匹配单板 DDR 颗粒（换 xlsm 重生成）。**xlsm 选哪个由 SoC 内置 DDR 变体决定——走 `ohos-dev-soc-spec-parse` skill 单点查询"该用哪个 xlsm"**（命中 `ddr-variant-guide.md` 变体表，如 Hi3516CV610 -10B→DDR2 64MB QFN xlsm，-20S/-20G→DDR3 128MB QFN xlsm） |

### 阶段 2：uboot 阶段（烧 env/kernel/rootfs，网口 TFTP）

| 日志/现象 | 原因 | 处置 |
|---|---|---|
| `TFTP 超时` | 服务器 IP 错 / 掩码网关错 / 板端 IP 被占 / 防火墙没关 / TFTP 参数太小 | 重载 PC IP、ping 板端、关防火墙、调大 TFTP 丢包/超时参数 |
| 串口找不到 / `tftp 端口被占用` | Linux 没 root 权限 / 69 端口被占 | root 运行；`netstat -ano -p udp` 查 69 端口占用进程杀掉 |
| `no find spi` + `Invalid spi flash block size!` | ★ **介质错配**（实测案例）| 见下方专节 |
| Nand 打印 `pure data length` / `len_incl_bad` | 正常反馈（含坏块统计） | 非 error，看坏块比例 |

### 阶段 3：烧写后启动（包烧进去了但起不来）

| 现象 | 原因 | 处置 |
|---|---|---|
| 断电重启后不开始烧写 | 串口选错/没连好 | 终端看串口，等控制台打印 |
| 烧写后无串口输出 | reset_mode 不匹配 / 波特率错 | 试 dtr/none，核对 115200 |
| 芯片变砖 | 烧录中断 / 固件不匹配 | HiBurn 强制擦除全片重烧 |
| 启动到一半卡 / kernel panic | 包内容不一致（rootfstype↔rootfs、mtdparts↔实际分区） | 核对 GATE-B+ 三方一致性 |
| uboot `BUG: Driver does not support pagesize 8192`（fmc100.c）/ 内核 `cannot found in spi nand id table` + `bsp_spi_nand_probe error -19`(-ENODEV) → UBI/rootfs 起不来 | ★ **板载 SPI Nand 颗粒不在 ID 表**（实测案例，见 BG003）| 见下方专节 |

### ★ 板载 SPI Nand 颗粒不在 ID 表（实测新增，重要）

**症状**：板载 SPI Nand 颗粒（如 DS35Q1GB-IB，ID `0xe5,0xf1`）不在海思 SPI Nand ID 表 `fmc_spi_nand_flash_table[]`（表里只有 HY035 `0xe5,0xf2` + HY073 等），两侧表现不同：
- **uboot 侧**：`spi_nand_get_flash_info` 返回 NULL → 回退通用 NAND ID 表误算 pagesize=8192 → `fmc100.c:838 BUG: Driver does not support pagesize 8192`（颗粒实际 2KB page / 128B OOB）。
- **内核侧**：ID 表查不到 → `cannot found in spi nand id table` → `bsp_spi_nand_probe error -19`(-ENODEV) → UBI/rootfs 失败。

**根因**：颗粒 ID 不在海思 SPI Nand ID 表。⚠️ **uboot 与内核是两份独立的 ID 表**（uboot `drivers/mtd/nand/raw/fmc100/fmc_ids_hi3516cv610.c` + 内核 `drivers/mtd/nand/fmc100/fmc_ids_hi3516cv610.c`，路径差一层但是两份独立源文件）——补颗粒**两侧都要补**，否则一侧识别另一侧 probe 失败。

**处置**：
1. 抓颗粒 ID（uboot 启动早期 `spi nand id: 0xe5 0xf1` 或读 JEDEC ID）→ grep 该 ID 在 `fmc_ids_hi3516cv610.c`（两侧都查），确认不在表。
2. **两侧都补条目**：照抄同表同厂商前缀（如 `0xe5`）、同规格（pagesize/OOB）的现有条目（如 HY035），只改 id + name，参数按颗粒规格书核对。别从零写条目（字段多易错）。
3. 重编 uboot（`make ... gslboot_build`）+ 内核（`./build.sh ...`），重烧。

**教训**：报错字面提到 `id table` / `probe 失败` / `pagesize 8192`（8192 是回退通用表误算的默认值，不是颗粒真实 pagesize）→ 优先查板载颗粒在不在 SPI Nand ID 表，别去改驱动支持 8192。完整诊断见 `skills/ohos-issue-lite-diagnose/references/diagnostic-cases.md` BG003。

### ★ 介质错配（实测新增，重要）

**症状**：非裸烧（跳过 boot）烧 env/kernel/rootfs 时，控制台打印：
```
Loading Environment from NAND... OK     ← 板上现有 uboot 是 NAND 版
getinfo spi → no find spi               ← 找不到 SPI Nor 芯片
Invalid spi flash block size!           ← 拿不到 block size，烧不下去
```
**根因**：板子的实际 boot 介质（NAND）≠ 烧录包目标介质（SPI Nor）。板子上没贴 SPI Nor 芯片，或现有 uboot 是别的介质的。`intake.boot.medium`（P1 Step 0 前置采集）假设错——没对着实际硬件确认。
**处置**：
1. 看板上现有 uboot 的 `getinfo` 输出确认实际介质（`getinfo spi`/`getinfo nand`/`getinfo mmc`）
2. 按实际介质重做包（NAND→ubifs+nand_env+NAND defconfig；SPI Nor→jffs2+nor_env；eMMC→ext4+emmc_env）
3. **回填 P1 Step 0**：`intake.boot.medium` 不能假设，必须从硬件确认（板上 uboot getinfo / 拨码 / 原理图）

### 关键判断速记

- **完全没 `###`** → 没进 bootrom（上电时序/串口/COM/bootrom_sel）
- **`###` 走一段停** → bootrom 起来了，DDR/boot_image 格式问题（head frame / DDR Training / 介质错配）
- **`###` 走完进 uboot 后卡** → TFTP/网络问题（其他分区烧写）
- **`no find spi/nand/mmc` + `Invalid ... block size`** → 介质错配，包跟板子介质不一致
- **全烧完重启卡** → 包内容不一致（kernel panic / rootfs 挂载失败）
- **烧到 100% → `Uncompress Fail! err=0x81`** → GZIP 解压 IP 报错，uboot 内容本身有问题（见 BG002：多半是 defconfig 用错 / 手工拼绕过标准 gslboot_build）
- **uboot `pagesize 8192` BUG / 内核 `cannot found in spi nand id table` + `probe -19`** → 板载 SPI Nand 颗粒不在 ID 表，两侧（uboot raw/fmc100 + 内核 fmc100）都要补条目（见 BG003）

反馈问题必带：用控制台工具栏**导出按钮**导出完整控制台日志（厂商要求）。

## 烧录镜像构建通用原则（L0 + L1，专家结论）

> 来源：裸烧 boot_image 0x81 诊断（见 `skills/ohos-issue-lite-diagnose/references/diagnostic-cases.md` BG002）+ Hi3861 L0 官方文档。以下三条是专家结论，**L0（Mini/Hi3861）+ L1（hi3516cv610）都适用**。

### 专家结论 1：烧录镜像必须从 SDK 编译生成（禁止手工拼）

**L0 + L1 通用**：烧到板上的镜像文件必须由 SDK/hb 标准编译产出，**禁止手工拼 input / 手工喂 bin 绕过标准构建**。

- **L1（hi3516cv610）**：`boot_image.bin` 必须走标准 `./build.sh dmeb all debug pack` 或 `make ... gslboot_build`。boot_image 含 DDR 初始化参数 + uboot，手工拼易错（GSL/uboot code/reg_info 错乱）且无法保证与 SDK 标准一致。实测：手工拼 → 0x81。
- **L0（Hi3861）**：烧录文件 `Hi3861_wifiiot_app_burn.bin` + `Hi3861_loader_signed.bin` 必须由 `hb set`（选 `wifiiot_hispark_pegasus`）→ `hb build -f` 从完整 OpenHarmony 源码树 + 厂商 SDK 编译产出（输出在 `out/hispark_pegasus/wifiiot_hispark_pegasus`）。L0 无 boot_image 打包概念，直接烧 hb 产出的 bin，但仍必须从 SDK 编译，不手工拼/改 bin。

### 专家结论 2：SDK 不全必须问用户提供完整 SDK（不能手工拼绕过）

**L0 + L1 通用**：SDK/源码不全跑不了标准编译时，**必须向用户索取完整 SDK**（能跑标准 build 的完整参考仓），不能手工拼绕过。

- **完整性标准（L1）**：顶层 Makefile + soc/ + third_party/ + build/ 齐全，能跑通标准 build 产出 boot_image（hi3516cv610 = `./build.sh dmeb all debug pack`，dmeb 是 hi3516cv610 的产品名/开发板；其他 L1 芯片换各自产品名）。
- **完整性标准（L0）**：完整 OpenHarmony 源码树（build/ + kernel/liteos_m/ + device/ + vendor/）+ Hi3861 特有工具齐全，`hb build -f` 能跑通产出 `Hi3861_wifiiot_app_burn.bin`。
- **获取方式**：向用户索取完整 SDK；或 gitcode/gitee 克隆完整参考仓 + `git submodule update --init --recursive`。**不要 copy 片段 + 手工拼 input 绕过标准构建**。

### 专家结论 3：同一 SDK 版本标准编译应一致（不一致 = 构建流程错，是诊断信号）

**L0 + L1 通用**：同一 SDK 版本标准编译产出的镜像应一致（大小/md5）。**不一致说明构建流程错了**（如用错 defconfig、手工拼、SDK 版本不符），是诊断信号——回溯构建流程，别在二进制位级 debug。

- **L1 核对**：boot_image 大小/md5 与**该芯片** SDK 标准产出一致（hi3516cv610 debug = 227840B / ~223K；此值是 hi3516cv610 的，**不是 L1 通用标准**——其他 L1 芯片大小各异，按各自 SDK 标准产出核对）。
- **L0 核对**：`Hi3861_wifiiot_app_burn.bin` 大小与同 SDK 版本标准产出一致；不一致 → 检查 config.gni / 工具链 / SDK 版本是否匹配。

## boot_image 标准构建流程（L1/Hi3516CV610，实测沉淀）

> 来源：裸烧 boot_image 0x81 诊断（见 `skills/ohos-issue-lite-diagnose/references/diagnostic-cases.md` BG002）。核心教训：**同一 SDK 版本标准编译应一致**，不一致说明构建流程错了。不手工拼 input，走标准 `gslboot_build`。本节为 L1 专属（L0 无 boot_image 概念，见上方通用原则）。

### 标准构建命令（必须走，不手工拼）

```bash
# 方式 A：标准 gslboot_build（推荐）
make LIB_TYPE=musl CHIP=hi3516cv610 BOOT_MEDIA=spi_nand DEBUG=1 gslboot_build
# 方式 B：等价 build.sh
cd build && ./build.sh dmeb all debug pack
```

**禁止手工拼**：不要 copy image_tool + 手工喂 3 个 input + oem_quick_build.py 绕过标准 `gslboot_build`。实测：手工拼出的 boot_image ~200K，与 SDK 标准编的 223K 不一致 → 烧到 100% `Uncompress Fail! err=0x81`。

### defconfig 选择（裸烧/下载模式必用 debug）

| 场景 | defconfig | 来源 | 备注 |
|---|---|---|---|
| **裸烧 / 下载模式** | `hi3516cv610_debug_defconfig` | `DEBUG=1` 触发 | ★ 裸烧必用 |
| 量产生产 | `hi3516cv610_defconfig` | 默认（非 debug） | 含 `CONFIG_BSP_DISABLE_DOWNLOAD=y` 生产标志，**不适合裸烧** |

实测：误用非 debug defconfig（含 `CONFIG_BSP_DISABLE_DOWNLOAD=y`）裸烧 → uboot 大小差 24K → `Uncompress Fail! err=0x81`。SDK 标准编译（debug defconfig）产出的 bin 烧出 `Uncompress Ok!`，是强线索。但 0x81 根因**未 100% 确证**（用户手动换"别的 bin"也启动了 uboot），defconfig 差异是定位方向而非已确证的唯一根因——见 BG002。

### BOOT_MEDIA（DMEB 默认 SPI Nand，须显式指定）

DMEB demo 板默认 SPI Nand Flash。`build.sh` 默认 `spi`=SPI Nor 与板不符，**必须显式 `BOOT_MEDIA=spi_nand`**。介质确认走 01-env-prep Step 0 前置采集（板上 uboot `getinfo` / 拨码 / 原理图，不能假设）。

### input 来源映射（手工流程也要遵守）

参考仓 `boards/dmeb/Makefile` 的 `gslboot_build` 定义了 3 个 input 的权威来源：

| image_tool input | 权威来源 | 地址/大小 | 命名陷阱 |
|---|---|---|---|
| `gsl.bin` | `components/gsl/pub/gsl.bin`（从 `boards/dmeb/components/gsl` 源码 `make CHIP=hi3516cv610` 产出） | ~20KB | ★ 别误用 `u-boot-hi3516cv610.bin`（148KB，u-boot 树产物，不是 gsl）——见 BG001 |
| `reg_info.bin` | `xlsm_to_bin.py` 按变体 xlsm 生成（DDR 变体决定 xlsm，走 `ohos-dev-soc-spec-parse` 查） | — | xlsm 选错 → DDR Training 失败 |
| `u-boot-original.bin` | **hw_comp stub**（`u-boot-hi3516cv610.bin`，@0x41700000） | — | ★★ **命名误导**："original"像未压缩 u-boot.bin，**实际要 hw_comp stub，≠ `u-boot.bin`** |

> **命名陷阱（实测教训）**：`u-boot-original.bin` 的"original"容易让人以为是"未压缩的 u-boot.bin"，实际它要的是 hw_comp stub（`u-boot-hi3516cv610.bin` @0x41700000）。误用 `u-boot.bin` → boot_image 内容错。

### 同一 SDK 版本一致性核对（必做）

编出的 boot_image 应与 SDK 标准一致：
- [ ] 大小一致（如 Hi3516CV610 debug 标准产出 227840B / ~223K）
- [ ] md5 一致（有参考产出时对比）
- 不一致 → **构建流程错了**，回溯流程别在二进制位级 debug

### ⚠️ B18 boot_image 大小一致性核对（非标准大小 = stub 布局被改信号）

boot_image 出现**非标准大小**（如 219.5K vs SDK 标准 223K）= hw_comp stub 布局被改动（如 debug print 注入改了段布局）的信号 → `0x81 Uncompress Fail` 风险。

- 标准 debug 产出 227840B / ~223K（Hi3516CV610）。差超过几百字节就要警惕。
- 大小偏差 + 烧到 100% `Uncompress Fail! err=0x81` → 回溯构建流程（defconfig 是否 debug / 是否手工拼 / stub 是否被改），别在二进制位级 debug（见专家结论 3）。
- 实测：手工拼出的 boot_image ~200K 与标准 223K 不一致 → 0x81。

### ⚠️ B17 env 去\r + UBI vol_name 匹配 bootargs + vtbl 偏移验（rootfs 重打包后必查）

rootfs 重打包后三项必查：

1. **env 源文件去 \r**（CRLF→LF）：env 源 `.txt` 必须是 LF 行尾，CRLF 会污染 env 字段。`mkenvimage` 前先 `dos2unix` 或 `sed -i 's/\r$//'`。
2. **UBI vol_name 匹配 bootargs**：rootfs 的 UBI volume name 必须匹配 bootargs `root=ubi0:ubifs` 的 vol_name（`ubifs`）。vol_name 错 → 内核挂不上 rootfs。
3. **vtbl 偏移验**：rootfs ubifs 镜像的 UBI volume table（vtbl）偏移 `4112`(0x1010) 处应为 `75 62 69 66 73`（ASCII "ubifs"）：
   ```bash
   # 验 vtbl 偏移 0x1010 处是 "ubifs"
   xxd -s 0x1010 -l 5 <rootfs>.ubifs   # 期望: 75 62 69 66 73
   ```
   不匹配 → vol_name 错，重打 ubifs 时 `-n ubifs` 指定对 vol_name。

> 实测：rootfs 重打包后 vol_name 与 bootargs 不匹配 → 内核 UBI 挂载失败。vtbl 偏移验是机器可查项。

## init.cfg 命令支持集（B15，OH init 限制）

OH beget init 的 `init.cfg` 命令只支持：`mount` / `mkdir` / `chmod` / `chown` / `start` / `exec` / `export`。**不支持 `mknod`**。

- 源码依据：`base/startup/init/services/init/init_common_cmds.c`（命令注册表）
- 需要 mknod 时用 `exec /bin/busybox mknod ...` 绕（exec 调 busybox 执行 mknod）
- 写 init.cfg 别用 `mknod` 直接命令，会被 init 忽略/报错

> 完整 init.cfg 模板（18 services + pre-init/init/post-init job + 目录权限清单 + /dev 节点权限）见 `references/l1-init-cfg-reference.md`。

### 服务器 SDK 片段不全的应对

服务器 SDK 片段不全跑不了标准 `build.sh dmeb all` 时，**补齐完整参考仓**（gitcode 克隆 + submodule）跑标准 build.sh，**不要手工拼 input**。实测：手工拼绕过标准 `gslboot_build` → boot_image 与标准不一致 → 0x81。

## L0 可烧件格式 + HiBurn 行为（Hi3861，实测沉淀）

> 来源：Hi3861 端到端验证。澄清 L0（Hi3861）可烧件的真正格式与 HiBurn 行为，避免误烧 raw 件或误判握手码。

### 可烧件格式：OHOS_Image.bin 直接是 0xBEEFADDF 头可烧件

`build.sh --product wifiiot_hispark_pegasus` 编出的 `out/hispark_pegasus/wifiiot_hispark_pegasus/Hi3861_wifiiot_app_burn.bin`（亦即 sdk_liteos 产出的 `OHOS_Image.bin`）**直接就是带 `0xBEEFADDF` 头的可烧件**，由 `packet_bin` 打包（loader_signed + wifiiot_app_burn 合并），**不是 raw**。

- **HiBurn GUI 烧这个 0xBEEFADDF 头件**——不是 raw `OHOS_Image`（无头，7350 0030 头，烧不进），也不是单独烧 `aa55` burn bin。
- 误烧 raw `OHOS_Image` → HiBurn 不识别头 / 烧进去了但起不来。
- 完整可烧件识别与烧法见 `references/devices/hi3861_hispark_pegasus.json` 的 `_burn_notes`。

### HiBurn auto burn 操作 + 握手码辨识

- **auto burn 必勾上** + **按 LINK + RESET 硬复位进下载模式**（见设备配置 `_burn_notes.enter_download_mode`）。AT+RST 软复位不进下载模式。
- **`0xC35A69A6` 是握手重试码**（板子没及时进下载模式 / HiBurn 与 bootrom 时序错开），**不是校验 fail**。处置：重试按 LINK+RESET 时序，确认串口接触、COM 号、波特率。
- **校验 fail** 是签名/格式问题（烧的件头不对 / 件损坏 / 签名校验不过），与握手重试码是两类故障，别混淆。

### 干净仓 GN 不复现 internal error

**干净仓 `build.sh` 约 16s 编通（GN 无问题）**。`gn internal error` / GN 异常退出是**脏仓状态**（挖空恢复不全 / build 注册半恢复 / `.gn` 缓存损坏）导致，干净仓不复现。遇 GN internal error 先 `hb clean` + 确认仓完整性（`build/lite` 注册齐全、`vendor/hispark_pegasus` 完整、无半恢复残留），别在脏仓上 debug GN。

## test 链进 wifiiot 产品（Hi3861，实测沉淀）

把生成的 test target 链进 wifiiot 产品编译，**只链要跑的那个 acts target**，别全链：

```gn
# sdk_liteos/BUILD.gn
enable_hos_vendor_wifiiot_xts = true

deps = [
  "//test/xts/acts/iothardware_lite/peripheral_hal:ActsWifiIotTest",  # 只链这一个
]
```

- **全链 `acts`** 会因 `KvStore` / `Lwip` 等依赖炸链接（L0 RAM 装不下全部 acts + 符号冲突）。**只链 `ActsWifiIotTest`**（或当前要验的那个 target），其余 acts 不链。
- `enable_hos_vendor_wifiiot_xts=true` 是开关——不开则 test target 不进 wifiiot 产品镜像，烧板后测试不跑。
- 链完 `build.sh --product wifiiot_hispark_pegasus` 重编，产物里要有 test 的 `initCase*` 符号（见 ohos-test-lite-ut-gen Step 7 §抗 gc-sections 编后必验）。

## 验证类任务终点定义（实测沉淀）

**验证类任务的终点 = 可烧录件烧进板子 + 板子上 test 执行 PASS**，不是以下任一中间态：

| 不是终点 | 为什么 |
|---|---|
| raw 件有符号 | raw `OHOS_Image` 不能直接烧，烧了也不跑 |
| 编译过 | 编译过 ≠ 可烧（可能产 raw 件 / 没 0xBEEFADDF 头） |
| ok 件能烧 | 烧进去 ≠ test 跑通（test 可能没链进 / zinitcall.test2 被丢 / HardFault） |

**agent 不中途停半成品反复确认**——遇到"差一步"（如 test 没跑 / 只烧了 raw / gc-sections 丢了 initCase）继续推进到板上 test PASS 才算完成，别在中间态停下来问用户"要不要继续"。中间态确认是噪音，终点是板上 PASS。

## Exceptions and Fallbacks（异常与兜底）

| 场景 | 处理 |
|------|------|
| **SSH 连不上 / 认证失败** | 按附录 C 故障排查速查（`ssh -v` 看认证细节 / `nc -zv` 探端口）；修好连接再跑流水线，不带病执行 |
| **远程编译失败（build.sh 报错）** | 报错信息先联网查（联网检索，WebSearch 或等价物；坏用备选检索 CLI 如 opencode/curl）已知案例；工具链类错误核 `toolchain_prefix` 与 PATH；GN internal error → `hb clean` + 核仓完整性，不在脏仓 debug |
| **产物下载不完整 / .map 缺失** | SCP 校验文件大小/md5 后再进烧录；.map 缺失则 MAP 分析降级跳过并告知用户，不编造分析结果 |
| **AT 静默（烧录前 AT+RST 发不出）** | burn_one.py 自动降级链：`at_probe` → `WAKE_MAGIC` 唤醒 → 仍失败降级为仅监听串口 + 提示用户手按 RST，避免静默超时白等 |
| **烧录失败** | 按本文「烧录失败症状 → 原因 → 处置」三阶段表分类定位（bootrom / uboot / 烧后启动），回溯 GATE-B+ 该抓住的检查项；错误码先联网查含义 |
| **介质错配**（`no find spi` + `Invalid ... block size`） | getinfo 确认实际介质 → 按实际介质重做包 → 回填 `intake.boot.medium` 确认来源，下次不再假设 |
| **烧到 100% Uncompress Fail 0x81** | 回溯构建流程（defconfig 是否 debug / 是否手工拼 / stub 是否被改 / 大小是否标准），别在二进制位级 debug |
| **板载 SPI Nand 颗粒不在 ID 表**（pagesize 8192 BUG / probe -19） | 两侧（uboot + 内核）ID 表都补条目，照抄同规格现有条目只改 id+name |
| **XTS 跑完统计不到** | 结束标志是 `All the test suites finished`；收到即视为完成并出 `[统计] N Tests, M Failures` 行；没等到 → 查复位是否成功（AT 降级链）+ timeout 是否过短 |
| **编译/烧录均在远端且用户不在场** | 可自动化的阶段（0/1/2/5）继续；硬件操作（3/4 涉及按 RST/选择烧录模式）等用户在场再执行，不代替用户按板 |
| **同一问题反复失败（3+ 次）** | 停下汇总已试方案 + 失败证据，请用户介入决策或换诊断路径（ohos-issue-lite-diagnose），不无限重试 |

## 附录

### 通用规则：改烧录件立即更 CHANGES_*.md（D4）

每次改烧录件（`boot_image`/`uImage`/`env`/`rootfs`/`burn_table`）后**立即更新**对应 `partitions/CHANGES_*.md`：记录改了什么 + 新 md5 + 根因/修复说明。每产物带 md5 历史。

- changelog 按日期分文件（`CHANGES_20260717.md` / `CHANGES_20260720.md` ...），同日多次改更新同文件
- 文件清单表更新 md5 + 大小 + 改动说明；加修改小节（改了什么/为什么/根因）
- 执行代理（含被委派的子执行者）改完烧录件同样要更新 changelog（或由主执行者补记）
- 烧录件多轮迭代不记 changelog 会丢失修改历程（boot_image 从手工拼错乱→SDK 标准→干净版，uImage legacy→FIT，env 去\r，rootfs vol_name），状态混乱会误烧旧版
- 详见 memory `update-changelog-after-burnfile-change`；与 `04-build-verify` Step 4.7 D4 联动

### A. 设备配置文件规范

`references/devices/*.json` 的结构：

```json
{
  "_device_profile": "人类可读的设备名称",
  "_chip": "芯片型号",
  "_arch": "架构",
  "_board": "开发板",
  "connection": { /* 默认连接参数（被 config.json 覆盖）*/ },
  "build": {
    "code_dir": "...",
    "product_name": "...",
    "build_command": "...",
    "toolchain_prefix": "...",
    "build_modes": { "<mode>": { "command": "...", "artifacts": [...] } }
  },
  "device": { "burn_tool": "...", ... },
  "hardware": { "flash_total_kb": 0, "ram_total_kb": 0 }
}
```

**加载优先级**：CLI 参数 > config.json > 设备配置文件默认值

### B. 连接方式扩展

添加新的连接方式：

1. 在 `references/connection-methods/` 创建 `<name>.md`
2. 在 `config.example.json` 的 `connection.<name>` 添加字段
3. 在 Phase 0 路由表中添加分支

### C. 故障排查速查

| 症状 | 可能原因 | 检查方法 |
|------|---------|---------|
| SSH Permission denied | 密钥未推送 / 用户名错误 | `ssh -v` 查看认证细节 |
| SSH Connection refused | 端口错误 / SSH 服务未启动 | `nc -zv host port` |
| `build.sh: not found` | code_dir 路径错误 | `ls <code_dir>/build.sh` |
| `cannot find -lgcc` | toolchain_prefix 错误 / 不在 PATH | `which <prefix>gcc` |
| COM 端口被占用 | 上次烧录进程未退出 | `Get-PnpDevice -Class Ports` |
| 烧录卡在 Entry loader | 正常现象，等待完成 | 不要中断，至少等 2 分钟 |
| 烧录后无串口输出 | reset_mode 不匹配 / 波特率错误 | 尝试 dtr/none 模式 |
| 芯片变砖 | 烧录中断 / 固件不匹配 | 用 HiBurn 强制擦除全片后重烧 |
