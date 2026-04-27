# 鼠标适配指南

## 目录

1. [鼠标操作](#鼠标操作)
2. [鼠标悬浮效果](#鼠标悬浮效果)

---

## 鼠标操作

### 左键点击

```typescript
// 使用onClick处理
Button('按钮')
  .onClick(() => {
    // onClick支持鼠标左键点击
  })
```

### 右键点击

```typescript
// 使用onMouse处理
Button('按钮')
  .onMouse((event) => {
    if (event.button === MouseButton.Right) { /* 鼠标右键点击 */ }
  })
```

### 右键菜单

### 使用 bindContextMenu

```typescript
@Entry
@Component
struct RightClickMenuExample {
  build() {
    Column() {
      Text('右键点击或长按打开菜单')
        .fontSize(16)
        .padding(16)
    }
    .width('100%')
    .height(200)
    .backgroundColor('#F5F5F5')
    .bindContextMenu(this.ContextMenu, ResponseType.LongPress)
    .bindContextMenu(this.ContextMenu, ResponseType.RightClick)
  }

  @Builder
  ContextMenu() {
    Menu() {
      MenuItem({ content: '刷新' })
        .onClick(() => console.log('刷新'))

      MenuItem({ content: '设置' })
        .onClick(() => console.log('设置'))

      MenuItem({ content: '关于' })
        .onClick(() => console.log('关于'))
    }
  }
}
```
---

## 鼠标悬浮效果

### 使用 hoverEffect

```typescript
@Entry
@Component
struct HoverEffectExample {
  build() {
    Column() {
      // 高亮效果
      Button('高亮效果')
        .hoverEffect(HoverEffect.Highlight)

      // 缩放效果
      Button('缩放效果')
        .hoverEffect(HoverEffect.Scale)

      // 无效果
      Button('无效果')
        .hoverEffect(HoverEffect.None)
    }
  }
}
```

### HoverEffect 枚举

| 效果 | 说明 |
|-----|------|
| Highlight | 背景高亮（默认） |
| Scale | 轻微缩放 |
| None | 无效果 |

### 自定义悬浮样式

```typescript
@Entry
@Component
struct CustomHoverExample {
  @State isHovered: boolean = false;

  build() {
    Column() {
      Text('自定义悬浮效果')
    }
    .width(200)
    .height(100)
    .backgroundColor(this.isHovered ? '#E8E8E8' : '#F5F5F5')
    .borderRadius(8)
    .onHover((isHover: boolean) => {
      this.isHovered = isHover;
    })
  }
}
```
---