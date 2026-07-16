# Eval Results / 评估报告（with skill vs without skill）

> 对齐 `openharmony-skills` README 提交要求 #3（with/without 对比）、#4（证明提升）、#5（含用例结果、通过情况、关键差异）。

## 总览 / Summary

| 用例 / Case | with skill | without skill（基线） | 结论 / Verdict |
|---|---|---|---|
| onTouch 触摸事件对标 | 12/12 预期发现全中 | 6+ 处与公共 SDK 相反的结论 | skill 显著提升准确性 |
| 应用级快捷键对标 | 作用域锁定、无臆造、三平台应用级覆盖 | 范围基本对，但**臆造** ArkUI API | skill 显著提升严谨性 |

---

## 用例 1：onTouch

- **Prompt**：「对 ArkUI 的 onTouch 接口做与 Android、iOS 触摸事件的竞品分析，给出能力与规格对比。」
- **with skill 产出**：`examples/onTouch-analysis.md`（金标准）。预期发现核对 **12/12 通过**：权威源 interface_sdk-js / 坐标单位 vp / `screenX/Y` 废弃 / 压力双口径 / 事件级 vs 触点级 / `hand`(InteractionHand) / `changedTouches·touches` 重采样 / `getHistoricalPoints` / 分发(冒泡+stopPropagation+Responder Chain) / 六段结构 / `@since`+单位标注 / 双向交叉验证。
- **without skill（隔离 subagent，纯通用知识）关键错误**：
  1. 时间戳写成 `timestamp (ms)` → 实际 **ns**（`BaseEvent.timestamp` 8+）。
  2. `screenX/screenY` 当作现役"屏幕坐标" → 实际 **API 10 起废弃**，应用 `windowX/Y`。
  3. 称 ArkUI **无批量历史点** → 实际有 `getHistoricalPoints()`（10+）。
  4. 称 ArkUI **未暴露接触面积** → 实际有 `width/height`（15+, vp）。
  5. 称 ArkUI **无显式 stopPropagation** → 实际 `TouchEvent.stopPropagation()`（7+）存在。
  6. **未提坐标单位 vp**（高频迁移坑）；**未提压力双口径**（事件级 [0,1] vs 触点级 [0,65535)）。
  7. `sourceTool`/`tiltX` 归到触点级 `TouchObject`（实际事件级 `BaseEvent`）。
  8. 未以 `interface_sdk-js` 为源，自述"未实时检索最新文档"。
- **关键差异 / Key diff**：without skill 在"单位 / 废弃 / 历史点 / 接触面积 / stopPropagation / 压力口径"6+ 处给出**与公共 SDK 相反**的结论（正是用 ace_engine 内部定义或记忆会犯的错）；with skill 全部正确。直接证明「权威源规则」的价值。

## 用例 2：应用级快捷键

- **Prompt**：「分析 ArkUI 应用级快捷键的实现，对标 Android 和 iOS 的应用级快捷键能力。」
- **with skill 产出**：`evals/runs/with-skill-app-level-shortcut.md`。作用域**锁定应用级**（未降级）；ArkUI = 窗口级 `UIContext.onKeyEvent` 命令式 + `MenuItem.labelInfo`（仅提示）+ `inputConsumer`（系统应用 only）；iOS `UIKeyCommand`；Android menu accelerator / `onKeyShortcut`。ArkUI 不确定 API 标 `待核`，**无臆造**。
- **without skill（隔离 subagent）关键问题**：
  1. **臆造 ArkUI 声明式 API** `bindShortcutKey("Ctrl+S", ...)` 与"UIContext 全局注册"——无权威源证实，属幻觉。
  2. 未以 `interface_sdk-js` 为源，自述"未实时检索最新文档，API 名以官方为准"。
  3. 范围判断本身尚可（覆盖了应用级、`UIKeyCommand`、`Ctrl+/` 助手），但 ArkUI 侧 API 靠猜。
- **关键差异 / Key diff**：without skill 在 ArkUI 侧**臆造 API**；with skill **标注待核、不臆造**，并点明 ArkUI 应用级为命令式、与 iOS 声明式 `UIKeyCommand` 的心智差异。证明「权威源规则 + 作用域锁定」的价值。

---

## 通过标准 / Pass criteria

- **with skill**：两用例预期发现全中（onTouch 12/12；应用级快捷键：作用域锁定 + 无臆造 + 三平台应用级覆盖）。✅
- **with vs without**：without 在 onTouch 6+ 处错误、在快捷键臆造 API；with 全部规避。✅ 证伪"无 skill 也行"。

## 原始产物 / Artifacts

- with skill onTouch：`examples/onTouch-analysis.md`
- with skill 应用级快捷键：关键产出见上方「用例 2」（不单独存档，保持 `evals/` 精简、贴合仓库惯例）。
- without skill 原始记录：隔离 subagent 产出，本报告摘录其关键错误作为证据；完整记录随 MR 附上。

## skills-judge 评分 / Scoring

- 官方 `skills-judge` 当前**未在本机/本仓安装**（仓库 skills/ 与本地仅有 `skill-creator`），需获取该工具后运行以得到正式评级。
- **临时自评（按实践指南 §5.2 维度，非官方）**：D1 知识价值 高 / D2 思维模型 高 / D3 反模式 高 / D4 规范契合 高 / D5 渐进披露 合格 / D6 可读度 合格 / D7 模式契合 合格 / D8 实用可用 高 → 预估 **B+**（D1/D4/D8 达"高"，无单项严重缺陷）。正式评级以 `skills-judge` 实跑为准。
