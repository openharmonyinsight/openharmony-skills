# ArkUI 焦点管理 验证规格

> 基于 spec.md 和 design.md 派生。spec.md 已描述的正常流程、异常规则、错误码不在此重复，
> 仅补充集成/系统验证视角的增量场景。场景必须关联 spec.md AC 编号，保持追溯链完整。

## 概述

| 属性     | 值              |
| -------- | --------------- |
| 关联 AC  | AC-1.1 ~ AC-3.2 |
| 验证层级 | L2/L3           |

标签: `smoke` `regression` `api`

## 场景

> 每个场景的 Given / When 须是可操作的用户 / 业务动作序列（优先从 proposal「用户场景与业务触发」
> 与 spec AC 派生），Then 须是可观测结果——保证能直接翻译成测试步骤与检查点。
> 场景确属系统 / 服务内部行为时，标"系统视角"并补上触发它的上层用户 / 业务动作。

### SC-1: 终端用户 Tab 遍历触发获焦/失焦回调

标签: `happy-path`

* Given 开发者已对自定义按钮声明 `focusable(true)` 并注册 `onFocus`/`onBlur`
* When 终端用户按 Tab 遍历到该按钮，随后继续按 Tab 将焦点移走
* Then 按钮获焦时 `onFocus(focusSource=Tab)` 触发、可据此高亮；焦点移走时 `onBlur(target=下一组件)` 触发、高亮取消
* 关联: proposal.md US-1 / spec.md AC-1.1~1.3

---

### SC-2: 编程式 requestFocus 切换焦点（成功与不可焦点回落）

标签: `api`

* Given 开发者已挂载目标组件并声明 `focusable(true)`，当前焦点在原组件
* When 开发者调用 `目标组件.requestFocus()`
* Then 目标可焦点且已挂载时收 `onFocus`、原组件收 `onBlur`，`requestFocus` 返回 `true`；目标不可焦点或已卸载时返回 `false` 且焦点不变
* 关联: proposal.md US-2 / spec.md AC-2.1~2.3

---

### SC-3: 持焦组件卸载时自动清理并转移焦点（系统视角）

标签: `regression`

> 系统视角：焦点管理器内部行为。上层触发 = 终端用户导航离开页面，或组件被条件渲染移除导致 `onDisappear`（见 proposal US-3）。

* Given 某组件持有焦点、且焦点链中存在其他可焦点组件
* When 持焦组件因页面导航离开或条件渲染移除而触发 `onDisappear`
* Then 焦点管理器从注册表移除该节点，并将焦点转移到焦点链下一个可焦点组件（无则置空），不残留悬空焦点
* 关联: proposal.md US-3 / spec.md AC-3.1~3.2
