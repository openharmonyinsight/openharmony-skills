# 小方形屏底部栏未收起导致主内容区被挤压案例

## 场景说明

页面主体由三块区域组成：

- 顶部用户信息区 `node592`
- 中间消息列表区 `node588`
- 底部导航区 `node599`

中间列表区通过 `RelativeContainer` 同时锚定在顶部区和底部区之间：

```typescript
.alignRules({
  top: { anchor: 'node592', align: VerticalAlign.Bottom },
  bottom: { anchor: 'node599', align: VerticalAlign.Top }
})
```

因此底部区只要存在过大的固定垂直占位，就会直接压缩中间列表区的可用高度。这里的占位不一定只来自 `.height(...)`，也可能来自：

- 上下 `padding`
- 上下 `margin`
- 额外包裹容器的固定高度
- 安全区或底部占位容器

## 正确案例

### 关键代码

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
    // ...
  }
  .width('100%')
  .clip(true)
  .height(this.getBarHeight())
}
.width('100%')
```

### 正确原因

`Goodcase.ets` 在小方形屏条件 `WIDTH_SM + HEIGHT_MD` 下，将底部导航主容器的核心占位收缩为 `0`，并通过 `.clip(true)` 截断内部内容。

结果是：

- 底部导航不再占据主布局高度
- 中间消息列表区得到更多可用空间
- 原本被底部区挤掉的组件可以显示出来

## 错误案例

### 问题代码

```typescript
Row() {
  Stack() {
    // ...
  }
  .width('100%')
  .height(64)
}
.width('100%')
.padding({ left: 12, right: 12, top: 8, bottom: 12 })
```

### 错误原因

`Index.ets` 保留了底部导航的固定垂直占位，没有根据小方形屏断点收起。

在这种布局里：

- `node599` 始终占据底部空间
- `node588` 的上下锚点间距被压缩
- 中间列表和分组内容区高度不足
- 小方形屏上会出现部分组件不显示或显示不全

## 最小根因

根因不是列表项本身，而是底部导航区没有在小方形屏下按断点消除多余的固定垂直占位，导致被它锚定的主内容区高度不足。

## 直接修复

将底部栏的固定垂直占位改为按断点动态收起：

```typescript
private getBarHeight(): number {
  if (this.currentWidthBreakpoint === WidthBreakpoint.WIDTH_SM &&
      this.currentHeightBreakpoint === HeightBreakpoint.HEIGHT_MD) {
    return 0;
  }
  return 100
}
```

并同步改为：

```typescript
.clip(true)
.height(this.getBarHeight())
```

如果外层还有额外垂直占位，也要一并检查并收起，例如：

```typescript
.padding({ top: 0, bottom: 0 })
```

或移除只在常规屏需要的固定高度包裹层。

## 通用结论

- 当中间内容区被上下锚点夹住时，底部栏是否仍占据固定垂直空间会直接影响主内容可见面积
- 小方形屏适配失败时，应优先检查底部固定栏、工具栏、导航栏是否仍保留常规屏的高度、padding、margin 或外层包裹占位
- 如果底部栏只需要在常规屏展示，在小方形屏下应根据断点尽量把这部分垂直占位收缩到最小，并配合 `.clip(true)`
