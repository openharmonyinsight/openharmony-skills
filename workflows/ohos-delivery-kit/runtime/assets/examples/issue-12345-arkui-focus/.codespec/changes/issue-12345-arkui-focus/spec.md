# Spec

## 概述

| 属性 | 值 |
|------|-----|
| 特性名称 | ArkUI 焦点管理 |
| 特性编号 | FEAT-ARKUI-FOCUS-001 |
| 优先级 | P0 |
| 复杂度 | 标准（引用 proposal.md 分级判断结果） |
| 目标版本 | 6.0 |

## 用户故事或场景

### US-1: 焦点获取通知

**作为** ArkUI 开发者，**我想要** 在自定义组件获得焦点时收到通知，**以便** 更新 UI 状态以反映焦点变化。

**验收标准：**

> 使用 Given/When/Then 格式。Given 前置条件；When 用户/业务可操作动作；Then 通过三层接口边界可观测的结果（public/system/inner API 返回值/回调/错误码，或终端用户可感知）。Then 禁内部实现（注册表/状态机/焦点链遍历）——移 design.md「状态归属与不变量」。
- **AC-1.1:** Given 组件声明 `focusable(true)` 并挂载 When 终端用户按 Tab/点击，或开发者调 `requestFocus()` Then 该组件可获焦，获焦时触发 `onFocus` 回调（见 AC-1.2）
- **AC-1.2:** Given 组件声明 `focusable(true)` 并挂载 When 终端用户按 Tab/点击，或开发者调 `requestFocus()` Then 组件收 `onFocus(focusSource=Tab/Click/Programmatic)` 回调
- **AC-1.3:** Given 组件持有焦点 When 焦点转移到其他组件 Then 原组件收 `onBlur(focusTarget=下一组件 ID)` 回调

### US-2: 编程式焦点切换

**作为** ArkUI 开发者，**我想要** 通过代码控制焦点在组件间切换，**以便** 实现自定义焦点导航逻辑。

**验收标准：**

- **AC-2.1:** Given 目标组件已挂载且 `focusable=true` When 开发者调 `component.requestFocus()` Then 焦点切到目标，目标收 `onFocus`、原组件收 `onBlur`，返回 true
- **AC-2.2:** Given 目标组件不可焦点或已卸载 When 开发者调 `component.requestFocus()` Then 返回 false，焦点不变，不抛异常
- **AC-2.3:** Given 当前无可焦点组件 When 开发者调 `requestFocus()` Then 返回 false，不抛异常

### US-3: 焦点生命周期管理

**作为** 框架开发者，**我想要** 焦点系统在组件卸载时自动清理焦点，**以便** 防止悬空引用和焦点泄漏。

**验收标准：**

- **AC-3.1:** Given 持有焦点的组件被卸载 When 组件触发卸载（终端用户导航离开或条件渲染移除） Then 焦点转移到焦点链下一个可焦点组件（该组件收 `onFocus`）；无可焦点组件则无焦点（卸载前 `onBlur` 触发）
- **AC-3.2:** Given 组件在 `onBlur` 回调中 When 组件调 `requestFocus` 请求焦点回到自身 Then 该请求被忽略（防止焦点循环），记录 WARN 日志

## 业务规则

| 规则 ID | 规则描述 | 约束条件 | 关联 AC |
|---------|----------|----------|---------|
| BR-001 | 同一时刻最多一个组件持有焦点 | 焦点管理器维护唯一 `currentFocusNode` 指针 | AC-1.1, AC-2.1 |
| BR-002 | 组件卸载时自动从焦点注册表移除 | 在组件 onDisappear 生命周期中触发注销 | AC-3.1 |
| BR-003 | focusable 声明为组件级属性，不可继承 | 父组件 focusable=true 不影响子组件焦点参与 | AC-1.1 |
| BR-004 | 焦点切换不触发组件重建 | 仅触发 onFocus/onBlur 回调，不触发 build/render | AC-1.2, AC-1.3 |

## 异常与边界规则

> 超时操作必须给出精确阈值（ms/s），不可写"待定义"。跨进程字段必须给出精确限制（字节数/长度）。

| 编号 | 场景 | 触发条件 | 系统行为 | 关联 AC |
|------|------|----------|----------|---------|
| EX-001 | 无可焦点组件 | 焦点注册表为空时调用 requestFocus | 返回 false，不抛异常 | AC-2.3 |
| EX-002 | 焦点循环防护 | 组件在 onBlur 回调中调用 requestFocus 请求焦点回到自身 | 忽略请求，记录 WARN 日志 | AC-3.2 |
| EX-003 | 已卸载组件调用 | 组件卸载后仍持有引用并调用 requestFocus | 返回 false，不抛异常 | AC-2.2 |
| EX-004 | 焦点链断裂 | 持有焦点的组件卸载且无下一个可焦点组件 | 焦点置空，currentFocusNode=nullptr | AC-3.1 |

## 错误码定义

> 每个错误码必须给出精确的数值和含义。避免"返回错误"这种模糊描述——要写明错误类型、错误消息和触发条件。

| 错误码 ID | 错误码值 | 含义 | 关联 AC |
|-----------|----------|------|---------|
| ERR_FOCUS_NOT_FOCUSABLE | 0x80000001 | 目标组件未声明 focusable(true)，不可获得焦点 | AC-2.2 |
| ERR_FOCUS_ALREADY_DETACHED | 0x80000002 | 目标组件已从组件树卸载，焦点操作无效 | AC-2.2, EX-003 |

## 接口变更分析

### 新增接口

| 接口名称 | 开放级别 | 参数概要 | 返回值 | 错误码 | 关联 AC |
|----------|----------|----------|--------|--------|---------|
| focusable(enabled: boolean) | Public | enabled: 是否参与焦点管理 | void | — | AC-1.1 |
| onFocus(callback: (source: FocusSource) => void) | Public | callback: 焦点获取回调，FocusSource 枚举 | void | — | AC-1.2 |
| onBlur(callback: (target: string) => void) | Public | callback: 焦点失去回调，target 为焦点去向组件 ID | void | — | AC-1.3 |
| requestFocus(): boolean | Public | 无 | boolean（成功/失败） | ERR_FOCUS_NOT_FOCUSABLE, ERR_FOCUS_ALREADY_DETACHED | AC-2.1, AC-2.2 |

### 变更/废弃接口

| 接口名称 | 开放级别 | 变更类型 | 影响场景 | 迁移指引 | 关联 AC |
|----------|----------|----------|----------|----------|---------|

## 兼容性声明

- **已有 API 行为变更:** 否（纯增量 API，现有组件默认不参与焦点管理）
- **配置文件格式变更:** 否
- **数据存储格式变更:** 否

## 验证映射

| AC | 关联规则 | 验证方式 | 证据 |
|----|----------|----------|------|
| AC-1.1 | BR-001, BR-003 | 单元测试：验证 focusable(true) 组件注册到焦点节点表 | |
| AC-1.2 | BR-004 | 集成测试：验证 onFocus 回调触发时机和 FocusSource 参数正确性 | |
| AC-1.3 | BR-004 | 集成测试：验证 onBlur 回调触发时机和 target 参数正确性 | |
| AC-2.1 | BR-001 | 集成测试：端到端 requestFocus → 焦点切换 → 双回调触发 | |
| AC-2.2 | ERR_FOCUS_NOT_FOCUSABLE | 单元测试：不可焦点目标 requestFocus 返回 false | |
| AC-2.3 | EX-001 | 单元测试：空注册表 requestFocus 返回 false | |
| AC-3.1 | BR-002, EX-004 | 集成测试：模拟组件卸载，验证焦点转移和注册清理 | |
| AC-3.2 | EX-002 | 单元测试：onBlur 中 requestFocus 自身被忽略 + WARN 日志 | |

## 测试设计提示

> 面向 AI 生成测试和实现计划。每条 AC 至少给出一个测试入口；`Red 条件` 必须说明实现前为什么会失败，避免写出立即通过的无效测试。

| AC | 测试类型 | 测试文件 | 测试名称 | 输入/触发 | 期望输出/错误 | Red 条件 |
|----|----------|----------|----------|-----------|---------------|----------|
| AC-1.1 | 单元测试 | frameworks/arkui/component/focus/focus_manager_test.cpp | RegisterFocusableNode | focusable(true) + onAppear | 注册表包含 componentId | FocusManager/FocusNode 文件尚不存在 |
| AC-1.2 | 集成测试 | frameworks/arkui/component/focus/focus_manager_test.cpp | DispatchOnFocusCallback | requestFocus 到目标组件 | onFocus 收到 Programmatic 来源 | onFocus 回调未接入 |
| AC-1.3 | 集成测试 | frameworks/arkui/component/focus/focus_manager_test.cpp | DispatchOnBlurCallback | A 切换到 B | A.onBlur 收到 B 的 componentId | onBlur 回调未接入 |
| AC-2.1 | 集成测试 | frameworks/arkui/component/focus/focus_manager_test.cpp | RequestFocusValidTarget | 已挂载且 focusable=true 的目标 | 返回 true，焦点切换完成 | requestFocus 方法尚不存在 |
| AC-2.2 | 单元测试 | frameworks/arkui/component/focus/focus_manager_test.cpp | RequestFocusInvalidTarget | 未 focusable 或已卸载目标 | 返回 false，不抛异常 | 异常路径未实现 |
| AC-2.3 | 单元测试 | frameworks/arkui/component/focus/focus_manager_test.cpp | RequestFocusEmptyRegistry | 空注册表调用 requestFocus | 返回 false，不抛异常 | 空注册表保护未实现 |
| AC-3.1 | 集成测试 | frameworks/arkui/component/focus/focus_manager_test.cpp | DetachCurrentFocusNode | 持焦点组件 onDisappear | 注册清理，焦点转移或置空 | onDisappear 未接入清理 |
| AC-3.2 | 单元测试 | frameworks/arkui/component/focus/focus_manager_test.cpp | RejectReentrantRequestFocus | onBlur 中 requestFocus 自身 | 返回 false，WARN 日志 | 重入保护标志不存在 |

> AC → 实现文件 + Task + 验证状态的映射见 `execution-plan.md`「AC 到 Task 追溯」+「代码范围映射」。
