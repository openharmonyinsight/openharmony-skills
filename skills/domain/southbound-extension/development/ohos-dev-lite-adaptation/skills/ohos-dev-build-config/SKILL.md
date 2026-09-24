---
name: ohos-dev-build-config
description: OpenHarmony Lite 芯片适配的构建装配层——生成 config.gni、BUILD.gn、linker.ld、config.json、ohos.build、hals/ 等构建与产品注册文件，让新芯片可被 build.sh 发现并编译。Use when a new chip/SoC needs to be wired into the OpenHarmony Lite (L0/L1) build; triggers include 构建配置生成、产品注册三件套、新板子接入编译、config.json 怎么写、ohos.build part 名怎么取、config.gni 变量怎么填、linker.ld 链接脚本、build.sh 找不到产品 / product not found / no such target、hb 装配失败、编译报 overflowed / undefined reference、裸 gn+ninja 与 build.sh 的区别、hals/ 目录骨架。上游消费 ohos-dev-soc-spec-parse 的 chip_spec.json。
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: build
  capability: config
  version: 0.1.0
  status: trial
---

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 完整装配任务 | "给 XX 芯片生成构建配置"、"XX 要接进 build.sh"、"新板子接入编译"、"生成产品注册三件套" |
| 单文件生成/修改 | "config.gni 怎么写"、"linker.ld 链接脚本怎么生成"、"ohos.build part 名是什么"、"config.json 产品定义" |
| 症状词（隐性需求） | "build.sh 找不到我的产品"、"product not found"、"no such target"、"hb 装配失败"、"region overflowed"、"undefined reference"、"component not found" |
| 编译方式咨询 | "直接 gn gen + ninja 跑正式编译行吗"、"build.sh 和裸 ninja 什么区别" |
| 下游 skill 链式调用 | ohos-dev-board-config-gen / ohos-dev-hal-skeleton-gen 产出后需要编译入口与产品注册配套 |
| 同义表达 | 构建接线 / vendor 目录组织 / GN 装配 / 产品定义文件 |

**不触发**（明确排除）：只生成设备硬件描述文件（board_config.h / HCS / defconfig → ohos-dev-board-config-gen）；只生成驱动代码（→ ohos-dev-hal-skeleton-gen）；`build/` 平台模板本身的修改（本 SKILL 平台模板只读）；内核组件裁剪（→ ohos-dev-kernel-trim-config）。

## Scope

本 SKILL 是 OpenHarmony Lite（L0 轻量系统 / L1 小型系统）新芯片适配的**构建装配层**：生成让 `build.sh`/`hb` 能**发现产品**、并把内核/驱动/应用/SDK **装配进编译图**所需的全部构建配置与产品注册文件，引导用户完成编译验证。

本 SKILL 只做"接线 + 入口"，不生成任何会被编译进固件的源码。

> 文件已存在时检查内容正确性而非覆盖。

**输入**：芯片规格（首选上游 ohos-dev-soc-spec-parse 产出的 `chip_spec.json`；无则按 Step 1 必填表向用户收集）。
**输出**：8 类构建与产品注册文件（config.gni / linker.ld / SoC+Board BUILD.gn / config.json / ohos.build / vendor BUILD.gn / hals/ 骨架）。
**不适用**：设备硬件配置文件生成（→ ohos-dev-board-config-gen）；驱动/HAL 源码生成（→ ohos-dev-hal-skeleton-gen）。

## Initial Checks

收到任务后，按以下顺序先做判断（各步结论决定后续路径）：

1. **输入来源判断**：有上游 `chip_spec.json`？→ 直接取字段（芯片名/架构/内存映射/GIC/晶振/存储类型）；无 → 按 Step 1 必填表收集，缺失项追问用户，不猜。
2. **系统级别 L0/L1 判定**：决定 linker.ld 是否必需（仅 L0 MCU 需要 MEMORY/SECTIONS；L1 只做占位标注）、Board 配置目录 `liteos_m/` vs `liteos_a/`、config.json `type`（mini=L0 轻量 / small=L1 小型）。
3. **文件已存在 or 新建**：已存在 → 检查内容正确性而非覆盖。
4. **SoC/Board config.gni 拆分判定**：简单单板 → 变量集中 Board 级；多板共享 SoC → 公共变量放 SoC 级 + Board 级 `import()`。
5. **厂商 SDK 就绪情况**：决定 SoC BUILD.gn 接入点写法（无 SDK 时空 `deps` + TODO 注释，路径留给厂商）。
6. **编译环境可用性**：本机/远程有 OH 源码树 + prebuilts？→ 决定 Step 5 是真跑 `./build.sh` 还是给完整命令 + 预期产物清单 + 排查表（环境不可用时不得声称编译通过）。
7. **架构 → 样本映射**：按 CPU 架构选定参照的 `examples/<arch>/` 样本目录（见下方映射表）。

## Prohibited Practices（构建装配禁止操作）

| 禁止 | 正确做法 |
|------|---------|
| 用裸 `gn gen`+`ninja` 当正式编译 | 一律 `./build.sh --product <product_name>`；裸 gn/ninja 仅 GN 语法冒烟 |
| 凭经验填 march/mabi/-mcpu | 从厂商 SDK/工具链提取实际值；RISC-V 不用 `-mcpu`（见 config-gni-guide） |
| 在 SoC BUILD.gn 写死厂商 SDK 源码路径 | 只留 `deps` 接入点 + TODO 注释，挂 SDK 留给厂商 |
| 先于 config.json 生成 ohos.build | part 名依赖 product_name，按 Step 3 顺序 |
| 把 HAL/驱动源码写进 hals/ | hals/ 只生成目录骨架与占位 BUILD.gn |
| 跳过 Step 4 咬合校验直接编译 | 咬合 5 条不过，编译必在 hb 装配阶段失败 |
| 修改 `build/` 或 `build/lite/` 平台模板 | 平台模板只读；本 SKILL 只生成 vendor/device 侧文件 |

---

## ① 文件路由表

根据用户意图，读取对应的参考文件。**每次只读一个**，不要一次性加载所有 reference。

| 用户意图 | Agent 读取 | 预估行数 |
|---------|-----------|:-------:|
| 生成 config.gni（Board/SoC 级） | `references/config-gni-guide.md` | ~170 |
| 生成 BUILD.gn（SoC/Board 构建，含 SDK 接入点） | `references/build-gn-templates.md` | ~310 |
| 生成 linker.ld（链接脚本） | `references/linker-templates.md` | ~290 |
| 生成 config.json（产品定义） | `references/config-json-guide.md` | ~210 |
| 生成 ohos.build / vendor BUILD.gn / hals/（产品注册三件套） | `references/ohos-build-guide.md` | ~160 |
| GN 语法不确定 | `references/gn-syntax.md` | ~230 |
| 编译报错诊断 | **Grep** `references/error-cheatsheet.md "<关键词>"` | 按匹配 |
| 编译报错深度修复（warning→patch 映射 / GT 文件 patch / 工具链 wrapper / 修复分类决策树） | `references/compiler_fix_playbook.md` | ~620 |
| 查参考资料与上游仓库链接（官方文档 / build_lite / 移植案例） | `references/bibliography.md` | ~110 |
| 查询 mini/small（=L0/L1）官方子系统清单 | 搜索 `references/config-json-guide.md` §5 curated 子集 或联网查找 OH 官方 subsystems 注册表 | — |
| 需要参照已有芯片配置 | `examples/<arch>/` 目录 | ~200/套 |

### 架构 → 样本目录映射

| 芯片架构 | 代表芯片 | 样本目录 |
|---------|---------|---------|
| ARM Cortex-M（M0/M3/M4/M7/M33） | STM32F407 | `examples/arm-cortex-m/` |
| RISC-V（rv32imac/rv32imc） | Hi3861 | `examples/risc-v/` |
| ARM Cortex-A（A7/A53/A55） | Hi3516 | `examples/cortex-a/` |

### 错误诊断 Grep 用法

当用户粘贴编译错误时，从错误消息中提取关键词，执行：
```
Grep references/error-cheatsheet.md "<关键词>"
```
常用关键词示例：`"overflowed"`、`"undefined reference"`、`"No such file"`、`"Expected a newline"`、`"Hard Fault"`、`"cycle"`、`"product"`、`"no such target"`

---

## ② 工作流

### Step 1: 收集芯片规格

生成任何配置文件前，必须收集以下信息（缺失项需追问用户）：

| 必填项 | 说明 | 示例 |
|-------|------|------|
| 芯片名称 | 芯片型号 | STM32F407ZG |
| CPU 架构 | 核心类型 | cortex-m4 / rv32imac / cortex-a7 |
| Flash 基地址 + 大小 | 十六进制地址和容量 | 0x08000000, 1MB |
| RAM 基地址 + 大小 | 十六进制地址和容量 | 0x20000000, 192KB |
| 工具链偏好 | GCC / Clang | arm-none-eabi-gcc |
| 系统级别 | L0 (Mini) / L1 (Small) | L0 |
| device_company / board | 厂商名 / 板名（决定目录与 product_name） | hisilicon / hispark_pegasus |
| 厂商 SDK 是否就绪 | 决定 SoC BUILD.gn 接入点写法 | 已有 scons SDK / 暂无 |

### Step 2: 确定目录结构

生成的文件按三级放在 OpenHarmony 源码树正确位置。目录约定 `vendor/<device_company>/<board>/`（**不是** `<vendor>/<product>`）：

```
OpenHarmony/
├── device/board/<device_company>/<board>/
│   ├── BUILD.gn                          ← Board 构建入口（config.json device_build_path 指向）
│   └── liteos_m/                         ← L0；L1 用 liteos_a/
│       └── config.gni                    ← Board 级构建变量（构建入口）
├── device/soc/<device_company>/<soc>/
│   ├── BUILD.gn                          ← SoC 构建入口（预留厂商 SDK 接入点）
│   ├── config.gni                        ← SoC 公共变量（可选，多板共享时）
│   └── ld/
│       └── linker.ld                     ← 链接脚本（仅 L0 MCU）
└── vendor/<device_company>/<board>/
    ├── config.json                       ← 产品定义（product_name / subsystems / 元数据）
    ├── ohos.build                        ← 部件/子系统注册（module_list 指向 vendor BUILD.gn）
    ├── BUILD.gn                          ← 产品构建 target（ohos.build module_list 指向）
    └── hals/                             ← HAL 适配目录（config.json product_adapter_dir 指向）
        └── BUILD.gn                      ← 占位
```

> **已知惯例偏差**（SR-04 实测发现）：OH 上游 Hi3516 L1 样本实际用 `vendor/<device_company>/<product_name>/` 作目录名（如 `vendor/hisilicon/hispark_taurus_linux/`，product_name 作目录名而非 board 名）。L1 场景 board 与 product_name 常合为一层，以 OH 上游实际惯例为准并在产出中注明。

#### SoC config.gni vs Board config.gni 选择规则

- **简单芯片（单板）**：只需 `device/board/<dc>/<board>/liteos_m/config.gni`，所有变量集中在此
- **多板共享 SoC**：将共用变量（`soc_name`、内存映射等）放入 `device/soc/<dc>/<soc>/config.gni`，Board 级通过 `import()` 引用
- 构建入口总是先加载 Board 级 config.gni，Board 级可选择 import SoC 级

### Step 3: 按顺序生成文件

**生成顺序**（依赖从底到顶，ohos.build 依赖 config.json 的 product_name，**不可乱序**）：

```
config.gni → linker.ld(L0) → SoC BUILD.gn(含SDK接入点)
→ Board BUILD.gn → vendor config.json → ohos.build → vendor BUILD.gn → hals/
```

对每个文件，先 Read 对应的参考文件，再生成内容：

1. **config.gni**：Read `references/config-gni-guide.md`，参照 `examples/<arch>/config.gni`
2. **linker.ld**（仅 L0）：Read `references/linker-templates.md`，参照 `examples/<arch>/linker.ld`
3. **SoC BUILD.gn**：Read `references/build-gn-templates.md`（含 SDK 接入点章节），参照 `examples/<arch>/BUILD.gn`
4. **Board BUILD.gn**：同上（Board 级 BUILD.gn 章节）
5. **vendor config.json**：Read `references/config-json-guide.md`，参照 `examples/<arch>/config.json`
6. **ohos.build**：Read `references/ohos-build-guide.md`（用 config.json 的 product_name 构造 part 名）
7. **vendor BUILD.gn**：同 `ohos-build-guide.md`（group 名 = board 名）
8. **hals/**：同 `ohos-build-guide.md`（目录 + 占位 BUILD.gn）

如果 GN 语法不确定，额外 Read `references/gn-syntax.md`。

### Step 4: 交叉验证

生成所有文件后，逐项检查一致性与装配咬合：

**装配咬合（决定能否 build 起来，必查）**：
- [ ] `ohos.build` 的 part/subsystem 名 = `product_` + config.json 的 `product_name`
- [ ] `ohos.build` `module_list` 的 target 名 == vendor BUILD.gn 的 `group("<board>")` 名
- [ ] config.json `device_build_path` 路径存在且含 Board 级 BUILD.gn
- [ ] config.json `product_adapter_dir` 指向的 `hals/` 目录存在且含 BUILD.gn
- [ ] config.json `product_name` 与 `vendor/<device_company>/<board>/` 目录约定一致

**配置一致性（保留）**：
- [ ] `kernel_type` 在 config.gni 和 config.json 中一致（L0: liteos_m / L1: liteos_a 或 linux）
- [ ] march/mabi 三处一致:config.gni 的 `board_arch` + `board_cflags`(-march/-mabi/-mcpu) == 厂商 SDK/工具链实际值;RISC-V 不用 `-mcpu`(`board_cpu` 留空),详见 `references/config-gni-guide.md` → march/mabi 一致性
- [ ] linker.ld 的 MEMORY 地址与用户提供的 Flash/RAM 参数一致
- [ ] config.json 中的 component 名称与 OpenHarmony 仓库注册名拼写一致
- [ ] SoC/Board BUILD.gn 中的 `include_dirs` 路径存在且格式正确（`//` 开头）
- [ ] `board_toolchain_prefix` 与 `board_toolchain` 名称对应
- [ ] SoC BUILD.gn 的 SDK 接入点 `deps` 与厂商 SDK 实际情况一致（无 SDK 时空 deps + TODO 注释）

### Step 5: 编译验证

告知用户运行编译命令。OpenHarmony Lite 的编译入口是仓库根的 `build.sh`（内部 hb → gn gen + ninja），**不是**裸 `ninja`。

#### 标准编译（推荐）

```bash
# 前提：prebuilts 已就绪（首次需先跑 build/prebuilts_download.sh 下载 python3/node/ohpm 等）
./build.sh --product <product_name>
```

- `<product_name>` 即 config.json 的 `product_name`（如 `wifiiot_hispark_pegasus`）
- `build.sh` 封装了 hb 工具链、product 解析、子系统遍历，内部调用 gn gen + ninja
- 编译产物在 `out/<board>/<product>/` 下

#### 最小冒烟（仅验证 GN 配置语法，不产出可用固件）

仅在 `build.sh` 不可用、或只想验证刚生成的 GN 配置是否自洽时使用：

```bash
./build.sh --product-name {product}         # 仍走 hb，比裸 gn 更接近真实
# 或退到最底层（仅语法冒烟，需 prebuilts 就绪）：
gn gen out/<board>/<product> --args='product_name="<product_name>"'
ninja -C out/<board>/<product>
```

> 裸 `gn gen`+`ninja` 会绕过 hb 的 product/子系统装配逻辑，**仅适合检查配置语法**，不能产出可烧录固件。正式编译一律用 `./build.sh --product`。

如果编译报错，引导用户粘贴错误信息，然后 **Grep** `references/error-cheatsheet.md` 查找修复方案。常见三类：产品未发现（`product`/`no such target`）、链接溢出（`overflowed`）、依赖缺失（`undefined reference`/`No such file`）。

> 本 Step 只做配置生成后的本地编译验证。

---

## ③ config.gni 变量速查

快速回忆用。详细含义和填法见 `references/config-gni-guide.md`。

| 变量 | 类型 | 示例值 | 说明 |
|------|------|--------|------|
| `kernel_type` | string | `"liteos_m"` / `"liteos_a"` / `"linux"` | 内核类型（须与 config.json 一致；L0=liteos_m，L1-LiteOS=liteos_a，L1-Linux=linux） |
| `kernel_version` | string | `"3.0.0"` | 内核版本 |
| `board_cpu` | string | `"cortex-m4"` / `""` | CPU 核心（部分芯片可留空） |
| `board_arch` | string | `"arm"` / `"rv32imac"` | 架构标识 |
| `board_toolchain` | string | `"arm-none-eabi-gcc"` | 工具链名称 |
| `board_toolchain_path` | string | `""` | 工具链路径（已加 PATH 则留空） |
| `board_toolchain_prefix` | string | `"arm-none-eabi-"` | 编译器前缀 |
| `board_toolchain_type` | string | `"gcc"` / `"clang"` | 编译器类型 |
| `board_cflags` | list | `["-mcpu=cortex-m4", "-mthumb", ...]` | C 编译标志 |
| `board_asmflags` | list | `["-mcpu=cortex-m4", ...]` | 汇编标志 |
| `board_cxx_flags` | list | `board_cflags` | C++ 标志 |
| `board_ld_flags` | list | `[]` | 链接标志 |
| `board_include_dirs` | list | `["//kernel/liteos_m/kal/cmsis"]` | 全局头文件路径 |
| `board_adapter_dir` | string | `"//device/soc/hisilicon/hi3861v100/hi3861_adapter"` | HAL 适配目录 |
| `board_configed_sysroot` | string | `""` | Sysroot（通常留空） |
| `storage_type` | string | `"spinor"` / `"emmc"` / `""` | 存储类型 |

---

## Exceptions and Fallbacks（异常与兜底）

信息不足、编译失败、材料矛盾时的处理规则（按场景）：

| 场景 | 处理 |
|------|------|
| **必填信息缺失**（内存映射/架构/板名/工具链） | 按 Step 1 必填表追问用户；march/mabi/-mcpu 一律从厂商 SDK/工具链提取实际值，禁止凭经验猜 |
| **编译环境不可用**（本机无 OH 源码树 / prebuilts 未就绪） | 不谎称编译通过——给完整可复制命令（prebuilts_download → 拷贝目录树 → build.sh）+ 预期固件产物清单 + 常见报错排查表，交用户在源码树环境执行（SR-04 实测做法） |
| **编译报错** | 提取关键词 Grep `references/error-cheatsheet.md`；常见三类路由：产品未发现（`product not found`/`no such target`，多半 config.json 位置/product_name/目录名不一致）、链接溢出（`overflowed`，L0 高频）、依赖缺失（`undefined reference`/`No such file`，核对 SoC BUILD.gn deps/include_dirs） |
| **GN 语法不确定** | 先 Read `references/gn-syntax.md` 再生成，禁止跳过直接写 |
| **样本与正文约定矛盾**（examples/cortex-a config.json 用 product_name 作 vendor 目录名，与 Step 2 文字 `<board>` 不一致） | 以 OH 上游实际惯例为准（L1 场景 `vendor/<device_company>/<product_name>/`），并在产出中注明取舍；咬合校验按实际目录组织跑（SR-04 实测：按 product_name 目录组织，咬合 5 条 5/5 PASS） |
| **references 内 kernel_type 大小写不一致**（config-gni-guide 写 "liteos_m" 大写，examples/OH 上游用小写） | 以 OH 上游小写 `liteos_m` / `liteos_a` / `linux` 为准（SKILL 速查表亦为小写） |
| **L1 场景无 linker.ld 模板**（linker-templates.md 仅覆盖 L0 MCU） | L1 生成占位标注文件（LiteOS-A / Linux 内核自带链接脚本，不强制手写）+ 内存映射参考表，不强行写 MEMORY/SECTIONS |
| **chip_spec.json 缺字段**（如 processNode 厂商未公开） | 标 TODO/null 并注明原因，禁止编造（SR-04 实测：processNode 标 TODO） |
| **文件已存在** | 检查内容正确性而非覆盖 |
