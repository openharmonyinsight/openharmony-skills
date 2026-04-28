# 自适应布局指南

## 目录

1. [核心概念](#核心概念)
2. [七种自适应能力](#七种自适应能力)
3. [注意事项](#注意事项)

---

## 核心概念

### 什么是自适应布局

自适应布局关注**组件级**的微观调整，通过组件属性配置让布局自动适应容器尺寸变化，无需断点参与。与响应式布局（需要断点切换页面结构）互补，自适应布局是优先使用的基础手段。

### 自适应布局 vs 响应式布局

| 对比项 | 自适应布局 | 响应式布局 |
|--------|-----------|-----------|
| 关注点 | 组件级微观调整 | 页面级宏观调整 |
| 是否需要断点 | 否 | 是 |
| 实现方式 | 组件属性（layoutWeight、Blank 等） | GridRow、SideBarContainer 等 |
| 典型场景 | 表单输入框拉伸、图片等比缩放 | 单栏变双栏、导航+内容切换 |

### 关键属性/API

| 属性/API | 说明 | 适用能力 |
|---------|------|---------|
| `layoutWeight` | 按权重分配剩余空间 | 拉伸、均分、占比 |
| `Blank()` | 弹性空白填充 | 拉伸 |
| `aspectRatio` | 固定宽高比 | 缩放 |
| `displayPriority` | 按优先级显隐 | 隐藏 |
| `Visibility` | 手动控制组件显隐 | 隐藏 |
| `FlexWrap.Wrap` | 自动换行 | 折行 |
| `FlexAlign.SpaceEvenly` | 子项均匀分布 | 均分 |
| 百分比宽高 | 用 `'30%'` 等字符串设置尺寸 | 占比 |
| `List` | 可滚动列表，按需加载 | 延伸 |
| `Scroll` | 可滚动容器 | 延伸 |

---

## 七种自适应能力

### 1. 拉伸 (Stretch)

容器内的组件跟随容器尺寸变化。

**layoutWeight**：子组件按权重分配剩余空间。

```typescript
Row() {
  Text('标签')
  TextInput().layoutWeight(1)  // 自动拉伸填充剩余空间
}
```

**Blank**：在固定宽度元素之间插入弹性空白。

```typescript
Row() {
  Text('固定标题')
  Blank()         // 自动填充中间空白
  Text('固定操作')
}
```

### 2. 缩放 (Scale)

组件按容器宽度等比缩放，通过百分比宽度配合 `aspectRatio` 保持宽高比。

```typescript
Image($r('app.media.banner'))
  .width('100%')
  .aspectRatio(16 / 9)   // 高度自动计算
```

自定义组件也可使用：

```typescript
Column() {
  Text('等比缩放卡片')
}
.width('100%')
.aspectRatio(3 / 2)
```

### 3. 隐藏 (Hidden)

空间不足时按优先级自动隐藏次要内容。

**displayPriority（推荐）**：优先级数值越大越不容易被隐藏，默认值为 1。

```typescript
Row() {
  Text('核心标题').displayPriority(2)   // 高优先级
  Text('副标题').displayPriority(1)     // 低优先级，空间不足时先隐藏
}
```

**visibility**：通过条件判断手动控制显隐，适合需要精确控制阈值的场景。

```typescript
Text('摘要')
  .visibility(this.width > 300 ? Visibility.Visible : Visibility.None)
```

### 4. 折行 (Wrap)

空间不足时自动换行。

```typescript
Flex({ wrap: FlexWrap.Wrap }) {
  ForEach(this.tags, (tag: string) => {
    Text(tag).margin({ right: 8, bottom: 8 })
  })
}
```

### 5. 均分 (Equi-width)

将空间平均分配给子组件。

**SpaceEvenly**：子项间距相等，包括首尾与容器边缘的间距。

```typescript
Row() {
  ForEach(this.icons, (icon: Resource) => {
    Image(icon).width(24)
  })
}
.width('100%')
.justifyContent(FlexAlign.SpaceEvenly)
```

**layoutWeight**：每个子项设置相同权重，平分空间。

```typescript
Row() {
  ForEach(this.items, (item: Item) => {
    Column() { /* 内容 */ }.layoutWeight(1)
  })
}
```

### 6. 占比 (Proportion)

按照特定比例分配空间。

**layoutWeight**：按权重值分配剩余空间。

```typescript
Row() {
  Column() { /* 侧边栏 */ }.layoutWeight(1)
  Column() { /* 内容区 */ }.layoutWeight(3)  // 占3/4
}
```

**百分比宽高**：直接用百分比字符串设置尺寸。

```typescript
Row() {
  Column() { /* 侧边栏 */ }.width('30%')
  Column() { /* 内容区 */ }.width('70%')
}
```

### 7. 延伸 (Extension)

屏幕越大显示内容越多，通过可滚动容器实现。

**List**：自带滚动和按需加载，适合纵向延伸。

```typescript
List() {
  ForEach(this.items, (item: Item) => {
    ListItem() { /* 列表项 */ }
  })
}
```

**Scroll + Row/Column**：手动组合，适合横向延伸。

```typescript
Scroll() {
  Row() {
    ForEach(this.items, (item: Item) => {
      Column() { /* 卡片 */ }.width(160).margin({ right: 12 })
    })
  }
}
.scrollable(ScrollDirection.Horizontal)
```

---

## 注意事项

- `displayPriority` 只在父容器空间不足时才会隐藏子组件，空间充足时所有组件都会显示
- `Blank` 只能在 Flex/Row/Column 等弹性布局容器中使用
- `aspectRatio` 设置后高度由宽度和比例自动计算，不要再手动设置 height
- `layoutWeight` 在非弹性容器中不生效，需配合 Flex/Row/Column 使用
- 自适应布局不需要断点参与；需要断点切换页面结构的场景参考栅格布局（GridRow）和响应式布局
