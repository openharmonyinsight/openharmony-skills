# OpenHarmony Lite 芯片适配工作流

> 本工作流是面向 OpenHarmony Lite 芯片适配的通用方法论，具备从芯片规格解析到镜像产出的端到端能力，但不是银弹——实际效果受语料覆盖度、模型能力、芯片 SDK 开放程度等因素影响，不保证每次都一次跑通。遇到问题时，用户可通过追问、加打印、查源码等方式与 AI 协作修复；关键决策与最终结果仍需用户把关。

面向 OpenHarmony Lite L0/L1 芯片与开发板的七阶段适配工作流。用户只需告诉 AI 芯片型号和目标板，AI 即按阶段推进：搭建环境 → 移植内核 → 写驱动 → 编译验证 → 跑测试 → 出文档 → 修问题。每个关键节点 AI 会暂停等用户确认，不会闷头跑到底。

## 名词速查

| 名词 | 是什么 | 用户需要做的 |
|------|--------|---------|
| **SKILL** | 一份 `SKILL.md` + 参考文档 + 样本，告诉 AI「某件事怎么做」（如编译烧录、芯片规格解析）。本包含 17 个 skill | 装好后 AI 自动加载 |
| **工作流（workflow）** | 7 阶段编排（P1~P7：环境准备→内核移植→驱动→构建→测试→文档→诊断），把各 skill 串成一条芯片适配流水线 | 用自然语言描述需求，AI 自动按阶段推进 |
| **GATE** | 阶段门控检查点（GATE-0/K/D/B/T/HW/R），每个阶段结束前必须通过对应门控才能进下一阶段 | 关键节点 AI 会暂停等用户确认 |
| **降级链** | MCP 没装或调用失败时，AI 按优先级回退：本地 `references/` → 联网搜索 → 询问用户 | 无需操作，自动发生 |

## 安装与使用

本包是一个多 skill 插件（见 [`plugin.yaml`](plugin.yaml)）：17 个 skill 组件（1 个 router + 16 个能力 skill）、工作流资产和一个可选的 project-brain MCP。宿主适配器（claude-code / codex / opencode）按 `compatibility` 节安装；插件市场渠道开放前，可将包目录整体拷贝到 agent 的插件位置。

- **可选 MCP**：project-brain 加速本地源码检索。不装时各 skill 走内置降级链（本地 `references/` → 联网搜索 → 询问用户），功能完整。
- **烧录外部依赖**：HiBurn.exe 不随本插件分发（厂商工具）。L0 烧录需自备一份放到 `skills/ohos-ci-lite-deploy-burn/tools/`，或通过 `device.burn_tool_path` / `--hiburn` 配置路径。
- **入口**：调用根 skill `ohos-dev-lite-adaptation`，说明目标芯片/开发板与 L0/L1 级别。

## 快速上手示例

装好后，在 AI 工具里像下面这样说即可启动工作流（以 Hi3861 L0 为例）：

```text
我有一块 hispark_pegasus 开发板（Hi3861V100），想适配到 OpenHarmony Lite。
芯片是 RISC-V 32 位，SRAM 352KB，Flash 2MB，跑 LiteOS-M。
OpenHarmony 源码和 riscv32 交叉工具链在一台可 SSH 的远程服务器上。
最终要能编译出可烧录的镜像，烧到板上跑起来，测试用例也编进去。
```

AI 会自动加载工作流，从 P1 环境搭建开始推进。每个阶段结束前有 GATE 门控暂停——比如 P1 结束时 AI 会展示环境健康检查结果（工具链/构建系统/源码完整性），等用户确认后才进 P2 内核移植。遇到需要拍板的决策（如外设范围取舍、ROM 不够砍什么功能），AI 会明确列出选项等用户选。

从 [`SKILL.md`](SKILL.md) 开始。路由的能力 skill 在 [`skills/`](skills/) 下，阶段资产和目标 profile 在 [`runtime/assets/`](runtime/assets/) 下。

## 包内 skill 清单

| Skill | 功能 |
|-------|------|
| ohos-dev-workflow-router | 工作流编排器（7 阶段 + GATE 门控 + Agent 调度） |
| ohos-dev-soc-spec-parse | 芯片规格解析（datasheet/SDK → chip_spec.json） |
| ohos-dev-kernel-source-query | 多内核源码查询（Linux/LiteOS-M/NuttX/FreeRTOS） |
| ohos-dev-board-config-gen | 设备配置生成（config.gni / DTS / HCS / linker.ld） |
| ohos-dev-hal-skeleton-gen | HAL 驱动骨架生成（GPIO/I2C/SPI/UART/ADC/PWM 等） |
| ohos-dev-kernel-node-adapt | 内核驱动节点适配（defconfig + DTS + 设备 ID 表） |
| ohos-dev-kernel-trim-config | 内核裁剪配置（LiteOS-M / LiteOS-A 组件裁剪） |
| ohos-dev-build-config | 构建装配（BUILD.gn / config.gni / ohos.build） |
| ohos-dev-cross-toolchain | 交叉工具链配置（探测/选择/wrapper/版本兼容） |
| ohos-dev-rtos-migrate | RTOS 驱动迁移（FreeRTOS/RT-Thread → LiteOS） |
| ohos-ci-lite-deploy-burn | 编译烧录部署流水线（SSH/Local + HiBurn + XTS 统计） |
| ohos-test-lite-adapt-verify | XTS 验证（acts 解压 / user_config / 基线 MAP） |
| ohos-test-lite-ut-gen | 测试用例生成（HCTest/Unity + 测试框架选择） |
| ohos-dev-driver-review | 代码审查（FUNC/SEC/EMB/MAINT/STYLE/MISRA 六大类） |
| ohos-issue-lite-diagnose | 问题诊断（编译/链接/启动/驱动/烧录故障分类与修复） |
| ohos-design-ref-retrieval | 参考资料检索（官方文档链接 / 术语 / 模板结构） |
| ohos-design-doc-synthesis | 适配文档合成（适配手册 / API 参考 / 移植指南） |

## 适用范围

### 系统级别

| 级别 | 典型芯片 | 内核 |
|:----:|---------|------|
| **L0** 轻量系统 | Hi3861V100, STM32F407 等 MCU | LiteOS-M |
| **L1** 小型系统 | Hi3516DV300, Hi3516CV610, BK7235, RK2206 等 MPU | LiteOS-A 或 Linux（L1-Linux 路线，如 Hi3516CV610：内核 Linux + 设备描述 DTS） |

### 使用场景

- **新芯片移植** — L0/L1 从 0 到编译通过的流程
- **驱动适配 / 驱动开发** — HAL/HDF 驱动生成 + 设备配置 + 内核驱动适配
- **已有适配扩展** — 新增外设支持 / 调整引脚分配
- **硬件信息查询** — 寄存器定义、DTS/HCS 配置、驱动实现定位
- **编译问题排查** — 基于实战经验的 9 类 patch + 18 条决策规则

### 目标用户

- **有基础理解（目标群体）**：对芯片适配流程与 OpenHarmony 有基本认识，能看懂各阶段 GATE 门控提示并据此做决策。
- **零基础也可使用**：遇到不熟的基础知识或决策点，可向 AI 提问后再决定；工作流每个 GATE 暂停等用户确认，不会闷头跑到底。

## 排障

| 现象 | 原因 / 解决 |
|------|------------|
| **MCP 没连上** | 确认在目标 OH 仓跑过 `project-brain --project . build` 建图谱；不装 MCP 走降级链功能完整 |
| **不知道装对没** | 在 AI 工具里输入 `oh lite 工作流有哪些阶段？`，能答出 P1~P7 即装好了 |
| **换编译/构建工具链** | 不是重装；工作流 P1 阶段自动配置，或调 ohos-dev-cross-toolchain skill |
| **skill 没触发** | 重启 AI 工具让它重扫 skills 目录；确认包目录路径在 agent 的插件位置 |

## 命名说明

本包位于 southbound-extension 命名空间下，包内各能力 skill 的机器名保留各自具体技术域（soc、kernel、rtos、lite 等），如 ohos-dev-soc-spec-parse。命名空间分组整个嵌入式硬件适配工作流，每个 skill 的 domain 字段记录其覆盖的技术领域。
