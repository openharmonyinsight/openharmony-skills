---
name: ohos-design-arkui-api-competitive-analysis
description: This skill should be used when the user asks to "竞品分析 ArkUI 接口", "对标 ArkUI 与 Android/iOS", "compare ArkUI API with Android/iOS", "做接口对标 / capability gap analysis", or mentions competitive analysis of ArkUI touch/gesture/component/layout/state/animation APIs. Provides a reusable 12-dimension framework, a no-scope-downgrade rule (lock the user-specified tier), an authoritative-source rule (interface_sdk-js), a bilingual report template with usage code, and a gold-standard onTouch example to produce spec-accurate comparison reports against Android (Compose/View) and iOS (SwiftUI/UIKit).
metadata:
  version: 1.0.2
---

# ArkUI API Competitive Analysis Skill / ArkUI 接口竞品分析

对 ArkUI 的 UI 接口（事件 / 手势 / 组件 / 布局 / 状态 / 动画）产出**结构一致、规格准确**的对标报告，对标 **Android（Compose/View）** 与 **iOS（SwiftUI/UIKit）**。本 skill 只做"判断与方法"，不实现代码；核心铁律：**公共接口定义以 `interface_sdk-js` 为唯一权威**，ace_engine 内部定义仅作实现对照。

# Task and Boundaries / 任务与边界

- **Goal / 目标**：对用户指定的 ArkUI 公共 UI 接口，产出一份对标 Android+iOS 的报告——规格速览 + **用法示例代码** + 能力对比矩阵 + 关键差异点（缺失 / 独有 / 行为差异）+ 结论与迁移路径 + 附录（来源）。
- **Input / 输入**：用户指明的 ArkUI 接口（如 `onTouch`、`List`）；可选对标平台（默认 Android + iOS）；可选是否含声明式（Compose/SwiftUI）与底层（View/UIKit）两层。
- **In scope / 能力边界**：仅做**公共 API 层**的能力 / 规格对标。
- **Out of scope / 不做什么**：不实现代码、不跑性能基准、不对标 Flutter/Web、不修改 ace_engine；**不用 ace_engine 内部 `.d.ts` / C++ 作公共能力结论**；不臆造字段或 `@since` 版本。

# Trigger Signals / 触发信号

- "竞品分析 / 对标 ArkUI 接口"、"compare ArkUI API with Android/iOS"、"API 能力差异 / gap analysis"。
- 设计或评审某个 ArkUI 接口前，需要参考 Android/iOS 同类能力。
- 迁移评估：从 Android/iOS 迁到 ArkUI（或反向）的能力对齐。
- 关键词：触摸 / 手势 / 组件 / 布局 / 状态 / 动画 对标、跨平台接口对比、规格口径对齐。

# Initial Checks / 初始检查（收到请求先做，按序）

1. **明确分析对象**：哪个 ArkUI 接口？对标哪些平台（默认 Android+iOS）？是否需要声明式与底层两层。
2. **锁定作用域层级（勿降级）**：用户若指明带层级的能力（如"应用级"快捷键、"组件级"触摸），必须按 `references/analysis-dimensions.md` 的「作用域层级」锁定到**用户指定的那一层**，**不得降级**成通用或其它层级。对标接口也只取该层级。
3. **判定接口类别**：事件 / 手势 / 组件 / 布局 / 状态 / 动画 六类之一 → 用 `references/analysis-dimensions.md` 的「API 类别 → 维度权重」表**裁剪**要展开的维度（不要全量堆 12 维）。
4. **准备取 ArkUI 公共定义**：进入 Execution Strategy 第 1 步的权威源规则。

# Execution Strategy / 执行策略

1. **取 ArkUI 公共规格（权威源 = `interface_sdk-js`）**。规则与命令见 `references/authoritative-sources.md`。对每个字段记录：字段名、`@since`、单位、取值范围、默认值、是否废弃、归属（事件级 BaseEvent vs 触点级 TouchObject 等）。**禁止用 ace_engine 内部 `.d.ts` / C++ 作为公共能力结论。**
2. **确定对标接口**：Android 优先 Compose（必要时退到 View / `MotionEvent`），iOS 优先 SwiftUI（必要时退到 UIKit / `UITouch` / Responder）。去各自官方文档取**同口径**字段；若第 2 步锁定了作用域层级，对标接口也只取该层级。
3. **套维度**：按第 3 步裁剪出的维度逐维对比，写进能力矩阵；每条 ArkUI 断言带 `@since` + 单位。
4. **出报告**：套 `examples/onTouch-analysis.md` 的结构——Meta / 规格速览 / **用法示例代码** / 能力对比矩阵 / 关键差异点 / 结论与迁移路径 / 附录（来源）。**格式要点**：① 规格速览中**每平台用结构化列表 / 代码块**（不要压成单行难读）；② **附每平台 1 段最小用法示例代码**说明用法；③ 若用户锁定了作用域层级，报告标题、规格、结论都要**显式围绕该层级**；④ "缺失 / 独有"类结论须**双向交叉验证**。
5. **校验**：过 `evals/` 中相关用例的预期发现清单，并确保未触犯下方 Prohibited Practices。

# Prohibited Practices / 禁止做法（反模式）

- 用 **ace_engine 内部 `.d.ts` 或 C++ struct** 的字段名 / 口径作公共能力结论。典型错误（已在 onTouch 校准中发现）：把 `force` / `operatingHand` 当公共字段、把 **px** 当触摸坐标单位、把 `screenX/Y` 当现役字段。
- **把用户指定的作用域层级降级**成通用或其它层级来分析（如把"应用级快捷键"降级成组件级 key event，导致只描述普通快捷键而漏掉应用级实现）。
- 不标 `@since` / 单位 / 取值范围就下"支持 / 不支持"结论。
- 把**事件级**字段（如 `sourceTool` / `tiltX` / `source`）误归到**触点级**对象（如 `TouchObject`）。
- 机械套满 12 维而不按接口类别裁剪，导致报告冗长无重点。
- 仅凭 ArkUI 或仅凭一方平台文档就断言"缺失 / 独有"，不做双向交叉验证。
- 用已废弃字段（如 `screenX/Y`）当现役能力来对比。

# Exceptions and Fallbacks / 异常与兜底

- gitcode `oh-gc search code` 端点不可用 → 改用 gitcode / gitee **raw `.d.ts`**，再兜底 `docs.openharmony.cn`（由 `interface_sdk-js` 生成，含 `@since` / 单位 / 废弃标记）。
- 某平台无直接对应接口 → 矩阵列 `N/A`，并给出最接近的等价替代路径与差异说明。
- 字段公共性或 `@since` 存疑 → 标注"待核（@since?）"，**不臆断**。
- 用户接口不属于六类 → 先归类；无法归类则说明无法套权重表、按通用维度全展开。
- 用户只想要一个对标平台 → 尊重选择，矩阵只留该列。
- 用户指定层级在某平台确无原生支持 → 明确标注"该平台无原生实现"，给出最接近替代，勿伪造成有。

# References / 参考文档（何时读取）

| 文档 / Doc | 用途 / Purpose | 何时读取 / When to read |
|---|---|---|
| `references/analysis-dimensions.md` | 12 维框架 + 「API 类别 → 维度权重」裁剪表 + **「作用域层级（勿降级）」** | 判定接口类别后、展开维度前；**锁定带层级能力的作用域时必读** |
| `references/authoritative-sources.md` | `interface_sdk-js` 取数规则 / 命令 / 兜底 + 校准后的 onTouch 公共规格 | 取 ArkUI 公共定义时 |
| `examples/onTouch-analysis.md` | 金标准样例（格式与深度基准，含用法代码） | 开始写报告时 |
| `evals/` | 测试用例（onTouch 触摸类、应用级快捷键作用域类等）与预期发现清单 | 报告产出后自检 |
| 外部 | [Agent Skills Spec](https://agentskills.io/specification) · Android `MotionEvent` · iOS `UITouch`/`UIResponder` | 取对标平台规格时 |
