# 安全区域API完全指南

## 目录

1. [概述](#概述)
2. [API 参考](#api-参考)
3. [基本用法](#基本用法)
4. [常见问题](#常见问题)
5. [最佳实践](#最佳实践)

---

## 概述

安全区域 (Safe Area) 是指应用可以安全放置内容而不会被系统 UI 遮挡的区域。

### 安全区域 vs 避让区域

- **避让区域**: 系统占用的区域（状态栏、导航栏等）
- **安全区域**: 除去避让区域后的可用区域

---

## API 参考

### expandSafeArea 语法

```typescript
.expandSafeArea(types?: SafeAreaType[], edges?: SafeAreaEdge[])
```

**参数说明：**
- **types**: 要扩展的安全区域类型数组
- **edges**: 要扩展的边缘数组

### SafeAreaType 枚举

| 类型 | 说明 |
|-----|------|
| SYSTEM | 系统安全区域（状态栏、导航栏） |
| CUTOUT | 挖孔区域 |
| KEYBOARD | 软键盘区域 |

### SafeAreaEdge 枚举

| 边缘 | 说明 |
|-----|------|
| TOP | 顶部边缘 |
| BOTTOM | 底部边缘 |
| LEFT | 左侧边缘 |
| RIGHT | 右侧边缘 |

---

## 基本用法

### 背景色延伸

外层容器使用 `expandSafeArea` 延伸背景，内层使用 `padding` 保持内容在安全区域内：

```typescript
Column() {
  Column() {
    Text('标题')
      .fontSize(24)
      .fontWeight(FontWeight.Bold)

    Text('内容区域')
      .margin({ top: 16 })
  }
  .padding(16)
  .width('100%')
}
.width('100%')
.height('100%')
.backgroundColor('#007AFF')
.expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP, SafeAreaEdge.BOTTOM])
```

### 图片延伸

使用 Stack 分层：背景图片延伸到安全区域，内容层保持 padding：

```typescript
Stack() {
  Image($r('app.media.banner'))
    .width('100%')
    .height('100%')
    .objectFit(ImageFit.Cover)
    .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP])

  Column() {
    Text('标题')
      .fontSize(24)
      .fontColor(Color.White)

    Blank()

    Text('底部内容')
      .fontColor(Color.White)
  }
  .width('100%')
  .height('100%')
  .padding({ top: 48, bottom: 32, left: 16, right: 16 })
}
```

> **完整示例：** [BackgroundImmersiveExample.ets](../assets/BackgroundImmersiveExample.ets) — 使用 Stack + Image + expandSafeArea 实现背景图片沉浸式延伸、内容层保持 padding 避让的完整页面实现。

### 列表背景色延伸到底部

外层 Column 延伸背景，底部按钮不延伸，保持可见：

```typescript
Column() {
  List() {
    ForEach([1, 2, 3, 4, 5], (item: number) => {
      ListItem() {
        Text(`列表项 ${item}`)
          .width('100%')
          .height(60)
          .backgroundColor(Color.White)
          .borderRadius(8)
          .margin({ bottom: 8 })
      }
    })
  }
  .width('100%')
  .layoutWeight(1)
  .padding(16)

  Button('确认')
    .width('90%')
    .margin({ bottom: 16 })
}
.width('100%')
.height('100%')
.backgroundColor('#F5F5F5')
.expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.BOTTOM])
```

### 挖孔区延伸

使用 `SafeAreaType.CUTOUT` 扩展到挖孔区域：

```typescript
Column() {
  Text('内容')
}
.width('100%')
.height('100%')
.backgroundColor('#FF9500')
.expandSafeArea([SafeAreaType.CUTOUT], [SafeAreaEdge.TOP])
```

> 详细的挖孔避让方案请参阅 [avoid_area_types.md — 挖孔区/刘海](./avoid_area_types.md#挖孔区刘海)。

### 根据内容类型决定是否延伸

```typescript
// 可交互元素 - 不应延伸到安全区域
Button('确认')
   .fontSize(16)

// 纯展示元素 - 可以延伸
Image($r('app.media.background'))
  .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP])
```

---

## 常见问题

### Q: expandSafeArea 不生效？
确保:
1. 组件有设置背景色或背景图
2. 组件的父容器允许扩展
3. 没有其他 padding/margin 限制

### Q: 内容被遮挡？
使用两层结构: 外层 expandSafeArea 延伸背景，内层 padding 保持内容在安全区域内。

### Q: 如何处理键盘？
软键盘避让推荐使用 `KeyboardAvoidMode` 或监听 `avoidAreaChange`，详见 [keyboard_handling.md](./keyboard_handling.md)。`expandSafeArea` 的 `SafeAreaType.KEYBOARD` 适用于需要背景延伸到键盘区域的场景。

---
