# Eval: Flex 布局 / Flex layout

## Prompt（测试输入）

> 对 ArkUI 的 Flex 布局做与 Android(FlexboxLayout/Compose Row·Column)、iOS(UIStackView/SwiftUI HStack·VStack) 的竞品分析，给出能力与规格对比。

跑两遍：**with skill** 与 **without skill**。

## 预期关键发现 / Expected findings（with skill 必须命中）

ArkUI 侧以 `interface_sdk-js` 为准；布局类高权重维度 1·3·9·12。

- [ ] **权威源**：ArkUI `Flex`(`direction`/`justifyContent`/`alignItems`/`alignContent`/`wrap`)、`flexGrow`/`flexShrink`/`flexBasis`/`alignSelf`、`Row`/`Column` 以 `interface_sdk-js` 为源；`@since`（核心 7+，特性 标 `待核`）。
- [ ] **API 形态(1)**：声明式 vs 命令式（ArkUI/Compose/SwiftUI 声明式 vs FlexboxLayout/UIStackView 命令式）。
- [ ] **规格精度(3)**：`flexBasis` 是否支持百分比（ArkUI 否、FlexboxLayout 是）；`order` 视觉重排（仅 FlexboxLayout 原生）；`SpaceEvenly`/`alignContent`/reverse 覆盖。
- [ ] **跨端一致性(9)**：ArkUI `Flex`（二次测量）vs `Row`/`Column`（单次测量）双 API 取舍——官方推荐 `Row`/`Column` 的性能理由。
- [ ] **心智(12)**：CSS Flexbox 完整度排序（FlexboxLayout ≥ ArkUI Flex > Compose/SwiftUI > UIStackView）。
- [ ] **不污染**：布局分析**不**引入触摸坐标单位/触点归属等无关维度。
- [ ] **格式**：每平台结构化规格 + 用法代码；断言带来源编号；版本基线。

## 通过标准

- with skill：清单全中。
- without skill 对比：典型凭通用知识罗列、不锁版本、无来源编号、自由结构。

## 备注

- 代表**布局类**，验证框架在该类的适用性 + C7（不把 Touch 维度污染到布局）。
