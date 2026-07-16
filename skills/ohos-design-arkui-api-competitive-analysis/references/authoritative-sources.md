# Authoritative Source Rule / 权威数据源铁律

## 1. 唯一权威：interface_sdk-js

**公共接口定义一律以 `interface_sdk-js` 仓库为唯一权威**：

- 仓库：https://gitcode.com/openharmony/interface_sdk-js （`api/` 下的 `.d.ts` / `.static.d.ets`）。
- 渲染文档（由该仓库生成，可读性最好、含 `@since`/单位/废弃）：`docs.openharmony.cn` 与 gitee `openharmony/docs` 的 `zh-cn/application-dev/reference/apis-arkui/arkui-ts/*.md`。

> **ace_engine 内部 `.d.ts` / C++ 不是公共面**：如 `frameworks/bridge/declarative_frontend/.../index.d.ts`、`interfaces/inner_api/ace_kit/include/ui/event/touch_event.h`。它们是前端桥接/实现内部，字段名、单位、`@since`、废弃状态都与公共 SDK **可能不一致**，**仅作实现对照，不得作公共能力结论**。

## 2. 实测反例（为什么必须以 interface_sdk-js 为准）

用 ace_engine 内部定义做 onTouch 对标会得到**错误结论**（已在 skill 设计阶段用权威源校准）：

| 内部定义（错误） | interface_sdk-js 公共面（正确） |
|---|---|
| 触摸坐标单位 px | **vp** |
| `screenX/Y` 现役字段 | **`screenX/Y` 自 API 10 废弃**，用 `windowX/Y` |
| TouchObject 有 `force` | 公共面是 **`pressure`**（触点级 15+，`[0,65535)`）；`force` 仅在 HistoricalPoint |
| `sourceTool`/`tiltX` 在 TouchObject | 它们在 **TouchEvent（继承 BaseEvent）事件级** |
| `operatingHand` | 公共名是 **`hand`（InteractionHand，15+）** |
| 单一压力口径 | **两套**：事件级 `pressure`(9+,[0,1]) vs 触点级 `pressure`(15+,[0,65535)) |

## 3. 取数命令（按可用性优先）

1. **`oh-gc search code "<符号>"`** —— 在 gitcode 仓库内检索 `.d.ts`（首选；端点偶尔不可用，见兜底）。
2. **gitcode / gitee raw `.d.ts`** ——
   `https://gitcode.com/openharmony/interface_sdk-js/raw/master/<path>`（gitcode raw 常被 JS 壳拦截，可试 gitee 镜像 `https://gitee.com/openharmony/interface_sdk-js/raw/master/<path>`）。
3. **兜底：官方渲染文档** ——
   `https://gitee.com/openharmony/docs/raw/master/zh-cn/application-dev/reference/apis-arkui/arkui-ts/<topic>.md`，含 `@since`/单位/废弃，对竞品分析信息量最大。

## 4. 校准后的 onTouch 公共面权威规格（示范"如何正确读权威源"）

来源：`ts-universal-events-touch.md` + `ts-gesture-customize-judge.md#baseevent8`。

- **`onTouch(event: (event: TouchEvent) => void): T`** — API 7+（原子化服务 11+）；所有组件通用；默认冒泡；鼠标左键按下也转换为触摸事件。
- **`TouchEvent` extends `BaseEvent`**
  - 自身：`type`(TouchType,7+) · `touches[]`(7+) · `changedTouches[]`(7+) · `stopPropagation()`(7+) · `preventDefault()`(12+，**仅 Hyperlink**，其余抛 100017) · `eventHandleId?`(24+) · `getHistoricalPoints(): HistoricalPoint[]`(10+)
  - 继承 BaseEvent（事件级）：`target`(8+) · `timestamp`(8+,**ns**) · `source`(SourceType,8+) · `pressure`(9+,[0,1] 归一) · `tiltX/tiltY`(9+) · `sourceTool`(9+) · `rollAngle?`(17+) · `deviceId?`(12+) · `targetDisplayId?`(15+) · `getModifierKeyState?()`(12+,Ctrl/Alt/Shift，不支持手写笔)
  - 行为：非注入场景下 `changedTouches` 按**屏幕刷新率重采样**、`touches` 按**器件刷新率**上报，二者数据可能不同。
- **`TouchObject`**（触点级）：`type`(7+) · `id`(7+) · `x/y`(7+,**vp**) · `windowX/Y`(10+,vp) · `displayX/Y`(10+,vp) · `globalDisplayX/Y?`(20+,vp) · `screenX/Y`(**deprecated 10+**→用 `windowX/Y`) · `pressedTime?`(15+,ns) · `pressure?`(15+,[0,65535)) · `width?/height?`(15+,vp) · `hand?`(InteractionHand,15+)
- **`HistoricalPoint`**(10+)：`touchObject` · `size`(默认 0) · `force`([0,65535)) · `timestamp`(ns)

> 单位铁律：ArkUI 触摸坐标一律 **vp**（对比 Android=px、iOS=pt）。时间一律 **ns**（对比 Android=ms、iOS=秒）。压力双口径勿混。
