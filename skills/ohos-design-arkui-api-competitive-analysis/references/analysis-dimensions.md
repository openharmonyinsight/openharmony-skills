# Analysis Dimensions / 竞品分析维度框架

输入/交互事件类竞品分析的 **4 组 / 12 维**。每维给：**Definition** / **What to look for** / **How to check**。先用「维度权重裁剪表」按输入事件子类选出高权重维度。

> 作用域：本框架当前服务于**输入/交互事件类**（触摸 / 按键·快捷键 / 指针）。每项实质性断言须关联来源编号（见 `authoritative-sources.md` 来源引用格式）；"缺失/独有/优于"须双向检索。

## 维度权重裁剪表 / Weight by input-event sub-type

| 输入事件子类 / Sub-type | 高权重维度 / High | 低权重维度 / Low |
|---|---|---|
| 触摸/指针 touch·pointer（onTouch / onHover / 指针） | 2 · 3 · 4 · 5 · 7 · 11 | 8 · 10 |
| 按键/快捷键 key·shortcut（onKeyEvent / 应用级快捷键） | 2 · 3 · 5 · 10 · 11 | 4（笔姿态）· 7 |

> 用法：判定子类后，只展开高权重维度；低权重维度仅在用户明确关心时展开。`@since` 与来源为所有维度强制；单位/范围/默认值仅适用时记录。

## Capability Scope Tiers / 作用域层级（勿降级）

带层级的能力，**用户指明某一层时只分析该层**。常见：

| 能力 / Capability | 典型层级 / Typical tiers |
|---|---|
| 快捷键 / Shortcut | 应用级（app 内全局键盘）/ 组件级（单组件按键）/ 系统级（OS 全局热键） |
| 触摸 / Touch | 组件级 / 窗口或全局 hit-test |
| 拖拽 / Drag | 组件级 / app 级 / 跨窗口 |
| 焦点 / Focus | 组件级 / app 级 |

### 快捷键作用域对照（应用级键盘快捷键，勿与 launcher 启动快捷方式混淆）

| 层级 | ArkUI 取数线索（以 interface_sdk-js 为准） | Android（**键盘**快捷键） | iOS |
|---|---|---|---|
| **应用级 / App-level** | 窗口级 `UIContext.onKeyEvent`（命令式，自匹配修饰键）；`MenuItem.labelInfo` 仅提示 | `Activity.onKeyShortcut` / `onProvideKeyboardShortcuts` / Menu keyboard shortcuts（`alphabeticShortcut`+modifier）/ `dispatchKeyShortcutEvent` / Compose key input（`Modifier.onKeyEvent`） | **`UIKeyCommand`**（responder/command chain 注册，app 级生效） |
| 组件级 | `onKeyEvent`（CommonMethod） | `View.onKeyDown/onKeyUp` | `pressesBegan/pressesEnded`（iPadOS 硬键盘） |
| 系统级 | `ohos.multimodalInput.inputConsumer`（系统应用 only） | 无通用 app 全局 | Carbon `RegisterEventHotKey`（平台特定） |

> ⚠️ `ShortcutManager`（Android）管理的是 **launcher 静态/动态/固定 App Shortcuts（长按图标）**，**不是键盘 accelerator**；除非分析"应用启动快捷方式"，否则不作为键盘快捷键对标。具体 API 名以 `interface_sdk-js` 与各平台官方文档为准。

---

## A. Capability & Spec / 能力与规格

### 1. API Shape & Signature / API 形态与签名
- **Definition**：命名、参数风格、声明式 vs 命令式、Builder/Modifier/链式、类型表达力。
- **What to look for**：方法/属性命名；回调签名；声明式与命令式是否同步（ArkUI static `.static.d.ets` vs dynamic `.d.ts`）。
- **How to check**：ArkUI 取 `interface_sdk-js`；Android Compose Modifier vs View 方法；iOS SwiftUI modifier vs UIKit 方法。

### 2. Capability Coverage / 能力覆盖
- **Definition**：功能点齐全；缺失 / 独有；子能力枚举（事件阶段、坐标空间、**作用域层级**）。
- **What to look for**：三平台是否都有；独有项（ArkUI 多坐标空间 / `hand`；iOS `stationary`）；**层级是否齐全**。
- **How to check**：列子能力逐项打勾；缺失/独有须**双向交叉检索**（见 `platform-source-routing.md`）。

### 3. Spec Precision / 规格精度
- **Definition**：单位、取值范围、默认值、枚举、空值语义、`@since`、废弃。
- **What to look for**：**单位口径**（ArkUI 触摸坐标 vp，Android px，iOS pt——迁移坑）；范围与钳制；废弃字段。
- **How to check**：`interface_sdk-js` 逐字段核；`@deprecated`（如 ArkUI `screenX/Y` 自 10 废弃）。

---

## B. Input & Interaction / 输入与交互

### 4. Multi-Input Source / 多输入源
- **Definition**：指 / 笔 / 鼠标 / 触控板 / 手柄 / 键盘；折叠屏；多屏。
- **What to look for**：`sourceType`/`sourceTool`/`toolType`/`type` 枚举；笔姿态（`tiltX/Y`、`rollAngle`、`altitudeAngle`）；多屏坐标。
- **How to check**：枚举成员逐项比对。

### 5. Dispatch & Interaction Model / 分发与交互
- **Definition**：冒泡 / 拦截 / hit-test、手势仲裁、优先级、**快捷键注册/命中链**。
- **What to look for**：默认是否冒泡；阻止 API（ArkUI `stopPropagation`、Android `onInterceptTouchEvent`、iOS Responder Chain）；手势优先级（ArkUI `priorityGesture/parallelGesture` ≈ SwiftUI `simultaneousGesture/highPriorityGesture`）。
- **How to check**：分发流程文档；等价拦截 API；快捷键各层注册机制。

### 6. Accessibility / 可访问性
- **Definition**：屏幕阅读、语义、焦点、兜底。
- **How to check**：ArkUI accessibility 属性、Android `AccessibilityNodeInfo`、iOS `UIAccessibility`。

---

## C. Performance & Engineering / 性能与工程

### 7. Performance & Overhead / 性能与开销
- **Definition**：分发频率、采样合并、节流、线程、阻塞。
- **What to look for**：**采样三类需区分**——
  - **historical（历史中间采样）**：ArkUI `TouchEvent.getHistoricalPoints()`(10+) → `HistoricalPoint[]`；Android `getHistorySize()`+`getHistoricalX/Y/P()`。
  - **coalesced（合并采样）**：iOS `UIEvent.coalescedTouches(for:)` 返回与主触点关联的合并采样。
  - **predicted（预测采样）**：iOS `UIEvent.predictedTouches(for:)`；ArkUI/Android 视接口而定。
  - 另：ArkUI `changedTouches`（屏幕刷新率重采样）vs `touches`（器件刷新率）可能不同。
- **How to check**：查各平台采样/历史/合并 API；不做实测基准。

### 8. State & Lifecycle / 状态与生命周期
- **Definition**：接口与组件生命周期、回调时机、副作用。
- **How to check**：生命周期文档与时序。

### 9. Cross-Platform Consistency / 跨端一致性
- **Definition**：手机/平板/穿戴/桌面/车机一致性。
- **How to check**：设备形态约束与 `SystemCapability`。

---

## D. Evolution & Ecosystem / 演进与生态

### 10. Versioning & Compatibility / 版本与兼容
- **Definition**：废弃、增量、迁移、向前/向后兼容。
- **What to look for**：`@deprecated`/`@obsoleted`；破坏性变更；迁移替代。

### 11. Ecosystem & Interoperability / 生态与互操作
- **Definition**：与标准（W3C Pointer/Keyboard Events）对齐、互操作、序列化、调试/测试、事件注入。
- **What to look for**：ArkUI `eventHandleId`+`postEventWithStrategy`；键码标准对齐。

### 12. Usability & Mental Model / 易用心智
- **Definition**：学习成本、抽象层次（raw event vs 声明式注册）、默认行为、错误处理。
- **What to look for**：声明式 vs 命令式（iOS `UIKeyCommand` 声明式 vs ArkUI 窗口监听命令式）；错误码（ArkUI `preventDefault` 仅 Hyperlink，余抛 100017）。
