# Eval: List 组件 / List component

## Prompt（测试输入）

> 对 ArkUI 的 List 组件做与 Android(RecyclerView/Compose LazyColumn)、iOS(UITableView/SwiftUI List) 的竞品分析，给出能力与规格对比。

跑两遍：**with skill** 与 **without skill**。

## 预期关键发现 / Expected findings（with skill 必须命中）

ArkUI 侧以 `interface_sdk-js` 为准；组件类高权重维度 2·5·6·8·10。

- [ ] **权威源**：ArkUI List/`ListItem`/`ListItemGroup`/`Scroller`、`lanes`/`cachedCount`/`stickyHeader`/`chainAnimation`/`editMode` 等以 `interface_sdk-js` 为源；`@since`（核心 7+，具体特性 标 `待核`）。
- [ ] **能力覆盖(2)**：分组(`ListItemGroup`)、多列(`lanes`)、粘性头、懒加载、下拉刷新；对照 RecyclerView(LAYOUT MANAGER+DiffUtil)、Compose LazyColumn、UITableView/SwiftUI List。
- [ ] **分发/滚动(5)**：滚动控制(`Scroller.scrollToIndex/scrollTo`)、`onReachStart/End`、`onScrollIndex`；嵌套滚动协同。
- [ ] **可访问性(6)**：ListItem 语义标注。
- [ ] **状态/生命周期(8)**：数据驱动（`@State`/`ForEach`/`LazyForEach`+`IDataSource`）；差异数据更新能力（是否等价 DiffUtil）。
- [ ] **版本/兼容(10)**：`@since` 与废弃。
- [ ] **格式**：每平台结构化规格 + 用法代码；断言带来源编号；版本基线。

## 通过标准

- with skill：清单全中。
- without skill 对比：典型"未检索代码仓库"、凭通用知识罗列、不锁版本、无来源编号、自由结构。

## 备注

- 代表**组件类**，验证框架在该类的适用性（C1 宽范围覆盖）。
