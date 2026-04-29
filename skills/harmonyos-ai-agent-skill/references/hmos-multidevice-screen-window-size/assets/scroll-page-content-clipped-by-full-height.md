# Scroll 页面内容被 `height('100%')` 锁死导致截断案例

## 场景说明

场景是一个密码输入页，页面主体内容高度超过小屏视口。

预期行为是：

- 小屏设备上页面可以纵向滚动
- 底部数字键盘和其他内容都能完整查看

## 正确案例

### 关键代码

```typescript
RelativeContainer() {
  Scroll() {
    Node4081Stack({ passcode: this.passcode })
  }
  .scrollable(ScrollDirection.Vertical)
  .scrollBar(BarState.Off)
  .alignRules({
    top: { anchor: '__container__', align: VerticalAlign.Top },
    left: { anchor: '__container__', align: HorizontalAlign.Start }
  })
  .width('100%')
  .height('100%')
}
```

同时，滚动内容内部容器不再强制占满父高度：

```typescript
Column() {
  ...
}
.width('100%')
.justifyContent(FlexAlign.Start)

Stack() {
  Node4083Column({ passcode: this.passcode })
}
.width('100%')
```

### 正确原因

这里把页面主体放进了 `Scroll`，由 `Scroll` 占满视口，高度超出的部分交给滚动容器处理。

同时内容树中的 `Stack` / `Column` 没有再写 `height('100%')`，因此它们会按真实内容高度撑开。内容高度大于视口时，`Scroll` 才能得到可滚动区域。

## 错误案例

### 问题代码

```typescript
RelativeContainer() {
  Node4081Stack({ passcode: this.passcode })
    .alignRules({
      top: { anchor: '__container__', align: VerticalAlign.Top },
      left: { anchor: '__container__', align: HorizontalAlign.Start }
    })
    .width('100%')
    .height('100%')
}
```

同时内容内部又被继续锁高：

```typescript
Column() {
  ...
}
.width('100%')
.height('100%')
.justifyContent(FlexAlign.Start)

Stack() {
  Node4083Column({ passcode: this.passcode })
}
.width('100%')
.height('100%')
```

### 错误原因

这里有两个会共同触发截断的问题：

- 页面主体没有放进 `Scroll`，超出视口后没有滚动承接
- 内容根节点和内部列容器都被写成 `height('100%')`，高度被锁定为视口高度，不能按内容继续增长

因此在小屏上：

- 页面内容超出后只能被裁掉
- 底部区域无法进入可见区域
- 用户无法通过滚动查看完整内容

## 直接修复

1. 将页面主体包进 `Scroll`
2. 删除滚动内容树上不必要的 `height('100%')`

可直接改成：

```typescript
RelativeContainer() {
  Scroll() {
    Node4081Stack({ passcode: this.passcode })
  }
  .scrollable(ScrollDirection.Vertical)
  .scrollBar(BarState.Off)
  .alignRules({
    top: { anchor: '__container__', align: VerticalAlign.Top },
    left: { anchor: '__container__', align: HorizontalAlign.Start }
  })
  .width('100%')
  .height('100%')
}
```

并把内容容器上的：

```typescript
.height('100%')
```

删除，让内容按实际高度撑开。

## 通用结论

- `Scroll` 应该负责占满视口，内容节点负责按内容高度自然撑开
- 如果内容本身也被写成 `height('100%')`，即使看起来“铺满页面”，在小屏下也容易把超出部分锁死并产生截断
- 对于可能超出一屏的页面，不要把滚动内容根节点和主列容器同时固定为全高
