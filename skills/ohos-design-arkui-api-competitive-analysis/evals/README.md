# Evals / 测试用例

本目录提供上库评审所需的 `with skill` / `without skill` 测试用例与通过标准（对齐 `openharmony-skills` README「提交要求」）。

## 用例 / Cases

| 文件 | 类别 | 主题 |
|---|---|---|
| `onTouch.md` | 事件·触摸 | ArkUI onTouch ↔ Android/iOS |
| `app-level-shortcut.md` | 事件·键盘快捷键 | ArkUI `keyboardShortcut` ↔ Android/iOS |
| `gesture-PanGesture.md` | 手势 | ArkUI PanGesture ↔ Android/iOS |
| `component-List.md` | 组件 | ArkUI List ↔ RecyclerView/Compose/UITableView |
| `layout-Flex.md` | 布局 | ArkUI Flex ↔ FlexboxLayout/Compose/UIStackView |
| `animation-animateTo.md` | 状态/动画 | ArkUI animateTo ↔ ObjectAnimator/UIView.animate/Core Animation |

覆盖 6 类，验证框架泛化（C1）。每用例 with/without 对比见 `RESULTS.md`。

## 跑法 / How to run

1. **with skill**：在本 skill 已加载的会话中，输入用例 Prompt，按「预期关键发现」清单逐项核对。
2. **without skill**：在**未加载**本 skill 的新会话中，输入同一 Prompt，记录产出。
3. 对比两者：重点看 ArkUI 侧是否以 `interface_sdk-js` 为源、单位/字段/版本是否准确、结构是否一致。

## 通过标准 / Pass criteria

- with skill：预期清单**全部命中**。
- with vs without：with 明显更准确、更结构化，且避免了 without 的典型错误（px 单位、`force`/`operatingHand`、现役 `screenX/Y`、sourceTool 误归触点级），证伪"无 skill 也行"。

## 上库要求 / Submission

- [ ] with skill 全部通过。
- [ ] 留存 with / without 两份产出（Prompt + 结果对比），按仓库要求附截图。
- [ ] 用 `skills-judge` 评分 ≥ B。
