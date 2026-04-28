# 响应式布局指南

## 目录

1. [核心概念](#核心概念)
2. [四种响应式布局](#四种响应式布局)

---

## 核心概念

### 响应式布局简介

- 响应式布局即页面根据不同屏幕尺寸自动调整布局，是页面在各种设备，各种尺寸的屏幕上都有良好的UI体验。
- 响应式布局的基础是断点（参考[断点系统完全指南](./breakpoint_system.md)）,通过断点的变化来调整布局。
- 响应式布局有重复布局，分栏布局，挪移布局和缩进布局等具体的布局方式

### 关键属性/API

| 属性/API | 说明 | 适用能力 |
|---------|------|---------|
| `lanes` | 设置List组件的布局列数或行数（List垂直滚动时表示列数，水平滚动时表示行数） | 重复布局 |
| `space` | List组件的子组件主轴方向的间隔。 | 重复布局 |
| `columnsTemplate` | 设置当前网格布局列的数量、固定列宽或最小列宽值，不设置时默认1列。 | 重复布局 |
| `displayCount` | 设置Swiper组件视窗内元素显示个数 | 重复布局 |
| `prevMargin` | 设置Swiper组件前边距，用于露出前一项的一小部分 | 重复布局 |
| `nextMargin` | 设置Swiper组件后边距，用于露出后一项的一小部分 | 重复布局 |
| `showSideBar` | 设置SideBarContainer组件是否显示侧边栏 | 分栏布局 |
| `sideBarWidth` | 设置SideBarContainer组件侧边栏的宽度 | 分栏布局 |
| `mode`(Navigation) | 设置导航页的显示模式，支持单栏（Stack）、分栏（Split）和自适应（Auto） | 分栏布局，挪移布局 |
| `columns`(GridRow) | 设置GridRow在不同断点下的布局列数 | 挪移布局，缩进布局 |
| `span`(GridCol) | 设置栅格子组件GridCol占用栅格容器组件GridRow的列数 | 挪移布局，缩进布局 |

---

## 四种响应式布局

### 一、重复布局（4个场景）

重复布局是指在空间充足时，重复使用相同或相似的结构、组件或排列方式，用以展示更多内容、保持视觉一致性并提高用户体验。常用的重复布局包括列表布局、瀑布流布局、轮播布局和网格布局。

#### 1. 列表布局（List + 断点）

列表布局基于横向断点，动态调整列数以实现重复布局。
具体方案：设置不同横向断点下，List组件的lanes、space属性实现目标效果。

```typescript
List({
  space: new WidthBreakpointType(8, 12, 16, 16).getValue(this.mainWindowInfo.widthBp),
  scroller: this.listScroller
}) {
  // ...
}
.scrollBar(BarState.Off)
.lanes(new WidthBreakpointType(1, 2, 3, 3).getValue(this.mainWindowInfo.widthBp), 12)
```
#### 2. 瀑布流布局（WaterFlow + 断点）

瀑布流布局基于横向断点，动态控制列数以实现重复布局。
具体方案：设置不同横向断点下，WaterFlow组件的columnsTemplate属性实现目标效果。

```typescript
WaterFlow() {
  LazyForEach(this.dataSource, (item: number, index: number) => {
    FlowItem() {
      Row() {}
      .width('100%')
      .height('100%')
      .borderRadius(16)
      .backgroundColor('#F1F3F5')
    }
    .width('100%')
    .height(this.itemHeightArray[index])
  }, (item: number, index: number) => JSON.stringify(item) + index)
}
.columnsTemplate(`repeat(${new WidthBreakpointType(2, 3, 4, 4).getValue(this.mainWindowInfo.widthBp)}, 1fr)`)
.columnsGap(12)
.rowsGap(12)
.width('100%')
```
#### 3. 轮播布局（Swiper + 断点）

轮播布局基于横向断点，动态控制视窗内显示元素的个数以实现重复布局。
具体方案：设置不同横向断点下，Swiper组件的displayCount、prevMargin、nextMargin和indicator属性实现目标效果。

```typescript
Swiper() {
  // ...
}
.displayCount(new WidthBreakpointType(1, 2, 3, 3).getValue(this.mainWindowInfo.widthBp))
// Setting the navigation point Style of the swiper.
.indicator(this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_SM ? Indicator.dot()
  .itemWidth(6)
  .itemHeight(6)
  .selectedItemWidth(12)
  .selectedItemHeight(6)
  .color('#4DFFFFFF')
  .selectedColor(Color.White) : false
)
// The sizes of the front and rear banners on the MD and LG devices are different.
.prevMargin(new WidthBreakpointType(0, 12, 64, 64).getValue(this.mainWindowInfo.widthBp))
.nextMargin(new WidthBreakpointType(0, 12, 64, 64).getValue(this.mainWindowInfo.widthBp))
```
#### 4. 网格布局（Grid + 断点）

网格布局基于横向断点，动态控制列数/行数以实现重复布局。
具体方案：设置不同横向断点下，Grid组件的columnsTemplate属性实现目标效果。在不设置Grid组件行数的情况下，行数 = 展示元素数量 / 列数。

```typescript
Grid() {
  ForEach(this.infoArray.slice(new WidthBreakpointType(4, 2, 0, 0).getValue(this.mainWindowInfo.widthBp)),
    (item: number) => {
      // ...
    }, (item: number, index: number) => JSON.stringify(item) + index)
}
.width('100%')
.columnsTemplate(`repeat(${new WidthBreakpointType(2, 3, 4, 4).getValue(this.mainWindowInfo.widthBp)}, 1fr)`)
.columnsGap(12)
.rowsGap(12)
```

### 二、分栏布局（6个场景）

分栏布局是指在空间充足时，将窗口划分为两栏或三栏，用于展示多类内容。常见的分栏布局包括侧边栏、单/双栏和三分栏。

#### 1. 侧边栏（SideBarContainer + 断点）

侧边栏基于横向断点，动态控制侧边栏是否显示，实现二分栏布局。
具体方案：在不同横向断点下，动态控制SideBarContainer组件的showSideBar和sideBarWidth属性实现目标效果。

```typescript
SideBarContainer(this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_SM ? SideBarContainerType.Overlay :
  SideBarContainerType.Embed) {
  Column() {
    // ...
  }
  .backgroundColor('#F1F3F5')

  Column() {
    // ...
  }
  .backgroundColor('#FDBFFC')
  .padding({
    top: this.getUIContext().px2vp(this.mainWindowInfo.AvoidSystem?.topRect.height) + 12,
    bottom: this.getUIContext().px2vp(this.mainWindowInfo.AvoidNavigationIndicator?.bottomRect.height),
    left: 16,
    right: 16
  })
}
.showSideBar(this.isShowingSidebar)
.sideBarWidth(new WidthBreakpointType('80%', '50%', '40%', '40%').getValue(this.mainWindowInfo.widthBp))
.controlButton({ top: this.getUIContext().px2vp(this.mainWindowInfo.AvoidSystem?.topRect.height) + 12 })
```

#### 2. 单/双栏（Navigation + 断点）

单/双栏基于横向断点，动态控制导航栏的显示模式，实现二分栏布局。
具体方案: 设置不同横向断点下，Navigation组件的mode属性实现目标效果。

```typescript
Navigation(this.pathStack) {
  // ...
}
.mode(this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_SM ? NavigationMode.Stack : NavigationMode.Split)
```

#### 3. 二分栏典型场景——聊天（Navigation 双栏路由切换）

某些应用在双栏布局下支持通过右侧内容区链接跳转至其扩展页面并单栏展示。以社交应用为例，在横向断点为md、lg和xl时，左侧导航栏为聊天列表，右侧内容区显示聊天框，包括文字信息和商品链接；当用户在右侧点击商品链接时，可进入单栏模式，全屏展示对应的商品扩展区页面，同时隐藏原聊天页，实现沉浸式浏览体验。

```typescript
@Builder
PageMap(name: string) {
  if (name === 'conversationDetail') {
    ConversationDetail({
      // ...
    })
  } else if (name === 'conversationDetailNone') {
    ConversationDetailNone();
  } else if (name === 'productPage') {
    ProductPage({
      // ...
    })
  }
}

build() {
  Navigation(this.pathStack) {
    ConversationNavBarView({
      mainWindowInfo: this.mainWindowInfo,
      pageInfos: this.pageInfos,
      pathStack: this.pathStack,
    })
  }
  .mode(this.getNavMode())
  // ...
  .navDestination(this.PageMap)
}

getNavMode(): NavigationMode {
  if (!this.isNavFullScreen && this.mainWindowInfo.widthBp !== WidthBreakpoint.WIDTH_SM) {
    return NavigationMode.Split;
  }
  return NavigationMode.Stack
}
```

#### 4. 三分栏（SideBarContainer + Navigation + 断点）

三分栏基于横向断点，动态控制导航栏的显示模式和侧边栏是否显示，实现三分栏布局。
具体方案：在不同横向断点下，动态控制SideBarContainer组件的showSideBar、sideBarWidth属性，和Navigation组件的mode、navBarWidth属性实现目标效果。

```typescript
SideBarContainer(new WidthBreakpointType(SideBarContainerType.Overlay, SideBarContainerType.Overlay,
  SideBarContainerType.Embed, SideBarContainerType.Embed).getValue(this.mainWindowInfo.widthBp)) {
  Column() {
    // ...
  }
  // ...

  Column() {
    Navigation(this.pathStack) {
      NavigationBarView({
        mainWindowInfo: this.mainWindowInfo,
        pageInfos: this.pageInfos,
        pathStack: this.pathStack,
        isShowingSidebar: this.isShowingSidebar,
        isTriView: true
      })
    }
    .width('100%')
    .height('100%')
    .mode(this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_SM ? NavigationMode.Stack : NavigationMode.Split)
    .navBarWidth(this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_MD ? '50%' : '40%')
    .navDestination(this.PageMap)
    .backgroundColor('#B8EEB2')
  }
  // ...
}
.showSideBar(this.isShowingSidebar)
.sideBarWidth(new WidthBreakpointType('80%', '50%', '20%', '20%').getValue(this.mainWindowInfo.widthBp))
```

#### 5. 三分栏典型场景——邮箱（账户/收件箱/详情）

在邮箱场景中，单栏状态下，默认展示收件箱页，当选择邮件对象后，展示邮件详情页。双栏和三栏状态下，右侧默认不展示邮件详情页，当选择邮件对象后，右侧展示邮件详情页。

具体方案：对SideBarContainer组件的showSideBar属性进行赋值，如果横向断点为lg或xl，则默认显示侧边栏，反之，则默认不显示。
```typescript
build() {
  GridRow() {
    GridCol({ span: { sm: 12, md: 12, lg: 12, xl: 12 } }) {
      SideBarContainer(new WidthBreakpointType(SideBarContainerType.Overlay, SideBarContainerType.Overlay,
        SideBarContainerType.Embed, SideBarContainerType.Embed).getValue(this.mainWindowInfo.widthBp)) {
        // Area A
        Column() {
          MailSideBar()
        }
        .width('100%')
        .height('100%')
        .backgroundColor($r('sys.color.gray_01'))

        // Area B+C
        Column() {
          Stack() {
            MailNavigation({
              mainWindowInfo: this.mainWindowInfo,
              pageInfos: this.pageInfos,
              pathStack: this.pathStack,
            })
              .margin({ top: 18 })
              .padding({ left: this.getUIContext().px2vp(this.mainWindowInfo.AvoidSystem?.topRect.left) })
            // ...
          }
        }
        .width('100%')
        .height('100%')
      }
      .showSideBar(this.isShowingSidebar)
      // ...
    }
  }
  .width('100%')
  .height('100%')
}
```

在SideBarContainer组件内容区中使用Navigation组件，对Navigation组件的mode属性进行赋值，如果断点为sm或xs，则为单栏，反之则为双栏。

```typescript
build() {
  Navigation(this.pathStack) {
    // ...
  }
  .mode(this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_SM ? NavigationMode.Stack : this.notesNavMode)
  .navDestination(this.myRouter)
  // ...
}
```


#### 6. 三分栏典型场景——日历（单栏优先导航区）

在三分栏的单栏布局中，通常展示的重点是Navigation的内容区。但在某些场景下，内容区的优先级低于导航区，例如日历日程功能。在这种情况下，单栏布局会优先展示日历（即Navigation的导航区）。

```typescript
Row() {
  // ...

  if (this.mainWindowInfo.widthBp !== WidthBreakpoint.WIDTH_SM) {
    Column() {
      // ...
    }
    // ...
    .onClick(() => {
      if (this.navMode === NavigationMode.Split) {
        this.navMode = NavigationMode.Stack;
      } else if (this.navMode === NavigationMode.Stack && this.selectedItem.isTrip) {
        this.navMode = NavigationMode.Split;
      }
    })
  }
  // ...
Navigation(this.pathStack) {
  CalendarView({
    mainWindowInfo: this.mainWindowInfo,
    pathStack: this.pathStack,
  })
}
.navDestination(this.pageMap)
.mode(this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_SM ? NavigationMode.Stack : this.navMode)
// ...
.onNavigationModeChange((mode: NavigationMode) => {
  if (this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_SM || mode === NavigationMode.Stack) {
    this.pathStack.clear();
  } else if (mode === NavigationMode.Split) {
    this.pathStack.pushPath({ name: this.selectedItem.date, param: this.selectedItem }, false);
  }
})
```


### 三、挪移布局（2个场景）

挪移布局是指在空间充足时，通过调整组件的位置与展示方式，在左右布局与上下布局之间切换，用以展示更多内容或提高用户体验。常用的挪移布局包括插图和文字组合布局、底部/侧边导航。

#### 1. 插图和文字组合布局（GridRow/GridCol + 断点）

插图和文字组合布局基于横向断点，设置组件所占不同的栅格数，实现左右布局与上下布局的切换。
具体方案：设置不同横向断点下，GridRow组件的columns、breakpoints属性，和GridCol组件的span属性实现目标效果。

```typescript
GridRow({
  columns: { xs: 4, sm: 4, md: 8, lg: 12, xl: 12 },
  gutter: 0,
  breakpoints: { value: ['320vp', '600vp', '840vp', '1440vp']},
  direction: GridRowDirection.Row
}) {
  GridCol({
    span: { xs: 4, sm: 4, md: 4, lg: 4, xl: 4 },
    offset: 0
  }) {
    // ...
  }
  .height(this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_SM ? this.getGridColHeight() : '100%')
  .padding({ top: this.getUIContext().px2vp(this.mainWindowInfo.AvoidSystem?.topRect.height) + 12})
  .backgroundColor('#AAD3F1')

  GridCol({
    span: { xs: 4, sm: 4, md: 4, lg: 8, xl: 8 },
    offset: 0
  }) {
    // ...
  }
  .backgroundColor(Color.Pink)
  .layoutWeight(1)
  .padding({ top: this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_SM ? 0 :
    this.getUIContext().px2vp(this.mainWindowInfo.AvoidSystem?.topRect.height) })
}
```

#### 2. 底部/侧边导航（Tabs + 断点，xl/PC 可切 SideBarContainer）

底部/侧边导航基于横向断点，设置导航栏的位置与方向，实现上下布局与左右布局的切换。
具体方案: 设置不同横向断点下，Tabs组件的barPosition、vertical、barHeight、barWidth和barMode属性实现目标效果。

```typescript
Tabs({
  barPosition: this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_LG ? BarPosition.Start : BarPosition.End
}) {
  TabContent() {
    TopTabView({
      pageInfos: this.pageInfos,
      mainWindowInfo: this.mainWindowInfo,
      firstLevelIndex: this.firstLevelIndex,
      tabData: this.tabData
    })
  }
  .tabBar(this.tabBuilder(this.firstTabList[0], 0))

  TabContent()
    .tabBar(this.tabBuilder(this.firstTabList[1], 1))

  TabContent()
    .tabBar(this.tabBuilder(this.firstTabList[2], 2))

  TabContent()
    .tabBar(this.tabBuilder(this.firstTabList[3], 3))
}
.barBackgroundColor('#CCF1F3F5')
.barWidth(this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_LG ? 96 : '100%')
.barHeight(this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_LG ? '100%' : 56 + this.getUIContext().px2vp(this.mainWindowInfo.AvoidNavigationIndicator?.bottomRect.height))
.barMode(this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_LG ? BarMode.Scrollable : BarMode.Fixed,
  { nonScrollableLayoutStyle: LayoutStyle.ALWAYS_CENTER })
.barBackgroundBlurStyle(BlurStyle.COMPONENT_THICK)
.vertical(this.mainWindowInfo.widthBp === WidthBreakpoint.WIDTH_LG)
.onChange((index: number) => {
  this.firstLevelIndex = index;
})
```

### 四、缩进布局（1个场景）

缩进布局是指在空间充足时，组件居中展示并在两侧留白，通过调整内容的缩进来建立视觉层次结构，提高可读性和美观性。常用的缩进布局包括单列列表布局。

#### 1. 单列列表布局（GridRow/GridCol 的 span + offset）

单列列表布局基于横向断点，设置栅格子组件所占的栅格列数和偏移列数，实现缩进布局。
具体方案：设置不同横向断点下，GridRow组件的columns、breakpoints属性和GridCol组件的span、offset属性实现目标效果。

```typescript
GridRow({
  columns: { xs: 4, sm: 4, md: 8, lg: 12, xl: 12 },
  gutter: 0,
  breakpoints: { value: ['320vp', '600vp', '840vp', '1440vp']},
  direction: GridRowDirection.Row
}) {
  GridCol({
    span: { xs: 4, sm: 4, md: 6, lg: 8, xl: 8 },
    offset: { xs: 0, sm: 0, md: 1, lg: 2, xl: 2 }
  }) {
    // ...
  }
  .width('100%')
  .height('100%')
}
```