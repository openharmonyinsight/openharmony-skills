---
name: ohos-design-arkui-api-competitive-analysis
description: This skill should be used when the user asks to "竞品分析 ArkUI 接口", "对标 ArkUI 与 Android/iOS", "compare ArkUI API with Android/iOS", "做接口对标 / capability gap analysis", or mentions competitive analysis of ArkUI UI APIs (事件 touch/key、手势 gesture、组件 component、布局 layout、状态/动画 state/animation). Provides a reusable 12-dimension framework, a no-scope-downgrade rule, a platform-version-baseline rule, an authoritative-source rule (interface_sdk-js) with per-assertion source citations, a bilingual report template with usage code, and a gold-standard onTouch example. Validated across touch, keyboard-shortcut, gesture, component, layout, and animation evals.
metadata:
  version: 1.2.0
---

# ArkUI API Competitive Analysis Skill / ArkUI 接口竞品分析

对 ArkUI 的 UI 接口（事件 / 手势 / 组件 / 布局 / 状态 / 动画）产出**结构一致、规格准确**的对标报告，对标 **Android（Compose/View）** 与 **iOS（SwiftUI/UIKit）**。本 skill 只做"判断与方法"，不实现代码。

核心铁律：**公共接口定义以 `interface_sdk-js` 为唯一权威**，ace_engine 内部定义仅作实现对照。

# Task and Boundaries / 任务与边界

- **Goal**：对指定的 ArkUI 公共 UI 接口，产出对标 Android+iOS 的报告——规格速览 + **用法示例代码** + 能力矩阵 + 关键差异点 + 结论与迁移 + 附录（**带来源编号的来源表**）。
- **Input**：用户指明的 ArkUI 接口（如 `onTouch`、`keyboardShortcut`、`PanGesture`、`List`、`Flex`、`animateTo`）；对标平台（默认 Android+iOS）；可选层级。
- **In scope**：公共 UI API 的能力 / 规格对标（事件 / 手势 / 组件 / 布局 / 状态 / 动画）。
- **Out of scope**：不实现代码、不跑性能基准、不对标 Flutter/Web、不改 ace_engine；不用内部定义作公共结论；不臆造字段/版本。
- **已验证覆盖（evals）**：触摸 `onTouch`、键盘快捷键 `keyboardShortcut`、手势 `PanGesture`、组件 `List`、布局 `Flex`、动画 `animateTo`。

# Trigger Signals / 触发信号

- "竞品分析 / 对标 ArkUI 接口"、"compare ArkUI API with Android/iOS"、"API 能力差异 / gap analysis"。
- 设计或评审 ArkUI 接口前，参考 Android/iOS 同类能力。
- 迁移评估（Android/iOS ↔ ArkUI）。

# Initial Checks / 初始检查（按序）

1. **明确分析对象**：哪个 ArkUI 接口？对标平台？层级？
2. **锁定作用域层级（勿降级）**：带层级能力（"应用级"键盘快捷键、"组件级"触摸）按 `references/analysis-dimensions.md`「作用域层级」锁定到指定层，对标接口也只取该层。
3. **锁定平台版本基线**：记录 **ArkUI API/SDK Version（或分支）**、**Android API Level + Compose 版本**、**iOS/iPadOS 版本**、**资料查询日期**；未指定选当前稳定版并显式记录；不得混用未发布 ArkUI API 与不同平台版本。
4. **判定接口类别**（事件 / 手势 / 组件 / 布局 / 状态 / 动画）→ 用 `references/analysis-dimensions.md` 权重表裁剪维度。
5. 准备取 ArkUI 公共定义。

# Execution Strategy / 执行策略

1. **取 ArkUI 公共规格（权威源 = `interface_sdk-js`）**。规则见 `references/authoritative-sources.md`。**记录要求**：`@since` **必须**记录；单位 / 取值范围 / 默认值 / 归属 **仅在适用时记录**（避免把触摸的"单位 / 触点归属"硬套到不适用字段，如布局/动画）。禁止用 ace_engine 内部定义。
2. **确定对标接口**：按 `references/platform-source-routing.md` 取 Android（优先 Compose，必要时 View）与 iOS（优先 SwiftUI，必要时 UIKit）**同口径、同版本**接口。
3. **按需加载专项规格**：识别为触摸 / 指针输入时，才读 `references/input-event-spec.md`（ArkUI onTouch 校准规格）；通用流程不预载 Touch 规格，避免领域污染。
4. **套维度**（裁剪后）逐维对比，写能力矩阵。
5. **来源引用**：规格速览 / 能力矩阵 / 关键差异 / 迁移结论中**每项实质性断言**关联来源编号 `[n]`；来源表记录 平台、API/符号、官方 URL 或仓库路径、目标版本 / availability、查询日期、章节。区分官方证据 vs 推论；"缺失 / 独有 / 优于"须**双向检索**；无来源支撑标"待核"，不入确定性结论。
6. **出报告**：套 `examples/onTouch-analysis.md` 结构。格式要点：① 每平台规格结构化列表 / 代码块；② 每平台 1 段最小用法示例代码；③ 锁定层级则显式围绕该层；④ 断言带来源编号。
7. **校验**：过 `evals/` 相关用例预期发现 + Prohibited Practices。

# Prohibited Practices / 禁止做法

- 用 **ace_engine 内部 `.d.ts` / C++** 作公共能力结论（`force`/`operatingHand`、px 单位、现役 `screenX/Y`）。
- **把 Android `ShortcutManager` 当键盘快捷键**（它是 launcher 启动快捷方式）。ArkUI 键盘快捷键是 `keyboardShortcut`（声明式组件绑定），**不是**菜单 accelerator / 窗口 `onKeyEvent`。
- **称 iOS"无原生批量触摸采样"**（UIKit 有 `coalescedTouches`/`predictedTouches`；须区分 historical/coalesced/predicted）。
- 把用户指定的**作用域层级降级**。
- 不标 `@since` / 来源就下"支持 / 缺失 / 独有 / 优于"结论。
- 把**事件级**字段误归**触点级**；把触摸分析模式迁移到布局/动画等不适用领域。
- 用**未发布 ArkUI API** 或**混用不同平台版本**作对比。

# Exceptions and Fallbacks / 异常与兜底

- gitcode `oh-gc search code` 不可用 → raw `.d.ts` / `docs.openharmony.cn`。
- 某平台无对应接口 → `N/A` + 等价替代与差异。
- 字段公共性 / `@since` 存疑 → 标"待核"，不臆断。

# References / 参考文档（何时读取）

| 文档 / Doc | 用途 / Purpose | 何时读取 / When to read |
|---|---|---|
| `references/analysis-dimensions.md` | 12 维框架 + 维度权重裁剪 + 作用域层级 | 判定类别后、展开维度前；锁定层级时 |
| `references/authoritative-sources.md` | `interface_sdk-js` 取数规则 + 版本基线 + 来源引用格式 | 取 ArkUI 公共定义时 |
| `references/platform-source-routing.md` | Android/iOS 官方资料入口 + 证据优先级 + 交叉检索 | 取对标接口时 |
| `references/input-event-spec.md` | ArkUI onTouch 校准规格（触摸 / 指针专项） | **仅**触摸 / 指针输入时按需加载 |
| `examples/onTouch-analysis.md` | 金标准样例（含用法代码与来源编号） | 开始写报告时 |
| `evals/` | 用例（onTouch / keyboardShortcut / PanGesture / List / Flex / animateTo）+ `RESULTS.md` | 报告产出后自检 |
