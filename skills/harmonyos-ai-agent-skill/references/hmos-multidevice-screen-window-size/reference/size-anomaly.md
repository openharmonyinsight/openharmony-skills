# 尺寸异常修复指南

## 类别定义

**尺寸异常**是指组件的宽高尺寸在不同屏幕尺寸或设备类型上无法正确适配，导致显示效果异常的问题。

### 核心特征

- 组件的 `width` 或 `height` 值在多设备上不适配
- 组件出现截断（内容被切掉）或留白（空白区域过大）
- 问题通常与屏幕断点判断缺失或不当相关

### 常见现象

| 现象 | 描述 | 典型场景 |
|-----|------|---------|
| 组件截断 | 组件内容被裁剪，无法完整显示 | 小屏设备上固定高度的容器无法容纳所有内容 |
| 组件留白 | 组件周围出现不期望的空白区域 | 大屏设备上固定尺寸组件显得过小 |
| 尺寸溢出 | 组件超出父容器边界 | 子组件尺寸超过父容器限制 |
| 尺寸压缩 | 组件被强制压缩变形 | 空间不足时等比缩放导致变形 |

### 根因分类

1. **固定尺寸问题**：使用硬编码的像素值或固定百分比
2. **断点判断缺失**：未根据屏幕尺寸断点调整组件尺寸
3. **空间竞争问题**：多个组件争抢有限空间，导致相互挤压

---

## Bug 修复场景

### 场景 1：小方形屏底部栏未收起导致主内容区被挤压

#### 问题描述

在小方形屏设备上，底部导航栏或工具栏仍保持固定垂直占位，占用了主内容区的垂直空间，导致被上下锚点约束的中间内容区高度不足，出现组件不显示或显示不全。

#### 根因分析

固定占位不只包括 `.height(...)`，也可能来自：
- 上下 `padding` 和 `margin`
- 包裹层高度

```typescript
// 问题代码示例
Row() {
  Stack() {
    // bottom bar content
  }
  .width('100%')
  .height(100)  // 固定高度，未做断点判断
}
.width('100%')
```

#### 修复方案

对底部栏的垂直占位做断点判断；当设备为小宽度且中等高度这类小方形屏时，将底部栏主体高度及其附加垂直占位尽量收起，并启用裁剪避免内部内容外溢。

```typescript
@StorageLink('currentWidthBreakpoint') currentWidthBreakpoint: WidthBreakpoint = WidthBreakpoint.WIDTH_LG;
@StorageLink('currentHeightBreakpoint') currentHeightBreakpoint: HeightBreakpoint = HeightBreakpoint.HEIGHT_MD;

private getBarHeight(): number {
  if (this.currentWidthBreakpoint === WidthBreakpoint.WIDTH_SM &&
      this.currentHeightBreakpoint === HeightBreakpoint.HEIGHT_MD) {
    return 0;
  }
  return 100
}

Row() {
  Stack() {
    // bottom bar content
  }
  .width('100%')
  .clip(true)
  .height(this.getBarHeight())
}
.width('100%')

// 同时在小方形屏上移除额外的垂直占位
// 例如：条件性移除 top/bottom padding、margin、wrapper height
```

---

### 场景 2：内容超出父组件被截断/溢出显示

#### 问题描述

子组件的实际尺寸超出父容器的可显示区域，导致超出部分被截断不可见或溢出到父容器边界之外。

#### 根因分析

父容器无法容纳子组件的全部内容，可能是因为缺少滚动能力、容器高度约束不足等原因。

典型问题代码包括：

**问题 A：缺少 Scroll 容器**

可滚动页面的主体内容没有使用 `Scroll` 承接，或者 `Scroll` 内部的内容根节点被锁定了高度：

```typescript
// 问题代码
RelativeContainer() {
  Content()
    .width('100%')
    .height('100%')  // 问题：将内容高度锁死在视口高度
}
```

这样会把内容高度锁死在视口高度，超出部分既不能继续撑开，也无法形成正确的滚动区域。

**问题 B：使用非滚动容器渲染列表**

使用 `Row` / `Column` / `Stack` 等非滚动容器 + `ForEach` 渲染列表项：

```typescript
// 问题代码
Row({ space: 10 }) {
  ForEach(this.items, (item) => {
    Column() { /* 内容 */ }
  })
}
.width('60%')
```

这些容器不具备滚动延伸能力，当内容超出时会裁剪或溢出到屏幕外。

**问题 C：外部容器高度约束不足**

外部容器通过 `maxHeight`、`constraintSize({ maxHeight })`、`sheetMaxHeight` 等属性限制了最大高度，当内部内容的实际高度超过该限制时，超出部分被截断。

```typescript
// 问题代码：外部容器默认半屏高度，内部内容超过半屏被截断
ReDsActionSheetContent({
  slot: () => {
    this.renderUserCardDialog()  // 内容超过半屏，底部被截断
  },
  // sheetMaxHeight: '100%',  ← 未设置，使用默认半屏约束
})

// 外部容器组件内部通过 constraintSize 生效：
// .constraintSize({ maxHeight: this.sheetMaxHeight })
```

#### 修复方案

根据根因选择对应的修复方案：

**方案 A：使用 Scroll（适合单块整体内容）**

适用场景：页面主体内容是一个整体，需要滚动查看（如文章、表单、长图等）。

```typescript
// 修复后
RelativeContainer() {
  Scroll() {
    Content()  // 内容按自然高度布局
  }
  .width('100%')
  .height('100%')
  .scrollable(ScrollDirection.Vertical)  // 垂直滚动
  .scrollBar(BarState.Auto)
}

// 关键：删除 Content 上的 .height('100%')，让内容自然撑开
```

**方案 B：使用 List（适合多块同类内容）**

适用场景：内容由多个结构相同的列表项组成（如应用列表、图片网格、标签栏等）。

```typescript
// 修复后
List({ space: 10 }) {
  ForEach(this.items, (item) => {
    ListItem() {
      Column() { /* 内容 */ }
    }
  })
}
.listDirection(Axis.Horizontal)  // 横向滚动
.scrollBar(BarState.Auto)
.width('100%')
.height(118)  // List 必须设置明确的高度约束
```

**方案 C：调整外部容器高度约束（适合容器约束导致的截断）**

适用场景：外部容器通过 `maxHeight`、`constraintSize`、`sheetMaxHeight` 等限制了最大高度，内部内容超过该限制被截断。

典型表现：直播全屏模式下点击主播头像弹出用户资料卡，切回竖屏后，资料卡底部的「已关注」按钮被截断不可见。

```typescript
// 问题代码：未设置 sheetMaxHeight，使用默认半屏
ReDsActionSheetContent({
  // ...
  slot: () => {
    this.renderUserCardDialog()  // 内容超过半屏，底部被截断
  },
  // sheetMaxHeight: '100%',  ← 未设置，使用默认半屏约束
})

// 修复：显式设置 sheetMaxHeight 为 '100%'
ReDsActionSheetContent({
  // ...
  slot: () => {
    this.renderUserCardDialog()
  },
  sheetMaxHeight: '100%',  // 允许全屏高度，内容不再被截断
})
```

通用思路：当内部内容高度超过外部容器的 `maxHeight` 约束时，应调整外部容器的高度配置（增大 `maxHeight`、移除 `constraintSize` 限制、或设置百分比），而非在内部内容层做 padding/Scroll 绕过。此类问题容易误判为"缺少设备避让"，应先确认是容器高度约束不足还是避让缺失。

#### 方案选择指南

| 特征 | Scroll | List |
|-----|--------|------|
| **内容结构** | 单块整体内容 | 多个同类子项 |
| **子项类型** | 不统一（文字、图片、表单混合） | 统一（都是应用卡片、都是图片等） |
| **布局方向** | 主要是垂直滚动 | 垂直或横向滚动 |
| **典型场景** | 文章页面、表单、详情页 | 应用列表、图片网格、标签栏 |
| **性能** | 内容少时性能好 | 大量列表项时性能更好（虚拟化） |

**注意**：如果内容截断的原因是外部容器的 `maxHeight` / `constraintSize` / `sheetMaxHeight` 等高度约束不足（而非缺少滚动容器），应使用方案 C 调整容器高度约束，而非添加滚动容器。

**特殊情况**：如果列表项需要按二维网格排列（如图片网格），应使用 `Grid` 而非 `List`。

#### AI 判断规则

1. **首先识别截断根因**：
   - 如果是缺少滚动容器导致内容无法滑动查看，属于滚动问题（方案 A/B）
   - 如果是外部容器高度约束不足导致内容被裁剪，属于约束问题（方案 C）
   - 区分"容器高度约束不足"与"未做系统栏避让"两类根因：容器截断修正高度配置，避让缺失加 padding

2. **检查滚动容器问题**：
   - 如果页面在小屏上内容超过一屏，但主体内容没有由 `Scroll` 承接，优先补 `Scroll`
   - 如果已使用 `Scroll` 但滚动内容根节点设置了 `height('100%')`，优先判断为全高锁定问题
   - 如果使用 `Row` / `Column` + `ForEach` 渲染列表，且在小屏幕或悬浮窗场景下内容被截断，应替换为 `List` + `ListItem`

3. **检查外部容器高度约束问题**：
   - 当内容组件底部被截断时，**逐层检查外部容器的最大高度约束**（`sheetMaxHeight`、`maxHeight`、`constraintSize({ maxHeight })`），找到第一个限制过小的约束点
   - 如果外部容器有默认半屏或固定像素的高度限制，且内部内容可能超过该限制（如资料卡、设置面板、长表单），必须显式调整该约束值

---

### 场景 3：AlphabetIndexer 索引条在高度不足时紧凑挤压

#### 问题描述

在小高度设备或折叠屏上，`AlphabetIndexer` 的索引条变得非常紧凑，所有字母挤在有限垂直空间内，导致可读性差或交互困难。

#### 根因分析

`AlphabetIndexer` 设置了 `.autoCollapse(false)`，在可用高度不足时不会自动折叠索引项，导致所有字母索引始终显示，造成空间不足时紧凑挤压。

```typescript
// 问题代码示例
AlphabetIndexer({ arrayValue: this.dataSet, selected: 0 })
  .autoCollapse(false)  // 禁用自动折叠，高度不足时不会收起索引项
  .selectedColor(this.selectedColor)
  .popupSelectedColor(this.popupSelectedColor)
```

#### 修复方案

启用 `.autoCollapse(true)`，让索引条在高度不足时自动折叠部分索引项，保证显示效果。

```typescript
AlphabetIndexer({ arrayValue: this.dataSet, selected: 0 })
  .autoCollapse(true)  // 启用自动折叠
  .selectedColor(this.selectedColor)
  .popupSelectedColor(this.popupSelectedColor)
```

#### AI 判断规则

1. 如果页面使用了 `AlphabetIndexer` 且在小高度设备或折叠屏上索引条出现挤压、紧凑问题，优先检查 `.autoCollapse()` 是否为 `false`。

2. 除非索引条始终有充足高度保证，否则应默认使用 `.autoCollapse(true)`。

3. 在多设备适配场景下，启用自动折叠是更稳健的默认配置。

---

### 场景 4：flex 容器内子组件溢出截断，未按预期省略或保持完整

#### 问题描述

flex 容器（Row/Column/Flex）内子组件总尺寸超过父容器或屏幕可用空间，需要保证所有组件内容都在可视区域内完整展示（不被截断/裁剪），但实际上部分组件溢出被截断或被意外压缩。

#### 根因分析

子组件尺寸超过容器可用空间时，默认的 flexShrink 分配可能不符合开发者预期：

- 未显式设置 flexShrink 的子组件均参与等比收缩，无法精确控制谁被压缩、谁保持完整
- 容器本身缺少主轴尺寸约束（Row 需要 `.width`，Column 需要 `.height`）时，flexShrink 无法触发计算
- 结果：需要完整展示的组件被意外压缩或溢出裁剪，需要被压缩的组件反而没有让出空间

```typescript
// 问题代码示例（以 Row 为例，Column/Flex 同理）
Row() {
  Text(this.nick_name)
    .maxLines(1)
    .textOverflow({ overflow: TextOverflow.Ellipsis })
    // 缺少 .flexShrink(1)
  Row() {
    Image(...)
    Text("标签")
  }
  // 缺少 .flexShrink(0)
}
// 缺少 .width('100%')
```

#### 修复方案

对可以被压缩的子组件设置 `.flexShrink(1)`，对需要保持完整展示的子组件设置 `.flexShrink(0)`，并确保 flex 容器设置了主轴尺寸约束。

```typescript
// 修复后
Row() {
  Text(this.nick_name)
    .maxLines(1)
    .textOverflow({ overflow: TextOverflow.Ellipsis })
    .flexShrink(1)           // 允许压缩，配合省略号
  Row() {
    Image(...)
    Text("标签")
  }
  .flexShrink(0)             // 保持完整，不被压缩
}
.width('100%')                // 提供主轴约束边界（Column 对应 .height('100%')）
```

#### AI 判断规则

1. 如果 flex 容器（Row/Column/Flex）内子组件超出父容器或屏幕可用空间，且需要保证所有组件完整展示，必须显式设置 `.flexShrink()` 来分配压缩优先级：可以被压缩的组件设 `.flexShrink(1)`，需要完整展示的组件设 `.flexShrink(0)`。
2. 如果子组件超出可视区被截断，检查 flex 容器是否缺少主轴尺寸约束（Row → `.width`，Column → `.height`）。
3. 确保只有需要被压缩的子组件设置 `.flexShrink(1)`，其余设置 `.flexShrink(0)`，避免不需要压缩的组件被意外压缩。

---

### 场景 5：宽屏设备页面居中显示导致两侧出现黑色留白

#### 问题描述

在宽屏设备（平板、折叠屏展开态）上，页面内容被约束为固定宽高比（如手机比例 9:19.5），在屏幕中央显示，两侧或上下出现大面积黑色留白（来自外层容器的背景色），页面未能铺满整个屏幕。

#### 根因分析

内容容器使用了 `.aspectRatio()` 强制约束宽高比，而非让内容自适应填满可用空间。当屏幕宽高比与容器设定的宽高比不一致时，容器无法铺满屏幕，剩余区域显示外层背景色（通常为黑色）。

```typescript
// 问题代码示例
build() {
  Column() {
    Column() {
      // 页面内容
    }
    .height('100%')
    .aspectRatio(this.isNarrowScreen ? 1 : 9 / 19.5)  // 强制宽高比，宽屏上宽度不足
  }
  .width('100%')
  .height('100%')
  .backgroundColor('#000')  // 外层黑色背景，露出黑边
}
```

`.aspectRatio()` 会在保持指定比例的前提下，在可用空间内按最大适配计算实际尺寸。当父容器宽度远大于按宽高比计算出的内容宽度时，两侧出现留白。

#### 修复方案

移除内容容器的 `.aspectRatio()` 约束，改为显式设置 `.width('100%')` 和 `.height('100%')`，让内容自适应填满整个屏幕空间。

```typescript
// 修复后
build() {
  Column() {
    Column() {
      // 页面内容
    }
    .width('100%')   // 宽度铺满
    .height('100%')  // 高度铺满
  }
  .width('100%')
  .height('100%')
  .backgroundColor('#000')
}
```

如果需要在宽屏上对内容区域做最大宽度限制（如限制为 sm 断点宽度），应使用 `.constraintSize({ maxWidth: ... })` 而非 `.aspectRatio()`，这样内容仍然可以在垂直方向填满屏幕。

#### AI 判断规则

1. 如果宽屏设备上页面两侧或上下出现与外层背景色一致的大面积留白，优先检查内容容器是否使用了 `.aspectRatio()` 强制约束宽高比。
2. `.aspectRatio()` 适用于图片、视频等固定比例内容，不适用于页面级别的整体布局容器。
3. 如果需要限制内容在宽屏上的最大宽度，应使用 `.constraintSize({ maxWidth: ... })` 配合居中对齐，而非通过宽高比间接控制宽度。

---

### 场景 6：屏幕旋转后自定义键盘等组件宽度未更新导致截断

#### 问题描述

自定义键盘等组件的宽度基于窗口尺寸动态计算并存储在状态变量中，当设备旋转（横屏→竖屏）时，组件宽度未随窗口尺寸变化而更新，仍保持旋转前的宽屏宽度，导致组件右侧超出可视区域被截断。

#### 根因分析

组件在 `aboutToAppear` 中通过 `window.getWindowProperties().windowRect` 获取初始窗口尺寸并计算宽度，同时注册了 `windowSizeChange` 回调监听旋转等窗口变化事件。但回调中只更新了横竖屏标记（`isLandscape`），未同步更新宽度状态变量（`keyboardWidth`）。旋转后 `keyboardWidth` 仍保持横屏值（如 800vp），而实际屏幕宽度已缩小为竖屏值（如 360vp），父容器 `.clip(true)` 将超出的部分裁剪掉。

```typescript
@State keyboardWidth: number = 0

aboutToAppear() {
  window.getLastWindow(this.getUIContext().getHostContext()).then((win: window.Window) => {
    let rect: window.Rect = win.getWindowProperties().windowRect
    this.keyboardWidth = this.getUIContext().px2vp(rect.width)

    this.windowSizeCallback = (data: window.Size) => {
      this.isLandscape = data.width > data.height
      // BUG: keyboardWidth 未在回调中更新
      // 横屏(800vp) -> 竖屏(360vp)，keyboardWidth 仍为 800vp
    }
    win.on('windowSizeChange', this.windowSizeCallback)
  })
}

build() {
  Stack() {
    Column() {
      // 键盘按键行
    }
    .width(this.keyboardWidth)  // 使用过期的横屏宽度
  }
  .width('100%')
  .clip(true)                   // 超出部分被裁剪
}
```

#### 修复方案

在 `windowSizeChange` 回调中同步更新所有依赖窗口尺寸的状态变量，确保旋转后组件宽度与实际窗口宽度一致。

```typescript
this.windowSizeCallback = (data: window.Size) => {
  this.isLandscape = data.width > data.height
  this.keyboardWidth = this.getUIContext().px2vp(data.width)  // 同步更新宽度
}
```

#### AI 判断规则

1. 如果组件在屏幕旋转后出现截断或尺寸异常，且组件宽度来源于窗口尺寸的状态变量，优先检查 `windowSizeChange` 回调中是否同步更新了该状态变量。
2. 回调中需要同步更新的不只是横竖屏标记，所有从 `windowRect` / `window.Size` 派生的尺寸状态变量（宽度、高度等）都必须在回调中重新计算赋值。
3. 此模式不仅限于自定义键盘，任何通过 `windowSizeChange` 监听窗口变化并根据窗口尺寸动态设置组件宽高的场景都适用。

---

## AI 判断规则

1. 如果页面主内容区通过 `RelativeContainer`、`Stack` 或其他布局被顶部区和底部区同时约束，先检查底部区是否保留固定垂直占位，不要只看 `.height(...)`。

2. 如果问题只出现在小方形屏、方屏或短高度设备，优先检查是否缺少基于 `currentWidthBreakpoint` 和 `currentHeightBreakpoint` 的高度分支。

3. 继续检查底部区的上下 `padding`、`margin`、包裹层高度是否仍在小屏保留。

4. 如果底部栏在小屏不应展示完整功能，应优先收起底部栏占位，而不是先压缩中间列表项。

5. 当主体高度收起为 `0` 时，底部栏内容容器应配合 `.clip(true)`，避免内部子组件继续占据视觉空间。

6. **检查内容截断根因**：内容被截断时，按以下顺序排查：
   - **缺少滚动容器**：单块整体内容使用 `Scroll`，多块同类内容使用 `List`
   - **外部容器高度约束不足**：逐层检查 `maxHeight`、`constraintSize`、`sheetMaxHeight` 等约束，找到限制过小的约束点并调整
   - 注意区分"容器高度约束不足"与"未做系统栏避让"两类根因

7. **检查旋转后尺寸状态同步**：如果组件在屏幕旋转后出现截断，且组件宽高通过状态变量存储并绑定到布局属性上，检查 `windowSizeChange` 回调中是否同步更新了所有从窗口尺寸派生的状态变量（宽度、高度等），而非仅更新横竖屏标记。


