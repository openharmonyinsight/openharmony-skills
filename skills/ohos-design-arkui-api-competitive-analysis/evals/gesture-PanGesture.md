# Eval: PanGesture 手势 / Pan gesture

## Prompt（测试输入）

> 对 ArkUI 的 PanGesture 做与 Android、iOS 拖拽/平移手势的竞品分析，给出能力与规格对比。

跑两遍：**with skill** 与 **without skill**。

## 预期关键发现 / Expected findings（with skill 必须命中）

ArkUI 侧以 `interface_sdk-js` 为准；手势类高权重维度 1·2·4·5·12。

- [ ] **权威源**：ArkUI 字段（`fingers`/`distance`/`direction`/`distanceMap`、`GestureEvent` 的 `offsetX/Y`/`velocity`/`fingers`/`angle`）以 `interface_sdk-js` 为源；`@since`（核心 7+，子特性如 `distanceMap`/`velocity` 直出 标 `待核`）。
- [ ] **能力覆盖(2)**：声明式可配置阈值/方向（`distance`/`distanceMap`/`PanDirection`）；多指（`fingers`）；手势组合（`parallelGesture`/`priorityGesture`/`GestureGroup`）。
- [ ] **分发/仲裁(5)**：ArkUI `priority/parallel/exclusive` ≈ iOS `require(toFail:)`/`shouldRecognizeSimultaneouslyWith`；Android 命令式 `GestureDetector`/`onTouch` 自裁。
- [ ] **位移语义差异**：ArkUI `offsetX/Y` 累计；Android `onScroll` 给**增量**(反向)；iOS `translation(in:)` 累计可重置。
- [ ] **状态机**：iOS 显式 7 态（含 `.failed`）；ArkUI/Android 无显式失败态。
- [ ] **声明式心智(12)**：ArkUI 声明式绑定 vs Android 命令式 listener vs iOS target/action。
- [ ] **格式**：每平台结构化规格 + 用法代码；断言带来源编号；版本基线；不把触摸坐标单位(vp/px/pt)硬套到手势位移语义。

## 通过标准

- with skill：清单全中。
- without skill 对比：典型用通用知识/ace_engine 内部路径、不锁版本、无来源编号、自由结构；可能误把手势位移与触摸坐标单位混为一谈。

## 备注

- 代表**手势类**，验证框架在该类的适用性（C1 宽范围覆盖）。
