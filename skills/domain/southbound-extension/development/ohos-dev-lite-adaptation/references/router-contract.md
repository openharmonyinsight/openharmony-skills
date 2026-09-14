---
name: ohos-dev-lite-adaptation
description: OpenHarmony Lite 芯片适配 7 阶段工作流编排器。Use when the user wants to start, resume, or advance the complete L0/L1 adaptation workflow; triggers include 开始移植、运行工作流、进入下一阶段、走完整个适配流程。阶段内的构建、测试或故障请求路由到对应专用 skill。
license: MIT
metadata:
  author: openharmony
  version: 0.1.0
  status: trial
  scope: domain
  stage: development
  domain: lite
  capability: adaptation
---

# OpenHarmony Lite SOC 适配工作流 — 编排器

## 概述

本文件是 **ohos-lite-adaptation 工作流的编排器**，定义 **7 个**执行阶段的**输入输出契约**、**路由规则**、**门控检查点**和**错误恢复策略**。

> **执行顺序原则**：编排器先于子技能编写。本文件定义"做什么"，各阶段的 SKILL 定义"怎么做"。
> **Agent 增强**：本编排器默认为单 Agent 顺序执行模型。如需 子代理 分发（提升 Context 管理、领域识别精度、审查独立性等质量维度，详见 `references/agent-dispatch-protocol.md`（Agent 调度设计完整版）），编排器从"路由器"升级为"调度器"。启用不改变本文件的阶段契约和路由规则，仅在执行层增加分发与合并能力。

---

## 阶段总览

```

┌─────────────────────────────────────────────────────────┐
│  Phase 1: 项目初始化与环境准备                            │
│  输入: 芯片型号/架构/RAM-Flash/目标系统(L0|L1)           │
│  输出: ./build.sh --product-name {product} 可执行的基准环境 + 项目骨架               │
│  门控: GATE-0 项目启动确认                                │
└──────────────────────┬──────────────────────────────────┘
                       │ ./build.sh --product-name {product} 能跑通基础产品
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Phase 2: 内核移植（完整）★ 核心阶段 ★                   │
│  输入: P1 产出的项目骨架 + 芯片内核规格                    │
│  输出: 内核可启动到 main() + C库可链接                     │
│  门控: GATE-K 内核基线确认                               │
└──────────────────────┬──────────────────────────────────┘
                       │ 内核可启动 + 构建体系完整
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Phase 3: 驱动开发与设备配置                              │
│  输入: P2 产出的内核基线 + 外设需求列表                    │
│  输出: 可编译的外设驱动 + HCS设备配置                      │
│  门控: GATE-D 驱动范围确认                                │
└──────────────────────┬──────────────────────────────────┘
                       │ 驱动代码 + 设备配置就绪
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Phase 4: 编译构建与验证                                  │
│  输入: P3 产出的完整代码                                 │
│  输出: 可烧录运行的固件 + 编译通过证明                     │
│  门控: GATE-B 编译通过确认 ⚠️ 关键门控                    │
└──────────────────────┬──────────────────────────────────┘
                       │ 固件可烧录运行
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Phase 5: 测试                                          │
│  输入: P4 产出的固件 + 驱动接口定义                       │
│  输出: 测试套件 + 编译报告 +（可选）硬件运行报告           │
│  门控: GATE-T 测试编译 / GATE-HW 硬件运行                  │
└──────────────────────┬──────────────────────────────────┘
                       │ GATE-T 通过；GATE-HW 可为 SKIPPED_NO_HARDWARE
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Phase 6: 文档与审查                                     │
│  输入: P1~P5 全部产出                                    │
│  输出: 适配文档 + 审查报告                               │
│  门控: GATE-R 审查签署                                   │
└──────────────────────┬──────────────────────────────────┘
                       │ 文档交付完成
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Phase 7: 问题诊断与修复 ← 逃生舱（任意阶段可切入）        │
│  输入: 错误现象/日志/现场状态                             │
│  输出: 根因定位 + 修复方案 + 回归断点                     │
│  门控: 无（诊断即服务）                                   │
└─────────────────────────────────────────────────────────┘
```

---

## 范围与未覆盖环节（显式声明，P-显式未验证）

P1-P7 当前只承诺 **L0/L1 首次芯片适配到可烧录镜像 + 测试编译产物**。L2/Linux 不在本流程的实现范围内；以下环节**当前未覆盖**，显式声明（不假装覆盖）：

所有验证结论必须引用同一份运行时 `verification_manifest`。Manifest 至少记录目标芯片/板卡、提交或源码快照、实际命令、工具链版本、产物 SHA256、日志路径、测试计数、硬件状态和时间戳；没有对应证据只能标记为 `UNVERIFIED`，不得写成 PASS。P4 创建构建与候选产物记录，P5 补充测试编译与硬件执行记录，P6 补充文档/审查及独立性状态；GATE-交付冻结最终版本并归档。P7 修复任一上游输入后，必须使受影响的后续记录、哈希和门控状态失效，重新执行后再更新 Manifest。

| 未覆盖环节 | 性质 | 备注 |
|---|---|---|
| **OTA / 固件升级** | 产品级功能 | A/B 分区、升级 agent、签名升级包——超出首次适配范围，需独立设计 |
| **量产工具链 / 烧录自动化** | 生产级 | 工厂烧录、批量配置、SN 烧写——超出开发适配 |
| **性能调优 / 功耗优化** | 优化阶段 | DVFS、深度睡眠、启动耗时——适配通过后再做 |
| **L2/Linux 标准系统适配** | 不同系统分支 | 需要独立的 Linux/HDF/镜像/测试流程，当前不由 P1-P7 承诺 |

> 遇到这些环节时，工作流应**显式声明"超出 P1-P7 范围"**并转交用户/单独迭代，不准默写"已处理"。

## 各阶段契约定义

### Phase 1: 项目初始化与环境准备 (`{{ASSET_ROOT}}/workflow/steps/01-env-prep`)

| 属性 | 定义 |
|------|------|
| **目标** | 搭建可执行 `./build.sh --product-name {product}` 的最小环境 |
| **输入** | `target.name`, `target.arch`, `target.ram_size`, `target.flash_size`, `target.system_type` (`mini`\|`small`；mini=L0 \| small=L1) |
| **产出** | ① `device/board/{vendor}/{board}/` 目录结构 ② `config.json` + `config.gni` 基准模板 ③ `./build.sh --product-name {product}` 可执行 ④ 芯片基础信息清单 |
| **引用的 tools/** | （无独立工具依赖） |
| **前置条件** | 用户已确定目标芯片和系统级别 |
| **后续消费** | P2 (内核移植), P3 (驱动开发) |

**子步骤**：
1. 目录规划：创建 Board/SoC 分离的 device 树结构
2. hb 工具链安装 + 源码同步 (`repo init/sync`)
3. config.json / config.gni 预编译适配（填入芯片基础参数）
4. `./build.sh --product-name {product}` 选定产品并跑通基础编译验证
5. 收集芯片基础信息（型号/架构/资源约束/外设列表初版）

**GATE-0 确认项**：
- [ ] 目标系统 L0/L1 确认正确？
- [ ] 芯片型号和架构匹配？
- [ ] `./build.sh --product-name {product}` 对基础产品能跑通？

---

### target profile 加载规则（P1 加载，P2/P3/P4 消费）

> target profile 是 per-target 结构化配置，存放在 `{{ASSET_ROOT}}/workflow/target-profiles/`（字段定义见该目录 `README.md`：`kernel_family` / `driver_model` / `device_description` / `build_integration` / `source_strategy` / `required_outputs`；L1 还含 `burn_package`——boot_chain.required_inputs + `BLOCKED_VENDOR_SDK` 策略 + required_artifacts）。02/03 阶段顶部已强制 "load a target profile from {{ASSET_ROOT}}/workflow/target-profiles/"，本节定义编排器侧的加载规则。profile 是路由数据不是通用规则——它选择芯片/系统特定的实现路线，不改变 P2/P3 阶段本身。

| 规则 | 内容 |
|------|------|
| **加载时点** | P1 信息收集阶段（Step 5）加载，把选定 profile 的**路径写入 `workflow_config.yaml` 的 `target.profile` 字段** + 选定值记录到 session manifest，**进入 P2 前必须完成**。P2/P3/P4 消费前校验 `target.profile` 与 session manifest 记录一致（不一致停下问）；三者消费同一份 profile（P4 启动链预检读 `burn_package`） |
| **加载位置与优先级** | `{{ASSET_ROOT}}/workflow/target-profiles/<target>-<kernel>-<level>.yaml`（如 `hi3516cv610-linux-l1.yaml`）。**用户配置优先于内置**——用户提供或确认的 target 专属配置优先；无用户配置才用内置 profile |
| **profile 与 L0/L1 的关系** | **profile 是数据源，L0/L1 标签是推导结论不是判定依据**。`target.system_type` 值域映射：mini=L0 轻量 / small=L1 小型（A2）。内核选型读 `kernel_family`、驱动框架读 `driver_model`、设备描述读 `device_description`，**均不从 mini/small 值域或 L0/L1 标签推断** |
| **新芯片无内置 profile** | P1 按芯片信息（chip-spec / 芯片规格提取）生成**草稿 profile**（必含 README 列出的必填字段），并在 `DECISIONS.md` 记录生成依据与字段来源。无 profile 不准进 P2 实现——README: "If no profile exists, the workflow must stop at profile selection and create one before implementation" |

---

### Phase 2: 内核移植（完整）(`{{ASSET_ROOT}}/workflow/steps/02-kernel-port`)

| 属性 | 定义 |
|------|------|
| **目标** | 内核可启动到 `main()`，C 库调用可链接 |
| **输入** | P1 产出的项目骨架 + 内核规格（中断控制器/时钟/内存映射） |
| **产出** | ① Kconfig 适配链（board→series→soc→defconfig） ② BUILD.gn 编译入口 ③ 启动代码（startup_S/system_init/向量表） ④ C 库适配（malloc wrap/printf） ⑤ linker.ld |
| **引用的 tools/** | `ohos-dev-kernel-source-query`（查询 Kconfig/BUILD.gn 样本）、`ohos-dev-soc-spec-parse`（提取寄存器/中断号） |
| **前置条件** | P1 完成（./build.sh --product-name {product} 基线可用） |
| **后续消费** | P3 (驱动开发, 需要 kernel HAL 接口)、P4 (构建验证) |

**子步骤**：

| 步骤 | 内容 | 新建/迁移自 |
|------|------|:-----------:|
| 2a | Kconfig 适配链（4级：board→series→soc→defconfig+组件裁剪） | 迁移: 07-kernel-trim + 新增 |
| 2b | BUILD.gn 编译入口（SoC级 + Board级） | 迁移: 05-build-config 部分 |
| 2c | **内核启动代码**（startup_S汇编入口/system_init C初始化/中断向量表/时钟UART基础HAL） | **新建** |
| 2d | **C库适配**（malloc_r/free_r --wrap / vprintf/snprintf/sprintf，L0必需L1可选） | **新建** |
| 2e | linker.ld 链接脚本（Flash/RAM布局/段定义） | 迁移: 05-build-config 部分 |

**GATE-K 确认项**：
- [ ] **Step 2pre 可行性报告 `kernel-choice-feasibility.md` 已产出？**（含 arch 检查 + SDK 独立性检查 + 方式 A/B 显式选择与理由。缺此文件 = GATE-K FAIL，不准进 Step 2a。见 `steps/02-kernel-port` §反短路规则）
- [ ] Kconfig 链完整？`./build.sh --product-name {product}` 能看到新 SoC？
- [ ] BUILD.gn 被 gn 构建系统发现？
- [ ] 启动代码能链接无 undefined symbol？
- [ ] linker.ld 地址范围正确（不超出 Flash/RAM）？
- [ ] **内核能否启动到 main()？**（最高优先级验证）
- [ ] **[来源完整性] 本阶段的 .c/.h 源文件是如何产生的？**
  - `generated`（由工作流从规格书/模板生成）→ 记录输入 spec + 使用的工具
  - `adapted_from_existing`（基于现有代码修改）→ 记录原始来源 + 改动范围
  - `manual`（手工编写）→ 记录依据
  - ⚠️ 如果所有源文件 SHA 与任何现有适配代码一致 → **触发目标漂移警报**

---

### Phase 3: 驱动开发与设备配置 (`{{ASSET_ROOT}}/workflow/steps/03-driver-device`)

| 属性 | 定义 |
|------|------|
| **目标** | 生成可编译的外设驱动代码 + HCS 设备树配置 |
| **输入** | P2 产出的内核基线 + 外设需求列表（来自用户或 P1 信息收集） |
| **产出** | ① profile 所选驱动/集成源码 ② profile 所选设备描述（HCS、DTS 或其他）③ BUILD.gn/构建集成声明 ④ （可选）RTOS→OH API 映射表 |
| **引用的 tools/** | `ohos-dev-soc-spec-parse`（提取寄存器/中断/时钟/引脚）、`ohos-dev-board-config-gen`（生成HCS/linker片段） |
| **前置条件** | P2 完成（内核基线可启动） |
| **后续消费** | P4 (构建验证, 全量编译含驱动) |

**子步骤**：

| 步骤 | 内容 | 性质 | 迁移自 |
|------|------|:----:|--------|
| 3a | 芯片规格提取（从DTS/SDK/手册提取寄存器/中断/时钟/引脚） | 使能活动（按需触发） | 02-chip-spec（缩减） |
| 3b | 外设驱动代码生成（GPIO/UART/I2C/SPI/PWM/...） | 核心 | 03-hal-driver |
| 3c | HCS 设备树配置 + 驱动绑定关系 | 核心 | 04-device-config |
| 3d | RTOS 驱动迁移（FreeRTOS/RT-Thread/Zephyr→OH，可选） | 可选子步骤 | 06-rtos-migration（降格） |

**GATE-D 确认项**：
- [ ] 需要哪些外设？（范围确认）
- [ ] 驱动框架是否与 target profile 一致，而非从 L0/L1 标签推断？
- [ ] HCS 配置与驱动代码匹配？
- [ ] **[来源完整性] 本阶段的驱动源码是如何产生的？**
  - `generated`（由 ohos-dev-soc-spec-parse + ohos-dev-board-config-gen 从规格书生成）→ 记录输入 datasheet + 工具
  - `adapted_from_existing`（基于现有驱动修改）→ 记录原始来源 + 改动范围
  - ⚠️ 如果驱动代码 SHA 与任何现有适配一致 → **触发目标漂移警报**
- [ ] **[工具链就绪] 驱动代码生成所需的工具是否可用？**
  - ohos-dev-soc-spec-parse 可执行？还是仅有方法论文档？
  - ohos-dev-board-config-gen 的 HCS 模板可用？
  - 如果不可用 → 明确标记为"手工模式"，禁止 silent fallback 到复制现有代码

---

### Phase 4: 编译构建与验证 (`{{ASSET_ROOT}}/workflow/steps/04-build-verify`)

| 属性 | 定义 |
|------|------|
| **目标** | 产出可烧录运行的固件 |
| **输入** | P1~P3 全部产出（完整代码） |
| **产出** | ① **GATE-0 环境健康报告** (4 子门控, 实测证明必需) ② `./build.sh --product-name {product}` 全量编译通过 ③ **可烧录固件包**（L0: 单 `.bin` 如 Hi3861_wifiiot_app_burn.bin / `.elf`；**L1 多产物结构**：boot_image + env + uImage + rootfs + eMMC xml 分区布局，非仅 uImage/vmlinux）④ 大小分析报告 ⑤ （可选）烧录到板子并基本运行验证 |
| **引用的 tools/** | `ohos-dev-build-config`（GN语法/错误诊断/config修复/编译修复知识库 `compiler_fix_playbook.md`）、`ohos-ci-lite-deploy-burn`（编译→下载→烧录→MAP 分析，烧录验证由此 skill 覆盖） |
| **前置条件** | P2 + P3 完成 |
| **后续消费** | P5 (测试, 需要固件)、P7 (诊断, 编译失败时切入) |

### 多产物结构（实测验证，MCU bootloader 常见模式）

> OH Lite wifiiot 产品产出 **多个独立二进制**，有独立链接步骤。

| 产物 | 典型大小 | 链接顺序 | 独立性 | 门控优先级 |
|------|---------|---------|--------:|:----------:|
| `*boot*.bin` | ~25KB | 第 1 个 | ✅ 完全独立 | Info |
| `*loader*.bin` | ~16KB | 第 2 个 | ✅ 完全独立 | Info |
| **主固件** (`*.out` / `.elf`) | **1~2MB ELF** | **最后** | ⚠️ 依赖前两者 ROM_TEXT | **🔴 Critical** |

**GATE-B 判定规则**：GATE-V11 只表示编译结果，GATE-V12 才表示所需产物结构/大小完整；两者均通过才可签发 GATE-B PASS。
- 主产物 PASS 但次要产物异常 → **GATE-V11 PASS，GATE-V12 FAIL/CONDITIONAL，GATE-B 不得 PASS**
- 主产物 FAIL → **GATE-V11 FAIL，GATE-B FAIL**
- 缺少用户明确允许跳过的非必需产物 → **CONDITIONAL**，必须进入 GATE-B+ 风险清单

> 配置启用: `workflow_config.yaml` → `gates.multi_output.enabled: true`

### 子步骤（实测校准后）

| 步骤 | 内容 | 新增? |
|------|------|:----:|
| **0. GATE-0** | 环境健康检查 (hb/gn/components/toolchain 4子门控) | ★ **新增 — 实测证明必需** |
| 1. GN 配置补全 + Linker 脚本最终化 | — |
| 2. `./build.sh --product-name {product}` 全量编译 (或 direct_build_cmd fallback) | — |
| **F. Compiler Fix Loop** | 错误分类 → Decision Tree → Patch/Experiment → 重编 | ★ **核心循环** |
| 3. 二进制大小分析 + Multi-Output 验证 | — |
| 4. （可选）烧录验证 | — |
| **4.5 L1 多产物构建** | uImage FIT 打包 + boot_image 构建 + env 生成 | ★ L1 必需 |

> **P4 Step 4.5 vendor 构建系统缺失指引（实测教训）**: P4 boot_image 构建假设用户给完整 vendor 构建系统，但 SDK 可能只含 soc（实测教训：服务端裸 SDK 无 osdrv/build/Makefile/gslboot → boot_image 硬阻塞）。**vendor 构建系统缺失时的处理**：
>
> 1. **显式声明 boot_image 无法构建**——写入 `DECISIONS.md` 缺口标记 + `workflow_config.yaml.gates` 未验证项，注明根因（vendor 构建系统不在 SDK 内）。
> 2. **向用户询问完整 vendor 构建系统的来源或访问授权**（用户提供 SDK 根目录/只读位置即可，P1 负责盘点是否含 `boards/dmeb/`、`gslboot_build/`、`u-boot/` 等部件）——不要求用户逐项列出或寻找文件，也不准默写"已构建 boot_image"。
> 3. **用户无 vendor 构建系统时的收尾**（三选一，问用户选哪个）：
>    - **跳过 boot_image**：GATE-V12 终止，GATE-B+ 显式标 boot_image"未验证"（缺失），其余产物（vmlinux/rootfs）正常验收。**实测选了这条**。
>    - **等用户补齐 vendor 构建系统后继续**：暂停 P4 Step 4.5，待用户提供后重跑。
>    - **终止适配**：boot_image 是必需产物且无法补齐 → GATE-V12 FAIL，转 P7 诊断或转交用户人工处理。
> 4. **env / uImage FIT 同理**：无 U-Boot 源码 → env 无法生成（标缺口）；uImage 只能打 legacy（实测教训：legacy 烧了必 reboot loop，必须 `mkimage -f linux_image.its uImage` 打 FIT，需 devicetree.dtb）。
>
> **实测教训回填**："SDK 不全必须问用户"——但工作流要明确"问完用户没有后怎么收尾"（核心：是终止还是跳过还是等）。本指引给出三选一收尾，不准撞墙后悬而不决。

### OH 上游代码 bug 处理指引（实测教训）

> P4 编译修复循环常撞 OH 仓上游代码 bug（非芯片特定）。实测案例：`surface_lite` C++ 基类 `Surface::SetUserData(const int&, const int&)` vs 子类 `SurfaceImpl::SetUserData(const std::string&, const std::string&)` 签名不匹配 → abstract class，GCC 12 严格检查暴露，clang 不报。此类 bug 不是 cv610 适配引入的，是 OH 上游共享代码本身的问题，处理不当会污染共享代码影响其他板。

**第一步：区分问题性质**

| 性质 | 判据 | 处理者 |
|------|------|--------|
| **芯片特定问题** | 只在该芯片工具链/架构/SDK 组合下触发，根因在芯片驱动/配置/工具链路径 | 适配者修（改 device/soc/ 或 device/board/ 范围内） |
| **OH 上游代码 bug** | 非芯片特定，任何用 GCC 严格检查/不同编译器/不同架构都可能触发，根因在 OH 共享代码（foundation/ drivers/ build/ third_party/ 等） | 按下方优先级处理 |

**第二步：OH 上游 bug 处理优先级（从低风险到高风险，优先选 ①）**

| 优先级 | 策略 | 适用场景 | 风险 |
|:------:|------|---------|------|
| ① | **绕过依赖**（移除该组件） | 该组件不在 scope（如标准集无 display → graphic 不需要）→ 从子系统配置/BUILD.gn 移除依赖 | 低，只动本板配置，不改共享代码 |
| ② | **最小 patch 绕过**（加 stub / 条件编译 / 去掉 override 关键字等） | 组件在 scope 必须用，但可局部绕过不改共享代码逻辑 | 中，patch 要最小化且打个性化标签，不改共享代码语义 |
| ③ | **修上游**（改 OH 共享代码逻辑） | ① ② 都不可行，必须修共享代码 | 高，改 OH 共享代码影响所有板，必须评估影响面 + 必要时问用户 |

**第三步：记 finding**

无论选哪个优先级，OH 上游 bug 必须记进 `PROVENANCE.md` 的 Findings 段：bug 详情（组件/文件/错误现象/根因）+ 处理方式（①/②/③ + 具体改动）+ 影响面评估，供后续 GATE-交付 评估是否回填上游 / 通报 OH 社区。

> **执行纪律**：不改 OH 上游共享代码逻辑除非必要（优先级 ③ 是最后选择）。优先级 ① ② 的改动必须限于本板 scope（子系统配置 / BUILD.gn 条件分支 / 本板 patch），不准把"绕过"写成"改共享代码逻辑"扩散到其他板。优先级 ③ 必要时按 §决策分级 + 术语大白话 转发用户（改共享代码是 trade-off，属业务决策）。

---

### Phase 5: 测试 (`{{ASSET_ROOT}}/workflow/steps/05-test-gen`)

| 属性 | 定义 |
|------|------|
| **目标** | 生成测试套件、完成测试编译，并在具备硬件时执行硬件运行测试 |
| **输入** | P4 产出的固件 + P3 定义的驱动 Method 接口 |
| **产出** | ① 测试框架初始化（HCTest/Unity） ② 单元测试用例 ③ 集成测试用例 ④ 测试编译报告 ⑤（可选）硬件运行报告 |
| **引用的 tools/** | `ohos-test-lite-ut-gen`（测试用例生成）+ `skills/ohos-test-lite-ut-gen/references/`（hctest-unity-guide / test-code-templates / test-framework-cheatsheet 等 API 与模板语料） |
| **前置条件** | P4 编译通过；P5-A 不依赖硬件，P5-B 需要用户确认和硬件条件 |
| **后续消费** | P6 (文档, 测试结果是交付物的一部分) |

**子步骤**：
1. 测试框架选择与初始化
2. 单元测试用例生成（基于驱动 Method 接口边界）
3. 集成测试（多外设协同场景）
4. GATE-T：测试编译与证据归档
5. GATE-HW：硬件在环测试（目标板实测，如有条件）

---

### Phase 6: 文档与审查 (`{{ASSET_ROOT}}/workflow/steps/06-doc-review`)

| 属性 | 定义 |
|------|------|
| **目标** | 产出适配文档 + 6类规则引擎/8维双视图代码审查报告 |
| **输入** | P1~P5 全部产出 |
| **产出** | ① 芯片适配手册 ② API参考文档 ③ 移植指南 ④ 代码审查报告（6类主分组 + 6类↔8维交叉矩阵双视图） |
| **引用的 tools/** | `ohos-design-ref-retrieval`（6a 文档，语料 `skills/ohos-design-ref-retrieval/references/`：doc-templates/terminology/bibliography）+ `ohos-dev-driver-review`（6b 审查，语料 `skills/ohos-dev-driver-review/references/`：review-rules/coding-standards/review-examples） |
| **前置条件** | P4 至少完成（文档可在并行开始） |
| **后续消费** | 最终交付 |

**子步骤**：

| 步骤 | 内容 | 迁移自 |
|------|------|--------|
| 6a | 适配文档生成（手册/API/移植指南） | 08-doc-gen |
| 6b | 代码审查 — `ohos-dev-driver-review` 按 FUNC/SEC/EMB/MAINT/STYLE/MISRA 六大类规则审查，产出 6类主分组 + 6类↔8维（正确性/安全性/规范性/性能/可测试性/可维护性/兼容性/文档）交叉矩阵双视图报告 | 10-code-review |

**审查规则引擎 6 大类**（`ohos-dev-driver-review` 规则引擎，主分组）：

| 类别 | 全称 | 重点 |
|------|------|------|
| FUNC | 功能正确性 | 功能逻辑、状态机、边界条件 |
| SEC | 安全性 | 缓冲区溢出、权限检查、注入风险 |
| EMB | 嵌入式约束 | 资源占用、中断安全、并发/原子性、栈/堆使用 |
| MAINT | 可维护性 | 模块耦合度、魔数消除、配置外置、可读性 |
| STYLE | 规范性 | 编码风格、命名、注释完整性 |
| MISRA | MISRA 合规 | MISRA C 强制/建议规则遵守 |

**报告 8 维度**（双视图交叉矩阵的维度轴）：

| 维度 | 级别 | 重点 |
|------|:----:|------|
| 正确性 | Critical | 功能逻辑、状态机、边界条件 |
| 安全性 | Critical | 缓冲区溢出、权限检查、注入风险 |
| 规范性 | Warning | 编码风格、命名、注释完整性 |
| 性能 | Warning | 内存占用、中断延迟、功耗 |
| 可测试性 | Info | Mock点、日志埋点、断言覆盖 |
| 可维护性 | Info | 模块耦合度、魔数消除、配置外置 |
| 兼容性 | Info | L0/L1差异处理、多版本API |
| 文档 | Info | API注释、README、示例代码 |

---

### Phase 7: 问题诊断与修复 (`{{ASSET_ROOT}}/workflow/steps/07-problem-diag`) ★ 逃生舱

| 属性 | 定义 |
|------|------|
| **目标** | 定位任何阶段的问题根因并提供修复方案 |
| **输入** | 错误现象描述 + 日志 + 现场状态 + 出错阶段 |
| **产出** | ① 根因定位 ② 修复方案 ③ 回归断点（返回哪个阶段继续） |
| **引用的 tools/** | `ohos-issue-lite-diagnose`（诊断，语料 `skills/ohos-issue-lite-diagnose/references/`：fault-knowledge-base/fault-cheatsheet/diagnostic-cases/log-acquisition-guide/debug-tools-guide 知识库） |
| **前置条件** | 任何阶段遇到无法解决的问题时切入 |
| **后续消费** | 返回出错阶段继续（回归断点） |

**特殊性质**：Phase 7 不是顺序流程中的一步，而是**任意阶段的逃生舱**。当 P1~P6 中任何一步遇到阻塞时，路由器自动切入 P7，修复后返回原断点。P7 必须记录 `return_phase`、`return_step` 和 `same_error_rounds`，否则不得标记为可恢复。

---

## 路由规则

```
function route(user_input, current_phase, progress, workflow_config):
    # R1: 显式指定
    if user_input.specifies_target_phase:
        return user_input.target_phase

    # R2: 错误/问题 → 切入逃生舱
    if user_input.is_error_or_problem or current_phase.stuck:
        return PHASE_7_DIAGNOSE

    # R3-R10: 顺序推进（拓扑序）；verify-only 只执行 P4
    mode = workflow_config.workflow.mode
    if not progress.exists and mode != "verify-only":
        return PHASE_1_INIT
    phases = [P4] if mode == "verify-only" else [P1, P2, P3, P4, P5, P6]
    for phase in phases:
        state = progress.phases[phase]
        phase_key = {P1: "p1_env_prep", P2: "p2_kernel_port", P3: "p3_driver_device", P4: "p4_build_verify", P5: "p5_test_gen", P6: "p6_doc_review"}[phase]
        if state in [COMPLETED, SKIPPED_USER, SKIPPED_MODE, CONDITIONAL_DELIVERY]:
            continue  # CONDITIONAL_DELIVERY 是条件终态：风险已冻结进入条件性交付，重入不再回 P6
        if state == GATE_REVIEW:
            sd = progress.phases[phase]
            # 优先级 1：未关闭 Critical 最高——显式跳过/独立性未验证都不得清除，一律回炉
            # （条件性交付不得掩盖真实审查失败）
            if not sd.criticals_closed:
                progress.phases[phase] = IN_PROGRESS
                return phase
            # 优先级 2：用户显式跳过审查（Critical 已关闭才允许）——按契约记录风险进入跳过终态，
            # 由 GATE-交付 条件性签发；不再被 gate_passed=False 挡在回炉分支
            if user_input.explicitly_skips_review:
                progress.phases[phase] = SKIPPED_USER
                progress.phases[phase].skip_reason = "user_requested_at_gate"
                verification_manifest.record_skipped(phase, "user_requested_at_gate", risk="review evidence absent")
                continue
            # 优先级 3：唯一缺口 = 审查独立性（产出齐全 + Critical 已关闭 + 仅独立性未验证）
            # → 冻结风险清单进入条件终态（不回 P6 重做；FAIL 才回炉）
            if sd.independence_status == "UNVERIFIED_INDEPENDENCE" and sd.work_complete:
                progress.phases[phase] = CONDITIONAL_DELIVERY
                progress.phases[phase].risk_note = "independence unverified; risk list frozen"
                verification_manifest.record_conditional(phase, "independence_unverified", risk="review independence unverified")
                continue
            # 优先级 4：其余门控未过（含独立性已验证但 gate 仍未过）→ 回炉
            if not sd.gate_passed:
                progress.phases[phase] = IN_PROGRESS
                return phase
            progress.phases[phase] = COMPLETED
            continue
        if not workflow_config.phases[phase_key].enabled:
            progress.phases[phase] = SKIPPED_USER
            progress.phases[phase].skip_reason = "config_disabled"
            verification_manifest.record_skipped(phase, "config_disabled", risk="phase evidence absent")
            continue
        if phase in [P5, P6] and mode == "quick-prototype":
            progress.phases[phase] = SKIPPED_MODE
            progress.phases[phase].skip_reason = "quick-prototype"
            verification_manifest.record_skipped(phase, "quick-prototype", risk="test/review evidence absent")
            continue
        if phase == P5 and user_input.explicitly_skips_tests:
            progress.phases[phase] = SKIPPED_USER
            progress.phases[phase].skip_reason = "user_requested"
            verification_manifest.record_skipped(phase, "user_requested", risk="test evidence absent")
            continue
        if phase == P6 and user_input.explicitly_skips_review:
            progress.phases[phase] = SKIPPED_USER
            progress.phases[phase].skip_reason = "user_requested"
            verification_manifest.record_skipped(phase, "user_requested", risk="documentation/review evidence absent")
            continue
        return phase

    # R11: 全部完成
    return COMPLETION_REPORT
```


> **UNVERIFIED_INDEPENDENCE 终态处理**：宿主不支持隔离会话时，P6 完成文档与审查后记录
> `UNVERIFIED_INDEPENDENCE`，此时**不再回退 P6 重做**——直接标记
> `CONDITIONAL_DELIVERY`（条件性交付）：工作已完成但独立性受限，风险清单已冻结，
> 进入 GATE-交付 的条件性签发流程（CONDITIONAL 而非 PASS）。
> 与 FAIL（工作未完成，需修复后重做）严格区分。
> 路由已实现该转移，GATE_REVIEW 态按优先级处理：① 未关闭 Critical → 一律回炉（显式跳过/独立性未验证都不得清除）；② 用户显式跳过审查（Critical 已关闭）→ SKIPPED_USER，按契约记录风险，GATE-交付 条件性签发；③ 唯一缺口为审查独立性（产出齐全 + Critical 已关闭）→ CONDITIONAL_DELIVERY；④ 其余门控未过 → 回炉。终态列表同样识别 CONDITIONAL_DELIVERY，再次调用不再落回 `return phase`。

### 可选阶段判断

| 阶段 | 默认行为 | 跳过条件 |
|------|---------|---------|
| P5 测试 | 执行 | 用户明确跳过；无硬件只允许跳过 P5-B 硬件运行，不得跳过 P5-A 测试编译 |
| P6 文档 | 执行 | 用户明确跳过 / 仅做原型验证 |
| P3d RTOS迁移 | 跳过 | 用户无现有RTOS驱动可迁移 |

---

## 门控检查点

| 门控 | 位置 | 确认内容 | 风险 | 门控类型 | 必须暂停? |
|------|------|---------|:----:|:--------:|:-------:|
| **GATE-0** | P1 之后 (P4 Step 0 复检) | 芯片/系统/版本/./build.sh --product-name {product}基线 + **4 子门控** (hb模块/gn/components/toolchain) + **SDK 完整性核查** + **工具链路径全扫** | 🔴 高 | 技术 | PASS 后自决过 |
| **GATE-K** | P2 之后 | **Step 2pre 可行性报告 `kernel-choice-feasibility.md` 已产出**（arch+SDK 独立性+方式 A/B 选择）+ 内核可启动到main()? + **(L1) DTS 来源声明**（generated from spec / patched from 补丁，须显式） | 🔴 高 | 技术 | PASS 后自决过 |
| **GATE-D** | P3 之后 | 驱动范围/HCS匹配 | 🟡 中 | 技术 | PASS 后自决过 |
| **GATE-B** | P4 之后 | **./build.sh --product-name {product}零错误通过 + 完整可烧录包产出**（L0: 单 .bin 如 Hi3861_wifiiot_app_burn.bin；L1: uImage + rootfs + boot_image + eMMC xml 分区布局，非仅 uImage/vmlinux）(主产物为 Critical 判定)。**P4 内部细分为 GATE-V11（编译通过）+ GATE-V12（多产物大小/结构验证）两级子门控**——详见 `steps/04-build-verify/SKILL.md` | 🔴 高 | 技术 | PASS 后自决过 |
| **GATE-B+** | P4 烧录包产出后 | **烧录包消费者验收（自校验）**：每个产物标识消费者 + 给出接受性外部锚（厂商工具产出/magic-byte/跨产物一致性/用户试烧），机器可查的一致性必跑；无锚则显式声明"未验证"，不准默写"完成" | 🔴 高 | 技术 | PASS 后自决过 |
| **GATE-BURN** | P4 烧录 | 烧录操作（按目标 L0/L1 选择 HiBurn、HiTool 或厂商 ToolPlatform）需用户确认模式后执行；无硬件条件跳过并记录 | 🔴 高 | 业务 | ✅ 是 |
| **GATE-T** | P5-A 之后 | 测试源码/二进制已编译，命令、产物、数量和日志已归档 | 🔴 高 | 技术 | PASS 后自决过 |
| **GATE-HW** | P5-B 硬件运行 | 烧录、串口、HIL/XTS 运行需用户确认；无硬件可标记 `SKIPPED_NO_HARDWARE` | 🔴 高 | 业务 | ✅ 是 |
| **GATE-交付** | P6 完成后，或 P5/P6 已显式跳过后 | **问用户输出件归档到哪个本地路径 + 拉取完成**（镜像 + 已编译测试产物，不能只留服务端/testcases 仓）+ **经验回填环节**（manual 模式问用户是否回填本次适配教训，auto 自动回填，off 跳过）。当 P5/P6 为 `SKIPPED_*`、硬件为 `SKIPPED_NO_HARDWARE` 或审查独立性为 `UNVERIFIED_INDEPENDENCE` 时，只能给出 `CONDITIONAL` 交付，Manifest 必须列明缺失证据和风险。**ad-hoc / 工作流外构建同样适用**：任何产出件下载前必问归档路径，不得自定 | 🔴 高 | 业务 | ✅ 是 |
| **GATE-R** | P6 之后 | 文档与独立代码审查均产出；Critical 发现已关闭；完成交叉核对和签署。`UNVERIFIED_INDEPENDENCE` 时不得 PASS，只能随最终交付标为 `CONDITIONAL` | 🔴 高 | 技术 | PASS 后自决过 |

> **门控类型分级规则（实测教训）**：门控分两类，"必须暂停"列按类型取值，不再一刀切"必须停"。
>
 > - **技术门控**（GATE-0 / GATE-K / GATE-D / GATE-B / GATE-B+ / GATE-T / GATE-R 等纯构建、测试编译、审查结果门控）：证据清单全 PASS + 来源完整性核查 PASS → **执行者自决推进**，展示确认清单作汇报用但不阻塞、不等用户确认；任一 FAIL → 停下修；遇来源完整性警报（目标漂移）→ 停转发。
> - **业务门控**（GATE-交付 归档路径 / GATE-BURN 烧录模式 / GATE-HW 测试运行 / 经验回填开关 / trade-off / 需用户拍板）：**必须停下展示清单等用户确认，不自决**。
>
> **判定口诀**：遇门控 PASS 准备推进时先问自己——"这是真的应该由用户决定的问题吗？"——是（业务门控）→ 停转发等明确答复；否（技术门控 PASS）→ 自决过。与 §决策分级 + 术语大白话 的问用户与自决平衡精神一致：技术门控 PASS = 技术执行验证通过，自决推进符合技术自决；业务门控涉及用户资产（归档路径/硬件/教训回填），停下转发符合问用户。

### 门控参数消费契约

宿主适配器在执行门控时 MUST 从 `workflow_config.yaml.gates` 读取阈值和校验开关；这些字段不是装饰性元数据。**字段分两类，消费者不同，不得混用**：

```python
def evaluate_gate(metrics, config):
    gates = config["gates"]
    # ── 构建门控（GATE-V12 / GATE-B）：产物结构类 ──
    if metrics.system_level == "L1" and gates["validation"]["small_requires_multi_output"]:
        require(gates["multi_output"]["enabled"])   # L1 多产物结构强制
    require(metrics.evidence_present if gates["validation"]["evidence_required_for_pass"] else True)
        # 证据开关：所有技术门控通用——evidence_present 对应 verification_manifest 有记录

def evaluate_quality(metrics, config):
    # ── 质量评估（GATE-交付 前的 Round-Trip 质量判定）：覆盖率类 ──
    # l1~l4 为 Round-Trip 验证级别指标（L1 结构层/L2 符号层/L3 功能层/L4 泛化层），
    # 不是编译门控指标——只在 GATE-交付 前的整体质量判定中消费
    gates = config["gates"]
    require(metrics.l1 >= gates["l1_pass_threshold"])
    require(metrics.l2 >= gates["l2_pass_threshold"])
    require(metrics.l3 >= gates["l3_pass_threshold"])
    require(metrics.l4 >= gates["l4_pass_threshold"])
    require(abs(metrics.firmware_deviation) <= gates["l5_firmware_deviation"])
```

`convergence_rounds`、`cross_target_count` 和 `rom_overflow_strategy` 分别由收敛判定、泛化判定和 ROM 溢出分支消费；未实现对应消费者时，宿主必须将该项标记为 `UNSUPPORTED_CONFIG` 并阻止签发 PASS。

> **GATE-0 扩展说明（实测校准）**: GATE-0 原定义在 P1 之后做一次性环境检查。实测证明 **编译前必须复检**——P1→P4 之间环境可能变化（hb 损坏、工具链被替换等）。P4 Step 0 的 GATE-0 是 **正式编译前的最终健康检查**，含 4 个子门控。详见 `steps/04-build-verify/SKILL.md` §Step 0。

> **GATE-0 4d 工具链子门控——一次性全扫所有 build 脚本（实测教训）**: 工具链路径校验不能只查 config.gni + sdk_linux/build.sh 两处（实测教训：P1 查改了这两处，P2 又发现 kernel.mk L76 TC_DIR 同样指向错误路径，跨阶段漏到 P2 才补）。**P1 GATE-0 + P4 GATE-0 复检都执行一次性全扫**：
>
> ```bash
> # 全扫所有含 TC_DIR / 工具链路径的 build 脚本（排除 .bak + /out/）
> grep -rnE "TC_DIR|toolchain.*path|openeuler_gcc|cv610_tc" "$OHROOT" \
>   --include="*.sh" --include="*.mk" --include="*.gni" --include="*.gn" \
>   --include="*.py" --include="Makefile*" \
>   --exclude-dir=out --exclude="*.bak*"
> ```
>
> 必扫文件清单（不只这 4 个，凡 grep 命中的都查）：`config.gni`（board + soc + sdk_linux 各一份）/ `sdk_linux/build.sh` / `kernel/linux/build/kernel.mk` / `build/ohos/kernel/kernel.gni` / 任何含 `TC_DIR` 或工具链路径的文件。所有命中的 TC_DIR / 工具链路径必须**相互一致**且**指向已验证可用的工具链 bin**（briefing 提供的路径为准，已验证 GCC 版本）。路径冲突 = GATE-0 FAIL，必须一次性全修，不准跨阶段漏。

> **GATE-0 SDK 完整性核查（实测教训）**: P1 Step 0 / GATE-0 必须核查 SDK 是否含构建所需的全部部件，不全则**显式声明缺口 + 问用户**，不准默写"SDK 完整"。
>
> L1 多产物构建（boot_image + env + uImage + rootfs）所需 SDK 部件清单：
>
> | 部件 | 用途 | 典型路径 | 缺失影响 |
> |------|------|---------|---------|
> | `osdrv/` | boot_image / U-Boot 构建 | SDK 根 `osdrv/` 或 OH 仓 `device/soc/{vendor}/{chip}/osdrv/` | boot_image 无法构建 |
> | `U-Boot/` 或 `u-boot/` | U-Boot 源码 → env 分区 + uImage FIT 打包 | SDK `osdrv/uboot/` 或独立 | env 无法生成 + uImage 只能打 legacy（实测教训：legacy uImage 烧了必 reboot loop） |
> | `gslboot_build/` 或等价 | boot_image 构建（海思 gslboot 模式） | SDK `osdrv/tools/pc/gslboot_build/` | boot_image 无法构建 |
> | `.xlsm` | 板级 DDR 变体配置（含变体后缀，决定 DMEB demo 板型号） | 参考仓 `boards/dmeb/*.xlsm`（不在 SDK——自查撞墙点） | 无法确认 DDR 变体（D2） |
> | `sdk_linux/` | OH 仓标准构建（BUILD.gn + build.sh + config.gni + drv + include） | OH 仓 `device/soc/{vendor}/{chip}/sdk_linux/` | 标准构建走不通（但服务端裸 SDK 缺失不阻塞——OH 仓自有 sdk_linux 即可） |
>
> **核查动作**：① SSH 上服务端 / 本地 ls SDK 根 + OH 仓 device/soc/ 列上述部件是否存在；② 对照 `workflow_config.yaml.target` + briefing 提供的工具链路径确认部件路径一致；③ 缺失部件**显式声明缺口**（在 `DECISIONS.md` 记缺口标记 + `workflow_config.yaml.gates` 缺口标记），问用户："SDK 缺 {部件}，{影响}。请提供完整 vendor 构建系统 / 跳过该产物并在 GATE-B+ 标未验证 / 等待补齐"——不准默写"SDK 完整"或默写"已构建"。

> **P1 SDK 输入职责与问询规则**：用户只负责提供 vendor SDK 根目录或经授权的只读位置，并确认目标芯片/板型/启动介质。默认交付物是完整可烧录镜像；仅当用户明确要求缩小范围或指定烧录格式时才就此询问。其余全部由 P1 负责：盘点所给根目录，把每个候选件分类为源码 / 构建系统输入 / 板级约束 / 工具链 / 二进制 / 仅参考材料；核对锁定的 OH 树；产出带哈希与溯源的最小 allowlist R2 交接清单。不得问用户"要不要提供某个单独文件"（如内核 Makefile 或 U-Boot 环境模板）。

**L1 镜像路径硬门控**：P1 在选定或交接 greenfield 策略前，必须单独分类 vendor 启动链输入：GSL/DDR 初始化、DDR/寄存器或 `reg_info` 参数、U-Boot 或等价的 boot-image 生成器、以及确切的构建/打包命令。greenfield/manual 模式只授权编写 OH 集成代码，不解锁本门控、不允许发明 vendor 启动二进制。这些输入未就位、或未被显式授权用于可评审的启动链实现时，P1 必须把镜像路径置为 `BLOCKED_VENDOR_SDK` 并停止默认的完整镜像交付路径。内核/rootfs 工作只能作为显式记录的"非交付诊断"继续，不得被包装或描述为"部分烧录包"。P4 不得把该阻塞当作新发现重新触发。

> **公开资料检索优先**：在把某能力判定为"私有 SDK 缺口"之前，P1 必须先检索本仓检索策略允许的公开源：官方芯片文档、公开的 vendor/OpenHarmony 仓、官方工具文档、上游源码历史。公开发现记录 URL、修订/日期、许可/访问状态，落盘时记 SHA256。只向用户询问非公开的事实或产物：SDK/BSP 访问途径、公开渠道拿不到的板级 DDR/flash/安全启动信息、受限制的二进制/密钥/许可、硬件可用性、交付选择。禁止用公开检索结果推断私有板级事实；在用户提供或实测观察前一律标 `UNVERIFIED`。
>
> 若某组件不在精选交接清单（curated handoff）里，P1 必须先判断它是否存在于被授权的完整 SDK 或锁定的 OH 树中、能否安全落盘。仅当以下三种情况才问用户：(a) 完整 SDK/OH 树也缺该组件；(b) 因许可/安全/防引用约束无法转移；(c) 实现策略的选择会改变交付物或风险。提问必须点名缺失的能力和影响，不得预设一个猜测的文件名。答案记入 `DECISIONS.md` 和 `workflow_config.yaml.gates`；未选定的策略是 `FAIL_REQUIRES_USER_DECISION`，不是 `INPUT_READY`。
>
> 部分 vendor SDK 是证据，不证明其孤立文件已足够。特别是：vendor 内核 Makefile 或板级环境模板可以确立内核/存储/分区/启动约束，但不能证明 OpenHarmony `device/soc/.../sdk_linux` 存在。P1 必须把这类文件标为 `constraint_only`，直到其传递构建依赖与消费者都在场。

> **门控交互模式**：到达每个门控时，Agent 必须**展示确认清单**作为阶段汇报。是否停下等用户确认按 §门控类型分级规则（实测教训）执行：技术门控 PASS 后自决推进（展示清单作汇报但不阻塞）；业务门控必须停下等用户逐项确认后才进入下一阶段。不允许自动跳过门控（技术门控也要先展示清单再自决过，不准默写"已通过"不汇报）。

### 经验回填环节（GATE-交付 后置，用户可控开关）

> 本环节受 `workflow_config.yaml.experience.accumulation` 控制，决定本次适配的根因/教训是否回填到工作流正文/语料。**默认 manual 模式不回填**——GATE-交付 时问用户是否回填 + 回填哪些，用户不主动说 yes 就不回填。

**三种模式**（`workflow_config.yaml.experience.accumulation`）：

| 模式 | 行为 | 适用场景 |
|------|------|---------|
| `manual`（默认） | GATE-交付 时停下问用户："本次适配有哪些值得回填的教训？要回填哪些？" 用户明确说 yes 才回填，不主动回填 | 默认模式。真实用户首次适配，避免污染通用工作流 |
| `auto` | 自动回填所有定位到的根因/教训到对应 step SKILL.md / references/ | 调试追踪项目（多轮验证场景），主动积累教训 |
| `off` | 不回填，跳过本环节 | 一次性原型 / 用户明确不想污染工作流 |

**回填范围**（`workflow_config.yaml.experience.scope`，默认 `[cases, fault-kb, methods]`）：

| 范围标签 | 回填目标 | 内容 |
|---------|---------|------|
| `cases` | `skills/ohos-issue-lite-diagnose/references/diagnostic-cases.md` | 诊断案例（错误现象→根因→修复→验证） |
| `fault-kb` | `skills/ohos-issue-lite-diagnose/references/fault-knowledge-base.md` | 故障知识库条目（错误码/寄存器值→根因映射） |
| `methods` | 对应 step 的 `SKILL.md` 方法节 | 正文方法（如 GATE-0 加工具链全扫、GATE-B+ 加消费者验收） |

**个性化标签**（`workflow_config.yaml.experience.personalize_tag: true` 默认开启）：回填时在每条教训末尾打 `（来源：{chip} @ {iter}, {date}）`，区分通用教训 vs 个性化教训（特定芯片/特定迭代）。

> **回填纪律**：manual 模式下用户说 yes 才回填，说 no 就不回填（不准"我觉得有用就回填"）。auto 模式回填也要打个性化标签，避免通用工作流被特定芯片教训污染。回填动作本身在 P6 文档审查之后、GATE-交付 收尾前完成。

### P-原则总览

本工作流遵循 5 条贯穿性原则，集中定义如下（各原则在 01/02/03/04/07 step 落地处有内联引用）：

| 原则 | 一句话定义 |
|------|-----------|
| **P-前置采集** | 能提前定的决策（boot.medium / SDK 完整性 / DDR 变体 / 版本号 / 子系统选配等）在工作流开始时批量采集落盘到 `DECISIONS.md` / `workflow_config.yaml`，不留到门控处临时问（落地：`01-env-prep` Step 0a/0b）。**版本号规则默认 `{chip}_{date}`**（不含 iter——iter 是多轮调试追踪项目才加的后缀，真实用户首次适配没有 iter 概念；实测教训：默认带 {iter} 是过拟合多轮调试实践回填的）。多轮调试时用户自加 iter 后缀（如 `{chip}_{date}_iterN`），不作为默认。 |
| **P-显式未验证** | 不准默写"已生成/已通过"而实际依赖补丁或未实测——来源/验证状态必须显式声明，未验证项必须烧前解决（落地：`04-build-verify` GATE-B+ 消费者验收、`02-kernel-port` GATE-K 来源完整性）。 |
| **P-对抗自检** | 产出者自证 ≠ 真实（如 PROVENANCE 自证 jffs2 实际 ext4），自校验环节须对抗式复核，不信任单方声明（落地：`04-build-verify` GATE-B+ magic-byte / 跨产物一致性）。 |
| **P-消费验收** | 每个产出件有明确消费者验收：烧录包消费者自校验、`GATE-交付` 归档路径硬约束（ad-hoc / 工作流外构建同样适用，下载前必问归档路径）（落地：`04-build-verify` GATE-B+、`05-test-gen` GATE-交付）。 |
| **P-失败回填** | 定位到的根因 / 教训回填到正文方法（A 类，写入对应 step 的 SKILL.md 方法节）或 `references/` 语料（B 类，写入对应 skill 的 references/），不只修当前问题（落地：`07-problem-diag` 根因回填、历次回填批次见 `references/agent-dispatch-protocol.md` 附：编排器版本记录）。**用户可控开关**：回填行为受 `workflow_config.yaml.experience.accumulation` 控制（`manual` 默认不回填 / `auto` 自动回填 / `off` 不回填），manual 模式 GATE-交付 时问用户是否回填 + 回填哪些，用户不主动说 yes 就不回填（详见 §经验回填环节）。回填时打个性化标签 `（来源：芯片 @ iter, 日期）` 区分通用 vs 个性化教训。 |

---

## 错误恢复策略

| 错误类型 | 触发阶段 | 恢复策略 | 返回点 |
|---------|---------|---------|--------|
| 知识检索失败 | 任意 | 降级链：知识检索工具 → 本地 references/ → 联网搜索 → 询问用户 | 当前阶段 |
| 子技能产出不符预期 | 任意 | 回退到上一门控 → 调整参数 → 重试 | 上一门控 |
| **编译/链接错误** | P4 | **Compiler Fix Loop** (P4 Step F): 错误分类(GT/framework/gen) → Decision Tree → Patch/Experiment → 全量重编 → 循环直到通过。3 轮卡同一错误 → stuck, 切入 P7。详见 `steps/04-build-verify/SKILL.md` §Step F + `compiler_fix_playbook.md` §2 | P4 断点 |
| **内核启动失败** | P2 GATE-K | **切入 Phase 7 诊断** → 分析启动日志 → 修复启动代码/C库/linker | P2 断点 |
| **驱动加载失败** | P3/P4 | **切入 Phase 7 诊断** → 检查HCS绑定/注册函数/中断配置 | P3/P4 断点 |
| HardFault / 异常 | P4 烧录后 | **切入 Phase 7 诊断** → 分析Fault寄存器/栈回溯 → 定位非法访问 | P4 断点 |
| 环境损坏（hb不可用） | P1 | 回退到 P1 Step 2 → 重新安装工具链/重新sync源码 | P1 Step 2 |

---

## Agent 调度协议（子代理 Dispatch）— 摘要

> **本节是调度协议的摘要。** 完整协议（调度模式总览 / 阶段 Agent 分发表 / 上下文打包协议 / 子代理产出格式 / 并行组定义 / 派发伪代码 / should_dispatch / Prompt 模板结构）下沉在 `references/agent-dispatch-protocol.md`。
>
> **读取条件（Progressive Disclosure）**：单 Agent 模式（`workflow_config.yaml.workflow.dispatch_mode: single`，默认）**不读取**该文件——编排器仍按「路由规则」顺序执行各阶段，本节仅作模式判定。当 `workflow.dispatch_mode` 为 `enabled` 或 `required` 时，编排器从路由器切换为调度器模式，**MUST READ `references/agent-dispatch-protocol.md` 全文**后再执行派发。`DECISIONS.md` 仅供人类对账。调度协议的 `task()` category 等机制未实证——启用调度前先完成单 Agent 模式验证。
>
> **决策变量 A1-A6 映射**（运行时由宿主适配器从结构化配置显式映射，不解析 Markdown；`DECISIONS.md` 是人类可读的 A1-A7 决策记录，用于对账。缺失映射必须报错或使用下列声明过的默认值）：
>
> **`DECISIONS.md` 与 `workflow_config.yaml` 职责分工**（互补不互替）：
> - **`DECISIONS.md`** 记录 A1-A7 决策及理由，供人类审核和宿主适配器对账。
> - **`workflow_config.yaml`** 装结构化配置（`target.*` / `workflow.*` / `intake.*` / `phases.*` / `experience.*`），各 step 按需读取，用户填 `{{ASSET_ROOT}}/workflow/workflow_config.template.yaml` 可触发跳过询问。
> - 两者均由 `01-env-prep` Step 0 产出：决策记录 → `DECISIONS.md`，结构化配置 → `workflow_config.yaml`。编排器由宿主适配器读取结构化配置；阶段内详细配置由各 step 自行从 `workflow_config.yaml` 取。
>
> | 变量 | 结构化来源与含义 | 取值 | 默认（结构化字段缺失时） |
> |------|------|------|---------------------------|
> | **A1** | `workflow.mode`：完整 7 阶段 / 仅 P4 编译验证 / 快速原型跳过 P5-P6 | `full` / `verify-only` / `quick-prototype` | `full` |
> | **A2** | `target.system_type` + `target.arch` + `target.product_type`：决定 P2/P3/P4 行为分支 | `mini` / `small`（映射 L0 / L1） | 用户输入必填（无默认） |
> | **A3** | `phases.*.enabled`：P5 测试 / P6 文档+审查 / P3d RTOS 迁移是否跳过 | 每阶段 `true` / `false` | P5 `true` / P6 `true` / P3d `false` |
> | **A4** | `phases.p2_kernel_port.trim_components`：已并入 P2 Step 2a 的内核裁剪项 | 已核实的组件列表 | `[]` |
> | **A5** | `workflow.dispatch_mode`：是否启用子代理调度 | `single` / `enabled` / `required` | `single` |
> | **A6** | `workflow.p7_escalation`：P7 按错误上下文选择常规或重度推理 | `auto` | `auto`（HardFault/启动挂起/间歇性失败用 `ultrabrain`，其余用 `unspecified-high`） |
>
> 另有 **A7** `experience.accumulation`（`manual` / `auto` / `off`，用户可控回填开关），由 §经验回填环节 消费，不进调度协议。
> `DECISIONS.md` 由 P1 Step 0 前置决策采集生成（用户可在工作流开始时填写，或由 Step 0a 苏格拉底澄清派生），并与上述结构化字段对账。A5/A6 是调度协议核心变量；A1-A4 由路由与门控消费（A1 定阶段范围，A2 定 P2/P3/P4 行为分支，A3 驱动 §可选阶段判断，A4 已并入 P2）。

## 决策分级 + 术语大白话（实测教训）

> 工作流用户可见的决策点 / 门控提问必须用大白话，不准只用内部术语（A1-A6 / partial_reference / greenfield / GATE-xxx）绕用户。内部术语只作编排器内部变量，向用户提问时必须配大白话解释。

**决策分级（问用户 ↔ 自决平衡）**：遇问题先分级——业务决策停转发用户，技术执行自决。

| 级别 | 含义 | 处理方式 | 典型例子 |
|------|------|---------|---------|
| **业务决策** | 物理板型 / scope 取舍 / trade-off 代价 / 新芯片选型 / 归档路径 / 经验回填开关——需用户拍板的选择 | **停下转发用户，不默认推进**（含主 agent 也不能替用户默认，实测教训） | boot 介质 SPI Nand vs eMMC、外设范围、版本号、归档路径、boot_image 缺失后是否终止 |
| **技术执行** | 内核 config、patch 适用性、工具链路径、构建路径当只有一条可行、按工作流教训可定的——执行者按工作流教训+验证自决 | **执行者自决，不转发用户**（实测教训） | defconfig 开 MTD、加 BINDER_IPC_32BIT 宏、修 TC_DIR 路径、路径 B OH 集成当唯一可行时 |

**内部术语 → 大白话对照表**（**面向用户的转译表述**，供向用户提问/汇报时使用；A1-A7 的技术定义以 §Agent 调度协议 摘要中的决策变量表和 `DECISIONS.md` 为准）：

| 内部术语 | 大白话 |
|---------|--------|
| **A1** | 这次跑哪一种：完整全流程 / 只做编译验证 / 快速出固件（跳过测试和文档） |
| **A2** | 目标资源级别（L0/L1）与 target profile：profile 明确内核、驱动模型、设备描述和构建集成；不从等级推断 LiteOS/HDF |
| **A3** | 哪些可跳过的环节要跳：测试 / 文档+审查 / RTOS 驱动迁移 |
| **A4** | 内核裁剪怎么做（已并入内核配置阶段，不再单独决策） |
| **A5** | 分发模式：单 agent 顺序跑 vs 多子代理并行跑 |
| **A6** | 遇到疑难杂症时，诊断要不要升级到更强的推理档位 |
| **partial_reference** | OH 仓里已有这颗芯片的半成品骨架，复用它补全修正（不是从零重写） |
| **greenfield** | OH 仓里没有，从零生成全部文件 |
| **has_reference** | OH 仓里有完整参考适配，可直接复用 |
| **GATE-0** | 项目启动确认（环境基线 + 工具链 4 子门控） |
| **GATE-K** | 内核基线确认（内核能否启动到 main() + 来源完整性） |
| **GATE-D** | 驱动范围确认（HCS 配置与驱动匹配） |
| **GATE-B** | 编译通过确认（GATE-V11 编译 + GATE-V12 多产物大小/结构） |
| **GATE-B+** | 烧录前消费者验收门控——每个产物有消费者 + 外部锚（厂商工具产出/magic-byte/跨产物一致性/用户试烧），无锚则显式声明"未验证"，不准默写"已构建" |
| **GATE-BURN** | 烧录操作确认（按目标级别选择 HiBurn、HiTool 或厂商 ToolPlatform，需用户确认模式后执行） |
| **GATE-HW** | 测试硬件运行确认（串口捕获/HIL/XTS，需用户确认后执行） |
| **GATE-交付** | 交付前归档路径硬约束——问用户输出件归档到哪个本地路径，ad-hoc/工作流外构建同样适用 |

> **执行纪律（问用户与自决平衡）**：遇决策先按上表分级。业务决策必须停下转发等明确答复，绝不默认推进（哪怕主 agent 给"默认值"，只要用户没明确说也停下问）。技术执行按工作流教训+验证自决，不拿技术决策烦用户。

## 与共享工具的引用关系

各阶段 step 通过 plugin 根相对路径 `skills/<id>/` 引用共享工具（16 个能力 skill 平铺；编排器即本文件，阶段实现在 `{{ASSET_ROOT}}/workflow/steps/`）：

```
skills/                            # 共享工具 + 编排器（plugin 根下平铺）
├── ohos-dev-workflow-router/                 # ← 你在这里（编排器）
│   └── references/
│       └── agent-dispatch-protocol.md  # Agent 调度协议完整版（仅 A5 启用调度时读取）
├── ohos-dev-soc-spec-parse/
├── ohos-dev-board-config-gen/
├── ohos-dev-build-config/
├── ohos-dev-kernel-source-query/
├── ohos-ci-lite-deploy-burn/          # 编译→下载→烧录→MAP 分析（覆盖烧录）
└── ohos-dev-cross-toolchain/         # 交叉编译工具链配置

{{ASSET_ROOT}}/workflow/           # 工作流运行时资产
├── DECISIONS.md                   # A1-A7 人类可读决策记录（供宿主适配器对账）
├── workflow_config.template.yaml  # 结构化配置模板
├── target-profiles/               # per-target 结构化配置（P1 加载，见 §target profile 加载规则）
│   ├── README.md                  # profile 必填字段定义 + 无 profile 须先建再实现
│   └── hi3516cv610-linux-l1.yaml  # 内置 profile（Hi3516CV610 / Linux / L1）
└── steps/
    ├── 01-env-prep/SKILL.md      # （无工具依赖）
    ├── 02-kernel-port/SKILL.md   # 引用 skills/ohos-dev-kernel-source-query
    │                              # 引用 skills/ohos-dev-soc-spec-parse
    ├── 03-driver-device/SKILL.md # 引用 skills/ohos-dev-soc-spec-parse
    │                              # 引用 skills/ohos-dev-board-config-gen
    ├── 04-build-verify/SKILL.md  # 引用 skills/ohos-dev-build-config
    │                              # 引用 skills/ohos-ci-lite-deploy-burn（烧录验证）
    ├── 05-test-gen/SKILL.md       # （无强制工具依赖）
    ├── 06-doc-review/SKILL.md     # （无强制工具依赖）
    └── 07-problem-diag/SKILL.md   # （无强制工具依赖）
```

---

## P-交接与安全契约

每个阶段在下一阶段开始前必须公布 `confirmed`、`unverified`、`blockers`、`artifact_paths`、`completeness` 和 `verification_manifest` 引用。`intermediate` 和 `partial` 只是诊断状态，永远不准描述为最终烧录包。外部验收角色不在本工作流门控管辖内。

P1 必须评估板级代码、内核/U-Boot、镜像构建器、烧录介质、硬件/离线验证的可用性，并盘点 GSL/DDR/寄存器数据、U-Boot、镜像生产者和确切的打包命令。私有启动链输入缺失时在 P2/P4 前设 `BLOCKED_VENDOR_SDK`；内核/rootfs 工作只能作为诊断工作继续，且不准伪造 `boot_image.bin`。

P4 在启用时运行 `deps_guard` 和 `startup_guard`。失败按 `product_board_adaptation` / `source` / `workflow_input` / `toolchain_environment` 四分类归因（构建门控视角的责任归因，进 P7 后由诊断侧按 A-H 8 类重新归类，见 `04-build-verify` Step 3.5），记入 manifest 并阻断 GATE-B。守卫 PASS、编译 PASS、启动链完整性和硬件验收是相互独立的结果。

AI 起草代码、配置或脚本时必须记录来源/引用、假设、验证状态和人工确认点。vendor 私有输入只能被分析、验证或编排，永远不准被推断或伪造。

## 状态管理

### 进度追踪格式

```json
{
    "target": { "name": "", "arch": "", "system_type": "", "product_type": "" },
  "phases": {
    "P1": { "status": "pending|in_progress|completed|stuck|gate_review|skipped_user|skipped_mode|conditional_delivery|failed", "gate_passed": false, "evidence_refs": [] },
    "P2": { "status": "pending", "gate_passed": false, "substeps": { "2a":"...", "2b":"..." }, "evidence_refs": [] },
    "P5": { "status": "pending", "gate_passed": false, "compile_status": "pending|PASS|FAIL|SKIPPED_USER|SKIPPED_MODE", "hardware_status": "pending|PASS|FAIL|SKIPPED_NO_HARDWARE|SKIPPED_USER|SKIPPED_MODE", "evidence_refs": [] },
    "P6": { "status": "pending", "gate_passed": false, "independence_status": "null|VERIFIED_INDEPENDENCE|UNVERIFIED_INDEPENDENCE", "criticals_closed": false, "work_complete": false, "evidence_refs": [] },
    ...
    "P7": { "status": "pending", "invoked_from": null, "return_phase": null, "return_step": null, "same_error_rounds": 0 }
  },
  "current_phase": "P1",
  "last_gate": null,
  "error_history": [],
  "artifact_refs": [],
  "evidence_refs": []
}
```

### 状态转换规则

```
pending → in_progress (开始执行)
in_progress → completed (正常完成)
in_progress → stuck (遇到问题)
stuck → P7 (切入诊断)
P7 → in_progress (修复后返回原阶段断点)
completed → gate_review (到达门控)
gate_review → next_phase (门控通过)
gate_review → in_progress (门控不通过，补充执行)
pending → skipped (可选阶段被跳过)
```
