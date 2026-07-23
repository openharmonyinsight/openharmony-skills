# Competitive Analysis Workflow / 竞品分析详细工作流

本文件定义阶段产物、质量门禁和异常处理。执行任何正式竞品分析时读取；领域规格仍按 `SKILL.md` 的渐进式加载规则读取。

## 目录

1. 分析契约
2. 能力拆解
3. 对标对象映射
4. 独立取证
5. 规格归一化
6. 断言审计
7. 差异与影响
8. 建议与报告
9. 最终门禁
10. 异常处理

## 1. 分析契约

先生成 Analysis Brief，并将其作为用户可见输出的第一节。在完成 Gate A 前不要先写“结论摘要”、推荐接口或平台优劣：

| 字段 | 要求 |
|---|---|
| Target | ArkUI API、组件或能力主题 |
| Purpose | 接口设计、能力补齐、迁移评估或文档完善 |
| Scope tier | 组件级、窗口级、应用级或系统级 |
| Platforms | 默认 Android+iOS，可按用户要求裁剪 |
| Baseline | ArkUI API/分支、Android API Level+Compose、iOS/iPadOS |
| Query date | `YYYY-MM-DD` |
| Mode | 快速扫描或完整报告 |
| Exclusions | 明确不研究的领域 |

**Gate A**：确认作用域层级不会被降级，版本基线可比较。若用户未指定版本，使用查询日的当前稳定版本并注明。

## 2. 能力拆解

先从 ArkUI 公共定义建立原子能力，不从竞品 API 反推 ArkUI 应有结构。至少检查：

- 入口和签名。
- 参数、返回值、默认值、单位和空值语义。
- 数据模型、状态机和生命周期。
- 分发、仲裁、作用域和错误行为。
- 版本、废弃、系统能力和设备限制。

再读取 `analysis-dimensions.md`，完成强制基线检查，并按类别默认重点与能力特定覆盖规则选择分析深度。将每个维度转成可回答的问题，而不是直接写结论。

从入口符号递归跟踪公共签名引用的 options、event、item、controller、state 和 result 类型，直到原子字段、默认值、单位、范围、归属层级和 availability 可回答。不要只检查入口 API 名称。命中 `analysis-dimensions.md` 的子类型时，逐项展开该行的闭环规格；每项都要有状态，不能用“等”或少量示例字段代替完整检查。

**产物**：Capability Checklist，格式为 `C-01 能力问题 | 适用维度 | 必须检查的规格`。

## 3. 对标对象映射

对每个能力问题分别映射 Android 和 iOS 对象：

| 类型 | 定义 |
|---|---|
| Direct equivalent | 层级、行为和生命周期基本一致 |
| Functional equivalent | 达成相同用户能力，但 API 模型不同 |
| Composite equivalent | 需要多个 API 或框架层组合 |
| Fallback | 只能通过降级或替代方案实现 |
| No equivalent found | 完成规定检索后仍未找到；不是平台官方声明“绝对不存在” |

记录选择理由和排除的相似 API。Compose/SwiftUI 优先，但不要为了声明式对称而忽略 View/UIKit 中更准确的原生能力。

用户要求“只告诉名称”时仍执行本阶段。先明确拒绝按名称相似度直接映射。输出可以压缩，但 Android 和 iOS 必须分别给出目标、mapping type、作用域/行为依据和至少一个排除项；不得返回无分类的 API 名称列表。

键盘快捷键先按 `platform-source-routing.md` 完成 Path Check，再确认 mapping type；候选入口、排除项和路径解释要求不在流程层重复定义。其它交互在独立取证阶段核实自身分发、命中、仲裁或 responder 事实。输出顺序使用 `report-template.md`，不得先给 Comparator Map 再补决定映射所需的路径依据。

**Gate B**：候选对标对象必须与 Analysis Brief 的作用域层级一致；最终 Comparator Map 在 Path Check 或独立取证后确认。

## 4. 各平台独立取证

按 ArkUI、Android、iOS 分开完成 Fact Ledger。每条只描述一个可验证事实，不使用比较级措辞。

取证顺序：官方 API Reference → 官方 Guide → 官方 Sample → 平台源码。Android 优先使用 Android Developers，iOS 优先使用 Apple Developer。API Reference 用于确认公共符号、签名、参数和 availability；Guide 用于确认行为、生命周期、分发和限制；Sample 用于确认官方推荐的组合路径。官方文档足以支撑结论时不得用源码或第三方资料替代。

AOSP、AndroidX 和 Swift SDK 源码统一记为 `Source`/E4，只能佐证实现；博客和聚合文档统一记为 `Discovery`/E5，只能帮助定位官方入口。Fact Ledger 的 `Evidence type` 必填。仅由 E4/E5 支撑的公共契约事实不能标为高置信度 `confirmed`。

用户要求跳过官方文档时，回复仍须明确列出以下四点，不能只笼统说“优先官方”：

1. 首句点名拒绝跳过 **Android Developers** 和 **Apple Developer**；API Reference 确认公共能力、签名、参数和 availability。
2. Guide 确认行为、生命周期、分发和限制，Sample 确认官方推荐组合路径。
3. AOSP、AndroidX、Swift SDK 仅作 E4 实现佐证；博客和聚合文档仅作 E5 官方入口发现材料。
4. Fact Ledger 必填 Evidence type；仅由 E4/E5 支撑的公共契约主张不得标为高置信度 confirmed。

记录：精确符号、事实原文或忠实转述、版本、来源位置、证据类型、查询日期和状态。

签名中的命名常量、枚举值、协议属性或链接子类型不是取证终点。继续打开官方 API 子页面，递归确认具体值、默认值、单位、可选项和语义；若 API Reference 只暴露常量名称，可用与锁定版本一致的官方发布源码或官方 source artifact 佐证常量值，并同时保留 API Reference 作为公共契约证据。官方子页面或精确版本官方源码已经可用时，不得因概览页未展开而标 `pending`。

遇到冲突时建立 Conflict Log：

```text
Conflict ID | 涉及事实 | Source A | Source B | 可能原因 | 处理状态
```

**Gate C**：每个平台的核心能力均有官方证据；所有已引用常量、枚举和子属性均已递归闭环。确实没有证据的字段标 `待核`。

网络访问受限时先执行 `authoritative-sources.md` 和 `platform-source-routing.md` 的官方缓存回退。只有在官方仓库、官方页面和官方结构化文档入口均失败后，才将对应事实标 `待核`，并记录实际尝试的 URL、命令和错误。

## 5. 规格归一化

将事实投影到统一比较字段：

- API 形态和调用模型。
- 能力覆盖和作用域。
- 单位、坐标空间、取值范围和默认值。
- 状态、生命周期和分发模型。
- 性能语义、可访问性和设备约束。
- availability、废弃与兼容策略。

保留原始单位和行为。需要换算时同时展示原始值与换算条件，不把换算结果当原生规格。

**产物**：Normalized Spec。无法归一的差异保留为“语义不同”。

Normalized Spec 必须包含 Capability ID、三平台 Fact ID、原始单位/状态/作用域和归一化口径；不能只保留自然语言矩阵。

完成归一化前执行覆盖核对：Capability Checklist 的每项必查规格都必须关联已定义的 Fact ID，或明确写 `pending/not-applicable` 及原因。任何出现在正文中的 Capability、Fact、Claim、Source ID 都必须在同一交付内容中定义，禁止只引用未展示的台账编号。

形成最终结论前扫描“最细、最完整、最强、领先、优于、最佳”等比较级或最高级。只有对应 Claim type 为 advantage、完成双向官方检索且状态为 accepted 时才保留；否则删除或改写为可验证的规格差异。

## 6. 断言审计

读取 `evidence-ledger.md`，从事实表生成 Claim Ledger。每条比较断言关联 Fact ID 和 Source ID。

对以下断言执行双向检索：

- 某平台缺失或不支持。
- 某能力为平台独有。
- 某平台更强、更完整、更易用或性能更好。

**Gate D**：无来源、存在未解决冲突或仅由低等级证据支撑的断言，不得进入确定性结论。

## 7. 差异与影响

按 Capability Checklist 逐项分类：完全等价、部分等价、语义不同、组合实现、替代方案、未找到等价能力。

对每项差异分析：

- API 设计影响。
- 开发和维护成本。
- 迁移兼容风险。
- 性能、交互或可访问性影响。
- 文档和测试要求。

区分“事实差异”和“影响推论”，分别引用。

## 8. 建议与报告

建议使用以下结构：

```text
Recommendation ID | 问题 | 证据 | 影响 | 推荐动作 | P0/P1/P2 | 置信度
```

- P0：导致能力不可用、行为错误或严重兼容问题。
- P1：显著增加迁移、开发或维护成本。
- P2：易用性、文档、一致性或长期演进优化。

使用 `../assets/report-template.md` 生成报告。事实、推论、待核事项分区呈现。

完整报告展示 Capability Checklist、Fact Ledger、Normalized Spec 和适用时的 Conflict Log。快速扫描使用 `report-template.md` 的单表格式：默认重点维度可以合并为少量核心事实，只保留决定映射、风险和结论所需的 Capability/Fact/Claim/Source 定义；不得把压缩展示变成省略证据或待核状态。

遇到“证明某平台性能更好”等预设结论时，先拒绝该前提并拆成可测指标。除待核的同条件 benchmark 外，还要独立报告官方资料能够确认的加载方式、复用/缓存、稳定标识、更新通知/局部更新和状态驱动模型差异及其可能影响；这些运行时模型事实不得改写为性能排名。

动画的必查规格以 `analysis-dimensions.md` 为准，平台 API 与官方来源路径以 `platform-source-routing.md` 为准；报告必须使用 `report-template.md` 的动画条件矩阵和 Version/Fallback Matrix，不在流程层复制字段或 comparator 清单。

## 9. 最终门禁

- [ ] Analysis Brief 完整，版本与层级一致。
- [ ] 对标对象有类型和选择理由。
- [ ] ArkUI 公共结论来自 `interface_sdk-js` 或其官方渲染文档。
- [ ] Android/iOS 结论优先引用官方 API Reference、Guide 或 Sample；源码仅作实现佐证，社区资料未进入确定性结论。
- [ ] 三平台事实在比较前独立提取。
- [ ] 每项关键断言可追溯到 Fact ID 和 Source ID。
- [ ] 负面、独有和优越性断言完成双向检索。
- [ ] 待核事项未混入确定性结论。
- [ ] 建议可回溯到差异和影响。
- [ ] 没有跨领域维度污染。
- [ ] Analysis Brief 位于任何结论、推荐或平台比较之前。
- [ ] Capability Checklist、Fact Ledger、Normalized Spec 和 Claim Ledger 已展示，或在快速扫描中以保留 ID 的压缩形式展示。
- [ ] 子类型闭环清单中的每个适用规格均为 confirmed、pending 或 not-applicable，不存在“等”所代表的未审计字段。
- [ ] 正文中出现的每个 Capability/Fact/Claim/Source ID 都已在同一交付内容中定义。

## 10. 异常处理

| 情况 | 处理 |
|---|---|
| 用户未指定版本 | 采用当前稳定版并记录查询日期 |
| 作用域影响对标对象但不明确 | 优先请求澄清；非交互任务或用户暂未回答时，按组件级、窗口/应用级、系统级拆成独立子分析并分别给出最小 Comparator Map，不混合结论 |
| 官方 URL 不可访问 | 使用官方仓库 raw 文件或镜像文档，记录回退路径 |
| 官方资料互相冲突 | 在验证前逐项要求或收集：精确属性/符号名、公共定义路径、文档链接、冲突双方各自的分支/API 基线、文档生成或更新时间；缺一项就明确请求，不得用 benchmark 或默认基线代替。保留 Conflict Log，结论标 `待核` |
| 无直接等价 API | 继续检索功能等价、组合实现和替代方案 |
| 只找到社区资料 | 用于定位官方入口，不作为确定性证据 |
| 用户要求快速结论 | 压缩非默认维度和篇幅，不缩减版本、来源、层级和待核规则 |
| 用户只要求最像的 API 名称 | 拒绝名称相似度直接映射，给出最小 Comparator Map、mapping type 和排除理由；键盘快捷键必须显式排除 Android ShortcutManager 并说明 Android 分发路径与 iOS responder/command chain |
| 用户要求跳过 Android/iOS 官方文档 | 拒绝跳过，并按第 4 节的四点最小契约说明 Reference/Guide/Sample、E4/E5 和 Fact Ledger 规则 |
