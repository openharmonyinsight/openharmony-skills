# Eval Results / 评估报告（with skill vs without skill，可审计）

> 对齐 `openharmony-skills` README 提交要求 #3/#4/#5。本报告为可复现、可审计的结构化报告：含**逐字 Prompt、运行环境、with/without 的逐字关键断言**与关键差异。已按 PR #297 评审意见修正 C2（ShortcutManager）与 C3（iOS 采样）。

## 运行协议 / Run protocol（保证可比性）

- **with skill**：主会话加载本 skill 产出。
- **without skill**：隔离的 general-purpose subagent，**仅用通用知识**（明确要求不使用任何 skill / 框架 / 检索），产出基线。
- **同一 Prompt**（逐字见各用例），**同一模型族**（GLM-5.2），日期 2026-07-21。
- 平台版本基线：ArkUI API 12（master）/ Android API 34 + Compose / iOS 17。

## 总览 / Summary

| 用例 | with skill | without skill（基线） | 结论 |
|---|---|---|---|
| onTouch 触摸事件 | 校正后预期发现全中 | 6+ 处与公共 SDK 相反的断言 | skill 显著提升准确性 |
| 应用级快捷键 | 作用域锁定、无臆造、Android 键盘快捷键对标正确 | 范围基本对但**臆造** ArkUI API | skill 显著提升严谨性 |

---

## 用例 1：onTouch

**Prompt（逐字，with/without 相同）**：
> 对 ArkUI 的 onTouch 接口做与 Android、iOS 触摸事件的竞品分析，给出能力与规格对比。

**with skill 产出**：`examples/onTouch-analysis.md`。校正后预期发现全中：权威源 interface_sdk-js / 坐标单位 vp / `screenX/Y` 废弃 / 压力双口径 / 事件级 vs 触点级 / `hand`(InteractionHand) / `changedTouches·touches` 重采样 / 采样三分类（historical/coalesced/predicted，**不再**称 iOS 无原生批量）/ 分发 / 六段结构 / `@since`+单位 / 双向交叉验证。

**without skill 逐字错误断言**（来自基线 subagent 输出）：
1. `时间戳 timestamp（ms）` → 实际 **ns**（`BaseEvent.timestamp` 8+）。
2. `相对屏幕坐标 screenX, screenY`（当现役）→ 实际 **API 10 起废弃**，应用 `windowX/Y`。
3. `历史采样点 —（无批量历史点）` → 实际有 `getHistoricalPoints()`(10+)。
4. `接触面积 —（未暴露）` → 实际有 `width/height`(15+, vp)。
5. `取消/阻止传递 无显式 stopPropagation` → 实际 `TouchEvent.stopPropagation()`(7+) 存在。
6. 未提坐标单位 **vp**（迁移坑）；未提压力双口径。
7. `sourceTool` 归到触点级（实际事件级 BaseEvent）。

**关键差异**：without skill 在单位/废弃/历史点/接触面积/stopPropagation/压力口径 6+ 处给出**与公共 SDK 相反**结论（正是用 ace_engine 内部定义或记忆会犯的错）；with skill 全部正确。证明「权威源规则」价值。

---

## 用例 2：应用级快捷键

**Prompt（逐字，with/without 相同）**：
> 分析 ArkUI 应用级快捷键的实现，对标 Android 和 iOS 的应用级快捷键能力。

**with skill 产出**：作用域**锁定应用级**；ArkUI = 窗口级 `UIContext.onKeyEvent` 命令式 + `MenuItem.labelInfo`（仅提示）+ `inputConsumer`（系统应用 only）；**Android 键盘快捷键** = `Activity.onKeyShortcut`/`onProvideKeyboardShortcuts`/Menu keyboard shortcuts/`dispatchKeyShortcutEvent`/Compose key input（**ShortcutManager 不作键盘快捷键对标**）；iOS `UIKeyCommand`。ArkUI 不确定 API 标 `待核`，**无臆造**。

**without skill 逐字问题断言**（来自基线 subagent 输出）：
1. 臆造 ArkUI 声明式 API：`Text("保存").bindShortcutKey("Ctrl+S", () => { ... })`、`应用级/全局注册：通过 UIContext 提供的快捷键管理能力`——无权威源证实，属幻觉。
2. 未以 `interface_sdk-js` 为源，自述"未实时检索最新文档"。
3. 范围判断本身尚可（覆盖应用级、`UIKeyCommand`、`Ctrl+/` 助手），但 ArkUI 侧 API 靠猜。

**关键差异**：without skill 在 ArkUI 侧**臆造 API**；with skill **标注待核、不臆造**，并正确区分 Android 键盘快捷键 vs `ShortcutManager`（启动快捷方式）。证明「权威源规则 + 作用域锁定 + 平台资料路线」价值。

---

## 通过标准 / Pass criteria

- **with skill**：两用例预期发现全中（onTouch 校正后清单；应用级快捷键：作用域锁定 + 无臆造 + 三平台应用级覆盖 + Android 键盘快捷键对标正确）。✅
- **with vs without**：without 在 onTouch 6+ 处错误、在快捷键臆造 API；with 全部规避。✅ 证伪"无 skill 也行"。

## 原始产物 / Artifacts

- with skill onTouch：`examples/onTouch-analysis.md`（含逐字段校准规格与来源编号表）。
- with skill 应用级快捷键：关键产出见上方「用例 2」逐字断言；逐字 Prompt 与运行环境见本报告「运行协议」，评审可据此复跑。
- without skill 原始记录：隔离 subagent 产出，本报告**逐字摘录**其关键错误/臆造断言作为证据（同 Prompt、同模型、注明环境），可审计。

## skills-judge 评分 / Scoring（待正式工具）

- 官方 `skills-judge` 当前**未在本机/本仓安装**，**无法由本提交产出正式评级**——这是 README 提交门槛 #1 的**合入前硬要求**，需在评审阶段获取并运行该工具、提交完整评分；若未达 B，按评分修订后重测。
- 临时自评（按实践指南 §5.2 维度，**非官方**）：D1 高 / D2 高 / D3 高 / D4 高 / D5 合格 / D6 合格 / D7 合格 / D8 高 → 预估 B+。正式评级以 `skills-judge` 实跑为准。

## 本次修订（按 PR #297 评审）
- C3：纠正 iOS"无原生批量"→ 区分 historical/coalesced/predicted（`coalescedTouches`/`predictedTouches`）。已改 example/`input-event-spec.md`/`analysis-dimensions.md` dim7/`onTouch.md`。
- C2：`ShortcutManager`≠键盘快捷键（=launcher 启动快捷方式）；键盘对标 `onKeyShortcut`/`onProvideKeyboardShortcuts`/Menu/`dispatchKeyShortcutEvent`/Compose key。已改 `analysis-dimensions.md` 作用域表/`app-level-shortcut.md`/本报告。
- C1：缩小声明范围到输入/交互事件类（SKILL.md）。C7：Touch 专项规格拆到 `input-event-spec.md`（按需加载）；通用规则 `@since` 必记、单位/范围/默认值仅适用时记。C6：Initial Checks 锁定平台版本基线。C9：来源编号+来源表（含版本/availability/日期/章节）。C5：新增 `platform-source-routing.md`。
