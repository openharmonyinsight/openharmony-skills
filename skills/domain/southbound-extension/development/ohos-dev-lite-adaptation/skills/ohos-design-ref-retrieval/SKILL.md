---
name: ohos-design-ref-retrieval
description: OpenHarmony Lite (L0/L1) 参考资料检索助手。Use when the user needs links, terminology, API documentation, adaptation examples, or document-template structure during design; project-specific documents use ohos-design-doc-synthesis. Do not use for generating build files, extracting chip specifications, or diagnosing build/runtime failures.
metadata:
  author: openharmony
  scope: domain
  stage: design
  domain: ref
  capability: retrieval
  version: 0.1.0
  status: trial
---

# OpenHarmony Lite 适配参考资料检索

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 查移植指南 | "怎么开始适配""内核移植步骤""Hi3516CV610 L1 Linux 适配要哪些参考资料" |
| 查 API 定义 | "GpioOpen 的参数是什么""IoTI2cWrite 怎么用""LOS_TaskCreate 在哪定义" |
| 查适配案例 | "有没有 STM32F407 适配案例""RISC-V 移植案例""别人怎么适配 XX 芯片" |
| 查配置示例 | "config.gni 怎么写""链接脚本怎么配""device_info.hcs 示例" |
| 查 FAQ | "RAM 溢出怎么办""HardFault 如何排查""编译失败了查什么" |
| 查术语定义 | "L0 vs L1 什么意思""HDF 和 IoT 外设子系统区别""HCS 和 DTS 什么关系" |
| 适配文档模板/术语规范 | "适配手册模板""移植指南章节结构""术语规范" |
| 下游/上游 skill 链式调用 | ohos-design-doc-synthesis 合成项目专属文档前需本 skill 检索通用参考材料 + 提供模板结构与术语规范；设计阶段工作流路由到资料检索 |

**与 ohos-design-doc-synthesis 的分工（互斥边界）**：本 skill 管"检索推荐参考材料 + 模板结构 + 术语规范"；ohos-design-doc-synthesis 管"读上游 P1~P5 全部产出（chip_spec.json/内核配置/驱动清单/build 配置/XTS 结果/DECISIONS.md）合成项目专属完整文档"。用户要"一份填好本项目实际数据的完整适配手册"→ ohos-design-doc-synthesis；要"参考资料推荐/模板骨架/术语检查"→ 本 skill。

**不触发**（明确排除）：要生成会编译进固件的代码/配置文件（走 ohos-dev-board-config-gen / ohos-dev-build-config 等上游 SKILL）；只问某个具体芯片的硬件规格数值（走 ohos-dev-soc-spec-parse）。

## Scope

本 SKILL 是 OpenHarmony Lite（L0 轻量系统 / L1 小型系统）芯片适配的**参考资料检索层**：识别用户在适配设计阶段的意图（移植指导 / API 查询 / 案例参考 / 配置示例 / FAQ / 术语定义），从 references/ 中检索最相关的文档、头文件和配置样本，按标准文档模板组织输出。

**本 SKILL 做资料检索 + 意图识别 + 文档模板填充，不生成任何会被编译进固件的代码**。与上游 SKILL（如 ohos-dev-board-config-gen 生成配置文件）互补——本 SKILL 告诉用户"怎么配"和"为什么这么配"，上游 SKILL 生成具体的配置内容。

**输入**：用户自然语言查询（意图 + 芯片/模块关键词）；可选 chip_spec.json（生成适配文档时的模板变量来源）。
**输出**：`recommended-refs.md`（结构化参考资料推荐，每条带标题 + 来源路径 + 内容摘要 + 匹配度 + 使用阶段），或适配文档（按 L0/L1 模板填充，仅当用户明确要求"生成适配手册"时）。
**不适用**：非 OpenHarmony Lite 目标的文档需求；生成固件代码/配置文件；芯片规格数值提取（ohos-dev-soc-spec-parse 负责）。

### 意图分发清单

检索一律走降级链：**可用知识检索工具（如 MCP）→ 本地 references/ → 联网搜索 → 询问用户**。下表"检索降级链"列给出每个意图在各层级分别检索什么——所有层级都真实可用，按顺序尝试即可，不存在包内 resources/ 目录。

| 用户意图 | 检索降级链（知识检索工具 → 本地 references/ → 联网搜索） | 典型问题示例 |
|---------|------------|------------|
| **查移植指南** | 工具检索 porting-guide 类资料 → `references/doc-templates.md` §3-4 + `references/bibliography.md`（官方指南链接） | "怎么开始适配""内核移植步骤" |
| **查 API 定义** | 工具检索 API 头文件/函数签名（iot_gpio.h / hdf_gpio 等）→ `references/bibliography.md`（代码仓库链接）→ 联网查官方 API 文档 | "GpioOpen的参数是什么""IoTI2cWrite怎么用" |
| **查适配案例** | 工具检索 adaptation-case 类资料 + 跨 skill references（见 §① 末注）→ `references/bibliography.md`（社区案例链接） | "有没有 STM32F407 适配案例""RISC-V 移植案例" |
| **查配置示例** | 工具检索 config-example 类资料 → `references/doc-templates.md` §1-2（配置章节模板） | "config.gni 怎么写""链接脚本怎么配" |
| **查 FAQ** | 工具检索 FAQ/排障类资料 → `references/doc-templates.md` §3-4（FAQ 模板） | "RAM 溢出怎么办""HardFault 如何排查" |
| **查术语定义** | 本地直读 `references/terminology.md`（无需检索工具） | "L0 vs L1 什么意思""HDF 和 IoT 外设子系统区别" |
| **适配文档模板/术语规范** | 本地直读 `references/doc-templates.md` + `references/terminology.md`（模板骨架级；要填好项目全部实际数据的完整文档 → 走 ohos-design-doc-synthesis） | "适配手册模板长什么样""移植指南章节结构" |

### 文档生成禁止操作（Prohibited Practices）

| 禁止 | 正确做法 |
|------|---------|
| **凭记忆编造芯片规格数据（RAM/Flash/主频/引脚数）** | 从 ohos-dev-soc-spec-parse 输出的 `chip_spec.json` 或官方 Datasheet 提取，标注数据来源 |
| **术语不统一（如混用"轻量系统"/"Mini System"/"L0"）** | 遵循 `references/terminology.md` 标准术语：L0 = "轻量系统 (Mini System)"，L1 = "小型系统 (Small System)" |
| **适配状态标注不准确（未验证的功能标"已支持"）** | 功能模块状态分三档：✅ 已验证 / ⚠️ 理论支持（未实测）/ ❌ 明确不支持 |
| **忽略系统级别的文档差异** | L0 使用 IoT 外设驱动子系统（非 HDF）；L1 使用精简版 HDF + HCS 配置。适配手册中必须区分 |
| **适配案例中的芯片信息不加来源标注** | 引用已有适配案例时标注案例来源（仓库 + 文档路径），引用芯片规格时标注数据来源 |
| **文档中硬编码芯片参数值** | 使用 `${CHIP_NAME}` / `${RAM_SIZE}` 等变量占位，由用户填充 |
| **把 L0 接口推荐给 L1（或反之）** | 先判系统级别再选接口：L1 用精简版 HDF（gpio_if.h 等），不推荐 iot_gpio.h 等 L0 IoT 外设接口（反向同理） |
| **产出头部不标数据来源/检索日期** | 头部必须含检索日期 + cited 文件路径 + 数据来源（见 Step 5），保证 skill-ref 更新后重跑能拿到新值 |
| **适配手册的 build/烧录章节写成通用教程**（"先安装工具链，然后运行编译命令……"通篇无本项目值） | build/烧录章节必须写**本项目实际值**：实际编译命令、实际产物路径与大小、实际工具链版本、实际烧录参数——教程性内容一句带过 + 链官方指南，读者要的是"照着跑通"不是"重新学" |
| **全文数据多源混写**（概述章用新数据、build 章引用旧参数） | 全文芯片参数单源：一律从 chip_spec.json 取值（一处更新全文生效），禁止某章节凭旧记忆/旧文档填不同数值 |

---

## Initial Checks

收到查询后，先做以下判断（结论决定检索路径）：

1. **意图判定**：按 Step 1 的"适配阶段 × 需求类型"判断框架定 7 类意图之一；不明确时追问用户（芯片型号 + 系统级别 L0/L1 + 适配阶段），不猜测检索。
2. **系统级别判定（L0/L1）**：从用户表述或芯片型号判断（有 MMU 的 Cortex-A/RISC-V → L1；Cortex-M/无 MMU RISC-V → L0）。这决定 API/驱动框架类资料的推荐方向（L0 = IoT 外设驱动子系统，L1 = 精简版 HDF + HCS），也决定 Step 3 选哪套文档模板。
3. **内核路径细分（仅 L1）**：L1 有 LiteOS-A 与 Linux 两条路径（如 Hi3516CV610 = L1-Linux）。路径不同核心移植指南完全不同（LiteOS-A 内核移植 vs Linux 内核移植），推荐前必须确认，否则会把不相关指南排到 top。
4. **检索方式可用性**：有可用知识检索工具（MCP 等）→ 用其搜索/读取；否则直接读本地 references/；本地也没有 → 联网搜索 → 询问用户（见 §① 检索方式说明）。
5. **模板变量可用性**（仅"生成适配文档"意图）：chip_spec.json 是否已产出？缺失的关键规格变量（RAM/Flash/外设计数）必须向用户索取或指向 ohos-dev-soc-spec-parse，不得凭记忆填。

---

## ① 文件路由表

根据用户意图，读取对应的参考文件。**每次只读一个**，不要一次性加载所有 reference。

> **检索方式**: Agent 自动选择最匹配的可用知识检索工具。
> 如有可用的知识检索服务（MCP 等）→ 使用其搜索/读取能力
> 否则 → 直接 `read` 本地 references/ 下的文件
> 本地也没有 → 联网搜索 → 询问用户

### 本地参考文件（references/）

| 用户意图 | Agent 读取 | 预估行数 |
|---------|-----------|:-------:|
| 确定适配手册的结构和章节模板（L0 vs L1 不同） | `references/doc-templates.md` §1-2 | ~200 |
| 查 OpenHarmony Lite 标准术语（确保文档用语一致） | `references/terminology.md` | ~150 |
| 查外部参考链接（官方文档 / 社区案例 / 代码仓库） | `references/bibliography.md` | ~200 |
| 查 FAQ 模板和移植指南标准章节结构 | `references/doc-templates.md` §3-4 | ~120 |

### 本地参考文件续（移植指南 / API 头 / 案例 / 配置示例 / FAQ）

> 本包 references/ 只有索引、模板与链接（doc-templates.md / terminology.md / bibliography.md 三个文件），不含原始参考文件全文。移植指南全文 / API 头文件 / 适配案例 / 配置样本 / FAQ 等原始资料靠检索降级链的**知识检索工具层和联网层**获取；本地层只提供模板骨架（doc-templates.md）和外部链接（bibliography.md）。

| 用户意图 | Agent 读取 | 预估行数 |
|---------|-----------|:-------:|
| 查官方移植指南全文（L0 13 篇 + L1 7 篇 + 共用 4 篇） | `references/doc-templates.md` §3-4（移植指南标准章节结构） + `references/bibliography.md`（官方文档链接） | ~120 + ~200 |
| 查 IoT 外设 API 头文件（iot_gpio.h / iot_i2c.h 等） | `references/doc-templates.md` §1-2（适配手册模板含 API 章节） + `references/bibliography.md`（代码仓库链接） | ~200 + ~200 |
| 查已有芯片适配案例（STM32F407/BES2600W/ASR582X 等） | `references/bibliography.md`（社区案例链接） + `references/doc-templates.md`（案例引用模板） | ~200 + ~200 |
| 查配置示例（config.gni / config.json / 链接脚本） | `references/doc-templates.md` §1-2（配置章节模板） | ~200 |
| 查 FAQ（移植/构建/烧录/内核/启动/环境） | `references/doc-templates.md` §3-4（FAQ 模板和移植指南标准章节结构） | ~120 |
| 检索其他 skill 沉淀的实战参考（编译修复/驱动 playbook/烧录诊断等） | 各 skill 的 `skills/*/references/`（如 ohos-dev-build-config、ohos-dev-kernel-node-adapt、ohos-issue-lite-diagnose 的 references），经可用知识检索工具或直接 read | 按需 |

> 跨 skill references 检索（覆盖 ohos-dev-soc-spec-parse / ohos-dev-board-config-gen / ohos-ci-lite-deploy-burn / ohos-dev-kernel-node-adapt / ohos-issue-lite-diagnose / ohos-dev-hal-skeleton-gen / ohos-design-ref-retrieval 等）对用户意图更全面——实测 10 条推荐中 CV610 专属内容（DDR 变体鉴别 / init.cfg / CONFIG→/dev 映射 / 裸烧案例）均来自 expert 仓其他 skill 的 references。

---

## ② 工作流

### Step 1: 识别用户意图

不做机械关键词匹配（"包含'怎么'就查指南"在真实查询上必误判）。先问两个判断性问题，再用关键词佐证：

**问题一：用户在哪个适配阶段？**（决定优先推荐哪类资料）

| 阶段 | 特征 | 优先资料类型 |
|------|------|------------|
| 设计/选型（还没动代码） | 问"怎么开始""要哪些资料""L0 还是 L1" | 移植指南、术语定义 |
| 编码（在写驱动/配构建） | 问具体函数参数、具体配置文件写法 | API 定义、配置示例 |
| 排障（编译失败/运行异常） | 报错误现象（溢出/HardFault/起不来） | FAQ、适配案例（同类问题怎么解的） |

**问题二：要的是哪类信息？**（决定检索类别）

| 需求类型 | 用户想要 | 检索类别 |
|---------|---------|---------|
| 流程指导 | "怎么做"——步骤/顺序/方法 | 查移植指南 |
| 事实 | "是什么/参数是多少"——签名/取值/定义 | 查 API 定义 或 术语定义 |
| 案例 | "别人怎么做的"——可参照的先例 | 查适配案例 |
| 现成样本 | "抄什么"——可直接改用的文件 | 查配置示例 |
| 排障 | "出了什么问题"——现象→原因→解法 | 查 FAQ |
| 产出 | 要一份成品文档 | 生成适配文档（进 Step 3） |

**冲突消解**：一次查询常同时命中多类（如"config.gni 怎么写"既是配置示例又含"怎么"指导）——以**阶段×需求类型**判主意图（编码阶段+要现成样本 → 配置示例），其余作次意图顺带检索一句带过；两个问题仍定不了 → 追问用户：芯片型号 + 系统级别(L0/L1) + 适配阶段。

### Step 2: 检索 + 推荐

根据 Step 1 的意图分类，检索对应 resource 并推荐：

1. **检索**：按意图读取对应 references 文件（见 §① 文件路由表），在相关章节中定位最贴合的段落
2. **排序**：按下述相关度规则推荐 top 3-5 篇（星级/匹配度标注）
3. **输出**：每篇附带标题 + 来源路径 + 内容摘要（前 200 字符）+ **匹配依据**（命中了下述哪几级）
4. **溯源**：产出头部标注**检索日期** + **数据来源**（如"本 plugin references/ + skills/*/references/ + 官方文档"）——skill-ref 更新后重跑应能拿到新值（实测：同一查询在 skill-ref 修复 a4ce570 后重跑，旧错值自动消除）

**相关度排序规则**（从高到低，前两级是过滤级——不符即降出推荐或标注不匹配）：

| 级 | 规则 | 判定 |
|---|------|------|
| 1（过滤） | **系统级别匹配**：L0 资料不推给 L1 用户（反之亦然） | 意图/资料标注的 L0/L1 与用户系统级别一致 |
| 2（过滤，仅 L1） | **内核路径匹配**：L1 细分 LiteOS-A / Linux 两条路径，内核移植类资料路径不符的降级 | Initial Checks #3 的路径判定结论 |
| 3 | **意图直接对应**：查移植指南命中移植指南类文档 > 命中泛化嵌入式教程 | Step 1 判定的意图类别 |
| 4 | **芯片相关度**：同芯片型号 > 同厂商同架构 > 同系统级别泛例 | 查询/资料中的芯片型号 |
| 5（决胜） | **正文关键词命中密度**：同前四级时关键词密度高者先 | 段落内命中词数 |

### Step 3: 生成适配文档（仅当用户明确要求时；项目全数据合成优先路由 ohos-design-doc-synthesis）

> **与 ohos-design-doc-synthesis 的边界**：本 Step 提供模板骨架级填充（模板结构 + chip_spec.json 基础变量）；用户要的是"读上游 P1~P5 全部产出（chip_spec/内核配置/驱动清单/build 配置/XTS 结果/DECISIONS）合成的项目专属完整文档"时，路由到 ohos-design-doc-synthesis。

Read `references/doc-templates.md`，根据系统级别选择模板：

| 系统级别 | 模板 | doc-templates.md 位置 |
|---------|------|---------------------|
| L0（MCU） | L0轻量系统适配手册模板 | §1 |
| L1（MPU） | 参照 §3 移植指南标准章节结构（L0/L1 共用章节框架，L1 差异：驱动用精简版 HDF + HCS，内核用 LiteOS-A 含 MMU；L1-Linux 路线（kernel_family=linux）内核用 Linux、设备描述用 DTS） | §3 |

**变量填充来源**：

| 模板变量 | 数据来源 | 示例 |
|---------|---------|------|
| `${CHIP_NAME}` | ohos-dev-soc-spec-parse 输出或用户提供 | STM32F407ZG |
| `${CPU_ARCH}` | ohos-dev-soc-spec-parse 输出 `cpu.coreType` | Cortex-M4F |
| `${RAM_SIZE}` / `${FLASH_SIZE}` | ohos-dev-soc-spec-parse 输出 `memoryMap[]` | 192 KB / 1 MB |
| `${GPIO_COUNT}` 等外设规格 | ohos-dev-soc-spec-parse 输出 `peripherals[]` | 需从外设数组计数 |
| 功能模块验证状态 | 用户确认（不可由 Agent 推测） | ✅ 已验证 / ⚠️ 理论支持 |

### Step 4: 术语一致性检查

对照 `references/terminology.md` 检查生成的文档：

| 检查项 | 方法 | 级别 |
|--------|------|:----:|
| **系统级别表述** | L0 = "轻量系统 (Mini System)"；L1 = "小型系统 (Small System)"；不混用 | ERROR |
| **内核名称** | LiteOS-M（非 LiteOS_M / LITEOS-M）；LiteOS-A（非 LiteOS_A） | ERROR |
| **驱动框架表述** | L0 = IoT 外设驱动子系统（非 HDF）；L1 = 精简版 HDF | ERROR |
| **芯片架构术语** | 使用 `terminology.md` §3/§5 中的标准术语 | WARNING |
| **功能状态标注** | 三档：✅ 已验证 / ⚠️ 理论支持 / ❌ 明确不支持（不可用"应该支持"/"大概可行"） | ERROR |
| **L2 术语禁用（按 kernel_family 条件判定）** | 先读 `workflow_config.yaml` 的 `target.profile` → `kernel_family`。**LiteOS-M / LiteOS-A**：禁用 Linux DTS（用 HCS）、Kernel Panic（用 HardFault）、ext4/F2FS（用 LittleFS/FAT）、gtest 完整版（用 HCTest/精简版）。**Linux（L1-Linux 路线）**：允许 DTS、ext4、Kernel Panic、HWTEST_F/gtest——按 target profile 的 `kernel_family`/`device_description` 判定，不用 L0/L1 标签替代内核判定 | ERROR |

**这些术语为什么禁用**（写文档/答辩时的依据，不是死记；以下按 LiteOS-M/LiteOS-A 路线，L1-Linux 路线见上表条件判定）：

- **ext4/F2FS → LittleFS/FAT**：Lite 的 rootfs 只支持 LittleFS/FAT——ext4 需要 journal + page cache 等完整内核机制，L0/L1 的 footprint 和内核能力都不具备；LittleFS 是为 MCU NOR flash 设计的掉电安全文件系统（磨损均衡 + 掉电一致性），与 Lite 目标硬件匹配。
- **Kernel Panic → HardFault**：Kernel Panic 是 Linux 内核的故障机制；Lite 系统（Cortex-M/RISC-V liteos）没有 Linux panic 路径，对应的故障异常是 **HardFault**（ARM Cortex-M）或对应核的异常向量——诊断文档必须用对机制名，否则读者会去找错的排查路径。
- **gtest 完整版 → HCTest**：完整 gtest 依赖 C++ 异常/STL/较重运行时；L0/L1 lite 测试框架是 C 实现的 HCTest/精简版（iCunit 风格），写"用 gtest 验证"会误导出编译不过的方案。
- **完整 HDF → L0 IoT 外设子系统 / L1 精简版 HDF**：见下方「L0/L1 驱动框架差异的为什么」。

**L0/L1 驱动框架差异的为什么**：

- **L0 用 IoT 外设驱动子系统（非 HDF）**：L0 目标是 RAM 通常 < 512KB 的 MCU——完整 HDF 的服务注册/IPC/设备管理基础设施装不下。IoT 外设子系统是 C 函数表直接调用（IoTGpioInit 等直映射寄存器操作），零框架开销。
- **L1 用精简版 HDF（非完整 HDF）**：L1 有 MMU + 更多 RAM，能跑 HDF 的驱动模型（HdfDriverEntry + HCS 设备配置），但裁掉了完整 HDF 的分布式/跨设备能力——"精简版"保留驱动统一模型（可复用框架生态），去掉 L1 用不到的重量。文档里写"L1 用 HDF"而不带"精简版"，读者会去找完整 HDF 的远程设备管理文档，走错方向。

### Step 5: 输出与交付

生成的适配文档保存为 Markdown 文件，交付给用户确认后归档。文档头部必须包含：

```markdown
> **文档版本**: ${VERSION}
> **适配版本**: OpenHarmony Lite ${OHOS_VERSION}
> **系统级别**: L0 轻量系统 (Mini System) / L1 小型系统 (Small System)
> **芯片型号**: ${CHIP_NAME}
> **数据来源**: ohos-dev-soc-spec-parse / 官方 Datasheet §N / 已有适配案例 ${CASE_REF}
```

参考资料推荐类产出（recommended-refs.md）头部同样标注检索日期 + 数据来源 + 内核路径判定结论（如"L1-Linux：内核用 Linux 5.10 非 LiteOS-A"）。

---

## ③ 文档模板速查

快速回忆用。完整模板见 `references/doc-templates.md`。

### L0 轻量系统适配手册章节结构

| 章节 | 内容 | 必须？ |
|------|------|:----:|
| 1. 概述 | 芯片简介 + 核心规格表 + 适配范围 | ✅ |
| 2. 环境搭建 | hb 工具链安装 / 源码同步 / 编译验证 | ✅ |
| 3. 内核移植 | Kconfig 适配链 / BUILD.gn / 启动代码 / C 库适配 | ✅ |
| 4. 驱动开发 | IoT 外设驱动子系统：GPIO/UART/I2C/SPI 等 HAL 接口实现（操作函数表，非 HDF） | ✅ |
| 5. 编译构建 | config.gni / BUILD.gn / linker.ld / config.json | ✅ |
| 6. 烧录运行 | 烧录工具配置 / 串口输出 / 功能验证 | ✅ |
| 7. 附录 | 引脚映射表 / 内存布局 / 已知问题 | 按需 |
| 8. 参考资料 | 官方文档链接 / 芯片 Datasheet / 社区资源 | ✅ |

### L1 小型系统适配手册章节结构

与 L0 的差异：
- §4 驱动开发 → 精简版 HDF（HdfDriverEntry + HCS 配置），非 IoT 外设子系统
- §3 内核移植 → LiteOS-A（含 MMU/虚拟内存），非 LiteOS-M

### 术语速查

| 易错术语 | 正确写法 | 错误写法 |
|---------|---------|---------|
| 内核名 | **LiteOS-M** / **LiteOS-A** | LiteOS_M / LITEOS-M |
| 系统级别 | **L0 轻量系统 (Mini System)** / **L1 小型系统 (Small System)** | L0 Mini / L1 Small |
| L0 驱动框架 | **IoT 外设驱动子系统** | HDF / 轻量 HDF |
| L1 驱动框架 | **精简版 HDF** | 完整 HDF |
| 构建系统 | **build_lite** | build_lite_system |
| 配置格式（L1） | **HCS**（HDF Configuration Source） | DTS / Device Tree |
| 关键区别 | L0 不使用 HDF / HCS / OSAL | — |

---

## Exceptions and Fallbacks（异常与兜底）

| 场景 | 处理 |
|------|------|
| **用户意图不明确** | 追问芯片型号 + 系统级别(L0/L1) + 适配阶段，不猜测检索方向 |
| **知识检索服务不可用**（MCP 未配置/连接失败） | 降级链：本地 references/ → 联网搜索 → 询问用户。禁止以"工具不可用"为由拒绝检索 |
| **本地 references 也无对应资料** | 查 `references/bibliography.md` 外部官方链接 → 联网搜索官方文档/社区案例 → 仍无则告知用户数据源边界，不编造资料条目 |
| **cited 参考资料内容与产出 claim 不一致**（含具体数字/表格/章节号） | 逐条打开 cited 文件核实 claim 真实性；不符则改引正确文件或标注待核，不照抄可疑值 |
| **skill-ref 数据被后续修复更新**（旧值残留风险） | 产出头部标检索日期 + 数据来源；skill-ref 更新后重跑应拿到新值——若用户拿着旧产出质疑数值，先核 cited 文件当前状态再答，不直接背书旧值 |
| **chip_spec.json 缺失但用户要求生成适配文档** | 关键规格变量（RAM/Flash/主频/外设计数）向用户索取或指向 ohos-dev-soc-spec-parse 先提规格；缺的变量标 TODO + 注明"待 chip_spec.json"，不凭记忆填数值 |
| **L1 内核路径不明（LiteOS-A 还是 Linux）** | 先向用户确认内核路径再推荐核心移植指南；两条路径的指南差异大，宁问勿猜 |
| **用户要求生成固件代码/配置文件** | 明确告知超出本 skill 范围，路由到对应上游 SKILL（ohos-dev-board-config-gen / ohos-dev-build-config / ohos-dev-hal-skeleton-gen），本 skill 只提供"怎么配/为什么"的资料 |
