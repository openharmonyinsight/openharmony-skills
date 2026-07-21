# Eval: onTouch 竞品分析 / Competitive Analysis of onTouch

## Prompt（测试输入）

> 对 ArkUI 的 `onTouch` 接口做与 Android、iOS 触摸事件的竞品分析，给出能力与规格对比。

跑两遍：**with skill**（加载本 skill）与 **without skill**（不加载），对比产出。

## 预期关键发现 / Expected findings（with skill 必须命中）

ArkUI 侧的每一条都必须以 **`interface_sdk-js` / 官方文档**为来源，不得来自 ace_engine 内部 `.d.ts` 或 C++。

- [ ] **权威源**：明确以 `interface_sdk-js` 为 ArkUI 公共定义来源，并声明 ace_engine 内部仅作对照。
- [ ] **坐标单位 = vp**（不是 px）；并指出 Android=px、iOS=pt 的迁移换算。
- [ ] **`screenX/Y` 已废弃**（自 API 10），替代为 `windowX/Y`。
- [ ] **压力双口径**：事件级 `pressure`(9+,[0,1] 归一，继承 BaseEvent) vs 触点级 `pressure`(15+,[0,65535) 原始)；公共触点字段名是 `pressure` 而非 `force`（`force` 仅在 HistoricalPoint）。
- [ ] **事件级 vs 触点级归属**：`sourceTool`/`tiltX`/`tiltY`/`source` 在 `TouchEvent`（BaseEvent），不在 `TouchObject`。
- [ ] **`hand`（InteractionHand，15+）** 为左右手字段（不是内部命名 `operatingHand`）。
- [ ] **`changedTouches`/`touches` 重采样口径差异**：changedTouches 屏幕刷新率重采样、touches 器件刷新率，二者可能不同。
- [ ] **采样三类**：`getHistoricalPoints()`(10+) = historical；iOS `coalescedTouches`(coalesced)/`predictedTouches`(predicted)；区分 historical/coalesced/predicted，**不得**称 iOS 无原生批量。
- [ ] **分发**：默认冒泡 + `stopPropagation`；iOS 走 Responder Chain。
- [ ] **结构**：按 Meta / 规格速览 / 能力矩阵 / 关键差异 / 结论与迁移 / 附录来源 组织。
- [ ] **版本与单位标注**：ArkUI 字段带 `@since` + 单位（vp/ns）。
- [ ] **双向交叉验证**：缺失/独有结论（如 iOS `stationary`、Android id/index 双重）有对照说明。

## 通过标准 / Pass criteria

- with skill：上述清单全部命中。
- without skill 对比：典型会出现"坐标单位写成 px / 用 `force` / `operatingHand` / 现役 `screenX/Y` / sourceTool 归到 TouchObject"等错误（因模型易从 ace_engine 内部定义推断），证明 skill 的价值。

## 备注 / Notes

- 本 eval 是触摸事件类的自检；验证框架泛化性时，另用同类事件接口（如 `onClick`/`onHover`）再跑一遍，确认只展开高权重维度 2·3·4·5·7·11。
