---
name: ohos-design-doc-synthesis
description: OpenHarmony Lite (L0/L1) 适配文档合成器——读上游 P1~P5 产出（chip_spec.json / 内核配置 / 驱动清单 / build 配置 / XTS 结果 / DECISIONS.md），套三种 deliverable 模板（① 芯片适配手册 ② API 参考文档 ③ 移植指南），填项目实际数据，合成项目专属适配文档（markdown）。Use when project-specific adaptation documentation must be produced from actual pipeline outputs; triggers include 生成适配手册、出适配文档、API 参考文档、移植指南、交付文档、适配验收材料、整理适配产出成文档、写移植报告。与 ohos-design-ref-retrieval（检索通用参考资料）互补——本 skill 合成项目专属文档。
metadata:
  author: openharmony
  scope: domain
  stage: design
  domain: doc
  capability: synthesis
  version: 0.1.0
  status: trial
---

# OpenHarmony Lite 适配文档合成

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 明确出稿任务 | "生成适配手册"、"出适配文档"、"交付文档"、"写 API 参考"、"整理一份移植指南" |
| 流程末端链式调用 | 工作流 P1~P5 产出齐了要归档出交付件；ohos-test-lite-adapt-verify 结束后写验收材料 |
| 症状词（隐性需求） | "适配做完了怎么交付"、"给领导/客户看的总结文档"、"把这些产出（chip_spec/XTS/决策）串成一份文档" |
| 同义表达 | 适配报告 / 移植文档 / 交付说明书 / 芯片适配手册 |

**不触发**（明确排除）：检索通用参考资料/怎么配/为什么（走 ohos-design-ref-retrieval，它查官方移植指南/FAQ/案例）；重新提取芯片规格（ohos-dev-soc-spec-parse）；审查代码（ohos-dev-driver-review）。

## Scope

本 SKILL 是 OpenHarmony Lite（L0 轻量系统 / L1 小型系统）芯片适配的**文档合成层**：读取上游工作流 P1~P5 的实际产出（chip_spec.json / 内核配置 / 驱动清单 / build 配置 / XTS 结果 / DECISIONS.md），套用三种 deliverable 模板（① 芯片适配手册 ② API 参考文档 ③ 移植指南），填入**项目实际数据**（非占位符），输出项目专属的 markdown 适配文档。

**本 SKILL 真生成文档**（套模板 + 填实际数据 + 出稿），与 `ohos-design-ref-retrieval` 互补：
- **ohos-design-doc-synthesis（本 skill）**：合成**项目专属**适配文档——读本项目 P1~P5 产出，填本项目实际数据，出本项目的手册/API 参考/移植指南。
- **ohos-design-ref-retrieval**：检索**通用参考**材料——查官方移植指南/API 头文件/适配案例/FAQ，告诉用户"怎么配/为什么"。

边界：本 skill 不重新提取芯片规格（chip_spec.json 由 ohos-dev-soc-spec-parse 产出），不重新审查代码（审查报告由 ohos-dev-driver-review 产出），只把上游产出**合成**成可交付文档。

## Initial Checks

出稿前按以下顺序先做判断：

1. **deliverable 意图判断**（Step 0 决策树）：三种全出 / 仅 API 参考 / 仅移植指南 / 仅适配手册；不明确 → 追问，不默认全出。
2. **上游产出盘点**（Step 1）：chip_spec.json / 内核配置 / 驱动清单+HCS / build 配置 / XTS 结果 + DECISIONS.md 各项是否在？缺哪项对应章节标 WIP，不编造。
3. **系统级别判定（L0/L1）**：决定模板分支——L0 驱动章节用 IoT 外设子系统表述、无 HCS；L1 用精简版 HDF + HCS。从 chip_spec.json 的 targetSystemLevel 或用户确认取，不猜。
4. **数据可溯源预估**：规格/状态值是否都能落到某个上游产出？有"只有印象没有出处"的值 → 出稿前补来源或标 WIP。
5. **术语基准确认**：读 `references/terminology.md`，锁定 LiteOS-M/LiteOS-A/Linux(L1-Linux 路线)、轻量系统(Mini System)/小型系统(Small System)等标准写法，出稿全程一致。

## Prohibited Practices（文档合成禁止操作）

| 禁止 | 正确做法 |
|------|---------|
| **凭记忆编造芯片规格/驱动数据填进文档** | 从上游 P1~P5 产出读实际数据（chip_spec.json / 驱动清单 / XTS 结果），标注数据来源到文档头部「数据来源」 |
| **用占位符 `${CHIP_NAME}` 出交付稿** | 模板用占位符，但**出稿必须填项目实际数据**。占位符未填 = 文档未完成，标 WIP 不交付 |
| **功能模块状态不标注验证情况** | 三档：✅ 已验证（XTS/实测过）/ ⚠️ 理论支持（未实测）/ ❌ 明确不支持。从 XTS 结果 + DECISIONS.md 取实际状态 |
| **术语不统一（混用"轻量系统"/"Mini System"/"L0"）** | 遵循标准术语：L0 = "轻量系统 (Mini System)"，L1 = "小型系统 (Small System)"，内核名 LiteOS-M / LiteOS-A / Linux(L1-Linux 路线，按 kernel_family) |
| **L0/L1 驱动框架表述混用** | L0 = IoT 外设驱动子系统（非 HDF）；L1 = 精简版 HDF + HCS |
| **文档中硬编码芯片参数值又无来源标注** | 参数值必须能溯源到上游产出（chip_spec.json / 内核配置 / XTS），文档头部列「数据来源」清单 |
| **把 ohos-design-ref-retrieval 的检索结果当项目实际数据填** | ohos-design-ref-retrieval 给的是通用参考；本 skill 填的是本项目 P1~P5 产出。通用参考可作背景，不能冒充项目实测数据 |

---

## ① 文件路由表

### 本地参考文件（references/）

| 用户意图 | Agent 读取 | 预估行数 |
|---------|-----------|:-------:|
| 确定三种 deliverable 的章节模板骨架（适配手册/API 参考/移植指南） | `references/doc-templates.md` | ~250 |
| 查标准术语（确保文档用语一致） | `references/terminology.md`（本包自带，与 ohos-design-ref-retrieval 各自维护一份） | ~100 |

### 上游产出输入（P1~P5，必读）

| 产出 | 来源步骤 | 文档中填什么 |
|------|---------|------------|
| `chip_spec.json` | P1 ohos-dev-soc-spec-parse | 芯片规格表（CPU/RAM/Flash/外设/中断/内存映射）、DDR 变体 |
| 内核配置（Kconfig/.config/defconfig） | P2 kernel-port | 内核裁剪项、启动配置、BINDER_IPC_32BIT 等关键宏 |
| 驱动清单（HDF/IoT 外设驱动列表 + HCS） | P3 driver-device | 驱动开发章节、外设支持矩阵、API 参考的接口列表 |
| build 配置（config.gni/BUILD.gn/config.json/链接脚本） | P4 ohos-dev-build-config | 编译构建章节、内存布局、烧录配置 |
| XTS 结果 + DECISIONS.md | P5 ohos-test-lite-adapt-verify + 全程决策 | 功能验证状态（✅/⚠️/❌）、适配决策记录、已知问题 |

> 上游产出缺失时，对应章节标 WIP（Work In Progress）+ 列出"待 P? 产出后填"，不编造。

---

## ② 工作流

### Step 0: 意图判断

```
用户输入
  ├── "生成适配手册"/"出适配文档"/"交付文档"
  │   → 三种 deliverable 全出（适配手册 + API 参考 + 移植指南）
  ├── "生成 API 参考"/"API 文档"
  │   → 仅出 ② API 参考文档
  ├── "生成移植指南"/"移植文档"
  │   → 仅出 ③ 移植指南
  ├── "生成适配手册"
  │   → 仅出 ① 芯片适配手册
  └── 不明确
      → 追问：要哪种 deliverable？芯片型号？系统级别（L0/L1）？
```

### Step 1: 收集上游产出

读取 P1~P5 产出，建立文档数据池：

```
1. 读 chip_spec.json → 芯片规格（CPU/RAM/Flash/外设/中断/内存映射/DDR 变体）
2. 读内核配置（defconfig/.config）→ 内核裁剪项 + 关键宏（如 BINDER_IPC_32BIT）
3. 读驱动清单（HDF device list / IoT 外设 Operations 表 + HCS）→ 外设支持矩阵 + API 列表
4. 读 build 配置（config.gni/BUILD.gn/config.json/linker.ld）→ 构建/内存布局/烧录
5. 读 XTS 结果 + DECISIONS.md → 功能验证状态 + 决策记录 + 已知问题
6. 缺失项 → 标 WIP + 列"待 P? 产出后填"，不编造
```

**数据池结构**（内存中组织，不落盘）：
```
docDataPool = {
  chip: { from: chip_spec.json, cpu, ram, flash, peripherals, memoryMap, ddrVariant },
  kernel: { from: defconfig, keyConfigs, criticalMacros },
  drivers: { from: driver list + HCS, supportMatrix, apiList },
  build: { from: config.gni/BUILD.gn/config.json/linker.ld, memoryLayout, burnConfig },
  verify: { from: XTS + DECISIONS.md, moduleStatus[], decisions[], knownIssues[] }
}
```

### Step 2: 选择 deliverable 模板

Read `references/doc-templates.md`，按用户意图（Step 0）选模板：

| Deliverable | 模板位置 | 系统级别差异 |
|------------|---------|------------|
| ① 芯片适配手册 | `references/doc-templates.md` §1 | L0：驱动用 IoT 外设子系统；L1：驱动用精简版 HDF + HCS，内核 LiteOS-A（L1-Linux 路线 kernel_family=linux：内核 Linux + DTS） |
| ② API 参考文档 | `references/doc-templates.md` §2 | L0：IoT 外设 API（iot_gpio.h 等）；L1：HDF API + OSAL |
| ③ 移植指南 | `references/doc-templates.md` §3 | L0/L1 共用章节框架，差异在内核/驱动框架 |

### Step 3: 填充实际数据

把 Step 1 的 docDataPool 填进模板，**出稿必须填实际数据**（非占位符）：

```
对模板每个章节：
  ├── 章节需要的数据在 docDataPool 里有？
  │   ├── 有 → 填实际值 + 标数据来源（如「来源：chip_spec.json」）
  │   └── 无 → 标 WIP + 列「待 P? 产出后填」，不编造
  ├── 功能验证状态 → 从 verify.moduleStatus 取（✅/⚠️/❌），不推测
  └── 决策记录 → 从 verify.decisions 取 DECISIONS.md 原文，不改写
```

### Step 4: 术语一致性检查

| 检查项 | 方法 | 级别 |
|--------|------|:----:|
| 系统级别表述 | L0 = "轻量系统 (Mini System)"；L1 = "小型系统 (Small System)" | ERROR |
| 内核名称 | LiteOS-M / LiteOS-A（非 LiteOS_M / LITEOS-M） | ERROR |
| 驱动框架表述 | L0 = IoT 外设驱动子系统；L1 = 精简版 HDF | ERROR |
| 功能状态标注 | ✅ 已验证 / ⚠️ 理论支持 / ❌ 明确不支持（不可"应该支持"/"大概可行"） | ERROR |
| 数据来源标注 | 每个规格/状态值可溯源到上游产出 | WARNING |

### Step 5: 输出与交付

生成的文档保存为 markdown，交付给用户确认后归档。文档头部必须包含元信息块：

```markdown
> **文档类型**: 芯片适配手册 / API 参考文档 / 移植指南
> **文档版本**: ${VERSION}
> **适配版本**: OpenHarmony Lite ${OHOS_VERSION}
> **系统级别**: L0 轻量系统 (Mini System) / L1 小型系统 (Small System)
> **芯片型号**: ${CHIP_NAME}（实际值，非占位符）
> **数据来源**: chip_spec.json (P1) / 内核 defconfig (P2) / 驱动清单+HCS (P3) / build 配置 (P4) / XTS+DECISIONS.md (P5)
> **生成 skill**: ohos-design-doc-synthesis ${VERSION}
```

---

## ③ 三种 deliverable 速查

完整模板骨架（每章的内容与数据来源列）见 `references/doc-templates.md` §1/§2/§3，本章不重复维护。此处只记速记与差异：

| Deliverable | 章节数 | 关键差异/记忆点 |
|------------|:-----:|----------------|
| ① 芯片适配手册（§1） | 9 章 | L0/L1 差异集中在 §4 驱动章节（L0 IoT 外设子系统 / L1 精简版 HDF + HCS）；§7 验证状态矩阵从 XTS + DECISIONS.md 取，§8 已知问题写复现路径+规避方法（非免责声明） |
| ② API 参考文档（§2） | 5 章 | 接口列表按系统级别选（L0 IoT 外设 API / L1 HDF + OSAL）；每外设条目 = 签名 + 参数 + 返回值 + 调用约束 + 示例——调用约束必须写（中断上下文可否调用/需持有句柄等），不能只抄头文件注释 |
| ③ 移植指南（§3） | 7 章 | L0/L1 共用章节框架，差异在 §2 内核（LiteOS-M vs LiteOS-A/Linux）与 §3 驱动框架；§6 常见问题与 §7 参考案例（可引用 ohos-design-ref-retrieval 检索结果，标通用参考来源） |

**数据优先级**（同一数据出现在多个上游产出时）：chip_spec.json（规格值）> 内核/build 实际配置文件（P2/P4，实配值）> XTS 结果（验证状态）> DECISIONS.md（决策记录）。低优先级来源与高优先级冲突时按"数据矛盾"兜底处理（见 Exceptions），不静默择一。

### 术语速查

只列最常用 5 条（Step 4 校验的完整依据见 `references/terminology.md`，两包各自维护一份，改其一须同步另一份）：

| 易错术语 | 正确写法 | 错误写法 |
|---------|---------|---------|
| 内核名 | **LiteOS-M** / **LiteOS-A** | LiteOS_M / LITEOS-M |
| 系统级别 | **L0 轻量系统 (Mini System)** / **L1 小型系统 (Small System)** | L0 Mini / L1 Small |
| L0 驱动框架 | **IoT 外设驱动子系统** | HDF / 轻量 HDF |
| L1 驱动框架 | **精简版 HDF** | 完整 HDF |
| 关键区别 | L0 不使用 HDF / HCS / OSAL | — |

---

## Exceptions and Fallbacks（异常与兜底）

| 场景 | 处理 |
|------|------|
| **上游某项产出缺失**（如还没跑 XTS） | 对应章节标 WIP + 列"待 P? 产出后填"，不编造数据也不删章节 |
| **某个规格值查遍上游产出都没有出处** | 不凭记忆填——标 WIP/TODO + 注明"待补来源"；确需写时标注"参考值，非本项目实测" |
| **功能验证状态拿不准**（没跑过 XTS 也没 DECISIONS 记录） | 标 ⚠️ 理论支持（未实测），不升 ✅ 已验证、不写"应该支持" |
| **占位符填不上**（用户没给版本号/芯片丝印等） | 文档标 WIP 不交付，向用户追问实际值——占位符出现在交付稿 = 未完成 |
| **系统级别未知**（chip_spec.json 缺 targetSystemLevel 且用户没说） | 追问 L0/L1，不猜（猜错全篇驱动框架表述都错） |
| **上游产出之间数据矛盾**（如 chip_spec 与 build 配置的内存大小不一致） | 不静默择一——在文档中并列标注矛盾双方 + 请用户确认后再定稿 |
| **ohos-design-ref-retrieval 检索结果想用** | 只能作参考资料章节/背景说明，不能冒充本项目实测数据填规格表 |

---

---

> 速查: `references/doc-templates.md`
