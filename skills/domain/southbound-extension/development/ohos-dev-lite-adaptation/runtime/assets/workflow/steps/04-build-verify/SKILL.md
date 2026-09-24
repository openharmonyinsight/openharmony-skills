---
name: build-verify
description: 工作流 Phase 4（关键门控阶段）——执行 OpenHarmony Lite 全量编译（./build.sh --product-name {product}）、修复编译错误、分析固件大小、烧录验证。触发症状：用户说"编译"、"./build.sh --product-name {product} 报错"、"固件太大"、"烧录"、"构建验证"。⚠️ 通过/不通过的关键节点。
license: MIT
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: lite
  capability: build-verify
  version: 0.1.0
  status: trial
  category: workflow-step-build-verify
  references:
    compiler_playbook: skills/ohos-dev-build-config/references/compiler_fix_playbook.md
---

# Phase 4: 编译构建与验证

> **本文件已通过实测验证**（Hi3861V100 / wifiiot；工具链版本以 Step 0e 实测记录为准——prebuilt 13.2.0 + wrapper，SDK 内部构建实测 7.3.0）。
> 本阶段包含完整 GATE-0→V11→V12 门控流程、GT Patch Archive、Compiler Fix Decision Tree、多产物构建感知。

## 契约（来自编排器 `skills/ohos-dev-workflow-router/SKILL.md`，实测校准后）

| 属性 | 值 |
|------|-----|
| **输入** | P1~P3 全部产出（完整代码） |
| **产出** | ① **GATE-0 环境健康报告** ② ./build.sh --product-name {product} 全量编译通过 ③ 多产物固件(.bin/.elf) ④ 大小分析报告 ⑤ 烧录运行验证(可选) |
| **门控** | **GATE-0 → GATE-V11 → GATE-V12 三级门控体系** |
| **后续** | → P5 测试 / → P6 文档+审查 / → P7 诊断（编译失败时切入）|
| **多产物** | bootloader + loader + main app 独立链接（见 §Multi-Output） |

## 知识检索（可用时优先知识检索服务如 project-brain MCP；不可用按 skill 知识检索降级链：本地 references → 联网搜索 → 询问用户）

本步骤的本地代码分析，可用时优先使用（可选）project-brain 等知识检索服务 MCP（尤其 Compiler Fix Loop）：
- `impact_analysis` — 改某文件前评估波及面（修复前必用，避免改一处坏一片）
- `get_call_graph` — 追编译错误的调用链（谁调了出错的符号）
- `get_related_tests` — 改完找关联测试验证
- `locate_symbol` — 定位报错符号定义

> MCP 调失败或未装 → 按 skill 知识检索降级链回退。

## 决策分级（问用户 ↔ 自决平衡，编译/构建阶段适用）

> **实测教训**：①执行者在用户未明确决策时被主 agent 默认推进业务决策；②执行者把技术决策（binder/MTD/patch 适用性/工具链路径/构建路径当只有一条可行）转发用户烦用户。P4 是 GATE-B 门控阶段，决策密集（工具链路径修正、defconfig 调整、boot_image 缺失后是否终止、构建路径选择、 Compiler Fix Loop 修复策略），遇决策先按本表分级再决定转发还是自决。完整版见编排器 `skills/ohos-dev-workflow-router/SKILL.md`「决策分级 + 术语大白话」节。

| 级别 | 含义 | 处理方式 | P4 典型例子 |
|------|------|---------|---------|
| **业务决策** | 物理板型 / scope 取舍 / trade-off 代价 / 归档路径 / boot_image 缺失后是否终止 / 经验回填开关——需用户拍板的选择 | **停下转发用户，不默认推进**（含主 agent 也不能替用户默认，实测教训） | boot_image 缺失后终止 vs 跳过、归档路径、media 类型确认（调查后仍不确定才问） |
| **技术执行** | 内核 config flag、patch 适用性、工具链路径、构建路径当只有一条可行、Compiler Fix Loop 修复策略、按工作流教训可定的——执行者按工作流教训+验证自决 | **执行者自决，不转发用户**（实测教训） | defconfig 开 MTD、加 BINDER_IPC_32BIT 宏、修 TC_DIR 路径冲突、路径 B OH 集成当唯一可行时、-Werror warning 修复策略（Patch #001-#009 模式）、SDK 二进制指纹锁禁用（Patch #010） |

> **执行纪律（问用户与自决平衡）**：遇决策先按上表分级。业务决策必须停下转发等明确答复，绝不默认推进（哪怕主 agent 给"默认值"，只要用户没明确说也停下问）。技术执行按工作流教训+验证自决，不拿技术决策烦用户。判别口诀：**"这是真的应该由用户决定的问题吗？"**——是→停转发；否（按工作流教训+验证可定）→自决。

### 门控分级（实测教训，完整规则见编排器 `skills/ohos-dev-workflow-router/SKILL.md` §门控类型分级规则）

> **实测教训**：门控交互模式一刀切"必须停下展示清单等用户确认"未按决策分级 分级。技术门控 PASS = 技术执行验证通过，自决推进符合技术自决；业务门控涉及用户资产（归档路径/硬件/教训回填），停下转发符合问用户。本步骤涉及的门控按类型分级如下：

| 门控 | 类型 | PASS 后行为 |
|------|------|------------|
| **GATE-0**（环境健康 + 工具链全扫） | 技术 | 4 子门控全 PASS + 来源完整性 PASS → 自决过（展示清单作汇报不阻塞）；任一 FAIL → 停下修；遇来源完整性警报 → 停转发 |
| **GATE-V11**（编译门：主产物编译零错误） | 技术 | exit 0 + 零 error → 自决过；主产物 FAIL → 进 Step F 修复循环，且 GATE-B FAIL |
| **GATE-V12**（产物结构门：完整烧录包产出 + 大小/结构核验） | 技术 | 全产物就绪 → 自决过；任一产物异常 → 停下修，GATE-B 不得 PASS |
| **GATE-B**（P4 阶段门：V11+V12 会签） | 技术 | V11+V12 双 PASS → 签发 GATE-B PASS，自决过；任一 FAIL → GATE-B FAIL，停下修；缺用户明确允许跳过的非必需产物 → GATE-B 不得 PASS，标 CONDITIONAL 进 GATE-B+ 风险清单 |
| **GATE-B+**（烧录包消费者验收） | 技术 | 全产物有外部锚 + 一致性检查全过 → 自决过；无锚且未声明"未验证" → FAIL；显式声明"未验证" → CONDITIONAL（可进 GATE-交付 但必须转交用户） |
| **GATE-BURN**（烧录硬件操作） | 业务 | **必须停下问用户**采用协助模式还是手动模式，获准后才执行 |

> **判定口诀**：遇门控 PASS 准备推进时先问——"这是真的应该由用户决定的问题吗？"——是（本阶段业务门控 GATE-BURN）→ 停转发等明确答复；否（技术门控 GATE-0/V11/V12/B/B+ PASS）→ 自决过。技术门控也要先展示确认清单再自决过，不准默写"已通过"不汇报。最终 GATE-交付由编排器在 P6 后统一处理，P5 的 GATE-HW 由测试阶段处理。

## 子步骤（实测验证后的执行顺序）

```
Step 0: GATE-0 环境健康检查 ★ 新增（实测证明必需）
    │
    ├── 0a: hb 模块可导入?
    ├── 0b: gn 二进制可用?
    ├── 0c: components.json 存在? (动态生成)
    └── 0d: 工具链可用? (含 zicsr 等扩展)
    │
Step 1: GN 配置 + Linker 脚本最终化
    │
Step 2: 全量编译执行 (./build.sh --product-name {product} 或 direct_build_cmd fallback)
    │
    ├── 编译通过? → Step 3 (大小分析 + 门控)
    │
    └── 编译失败? → Step F: Compiler Fix Loop ★ 核心循环
         │
         ├── F1: 错误分类 (workflow-gen vs GT vs framework?)
         ├── F2: 选择修复策略 (见 Decision Tree)
         ├── F3: 执行修复 (Patch / config change / wrapper)
         ├── F4: 记录 (experiment or formal patch)
         └── 回 Step 2
    │
Step 3: 二进制大小分析 + Multi-Output 验证
    │
Step 3.5: 构建守卫与产物闭合（GATE-B 签发前置）
    │
Step 4: (可选) 烧录验证
```

---

## Step 0: GATE-0 — Build Environment Health Check

> **实测关键发现**: 编译失败的 **50%+ 是环境问题而非代码问题**。
> hb 损坏、工具链缺失、components.json 不存在——这些必须在正式编译前系统性检查和修复。
> GATE-0 失败 → BLOCKED（非代码质量问题），但必须记录。

### 0a: hb 模块可导入？

```bash
# 检查:
PYTHONPATH=<repo_root>/build python3 -c "import hb; print('hb OK, ver:', hb.__version__)"
```

| 结果 | 含义 | 修复方式 | 参考 |
|------|------|---------|------|
| ✅ OK | hb 可用 | 无需修复 | — |
| ❌ ModuleNotFoundError | Python 包结构损坏 | `pip install -e <repo_root>/build/hb` + 补 `__init__.py` | playbook §3 (Framework Patch) |
| ❌ ImportError (no_instance) | import path 错误 | 修复 util 文件的 from/import path | playbook §3 |

### 0b: gn 二进制可用？

```bash
gn --version   # 期望: v2026 或更新
ninja --version # 期望: v1.10.1+
```

> ⚠️ OH 构建 **必须** 使用 `ninja -w dupbuild=warn`（OH 有重复 NOTICE 文件规则）

### 0c: components.json 存在？

```bash
ls -la <out_dir>/build_configs/parts_info/components.json 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

| 结果 | 含义 | 修复方式 |
|------|------|---------|
| ✅ EXISTS | 已有产物缓存 | 无需操作 |
| ❌ MISSING | 首次构建或缓存被清理 | 执行 `./build.sh --product-name {product}` 自动生成（首次运行即生成 components.json） |

**关键**: `components.json` 是 **动态生成产物**，不在源码树中。`./build.sh` 首次运行会自动生成它，替代旧流程的 `hb set`。


### 0d: 工具链可用？+ ★ 一次性全扫路径冲突

**先读 `workflow_config.yaml` 的 `toolchain.mode`** 决定检查方式（见 `ohos-dev-cross-toolchain` skill）：auto→`which {prefix}gcc`；user→`{path}/{prefix}gcc`；wrapper→wrapper 脚本存在可执行；docker→镜像可拉起。

```bash
# auto:
which {toolchain_prefix}gcc 2>/dev/null && echo "FOUND: $(which {toolchain_prefix}gcc)"
{toolchain_prefix}gcc --version 2>/dev/null | head -1
# user: 用 {toolchain.path}/{toolchain.prefix}gcc 替代 which
# wrapper: 检查 {toolchain.wrapper} 存在且可执行
# docker: docker run --rm {toolchain.docker_image} {toolchain.prefix}gcc --version
```

| 结果 | 含义 | 下一步选项 |
|------|------|----------|
| ✅ FOUND + 版本匹配 | 工具链就绪 | → **必须进入 Step 0d-TC 全扫** + **Step 0e 做版本记录** |
| ✅ FOUND 但版本不匹配 | SDK 可能硬编码了旧版本号 | → 先修 usr.mk/scons_env_cfg.py (playbook §2 Patch #005) |
| ❌ NOT FOUND | 工具链未安装 | → **用户交互点** (见下方) |

#### ★ 一次性全扫工具链路径冲突（GATE-0 0d 子门控，实测教训）

> **实测教训**：P1 GATE-0 只查改了 `config.gni` + `sdk_linux/build.sh` 两处 TC_DIR，P2 又发现第三处 `kernel/linux/build/kernel.mk` L76 TC_DIR 同样指向旧路径 `/opt/cv610_tc/...`。**路径冲突跨阶段漏到 P2 才补**，浪费一轮内核移植。GATE-0 必须一次性全扫所有 build 脚本的 TC_DIR / 工具链路径，别让冲突跨阶段漏。

**全扫命令（GATE-0 0d 必跑，不止查 0d 主检查的 `{toolchain_prefix}gcc` 是否存在）**：

```bash
# 一次性扫所有 build 脚本里的 TC_DIR / 工具链路径（排除 .bak + /out/ 生成产物）
grep -rnE "cv610_tc|TC_DIR|openeuler_gcc_arm32le|/opt/[a-z_]+gcc" $OHROOT \
  --include="*.sh" --include="*.mk" --include="*.gni" --include="*.gn" \
  --include="*.py" --include="Makefile*" --include="*.mak" \
  | grep -vE "\.bak|/out/"
```

**扫到路径后的处理（决策分级：技术执行→自决，不转发用户）**：
- 所有 TC_DIR / 工具链路径**必须指向 `workflow_config.yaml.toolchain.path`**（briefing/用户确认的实际工具链路径，如 `/opt/openeuler_gcc_arm32le-musl/bin`）
- 任一文件指向不一致的旧路径（如 `/opt/cv610_tc/...`）→ **技术执行自决修正**：备份 `.bak.{iter}` → 改路径 → `bash -n` 语法验证 → 记录到 PROVENANCE
- 修正后重跑全扫命令确认 `0 残留冲突`（闭环验证）
- 扫描范围必须覆盖（但不限于）：`device/soc/*/sdk_linux/build.sh` + `device/soc/*/sdk_linux/config.gni` + `device/board/*/linux/config.gni` + `kernel/linux/build/kernel.mk` + 任何含 `TC_DIR` 或绝对工具链路径的 `.sh/.mk/.gni/.gn/.py/Makefile`

#### ★ P2/P3 接入新 build 脚本时补扫（全扫范围扩展，实测教训）

> **实测教训**：原文是"P1 GATE-0 + P4 GATE-0 复检执行一次性全扫"，但 kernel.mk 是 P2 Step 2b 才接入的文件，P1 GATE-0 全扫扫不到 → P2 接入时才发现 kernel.mk L38 `ifeq ($(KERNEL_ARCH), arm)` 硬编码 `gcc-linaro-7.5.0-arm-linux-gnueabi`，cv610 需 openeuler musl ARM32。**全扫不只 P1/P4 跑，P2/P3 接入新 build 脚本时也必须补扫**——凡接入一个新 build 脚本就跑一次全扫，别让冲突跨阶段漏。

**P2/P3 接入新 build 脚本时的补扫清单（接入时必跑，不只 P1/P4）**：
- `kernel/linux/build/kernel.mk`（P2 Step 2b 接入）— OH 仓共享文件，按 `KERNEL_ARCH` 硬编码工具链（arm→linaro gnueabi，arm64→linaro aarch64），不支持板级覆盖
- `kernel/linux/build/kernel_module_build.sh`（P2 Step 2b 接入）— 调 kernel.mk 的入口脚本
- `device/soc/*/sdk_linux/BUILD.gn`（P3 Step 3b 接入）— GN 构建文件可能有工具链路径
- 任何 P2/P3 才接入的 `.sh/.mk/.gni/.gn/.py/Makefile`（含 `TC_DIR` 或绝对工具链路径的）

**kernel.mk 板级工具链覆盖方式（最小侵入，不影响其他板）**：

kernel.mk 是 OH 仓共享文件，**直接改 `arm` 分支的工具链路径会影响所有 arm 板**（hi3516dv300 等）。板级覆盖必须用**环境变量 / 条件分支**，不改默认分支：

```makefile
# kernel.mk 默认 arm 分支（不动，保持其他板兼容）
ifeq ($(KERNEL_ARCH), arm)
KERNEL_CROSS_COMPILE := gcc-linaro-7.5.0-arm-linux-gnueabi
endif

# 板级覆盖块（加在 arch 分支后，环境变量设了才覆盖，最小侵入）
ifneq ($(KERNEL_TARGET_TOOLCHAIN_PREFIX_$(BOARD_UPPER)),)
KERNEL_CROSS_COMPILE := $(KERNEL_TARGET_TOOLCHAIN_PREFIX_$(BOARD_UPPER))
endif
```

配套在 `kernel_module_build.sh` 加板级分支设环境变量（如 `KERNEL_TARGET_TOOLCHAIN_PREFIX_CV610` + `KERNEL_TARGET_TOOLCHAIN_PATH_CV610`），板名匹配才设，不匹配走默认。

> **修复策略**：板级覆盖块是技术执行自决（不改共享代码默认行为，最小侵入）。改完备份 `.bak.{iter}` + `bash -n` / `make -n` 语法验证 + 记录 PROVENANCE。**禁止直接改 kernel.mk 的 arm/arm64 默认分支**——那是共享代码，改了影响所有 arm 板（OH 上游共享代码处理原则同理）。

| 扫描结果 | 含义 | 动作 |
|---------|------|------|
| 0 处路径冲突（全指向 `toolchain.path` 或无硬编码路径） | ✅ PASS | 进 Step 0e 版本记录 |
| N 处路径冲突（指向旧/错路径） | ⚠️ 技术执行自决修正 | 备份→改→语法验证→重扫确认 0 残留 |
| 扫到无法判断的路径变量（如 `$(cross_prefix)` 需运行时展开） | 标记待运行时验证 | 进 Step 0e 版本记录 + 编译时验证 |

#### 0d 用户交互点：工具链缺失

> **交叉编译工具链未检测到。**
>
> 目标芯片 **{chip_model}** ({arch})) 需要 **{prefix}gcc** 工具链。
>
> 请选择：
> - [ ] **提供路径** — 我已自行安装，填写路径: `__________`
> - [ ] **自动安装** — 工作流执行安装脚本
> - [ ] **跳过 L5** — 本次仅做源码级验证 (L1-L4)，编译留到后续迭代
> - [ ] **Docker 环境** — 使用预配置的编译容器镜像
> - [ ] **使用 Wrapper** — 用 wrapper script 包装现有二进制 (注入 flag/重定向)

> **⚠️ 实测经验**: 如果预 built 缺少特定指令集扩展 (如 zicsr),
> **Wrapper Script 方案是最高效解** (playbook §4)。无需重新编译整个工具链。

### 0e: 工具链版本实测与记录 ★ 新增 (实测)

> **⚠️ 实测血的教训**: 实测基于"工具链是 GCC 13.2.0"的错误假设打了 4 个无效 patch，
> 全部在实测审计时退回。**此步骤为强制门控，不可跳过。**

```bash
# 必须实测并记录以下三项（写入 workflow_config.yaml 或构建日志）:
echo "=== GCC Version ==="
{toolchain_prefix}gcc --version 2>&1 | head -1        # e.g. "GCC 7.3.0"
echo "=== GCC Dump Version ==="
{toolchain_prefix}gcc -dumpversion 2>&1                # e.g. "7.3.0"
echo "=== Binutils Version ==="
{toolchain_prefix}ld --version 2>&1 | head -1          # e.g. "GNU ld 2.31.1"
echo "=== Libgcc Path ==="
ls {toolchain_lib_path}/libgcc.a 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

| 检查项 | 期望 | 不匹配时动作 |
|--------|------|-------------|
| GCC version | 记录实际值 | 写入 `workflow_config.yaml.toolchain.gcc_version` |
| Binutils version | 记录实际值 | 写入 `workflow_config.yaml.toolchain.binutils_version` |
| libgcc.a 存在 | EXISTS | NOT FOUND → 检查 `{toolchain_lib_path}` 是否正确拼接 |

**决策规则 (F19)**: 后续所有 patch 的前提条件都基于此步骤记录的实际版本。
- 若 GCC ≥ 8: 预算 `-Wcast-function-type` (#003)
- 若 GCC ≥ 6: 预算 `-Wsign-compare` (#002)
- 若 Binutils ≥ 2.39: 预算单横线选项移除 (#004) — **否则不需要**
- 若换过编译器版本: 预算 ROM_TEXT 余量调整 (#009) — **否则不需要**

### GATE-0 判定矩阵

| 子门控 | 初始状态 | 初测最终 | 复测最终 | 修复动作 |
|--------|---------|------------|------------|---------|
| 0a hb 模块 | ❌ BROKEN | ✅ PASS | ✅ PASS | pip install-e + __init__.py + import fix (16 files) |
| 0b gn 二进制 | ✅ FOUND | ✅ PASS | ✅ PASS | 无需修复 |
| 0c components.json | ❌ MISSING | ✅ PASS | ✅ PASS | hb set auto-generate |
| 0d 工具链 | ❌ NOT INSTALLED | ✅ PASS (假设13.2) | ✅ PASS (实测 7.3.0) | prebuilt + 版本确认 |
| 0d-TC 工具链路径全扫 | N/A | ⚠️ **缺失** | ⚠️ **缺失** | ★ 新增：一次性全扫所有 build 脚本 TC_DIR/工具链路径（实测教训，避免跨阶段漏到 P2 才补） |
| 0e 版本记录 | N/A | ⚠️ **缺失** | ✅ PASS | 新增强制步骤 (实测) |

> **GATE-0 全部 PASS 后才进入 Step 1。任何子门控 FAIL → BLOCKED 并记录原因。**
> **⚠️ 实测更正**: 0e 为新增子门控，实测时缺失此步骤导致 4 个无效 patch。**

---

## Step 1: GN 配置 + Linker 脚本最终化

### 1.1 GN 配置补全

- 确保 `config.gni` 中所有新增源文件路径正确
- 每个 `BUILD.gn` 的 `sources = []` 列表包含实际存在的 `.c`/`.s` 文件
- 参考: `skills/ohos-dev-build-config/references/gn-syntax.md`

### 1.2 Linker.ld 最终化

- 合并 P2 的 linker 草案 + P3 的段需求
- **MEMORY 区域大小校验**: Flash/RAM 茌围是否覆盖所有 section (.text/.rodata/.data/.bss)
- ⚠️ **实测教训**: 不同 GCC 版本代码密度差 ~0.4%/major version, linker script 应预留 **+1~3% 余量**
- 参考: `skills/ohos-dev-build-config/references/linker-templates.md`

---

## Step 2: 全量编译执行

### 2.1 标准编译命令

```bash
# 方式 A: 通过 hb (标准)
./build.sh --product-name {product} --full

# 方式 B: 直接 SDK 内部构建 (绕过超时) ← 实测推荐作为 fallback
cd <sdk_liteos> && sh hm_build.sh <output> linux
```

> **何时使用 fallback**: 当 `./build.sh --product-name {product}` 因 `build_ext_components.py` 硬编码 500s 超时卡住时。
> 配置位置: `workflow_config.yaml` → `build_system.direct_build_cmd`

### 2.2 编译输出预期（Multi-Output 感知）

> **实测验证**: OH wifiiot 产品产出 **3 个独立二进制**, 有独立链接步骤：

| 产物 | 典型大小 | 链接顺序 | 独立性 |
|------|---------|---------|--------:|
| `*boot*.bin` | ~25KB | 第 1 个 | ✅ 完全独立 (自有 link.ld) |
| `*loader*.bin` | ~16KB | 第 2 个 | ✅ 完全独立 (自有 link.ld) |
| `*.out` / 主固件 | ~1-2MB ELF | **最后** | ⚠️ 依赖前两者 ROM_TEXT 容量 |

**判定规则（V11/V12/GATE-B 分工，与编排器 `skills/ohos-dev-workflow-router/SKILL.md` 门控表一致）**:
- **GATE-V11 = 编译门**——只表示编译结果：`./build.sh --product-name {product}`（或 direct_build_cmd）exit 0 + 主产物编译零错误 → **V11 PASS**；主产物 FAIL → **V11 FAIL，且 GATE-B FAIL**（进 Step F 修复循环）
- **GATE-V12 = 产物结构门**——完整烧录包产出 + 大小/结构核验（L0: 单 `.bin` 如 Hi3861_wifiiot_app_burn.bin；L1: boot_image + env + uImage + rootfs + eMMC xml 分区布局，非仅 uImage/vmlinux）：全产物就绪 → **V12 PASS**；主产物 PASS 但次要产物异常 → **V12 FAIL/CONDITIONAL，且 GATE-B 不得 PASS**
- **GATE-B = 两者会签**——V11 与 V12 均 PASS 才可签发 **GATE-B PASS**；任一 FAIL → GATE-B FAIL
- 缺少用户明确允许跳过的非必需产物 → **CONDITIONAL**，GATE-B 不得 PASS，必须进入 GATE-B+ 风险清单

> **关键洞察**: bootloader/loader 成功 ≠ 构建通过。** 必须检查**最后一个/主产物**的链接结果。

### 2.3 编译结果分类

```
./build.sh --product-name {product} (or direct_build_cmd) 执行后:
    │
    ├── exit 0 + 固件产出 → ✅ 进入 Step 3
    │
    ├── exit 非 0 + warning(s) → 🟡 进入 Step F (Compiler Fix Loop)
    │
    └── exit 非 0 + error(s) → 🔴 进入 Step F (Compiler Fix Loop)
```

---

## Step F: Compiler Fix Loop ★ 核心循环

> **这是 Phase 4 最常进入的循环。** 实测在此循环中完成了：
> - 9 个 GT patches (#001-#009)
> - 2 个 experiments (#007 LTO reverted, #008 minimal effect)
> - 1 个 framework patch 组 (hb Python, 16 files)
> - 最终从 BLOCKED → PASS

### ★ 遇 GCC/clang 兼容问题先查 compiler_fix_playbook（别从零重推导，实测教训）

> **实测教训**：P4 编译遇 GCC/clang 兼容问题（musl fortify/atomics/ld 选项/libunwind/C++ 接口等 7+ 类），执行者从零逐个重推导修复，浪费大量 context 重发明已沉淀的方案。协调员指示读 `skills/ohos-dev-build-config/references/compiler_fix_playbook.md` 发现 §8 已有实测回填的 L1-01~L1-22 共 22 项 framework patch（cv610 L1-Linux GCC 12.3.1 专用）+ Wrapper recipe + F-001~F-018 findings。**这些是已沉淀的 GT patch，执行者应直接按表应用，不该重新推导。**

**进入 Step F 第一步（在 F1 错误分类前）必做**：

遇 GCC/clang 兼容问题（包括但不限于以下类别）→ **先查 `skills/ohos-dev-build-config/references/compiler_fix_playbook.md`** 的 Decision Tree + 对应章节的 GT patch 复现，按表应用，别从零重推导：

| 问题类别 | playbook 章节 | 典型 patch ID（参考） |
|---|---|---|
| musl fortify/`diagnose_if`/`pass_object_size`/`enable_if`（clang 专用） | §8 L1-10 同类 + fortify.h 改 | L1-10 |
| musl `stdatomic_impl.h` `__c11_atomic_*`（clang 专用） | §8 L1-12 | L1-12 |
| musl Makefile `-Werror` 下 GCC warning 报错 | §8 L1-13 | L1-13 |
| `kernel.mk` CC=clang 强制 | §8 L1-07 | L1-07 |
| musl libunwind（Clang 库）GCC 无 | §8 L1-08（改 libgcc_eh.a） | L1-08 |
| ld `--no-dependent-libraries`（lld 专用） | §8 L1-09 | L1-09 |
| `_FORTIFY_SOURCE=2`（Clang fortify 不兼容 GCC） | §8 L1-10 | L1-10 |
| kernel.gni `linux_kernel_version` 默认值 | §8 L1-01 | L1-01 |
| musl `LINUXDIR` 指向旧内核 | §8 L1-02 | L1-02 |
| ipc BUILD.gn `configs -= clang_opt` 无条件 | §8 L1-03 | L1-03 |
| board 无 display 实现 | §8 L1-04 | L1-04 |
| ohos.build subsystem 名冲突 | §8 L1-05 | L1-05 |
| GCC 缺 `musl-gcc.specs` | §8 L1-06 | L1-06 |
| build/lite/config `-Werror` 下 GCC 报错 | §8 L1-19 | L1-19 |
| kernel core.c 引用不存在符号 | §8 L1-21 | L1-21 |
| L0 Hi3861 GCC/clang 兼容问题 | §1-7（Hi3861 L0 专用） | XX-XX 系列 |

**应用流程**：
1. 遇编译错误 → 先按错误类别查上表定位 playbook 章节
2. 读对应章节的 GT patch 复现（patch_id / 文件 / diff / 根因）+ Decision Tree
3. 按表应用修复（备份 `.bak.{iter}` → 改 → `bash -n`/`make -n` 语法验证 → 记录 PROVENANCE）
4. playbook 未列的新问题 → 才进 F1 错误分类 + F2 Decision Tree 从零推导，新发现的 patch 记进 PROVENANCE 供后续回填 playbook

> **执行纪律**：playbook 是实测沉淀的知识库，**优先复用已有 patch，别重发明**。playbook 未覆盖才从零推导，且推导出的新 patch 必须记进 PROVENANCE 的 Findings 段供 GATE-交付 评估是否回填 playbook。

### F1: 错误来源分类

```
编译错误日志
    │
    ├── 错误来自【Workflow 再生文件】(hollowed/.c)?
    │   → 【工作流自责】修改生成逻辑 → 重 Phase B → 重新编译
    │
    ├── 错误来自【GT 文件】(device/soc/ 或 vendor/)?
    │   → 进入 F2 (GT File Patch 流程)
    │
    ├── 错误来自【框架代码】(build/, drivers/hdf_core/, base/)?
    │   → 进入 F2 (Framework Patch 流程, 需用户批准)
    │
    ├── 错误来自【第三方库】(third_party/, musl/)?
    │   → 进入 F2 (Third-party Patch, 需用户批准)
    │
    └── 【非编译错误】: SconsBuildError "BASE BIN IS DIFFERENT"?
        → 进入 F2b (SDK 构建系统内部校验锁, 见下方)
```

#### ★ OH 上游代码 bug 处理（完整指引见编排器 `skills/ohos-dev-workflow-router/SKILL.md` §OH 上游代码 bug 处理指引）

> **实测教训**：P4 编译常撞 OH 仓上游代码 bug（非芯片特定）。案例：`surface_lite` C++ 基类 `Surface::SetUserData(const int&, const int&)` vs 子类 `SurfaceImpl::SetUserData(const std::string&, const std::string&)` 签名不匹配 → abstract class，GCC 12 严格检查暴露，clang 不报。此类 bug 不是适配引入的，是 OH 上游共享代码本身的问题，处理不当会污染共享代码影响其他板。

**F1 错误分类时，先区分问题性质**：

| 性质 | 判据 | 处理者 |
|------|------|--------|
| **芯片特定问题** | 只在该芯片工具链/架构/SDK 组合下触发，根因在芯片驱动/配置/工具链路径 | 适配者修（改 `device/soc/` 或 `device/board/` 范围内） |
| **OH 上游代码 bug** | 非芯片特定，任何用 GCC 严格检查/不同编译器/不同架构都可能触发，根因在 OH 共享代码（`foundation/` `drivers/` `build/` `third_party/` 等） | 按下方优先级处理（完整指引见 `skills/ohos-dev-workflow-router/SKILL.md` §OH 上游代码 bug 处理指引） |

**OH 上游 bug 处理优先级（从低风险到高风险，优先选 ①）**：

| 优先级 | 策略 | 适用场景 | 风险 |
|:------:|------|---------|------|
| ① | **绕过依赖**（移除该组件） | 该组件不在 scope（如标准集无 display → graphic 不需要）→ 从子系统配置/BUILD.gn 移除依赖 | 低，只动本板配置，不改共享代码 |
| ② | **最小 patch 绕过**（加 stub / 条件编译 / 去掉 override 关键字等） | 组件在 scope 必须用，但可局部绕过不改共享代码逻辑 | 中，patch 要最小化且打个性化标签，不改共享代码语义 |
| ③ | **修上游**（改 OH 共享代码逻辑） | ① ② 都不可行，必须修共享代码 | 高，改 OH 共享代码影响所有板，必须评估影响面 + 必要时问用户 |

**记 finding**：无论选哪个优先级，OH 上游 bug 必须记进 `PROVENANCE.md` 的 Findings 段：bug 详情（组件/文件/错误现象/根因）+ 处理方式（①/②/③ + 具体改动）+ 影响面评估，供后续 GATE-交付 评估是否回填上游 / 通报 OH 社区。

> **执行纪律**：不改 OH 上游共享代码逻辑除非必要（优先级 ③ 是最后选择）。优先级 ① ② 的改动必须限于本板 scope（子系统配置 / BUILD.gn 条件分支 / 本板 patch），不准把"绕过"写成"改共享代码逻辑"扩散到其他板。优先级 ③ 必要时按 §决策分级 转发用户（改共享代码是 trade-off，属业务决策）。完整指引见编排器 `skills/ohos-dev-workflow-router/SKILL.md` §OH 上游代码 bug 处理指引（实测教训）。

### F2: Compiler Fix Decision Tree

> **完整版见 `compiler_fix_playbook.md` §2 决策树。** 以下是快速参考：

```
错误类型?
│
├─ Warning (-Werror 提升为 error)
│   ├─ __attribute__((const)) on void?          → 移除属性 (Patch #001 模式)
│   ├─ sign-compare in ternary?                 → 显式 (int32_t) 转换 (Patch #002 模式)
│   ├─ cast-function-type?                    → void* 中转 (Patch #003 模式)
│   └─ unrecognized option `-X` (单横线)?           → 删除或改双横线 (Patch #004/#006 模式)
│
├─ Error: undefined reference
│   ├─ 符号在 Workflow 生成的 .o 中?       → 工作流自责, 修生成逻辑
│   ├─ 符号在单体库链接时出现?              → ❌ 不要用 LTO (EXP-007 证实)
│   └─ 符号在 GT 文件中?                     → 检查是否需要新源文件或修正调用
│
├─ Error: region overflowed (ROM_TEXT/RAM/.bss)
│   ├─ 溢出 < 1% of region size?               → linker script 调整 (+1~3% 余量) (Patch #009 模式) ✅ 推荐
│   ├─ 溢出 > 5%?                           → 代码太大, 需要裁剪或优化
│   └─ 尝试过 code optimize 无效?                  → linker adjust 是最后手段
│
└─ Error: assembler / CSR instruction error
    └─ 缺少指令集扩展?                        → Wrapper script 注入 (playbook §4) ✅ 推荐

⚠️ 非编译错误: SconsBuildError
    └─ "BASE BIN IS DIFFERENT WITH FIRST COMPILE"?
        → SDK 二进制指纹锁 (base_sum) → 禁用校验 (Patch #010 模式, playbook §2)
        → 搜索 `base_sum` 或 `base_bin_check` 定位代码位置
```

#### F2b: SDK 构建系统内部校验锁 ★ 新增 (实测)

> **此问题不是编译错误，而是 SDK 构建系统的自我保护机制误触发。**

**症状**:
```
scons_utils.SconsBuildError: ============== BASE BIN IS DIFFERENT WITH FIRST COMPILE! =============
BUILD FAILED!!!!
Failed building build/build_tmp/cache/Hi3861_wifiiot_app_base.bin
```

**触发时机**: ota_builder 阶段（通常在 Step 31/55 左右）重建 system_config.ld 后触发主 app 重新链接

**根因**: Hi3861 SDK 的 `scons_env_cfg.py` 有一个 `base_bin_check()` 方法：
- L79 硬编码 golden SHA256 hash（SDK 原始就有，非工作流加入）
- 每次构建结束后对产出 bin 做 hash 校验
- 任何源码/编译器/标志变更 → 新 bin hash ≠ golden → 抛异常

**修复方式 (Patch #010)**:

```python
# scons_env_cfg.py L79 (init):
self.base_sum = None  # disabled for chip adaptation workflow

# scons_env_cfg.py L269 (check logic):
if self.base_sum is None or self.base_sum == sha256sum:  # 加了 None 判断
    return None
```

**为什么禁用而非删除**: 保留方法结构，量产冻结时可改回 hash 值重新启用

**通用性**: ✅ Hi3861V100 特有，但同类 SoC 厂商 SDK 可能有类似机制

**详见**: `compiler_fix_playbook.md` §2 Patch #010, 规则 F21

### F3: 执行修复与记录

#### F3a: GT File Patch（需用户批准）

> **原则**: "原则上不允许修改非工作流生成的代码"
> **每次修改 GT 文件必须: 备份 → 最小改动 → diff → manifest → 用户确认"

```bash
# 1. 备份
cp <gt_file> {verify_dir}/gt_patches/<filename>.original.{timestamp}

# 2. 最小改动 (只改导致此错误的行)

# 3. 生成 diff
diff -u {backup} <gt_file> > {verify_dir}/gt_patches/<filename>.patch.{timestamp}

# 4. 更新 manifest JSON (patch_id auto-increment, category, approved_by)
```

**Patch 分类**:
| 类别 | 含义 | 是否需要用户批准 |
|------|------|:------------:|
| `warning_fix` | -Werror warning 修复 | ⚠️ 建议告知，可先修 |
| `error_fix` | compilation error 修复 | 🔴 **必须** |
| `compatibility` | binutils/GCC 版本兼容 | ⚠️ 建议告知 |
| `toolchain_adaptation` | SDK 硬编码版本适配 | ⚠️ 建议告知 |
| `memory_layout` | linker script 内存布局调整 | 🔴 **必须** (影响物理映射) |

> **完整 Patch 复现指南 + 9 个实际案例**: 见 `compiler_fix_playbook.md` §2

#### F3b: Framework Patch（需用户批准）

> OH 特有: hb Python 打包 bug 等。见 playbook §3。

#### F3c: Experiment Tracking（尝试性修复）

> 不是所有修复都成功。**必须记录实验**以便后续 iteration 不重复：

```yaml
experiments:
  - id: "EXP-{NNN}"
    hypothesis: "假设..."
    approach: "{做了什么}"
    result: "success | partial | failed | reverted"
    evidence: {before/after/metric}
    conclusion: "{为什么}"
    recommendation: "adopt | avoid | try_with_conditions"
    reverted: true/false
```

> **实测**:
> - EXP-007: LTO (`-flto`) → **reverted** (undefined refs in monolithic libs)
> - EXP-008: 去掉 stack-protector → **partial** (-40B, overflow still 1140B)

### F4: 重编译与循环退出

```bash
# 每轮修复后必须全量重新编译 (不用增量编译!)
<build_cmd>

# 收集结果:
#   exit_code?
#   errors_count?
#   warnings_count? (即使 exit 0 也要记录)
#   firmware outputs? (所有 .bin/.elf)
```

**退出条件**:
- ✅ `exit_code == 0` 且 errors_count == 0 → 进入 Step 3
- ⚠️ 连续 **3 轮**修复后仍卡在同一错误 → **标记 stuck**, 切入 P7 诊断
- ❌ 用户明确要求停止 → BLOCKED, 记录当前状态

---

## Step 3: 二进制大小分析 + Multi-Output 验证

### 3.1 大小分析

#### 3.1a 镜像大小偏差的根因顺序（L1 内核）

`uImage` 大小不能单独作为配置正确性的证明。与参考产物比较时，必须先归档并逐项核对：输入 `defconfig` 与最终 `.config` 的 SHA256、内核源代码基线 commit 与 patch 清单、以及编译器/binutils/目标 triple/`CROSS_COMPILE`/`LLVM` 参数和实际构建命令。对 defconfig 中存在但最终 `.config` 消失的符号，必须检查源码是否有对应 Kconfig；这是源码或 patch gap，不能归为“默认派生项”。

只有上述差异已解释后，才允许把大小差异归因于链接器或压缩波动。参考构建使用不同工具链时标记 `SIZE_COMPARISON_CONDITIONAL`，不得仅凭”接近”自动 PASS；显式配置项未进入最终 `.config` 时，GATE-V12 必须 FAIL/BLOCKED，先修复或补齐源码/patch。

#### 3.1b 产物大小核查（L0/L1 通用）

```bash
# 主固件
size <main_app.out>
# 或
riscv32-unknown-elf-objdump -h <main_app.out> | head -20

# 各产物
ls -la out/<board>/*boot*.bin out/<board>/*loader*.bin out/<board>/*.out
```

| 检查项 | 通过标准 | 实测实际值 |
|--------|---------|-------------|
| 主固件 `.text` 段 | 在 ROM 范围内 | 1.6MB, ROM_TEXT 占用正常 |
| 总固件大小 | 在芯片 Flash 容量内 | boot 25KB + loader 16KB + app 1.6MB |
| bootloader 可独立链接 | 不依赖 main app 产出 | ✅ 独立 PASS |
| 大小偏差 | ±{threshold}% (configurable) | N/A (首次构建无 baseline) |

### 3.2 GATE-V12 固件验证

| 产物 | 状态 | 备注 |
|------|------|------|
| bootloader | ✅ PASS | 25KB, 独立链接 |
| loader | ✅ PASS | 16KB, 独立链接 |
| main_app (.out) | ✅ PASS | 1.6MB, 有效 RISC-V ELF |
| **Verdict** | **PASS** | **全部产物就绪** |

---

## Step 3.5: 标准构建守卫与产物闭合（GATE-B 签发前置）

签发 GATE-B 前，必须跑 `workflow_config.yaml`（`build_quality` + `burn.package` 段）声明的三个守卫：

1. **`deps_guard`（依赖守卫）**：从模块/安装元数据解析全部直接与间接运行时依赖（含 `startup:init`、`customization:config_policy`），与 staging 镜像比对，记录缺失/多余文件。
2. **`startup_guard`（启动守卫）**：校验 init 配置、service 声明、挂载、权限、必需 /dev 节点、启动关联库。守卫失败按四分类归因——`product_board_adaptation`（板级适配）/ `source`（源码）/ `workflow_input`（工作流输入）/ `toolchain_environment`（工具链环境）——并阻断 GATE-B。
3. **`artifact_closure`（产物闭合守卫）**：解析选定的 XML/分区 manifest，要求每个被引用文件都存在于 staging 目录内。默认完整包显式核查 `boot_image.bin`、`env.bin`、`uImage`、`rootfs.ext4`（或 profile 声明的 rootfs 类型）和 XML 本身。任一必需文件缺失即 `BLOCKED`/`INCOMPLETE`，不准静默降级为部分交付。

> **四分类与 P7 诊断分类的关系**：`product_board_adaptation` / `source` / `workflow_input` / `toolchain_environment` 是**构建门控视角的责任归因**（谁的锅：板级适配 / 源码 / 工作流输入 / 工具链环境），用于 GATE-B 阻断与缺口指派；进 P7 诊断后由诊断侧按其 A-H 8 类错误分类（见 `skills/ohos-issue-lite-diagnose`）重新归类。两套分类视角不同、并存使用，互不替代。

**结果独立性**：`deps_guard PASS`、`startup_guard PASS`、编译 PASS、启动链完整性、硬件验收是**相互独立的结果**，一项通过不代表其余通过。仅有内核/rootfs 或中间 eMMC 镜像时必须标 `intermediate/partial`，不能满足最终包闭合（与 GATE-B+ 的 partial package 判定一致）。

---

## Step 4: 烧录验证（GATE-BURN 硬件确认门）

> **GATE-BURN**: 烧录是硬件操作（按目标 L0/L1 选择 HiBurn、HiTool 或厂商 ToolPlatform）。执行者到此**必须停下**，先向用户问询采用哪种模式，获准后才执行。无硬件条件时跳过并记录。

### 用户交互点：烧录模式选择

执行者到此后，向用户提出以下问询：

> 烧录需要硬件操作。你想怎么做？
> - **A. 协助模式**：我来执行 `burn_one.py`（跑烧录脚本、抓串口），但到需要复位板子时我会提示你，**你在板子上按 reset 键**。
> - **B. 手动模式**：你自己烧录 + 跑 XTS，我这边待命，需要我解析结果/排查问题时叫我。

### 按模式执行

- **A 协助模式**：执行者用 `ohos-ci-lite-deploy-burn` skill 跑 `burn_one.py OHOS_Image.bin -com COM4 -baud 115200 --hiburn "${HIBURN_EXE}" --reset-mode at --timeout 90`（外部 HiBurn 路径显式传入，不依赖脚本同目录默认值）；脚本到 reset 节点会等待，执行者**提示用户"请在板子上按 reset 键"**，用户按完确认后继续；串口捕获启动日志验证烧录成功。
- **B 手动模式**：执行者把烧录命令 + XTS 命令交给用户，待用户跑完回报结果，执行者协助解析串口输出/XTS pass-fail。

> **注意**: 此步骤不影响 GATE-B/P4 代码判定。烧录失败通常是硬件/连接问题，不是工作流代码问题。但烧录是 P5 XTS 的前提——不烧录就跑不了 XTS。

---

## 引用的 tools/

| 工具 | 用途 | 路径 | 新增? |
|------|------|------|:----:|
| **ohos-dev-build-config** | GN语法/config修复/错误诊断 | `skills/ohos-dev-build-config` | — |
| **ohos-dev-build-config/references/compiler_fix_playbook.md** | **★ 编译修复完整知识库 (9 patches + wrapper + decision tree + 18 findings)** | `skills/ohos-dev-build-config/references/compiler_fix_playbook.md` | ✅ **新增** |
| **ohos-ci-lite-deploy-burn** | 上板烧录（L0 HiBurn + L1 ToolPlatform/HiTool，含 boot_image 标准构建流程、init.cfg 参考、烧录失败症状表） | `skills/ohos-ci-lite-deploy-burn` | — |

## 语料索引

- **构建装配工具**: `skills/ohos-dev-build-config/references/`
  - `gn-syntax.md`, `error-cheatsheet.md`, `linker-templates.md`, `build-gn-templates.md`
  - **`compiler_fix_playbook.md`** ← ★ 实测沉淀 (本文档的核心依赖)
- **linker 样本(多架构)**: `samples/` (ARM Cortex-M / Cortex-A / RISC-V)
- **构建样本**: 见本步骤 `references/build-lite-reference.md` 与 `references/gn-templates.md`
- **BES2600W 构建**: bibliography.md 中的 gitee 链接

---

## Agent Dispatch Spec

### 分发规格

| 属性 | 值 |
|------|-----|
| **agent_role** | `build-expert` |
| **category** | `deep` |
| **load_skills** | `[ohos-dev-build-config, ohos-ci-lite-deploy-burn, ohos-dev-cross-toolchain]` |
| **dispatch_mode** | **部分并行** |
| **parallel_groups** | G1: [GN配置, linker配置] 并行 → G2: [编译] 串行 → G3: [修复] 循环 |

## Step 4.4: U-Boot 编译 + boot_image 完整产出链（L1-Linux）

GATE-B 内核编译通过后，编译 U-Boot 并产出 boot_image + env，补全完整烧录包。

### 启动链预检（报告"可烧录镜像"前的强制检查）

`./build.sh --product-name {product}` 跑通只证明 GN/Ninja 构建成功，**不证明板子能被烧录、能启动**。把 L1/Linux 产出称为"可烧录"之前，必须核查选定 target profile（`workflow_config.yaml.target.profile` 指向，P1 选定）与 vendor SDK 的完整启动链生产者集合：

- vendor `gslboot_build`（或等价物）的入口、输入与预期 `boot_image.bin` 产出；
- boot 镜像的确切配置输入，含 DDR/寄存器表；
- 目标介质的 env 来源与 `mkenvimage` 产出；
- 目标专属的分区生成器（优先 `env2burn` 或等价物），或直接从 `blkdevparts` 机械化生成的 XML；
- 同一选定介质 profile 的镜像大小与文件系统约束。

在 verification manifest 里**单独记录 `burn_chain_status`**。任一生产者缺失即为 `BLOCKED_VENDOR_SDK`——即使 GN/Ninja 和 `uImage` 都成功，GATE-B+ 也不得 PASS。不准用手工拼装的 U-Boot 二进制顶替 `boot_image.bin`。

默认 `intake.deliverable.goal` 是 `full-burnable-image`。该目标生效且预检被阻塞时，在产出下方第 1-4 项之前就停止烧录包 staging 路径。这些文件可作为普通构建产物留作诊断，但不准放进被当作"部分交付包"呈现的目录。只有用户显式选择 `kernel-rootfs-only` 才允许启用缩减的产物范围。

eMMC 介质在 GATE-B+ PASS 前必须全部满足：

1. `env.bin` 由选定的 eMMC env 文本生成；
2. XML 分区名/起始/长度从 `blkdevparts` 派生，且每个 `SelectFile` 解析到**同一 staging 烧录包目录**内的常规文件（不是构建树里的任意位置）；
3. 内核放得进 env 的 kernel 分区，且 `mkimage -l` 的架构 / load / entry 字段已记录；
4. ext4 镜像不大于 rootfs 分区容量，`file` 或 `dumpe2fs` 确认是 ext4。仅当选定 target profile 显式声明固定大小/填充镜像时才要求两者相等。XML/env 的分区长度描述的是**板上容量**，本身不要求等大的 sparse 或零填充输入镜像；
5. `boot_image.bin` 由 vendor 生产者产出并通过其目标专属的大小/格式检查。

仅第 1-4 项只能构成 `eMMC partial package`（部分包），不是可烧录包。这个区分在 Phase C 与最终交接里必须保持显式。任何包被称为完整之前，staging 后跑一次包闭合检查：

```bash
# 在包含 XML 及其选定文件的目录中执行。
python3 - Hi3516CV610-emmc.xml <<'PY'
import pathlib
import sys
import xml.etree.ElementTree as ET

xml = pathlib.Path(sys.argv[1])
root = ET.parse(xml).getroot()
missing = []
for part in root.findall('.//Part'):
    selected = part.get('SelectFile')
    if selected and not (xml.parent / selected).is_file():
        missing.append(selected)
if missing:
    raise SystemExit('package closure failed; missing: ' + ', '.join(missing))
PY
```

用选定的目标 XML 名，不要用上例的示例名。被引用文件缺失即 `FAIL`——即使其他产物都编译通过；不准在未把该包记录为 partial/blocked 的情况下，交付引用了未来文件或外部文件的 XML。

### ⚠️ boot_image ≠ u-boot.bin（完整产出链原则 A7）
boot_image 是**厂商格式打包产物**，不是裸 u-boot.bin。烧录工具只认厂商私有镜像格式（含 header + U-Boot + 寄存器初始化表），裸/压缩 u-boot.bin 会被烧录工具拒。实测：raw u-boot.bin 238KB 被拒 → 压缩 146KB 被拒 → image_tool 打包成 Hisilicon 格式 309KB 通过。**交付物 = 完整产出链的末端，不是中间步骤。**

### ⚠️ 烧录镜像构建通用原则（L0 + L1，专家结论）

> 专家结论，**L0（Mini/Hi3861）+ L1（hi3516cv610）都适用**。来源：0x81 实测诊断 + Hi3861 L0 官方文档（gitee openharmony/docs quickstart-pkg-3861-build/burn）。

1. **烧录镜像必须从 SDK 编译生成（禁止手工拼）**：
   - L1：`boot_image.bin` 走标准 build（hi3516cv610 = `./build.sh dmeb all debug pack` / `make ... gslboot_build`，dmeb 是 hi3516cv610 产品名，其他 L1 芯片换各自产品名；含 DDR 初始化 + uboot，手工拼易错）。
   - L0：`Hi3861_wifiiot_app_burn.bin` + `Hi3861_loader_signed.bin` 走 `hb set`（选 `wifiiot_hispark_pegasus`）→ `hb build -f`（L0 无 boot_image 打包概念，直接烧 hb 产出的 bin，但仍必须从 SDK 编译）。
2. **SDK 不全必须问用户提供完整 SDK（不能手工拼绕过）**：
   - 完整性标准：能跑标准 build（L1 hi3516cv610: `build.sh dmeb all`，其他 L1 芯片换各自产品名；L0: `hb build -f`）。
   - 获取：向用户索取完整 SDK，或 gitcode/gitee 克隆完整参考仓 + submodule。不要 copy 片段 + 手工拼 input。
3. **同一 SDK 版本标准编译应一致（不一致 = 构建流程错，是诊断信号）**：
   - L1：boot_image 大小/md5 与**该芯片** SDK 标准产出一致（hi3516cv610 debug = 227840B；此值是 hi3516cv610 的，**不是 L1 通用标准**，其他 L1 芯片按各自 SDK 标准产出核对）。
   - L0：`Hi3861_wifiiot_app_burn.bin` 大小与同 SDK 版本标准产出一致；不一致 → 检查 config.gni / 工具链 / SDK 版本。

### ⚠️ 走标准 gslboot_build，不手工拼（0x81 实测教训）
boot_image 构建必须走 SDK 标准 `gslboot_build`，**禁止手工拼**（copy image_tool + 手工喂 3 个 input + oem_quick_build.py）。实测：服务器 SDK 片段不全跑不了标准 `build.sh dmeb all`，被迫手工拼 → boot_image ~200K 与 SDK 标准 223K 不一致 → 烧到 100% `Uncompress Fail! err=0x81`（GZIP 解压 IP 报错）。详见 `skills/ohos-issue-lite-diagnose/references/diagnostic-cases.md` BG002。

**标准构建命令（必须走）**：
```bash
# 方式 A：标准 gslboot_build
make LIB_TYPE=musl CHIP=hi3516cv610 BOOT_MEDIA=spi_nand DEBUG=1 gslboot_build
# 方式 B：等价 build.sh
cd build && ./build.sh dmeb all debug pack
```

**服务器 SDK 片段不全 → 补齐完整参考仓**（gitcode 克隆 + submodule）跑标准 build.sh，不要手工拼 input。

#### ★ vendor 构建系统未提供时的收尾指引（实测教训）

> **实测教训**：工作流假设用户会给完整 vendor 构建系统，但 SDK 只含 soc 片段。P4 Step 4.5 撞到"boot_image 构建需 vendor 构建系统（boards/dmeb/gslboot/u-boot）但 SDK 内缺失"的硬阻塞，工作流没明确"问完用户没有后怎么收尾"——是终止还是跳过还是等。本节补这个收尾指引。

**触发条件**：vendor 构建系统（`boards/dmeb/` + `gslboot_build` + U-Boot 源码 + `osdrv/` + `build/Makefile` 等）在 SDK/OH 仓内缺失，且向用户索取后用户也未提供（或明确表示没有）。

**收尾动作（按顺序，不准默写"boot_image 已构建"而实际没产出）**：

1. **① 显式声明 boot_image 无法构建**——在 PROVENANCE + GATE-V12 报告 + GATE-B+ 消费者验收表里**明确标注**：`boot_image: 未构建（vendor 构建系统缺失）`，不准写"已构建"或留空让人误以为已构建（P-显式未验证的执行约束）
2. **② 问用户提供完整 vendor 构建系统**——向用户索取：完整参考仓（含 `boards/dmeb/` + `gslboot_build` + U-Boot 源码）或厂商 SDK 完整包；提供获取途径（gitcode/gitee 克隆 + `git submodule update --init --recursive`）。**这是业务决策**——用户提供 vs 不提供决定后续走向，按业务分级停转发等用户明确答复
3. **③ 或跳过 boot_image 并在 GATE-B+ 消费者验收标"boot_image 未验证"**——用户明确表示无法提供 vendor 构建系统时，跳过 boot_image 构建，但必须在 GATE-B+ 消费者验收表（见 Step 4.7）的 boot_image.bin 行**显式声明"未验证，需用户试烧/补 vendor 构建系统后再构建"**，且把"boot_image 未验证"明确转交给用户（不准默写"完成"）
4. **④ 不能默写"boot_image 已构建"而实际没产出**——这是 P-显式未验证的硬约束：没编出 boot_image 就不准在 GATE-B+/GATE-交付/PROVENANCE 里写"boot_image 已构建/已完成"。实测：P4 Step 4.5 撞到 vendor 构建系统缺失时，工作流此前只有实测教训"SDK 不全必须问用户"，但没明确"问完用户没有后怎么收尾"，导致 GATE-V12 终止时 boot_image 状态表述模糊

**与其他产物的关系**：boot_image 缺失不影响 uImage（内核）/ rootfs（文件系统）/ env（U-Boot 环境变量）的独立构建——这些产物有自己的构建路径，不依赖 vendor 构建系统。但 boot_image 缺失 = 烧录包不完整 = 无法完整烧录启动，GATE-B+ 整体判定降级为 CONDITIONAL（可进 GATE-交付 归档其他产物，但必须把"boot_image 未验证"明确转交用户）。

**决策分级**：①技术执行（自决声明缺失）；②业务决策（停转发等用户答复是否提供 vendor 构建系统）；③业务决策（用户决定跳过后执行者自决标"未验证"）；④硬约束（不准默写已构建）。

### ⚠️ defconfig 选择：裸烧/下载模式必用 debug（0x81 实测教训）

| 场景 | defconfig | 来源 | 备注 |
|---|---|---|---|
| **裸烧 / 下载模式** | `hi3516cv610_debug_defconfig` | `DEBUG=1` 触发 | ★ 裸烧必用 |
| 量产生产 | `hi3516cv610_defconfig` | 默认（非 debug） | 含 `CONFIG_BSP_DISABLE_DOWNLOAD=y` 生产标志，**不适合裸烧** |

实测：误用非 debug defconfig 裸烧 → uboot 大小差 24K → `Uncompress Fail! err=0x81`。SDK 标准编译（debug defconfig）产出烧出 `Uncompress Ok!`，是强线索。但 0x81 根因**未 100% 确证**（用户手动换"别的 bin"也启动了 uboot），defconfig 差异是定位方向而非已确证唯一根因——见 BG002。

### ⚠️ BOOT_MEDIA 须显式指定（DMEB 默认 SPI Nand）
DMEB demo 板默认 SPI Nand Flash。`build.sh` 默认 `spi`=SPI Nor 与板不符，**必须显式 `BOOT_MEDIA=spi_nand`**。介质确认走 01-env-prep Step 0 前置采集。

### ⚠️ input 来源映射 + 命名陷阱（手工流程也要遵守）
参考仓 `boards/dmeb/Makefile` 的 `gslboot_build` 定义了 3 个 input 的权威来源：
- `gsl.bin` = `components/gsl/pub/gsl.bin`（~20KB）——★ 别误用 `u-boot-hi3516cv610.bin`（见 BG001）
- `reg_info.bin` = `xlsm_to_bin.py` 按变体 xlsm 生成（走 `ohos-dev-soc-spec-parse` 查 xlsm）
- `u-boot-original.bin` = **hw_comp stub**（`u-boot-hi3516cv610.bin` @0x41700000）——★ **命名误导**："original"像未压缩 u-boot.bin，实际要 hw_comp stub，≠ `u-boot.bin`

### ⚠️ 同一 SDK 版本一致性核对（必做）
编出的 boot_image 应与 SDK 标准一致（大小/md5）。实测基线 debug 产出 227840B / ~223K。**不一致 → 构建流程错了**，回溯流程别在二进制位级 debug。

### 产出链探查（先查厂商工具，M3 厂商工具发现原则）
不同芯片的 image_tool 不同（Hi3516 用 `oem_quick_build.py`，其他芯片可能用 mkimg/hiimage）。产出前先查厂商 SDK 有无：
1. **image_tool / oem_quick_build / mkimg 类打包工具**（u-boot + reg_info → 厂商格式 boot_image）——B 类，优先用
2. **xlsm_to_bin / 寄存器配置工具**（.xlsm/.xls → reg_info.bin 寄存器初始化表）——B 类
3. **secure boot 变体工具**（oem_quick_build_secure_boot.py / 签名工具 / 密钥）——见下方安全模式
4. 查到厂商工具 → 用之（B 类，别重造轮子）；查不到 → 自己写打包脚本（C 类）+ 记录降级理由

### 流程
1. **编译 U-Boot**：`make CROSS_COMPILE={prefix} {chip}_{media}_defconfig` → `make` → 产出 raw `u-boot.bin`（**中间产物，非 boot_image**）
2. **reg_info.bin**（寄存器初始化表）：用厂商 `xlsm_to_bin.py` 把 `.xlsm` → `reg_info.bin`（B 类工具）。**`.xlsm` 选哪个由 SoC 内置 DDR 变体决定（如 Hi3516CV610 -10B 用 DDR2 64MB QFN xlsm，-20S/-20G 用 DDR3 128MB QFN xlsm），走 `ohos-dev-soc-spec-parse` skill 单点查询"该用哪个 xlsm"**（命中 `ddr-variant-guide.md` 变体表直接回答，含 magic/命令）；ohos-dev-soc-spec-parse 未覆盖则查厂商 SDK boot_tools 目录 + 产品简介型号配置差异表（手工仅作回退）。无此工具则查 SDK 有无等价寄存器配置
3. **boot_image.bin**（厂商格式）：用厂商 `image_tool`/`oem_quick_build.py` 把 `u-boot.bin + reg_info.bin` 打包成厂商格式 boot_image（B 类工具）。**这一步产出的才是 boot_image**
4. **env.bin**：用 `mkenvimage -s {size} -o env.bin emmc_env.txt`（标准工具，B 类）。env 配置（bootcmd/bootargs/blkdevparts/rootfstype）从板级 spec/厂商参考调整（A 类）

### 安全模式变体（W3，P1 Step 5 检测结果的下游）
P1 Step 5 已检测 `intake.security.secure_mode`。此处的下游动作：
- `secure_mode: secure` → 用厂商 `oem_quick_build_secure_boot.py` 替代普通 build（产签名 boot_image）+ 需密钥（public_and_private_keys.py）+ 可能 TEE 变体（oem_quick_build_tee.py / emmc_tee_env.txt）。**问用户**密钥来源（厂商提供 / 自生成）
- `secure_mode: non-secure`（默认）→ 用普通 build，但**必须显式声明选了 non-secure**（不能默认跳过不记录，M4）
- `secure_mode: 未检测` → 回 P1 Step 5 补检测，不准跳过

> U-Boot 源码用厂商公开仓 + defconfig（B 类），boot_image 用厂商工具打包（B 类），env 配置从 spec 派生（A 类）。不自己写 U-Boot 源码，不自己造 image_tool。env2burn.py 生成的是**分区 xml**（见 Step 4.6），不是 env.bin——env.bin 用 mkenvimage。

## Step 4.5: rootfs 构建（L1-Linux 厂商构建路径）

GATE-B 编译通过后，构建 rootfs（可烧录镜像的文件系统部分）。

### 原则（最小厂商依赖）
- **rootfs 结构自己设计**（标准 Linux 目录 /bin /etc /lib /sbin...）——C 类
- **busybox 开源**，自己获取/编译（不依赖厂商）——C 类
- **init 脚本自己写**（标准 Linux init）——C 类
- **SDK .so 预编译库**直接放入 rootfs/lib（厂商提供）——B 类
- **不抄厂商 rootfs**——自己生成结构 + 脚本

### 流程
1. 获取 busybox（开源：下载源码编译，或用仓内已有的）
2. 创建 rootfs 目录结构（/bin /etc /sbin /lib /usr...）
3. 放入 busybox → /bin/busybox + 符号链接
4. 放入 SDK .so → /lib/
5. 写 init 脚本（/etc/init.d/rcS 或 /etc/inittab）
6. 放入内核模块 .ko（如有）→ /lib/modules/

### ⚠️ B6.0 rootfs 版本标记文件（构建侧写，诊断侧核对）

> 与 `skills/ohos-issue-lite-diagnose` Step 2.3（诊断侧核对版本标记）联动——**构建侧写、诊断侧核对**。本节是构建侧的写法。

**适用范围**：仅限多轮迭代调试期（如某子系统适配多轮定位）。第一稿适配一次通过不打标记。

**构建侧每次改 rootfs 必做**：
1. rootfs 写版本标记文件 `/etc/rootfs_version`，内容含：版本号 + 构建时间 + 关键改动（如 `oh-lite-rootfs fixXX-20260724\nfix: <本次改动摘要>`）
2. 版本号规则从 `workflow_config.yaml.burn.version_rule` 消费（默认 `{chip}_{date}`；多轮调试可由用户显式加 iter 后缀）
3. init.cfg post-init job 里加 `exec /bin/busybox cat /etc/rootfs_version` 打印到串口——**必打**（放 init.cfg 保证每次开机都打，不靠人记得 echo）
4. **高亮告知用户：此版本标记是调试临时标记，问题定位完成、回归验证通过后必须从 init.cfg + rootfs 删掉，不永久留存于正式产出**
5. 标记随烧录件一起更 changelog（见 D4 + memory `update-changelog-after-burnfile-change`）

> 通用方法：版本号规则前置采集（01-env-prep Step 0），构建侧写入 rootfs + init.cfg 打印，诊断侧拿到日志先 grep 版本标记核对。三方联动避免多轮迭代时日志和烧录件对不上。

### ⚠️ B6 rootfs 启动项五件套（init.cfg pre-init 必按序，bring-up 期必做）

OH beget init 不像标准 Linux sysvinit 自动挂 `/proc` `/sys`，只自动挂 devtmpfs。rootfs 的 init.cfg `pre-init` job 必须**按序**手动挂五件套，否则 service 起来后找不到 proc/sys/cgroup/binder → 各种诡异失败：

1. **mount proc + sysfs**：
   ```
   mount proc proc /proc
   mount sysfs sysfs /sys
   ```
2. **mount cgroup**：
   ```
   mkdir /sys/fs/cgroup
   mount cgroup none /sys/fs/cgroup
   ```
3. **mount binder**：
   ```
   mkdir /dev/binderfs
   mount binder binder /dev/binderfs
   ```
   > 注：本项假定禁了 binderfs 时 `/dev/binder` 由 devtmpfs 自动建（init.cfg 仍要 `chmod 0666 /dev/binder`，见 `skills/ohos-ci-lite-deploy-burn/references/l1-init-cfg-reference.md`）。cgroup 仍需显式挂。

> 完整 init.cfg（18 services + pre-init/init/post-init job + 目录权限清单）见 `skills/ohos-ci-lite-deploy-burn/references/l1-init-cfg-reference.md`。

### ⚠️ B6.1 init.cfg pre-init 时序约束（mount→chmod→mknod→start service 顺序不能错）

pre-init job 内的命令**必须按序**，错序会导致 service 启动时缺节点/缺权限：

1. **mount 伪文件系统**（proc/sysfs/cgroup/binder，见 B6 五件套）——最先，后续命令可能依赖 /proc /sys
2. **chmod /dev/\***（如 `chmod 0666 /dev/binder`）——必须在依赖该节点的 service start **前**。典型：`chmod 0666 /dev/binder` 必须在 foundation start 前（foundation 启动时要 open /dev/binder 做 BINDER_SET_CONTEXT_MGR，权限不足→EACCES→context mgr 起不来→IPC 不通）
3. **mknod /dev/\***（如 `exec /bin/busybox mknod /dev/hilog c 245 0`）——必须在依赖该节点的 service start **前**。典型：mknod /dev/hilog 必须在 hilog/apphilogcat 服务 start 前
4. **start service**（init job 的 start 序列）——最后，此时所有节点/权限/挂载就绪

> 通用原则：init.cfg 的 pre-init 是"环境准备"，init 是"起服务"。所有 mount/chmod/mknod 放 pre-init，service start 放 init。pre-init 内部按 mount→chmod→mknod 顺序。某 service 依赖某 /dev 节点 → 该节点的 mknod/chmod 必须排在该 service start 前。错序症状：service 起来报 `open /dev/xxx failed` 或 `EACCES`，但节点其实存在（只是建晚了/权限设晚了）。具体时序案例见 `skills/ohos-ci-lite-deploy-burn/references/l1-init-cfg-reference.md`。

### ⚠️ B7 OH param 目录三件套必填（缺则 softbus/deviceauth/huks 起不来）

rootfs 必须有 4 个 param 文件（从 OH `out/{product}/` 拷），缺一不可：

| 路径 | 来源 |
|---|---|
| `/system/etc/param/ohos_const/ohos.para` | OH out 拷 |
| `/system/etc/param/ohos.para` | OH out 拷 |
| `/system/etc/param/ohos.para.dac` | OH out 拷（DAC 访问控制） |
| `/vendor/etc/param/vendor.para` | OH out 拷 |

**softbus 额外补 4 参数**到 `vendor.para`（缺则 softbus 初始化失败）：
- `const.distributed_collaboration.productId`
- `const.build.ver.physical`
- `ohos.boot.sn`
- `ro.build.version.sdk`

**缺 param 的症状**：启动日志 `Read dir :/system/etc/param/ohos_const failed` → softbus / deviceauth_service / huks_server 起不来。实测：补 param 目录后 deviceauth/softbus 才正常（见 task #56）。

### ⚠️ B8 bring-up 期 importance:0 防 reboot loop（init.cfg 全 service）

bring-up 期 init.cfg 所有 service 设 `importance: 0` + **去掉 `critical` 数组**。否则 service 退出 → init `ReapService` 见 IMPORTANT 属性 → `reboot(RB_AUTOBOOT)` 软重启 loop（实测方案 B reboot loop 根因：内核没编 watchdog 驱动 → `/dev/watchdog` 缺 → watchdog_service 退出 → reboot loop）。

- **bring-up 期**：全部 service `importance: 0`，去掉 `critical` 数组（含 ueventd 的 `critical: [0,15,5]`）。
- **稳定后恢复稳态值**：`watchdog_service` importance=-20，`foundation` importance=1。
- **根因侧**：缺 `/dev` 节点优先做内核驱动适配（defconfig+DTS+重编 uImage），别只靠 rootfs 绕过——见 memory `prefer-driver-adaptation-over-rootfs-bypass` + `skills/ohos-issue-lite-diagnose`。

> 带查 symptom：启动到一半循环重启 / 串口反复打 init 日志 → 先查 init.cfg 有无 critical/importance 非零 + 对应 service 的 `/dev` 节点是否存在。

### ⚠️ B8.1 importance 技术债恢复策略（bring-up 期全 0 → 稳定后恢复稳态值）

bring-up 期为防 reboot loop 把全 service importance 设 0，是**临时技术债**——稳态下 importance 分级是系统韧性的一部分（关键 service 挂了该触发恢复/告警，不能静默）。稳定后必须恢复，不能遗留全 0 进量产。

**恢复时机判定**（全部满足才恢复）：
1. `/dev` 节点齐全（watchdog/binder/hilog 等驱动适配完成，不再靠 rootfs 绕过）
2. 全 service 正常起来（无 reboot loop、无连锁挂死）
3. XTS 核心用例通过且不触发 reboot loop

**恢复清单**（按上游稳态值，具体值进 references，本表只给通用方法）：
- 关键看门狗类 service（如某 watchdog service）：恢复高优先级 importance（如上游 -20）
- 核心 SA（如某系统服务管理进程）：恢复中优先级 importance（如上游 1）
- 辅助/非关键 service：保持 0 或按上游值

**恢复后验证**：恢复 importance 后重烧、跑 XTS 核心用例 + 多次启动，确认不回归 reboot loop。回归了 → 回退 importance 再查根因（通常是某个 `/dev` 节点其实没真正适配好，恢复 importance 后该 service 挂了触发 reboot）。

> 通用方法：全 0 是 bring-up 期技术债，不是终态。具体某芯片的 N 个 service 稳态值清单进 `skills/ohos-ci-lite-deploy-burn/references/l1-init-cfg-reference.md`（如 hi3516cv610 18 服务稳态值表）。

### ⚠️ B8.2 删服务前依赖审计（删任一 service 前必查 .so 依赖闭包）

bring-up 期常想删某个起不来的 service "减负"，但 service 之间有 .so 依赖——删了 A 可能导致 B 链接 A 的 .so 失败 → B 也起不来 → 连锁。

**删服务前必做**：对该 service 的可执行文件 + 它提供的 .so，**递归**查哪些其他 service 链了它们：

```bash
# 查某 service 可执行文件依赖的 .so（确认它不依赖别人）
readelf -d <rootfs>/bin/<service> | grep NEEDED
# 查某 .so 被谁依赖（确认删了它不会让别的 service 断链）
# 遍历 rootfs 所有 ELF，grep NEEDED 里有没有该 .so
for elf in $(find <rootfs> -type f -exec sh -c 'file "$1" | grep -q ELF' _ {} \; -print); do
    readelf -d "$elf" 2>/dev/null | grep -q "<target>.so" && echo "$elf 依赖 <target>.so"
done
```

**判定**：
- 该 service 可执行文件依赖的 .so 都在 rootfs（删它不影响别人对它没依赖的情况）→ 可删
- 有其他 service 链了该 service 提供的 .so → **不能删**（删了会让依赖方断链起不来），要么保留该 service，要么把 .so 留下只删可执行文件
- 递归查 NEEDED：A 依赖 B.so，B.so 又依赖 C.so → 删 C.so 会同时断 A 和 B

> 通用方法：删 service 不是删一个文件——它是 .so 依赖图里的一个节点，删前查入度（谁依赖它）。实测教训见 `skills/ohos-ci-lite-deploy-burn/references/l1-init-cfg-reference.md`（softbus_server 是 foundation 硬依赖案例）。

### ⚠️ B10 musl ld==libc + __fd_chk 符号（rootfs /lib 动态链接器）

OH musl **无独立 ld-musl-arm.so.1**，`libc.so` 即动态链接器。rootfs `/lib/ld-musl-arm.so.1` 必须是 **OH sysroot `libc.so` 的拷贝**（md5 一致），不能用 prebuilts 独立版。

```bash
# 验证：md5 一致
md5sum <OH_sysroot>/lib/libc.so <rootfs>/lib/ld-musl-arm.so.1   # 两者应相同
# 验证：含 OH fortify __fd_chk 符号
nm -D <OH_sysroot>/lib/libc.so | grep __fd_chk
```

**根因**：prebuilts 独立 ld-musl 版缺 OH fortify 符号（`__fd_chk` 等）→ 全部 service 启动报 `Error relocating: symbol not found`。实测教训：用错 ld → service 全起不来，错误指向各 .so 缺符号，实际是动态链接器错。

## Step 4.6: 镜像打包 + 分区 xml

把 rootfs 目录 + uImage 打包成可烧录镜像，生成分区 xml。

### rootfs 镜像（按 flash 类型选文件系统 + 三方一致 gap7）
- **eMMC → ext4**（`mkfs.ext4`/`mke2fs -t ext4`），**NOR → jffs2**（`mkfs.jffs2`），**NAND → jffs2/ubifs**
- 文件系统类型从 env 的 `rootfstype=` 或芯片 spec 确认，**不能写死 jffs2**（实测：初版 jffs2 错，env rootfstype=ext4）
- **三方一致（机器可查，进 GATE-B+）**：`内核 rootfstype` ↔ `rootfs 镜像实际文件系统`（`dumpe2fs`/`file` 验证）↔ `eMMC xml 的 FileSystem 属性` 三者必须一致
- 打包脚本自己写（调标准 mkfs，C 类），不抄厂商 mkimg

### 分区 xml（C2/W2：先查厂商工具，禁止凭空编造）
分区布局从 env bootargs 的 `blkdevparts=` 派生。**生成方式优先级**：
1. **优先查厂商 SDK 有无 env2burn/mkburnxml 类工具**（从 env 文本自动生成 burn xml，B 类）——参考仓有 `env2burn.py`，执行者手写 xml 出错（misc/userdata、大小不匹配）；有工具就别手写
2. **无工具** → 解析 `blkdevparts=mmcblk0:512K(boot),512K(env),4M(kernel),96M(rootfs)` 字符串生成 xml（提供解析模板，C 类）
3. **禁止凭空编造分区名/大小**——分区名必须与 env bootargs 中的分区名**一致**（曾有执行者自拟 fastboot/boot，参考仓用 env 原名 boot/kernel；用 env 原名，不自拟）

### 完整包
uImage + rootfs 镜像(ext4/jffs2/ubifs) + boot_image.bin + env.bin + 分区 xml → 可烧录包

> 文件系统类型必须跟 env rootfstype 一致（三方一致，进 GATE-B+）。分区 xml 优先用厂商 env2burn 类工具，禁止凭空编分区名/大小。

## Step 4.7: GATE-B+ 烧录包消费者验收门控 ★ 自校验环节（Task3 / 实测沉淀）

> **为什么有这一步**：实测中反复出现"执行者以为行了，用户一试不行"——boot_image 格式被烧录工具拒、rootfs jffs2/ext4 错、xml 分区对不上。根因：之前的 GATE 只查**产出物存在性 + 编译通过**（自省式"我产出 X 了吗"），不查**消费者接受性**（对抗式"X 的消费者真的接受吗"）。本门控补这半边。

### 原则（P-消费验收 / P-对抗自检 / P-显式未验证）
- 每个烧录包产物必须标识其**消费者** + 给出**接受性外部锚**（不能自证"我产出了所以能用"）
- 外部锚四类：① 厂商工具产出 ② magic-byte/格式校验匹配已知 good 样本 ③ 跨产物一致性机器可查 ④ 用户试烧/试运行通过
- **拿不到外部锚 → 必须显式声明"未验证 + 需谁来验证"，不准写"完成"**（逼 gap 在用户试之前暴露）

### 消费者验收表（每个产物必填）

| 产物 | 消费者 | 接受性证据（外部锚） | 机器可查? | 无锚时 |
|---|---|---|:---:|---|
| boot_image.bin | 烧录工具 | ① 厂商 image_tool 产出 / ② magic-byte 匹配已知 good boot_image / ③ 参考仓同构产出 / ④ 用户试烧通过 | 部分 | 显式声明"未验证，需用户试烧" |
| **boot_image 大小与 references 标准核对**（必查） | references 标准（同 SDK 标准编产出） | boot_image 大小 == references 标准值（hi3516cv610 debug = 227840B；其他芯片查 `compiler_fix_playbook` §8 / vendor SDK 标准）。核对方式：`mkimage -l` / `hexdump` magic + `stat` 大小比对 references 标准值。大小匹配 → ✅；不匹配（偏离>5%） → ❌ **FAIL**（构建流程错，不准标 PASS，不准烧录），查根因：prebuilt u-boot vs 源码标准编 / 未标 DEBUG=1 defconfig / reg_info 错 / gslboot_build 路径错 | ✅ | 显式声明"未验证，需查 references 标准值后核对" |
| env.bin | 内核/U-Boot | rootfstype↔rootfs 一致 + blkdevparts↔xml 一致（跨产物）+ mkenvimage 产出 | ✅ | 同上 |
| uImage | U-Boot bootcmd | `mkimage -l uImage` 头校验（FIT/uImage 格式） | ✅ | 同上 |
| rootfs.ext4 | 内核 rootfstype | `dumpe2fs`/`file` 验证是 ext4 + env rootfstype=ext4 + xml FileSystem=ext4（三方一致） | ✅ | 同上 |
| eMMC xml | 烧录工具分区加载器 | 每个 SelectFile 存在 + Start/Length 不重叠不越界 + FileSystem↔SelectFile 内容一致 + 分区名↔env blkdevparts 一致 | ✅ | 同上 |
| **SPI Nand 颗粒 ID 覆盖**（板子用 SPI Nand 时必查） | 内核 fmc_ids 表 + U-Boot fmc_ids 表 | **有硬件/烧录日志**：板子实际颗粒 ID（如 DS35Q1GB-IB = 0xe5/0xf1）在内核 `drivers/mtd/spi/nand/fmc_ids_hi3516cv610.c` + U-Boot `drivers/mtd/spinand/` 的 fmc_ids 表里都能查到条目（用 `strings vmlinux` + `grep` U-Boot 源码双查）→ ✅ 在表里 / ❌ 不在表里（烧前补条目重编）。**无硬件/烧录日志**：标 ⚠️ **待烧录验证**——不假设 vendor 表覆盖实际板子（实测同板 DS35Q1GB-IB 不在 vendor 表），烧录后 probe 失败（0x81）→ 加颗粒条目重编 | ✅ | 显式声明"⚠️ 待烧录验证，需查板子实际颗粒型号 + ID 后补条目" |

### 机器可查的一致性检查（必须跑，不靠人眼）
- [ ] env.rootfstype == rootfs 镜像实际文件系统（dumpe2fs/file）== xml.FileSystem
- [ ] xml 分区数 == env blkdevparts 分区数，每分区名/大小一致
- [ ] xml 每个 SelectFile 指向的文件存在
- [ ] xml Start+Length 不重叠、不越界（不超介质总容量）
- [ ] uImage `mkimage -l` 通过
- [ ] boot_image 有厂商工具产出证据或 magic-byte 匹配（无→声明未验证）
- [ ] **★ boot_image 大小与 references 标准核对**（必查）：`stat` boot_image 大小 + `mkimage -l`/`hexdump` magic，与 references 标准值（hi3516cv610 debug = 227840B；其他芯片查 `compiler_fix_playbook` §8 / vendor SDK 标准）比对。偏离>5% → **FAIL**（构建流程错，不准标 PASS，不准烧录），查根因：prebuilt u-boot vs 源码标准编 / 未标 DEBUG=1 defconfig / reg_info 错 / gslboot_build 路径错（实测教训：偏离 223K = 构建流程错，烧出 0x81）
- [ ] **★ SPI Nand 颗粒 ID 覆盖验证（板子用 SPI Nand 时必查）**：**有硬件/烧录日志** → 板子实际颗粒 ID 在内核 + U-Boot 的 fmc_ids 表里都有条目（`strings vmlinux | grep <颗粒ID>` + U-Boot 源码 `grep <颗粒ID> drivers/mtd/spinand/` 双查）；不在表里 → 烧了 SPI Nand probe 失败（0x81 实测教训），必须烧前补条目。**无硬件/烧录日志**→ 标 ⚠️ **待烧录验证**，不假设 vendor 表覆盖实际板子（实测同板 DS35Q1GB-IB 不在 vendor 表）；烧录后 probe 失败（0x81）→ 加颗粒条目重编

### ⚠️ SPI Nand 颗粒 ID 覆盖未验证不能默写"boot_image 已构建"（实测教训）

> **实测教训**：板子 DMEB 的 SPI Nand 颗粒是 DS35Q1GB-IB（ID 0xe5/0xf1），不在 vendor 干净 SDK 的 fmc_ids 表（只有 HY035/HY073）→ boot_image 烧到板子 SPI Nand probe 会失败（起不来）。工作流 P2 内核驱动 port 没指引"查颗粒 ID 覆盖"，GATE-B+ 消费者验收也没"颗粒 ID 覆盖验证"项，briefing 也没把颗粒 ID 作为板子规格采集。**板子用 SPI Nand 时，颗粒 ID 覆盖是烧前必查项（不查烧了炸，0x81 实测教训）。**

**板子用 SPI Nand 时必做（在 GATE-B+ 消费者验收前完成）**：
1. **查板子实际颗粒型号 + ID**——从板子规格书 / briefing / 厂商 SDK 查颗粒型号（如 DS35Q1GB-IB）+ JEDEC ID（如 0xe5/0xf1）
2. **核查内核 fmc_ids 表**——`strings <out>/vmlinux | grep <颗粒ID或型号>` + 查内核源码 `drivers/mtd/spi/nand/fmc_ids_*.c` 有无该颗粒条目（用 vmlinux 验符号，不用 zImage——见 B12）
3. **核查 U-Boot fmc_ids 表**——查 U-Boot 源码 `drivers/mtd/spinand/` 的 fmc_ids 表有无该颗粒条目（U-Boot 也要 probe SPI Nand，缺条目同样炸）
4. **不在表里 → 烧前补条目**——按 vendor fmc_ids 表格式加条目（id/page_size/block_size/ooo_size/quad_read 等），重编 vmlinux + U-Boot + boot_image。**不准默写"boot_image 已构建"而颗粒 ID 没查**（P-显式未验证的硬约束，同理）

**颗粒 ID 查不到时的处理（决策分级）**：
- 颗粒型号能查到但 ID 表没条目 → **技术执行自决**补条目（按 vendor 格式 + 颗粒 datasheet 参数），重编
- 颗粒型号查不到 → **业务决策停转发**问用户板子实际颗粒型号（ briefing 没采集时回 P1 Step 0 补采集）

> **★ 无硬件/烧录日志时标"待烧录验证"**（实测教训）：板子无硬件或无烧录日志时，颗粒 ID 覆盖无法实测验证——此时**不假设 vendor 表覆盖实际板子**（实测同板 DS35Q1GB-IB 不在 vendor 表，vendor 表只查到 HY035/HY073）。GATE-B+ 消费者验收表颗粒 ID 行标 ⚠️ **待烧录验证**（不标 ✅ PASS，也不标 ❌ FAIL），并显式声明"烧录后 probe 失败（0x81）→ 加颗粒条目重编"。烧录延后 ≠ 风险消除——此为已知风险的延迟暴露，烧录时大概率撞上。**不准默写"vendor 表已覆盖"而实际未验**（P-显式未验证的硬约束）。

> **通用原则**：板子用 SPI Nand 时，颗粒 ID 覆盖验证与 boot_image 格式验证、rootfs 文件系统一致性同优先级——都是"烧了炸"级别的烧前必查项。未验证项不能默写"已构建"带过，必须显式声明"未验证，需查颗粒 ID 后补条目"（P-显式未验证）。无硬件时标"待烧录验证"并转交用户。

### ⚠️ boot_image 大小与 references 标准核对（GATE-B+ 硬检查，实测教训）

> **实测教训**：boot_image 产了 366KB，但实测基线 227840B（223K），references（`compiler_fix_playbook` §8 / 本 SKILL §烧录镜像构建通用原则）写了 227840B 标准但 GATE-B+ 没强制核对——Role 3 标 PASS 但大小错（偏离 223K = 构建流程错，烧出 0x81，实测教训）。GATE-B+ 消费者验收表必须加一行"boot_image 大小与 references 标准核对"作为**硬检查**。

**核对标准（按芯片查 references）**：
- **hi3516cv610 debug** = 227840B（223K）——已实机验证可启动的标准锚点（`Hi3516CV610_clone` 完整参考仓 + `make LIB_TYPE=musl CHIP=hi3516cv610 BOOT_MEDIA=spi_nand DEBUG=1 gslboot_build -j4` + `hi3516cv610_debug_defconfig`，烧出 `Uncompress Ok!` + 进 OH shell）
- **其他芯片** → 查 `compiler_fix_playbook` §8 / vendor SDK 标准 / 已实机验证的参考产出
- **hi3516cv610 非 debug** = 不适用裸烧（`hi3516cv610_defconfig` 含 `CONFIG_BSP_DISABLE_DOWNLOAD=y` 生产标志，不适合裸烧，见 §defconfig 选择）

**核对方式**：
```bash
# 1. 大小
stat -c %s boot_image.bin   # 期望 == references 标准值（如 hi3516cv610 debug = 227840B）
# 2. magic + 版本字段（辅助确认格式）
hexdump -C boot_image.bin | head -2   # hi3516cv610: magic eaff0000 + 版本 0002 0000
# 3. (如 boot_image 含 U-Boot) mkimage 头校验
mkimage -l boot_image.bin 2>/dev/null
```

**判定**：
| 大小核对结果 | 判定 | 动作 |
|---|---|---|
| 大小 == references 标准值（或偏差≤5%） | ✅ PASS | 进下一项检查 |
| 大小偏离 references 标准>5% | ❌ **FAIL** | **不准标 PASS，不准烧录**。查根因（按可能性排序）：① **u-boot.bin 不同源**（prebuilt vs 源码标准编）→ 重走标准 `gslboot_build` 从源码编；② **defconfig 变体错**（未标 DEBUG=1 / 用了非 debug defconfig）→ 用 `hi3516cv610_debug_defconfig` + `DEBUG=1` 重编；③ **reg_info 错**（xlsm 选错 DDR 变体）→ 走 `ohos-dev-soc-spec-parse` 查对应 xlsm 重转；④ **gslboot_build 路径错**（手工拼而非标准 build）→ 走标准 `build.sh dmeb all debug pack` / `make ... gslboot_build` |
| references 无标准值（新芯片无已验证产出） | ⚠️ 待建立标准 | 显式声明"无 references 标准，需用户试烧后建立锚点"，首轮以试烧通过为锚点回填 references |

> **实测教训**：偏离 223K = 构建流程错（用了 prebuilt u-boot 而非源码编 / 未标 DEBUG=1 defconfig / reg_info 错 / 手工拼而非标准 gslboot_build），烧出 0x81 Uncompress Fail。实测 7/20 干净版 219.5K 偏离标准就烧出 0x81 回归。**大小不匹配是构建流程错的强信号，别在二进制位级 debug，回溯流程**（见 §同一 SDK 版本一致性核对）。

> **决策分级**：大小核对是技术执行（机器可查）→ 自决核对；大小不匹配查根因是技术执行 → 自决重编；references 无标准值需试烧建立锚点 → 业务决策（停转发问用户是否试烧）。

### ⚠️ B11 烧前依赖闭包校验（GATE-B+ 机器可查项）

对 rootfs 全部 ELF（.so/.可执行）**递归** `readelf -d`，验所有 NEEDED 依赖 + UNDEFINED 符号可解，输出 `X ELF checked, 0 missing`。烧前把"运行时 `symbol not found`"提前到烧前机器可查。

```bash
# 遍历 rootfs 所有 ELF，递归查 NEEDED 依赖是否都在 /lib + UNDEFINED 符号能否解
for elf in $(find <rootfs> -type f -exec sh -c 'file "$1" | grep -q ELF' _ {} \; -print); do
    readelf -d "$elf" | grep NEEDED    # 每个 NEEDED 必须在 rootfs/lib 找到
    readelf -s "$elf"  | grep UND      # 每个 UNDEFINED 符号必须在某 .so 解到
done
# 期望汇总：X ELF checked, 0 missing
```

**判定**：`0 missing` → 该项 PASS；任一 NEEDED 找不到或 UNDEFINED 解不了 → **FAIL**（不准烧，先补 .so 或换对 ld-musl，见 B10）。实测：依赖闭包校验抓出 `libdsoftbus_server_plugin.so` 缺失 + ld-musl 用错（见 B10）。

### ⚠️ B12 内核符号验用 vmlinux 非 zImage（GATE-B+ 验证段）

验驱动符号（`binder_init` / `hilog_init_module` / `dw_wdt_drv_probe` / `DS35Q1GB-IB` 等）**用 `vmlinux`**，**不用 zImage**——zImage 是压缩的，`strings` 验不全。

```bash
# ✅ 对：用未压缩 vmlinux
strings <out>/vmlinux | grep -E 'binder_init|hilog_init_module|dw_wdt_drv_probe|DS35Q1GB'
# ❌ 错：zImage 压缩，strings 验不全
strings <out>/zImage | grep binder_init   # 可能漏报
```

**用途**：确认内核 defconfig 开了对应驱动（binder/hilog/watchdog/SPI Nand ID 表）+ DTS 节点生效。验不到符号 → 回 P2 内核步补 defconfig/DTS（见 memory `prefer-driver-adaptation-over-rootfs-bypass`）。

### ⚠️ D4 改烧录件立即更 CHANGES_*.md（通用规则，与 ohos-ci-lite-deploy-burn 附录联动）

每次改烧录件（`boot_image`/`uImage`/`env`/`rootfs`/`burn_table`）后**立即更新** `partitions/CHANGES_*.md`：记录改了什么 + 新 md5 + 根因/修复说明。每产物带 md5 历史。

- changelog 按日期分文件（`CHANGES_20260717.md` / `CHANGES_20260720.md` ...），同日多次改更新同文件
- 文件清单表更新 md5 + 大小 + 改动说明；加修改小节（改了什么/为什么/根因）
- 子代理改完烧录件也要让它更新 changelog（或在主会话补）
- 详见 memory `update-changelog-after-burnfile-change` + `skills/ohos-ci-lite-deploy-burn` 附录

### 判定
- 全部产物有外部锚 + 一致性检查全过（含 boot_image 大小核对匹配 + 颗粒 ID 覆盖验证） → **GATE-B+ PASS**
- **boot_image 大小偏离 references 标准>5%→ FAIL**（构建流程错，不准标 PASS，不准烧录，查根因重编）
- 任一产物无外部锚且未声明"未验证" → **FAIL**（不准进 GATE-交付）
- 颗粒 ID 无硬件/烧录日志时标 ⚠️ 待烧录验证→ 该项 **CONDITIONAL**（可进 GATE-交付 归档，但必须把"待烧录验证项"明确转交用户，烧录后 probe 失败需补条目重编）
- 任一产物显式声明"未验证，需用户试烧" → **CONDITIONAL**（可进 GATE-交付 归档，但必须把"未验证项"明确转交用户，不能默写"完成"）

### ⚠️ 未验证项必须烧前解决（实测教训，P-显式未验证的执行约束）
"未验证"不是终点——是**待解决的信号**。实测案例：boot.medium 标了"未验证需试烧"，结果烧时候才炸（板子是 Nand 不是 Nor）。未验证项在烧录前必须尽量消解，不能原样带进烧录：
1. **能问用户的先问**：boot 介质、安全模式、DDR 变体后缀、归档路径等——这些用户知道，直接问（P-前置采集），别留"未验证"。DDR 变体确定后走 `ohos-dev-soc-spec-parse` 查对应 xlsm/DDR 参数
2. **能上网搜的自搜**：demo 板默认介质、芯片 flash 规格、烧录工具报错含义——联网检索（宿主 WebSearch 或等价物）查官方文档/参考仓；联网检索失败则向用户说明失败表现并问有无其他搜法（见 skill 知识检索降级链兜底），别凭记忆
3. **能机器查的机器查**：跨产物一致性、magic-byte、文件系统类型——GATE-B+ 一致性检查已覆盖
4. **只剩"必须上机才知道"的**（如 boot_image 格式最终被烧录工具接受、能否启动到 shell）→ 这类才能以"未验证，需用户试烧"带过，且必须显式转交用户

> 原则：未验证项要主动消解（问用户 / 上网搜 / 机器查），消解不了的才显式转交用户试烧。不准把"本可查到的"留作"未验证"去烧时候炸。

> 本门控是**自校验环节**：用户介入前，用机器可查的一致性 + 外部锚把能验的都验了，验不了的显式标出。用户报"不行"时（P-失败回填）：分类失败（格式/一致性/缺失/消费者不匹配）→ 回溯本表哪行本该抓住 → 补该行检查。

## Step 5: 候选产物登记（P4 收尾，不触发 GATE-交付）

> P4 仅登记 GATE-B/GATE-B+ 的候选产物，写入 `verification_manifest`：来源快照、实际命令、日志、路径、SHA256、消费者验收结果和未验证项。不得在此阶段询问归档路径、拉取/复制产物或执行经验回填。
>
> GATE-交付只可由编排器在 P6 完成后，或 P5/P6 已显式记录为 `SKIPPED_*` 后触发；届时才由用户决定归档路径及经验回填。

### 登记范围
- **可烧录镜像**：uImage（内核）+ rootfs.jffs2（rootfs）+ boot_image.bin/u-boot.bin（U-Boot）+ env.bin（U-Boot 环境变量）+ eMMC xml（分区布局）
- **XTS 测试二进制**：Acts*.bin（P5 产出，在 `suites/acts/testcases/*/` 子目录下）
- （可选）vmlinux/zImage/reg_info.bin（调试用）

### 流程
1. 为每个候选镜像记录路径、大小、SHA256、生成命令和构建日志到 `verification_manifest`。
2. 记录 GATE-B/GATE-B+ 状态、消费者验收锚和所有 `UNVERIFIED`/`CONDITIONAL` 项。
3. 同步候选产物规格到 `PROVENANCE`，供 P5/P6 及最终 GATE-交付消费。

> 候选产物留在构建工作区不代表交付完成；归档、下载和最终 Manifest 冻结由后续 GATE-交付执行。

### PROVENANCE 一致性校验（W5，候选登记前必做）
实测：PROVENANCE 滞后（仍记 jffs2/6 分区，实际已 ext4/4 分区），凭 PROVENANCE 复现会产出错误版本。候选登记前必须校验 PROVENANCE 记录的产物规格 == 实际 images/：
- [ ] PROVENANCE 记的文件系统类型 == 实际 rootfs 文件系统
- [ ] PROVENANCE 记的分区数/大小 == 实际 xml
- [ ] PROVENANCE 记的工具/版本 == 实际用的
- 每次修正（文件系统/分区/工具链）后必须**同步更新 PROVENANCE**，不能改了产出不改正本（这是 P-对抗自检的活案例：PROVENANCE 自证 jffs2，实际 ext4，自证 ≠ 真实）

### Agent Prompt 模板 (要点)

```
1. TASK:
   对 {chip_model} ({arch}) 的 OpenHarmony Lite 适配项目执行全量编译构建与验证。
   这是 GATE-B 门控所在阶段——编译不通过则后续 P5/P6 无法进行。
   已通过实测验证 (Hi3861V100/wifiiot, verdict: PASS).

2. 前置条件 (GATE-0):
   先执行 4 项环境健康检查 (hb/gn/components/toolchain), 全部 PASS 后才编译。
   参考: compiler_fix_playbook.md §1 (决策树) 和 §GATE-0。

3. 编译执行:
   - 标准: `./build.sh --product-name {product} --full`
   - Fallback (超时时): direct_build_cmd from workflow_config.yaml
   - 注意 ninja 参数: `-w dupbuild=warn` (OH 专用)
   - 注意: 可能产出多个独立二进制 (bootloader/app), 检查最后一个/主产物

4. 错误处理 (Compiler Fix Loop):
   - 先分类: workflow-gen vs GT vs framework
   - GT 修复: 按 compiler_fixbook §2 流程 (备份→最小改→diff→manifest→用户批准)
   - Framework 修复: 记录并请求批准
   - 实验: 用 experiment 格式记录, reverted 的标注清楚
   - 每轮全量重编 (不用增量!)

5. 产出:
   - GATE-0 报告 (4 子门控)
   - 编译结果 (exit code, error/warning count)
   - 固件清单 (所有 .bin/.elf, 含大小)
   - 大小分析报告
   - gt_patches_manifest (如有 GT 修改)
   - experiments 记录 (如有实验)

6. EXPECTED OUTCOMES:
   ① GATE-0 全 PASS (或 BLOCKED + 原因)
   ② GATE-V11: 编译零错误 (exit 0 + 主产物)
   ③ GATE-V12: 完整烧录包产出 + 大小/结构核验 (V11+V12 双 PASS 才签发 GATE-B PASS)
   ④ 所有修改已归档 (patches + experiments)
```

## MUST DO (实测血泪教训)

- [ ] **编译前必做 GATE-0** (4 子门控, ~50% 初次编译失败是环境问题)
- [ ] **★ GATE-0 0d-TC 一次性全扫工具链路径冲突**  — `grep -rnE "TC_DIR|/opt/[a-z_]+gcc" $OHROOT --include="*.sh" --include="*.mk" --include="*.gni" ...` 排除 .bak + /out/，所有路径指向 `toolchain.path`，不一致自决修正（技术执行），别让冲突跨阶段漏到 P2
- [ ] **★ P2/P3 接入新 build 脚本时补扫工具链路径** — kernel.mk / kernel_module_build.sh / sdk_linux BUILD.gn 等 P2/P3 才接入的文件，接入时跑全扫（不只 P1/P4）；kernel.mk 是 OH 仓共享文件按 KERNEL_ARCH 硬编码工具链，板级覆盖用环境变量/条件分支（最小侵入，不改默认分支影响其他板）
- [ ] **★ 遇决策先分级** (决策分级) — 业务决策（boot_image 缺失后是否终止 / 归档路径 / 经验回填开关）停转发用户；技术执行（defconfig / patch 适用性 / 工具链路径 / 构建路径当唯一可行 / Compiler Fix 策略）自决不转发
- [ ] **★ 门控分级** — 技术门控（GATE-0/V11/V12/B/B+）PASS 后自决过（展示清单作汇报不阻塞）；业务门控（GATE-交付 归档路径 / GATE-BURN 烧录模式 / GATE-HW 测试运行）必须停下等用户确认。完整规则见 `skills/ohos-dev-workflow-router/SKILL.md` §门控类型分级规则
- [ ] **★ 遇 GCC/clang 兼容问题先查 compiler_fix_playbook** — musl fortify/atomics/ld 选项/libunwind/C++ 接口等兼容问题，先查 `skills/ohos-dev-build-config/references/compiler_fix_playbook.md` §8（Hi3516CV610 L1-Linux）或 §1-7（Hi3861 L0）的 GT patch 复现 + Decision Tree，按表应用 L1-XX/XX-XX 修复，别从零重推导
- [ ] **★ OH 上游代码 bug 按优先级处理** — 非芯片特定 bug（接口签名/类型不匹配/编译警告等 OH 共享代码问题）按 ① 绕过依赖（组件不在 scope 移除）→ ② 最小 patch 绕过（stub/条件编译）→ ③ 修上游（最后）优先级处理；记 finding。完整指引见 `skills/ohos-dev-workflow-router/SKILL.md` §OH 上游代码 bug 处理指引
- [ ] **★ SPI Nand 颗粒 ID 覆盖验证**（板子用 SPI Nand 时必查）— **有硬件/烧录日志**：核查板子实际颗粒 ID 在内核 + U-Boot 的 fmc_ids 表里都有条目（`strings vmlinux | grep <颗粒ID>` + U-Boot 源码双查）；不在表里 → 烧前补条目重编。**无硬件/烧录日志**：标 ⚠️ 待烧录验证，不假设 vendor 表覆盖实际板子（实测同板 DS35Q1GB-IB 不在 vendor 表），烧录后 probe 失败（0x81）→ 加颗粒条目重编。不准默写"boot_image 已构建"而颗粒 ID 没查（P-显式未验证）
- [ ] **★ boot_image 大小与 references 标准核对**（GATE-B+ 硬检查，必查）— `stat` boot_image 大小 + `mkimage -l`/`hexdump` magic，与 references 标准值（hi3516cv610 debug = 227840B；其他芯片查 `compiler_fix_playbook` §8 / vendor SDK 标准）比对。偏离>5% → **FAIL**（构建流程错，不准标 PASS，不准烧录），查根因（prebuilt vs 源码标准编 / 未标 DEBUG=1 defconfig / reg_info 错 / gslboot_build 路径错）重编。实测教训：偏离 223K = 构建流程错，烧出 0x81
- [ ] **★ boot_image vendor 构建系统缺失时显式声明未构建**  — 不准默写"已构建"而实际没产出（P-显式未验证）；问用户提供 vendor 构建系统（业务决策停转发），用户不给则跳过并在 GATE-B+ 标"boot_image 未验证"
- [ ] **每个 BUILD.gn 的 sources 列表必须包含实际存在的文件**
- [ ] **linker.ld MEMORY 区域预留 +1~3% 余量** (跨 GCC 版本代码密度差异)
- [ ] **遇到编译错误先查 compiler_fix_playbook §2 Decision Tree** 再动手修
- [ ] **每轮修复后全量重编** (增量编译可能隐藏依赖问题)
- [ ] **记录所有 warning** (即使 exit 0, -Werror 可能下次阻断)
- [ ] **GT 修改必须: 备份 → 最小改动 → diff → manifest → 用户批准**
- [ ] **工具链目录 cp 前 always rm** (hard link 级联覆盖风险)
- [ ] **SDK 硬编码版本号需 grep -r 全局搜索** (usr.mk + scons_env_cfg.py + ...)
- [ ] **超过 3 轮修复卡同一错误 → stuck, 切入 P7**
- [ ] **LTO 对单体库危险** — 不要对 monolithic 启用 `-fwhole-program`
- [ ] **ninja 必须 `-w dupbuild=warn`** (OH 重复 NOTICE 规则)

## MUST NOT DO (实测血泪教训)

- ❌ 不要忽略 undefined reference (即使"只是个警告")
- **❌ 不要手动修改 out/ 目录下的生成文件** (改源码重编)
- ❌ 不要假设编译器标志 — 使用目标项目默认 toolchain flags
- ❌ 不要跳过 linker 验证 (编译通过 ≠ 链接通过)
- ❌ 不要在无错误时自行添加优化选项 (可能引入新问题)
- ❌ 不要用 `as any` / `@ts-ignore` / pragma 忽略 warning
- ❌ 不要一次性改多个不相关文件来"试试"
- ❌ 不要跳过用户批准就修改 GT 文件
- ❌ 不要忘记备份 GT 原始文件

## 附录：A/B/C 厂商依赖分类表（C8）

> 帮执行者判断每个产物"自己生成 / 用厂商 / 从 spec 派生"。来源：厂商依赖边界实测分析。
> **A** = 自己写但需厂商硬件规格做输入；**B** = 厂商预编译/预写直接用；**C** = 完全自己写不依赖厂商。

| 代码/产物 | 分类 | 说明 |
|---|---|---|
| 内核 defconfig | A | 需芯片硬件能力——走 `ohos-dev-soc-spec-parse` 提取（datasheet/SDK config 仅作回退） |
| 内核补丁 | B | 厂商写，直接 apply |
| DTS 设备树 | A | 需寄存器/中断/pin mux——走 `ohos-dev-soc-spec-parse` 提取（或补丁带入——B，须声明） |
| U-Boot 配置 | A | 需板级分区/启动设备从 spec 提取 |
| 驱动代码（HAL/HDF） | A | 需 SDK API 头；映射逻辑自己写，不抄厂商源码（见 ohos-dev-hal-skeleton-gen Step 1b） |
| SDK 预编译库（.so/.a） | B | 厂商编译，直接链接 |
| SDK 头文件（.h） | B | 厂商提供，include 用 |
| boot_image.bin | B | 厂商 image_tool 产出（含寄存器初始化表） |
| env.bin | A/B | mkenvimage 产出（B），env 配置从 spec 派生（A） |
| reg_info.bin | B | 厂商 xlsm_to_bin 产出。**xlsm 选哪个由 SoC 内置 DDR 变体决定——走 `ohos-dev-soc-spec-parse` 单点查询**（如 Hi3516CV610 -10B→DDR2 64MB QFN xlsm） |
| rootfs 目录结构 | C | 自己设计（标准 Linux 目录） |
| busybox | C | 开源，自己编译/获取 |
| init 脚本 | C | 自己写（标准 Linux init） |
| rootfs 里的 SDK .so | B | 厂商预编译，放入 rootfs/lib |
| 镜像打包脚本（mkimg） | C | 自己写（调标准 mkfs.ext4/jffs2/ubifs） |
| 分区布局（eMMC xml） | A | 需板级 flash 布局从 env blkdevparts 提取（或厂商 env2burn 工具——B） |
| OH 组件集成（BUILD.gn/config.json） | C | 自己写（OH 框架特定） |
| XTS 测试配置 | C | 自己写（OH 标准） |
| build.sh/Makefile 构建配置 | A | 需 arch/flash/内存布局从 spec 提取 |
| linker 脚本 | A | 需内存映射从 spec 提取 |
| 烧录工具（ToolPlatform/HiTool） | B | 厂商工具，直接用 |
| 安全签名工具/密钥 | B | 厂商提供 |
| 工具链 | B/C | 厂商提供或自己配 |
| 工作流/skill/方法论 | C | 完全独立 |

> **原则**：B 类优先用厂商现成的（M3 厂商工具发现原则，别重造轮子）；A 类自己写但必须从 spec/SDK 头提取输入，不能凭想象；C 类完全自己生成。**预编译库占位 ≠ 真实适配**（见 03-driver Step 3c L1 真实 HDF vs 占位）。
