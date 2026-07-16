# Analysis Dimensions / 竞品分析维度框架

UI 接口竞品分析的 **4 组 / 12 维**。每维给：**Definition**（定义）/ **What to look for**（要找什么）/ **How to check**（怎么查）。先用「维度权重裁剪表」按接口类别选出高权重维度，避免全量堆砌。

## 维度权重裁剪表 / Weight by API category（先看这张）

| API 类别 / Category | 高权重维度 / High | 低权重维度 / Low |
|---|---|---|
| 事件类 events（onTouch / onHover / onClick） | 2 · 3 · 4 · 5 · 7 · 11 | 8 · 10 |
| 手势类 gestures（Tap / Pan / Pinch / Rotation） | 1 · 2 · 4 · 5 · 12 | 3（单位） |
| 组件类 components（List / Dialog / Picker） | 2 · 5 · 6 · 8 · 10 | 4 · 7 |
| 布局类 layout（Flex / Grid / Stack） | 1 · 3 · 9 · 12 | 4 · 5 · 6 |
| 状态 / 动画类 state / animation | 1 · 3 · 7 · 8 | 4 · 5 |

> 用法：判定接口类别后，只展开高权重维度；低权重维度仅在用户明确关心时展开。报告里**不必 12 维全填**。接口不属于以上类别时，按通用维度全展开并说明。

## Capability Scope Tiers / 作用域层级（勿降级）

某些能力天然分作用域层级。**用户指明某一层时，只分析该层，不得降级**成通用或其它层级。常见带层级的能力：

| 能力 / Capability | 典型层级 / Typical tiers |
|---|---|
| 快捷键 / Shortcut | 应用级（app 内全局）/ 组件级（单组件按键）/ 系统级（OS 全局热键） |
| 触摸 / Touch | 组件级 / 窗口或全局 hit-test |
| 拖拽 / Drag | 组件级 / app 级 / 跨窗口 |
| 焦点 / Focus | 组件级 / app 级 |

> 例：用户说"应用级快捷键"时，只覆盖应用级（如 iOS `UIKeyCommand`、Android `ShortcutManager`/菜单 accelerator、ArkUI 窗口或菜单级），不要降级成组件级 key event。具体 API 名以 `interface_sdk-js` 与各平台官方文档为准（勿臆造）；某平台确无原生实现时明确标注并给最接近替代。

---

## A. Capability & Spec / 能力与规格（最核心）

### 1. API Shape & Signature / API 形态与签名
- **Definition**：接口的命名、参数风格、声明式 vs 命令式、Builder/Modifier/链式、类型表达力（可选 / 联合 / 字面量类型）。
- **What to look for**：方法/属性命名是否一致；回调签名；泛型与可选参数；声明式与命令式是否同步（ArkUI 的 static `.static.d.ets` vs dynamic `.d.ts`）。
- **How to check**：ArkUI 取 `interface_sdk-js`；Android 看 Compose `@Composable`/Modifier vs View 方法；iOS 看 SwiftUI view modifier vs UIKit 方法。

### 2. Capability Coverage / 能力覆盖
- **Definition**：功能点是否齐全；缺失 / 独有能力；子能力枚举（事件阶段、坐标空间、手势类型）。
- **What to look for**：某能力三平台是否都有；ArkUI 独有（如多坐标空间、左右手 `hand`）；他平台独有（如 iOS `stationary` 相位）。
- **How to check**：列出接口的子能力清单逐项打勾；缺失/独有须**双向交叉验证**（不是只看一方文档）。

### 3. Spec Precision / 规格精度
- **Definition**：单位（px / vp / dp / pt）、取值范围、默认值、枚举值、空值 / undefined 语义、`@since` 版本、废弃标记。
- **What to look for**：**单位口径**（ArkUI 触摸坐标 = vp，Android = px，iOS = pt —— 高频迁移坑）；取值范围与钳制；默认值；`@since` 版本；已废弃字段。
- **How to check**：`interface_sdk-js` / 官方文档逐字段核单位与范围；废弃字段看 `@deprecated`（如 ArkUI `screenX/Y` 自 10 起废弃）。

---

## B. Input & Interaction / 输入与交互

### 4. Multi-Input Source / 多输入源适配
- **Definition**：手指 / 笔 / 鼠标 / 触控板 / 手柄 / 键盘支持；折叠屏；多屏多设备。
- **What to look for**：`sourceType` / `sourceTool` / `toolType` / `type` 枚举覆盖；手写笔姿态（`tiltX/Y`、`rollAngle`、`altitudeAngle`）；多屏坐标（`displayX/Y`、`globalDisplayX/Y`、`targetDisplayId`）。
- **How to check**：枚举成员逐项比对；笔姿态字段名/口径跨平台对照。

### 5. Dispatch & Interaction Model / 分发与交互模型
- **Definition**：冒泡 / 拦截 / 命中测试（hit-test）、手势仲裁、父子竞争、优先级。
- **What to look for**：事件默认是否冒泡；阻止冒泡的 API（ArkUI `stopPropagation`、Android `onInterceptTouchEvent`、iOS Responder Chain）；手势优先级模型（ArkUI `priorityGesture/parallelGesture` ≈ SwiftUI `simultaneousGesture/highPriorityGesture`）。
- **How to check**：查分发流程文档；列阻止冒泡/拦截的等价 API。

### 6. Accessibility / 可访问性
- **Definition**：屏幕阅读、语义属性、焦点管理、无障碍兜底。
- **What to look for**：语义化属性（`accessibilityText`/`accessibilityRole`）；焦点可达性；触摸目标尺寸兜底。
- **How to check**：查各平台无障碍 API（ArkUI accessibility 属性、Android `AccessibilityNodeInfo`、iOS `UIAccessibility`）。

---

## C. Performance & Engineering / 性能与工程

### 7. Performance & Overhead / 性能与开销
- **Definition**：分发频率、合批 / 历史点、节流、线程模型、是否阻塞 UI。
- **What to look for**：历史点批处理（ArkUI `getHistoricalPoints`、Android `getHistorySize`、iOS 无原生批量）；`changedTouches`/`touches` 重采样口径差异（ArkUI 独有行为）；高频事件节流。
- **How to check**：查事件批处理/历史点 API；不跑实测（本 skill 不做基准）。

### 8. State & Lifecycle / 状态与生命周期
- **Definition**：事件 / 接口与组件生命周期、回调时机、副作用。
- **What to look for**：回调触发时机与幂等性；组件销毁后是否还回调；状态绑定刷新时机。
- **How to check**：查生命周期文档与回调时序。

### 9. Cross-Platform Consistency / 跨端一致性
- **Definition**：手机 / 平板 / 穿戴 / 桌面 / 车机行为是否统一。
- **What to look for**：同一接口在不同设备形态上的能力差异；设备专属字段（如穿戴 Crown）。
- **How to check**：查设备形态约束与 `SystemCapability`。

---

## D. Evolution & Ecosystem / 演进与生态

### 10. Versioning & Compatibility / 版本演进与兼容
- **Definition**：废弃策略、增量能力、迁移路径、向前 / 向后兼容。
- **What to look for**：`@deprecated` / `@obsoleted`；版本演进带来的破坏性变更；迁移替代 API。
- **How to check**：`@since` / `@deprecated` 标记；release notes。

### 11. Ecosystem & Interoperability / 生态与互操作
- **Definition**：与标准（如 W3C Pointer Events）对齐度、与原生 / 三方库互操作、序列化、调试 / 测试工具。
- **What to look for**：事件模型是否贴近标准；跨语言/跨框架互操作；事件注入与测试（ArkUI `eventHandleId` + `postEventWithStrategy`）。
- **How to check**：对照 W3C Pointer Events；查互操作/注入 API。

### 12. Usability & Mental Model / 易用心智模型
- **Definition**：学习成本、抽象层次选择（raw event vs gesture）、默认行为、错误处理。
- **What to look for**：底层事件与高层手势是否分离；默认行为是否合理；错误码与异常（如 ArkUI `preventDefault` 仅 Hyperlink、其余抛 100017）。
- **How to check**：对比 raw/gesture 两层抽象；列错误码与约束。
