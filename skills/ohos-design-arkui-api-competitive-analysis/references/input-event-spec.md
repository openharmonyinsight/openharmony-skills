# Input-Event Calibrated Spec / 输入事件校准规格（触摸/指针专项）

> **按需加载**：仅当分析对象为**触摸/指针输入**时读取。来源 `interface_sdk-js` / `ts-universal-events-touch.md` + `ts-gesture-customize-judge.md#baseevent8`。

## onTouch 公共面（校准后）

- **`onTouch(event: (event: TouchEvent) => void): T`** — API 7+（原子化服务 11+）；所有组件通用；默认冒泡；鼠标左键按下也转换为触摸事件。
- **`TouchEvent` extends `BaseEvent`**
  - 自身：`type`(TouchType,7+) · `touches[]`(7+) · `changedTouches[]`(7+) · `stopPropagation()`(7+) · `preventDefault()`(12+，**仅 Hyperlink**，其余抛 100017) · `eventHandleId?`(24+) · `getHistoricalPoints(): HistoricalPoint[]`(10+)
  - 继承 BaseEvent（事件级）：`target`(8+) · `timestamp`(8+,**ns**) · `source`(SourceType,8+) · `pressure`(9+,[0,1] 归一) · `tiltX/tiltY`(9+) · `sourceTool`(9+) · `rollAngle?`(17+) · `deviceId?`(12+) · `targetDisplayId?`(15+) · `getModifierKeyState?()`(12+,Ctrl/Alt/Shift，不支持手写笔)
  - 行为：非注入场景下 `changedTouches` 按**屏幕刷新率重采样**、`touches` 按**器件刷新率**上报，二者可能不同。
- **`TouchObject`**（触点级）：`type`(7+) · `id`(7+) · `x/y`(7+,**vp**) · `windowX/Y`(10+,vp) · `displayX/Y`(10+,vp) · `globalDisplayX/Y?`(20+,vp) · `screenX/Y`(**deprecated 10+**→用 `windowX/Y`) · `pressedTime?`(15+,ns) · `pressure?`(15+,[0,65535)) · `width?/height?`(15+,vp) · `hand?`(InteractionHand,15+)
- **`HistoricalPoint`**(10+)：`touchObject` · `size`(默认 0) · `force`([0,65535)) · `timestamp`(ns)

## 采样三类（务必区分，勿称 iOS"无原生批量"）

| 采样类型 | ArkUI | Android | iOS |
|---|---|---|---|
| **historical（历史中间采样）** | `getHistoricalPoints()`(10+) → `HistoricalPoint[]` | `getHistorySize()`+`getHistoricalX/Y/P()` | （无等价 historical API；以 coalesced 为主） |
| **coalesced（合并采样）** | — | （MotionEvent 本身即合并多采样） | **`UIEvent.coalescedTouches(for:)`** |
| **predicted（预测采样）** | — | — | **`UIEvent.predictedTouches(for:)`** |

> 修正：此前版本写 iOS"无原生批量、需自行用 timestamp 拼"是**错误的**。UIKit 提供 `coalescedTouches(for:)`（合并采样）与 `predictedTouches(for:)`（预测采样），属原生批量/合并访问；只是其模型与 ArkUI `HistoricalPoint` / Android `getHistorical*` 的"历史中间采样"不完全相同。三者须分别表述。

## 单位铁律
坐标一律 **vp**（Android px、iOS pt）；时间一律 **ns**（Android ms、iOS 秒）；压力双口径（事件级 [0,1] vs 触点级 [0,65535)）勿混。
