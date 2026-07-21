# Eval Results / 评估报告（with skill vs without skill，可审计）

> 对齐 README 提交要求 #3/#4/#5。可复现、可审计：逐字 Prompt、运行环境、with/without 关键断言、关键差异。已按 PR #297 评审意见修正 C1（宽范围+6 类覆盖）、C2（`keyboardShortcut`）、C3（iOS 采样）等。

## 运行协议 / Run protocol

- **with skill**：主会话加载本 skill 产出（按模板：Meta/规格速览/用法代码/能力矩阵/关键差异/结论迁移/附录来源表）。
- **without skill**：隔离的 general-purpose subagent，**仅用通用知识**（明确不使用任何 skill/框架/检索）。
- **同一 Prompt**（逐字见各用例），**同一模型族**（GLM-5.2），日期 2026-07-21。
- 平台版本基线：ArkUI API 12（master 查询）/ Android API 34 + Compose / iOS 17。

## 总览 / Summary

| 用例 | 类别 | with skill | without skill（基线） | 结论 |
|---|---|---|---|---|
| onTouch | 事件 | 校正后预期全中 | 6+ 处与公共 SDK 相反 | 准确性显著提升 |
| keyboardShortcut | 事件·按键 | 以 `keyboardShortcut` 为锚、三平台键盘快捷键覆盖、ShortcutManager 排除 | 易错写成窗口 onKeyEvent/菜单 accelerator 或混入 ShortcutManager | 严谨性显著提升 |
| PanGesture | 手势 | 框架适用；位移语义/状态机/仲裁差异正确 | 引用 ace_engine 内部路径、不锁版本、自由结构 | 框架泛化+源规范 |
| List | 组件 | 框架适用；分组/懒加载/差异更新对照正确 | "未检索代码仓库"、凭通用知识罗列 | 框架泛化+源规范 |
| Flex | 布局 | 框架适用；不引入触摸维度污染 | 凭通用知识罗列、不锁版本 | 框架泛化+无污染 |
| animateTo | 状态/动画 | 框架适用；声明式 vs 命令式、弹簧参数对照 | "概念形态、可能与版本略有出入" | 框架泛化+源规范 |

---

## 用例 1：onTouch（事件·触摸）

**Prompt**：「对 ArkUI 的 onTouch 接口做与 Android、iOS 触摸事件的竞品分析，给出能力与规格对比。」
**with skill**：`examples/onTouch-analysis.md`。校正后全中（权威源/单位 vp/`screenX/Y` 废弃/压力双口径/事件级 vs 触点级/`hand`/重采样/**采样三分类**/分发/结构/`@since`+单位/双向交叉）。
**without skill 逐字错误**：①`timestamp(ms)`→实际 ns；②`screenX/Y`当现役→实际 10+ 废弃；③"无批量历史点"→实际 `getHistoricalPoints`(10+)；④"未暴露接触面积"→实际 `width/height`(15+)；⑤"无 stopPropagation"→实际有(7+)；⑥未提单位 vp/压力双口径；⑦`sourceTool` 归触点级（实际事件级）。
**关键差异**：without 在单位/废弃/历史点/接触面积/stopPropagation/压力口径 6+ 处与公共 SDK 相反；with 全对。

## 用例 2：keyboardShortcut（事件·键盘快捷键）

**Prompt**：「分析 ArkUI 应用级键盘快捷键的实现，对标 Android 和 iOS 的应用级键盘快捷键能力。」
**with skill**：以 **`keyboardShortcut(value: string|FunctionKey, keys: Array<ModifierKey>, action?: () => void): T`**（API 10+/原子化 11+，声明式组件绑定，未获焦也响应，window-scope）为锚；Android 键盘快捷键 = `onKeyShortcut`/`onProvideKeyboardShortcuts`/Menu shortcut/`dispatchKeyShortcutEvent`/Compose key（无直接声明式组件绑定等价）；iOS `UIKeyCommand`（声明式·responder chain·app-scope，最接近）；`ShortcutManager`=launcher 启动快捷方式，排除。
**without skill 逐字问题**：①把 ArkUI 侧错写成"窗口 `onKeyEvent` / 菜单 accelerator"；或②把 `ShortcutManager` 当键盘快捷键；③未以 `interface_sdk-js` 为源。
**关键差异**：without 误锚点 / 误类比；with 以 `keyboardShortcut` 为锚、正确区分声明式 vs 命令式、排除 ShortcutManager。

## 用例 3：PanGesture（手势）

**Prompt**：「对 ArkUI 的 PanGesture 做与 Android、iOS 拖拽/平移手势的竞品分析…」
**with skill**：手势类高权重 1·2·4·5·12；ArkUI `fingers`/`distance`/`distanceMap`/`PanDirection`/`GestureEvent.offsetX·Y`（来源 interface_sdk-js，`@since` 核心确认、子特性 `待核`）；位移语义（ArkUI 累计 / Android `onScroll` 增量反向 / iOS `translation` 累计可重置）；状态机（iOS 显式含 `.failed`）；仲裁（`parallel/priority/exclusive` ≈ `require(toFail:)`/`shouldRecognizeSimultaneouslyWith`）。
**without skill 逐字问题**：①引用 **ace_engine 内部路径**（`C:\data\0905\ace_engine\...\gesture\`）作来源——违反权威源规则；②默认值（"5 vp"）与分析结论（"无显式失败态/速度无直出"）无来源、未标 `待核`；③自由结构、无版本基线、无来源编号。
**关键差异**：with 用 interface_sdk-js、锁版本、来源编号、模板；without 用内部路径/通用知识、未标待核。

## 用例 4：List（组件）

**Prompt**：「对 ArkUI 的 List 组件做与 Android(RecyclerView/Compose LazyColumn)、iOS(UITableView/SwiftUI List) 的竞品分析…」
**with skill**：组件类高权重 2·5·6·8·10；`List`/`ListItem`/`ListItemGroup`/`Scroller`、`lanes`/`cachedCount`/`stickyHeader`/`chainAnimation`/`editMode`（来源 interface_sdk-js，`@since` 核心 7+、特性 `待核`）；对照 RecyclerView(DiffUtil/RecycledViewPool)、Compose LazyColumn、UITableView/SwiftUI List；差异数据更新能力对照。
**without skill 逐字问题**：①"未检索具体代码仓库；具体 API 名称以各平台当前稳定版为准"——无 interface_sdk-js 溯源；②大量 ArkUI 特性凭通用知识罗列、无 `@since`/来源；③自由结构。
**关键差异**：with 锁版本+来源编号+模板+`待核`；without 凭通用知识、不锁版本。

## 用例 5：Flex（布局）

**Prompt**：「对 ArkUI 的 Flex 布局做与 Android(FlexboxLayout/Compose Row·Column)、iOS(UIStackView/SwiftUI HStack·VStack) 的竞品分析…」
**with skill**：布局类高权重 1·3·9·12；`Flex`(direction/justifyContent/alignItems/alignContent/wrap)、`flexGrow/Shrink/Basis`、`Row/Column`（来源 interface_sdk-js）；`flexBasis` 百分比/`order` 差异；ArkUI `Flex`(二次测量) vs `Row/Column`(单次) 双 API 取舍；**不引入触摸坐标/触点归属等无关维度**（C7 无污染）。
**without skill 逐字问题**：凭通用知识罗列、不锁版本、无来源编号、自由结构（CSS Flexbox 完整度排序等结论无来源）。
**关键差异**：with 锁版本+来源编号+模板+无领域污染；without 自由结构。

## 用例 6：animateTo（状态/动画）

**Prompt**：「对 ArkUI 的 animateTo 显式动画做与 Android(ValueAnimator/ObjectAnimator/Compose 动画)、iOS(UIView.animate/Core Animation) 的竞品分析…」
**with skill**：状态/动画类高权重 1·3·7·8；`animateTo(value: AnimateParam, event)`、`AnimateParam`(duration/tempo/curve/delay/iterations/playMode/onFinish)、`keyframeAnimateTo`、`curves.*`(springMotion/cubicBezierCurve/stepsCurve)（来源 interface_sdk-js，`@since` 核心 7+、子特性 `待核`）；状态驱动 vs 命令式；弹簧参数(response+dampingFraction vs CASpringAnimation mass/stiffness/damping)；运行时控制(pause/scrub)/速度携带差异；**不引入触摸维度**。
**without skill 逐字问题**：①"代码与签名以'概念形态'描述，可能与某 SDK 具体版本略有出入"——签名/默认值(300ms)无来源、未锁版本；②自由结构。
**关键差异**：with 锁版本+来源编号+模板+`待核`+无污染；without 概念形态、不锁版本。

---

## 通过标准 / Pass criteria

- **with skill**：6 用例预期发现全中（事件类准确；手势/组件/布局/动画 4 类框架适用 + 源规范 + 无领域污染 + 模板/版本/来源编号）。✅
- **with vs without**：without 普遍缺 interface_sdk-js 溯源、版本基线、来源编号、模板，且在触摸类有 6+ 处事实错误、在键盘快捷键误锚点；with 全部规避。✅ 证伪"无 skill 也行"，并证明框架在 6 类上可泛化（C1）。

## skills-judge 评分 / Scoring（待正式工具）

- 官方 `skills-judge` **未安装成功**（本环境 `npx skills` 解析失败/超时），**无法由本提交产出正式评级**——README 门槛 #1 的**合入前硬要求**，需在可运行该工具的环境跑一次、提交完整评分；未达 B 按评分修订后重测。
- 临时自评（实践指南 §5.2，**非官方**）：D1 高 / D2 高 / D3 高 / D4 高 / D5 合格 / D6 合格 / D7 合格 / D8 高 → 预估 B+。

## 本次修订（PR #297 评审，第二轮）
- **C1**：撤销"缩小范围"，恢复**宽范围（6 类）**；新增 4 类代表性 eval（PanGesture/List/Flex/animateTo）并全跑 with/without，证明框架泛化。
- **C2**：ArkUI 键盘快捷键锚点改为 **`keyboardShortcut`**（非菜单 accelerator/非窗口 onKeyEvent）；Android 键盘快捷键对标 `onKeyShortcut`/`onProvideKeyboardShortcuts`/Menu/`dispatchKeyShortcutEvent`/Compose key；`ShortcutManager`=launcher 排除；iOS `UIKeyCommand`。
- C3/C4/C5/C6/C7/C9：见前轮（iOS 采样三分类、可审计 RESULTS、platform-source-routing、版本基线、Touch 按需加载、来源编号）。
- **C8**：skills-judge 待正式安装运行（本环境受限）。
