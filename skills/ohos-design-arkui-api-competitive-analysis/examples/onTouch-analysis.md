# 竞品分析：onTouch / Competitive Analysis: onTouch

> 金标准样例（Gold standard）。它是格式与深度的基准：所有字段/`@since`/单位以 `interface_sdk-js` 为准；每条 ArkUI 断言带版本与单位；缺失/独有能力双向交叉验证。

## 0. Meta / 元信息

| 项 / Item | 值 / Value |
|---|---|
| ArkUI 接口 | `onTouch(event: (event: TouchEvent) => void): T`（API 7+，原子化服务 11+，`SystemCapability.ArkUI.ArkUI.Full`，所有组件通用，默认冒泡） |
| ArkUI 权威源 | `interface_sdk-js`（gitcode）/ `ts-universal-events-touch.md` + `ts-gesture-customize-judge.md`(BaseEvent) + `ts-appendix-enums.md` |
| Android 对照 | `View.OnTouchListener.onTouch(v, MotionEvent)` / Compose `Modifier.pointerInput` |
| iOS 对照 | `UIResponder.touchesBegan/Moved/Ended/Cancelled(Set<UITouch>, UIEvent)` / SwiftUI `DragGesture` |
| API 类别 / Category | 事件类 Touch Event；高权重维度：2·3·4·5·7·11 |

## 1. 规格速览 / Spec at a glance

### ArkUI（声明式，权威公共面）
```ts
onTouch(event: (event: TouchEvent) => void): T   // API 7+
// 鼠标左键按下也会转换成触摸事件触发该回调
interface TouchEvent extends BaseEvent {
  // —— 自身 ——
  type: TouchType;               // 7+  Down/Up/Move/Cancel
  touches: TouchObject[];        // 7+  全部触点（多指），使用前需校验非空
  changedTouches: TouchObject[]; // 7+  变化的触点
  stopPropagation(): void;       // 7+
  preventDefault(): void;        // 12+ 仅 Hyperlink 支持，其余抛 100017
  eventHandleId?: number;        // 24+ 事件注入(postEventWithStrategy)唯一标识
  getHistoricalPoints(): HistoricalPoint[]; // 10+
  // —— 继承 BaseEvent（事件级）——
  target; timestamp: number(ns); source: SourceType;            // 8+
  pressure: number([0,1] 归一); tiltX; tiltY; sourceTool: SourceTool; // 9+
  rollAngle?: number; deviceId?; targetDisplayId?;              // 17+/12+/15+
  getModifierKeyState?(keys): boolean;                          // 12+ Ctrl/Alt/Shift，不支持手写笔
}
interface TouchObject {          // 触点级
  type: TouchType; id: number;                          // 7+
  x: number; y: number;                                 // 7+ 单位 vp（组件坐标系）
  windowX: number; windowY: number;                     // 10+ vp（窗口）
  displayX: number; displayY: number;                   // 10+ vp（应用屏）
  globalDisplayX?: number; globalDisplayY?: number;     // 20+ vp（全局坐标系）
  screenX; screenY;                                     // (deprecated) 7+ 起，10+ 废弃 → 用 windowX/Y
  pressedTime?: number;                                 // 15+ ns
  pressure?: number;                                    // 15+ [0,65535) 原始
  width?: number; height?: number;                      // 15+ vp 触点面积
  hand?: InteractionHand;                               // 15+ 左右手
}
interface HistoricalPoint {      // 10+
  touchObject: TouchObject; size: number; force: number([0,65535)); timestamp: number(ns);
}
```
> **关键行为**：非注入场景下 `changedTouches` 按屏幕刷新率重采样、`touches` 按器件刷新率上报，**二者数据可能不同**。

### Android（命令式，View 体系）— `MotionEvent`
- **动作 / Action**：`getActionMasked()` → DOWN/UP/MOVE/CANCEL/OUTSIDE + POINTER_DOWN/POINTER_UP；`getActionIndex()` 取该动作的 pointer index。
- **多点 / Multi-pointer**：`getPointerCount()` · `getPointerId(index)`（**id 稳定 / index 会变**）· `findPointerIndex(id)`。
- **坐标 / Coords**：`getX/Y()`(view 相对，px) · `getRawX/Y()`(屏幕相对，px)；`getX(int)` 取指定 pointer。
- **物理 / Physics**：`getPressure()`([0,1] 归一) · `getSize()`。
- **工具/设备 / Tool**：`getToolType()`(FINGER/STYLUS/MOUSE/ERASER) · `getDeviceId()` · `getSource()` · `getButtonState()`/`getMetaState()`。
- **历史点 / History**：`getHistorySize()` + `getHistoricalX/Y/P()`。
- **笔姿 / Stylus**：`AXIS_TILT` · `AXIS_ORIENTATION`。
- **时间 / Time**：`getEventTime()` / `getDownTime()`（ms）。

### iOS（命令式 + Responder Chain）— `UITouch`
- **入口 / Entry**：`UIResponder.touchesBegan/Moved/Ended/Cancelled(_:with:)`，参数 `Set<UITouch>` + `UIEvent`。
- **相位 / Phase**：`phase` = began / moved / **stationary** / ended / cancelled。
- **坐标 / Coords**：`location(in:)` / `previousLocation(in:)`（按需查任意 view/window，pt）。
- **物理 / Physics**：`force` + `maximumPossibleForce`（绝对值）· `majorRadius`(+tolerance)。
- **属性 / Props**：`tapCount` · `timestamp`(秒) · `type`(direct/indirect/stylus)。
- **笔姿 / Stylus**：`altitudeAngle` · `azimuthAngle(in:)`。
- **分发 / Dispatch**：**Responder Chain** + hit-testing（系统决定 first responder，沿链冒泡）。

### 用法示例 / Usage examples（每平台 1 段，最小可运行）

```ts
// ArkUI —— 在组件上绑定 onTouch（注意坐标单位 vp）
Button('Touch').onTouch((event: TouchEvent) => {
  if (event.type === TouchType.Down) {
    const p = event.touches?.[0];
    console.info(`down at (${p?.x}vp, ${p?.y}vp) id=${p?.id}`);
  }
})
```
```kotlin
// Android —— View.onTouchEvent（坐标单位 px，pointer id 稳定）
override fun onTouchEvent(e: MotionEvent): Boolean {
  when (e.actionMasked) {
    MotionEvent.ACTION_DOWN -> {
      val pid = e.getPointerId(e.actionIndex)   // 跨手势稳定的 id
      Log.d("T", "down x=${e.x}px y=${e.y}px pid=$pid")
    }
  }
  return true
}
```
```swift
// iOS —— UIResponder.touchesBegan（坐标单位 pt，逐个 UITouch 查询）
override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
  guard let t = touches.first else { return }
  let loc = t.location(in: view)          // pt
  print("began at \(loc), phase=\(t.phase), taps=\(t.tapCount)")
}
```

## 2. 能力对比矩阵 / Capability Matrix

| 维度 / Dim | ArkUI（interface_sdk-js 公共面） | Android MotionEvent | iOS UITouch |
|---|---|---|---|
| 入口/冒泡 | onTouch(cb) 7+，所有组件，默认冒泡 | onTouch/onTouchEvent | 四回调，Responder Chain |
| 事件阶段 | Down/Up/Move/Cancel | DOWN/UP/MOVE/CANCEL + POINTER_DOWN/UP + OUTSIDE | began/moved/**stationary**/ended/cancelled |
| 多点模型 | `touches[]`+`changedTouches[]`（**changedTouches 屏幕刷新率重采样 / touches 器件刷新率，二者可能不同**） | pointer **id/index 双重** + `getPointerCount` | `Set<UITouch>` 每对象一指 |
| 坐标系 | 组件 x/y · 窗口 windowX/Y(10+) · 应用屏 displayX/Y(10+) · 全局 globalDisplayX/Y(20+)；screenX/Y 已废弃(10+) | view 相对 `getX/Y` + 屏幕相对 `getRawX/Y`（2 套） | `location(in:)` 按需查任意 view/window |
| **坐标单位** | **vp** | **px** | **pt** |
| 压力 | 事件级 `pressure`(9+,[0,1] 归一) + 触点级 `pressure`(15+,[0,65535) 原始) + 历史点 `force`([0,65535)) | `getPressure()`([0,1] 归一) | `force` + `maximumPossibleForce`(绝对) |
| 触点面积 | `width/height`(15+, vp) | `getSize()` | `majorRadius` + tolerance |
| 输入源/工具 | 事件级 `source`(SourceType,8+) + `sourceTool`(9+) | `toolType` + `source` | `type`(direct/indirect/stylus) |
| 笔姿态 | 事件级 `tiltX/tiltY`(9+) + `rollAngle`(17+) | `AXIS_TILT` + `AXIS_ORIENTATION` | `altitudeAngle` + `azimuthAngle` |
| 历史点/批量采样（historical/coalesced/predicted） | `getHistoricalPoints()`(10+)→`HistoricalPoint[]`(historical)[1] | `getHistorySize`+`getHistoricalX/Y/P`(historical)[2] | `coalescedTouches`(coalesced)+`predictedTouches`(predicted)[3] |
| 分发/拦截 | `stopPropagation`(7+) + `preventDefault`(12+，仅 Hyperlink) + `onTouchIntercept` | `onInterceptTouchEvent` 父拦截 + `requestDisallowIntercept` | Responder Chain + hit-testing |
| 时间戳 | `timestamp`(8+, ns) + `pressedTime`(15+, ns) | `eventTime`/`downTime`（ms） | `timestamp`（秒） |
| 多屏/设备 | `targetDisplayId`(15+) + `deviceId`(12+) + `globalDisplayX/Y`(20+) | `getDeviceId` + display API | 多 scene/display |
| 左右手 | `hand`: InteractionHand(15+) 触点级 | N/A | N/A |
| 修饰键 | `getModifierKeyState`(12+, Ctrl/Alt/Shift，**不支持手写笔**) | `getMetaState` + `getButtonState` | UIKeyModifierFlags |

## 3. 关键差异点 / Key Findings

**ArkUI 独有 / 更细（advantage）**
- 坐标单位 vp + 多套坐标空间（含全局 `globalDisplayX/Y` 20+），跨屏取值省心；Android 仅 2 套、iOS 需逐次 `location(in:)`。
- `changedTouches`/`touches` 重采样口径差异是 ArkUI **独有行为**，迁移与一致性测试要注意。
- 采样模型：ArkUI `getHistoricalPoints`(10+) 提供 **historical**；Android `getHistorical*`(historical)[2]；iOS `coalescedTouches`(coalesced)+`predictedTouches`(predicted)[3]。三平台 historical/coalesced/predicted 模型不同，**并非"iOS 无原生批量"**（前版结论有误，已纠正）。
- 触点级 `width/height` + 左右手 `hand`(15+) + 事件注入 `eventHandleId`(24+)。

**ArkUI 需对齐 / 注意（gap & risk）**
- 坐标单位 **vp** vs Android **px** vs iOS **pt**——跨平台迁移坐标需换算（高频坑）。
- `screenX/Y` 已废弃(10+)，勿用，统一用 `windowX/Y`。
- **压力双口径**：事件级 `pressure`=[0,1] 归一(9+) vs 触点级 `pressure`=[0,65535) 原始(15+)——易混。
- `preventDefault`(12+) 仅 Hyperlink 支持，其余抛 100017。

**平台对照 / Platform contrast**
- iOS 的 `stationary` 相位 + Responder Chain 心智与 ArkUI/Android 差异最大，迁移时分发逻辑需重写。
- Android pointer **id/index 双重模型** 心智最重，ArkUI 用单一稳定 `id` 简化（易用性更好）。

**共性 / Common ground**
- 三者都把"原始事件层"与"手势层"分离；**声明式手势优先级模型高度一致**：ArkUI `gesture/priorityGesture/parallelGesture` ≈ SwiftUI `gesture/simultaneousGesture/highPriorityGesture`（Android Compose 用 `pointerInput`+`detectXxx`，更底层）。

## 4. 结论与建议 / Conclusion

- **能力覆盖**：ArkUI 在触摸事件维度不弱于 Android/iOS，且在坐标空间、历史点、左右手、全局坐标上更优；主要风险在单位口径与压力双口径。
- **对齐优先级**：① 文档明确坐标单位 vp 及与 px/pt 的换算；② 压力双口径在事件级/触点级分别标注；③ 迁移文档强调 `screenX/Y` 已废弃。
- **迁移路径**：Android → pointer `id` 直接对应、坐标取 `x/y`(注意 vp↔px)、历史点用 `getHistoricalPoints()`；iOS → 把 Responder Chain 的分发逻辑改写为 `stopPropagation`/`onTouchIntercept`，触点对象由逐个 `UITouch` 查改为遍历 `touches[]`。

## 5. 附录 / Appendix（来源，每项断言关联编号）

平台版本基线：ArkUI API 12（master 查询）/ Android API 34 + Compose / iOS 17；查询日期 2026-07-21。

| # | 平台 | API/符号 | 证据 | 来源 | 版本/availability | 章节 |
|---|---|---|---|---|---|---|
| [1] | ArkUI | `getHistoricalPoints`/`HistoricalPoint` | 官方 | `ts-universal-events-touch.md`（interface_sdk-js 生成） | 10+ | HistoricalPoint 对象说明 |
| [2] | Android | `MotionEvent.getHistoricalX/Y/P` | 官方 | developer.android.com/reference/android/view/MotionEvent | API 1+ | Batched input |
| [3] | iOS | `UIEvent.coalescedTouches(for:)`/`predictedTouches(for:)` | 官方 | developer.apple.com/documentation/uikit/uievent | iOS | Touch events |
| [4] | ArkUI | `onTouch`/`TouchEvent`/`TouchObject`（vp / `screenX/Y` 废弃 / `pressure` / `hand`） | 官方 | `ts-universal-events-touch.md`+`ts-gesture-customize-judge.md#baseevent8`+`ts-appendix-enums.md`（interface_sdk-js） | 7+/10+/15+/20+ | onTouch / BaseEvent / TouchObject |
| [5] | Android | `MotionEvent`（`getActionMasked`/`getPointerId`/`getPressure`/`getToolType`） | 官方 | developer.android.com/reference/android/view/MotionEvent | API 5+ | Motion Events |
| [6] | iOS | `UITouch`/`UIResponder` | 官方 | developer.apple.com/documentation/uikit/uitouch、/uiresponder | iOS | Touches |

> "缺失/独有"结论（iOS `stationary`[6]、Android pointer id/index 双重[5]）已双向检索。内部对照（非公共结论）：ace_engine `frameworks/.../index.d.ts`、`interfaces/inner_api/ace_kit/include/ui/event/touch_event.h`。
